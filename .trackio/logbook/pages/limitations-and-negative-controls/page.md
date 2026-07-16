# Limitations and negative controls


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_ea21d5ae2c85", "created_at": "2026-07-16T16:20:15+00:00", "title": "Scoped conclusions"}
-->
# Limitations and negative controls

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
