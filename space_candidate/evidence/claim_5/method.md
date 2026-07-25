# Method and three research routes

## Route 1 — compositional proof audit

Trace Appendix E.2 through Theorem 4.3, Lemma E.1, and the primary JMLR
convergence theorem. This identifies two exact domain implications that do not
close: the covariance normalization and the initialization condition.

## Route 2 — direct Bayes algebra

Write `c=tr(Sigma^-2)^(1/4)`. The advertised limits have top block
`U*=c^-1 Sigma^-1` and bottom selector `V*=c`. For
`Gamma_w=[[Sigma,Sigma w],[w^T Sigma,w^T Sigma w]]`,

`V* Gamma_w U*(x,0)` has last coordinate `w^T x`.

Thus squared error is pointwise zero for every `w,x`, every dimension, and
every invertible anisotropic `Sigma`. Since squared loss is nonnegative, this
endpoint is exactly Bayes optimal.

## Route 3 — boundary dynamics and condition audit

For `d=1`, `Sigma=s>0`, balanced initialization reduces the infinite-flow ODE
to `x'=s^2 x(1-s x^2)`. Every `alpha>0` converges to `x=1/sqrt(s)`, so the
condition mismatch does not falsify the theorem in the scalar case. For
general `d`, the exact `d=1,s=1/4,alpha=4` arithmetic proves only that the
published range does not imply the cited sufficient condition.

The primary verifier checks all exact subresults and exits 2 because the two
universal dependencies remain unresolved. A tampered subcertificate exits 1.
The independent checker performs rational block algebra for several
anisotropic matrices. The negative control replaces `Sigma^-1` by `I` and
must produce nonzero anisotropic error.
