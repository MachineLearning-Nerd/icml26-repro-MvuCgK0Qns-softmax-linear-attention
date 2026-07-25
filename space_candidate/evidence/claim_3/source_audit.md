# Source audit — Lemma 2.1

- Source: https://ar5iv.labs.arxiv.org/html/2512.11784
- Retrieved with explicit `OpenResearch-Reproduction/1.0` User-Agent on 2026-07-25.
- HTML SHA-256: `6ae468a4032e920d159b609a78f1860bdf90004c7a692df60c601d9e3c9ff4c2`.
- Anchor: Section 2, HTML `S2.Thmtheorem1`.
- Proof anchor: Appendix A.
- PDF SHA-256: `3e1c12c82e55e253f2933c139a676b1a642e552637a17ca273e3f0dc47423ede`.

Lemma 2.1 assumes `mu=N(m,Gamma)` in `R^d` and states, for every `z in R^d`,

`T^{K,Q,V}[mu](z) = V m + V Gamma K^T Q z`.

It additionally states the Gaussian pushforward law. The imported judged Claim
3 concerns the operator identity; that exact universal identity is the contract
verified here. No dimension restriction or positive-definite restriction is
introduced: the proof uses `Gamma=B B^T`, which covers singular PSD covariance.
