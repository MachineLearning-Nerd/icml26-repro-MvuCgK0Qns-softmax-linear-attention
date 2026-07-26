# Limitations

- This is a proof certificate for population gradient flow, exactly the
  theorem's optimization model; it is not a finite-step optimizer experiment.
- The result is existential in `L(epsilon)`, as is the paper. No numerical
  prompt threshold is inferred from the concentration formula.
- The proof uses positive definiteness (`Sigma` invertible covariance). It does
  not silently extend the judged claim to singular covariance.
- The earlier BLOCKED packet is preserved unchanged as **Historical rejected
  baseline** under `evidence/claim_5`.
