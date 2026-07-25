# Method

Let `r_infinity=lim_t R_infinity(theta_infinity(t))`. For arbitrary
`epsilon>0`, choose a finite `T` with
`R_infinity(theta_infinity(T))<=r_infinity+epsilon/2`.

Lemma D.1 gives, on this fixed horizon, a trajectory gap at most
`g2(L) T exp(beta_infinity T)` with `g2(L)->0`. Corollary D.3 gives a uniform
risk gap `g1(L)->0` on the required ball. Since the infinite risk is Lipschitz
there, choose one `L(epsilon)` so their combined contribution at `T` is at
most `epsilon/2`. Thus `R_L(theta_L(T))<=r_infinity+epsilon`.

Along the finite gradient flow,
`d R_L(theta_L(t))/dt=-||grad R_L(theta_L(t))||^2<=0`. As a risk is bounded
below, its limit exists and is at most its value at `T`, proving the theorem.

The primary verifier checks the source, assumptions, fixed Gronwall constant,
exact epsilon ledger, energy identity, and order chain. The independent checker
rebuilds the order proof with rational arithmetic. A control deliberately
removes monotonicity and makes risk grow after `T`; it must be rejected.
