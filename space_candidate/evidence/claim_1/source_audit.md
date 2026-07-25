# Source audit — Proposition 3.1

- Source: https://ar5iv.labs.arxiv.org/html/2512.11784
- Retrieved with explicit `OpenResearch-Reproduction/1.0` User-Agent on 2026-07-25.
- HTML SHA-256: `6ae468a4032e920d159b609a78f1860bdf90004c7a692df60c601d9e3c9ff4c2`.
- Anchor: Section 3, HTML `S3.Thmtheorem1`.
- PDF SHA-256: `3e1c12c82e55e253f2933c139a676b1a642e552637a17ca273e3f0dc47423ede`.

The proposition assumes centered sub-Gaussian measures `mu` and `nu` with
parameters `sigma >= 1` and `1`, plus
`||T[mu]||_L4(nu) <= sigma^2 M < infinity`. It states that positive constants
`c1,c2`, depending only on `d,V,K,Q,M`, satisfy

`E[||T[mu_hat_L]-T[mu]||^2_L2(nu)] <= c1 sigma^6 ln(L) / L^(c2/sigma^2)`.

The displayed statement contains no `L >= 2` or sufficiently-large-`L`
qualification. The falsification contract therefore uses the literal positive
integer domain at `L=1`. If the authors intended an unstated lower bound, that
repaired theorem is outside this certificate.
