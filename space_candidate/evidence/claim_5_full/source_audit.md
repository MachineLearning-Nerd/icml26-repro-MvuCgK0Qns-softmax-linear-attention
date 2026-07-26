# Source audit — Theorem 5.1 full-domain certificate

- Judged source snapshot: <https://ar5iv.labs.arxiv.org/html/2512.11784>,
  retrieved 2026-07-25 with `OpenResearch-Reproduction/1.0`, SHA-256
  `6ae468a4032e920d159b609a78f1860bdf90004c7a692df60c601d9e3c9ff4c2`.
- Current arXiv v2 HTML: <https://arxiv.org/html/2512.11784v2>, retrieved
  2026-07-26 with the same User-Agent, SHA-256
  `96c0673a1e0abd5e677ef1dfd06d1f768fc72f95904de6d6cbb8ec80f92db2c2`.
- The judged statement is Theorem 5.1 at `S5.Thmtheorem1`. In v2 the same
  training conclusion is Theorem 5.2 at `S5.Thmtheorem2`, with proof
  `A6.SS2` and covariance lemma `A6.Thmtheorem1`.
- Primary cited source: Zhang, Frei, and Bartlett, *Trained Transformers Learn
  Linear Models In-Context*, JMLR 25 (2024), retrieved 2026-07-25, SHA-256
  `3612edf523d550dfc549d1d47a0294f2bd2da7642bddfa56b8d4a0fa0bd93446`.

The contract is universal over every positive-definite `Sigma`, the displayed
balanced initialization with
`0<alpha<sqrt(2)/(d^(1/4)||Sigma||_op)`, every `epsilon>0`, and all sufficiently
large prompt lengths. The direct proof below covers every `alpha>0`, so it
does not use the narrower sufficient condition in the cited JMLR theorem.

The v2 covariance lemma still writes `||Sigma||_op<=1`. The transfer audit
therefore reconstructs the scale dependence rather than silently treating
that lemma as universal.
