# Source and claim audit

Paper: **Softmax as Linear Attention in the Large-Prompt Regime: a
Measure-based Perspective** (`MvuCgK0Qns`, arXiv `2512.11784`). PDF SHA-256:
`3e1c12c82e55e253f2933c139a676b1a642e552637a17ca273e3f0dc47423ede`.

Official repository: `https://github.com/eboursier/softmax_as_linear.git`, pinned
at `8fa49b308eaac168bc4edcdc06f26703ac4520f8`. The reproduction imports no
official module.

## Claim mapping

- Claim 1 maps to the Gaussian exponential-tilt identity: the ratio of the
  independently integrated numerator and denominator is
  `V m + V Gamma U z`. Tensor Gauss-Hermite integration checks dimensions 1–3,
  centered and shifted Gaussians. A Rademacher control gives `tanh(z)` rather
  than `z`, delimiting the Gaussian mechanism.
- Claim 2 is tested at the output and exact parameter-Jacobian levels over
  seven prompt lengths and three covariance families. Exact finite Jacobians
  are independently finite-differenced. Finite stochastic gradients are also
  compared with the exact infinite-risk gradient at eight points per
  covariance along an Euler trajectory.
- Claim 3 is tested through the exact linear-limit solution
  `Gamma U*=A`, finite-softmax risk at that matrix through `L=4096`, and 36
  independently trained finite-prompt models. This is numerical support for
  transfer, not a proof of the theorem's universal quantifiers.

## Official-code boundary

The pinned `utils/data_utils.py` transforms the prompt covariance at line 148,
then transforms `x` a second time at line 153 where the query `x_q` would be
expected. The clean-room anisotropic generator therefore applies one Cholesky
transform to both prompt and query and verifies empirical construction through
the defining covariance, rather than treating that official path as decisive.
