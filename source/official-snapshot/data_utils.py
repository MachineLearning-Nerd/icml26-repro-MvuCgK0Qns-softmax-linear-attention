import torch
import numpy as np
import re
import os
from typing import Any, Dict, Optional

class DataMethod:
    def __init__(self, dict: Dict = None):
        self.dict = dict if dict is not None else {}
        self.seed = self.dict.get('seed', None)
        # Create a local generator for reproducible random numbers
        self.rng = torch.Generator()
        if self.seed is None:
            self.seed = np.random.randint(1024)
        self.rng.manual_seed(self.seed)


    def __generatedata__(self, **kwargs) -> Any:
        """
        This method generates synthetic data based on specified sequence length and dimension.

        Parameters:
            kwargs: Additional keyword arguments (not used here but allows for flexible method signature).

        Returns:
            torch.Tensor: Generated data tensor with shape (seq_len, dim).
        """
        # Retrieve the sequence length and dimension from the dictionary (with default values if not provided).
        seq_len = self.dict.get("seq_length", 100)
        dim = self.dict.get("dimension", 10)
        # Generate a tensor with random values sampled from a standard normal distribution.
        x = torch.randn(seq_len, dim, generator=self.rng)
        return x

    def __transform__(self, x: Any, **kwargs) -> Any:
        """
        This method transforms input data for training, validation, or testing purposes.

        Parameters:
            x (torch.Tensor): Input tensor with shape (batch_size, seq_len, dim).

        Returns:
            Tuple[torch.Tensor, torch.Tensor]: A tuple containing:
                - x: The input tensor excluding the last time step (shape: batch_size, seq_len - 1, dim).
                - y: The corresponding target tensor excluding the first time step (shape: batch_size, seq_len - 1, dim).
        """
        # Create a target tensor by removing the first element along the sequence dimension.
        y = x[..., 1:, :].clone()
        # Trim the input tensor to remove the last element along the sequence dimension.
        x = x[..., :-1, :]
        return x, y

def find_latest_checkpoint(directory):
    """
    Find latest checkpoint inside the directory for warm restart.
        
        Parameters:
            str: Path to directory where checkpoints are saved.

        Returns:
            str, int: path to latest checkpoint, latest step saved
    """
    pattern = re.compile(r"step_(\d+)\.pth")
    steps = []
    try:
        for fname in os.listdir(directory):
            match = pattern.match(fname)
            if match:
                steps.append(int(match.group(1)))
        if not steps:
            return None, None
        latest_step = max(steps)
        latest_path = os.path.join(directory, f"step_{latest_step}.pth")
    except:
        return None, None
    return latest_path, latest_step

def generate_covariance_matrix(d, rho=0.5):
    """
    Generate a d by d covariance matrix where each entry is given by rho^|i-j|,
    and return the covariance matrix along with its eigenvalues.

    Parameters:
        d (int): Dimension of the covariance matrix.
        rho (float): Correlation coefficient, where -1 < rho < 1.

    Returns:
        tuple: A tuple containing the covariance matrix (numpy.ndarray) and its eigenvalues (numpy.ndarray).
    """
    if not (-1 < rho < 1):
        raise ValueError("rho must be between -1 and 1 (exclusive).")

    # Create the covariance matrix
    covariance_matrix = np.zeros((d, d))
    for i in range(d):
        for j in range(d):
            covariance_matrix[i, j] = rho ** abs(i - j)

    # Compute the eigenvalues
    eigenvalues = np.linalg.eigvalsh(covariance_matrix)

    return covariance_matrix, eigenvalues

class LinearReg(DataMethod):
    """
    This class generates data for a linear regression task based on specific parameters, 
    such as data size, sequence length, noise level, and condition number of the covariance matrix.
    """

    def __init__(self, dict: Dict = None):
        """
        Initialize the LinearReg class with a set of parameters.

        Parameters:
            dict (Dict): Dictionary containing parameters for data generation.
        """
        # Call the parent class initializer.
        super().__init__(dict)
        # Extract parameters for data generation.
        self.L = dict['L']  # Sequence length
        self.dx = dict['dx']  # Input dimension
        self.dy = dict['dy']  # Output dimension
        self.noise_std = dict['noise_std']  # Standard deviation of the noise
        self.number_of_samples = dict['number_of_samples']  # Number of data samples
        rho = parse_kcm(dict['covariance'])
        if rho is None:
            self.covariance = None
            self.covariance_root = None
        else:
            self.covariance, _ = generate_covariance_matrix(self.dx, rho=rho)
            self.covariance = torch.from_numpy(self.covariance).to(torch.float32)
            self.covariance_root = torch.linalg.cholesky(self.covariance)


    def __generatedata__(self, **kwargs) -> Any:
        """
        Generate linear regression data.

        Parameters:
            kwargs: Additional keyword arguments (not used here).

        Returns:
            Tuple: Generated data tensors (z_q, z, y_q).
        """
        # Generate input data with shape (n, L, dx).
        x = torch.randn(self.number_of_samples, self.L, self.dx, generator=self.rng)
        if self.covariance is not None:
          x  = x @ self.covariance_root.T                       

        # Generate query data (single time-step data) with shape (n, 1, dx).
        x_q = torch.randn(self.number_of_samples, 1, self.dx, generator=self.rng)
        if self.covariance is not None:
          x  = x @ self.covariance_root.T         

        # Generate regression coefficients (beta) with shape (n, dx, dy).
        beta = torch.randn(self.number_of_samples, self.dx, self.dy, generator=self.rng) * torch.sqrt(torch.tensor(1/self.dx))
        
        # Generate target output data y with shape (n, L, dy) using x and beta.
        y = torch.einsum('nlx,nxy->nly', x, beta)
        # Add Gaussian noise to the output y.
        #y += math.sqrt(self.dx) * self.noise_std * torch.randn(self.number_of_samples, self.L, self.dy)
        y += self.noise_std * torch.randn(self.number_of_samples, self.L, self.dy, generator=self.rng)
        # Generate output data for query points y_q with shape (n, 1, dy).
        y_q = torch.einsum('nlx,nxy->nly', x_q, beta)
        y_q += self.noise_std * torch.randn(self.number_of_samples, 1, self.dy, generator=self.rng)

        # Concatenate x and y to form a combined tensor z for training purposes.
        z = torch.cat([x, y], dim=2)
        # Concatenate x_q with a zero-filled tensor to form z_q for query purposes.
        z_q = torch.cat([x_q, torch.zeros_like(y_q)], dim=2)
        return z_q.squeeze(0), z.squeeze(0), y_q

    def __transform__(self, x: Any, zero_index: Optional[int] = None, **kwargs) -> Any:
        """
        Transform the data for training, validation, and testing.

        Parameters:
            x (Any): Input data tensor.
            zero_index (Optional[int]): Index to set to zero in the data (if provided).

        Returns:
            Tuple: Transformed input and target tensors.
        """
        # Extract the last dimension of the data as the target output.
        y = x[..., :, -1].clone()

        # Optionally zero out a specified index.
        if zero_index is not None:
            x[..., zero_index, -1] = 0

        return x, y
    
class MultiTaskLinearReg(DataMethod):
    """
    This class generates data for a linear regression task based on specific parameters, 
    such as data size, sequence length, noise level, and condition number of the covariance matrix.
    """

    def __init__(self, dict: Dict = None):
        """
        Initialize the LinearReg class with a set of parameters.

        Parameters:
            dict (Dict): Dictionary containing parameters for data generation.
        """
        # Call the parent class initializer.
        super().__init__(dict)
        # Extract parameters for data generation.
        self.L = dict['L']  # Sequence length
        self.dx = dict['dx']  # Input dimension
        self.dx1 = dict['dx1'] 
        self.dx2 = dict['dx2']
        self.dy = dict['dy']  # Output dimension
        self.noise_std = dict['noise_std']  # Standard deviation of the noise
        self.number_of_samples = dict['number_of_samples']  # Number of data samples
        

    def __generatedata__(self, **kwargs) -> Any:
        """
        Generate linear regression data.

        Parameters:
            kwargs: Additional keyword arguments (not used here).

        Returns:
            Tuple: Generated data tensors (z_q, z, y_q).
        """
        # Generate input data with shape (n, L, dx).
        x = torch.randn(self.number_of_samples, self.L, self.dx, generator=self.rng)
        # Generate query data (single time-step data) with shape (n, 1, dx).
        x_q = torch.randn(self.number_of_samples, 1, self.dx, generator=self.rng)

        # Generate regression coefficients (beta) with shape (n, dx, dy).
        beta1 = torch.randn(self.number_of_samples, self.dx1, self.dy, generator=self.rng)
        beta2 = torch.randn(self.number_of_samples, self.dx2, self.dy, generator=self.rng)
        
        # Generate target output data y with shape (n, L, dy) using x and beta.
        y1 = torch.einsum('nlx,nxy->nly', x[:, :, :self.dx1], beta1)
        # Add Gaussian noise to the output y.
        y1 += np.sqrt(self.dx1) * self.noise_std * torch.randn(self.number_of_samples, self.L, self.dy, generator=self.rng)
        # Generate output data for query points y_q with shape (n, 1, dy).
        y_q1 = torch.einsum('nlx,nxy->nly', x_q[:, :, :self.dx1], beta1)

        y2 = torch.einsum('nlx,nxy->nly', x[:, :, self.dx - self.dx2:], beta2)
        # Add Gaussian noise to the output y.
        y2 += np.sqrt(self.dx2) * self.noise_std * torch.randn(self.number_of_samples, self.L, self.dy, generator=self.rng)
        # Generate output data for query points y_q with shape (n, 1, dy).
        y_q2 = torch.einsum('nlx,nxy->nly', x_q[:, :, self.dx - self.dx2:], beta2)

        # Concatenate x and y to form a combined tensor z for training purposes.
        z = torch.cat([x, y1, y2], dim=2)
        # Concatenate x_q with a zero-filled tensor to form z_q for query purposes.
        y_q = torch.cat([y_q1, y_q2], dim=2)
        y_q = y_q.squeeze(0)
        z_q = torch.cat([x_q, torch.zeros_like(y_q)], dim=2)
        return z_q.squeeze(0), z.squeeze(0), y_q

    def __transform__(self, x: Any, zero_index: Optional[int] = None, **kwargs) -> Any:
        """
        Transform the data for training, validation, and testing.

        Parameters:
            x (Any): Input data tensor.
            zero_index (Optional[int]): Index to set to zero in the data (if provided).

        Returns:
            Tuple: Transformed input and target tensors.
        """
        # Extract the last dimension of the data as the target output.
        y = x[..., :, -1].clone()

        # Optionally zero out a specified index.
        if zero_index is not None:
            x[..., zero_index, -1] = 0

        return x, y

def parse_kcm(s):
    if not s.startswith("KCM "):
        return None  # or raise an error

    rho = float(s.split(" ", 1)[1])
    return rho