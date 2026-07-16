from __future__ import annotations

import json
import subprocess
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TRACKIO = ROOT / ".venv" / "bin" / "trackio"
OUT = ROOT / "outputs" / "full"
ARTIFACT = "softmax-linear-attention-repro/softmax-linear-attention-cpu-reproduction:v0"

def call(*args: str) -> None:
    subprocess.run([str(TRACKIO), "logbook", *args], cwd=ROOT, check=True)

def page(title: str) -> None: call("page", title)
def md(p: str, title: str, body: str) -> None: call("cell", "markdown", "--page", p, "--title", title, body)
def fig(p: str, title: str, image: str, raw: str) -> None:
    call("cell", "figure", "--page", p, "--title", title, "--image", image, "--raw", raw)

def main() -> None:
    s = json.loads((OUT / "summary.json").read_text())
    c1, c2, c3 = s["claim_1"], s["claim_2"], s["claim_3"]
    rates = pd.read_csv(OUT / "concentration_rates.csv")
    p = "00 - Scored evidence summary"; page(p)
    md(p, "GO - all three claims supported", f"""# Scored evidence first — GO

**Paper:** Softmax as Linear Attention in the Large-Prompt Regime: a Measure-based Perspective  
**OpenReview:** `MvuCgK0Qns` | **arXiv:** `2512.11784`  
**Tags:** `icml2026-repro`, `paper-MvuCgK0Qns`  
**Compute:** local CPU only; no GPU, cloud, API model, or spend  
**Verification:** 8/8 fail-closed tests; wall time **{s['compute']['wall_seconds']:.2f}s**

| # | Exact challenge claim | Verdict | Decisive independent evidence |
|---:|---|---|---|
| 1 | Softmax attention converges to linear operator in infinite-prompt limit for i.i.d. Gaussian inputs. | **VERIFIED** | 48 tensor Gauss-Hermite cases, centered and shifted, match `Vm+VΓUz` to max error `{c1['max_quadrature_abs_error']:.2e}`. Finite output MSE falls 41–77×; a Rademacher control rejects the Gaussian affine formula by `{c1['rademacher_negative_control']['absolute_residual']:.3f}`. |
| 2 | Establishes non-asymptotic concentration bounds for softmax attention output and gradient stability along training trajectory. | **VERIFIED** | {c2['query_metric_comparisons']:,} output/U-Jacobian/V-Jacobian comparisons: all nine slopes `{c2['rate_slope_min']:.3f}` to `{c2['rate_slope_max']:.3f}`, minimum R² `{c2['rate_r_squared_min']:.3f}`. L=1024 gradients beat L=16 at {c2['long_prompt_gradient_wins']}/{c2['trajectory_checkpoints']} trajectory checks. |
| 3 | Large-prompt softmax attention inherits analytical structure of linear attention enabling transfer of optimization analyses. | **VERIFIED** | 36 trained models across three covariance families show 44–54× risk reductions and 20–206× parameter-distance reductions from L=16 to 1024. Exact anisotropic linear-limit matrices satisfy `ΓU*=A` within `{c3['max_bayes_operator_identity_error']:.2e}` and finite-softmax risk falls 232–263× through L=4096. |

The experiment uses float64, dimension 4 for finite-prompt work, three
covariance families including two anisotropic cases, exact analytic Jacobians,
fresh queries, and raw seed-level rows. Numerical evidence supports the
theorems' mechanism without being represented as a proof of universal constants.
""")
    call("pin", "--page", p)
    fig(p, "Identity, concentration, gradients, and transfer", "outputs/full/softmax_linear_evidence.png", "outputs/full/claim_evidence.csv")

    p = "Claim 1 - Gaussian affine limit"; page(p)
    md(p, "VERIFIED with independent integration and boundary control", f"""## Verdict: VERIFIED

The numerator and denominator of finite softmax attention are independently
integrated with tensor Gauss-Hermite rules. Across 48 cases in dimensions 1–3,
including nonzero means and randomly generated full covariances, the ratio
matches `V m + V Γ U z` with worst coordinate error
`{c1['max_quadrature_abs_error']:.3e}`.

Finite Monte Carlo prompts independently approach the same operator: output
MSE drops **{min(c1['finite_output_reductions'].values()):.1f}–{max(c1['finite_output_reductions'].values()):.1f}×**
from L=16 to 1024. The distributional boundary is explicit: for a one-dimensional
Rademacher input with `U=V=1,z=2`, the exact tilted output is `tanh(2)`, not 2,
leaving residual `{c1['rademacher_negative_control']['absolute_residual']:.6f}`.
This rejects a moment-only or distribution-free interpretation.
""")

    p = "Claim 2 - Concentration and gradient stability"; page(p)
    table = ["| regime | metric | slope | R² | L16/L1024 reduction |", "|---|---|---:|---:|---:|"]
    for r in rates.itertuples(): table.append(f"| {r.regime} | {r.metric} | {r.slope:.3f} | {r.r_squared:.3f} | {r.reduction_16_to_1024:.1f}× |")
    md(p, "VERIFIED at output, exact-Jacobian, and trajectory levels", f"""## Verdict: VERIFIED

{chr(10).join(table)}

There are 6,048 fresh-query cases and three metrics per case: output MSE,
U-Jacobian MSE, and V-Jacobian MSE. The closed-form finite Jacobians are also
finite-differenced in the test suite. All nine fits decay with high R².

For gradient stability, an exact infinite-population quadratic risk supplies
both risk and gradient. At eight Euler checkpoints per covariance, stochastic
finite-softmax gradients are independently estimated for L=16 and 1024.
Long-prompt discrepancy is lower at all **24/24** checkpoints; this tests the
claim along a trajectory rather than only at initialization.
""")
    fig(p, "Output and exact-Jacobian concentration", "outputs/full/softmax_linear_evidence.png", "outputs/full/concentration_aggregate.csv")

    p = "Claim 3 - Optimization transfer"; page(p)
    reductions = c3["trained_reductions"]
    rows = ["| covariance | trained risk reduction | parameter-distance reduction | Bayes-matrix risk reduction |",
            "|---|---:|---:|---:|"]
    for regime in sorted(reductions):
        rows.append(f"| {regime} | {reductions[regime]['trained_risk_reduction_L16_to_L1024']:.1f}× | {reductions[regime]['parameter_distance_reduction_L16_to_L1024']:.1f}× | {c3['bayes_risk_reductions'][regime]:.1f}× |")
    md(p, "VERIFIED with trained and exact-limit matrices", f"""## Verdict: VERIFIED

{chr(10).join(rows)}

The target linear operator is `A=0.18I`. The infinite Gaussian softmax risk is
exactly `||ΓU-A||²_F`, so `U*=Γ⁻¹A` is the linear-attention solution. Across all
three covariances, `ΓU*=A` holds to `{c3['max_bayes_operator_identity_error']:.2e}`
and infinite risk is below `{c3['max_infinite_bayes_risk']:.2e}`.

Finite softmax risk at this exact matrix continues falling through L=4096.
Separately, 36 finite-prompt models (3 seeds ×4 lengths ×3 covariances) are
trained from zero with analytic gradients. Both test risk and squared distance
to the linear solution shrink strongly as prompt length grows. This directly
demonstrates transfer of the analytical structure while avoiding a claim of
universal/global optimization proof.
""")
    fig(p, "Trained models and exact Bayes matrices", "outputs/full/softmax_linear_evidence.png", "outputs/full/trained_models.csv")

    p = "Methods, tests, and provenance"; page(p)
    md(p, "Independent, fail-closed protocol", """# Methods and provenance

Finite attention uses max-subtracted float64 softmax weights. Its weighted
mean and covariance yield exact U/V Jacobians. Gaussian quadrature integrates
the numerator and denominator separately. Training gradients use the same
weighted covariance, while infinite gradients come from a separate closed-form
quadratic risk.

Eight tests cover: Gaussian quadrature; the Rademacher boundary; all nine
concentration fits; finite-difference Jacobians; trajectory gradient stability;
exact Bayes identities; trained-model approach; and complete CPU outputs.

PDF SHA-256: `3e1c12c82e55e253f2933c139a676b1a642e552637a17ca273e3f0dc47423ede`.
Official repository pinned at `8fa49b308eaac168bc4edcdc06f26703ac4520f8`.
The independent implementation imports no official module. Raw rows, scripts,
tests, source snapshot, hashes, and limitations are in the artifact.
""")
    call("cell", "artifact", "--page", p, "--title", "Complete CPU reproduction bundle", "--type", "dataset", ARTIFACT)

    p = "Limitations and negative controls"; page(p)
    md(p, "Scoped conclusions", """# Limitations and negative controls

- Numerical concentration does not prove the paper's universal constants or
  all sufficiently large prompt lengths.
- The scope is single-head, single-layer attention at dimensions up to 4, which
  matches the theorem mechanism but is not a multi-layer language model.
- Near-L^-1 empirical slopes arise under mild fixed parameters; the theorem
  permits parameter-dependent slower rates.
- The Rademacher control shows the affine identity is specifically Gaussian.
- The official anisotropic data path transforms prompt `x` twice and leaves
  query `x_q` untransformed. The clean-room experiment transforms prompt and
  query once and does not use that path as evidence.
- Finite models use Adam for a numerical transfer probe; trajectory stability
  is separately tested against exact infinite-population Euler gradients.
""")

    p = "Conclusion"; page(p)
    md(p, "Final outcomes", """# Conclusion

- **Claim 1: VERIFIED.** Independent Gaussian integration reaches machine precision and the non-Gaussian control fails correctly.
- **Claim 2: VERIFIED.** Outputs, exact Jacobians, and trajectory gradients all concentrate with prompt length.
- **Claim 3: VERIFIED.** Trained finite-softmax models and exact linear-limit matrices converge in risk and structure across anisotropic covariances.
""")

if __name__ == "__main__": main()
