# Method

Set `a=K^T Q z` and represent every Gaussian vector with PSD covariance as
`X=m+B G`, where `G~N(0,I)` and `Gamma=B B^T`. Complete the square:

`a^T(m+B g)-||g||^2/2`

`= a^T m + ||B^T a||^2/2 - ||g-B^T a||^2/2`.

Translation invariance of the Gaussian integral gives

`F(a)=E exp(a^T X)=exp(a^T m+a^T Gamma a/2)`.

The finite moment-generating function can be differentiated, so

`E[X exp(a^T X)] = grad_a F(a)`

`= (m+Gamma a) F(a)`.

Multiplying by `V`, dividing by the strictly positive `F(a)`, and substituting
`a=K^T Q z` yields the lemma exactly.

The primary verifier reduces the completion-of-square equality to coefficients
of abstract scalar contractions and checks every proof step. The independent
checker builds sparse multivariate polynomials with rational coefficients for
generated dimensions `1,2,3,4,8,16`, including rank-deficient rectangular
`B`, and confirms coefficient equality exactly. A Rademacher control at
`a=2` has attention `tanh(2)<1`, not the Gaussian prediction `2`, and must be
rejected with exit code 1.
