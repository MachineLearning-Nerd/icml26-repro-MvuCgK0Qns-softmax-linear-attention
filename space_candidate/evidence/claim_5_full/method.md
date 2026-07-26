# Method — direct full-domain proof

Let the preserved parameter blocks be `A` and scalar `b`. Gaussian integration
reduces the infinite-prompt population risk to

`R(A,b)=1/2 tr((b Sigma A-I) Sigma (b Sigma A-I)^T)`.

Differentiation gives

`A_dot=b Sigma^2-b^2 Sigma^2 A Sigma`,

`b_dot=tr(A^T Sigma^2)-b tr(A^T Sigma^2 A Sigma)`.

## Convergence without the cited initialization restriction

The flow preserves `||A||_F^2-b^2=0`; the paper initializes both norms at
`alpha`. Since `b(0)>0`, `b` cannot cross zero: balancedness would force
`A=0`, and uniqueness of the ODE through that stationary point would
contradict the nonzero initialization. Loss sublevels are bounded on this
balanced manifold because
`Sigma` is positive definite. A bounded real-analytic gradient trajectory
converges to a stationary point.

At a stationary point with `b!=0`, the `A` equation gives `b A Sigma=I`,
hence `A=b^-1 Sigma^-1` and equivalently `b Sigma A=I`, the zero-risk
solution. If `b=0`, balancedness forces `A=0`, so the origin is the only
other stationary possibility.

Diagonalize `Sigma=diag(s_i)` and write `a_i=A_ii`. The exact diagonal dynamics
are

`a_i_dot=b s_i^2(1-b s_i a_i)`.

The initialization is `A(0)=alpha Theta Theta^T`, so all `a_i(0)>=0`, at least
one is positive, and any zero diagonal has strictly positive inward
derivative while `b>0`. Thus `tr(A)>0`. Moreover,

`tr(A)_dot=b sum_i s_i^2-b^2 sum_i s_i^3 a_i`.

Since `|a_i|<=||A||_F=b`, whenever
`b^2<sum_i s_i^2/(2 sum_i s_i^3)`,

`tr(A)_dot >= (b/2) sum_i s_i^2 > 0`.

Consequently a trajectory cannot converge to the origin: near it, its already
positive trace would be strictly increasing. The limit is therefore the
zero-risk stationary point. Balancedness uniquely fixes

`b=tr(Sigma^-2)^(1/4)` and
`A=tr(Sigma^-2)^(-1/4) Sigma^-1`.

This covers every `alpha>0`, stronger than the paper's displayed interval.

## Arbitrary covariance scale in the finite/infinite transfer

For fixed positive-definite `Sigma`, put
`tau=sqrt(||Sigma||_op)`. Writing `x_query=tau g` with `g` 1-sub-Gaussian and
replacing `U` by `tau U` inside the bounded-parameter estimates shows that
unit query scale only changes constants.

Conditionally on `w`, the prompt-token covariance has operator norm at most
`||Sigma||_op(1+||w||^2)`. Use
`sigma_w^2=max(1,||Sigma||_op(1+||w||^2))`. Its polynomial moments are finite.
For the logarithmic rate condition, split `||w||^2` at `sqrt(ln L)`: on the
bounded part the integrand is at most `exp(-C sqrt(ln L))`, while the
chi-square tail has the same exponential order up to a polynomial. Both beat
`ln(L)^4`.

Gaussian tilting is exactly
`N(Gamma_w U z,Gamma_w)`. On a bounded parameter ball, all required tilted
moments are polynomially bounded by `tau` and `sigma_w`. Thus the risk and
gradient gaps used in Theorem 4.3 still vanish for every fixed
positive-definite covariance. No formula-derived finite prompt threshold is
claimed.
