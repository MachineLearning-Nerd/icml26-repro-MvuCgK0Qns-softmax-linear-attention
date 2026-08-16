# Source and claim audit

This file defines which paper and code artifacts the current conclusions refer
to. A verdict is not intended to float across paper revisions or repository
changes without a new audit.

## Paper identity

- Title: **Softmax as Linear Attention in the Large-Prompt Regime: a Measure-based Perspective**
- Authors: Etienne Boursier and Claire Boyer
- OpenReview: `MvuCgK0Qns`
- arXiv identifier: `2512.11784`
- Local paper PDF: `paper.pdf`
- PDF SHA-256: `3e1c12c82e55e253f2933c139a676b1a642e552637a17ca273e3f0dc47423ede`
- Primary judged HTML source: https://ar5iv.labs.arxiv.org/html/2512.11784
- Judged HTML retrieval date: 2026-07-25
- Judged HTML SHA-256: `6ae468a4032e920d159b609a78f1860bdf90004c7a692df60c601d9e3c9ff4c2`
- Latest source: https://arxiv.org/html/2512.11784v2
- Latest source retrieval date: 2026-07-26
- Latest source SHA-256: `96c0673a1e0abd5e677ef1dfd06d1f768fc72f95904de6d6cbb8ec80f92db2c2`

The judged source calls the final result Theorem 5.1. arXiv v2 moves the
corresponding result to Theorem 5.2 and changes its proof anchor. The Claim 5
packet records both anchors explicitly.

## Official-code boundary

The paper's official repository is
https://github.com/eboursier/softmax_as_linear.git at pinned commit
`8fa49b308eaac168bc4edcdc06f26703ac4520f8`. The snapshot under
`source/official-snapshot` is retained for provenance and audit notes.

The current reproduction imports no official module. Its data generation,
exact certificates, independent checkers, and negative controls are separate
files under `reproduction/` and `space_candidate/evidence/`. A discrepancy in
the official helper path is therefore recorded as a source-audit observation,
not silently treated as ground truth.

## Claim mapping

### Proposition 3.1

The literal displayed bound contains `ln(L)`. The contract therefore tests the
unqualified positive-integer boundary `L=1`. The witness in
`space_candidate/evidence/claim_1/claim_contract.json` satisfies the Gaussian
assumptions and gives exact left side one and right side zero. The independent
checker and the `delta_0` control are both part of the verdict.

### Proposition 3.4

The contract includes Assumption 3.3 and its nine moment products. The
one-dimensional Gaussian witness has finite exact moments of orders 0, 4, and
8, while both displayed gradient bounds vanish at `L=1`. The independent
checker reconstructs both gradients; a degenerate zero-error distribution is
kept as a negative control.

### Lemma 2.1

For `X=m+BG` and `Gamma=BB^T`, completion of the square gives the Gaussian
normalizer and its derivative. The proof covers rank-deficient covariance
through the factorization, and the independent checker reconstructs exact
polynomial coefficients in dimensions 1, 2, 3, 4, 8, and 16. A Rademacher
control establishes that the affine identity is Gaussian-specific.

### Theorem 4.3

The checker follows the source proof's quantifiers: choose finite time using
the infinite-flow limit, choose a prompt length using both error budgets, and
then use non-increasing gradient-flow risk to pass from that time to the
limit. The control removes monotonicity and is rejected.

### Theorem 5.1 / Theorem 5.2

The full-domain packet derives the population risk
`R_inf(A,b)=1/2 tr((b Sigma A-I) Sigma (b Sigma A-I)^T)`, proves the balanced
invariant `||A||_F^2-b^2=0`, excludes the origin, identifies the unique
stationary endpoint, and verifies exact Bayes risk zero. A separate finite
covariance-scale argument supplies the moment and tail bounds needed by the
transfer theorem. The old packet remains marked blocked because it documents
the earlier dependency gap rather than the final proof.

## Interpretation boundary

The two falsifications are about the literal published contracts. The proof
certificates are scoped to their stated source versions, mathematical model,
and assumptions. Historical numerical output under `outputs/full` is
corroboration; it is not substituted for a universal proof.
