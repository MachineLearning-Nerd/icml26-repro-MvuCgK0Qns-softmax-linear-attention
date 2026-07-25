# Source audit — Theorem 4.3

- Source: https://ar5iv.labs.arxiv.org/html/2512.11784
- Retrieved with explicit `OpenResearch-Reproduction/1.0` User-Agent on 2026-07-25.
- HTML SHA-256: `6ae468a4032e920d159b609a78f1860bdf90004c7a692df60c601d9e3c9ff4c2`.
- Theorem anchor: `S4.Thmtheorem3`.
- Assumption 4.2 anchor: `S4.Thmtheorem2`.
- Proof anchor: Appendix D.1, `A4.SS1`.
- Trajectory lemma: `A4.Thmtheorem1`; risk corollary: `A4.Thmtheorem3`.
- PDF SHA-256: `3e1c12c82e55e253f2933c139a676b1a642e552637a17ca273e3f0dc47423ede`.

The theorem assumes a 1-smooth loss with first-argument gradient zero at the
origin, `C^2` infinite risk, a bounded infinite gradient-flow trajectory, and
Assumption 4.2. Its exact quantifiers are `for every epsilon>0`, `there exists
L(epsilon)`, `for every L>=L(epsilon)`.

Appendix D.1 first obtains `+2 epsilon` and then uses the arbitrariness of
epsilon; the certificate makes this relabeling explicit by allocating
`epsilon/2` to the infinite-flow tail and `epsilon/2` to the finite/infinite
comparison.

One proof display writes `beta_L`, but Lemma D.1 equations (22)-(24) define and
use the fixed `beta_infinity`, the Lipschitz constant of the infinite-risk
gradient on the compact ball. The fixed constant is required for
`g2(L) T exp(beta_infinity T)->0` and is the version certified here.
