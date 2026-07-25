# Method

Use the scalar instance `mu=nu=N(0,1)`, `K=0`, `Q=V=1`, `sigma=M=1`.
The score is identically zero. For a one-token prompt `X`, finite attention is
exactly `X`; population attention is zero. Thus the theorem's left side is
`E[X^2]=1`. Its right side is zero for every permitted positive `c1,c2` because
`ln(1)=0`.

The primary verifier checks the source hash, witness, assumptions, and exact
values. A separate script reconstructs the moment with rational arithmetic and
imports no reproduction module. The negative control replaces `N(0,1)` by the
valid centered sub-Gaussian measure `delta_0`; both sides are zero, so the
counterexample detector must reject it with exit code 1.
