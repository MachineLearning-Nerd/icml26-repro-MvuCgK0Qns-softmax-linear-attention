#!/usr/bin/env python3
"""Render the five evidence-bearing figures used by the public report."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


COLORS = {
    "FALSIFIED": "#b91c1c",
    "VERIFIED": "#047857",
    "BLOCKED": "#b45309",
    "historical": "#2563eb",
}
REGIME_LABELS = {
    "isotropic": "isotropic",
    "rotated_condition_8": "rotated, cond. 8",
    "toeplitz_rho_0.5": "Toeplitz, ρ=0.5",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def save(fig: plt.Figure, path: Path) -> None:
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def claim_outcomes(output_dir: Path) -> None:
    labels = ["Prop. 3.1", "Prop. 3.4", "Lemma 2.1", "Theorem 4.3", "Theorem 5.1"]
    statuses = ["FALSIFIED", "FALSIFIED", "VERIFIED", "VERIFIED", "VERIFIED"]
    basis = [
        "exact L=1 witness",
        "exact L=1 gradient witness",
        "dimension-free Gaussian proof",
        "arbitrary-ε transfer proof",
        "full-domain dynamics proof",
    ]
    fig, ax = plt.subplots(figsize=(11.5, 4.2))
    y = np.arange(len(labels))[::-1]
    ax.barh(y, np.ones(5), color=[COLORS[s] for s in statuses], height=0.66)
    for yi, status, reason in zip(y, statuses, basis):
        ax.text(0.03, yi, status, va="center", ha="left", color="white", weight="bold")
        ax.text(0.98, yi, reason, va="center", ha="right", color="white", fontsize=10)
    ax.set_yticks(y, labels)
    ax.set_xlim(0, 1)
    ax.set_xticks([])
    ax.set_title("Exact claim audit: all five quantified contracts resolved", loc="left", weight="bold")
    ax.text(
        0,
        -0.18,
        "Status is based on literal quantified contracts; historical d=4 numerics are not promoted to theorem proof.",
        transform=ax.transAxes,
        fontsize=9,
        color="#374151",
    )
    for spine in ax.spines.values():
        spine.set_visible(False)
    save(fig, output_dir / "claim_outcomes.png")


def literal_boundary(output_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    x = np.arange(2)
    width = 0.32
    ax.bar(x - width / 2, [1, 1], width, label="exact LHS", color="#b91c1c")
    ax.bar(x + width / 2, [0, 0], width, label="published RHS at L=1", color="#9ca3af")
    ax.set_xticks(x, ["Prop. 3.1 output", "Prop. 3.4 gradients"])
    ax.set_ylabel("squared-error bound")
    ax.set_ylim(0, 1.18)
    ax.legend(frameon=False, loc="upper right")
    ax.set_title("The literal bounds vanish at L=1, but the exact errors equal one", loc="left", weight="bold")
    ax.text(
        0.5,
        -0.17,
        "Witness: d=1, μ=ν=N(0,1); Prop. 3.4 satisfies all nine Assumption 3.3 moment bounds.",
        transform=ax.transAxes,
        ha="center",
        fontsize=9,
        color="#374151",
    )
    ax.spines[["top", "right"]].set_visible(False)
    save(fig, output_dir / "literal_l1_counterexamples.png")


def gaussian_identity(output_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(11.5, 3.5))
    ax.axis("off")
    boxes = [
        ("Gaussian prompt", "X=m+BG\nΓ=BBᵀ"),
        ("Tilt", "a=KᵀQz\nexp(aᵀX)"),
        ("Exact normalizer", "F(a)=exp(aᵀm+\n½aᵀΓa)"),
        ("Differentiate", "E[Xeᵃᵀˣ]=\n(m+Γa)F(a)"),
        ("Cancel F(a)", "T(z)=Vm+\nVΓKᵀQz"),
    ]
    xs = np.linspace(0.08, 0.92, len(boxes))
    for idx, (x, (title, body)) in enumerate(zip(xs, boxes)):
        ax.text(
            x,
            0.55,
            f"{title}\n\n{body}",
            transform=ax.transAxes,
            ha="center",
            va="center",
            bbox={"boxstyle": "round,pad=0.55", "fc": "#ecfdf5", "ec": "#047857", "lw": 1.5},
            fontsize=10,
        )
        if idx < len(boxes) - 1:
            ax.annotate(
                "",
                xy=(xs[idx + 1] - 0.075, 0.55),
                xytext=(x + 0.075, 0.55),
                xycoords=ax.transAxes,
                arrowprops={"arrowstyle": "->", "lw": 1.5, "color": "#374151"},
            )
    ax.set_title(
        "Lemma 2.1 is an exact identity in every dimension, including singular Gaussian covariance",
        loc="left",
        weight="bold",
    )
    save(fig, output_dir / "gaussian_identity_certificate.png")


def historical_concentration(output_dir: Path, data_dir: Path) -> None:
    rows = read_csv(data_dir / "concentration_aggregate.csv")
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.5), sharex=True)
    metrics = [("output_mse", "Output MSE"), ("jacobian_u_mse", "U-Jacobian MSE")]
    for ax, (metric, title) in zip(axes, metrics):
        for regime in REGIME_LABELS:
            subset = [r for r in rows if r["regime"] == regime]
            lengths = [int(r["prompt_length"]) for r in subset]
            values = [float(r[metric]) for r in subset]
            ax.loglog(lengths, values, marker="o", label=REGIME_LABELS[regime])
        ax.set_title(title)
        ax.set_xlabel("prompt length L")
        ax.grid(True, which="both", alpha=0.2)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("mean squared error")
    axes[1].legend(frameon=False, fontsize=8)
    fig.suptitle(
        "Historical d=4 numerics corroborate concentration, but do not prove the σ-dependent rates",
        x=0.06,
        ha="left",
        weight="bold",
    )
    save(fig, output_dir / "historical_concentration.png")


def bayes_full_domain(output_dir: Path, data_dir: Path) -> None:
    rows = read_csv(data_dir / "bayes_transfer.csv")
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.5))
    ax = axes[0]
    for regime in REGIME_LABELS:
        subset = [r for r in rows if r["regime"] == regime]
        ax.loglog(
            [int(r["prompt_length"]) for r in subset],
            [float(r["finite_softmax_risk"]) for r in subset],
            marker="o",
            label=REGIME_LABELS[regime],
        )
    ax.axhline(1e-32, color="#047857", linestyle="--", linewidth=1.2, label="exact limit risk = 0")
    ax.set_title("Historical finite-prompt risk")
    ax.set_xlabel("prompt length L")
    ax.set_ylabel("risk")
    ax.grid(True, which="both", alpha=0.2)
    ax.legend(frameon=False, fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)

    ax = axes[1]
    ax.axis("off")
    steps = [
        ("Exact risk", "R=½‖(bΣA−I)Σ¹ᐟ²‖²"),
        ("Balanced flow", "‖A‖²−b²=0"),
        ("Exclude origin", "tr(A)>0\nand increases nearby"),
        ("Unique limit", "bΣA=I\nrisk = 0"),
    ]
    ys = np.linspace(0.84, 0.16, len(steps))
    for idx, (y, (title, body)) in enumerate(zip(ys, steps)):
        ax.text(
            0.5,
            y,
            f"{title}\n{body}",
            transform=ax.transAxes,
            ha="center",
            va="center",
            bbox={"boxstyle": "round,pad=0.45", "fc": "#ecfdf5", "ec": "#047857"},
            fontsize=9.5,
        )
        if idx < len(steps) - 1:
            ax.annotate(
                "",
                xy=(0.5, ys[idx + 1] + 0.075),
                xytext=(0.5, y - 0.075),
                xycoords=ax.transAxes,
                arrowprops={"arrowstyle": "->", "color": "#374151"},
            )
    ax.set_title("Direct proof replaces the narrower citation", weight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle(
        "Theorem 5.1: exact Bayes endpoint and full-domain convergence certificate",
        x=0.06,
        ha="left",
        weight="bold",
    )
    save(fig, output_dir / "bayes_full_domain_proof.png")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("outputs/full"))
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    claim_outcomes(args.output_dir)
    literal_boundary(args.output_dir)
    gaussian_identity(args.output_dir)
    historical_concentration(args.output_dir, args.data_dir)
    bayes_full_domain(args.output_dir, args.data_dir)


if __name__ == "__main__":
    main()
