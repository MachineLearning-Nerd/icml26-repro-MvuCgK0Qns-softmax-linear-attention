import torch
import torch.nn as nn
import torch.optim as optim
from typing import Optional
import numpy as np
import random
import os
import re
from utils.data_utils import DataMethod, LinearReg, find_latest_checkpoint
from src.models import MultiHeadAttention
from utils.config import Config
from tqdm import tqdm

def set_seed(seed=217):
    """Set seed for reproducibility."""
    random.seed(seed)  # Python random module
    np.random.seed(seed)  # NumPy
    torch.manual_seed(seed)  # PyTorch CPU
    torch.cuda.manual_seed(seed)  # PyTorch GPU
    torch.cuda.manual_seed_all(seed)  # PyTorch multi-GPU

    # Ensure deterministic behavior
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

def train_step(model, z_q, z, y_q, optimizer, loss_func):
    optimizer.zero_grad()
    output = model(z_q, z)
    loss = loss_func(output, y_q)
    loss.backward()
    optimizer.step()
    return loss.detach().item(), output.detach()


def validate_step(model, z_q, z, y_q, loss_func):
    output = model(z_q, z)
    loss = loss_func(output, y_q)      
    return loss.detach().item()

def run_experiment(config, path, verbose=False):
    """
    Run an experiment based on the given configuration.

    Parameters:
        config (Config): Configuration object containing experiment parameters.
        path (str): Path of directory to save checkpoints

    Returns:
        dict: Dictionary containing results of the experiment, including losses and dynamics.
    """
    # Device setup
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if verbose:
        print(f"Using device: {device}")
        print(config)

    activation_dict = {
        "softmax": nn.functional.softmax,
        "linear": None
    }
    
    # Directory to save logs
    os.makedirs(path, exist_ok=True)
    
    # initialize model
    model = MultiHeadAttention(
        n_embd = config.n_embd,
        n_head = config.n_head,
        n_out = config.n_out,
        bias = False,
        activation = activation_dict[config.activation],
        normalize = config.normalize
    )
    
    # initialize data generation method
    data_generation = LinearReg({
        "L": config.L,
        "dx": config.d,
        "dy": 1,
        "number_of_samples": config.batch_size,
        "noise_std": config.noise_std,
        "seed": config.seed,
        "covariance": config.covariance
    })
    
    # Initialize optimizer
    optimizer_dict = {
        "SGD": torch.optim.SGD,
        "Adam": torch.optim.Adam,
        "AdamW": torch.optim.AdamW
    }
    optimizer = optimizer_dict[config.method](model.parameters(), lr=config.learning_rate, **config.optimizer_params)
    
    training_steps = range(config.training_steps) # training iterations to run
    
    loaded_warm = False # True if we manage to load previous checkpoiint
    
    # find latest checkpoint if warm restart
    if config.warm:
        latest_path, latest_step = find_latest_checkpoint(path)
        
        if latest_step is not None: 
            if latest_step>=(config.training_steps // config.save_log_every_step) * config.save_log_every_step:
                print('Run already completed; no rerun.')
                return 

            # load latest_checkpoint model
            checkpoint = torch.load(latest_path, map_location=torch.device(device))
            model_head_1 = checkpoint['model']  # Assuming the model is saved under the key 'model'

            # Create the model architecture
            model.load_state_dict(model_head_1, strict=True)
            data_generation.rng.set_state(checkpoint["rng_state"]) # restore state of data generator for reproducibility
    
            loaded_warm = True
            training_steps = range(latest_step, config.training_steps)
            print(f"Warm restart from step {latest_step}.")

        elif config.activation=='linear':
            # initialize the linear weights so that they correspond to softmax weights
            try:
                path_s = re.sub(
                                    r"Activation_linear_",
                                    "Activation_softmax_",
                                    path,
                                    count=1
                                )
                # load latest softmax checkpoint model
                checkpoint_s = torch.load(path_s+"/step_0.pth", map_location=torch.device(device))
                model_head_1 = checkpoint_s['model']  # Assuming the model is saved under the key 'model'
                data_generation.rng.set_state(checkpoint_s["rng_state"]) # restore state of data generator for reproducibility

                # Create the model architecture
                model.load_state_dict(model_head_1, strict=True)
                print(f"Loaded initial weights of softmax model.")
            except Exception as e:
                #print(f"Failed to evaluate model for activation={activation} and L={L}. Error: {e}")
                print(f"Failed to initialize as softmax model.")
        else:
            print("Failed to initialize from any checkpoint.")

    model.to(device)  # Move model to device

    # Initialize loss function
    loss_func = torch.nn.MSELoss()
    
    # save initial state     
    result = {
            'training_loss': np.NAN,
            'config': config,
            'model': model.state_dict(),
            'step': 0,
            'rng_state': data_generation.rng.get_state(),
            'z_q': None,
            'z': None,
            'y_q': None
        }
    torch.save(result, path+f"/step_0.pth")

    if verbose:
        training_steps = tqdm(training_steps)

    # Training loop with tqdm for progress monitoring
    for step in training_steps:
        # Generate training data
        zs_q, zs, ys_q = data_generation.__generatedata__()   
        
        loss, _ = train_step(model, zs_q.to(device), zs.to(device), ys_q.to(device), optimizer, loss_func)
    
        # Update progress bar description
        if verbose and (step + 1) % config.loss_log_every_step == 0:
            training_steps.set_description(f"Training loss {loss:.4f}")
            
        # save current logs
        if (step +1) % config.save_log_every_step == 0:
            
            result = {
                'training_loss': loss,
                'config': config,
                'model': model.state_dict(),
                'step': step+1,
                'rng_state': data_generation.rng.get_state(),
                'z_q': zs_q,
                'z': zs,
                'y_q': ys_q
            }
            torch.save(result, path+f"/step_{step+1}.pth")

    print('Run ended')


if __name__ == "__main__":

    # single worker to avoid crashes
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)

    # Set seed
    seed = 327
    set_seed(seed)

    # other parameters for the run
    n_head, d = 1, 5
    method, learning_rate, batch_size, optimizer_params, training_steps = 'SGD', 0.001, 128, {}, 300000
    rho = 0.5 # parameter for KCM covariance structure
    covariance = f"KCM {rho}"
    noise_std = np.sqrt(0.1)
    save_log_every_step = 1000
    warm = False
    normalize = True

    print(f"Running with:\n"
                f"  n_head: {n_head}\n"
                f"  d: {d}\n"
                f"  method: {method}\n"
                f"  learning_rate: {learning_rate}\n"
                f"  batch_size: {batch_size}\n"
                f"  noise_std: {noise_std}\n"
                f"  optimizer_params: {optimizer_params}\n"
                f"  training_steps: {training_steps}\n"
                f"  save_log_every_step: {save_log_every_step}\n"
                f"  warm: {warm}\n"
                f"  normalize: {normalize}\n"
                f"  seed: {seed}\n"
                f"  covariance: {covariance}\n"
                f")")

	# list of activation and L to run
    activation_ls = ['softmax', 'linear']
    L_ls = [*range(10, 100, 10), *range(100, 1001, 100)]

    for L in L_ls:
        for activation in activation_ls:
            config = Config(n_head=n_head, n_out=1, d=d, method=method,
                              L=L,
                              learning_rate=learning_rate, training_steps=training_steps, batch_size=batch_size, 
                              save_log_every_step=save_log_every_step, optimizer_params=optimizer_params, noise_std=noise_std, 
                              activation=activation, warm=warm, seed=seed, normalize=normalize, covariance = covariance)
            
            print(f"Running with activation {activation} and L={L}...")
            # Create the "saved_models" directory if it doesn't exist
            os.makedirs("saved_models", exist_ok=True)
            os.makedirs(f"saved_models/{covariance}", exist_ok=True)
            
            # Save the model in the "saved_models" directory
            log_path = f"saved_models/{covariance}/Activation_{activation}_L_{L}_d_{d}"

            run_experiment(config, log_path, verbose=True)

