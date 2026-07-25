# Source audit — Theorem 5.1

- Paper source: https://ar5iv.labs.arxiv.org/html/2512.11784
- Retrieved with explicit `OpenResearch-Reproduction/1.0` User-Agent on 2026-07-25.
- Paper HTML SHA-256: `6ae468a4032e920d159b609a78f1860bdf90004c7a692df60c601d9e3c9ff4c2`.
- Theorem anchor: `S5.Thmtheorem1`; proof: Appendix E.2, `A5.SS2`.
- Lemma E.1 anchor: `A5.Thmtheorem1`.
- Primary cited source: https://www.jmlr.org/papers/volume25/23-1042/23-1042.pdf
- JMLR source retrieved with the same explicit User-Agent on 2026-07-25.
- JMLR PDF SHA-256: `3612edf523d550dfc549d1d47a0294f2bd2da7642bddfa56b8d4a0fa0bd93446`.

Theorem 5.1 quantifies over every invertible `Sigma` and initializes with
`0<alpha<sqrt(2)/(d^(1/4)||Sigma||_op)`. It claims the limiting finite-prompt
gradient-flow risk is within arbitrary epsilon of the Bayes risk for every
sufficiently large prompt.

Two proof dependencies do not cover that literal domain as written:

1. Lemma E.1 verifies Assumption 4.2 only when `||Sigma||_op<=1`, while
   Theorem 5.1 states only invertibility.
2. At infinite prompt, the cited JMLR Theorem 4 sufficient condition is
   `alpha^2 ||Sigma||_op sqrt(d)<2`. The paper's displayed interval does not
   imply this for `||Sigma||_op<1`: `d=1`, `||Sigma||=1/4`, `alpha=4` satisfies
   `alpha<4sqrt(2)` but has cited-condition left side `4`, not `<2`.

These are proof gaps, not counterexamples to the theorem. The exact Bayes
endpoint is independently verified; the full universal convergence claim is
therefore BLOCKED rather than mislabeled as falsified.
