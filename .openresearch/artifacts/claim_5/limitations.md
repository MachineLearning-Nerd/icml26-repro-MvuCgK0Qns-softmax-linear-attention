# Limitations and deviations

- Exact Bayes optimality of the limit matrices does not prove gradient flow
  reaches them over the theorem's full domain.
- Lemma E.1 covers `||Sigma||_op<=1`, not every invertible `Sigma`.
- The displayed alpha interval does not imply the cited JMLR sufficient
  condition for all `||Sigma||_op<1`.
- The exact scalar ODE converges for every positive initialization, so the
  dependency mismatch is not a valid theorem counterexample.
- Unblocking requires a general-dimensional convergence proof over the full
  published domain or a valid assumption-satisfying counterexample.
