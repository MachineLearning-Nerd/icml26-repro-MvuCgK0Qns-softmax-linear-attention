# Method

Use the scalar instance `mu=nu=N(0,1)`, `U=0`, `V=1`, and `L=1`.
With one token, finite attention is `V X` regardless of `U`. Its derivative
with respect to `V` is therefore `X`, and its derivative with respect to `U`
is zero. Lemma 2.1 gives population attention `V U Z`; at the witness it has
`V`-derivative zero and `U`-derivative `Z`. Consequently both expected squared
gradient errors equal the exact standard-Gaussian second moment `1`.

Both advertised right sides are zero for every permitted positive `c1,c2`
because they contain `ln(1)` or `ln(1)^2`.

At `U=0` the exponential tilt in Assumption 3.3 is exactly one. Its nine left
sides reduce to `E|X|^p E|Z|^q`; selecting `M_pq` as the finite product of
moments `1,3,105` satisfies every condition with equality.

The primary verifier checks the source hash, witness, all nine moment bounds,
and both exact contradictions. A separate rational-arithmetic script
reconstructs the calculation without importing reproduction code. The
negative control uses `mu=nu=delta_0`, which satisfies the assumptions but
has zero error and must be rejected as a counterexample.
