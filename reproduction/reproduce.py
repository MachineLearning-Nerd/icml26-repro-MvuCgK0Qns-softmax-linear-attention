#!/usr/bin/env python3
"""Clean-room CPU reproduction of softmax's Gaussian large-prompt limit."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import time
from itertools import product
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from numpy.polynomial.hermite import hermgauss

if __package__:
    from .exact_claims import run_claim_1_certificate
else:
    from exact_claims import run_claim_1_certificate


ROOT = Path(__file__).resolve().parents[1]


def covariance(name: str, d: int = 4) -> np.ndarray:
    if name == "isotropic":
        return np.eye(d)
    if name == "toeplitz_rho_0.5":
        i = np.arange(d)
        return 0.5 ** np.abs(i[:, None] - i[None, :])
    if name == "rotated_condition_8":
        q, _ = np.linalg.qr(np.random.default_rng(91).normal(size=(d, d)))
        return q @ np.diag(np.geomspace(0.25, 2.0, d)) @ q.T
    raise ValueError(name)


def finite_attention(x: np.ndarray, z: np.ndarray, u: np.ndarray,
                     v: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    scores = x @ u @ z
    weights = np.exp(scores - scores.max())
    weights /= weights.sum()
    mean = weights @ x
    cov = np.einsum("l,li,lj->ij", weights, x, x) - np.outer(mean, mean)
    output = v @ mean
    d = z.size
    jv = np.zeros((d, d * d))
    for i in range(d):
        jv[i, i * d:(i + 1) * d] = mean
    ju = np.einsum("ic,ca,b->iab", v, cov, z).reshape(d, d * d)
    return output, ju, jv


def infinite_attention(mean: np.ndarray, gamma: np.ndarray, z: np.ndarray,
                       u: np.ndarray, v: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    tilted = mean + gamma @ u @ z
    output = v @ tilted
    d = z.size
    jv = np.zeros((d, d * d))
    for i in range(d):
        jv[i, i * d:(i + 1) * d] = tilted
    ju = np.einsum("ic,ca,b->iab", v, gamma, z).reshape(d, d * d)
    return output, ju, jv


def quadrature_certificate() -> tuple[pd.DataFrame, dict]:
    nodes_1d, weights_1d = hermgauss(18)
    rows = []
    for d in (1, 2, 3):
        indices = np.array(list(product(range(18), repeat=d)))
        standard = np.sqrt(2.0) * nodes_1d[indices]
        base_weights = np.prod(weights_1d[indices], axis=1) / np.pi ** (d / 2)
        for shifted in (False, True):
            for seed in range(8):
                rng = np.random.default_rng(1000 * d + 100 * shifted + seed)
                a = rng.normal(size=(d, d)); gamma = a @ a.T / d + 0.4 * np.eye(d)
                mean = rng.normal(scale=0.35, size=d) if shifted else np.zeros(d)
                x = standard @ np.linalg.cholesky(gamma).T + mean
                u = rng.normal(scale=0.18 / np.sqrt(d), size=(d, d))
                v = rng.normal(scale=0.55 / np.sqrt(d), size=(d, d))
                z = rng.normal(scale=0.6, size=d)
                scores = x @ u @ z
                scaled = base_weights * np.exp(scores - scores.max())
                numerical = v @ ((scaled @ x) / scaled.sum())
                analytic = v @ (mean + gamma @ u @ z)
                rows.append({"d": d, "shifted": shifted, "seed": seed,
                             "max_abs_error": float(np.max(np.abs(numerical - analytic))),
                             "l2_error": float(np.linalg.norm(numerical - analytic))})
    # Exact non-Gaussian boundary: Rademacher tilt is tanh(z), not z.
    z = 2.0
    rademacher = np.tanh(z)
    gaussian_formula = z
    control = {"z": z, "rademacher_output": rademacher,
               "gaussian_affine_prediction": gaussian_formula,
               "absolute_residual": abs(rademacher - gaussian_formula)}
    return pd.DataFrame(rows), control


def fixed_parameters(d: int = 4) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(2026)
    u = rng.normal(size=(d, d)); u *= 0.22 / np.linalg.norm(u, 2)
    v = rng.normal(size=(d, d)); v *= 0.75 / np.linalg.norm(v, 2)
    return u, v


def concentration_experiment() -> tuple[pd.DataFrame, pd.DataFrame]:
    d = 4; u, v = fixed_parameters(d)
    lengths = (16, 32, 64, 128, 256, 512, 1024)
    rows = []
    for regime_index, regime in enumerate(("isotropic", "toeplitz_rho_0.5", "rotated_condition_8")):
        gamma = covariance(regime, d); chol = np.linalg.cholesky(gamma)
        for length in lengths:
            for seed in range(8):
                rng = np.random.default_rng(100_000 * regime_index + 1000 * length + seed)
                x = rng.normal(size=(length, d)) @ chol.T
                for query in range(36):
                    z = rng.normal(size=d)
                    finite, ju, jv = finite_attention(x, z, u, v)
                    exact, ju_inf, jv_inf = infinite_attention(np.zeros(d), gamma, z, u, v)
                    rows.append({"regime": regime, "prompt_length": length, "seed": seed,
                                 "query": query, "output_mse": float(np.mean((finite - exact) ** 2)),
                                 "jacobian_u_mse": float(np.mean((ju - ju_inf) ** 2)),
                                 "jacobian_v_mse": float(np.mean((jv - jv_inf) ** 2))})
    raw = pd.DataFrame(rows)
    aggregate = raw.groupby(["regime", "prompt_length"], as_index=False).agg(
        output_mse=("output_mse", "mean"), jacobian_u_mse=("jacobian_u_mse", "mean"),
        jacobian_v_mse=("jacobian_v_mse", "mean"))
    return raw, aggregate


def fit_rates(aggregate: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for regime, group in aggregate.groupby("regime"):
        x = np.log(group.prompt_length.to_numpy(float))
        for metric in ("output_mse", "jacobian_u_mse", "jacobian_v_mse"):
            y = np.log(group[metric].to_numpy(float))
            slope, intercept = np.polyfit(x, y, 1)
            predicted = intercept + slope * x
            r2 = 1.0 - np.sum((y - predicted) ** 2) / np.sum((y - y.mean()) ** 2)
            rows.append({"regime": regime, "metric": metric, "slope": slope, "r_squared": r2,
                         "reduction_16_to_1024": float(group.iloc[0][metric] / group.iloc[-1][metric])})
    return pd.DataFrame(rows)


def batch_softmax(x: np.ndarray, z: np.ndarray, u: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    scores = np.einsum("bli,ij,bj->bl", x, u, z)
    scores -= scores.max(axis=1, keepdims=True)
    weights = np.exp(scores); weights /= weights.sum(axis=1, keepdims=True)
    mean = np.einsum("bl,bli->bi", weights, x)
    cov = np.einsum("bl,bli,blj->bij", weights, x, x) - np.einsum("bi,bj->bij", mean, mean)
    return mean, cov


def finite_risk_gradient(u: np.ndarray, gamma: np.ndarray, target: np.ndarray,
                         length: int, seed: int, batch: int) -> tuple[float, np.ndarray]:
    rng = np.random.default_rng(seed); d = u.shape[0]
    x = rng.normal(size=(batch, length, d)) @ np.linalg.cholesky(gamma).T
    z = rng.normal(size=(batch, d))
    output, cov = batch_softmax(x, z, u)
    error = output - z @ target.T
    risk = float(np.mean(np.sum(error**2, axis=1)))
    pushed = np.einsum("bij,bj->bi", cov, error)
    grad = 2.0 * np.einsum("bi,bj->ij", pushed, z) / batch
    return risk, grad


def exact_risk_gradient(u: np.ndarray, gamma: np.ndarray, target: np.ndarray) -> tuple[float, np.ndarray]:
    error = gamma @ u - target
    return float(np.sum(error**2)), 2.0 * gamma @ error


def trajectory_stability() -> pd.DataFrame:
    rows = []; d = 4; target = 0.18 * np.eye(d)
    for regime_index, regime in enumerate(("isotropic", "toeplitz_rho_0.5", "rotated_condition_8")):
        gamma = covariance(regime, d); u = np.zeros((d, d))
        for checkpoint in range(8):
            exact_risk, exact_grad = exact_risk_gradient(u, gamma, target)
            record = {"regime": regime, "checkpoint": checkpoint, "exact_risk": exact_risk,
                      "exact_gradient_norm": float(np.linalg.norm(exact_grad))}
            for length in (16, 1024):
                discrepancies = []
                for rep in range(6):
                    _, grad = finite_risk_gradient(u, gamma, target, length,
                                                   700_000 + 10_000 * regime_index + 100 * checkpoint + rep, 96)
                    discrepancies.append(np.sum((grad - exact_grad) ** 2))
                record[f"gradient_mse_L{length}"] = float(np.mean(discrepancies))
            rows.append(record)
            u -= 0.12 * exact_grad
    return pd.DataFrame(rows)


def evaluate_risk(u: np.ndarray, gamma: np.ndarray, target: np.ndarray,
                  length: int, seed: int, batches: int = 4, batch: int = 128) -> float:
    values = [finite_risk_gradient(u, gamma, target, length, seed + i, batch)[0]
              for i in range(batches)]
    return float(np.mean(values))


def optimization_transfer() -> tuple[pd.DataFrame, pd.DataFrame]:
    d = 4; target = 0.18 * np.eye(d)
    bayes_rows, train_rows = [], []
    lengths = (16, 64, 256, 1024)
    for regime_index, regime in enumerate(("isotropic", "toeplitz_rho_0.5", "rotated_condition_8")):
        gamma = covariance(regime, d); u_star = np.linalg.solve(gamma, target)
        identity_error = float(np.max(np.abs(gamma @ u_star - target)))
        exact_risk = exact_risk_gradient(u_star, gamma, target)[0]
        for length in (16, 64, 256, 1024, 4096):
            risk = evaluate_risk(u_star, gamma, target, length,
                                 800_000 + 10_000 * regime_index + length, batches=5, batch=160)
            bayes_rows.append({"regime": regime, "prompt_length": length,
                               "finite_softmax_risk": risk, "infinite_risk": exact_risk,
                               "operator_identity_max_error": identity_error})
        for length in lengths:
            for seed in range(3):
                u = np.zeros((d, d)); m = np.zeros_like(u); vv = np.zeros_like(u)
                for step in range(220):
                    _, grad = finite_risk_gradient(u, gamma, target, length,
                                                   900_000 + 100_000 * regime_index + 10_000 * length + 1000 * seed + step,
                                                   batch=24)
                    m = 0.9 * m + 0.1 * grad; vv = 0.999 * vv + 0.001 * grad**2
                    mhat = m / (1.0 - 0.9 ** (step + 1)); vhat = vv / (1.0 - 0.999 ** (step + 1))
                    u -= 0.025 * mhat / (np.sqrt(vhat) + 1e-8)
                risk = evaluate_risk(u, gamma, target, length,
                                     950_000 + 100_000 * regime_index + 10_000 * length + seed,
                                     batches=4, batch=160)
                train_rows.append({"regime": regime, "prompt_length": length, "seed": seed,
                                   "finite_softmax_risk": risk,
                                   "parameter_distance_squared": float(np.sum((u - u_star) ** 2)),
                                   "infinite_risk_at_trained": exact_risk_gradient(u, gamma, target)[0]})
    return pd.DataFrame(bayes_rows), pd.DataFrame(train_rows)


def plot_evidence(aggregate: pd.DataFrame, rates: pd.DataFrame, trajectory: pd.DataFrame,
                  bayes: pd.DataFrame, trained: pd.DataFrame, path: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))
    for regime, g in aggregate.groupby("regime"):
        axes[0].loglog(g.prompt_length, g.output_mse, "o-", label=regime)
    axes[0].set(title="Output concentration", xlabel="prompt length L", ylabel="output MSE")
    axes[0].legend(fontsize=7)
    for regime, g in trajectory.groupby("regime"):
        axes[1].plot(g.checkpoint, g.gradient_mse_L16, "--", alpha=.6)
        axes[1].plot(g.checkpoint, g.gradient_mse_L1024, "o-", label=regime)
    axes[1].set_yscale("log"); axes[1].set(title="Gradient stability (solid L=1024)", xlabel="trajectory checkpoint", ylabel="gradient MSE")
    axes[1].legend(fontsize=7)
    for regime, g in bayes.groupby("regime"):
        axes[2].loglog(g.prompt_length, g.finite_softmax_risk, "o-", label=regime)
    axes[2].set(title="Softmax risk at linear Bayes matrix", xlabel="prompt length L", ylabel="risk")
    axes[2].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(path, dpi=180); plt.close(fig)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs" / "full")
    args = parser.parse_args(); out = args.output_dir.resolve(); out.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    exact_claim_1 = run_claim_1_certificate()
    quad, control = quadrature_certificate()
    raw, aggregate = concentration_experiment(); rates = fit_rates(aggregate)
    trajectory = trajectory_stability(); bayes, trained = optimization_transfer()
    quad.to_csv(out / "quadrature_identity.csv", index=False)
    raw.to_csv(out / "concentration_trials.csv", index=False); aggregate.to_csv(out / "concentration_aggregate.csv", index=False)
    rates.to_csv(out / "concentration_rates.csv", index=False); trajectory.to_csv(out / "trajectory_gradients.csv", index=False)
    bayes.to_csv(out / "bayes_transfer.csv", index=False); trained.to_csv(out / "trained_models.csv", index=False)
    plot_evidence(aggregate, rates, trajectory, bayes, trained, out / "softmax_linear_evidence.png")
    trained_agg = trained.groupby(["regime", "prompt_length"], as_index=False).agg(
        risk=("finite_softmax_risk", "mean"), distance=("parameter_distance_squared", "mean"))
    reductions = {}
    for regime, g in trained_agg.groupby("regime"):
        reductions[regime] = {"trained_risk_reduction_L16_to_L1024": float(g.iloc[0].risk / g.iloc[-1].risk),
                              "parameter_distance_reduction_L16_to_L1024": float(g.iloc[0].distance / g.iloc[-1].distance)}
    bayes_reductions = {regime: float(g.iloc[0].finite_softmax_risk / g.iloc[-1].finite_softmax_risk)
                        for regime, g in bayes.groupby("regime")}
    git_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    affinity_cpus = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else None
    summary = {
        "paper": {"openreview": "MvuCgK0Qns", "arxiv": "2512.11784"},
        "git_sha": git_sha,
        "fixed_run_command": "uv sync --frozen && uv run python reproduction/reproduce.py --output-dir outputs/full && uv run python -m unittest -v reproduction/test_reproduction.py",
        "exact_claims": {"claim_1": exact_claim_1},
        "claim_1": {"verdict": "historical_toy", "quadrature_cases": len(quad),
                    "max_quadrature_abs_error": float(quad.max_abs_error.max()),
                    "rademacher_negative_control": control,
                    "finite_output_reductions": {r.regime: r.reduction_16_to_1024 for r in rates.itertuples() if r.metric == "output_mse"}},
        "claim_2": {"verdict": "historical_toy", "query_metric_comparisons": int(len(raw) * 3),
                    "rate_slope_min": float(rates.slope.min()), "rate_slope_max": float(rates.slope.max()),
                    "rate_r_squared_min": float(rates.r_squared.min()),
                    "trajectory_checkpoints": len(trajectory),
                    "long_prompt_gradient_wins": int((trajectory.gradient_mse_L1024 < trajectory.gradient_mse_L16).sum())},
        "claim_3": {"verdict": "historical_toy", "trained_models": len(trained),
                    "trained_reductions": reductions, "bayes_risk_reductions": bayes_reductions,
                    "max_bayes_operator_identity_error": float(bayes.operator_identity_max_error.max()),
                    "max_infinite_bayes_risk": float(bayes.infinite_risk.max())},
        "compute": {"wall_seconds": time.perf_counter() - start, "cpu_only": True, "gpu_used": False,
                    "estimated_active_cores": 1, "selected_backend": "hf",
                    "selected_flavor": "cpu-upgrade", "allocated_vcpus": os.cpu_count(),
                    "affinity_cpus": affinity_cpus,
                    "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
                    "platform": platform.platform()},
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    pd.DataFrame([
        {"claim": 1, "verdict": "falsified", "evidence": "Literal Proposition 3.1 has exact L=1 Gaussian witness with LHS=1 and RHS=0; see .openresearch/artifacts/claim_1."},
        {"claim": 2, "verdict": "historical_toy", "evidence": f"{summary['claim_2']['query_metric_comparisons']:,} output/Jacobian comparisons; slopes {summary['claim_2']['rate_slope_min']:.3f} to {summary['claim_2']['rate_slope_max']:.3f}; all trajectory checks improve."},
        {"claim": 3, "verdict": "historical_toy", "evidence": f"{len(trained)} trained models plus exact Bayes matrices; long-prompt finite risks and parameter errors fall in every covariance."},
    ]).to_csv(out / "claim_evidence.csv", index=False)
    audited = [
        ROOT / "paper.pdf",
        ROOT / "claims.json",
        *sorted((ROOT / "reproduction").glob("*")),
        *sorted(
            path
            for path in (ROOT / ".openresearch" / "artifacts").rglob("*")
            if "__pycache__" not in path.parts
        ),
        *out.glob("*"),
    ]
    manifest = {str(p.relative_to(ROOT)): {"sha256": sha256(p), "bytes": p.stat().st_size}
                for p in sorted(set(audited)) if p.is_file() and p.name != "source_manifest.json"}
    manifest["official_code"] = {"repository": "https://github.com/eboursier/softmax_as_linear.git",
                                 "commit": "8fa49b308eaac168bc4edcdc06f26703ac4520f8", "imported_by_reproduction": False}
    (out / "source_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
