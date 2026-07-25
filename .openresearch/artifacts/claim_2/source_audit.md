# Source audit — Proposition 3.4

- Source: https://ar5iv.labs.arxiv.org/html/2512.11784
- Retrieved with explicit `OpenResearch-Reproduction/1.0` User-Agent on 2026-07-25.
- HTML SHA-256: `6ae468a4032e920d159b609a78f1860bdf90004c7a692df60c601d9e3c9ff4c2`.
- Proposition anchor: Section 3, HTML `S3.Thmtheorem4`.
- Assumption anchor: Section 3, HTML `S3.Thmtheorem3`.
- PDF SHA-256: `3e1c12c82e55e253f2933c139a676b1a642e552637a17ca273e3f0dc47423ede`.

Assumption 3.3 requires centered `sigma`- and `1`-sub-Gaussian `mu,nu` and,
for every `p,q` in `{0,4,8}`, a finite `M_pq` satisfying the displayed
exponentially tilted moment bound. Proposition 3.4 then states positive
constants `c1,c2`, depending only on `d,U,V`, for which the `V`-gradient error
is bounded by

`c1 sigma^6 ln(L) / L^(c2/sigma^2)`

and the `U`-gradient error is bounded by

`c1 sigma^12 ln(L)^2 / L^(c2/sigma^2)`.

Neither display contains an `L >= 2` or sufficiently-large-`L` qualification.
The literal contract therefore includes `L=1`. For `U=0` and standard
Gaussians, every Assumption 3.3 bound is audited explicitly from moments
`E|G|^0=1`, `E|G|^4=3`, and `E|G|^8=105`.
