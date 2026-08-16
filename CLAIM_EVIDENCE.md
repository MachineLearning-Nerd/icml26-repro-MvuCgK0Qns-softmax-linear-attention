# Claim-to-evidence map

This document explains how each paper claim becomes a repository verdict. The
status labels distinguish a literal falsification from a scoped verification;
they are not a replacement for reading the paper source and the packet files.

## Production contract

For each claim, the audit records:

1. source URL, version, hash, and theorem anchor;
2. literal statement, assumptions, and quantifiers;
3. producer command and raw result;
4. independent checker implemented separately from the producer;
5. negative control and expected rejection;
6. limitations and the final status.

The machine-readable contracts are in
space_candidate/evidence/claim_*/claim_contract.json. The packet-level
verifier output is retained beside each packet.

## Proposition 3.1 — literal boundary certificate

- **Source:** Section 3, Proposition 3.1.
- **Contract:** the displayed positive-integer domain admits L=1.
- **Producer:** space_candidate/evidence/claim_1/raw_result.json.
- **Witness:** d=1, L=1, mu=nu=N(0,1), sigma=1, K=0, Q=V=M=1.
- **Exact comparison:** output error is 1; the stated ln(L) upper bound is 0
  for every positive pair of constants.
- **Independent checker:** independent_checker_output.txt reports PASS.
- **Negative control:** the delta_0 distribution has zero error and is
  correctly rejected as a falsification witness.
- **Verdict:** FALSIFIED_AS_WRITTEN.

This is a universal-quantifier counterexample. It does not assert that a
repaired theorem with an explicit sufficiently-large-prompt condition fails.

## Proposition 3.4 — literal gradient-bound certificate

- **Source:** Section 3, Proposition 3.4 and Assumption 3.3.
- **Contract:** both displayed gradient-error bounds hold under all stated
  moment assumptions for every admitted positive integer L.
- **Producer:** space_candidate/evidence/claim_2/raw_result.json.
- **Witness:** d=1, L=1, mu=nu=N(0,1), sigma=1, U=0, V=1.
- **Assumption audit:** all nine products of Gaussian moments of orders 0, 4,
  and 8 are finite.
- **Exact comparison:** both gradient-error left sides are 1; both literal
  ln(L)-based bounds are 0.
- **Independent checker:** reconstructs both gradients and reports PASS.
- **Negative control:** delta_0 has zero gradients and is correctly rejected.
- **Verdict:** FALSIFIED_AS_WRITTEN.

## Lemma 2.1 — Gaussian affine identity

- **Source:** Section 2, Lemma 2.1.
- **Producer:** space_candidate/evidence/claim_3/raw_result.json.
- **Proof path:** write X=m+BG, complete the square in the Gaussian
  exponential tilt, differentiate the normalizer, and cancel the positive
  denominator. This yields T(z)=Vm+V Gamma K^T Qz.
- **Domain:** every dimension and every positive-semidefinite covariance,
  including singular covariance represented as Gamma=BB^T.
- **Independent check:** exact sparse-polynomial reconstruction in dimensions
  1, 2, 3, 4, 8, and 16, covering 380 coefficients.
- **Negative control:** Rademacher attention at z=2 is
  0.9640275800758169, not the Gaussian affine prediction 2.
- **Verdict:** VERIFIED_SCOPED.

## Theorem 4.3 — risk-transfer order certificate

- **Source:** Section 4, Theorem 4.3 and Appendix D.1.
- **Producer:** space_candidate/evidence/claim_4/raw_result.json.
- **Proof path:** choose finite time from the infinite-flow limit; choose
  L(epsilon) so the uniform risk and finite-horizon trajectory errors each
  cost at most epsilon/2; then use dR_L/dt=-||grad R_L||^2 <= 0.
- **Independent check:** reconstructs the quantifier order and verifies the
  exact budget 1/2 + 1/2 = 1.
- **Negative control:** a path that is close at finite time but later increases
  risk is rejected when monotonicity is removed.
- **Verdict:** VERIFIED_SCOPED.
- **Limitation:** no numerical value of L(epsilon) is claimed.

## Theorem 5.1 / Theorem 5.2 — full-domain Bayes certificate

- **Source:** judged Section 5, Theorem 5.1; arXiv v2 Section 5, Theorem 5.2.
- **Producer:** space_candidate/evidence/claim_5_full/raw_result.json.
- **Population model:** R_inf(A,b)=1/2 tr((b Sigma A-I) Sigma
  (b Sigma A-I)^T).
- **Proof path:** derive the matrix gradient flow; prove the invariant
  ||A||_F^2-b^2=0; use bounded analytic gradient-flow convergence; exclude
  the origin with the positive diagonal/trace argument; identify
  b=tr(Sigma^-2)^(1/4) and A=tr(Sigma^-2)^(-1/4) Sigma^-1; verify exact
  zero-risk Bayes prediction; then transfer from arbitrary fixed
  positive-definite covariance scale.
- **Domain:** every positive-definite Sigma and every positive alpha with the
  stated balanced initialization factor, which is stronger than the displayed
  interval.
- **Independent check:** balance derivative, trace identity, anisotropic Bayes
  products, and finite covariance envelope all report PASS.
- **Negative control:** unbalanced initialization is rejected because the
  stationary dichotomy is unavailable.
- **Recorded scientific run:** HF run
  fa29e4cb-51dc-4ede-93c6-40a6517816f4, 20/20 tests, scientific Git SHA
  64130159f3df3a0053280ffde22bb70a7c791265.
- **Verdict:** VERIFIED_SCOPED_FULL_DOMAIN.

The earlier claim_5 packet is intentionally retained with status BLOCKED. It
is the dependency audit that motivated the direct proof; it is not a
contradictory current verdict.

## Historical numerical corroboration

outputs/full/summary.json records the older finite-prompt suite: 18,144
query-metric comparisons, 36 trained models, covariance reductions, and
Bayes-operator checks. Those values are useful corroboration, but they do not
prove the universal statements. The current theorem verdicts come from the
explicit proof and counterexample packets above.
