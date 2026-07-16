# Claim 1 - Gaussian affine limit


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_a4cc3578eb31", "created_at": "2026-07-16T16:20:09+00:00", "title": "VERIFIED with independent integration and boundary control"}
-->
## Verdict: VERIFIED

The numerator and denominator of finite softmax attention are independently
integrated with tensor Gauss-Hermite rules. Across 48 cases in dimensions 1–3,
including nonzero means and randomly generated full covariances, the ratio
matches `V m + V Γ U z` with worst coordinate error
`1.277e-15`.

Finite Monte Carlo prompts independently approach the same operator: output
MSE drops **41.4–76.9×**
from L=16 to 1024. The distributional boundary is explicit: for a one-dimensional
Rademacher input with `U=V=1,z=2`, the exact tilted output is `tanh(2)`, not 2,
leaving residual `1.035972`.
This rejects a moment-only or distribution-free interpretation.
