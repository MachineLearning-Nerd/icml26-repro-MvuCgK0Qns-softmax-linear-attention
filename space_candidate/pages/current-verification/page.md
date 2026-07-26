# Current verification

This is the current verifier. It supersedes the verifier at judged Space
revision `2f4196b0ec25bad9979ac21e92543168c33090a9`, whose pages are preserved as
[**Historical rejected baseline**](../historical-rejected-baseline/page.md).

## Claim 1 — Proposition 3.1

Verdict: **FALSIFIED** for the literal published statement.

Source: arXiv `2512.11784`, Section 3, Proposition 3.1, HTML anchor
`S3.Thmtheorem1`. The HTML was retrieved on 2026-07-25 with an explicit browser
User-Agent and hashes to
`6ae468a4032e920d159b609a78f1860bdf90004c7a692df60c601d9e3c9ff4c2`.

The proposition assumes centered sub-Gaussian `mu,nu` and states

`E[||T[mu_hat_L]-T[mu]||²_L2(nu)] <= c1 sigma^6 ln(L)/L^(c2/sigma²)`

without an `L>=2` or sufficiently-large-`L` qualifier.

Take `d=1`, `L=1`, `mu=nu=N(0,1)`, `sigma=1`, `K=0`, `Q=V=M=1`.
Every assumption holds and `T[mu]=0`. A one-token empirical prompt contains
`X~N(0,1)` and finite attention is exactly `X`, so

`LHS = E[X²] = 1`, while `RHS = c1 ln(1) = 0`

for every allowed `c1,c2>0`. This is an exact quantified contradiction, not a
toy-scale extrapolation.

- Raw result: [raw_result.json](../../evidence/claim_1/raw_result.json)
- Contract: [claim_contract.json](../../evidence/claim_1/claim_contract.json)
- Executable verifier: [verify_claim_1.py](../../evidence/claim_1/verify_claim_1.py)
- Verifier output: [verifier_output.txt](../../evidence/claim_1/verifier_output.txt)
- Independent checker: [independent_check.py](../../evidence/claim_1/independent_check.py)
- Independent checker output: [independent_checker_output.txt](../../evidence/claim_1/independent_checker_output.txt)
- Negative control: [negative_control.py](../../evidence/claim_1/negative_control.py)
- Negative-control output: [negative_control_output.txt](../../evidence/claim_1/negative_control_output.txt)

Audit packet: [source](../../evidence/claim_1/source_audit.md) ·
[method](../../evidence/claim_1/method.md) ·
[fixed command](../../evidence/claim_1/command.txt) ·
[environment/CPU](../../evidence/claim_1/environment.md) ·
[limitations](../../evidence/claim_1/limitations.md) ·
[evaluation record](../../evidence/claim_1/EVAL.md)

Primary verifier output:

```text
PASS: assumptions hold; exact LHS=1 > RHS=0 for every c1,c2>0.
```

Independent reconstruction:

```text
PASS independent reconstruction: Gaussian moment LHS=1; ln(1) makes RHS=0.
```

Negative control (`mu=delta_0`) is a valid assumption-satisfying instance but
has `LHS=RHS=0`; the counterexample detector rejects it with the intended exit
code 1.

Interpretation risk: if the authors intended an unstated `L>=2` or
sufficiently-large-`L` restriction, this witness does not falsify that repaired
statement. The published proposition does not state the repair.

## Claim 2 — Proposition 3.4

Verdict: **FALSIFIED** for the literal published statement.

Source: arXiv `2512.11784`, Section 3, Proposition 3.4, HTML anchor
`S3.Thmtheorem4`; the moment condition is Assumption 3.3 at
`S3.Thmtheorem3`. The same source hash and retrieval record above apply.

The proposition gives two bounds under Assumption 3.3:

- `V`-gradient squared error at most
  `c1 sigma^6 ln(L)/L^(c2/sigma²)`;
- `U`-gradient squared error at most
  `c1 sigma^12 ln(L)^2/L^(c2/sigma²)`.

Neither display qualifies the positive-integer prompt length with `L>=2` or
“sufficiently large.” Take `d=1`, `L=1`, `mu=nu=N(0,1)`, `sigma=1`, `U=0`,
and `V=1`. A one-token attention output is `VX`, so its `V`-gradient is `X`
and its `U`-gradient is zero. Gaussian population attention is `VUZ`, whose
respective gradients at the witness are zero and `Z`. Therefore

`V-gradient LHS = E[X²] = 1 > 0 = RHS`

and

`U-gradient LHS = E[Z²] = 1 > 0 = RHS`

for every allowed `c1,c2>0`.

This witness also satisfies every case of Assumption 3.3. At `U=0`, the
exponential tilt is one; for `p,q in {0,4,8}`, choose
`M_pq=E|X|^p E|Z|^q`. The required moments are exactly `1,3,105`, so all nine
bounds are finite and hold with equality.

- Raw result: [raw_result.json](../../evidence/claim_2/raw_result.json)
- Contract: [claim_contract.json](../../evidence/claim_2/claim_contract.json)
- Executable verifier: [verify_claim_2.py](../../evidence/claim_2/verify_claim_2.py)
- Verifier output: [verifier_output.txt](../../evidence/claim_2/verifier_output.txt)
- Independent checker: [independent_check.py](../../evidence/claim_2/independent_check.py)
- Independent output: [independent_checker_output.txt](../../evidence/claim_2/independent_checker_output.txt)
- Negative control: [negative_control.py](../../evidence/claim_2/negative_control.py)
- Negative-control output: [negative_control_output.txt](../../evidence/claim_2/negative_control_output.txt)
- Source audit: [source_audit.md](../../evidence/claim_2/source_audit.md)
- Method: [method.md](../../evidence/claim_2/method.md)
- Fixed command: [command.txt](../../evidence/claim_2/command.txt)
- Environment and CPU: [environment.md](../../evidence/claim_2/environment.md)
- Limitations: [limitations.md](../../evidence/claim_2/limitations.md)
- Evaluation record: [EVAL.md](../../evidence/claim_2/EVAL.md)

Primary verifier output:

```text
PASS: Assumption 3.3 holds; exact V- and U-gradient errors each have LHS=1 > RHS=0 for every c1,c2>0.
```

The independent reconstruction imports no reproduction code and checks all
nine moment products using exact integer arithmetic. The valid
`mu=nu=delta_0` control has zero gradient errors and is rejected with the
intended exit code 1.

Interpretation risk: an unstated `L>=2` or sufficiently-large-`L` restriction
would repair this boundary defect; this certificate tests the proposition as
published.

## Claim 3 — Lemma 2.1

Verdict: **VERIFIED**.

Source: arXiv `2512.11784`, Section 2, Lemma 2.1, HTML anchor
`S2.Thmtheorem1`. The lemma states, for every Gaussian
`mu=N(m,Gamma)` and every compatible `z`,

`T^{K,Q,V}[mu](z) = V m + V Gamma K^T Q z`.

This candidate replaces the historical `d=1–3` quadrature proxy with a
dimension-free symbolic certificate. Let `a=K^T Q z` and represent every
Gaussian with PSD covariance, including singular cases, as
`X=m+B G`, `G~N(0,I)`, `Gamma=B B^T`. Completing the square gives

`a^T(m+B g)-||g||²/2`

`=a^T m+||B^T a||²/2-||g-B^T a||²/2`.

Hence the Gaussian normalizer is

`F(a)=E exp(a^T X)=exp(a^T m+a^T Gamma a/2)`.

Differentiation gives the tilted first moment

`E[X exp(a^T X)]=(m+Gamma a)F(a)`.

The strictly positive normalizer cancels in attention, leaving
`V(m+Gamma a)`; substituting `a=K^T Q z` is exactly the published identity.
This derivation is valid for arbitrary dimension and does not extrapolate from
a finite sweep.

- Raw proof result: [raw_result.json](../../evidence/claim_3/raw_result.json)
- Contract: [claim_contract.json](../../evidence/claim_3/claim_contract.json)
- Executable verifier: [verify_claim_3.py](../../evidence/claim_3/verify_claim_3.py)
- Verifier output: [verifier_output.txt](../../evidence/claim_3/verifier_output.txt)
- Independent exact-polynomial checker: [independent_check.py](../../evidence/claim_3/independent_check.py)
- Independent output: [independent_checker_output.txt](../../evidence/claim_3/independent_checker_output.txt)
- Negative control: [negative_control.py](../../evidence/claim_3/negative_control.py)
- Negative-control output: [negative_control_output.txt](../../evidence/claim_3/negative_control_output.txt)
- Source audit: [source_audit.md](../../evidence/claim_3/source_audit.md)
- Method: [method.md](../../evidence/claim_3/method.md)
- Fixed command: [command.txt](../../evidence/claim_3/command.txt)
- Environment and CPU: [environment.md](../../evidence/claim_3/environment.md)
- Limitations: [limitations.md](../../evidence/claim_3/limitations.md)
- Evaluation record: [EVAL.md](../../evidence/claim_3/EVAL.md)

Primary verifier output:

```text
PASS: dimension-free Gaussian MGF derivation yields T[mu](z)=V m+V Gamma K^T Q z for every d and PSD Gamma.
```

The independent checker imports no reproduction code and exactly expands 380
sparse-polynomial coefficients across generated dimensions
`1,2,3,4,8,16`, including rank-deficient covariance factors. The Rademacher
control gives `tanh(2)=0.964...`, not `2`, and is rejected with exit code 1.

Scope: this verifies the exact operator identity in judged Claim 3. The
lemma's additional pushforward-law statement is not part of that imported
claim and is not silently credited here.

## Claim 4 — Theorem 4.3

Verdict: **VERIFIED**.

Source: Section 4, Theorem 4.3 (`S4.Thmtheorem3`), with proof in Appendix D.1
(`A4.SS1`). The exact claim is:

`for every epsilon>0, there exists L(epsilon), such that for every L>=L(epsilon),`

`lim_t R_L(theta_L(t)) <= lim_t R_infinity(theta_infinity(t)) + epsilon`.

This is now checked as an arbitrary-epsilon proof rather than inferred from the
historical 36-model proxy. Under the stated assumptions, Corollary D.3 gives a
uniform finite/infinite risk gap `g1(L)->0`. Lemma D.1 and Gronwall give, on
any fixed horizon,

`||theta_L(t)-theta_infinity(t)||`

`<=g2(L) t exp(beta_infinity t)`, with `g2(L)->0`.

For an arbitrary target `epsilon`, choose `T` so the infinite-flow tail costs
at most `epsilon/2`, then choose one `L(epsilon)` so the risk and trajectory
comparison at that fixed `T` costs at most `epsilon/2`. Exact rational
arithmetic checks that the budget is `1/2+1/2=1`.

Finally, along the finite gradient flow,

`d R_L/dt = -||grad R_L||² <= 0`.

Therefore its limiting risk is no larger than its already-bounded value at
`T`, establishing the published quantified conclusion.

- Raw proof result: [raw_result.json](../../evidence/claim_4/raw_result.json)
- Contract: [claim_contract.json](../../evidence/claim_4/claim_contract.json)
- Executable verifier: [verify_claim_4.py](../../evidence/claim_4/verify_claim_4.py)
- Verifier output: [verifier_output.txt](../../evidence/claim_4/verifier_output.txt)
- Independent order checker: [independent_check.py](../../evidence/claim_4/independent_check.py)
- Independent output: [independent_checker_output.txt](../../evidence/claim_4/independent_checker_output.txt)
- Negative control: [negative_control.py](../../evidence/claim_4/negative_control.py)
- Negative-control output: [negative_control_output.txt](../../evidence/claim_4/negative_control_output.txt)
- Source audit: [source_audit.md](../../evidence/claim_4/source_audit.md)
- Method: [method.md](../../evidence/claim_4/method.md)
- Fixed command: [command.txt](../../evidence/claim_4/command.txt)
- Environment and CPU: [environment.md](../../evidence/claim_4/environment.md)
- Limitations: [limitations.md](../../evidence/claim_4/limitations.md)
- Evaluation record: [EVAL.md](../../evidence/claim_4/EVAL.md)

Primary verifier output:

```text
PASS: for arbitrary epsilon, two exact epsilon/2 budgets plus gradient-flow monotonicity prove the full Theorem 4.3 limiting-risk bound.
```

Source audit: one Appendix D.1 display writes `beta_L`, but the underlying
Lemma D.1 equations (22)-(24) establish and use the fixed `beta_infinity`
Lipschitz constant. The fixed version is necessary and is what this certificate
checks. The source proof's final `2 epsilon` is resolved explicitly by starting
with `epsilon/2`.

The control matches the finite risk at `T` but removes monotonicity and lets it
grow afterwards; it is rejected with exit code 1. No explicit numerical
`L(epsilon)` is claimed because the theorem and supporting constants are
qualitative.

## Claim 5 — Theorem 5.1

Verdict: **VERIFIED**. Confidence: **HIGH**.

The exact published contract quantifies over every invertible `Sigma`, every
Equation (9) initialization with

`0<alpha<sqrt(2)/(d^(1/4)||Sigma||_op)`,

and every sufficiently large prompt length. It concludes that finite-softmax
gradient-flow risk approaches the Bayes risk.

The previous packet proved the endpoint but remained BLOCKED because the cited
JMLR theorem used a narrower initialization condition and the paper's
assumption lemma wrote `||Sigma||_op<=1`. The
[Historical rejected baseline](../historical-rejected-claim-5/page.md) is
preserved unchanged. The current verifier removes both dependencies with a
direct full-domain proof.

Let the preserved trainable blocks be a matrix `A` and scalar `b`. Gaussian
integration gives the exact infinite-prompt risk

`R(A,b)=1/2 tr((b Sigma A-I) Sigma (b Sigma A-I)^T)`.

Its gradient flow is

`A_dot=b Sigma^2-b^2 Sigma^2 A Sigma`,

`b_dot=tr(A^T Sigma^2)-b tr(A^T Sigma^2 A Sigma)`.

The paper's initialization satisfies the invariant
`||A(t)||_F^2-b(t)^2=0`. Since `b(0)>0`, it cannot cross zero: balancedness
would force `A=0`, and ODE uniqueness would contradict the nonzero
initialization. Loss sublevels are bounded because `Sigma` is positive
definite, and this bounded real-analytic gradient trajectory converges to a
stationary point. On the balanced manifold, a stationary point is either the
origin or satisfies `b A Sigma=I`, hence also `b Sigma A=I`.

The origin is impossible. Diagonalize `Sigma=diag(s_i)` and write
`a_i=A_ii`. Since `A(0)=alpha Theta Theta^T`, all `a_i(0)>=0`, at least one is
positive, and

`a_i_dot=b s_i^2(1-b s_i a_i)`

points strictly inward at `a_i=0`. Hence `tr(A)>0`. Near the origin,

`tr(A)_dot=b sum_i s_i^2-b^2 sum_i s_i^3 a_i`

`>=(b/2) sum_i s_i^2>0`,

using `|a_i|<=||A||_F=b`. A positive trace cannot converge to zero while
eventually increasing. Therefore the limit is the zero-risk stationary point.
Balancedness fixes it uniquely:

`b=tr(Sigma^-2)^(1/4)`,

`A=tr(Sigma^-2)^(-1/4) Sigma^-1`.

This proof holds for every `alpha>0`, stronger than the displayed interval.

For arbitrary covariance scale, put
`tau=sqrt(||Sigma||_op)<infinity`. Writing `x_query=tau g` with `g`
1-sub-Gaussian only rescales the bounded parameter in the concentration
estimates. Conditionally on `w`, a valid prompt-token sub-Gaussian envelope is

`sigma_w^2=max(1,||Sigma||_op(1+||w||^2))`.

Its polynomial moments are finite. With `a=max(1,||Sigma||op)`, splitting
`X=||w||^2` at `sqrt(ln L)` bounds the two pieces by
`exp(-(c/(2a))sqrt(ln L))` and
`2^(d/2)exp(-sqrt(ln L)/4)`. Both still vanish after multiplication by
`ln(L)^4`. Gaussian exponential tilting gives
`N(Gamma_w U z,Gamma_w)`, so the remaining moments are polynomially bounded
on a bounded parameter ball. Thus finite covariance scale changes constants,
not the vanishing risk and gradient gaps used by Theorem 4.3.

Finally, write `c=tr(Sigma^-2)^(1/4)`. For

`Gamma_w=[[Sigma,Sigma w],[w^T Sigma,w^T Sigma w]]`,

block multiplication gives

`Gamma_w U*(x,0)=c^-1(x,w^T x)`,

so `V* Gamma_w U*(x,0)` predicts `w^T x` pointwise. Its squared error and risk
are exactly zero for every invertible anisotropic `Sigma`; nonnegative squared
loss makes this Bayes optimal.

- Raw proof result: [raw_result.json](../../evidence/claim_5_full/raw_result.json)
- Contract: [claim_contract.json](../../evidence/claim_5_full/claim_contract.json)
- Fail-closed verifier: [verify_claim_5.py](../../evidence/claim_5_full/verify_claim_5.py)
- Verifier output: [verifier_output.txt](../../evidence/claim_5_full/verifier_output.txt)
- Independent dynamics checker: [independent_check.py](../../evidence/claim_5_full/independent_check.py)
- Independent output: [independent_checker_output.txt](../../evidence/claim_5_full/independent_checker_output.txt)
- Negative control: [negative_control.py](../../evidence/claim_5_full/negative_control.py)
- Negative-control output: [negative_control_output.txt](../../evidence/claim_5_full/negative_control_output.txt)
- Source audit: [source_audit.md](../../evidence/claim_5_full/source_audit.md)
- Method: [method.md](../../evidence/claim_5_full/method.md)
- Fixed command: [command.txt](../../evidence/claim_5_full/command.txt)
- Environment and CPU: [environment.md](../../evidence/claim_5_full/environment.md)
- Limitations: [limitations.md](../../evidence/claim_5_full/limitations.md)
- Evaluation record: [EVAL.md](../../evidence/claim_5_full/EVAL.md)

Verifier output:

```text
PASS: direct balanced-gradient-flow proof converges to the exact zero-risk Bayes endpoint for every positive-definite Sigma and every published initialization; finite covariance scale changes transfer constants only.
```

The independent checker uses exact rational arithmetic and imports no
reproduction code. The control violates the balance invariant and is rejected
with exit code 1, so the proof cannot be applied outside its stated
initialization assumptions.

## Fixed command, environment, and cumulative result

Every experiment inherited this command unchanged:

```text
uv sync --frozen && uv run python reproduction/reproduce.py --output-dir outputs/full && uv run python -m unittest -v reproduction/test_reproduction.py
```

The sole repository `.venv` is defined by Python `3.12.*`, `pyproject.toml`,
and `uv.lock`. The full-domain scientific run used Git SHA
`64130159f3df3a0053280ffde22bb70a7c791265`, deterministic numerical seeds
`0,1,2`, and passed 20/20 tests in run
`fa29e4cb-51dc-4ede-93c6-40a6517816f4`. It ran on Hugging Face
`cpu-upgrade` in 37 seconds. The flavor advertises 8 vCPUs/32 GB; Linux
`cpu.max="800000 100000"` confirms the actual schedulable quota was 8.0 CPUs.
Each exact certificate records its own sub-second verifier runtime. No GPU was
used. The complete evaluator-facing surface was independently rerun at Git SHA
`2cf14723924197cb375b727d228631fa0e10ed16` in HF run
`af8297d4-fd11-4529-a905-b37f19153959`: 20/20 tests and the canonical traversal
passed in 37 seconds with the same 8.0-CPU cgroup quota.

## Evaluator-visible evidence matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | Current verification | Yes | Yes | Yes | Yes | Yes | Literal Proposition 3.1 | FALSIFIED |
| 2 | Current verification | Yes | Yes | Yes | Yes | Yes | Literal Proposition 3.4 and Assumption 3.3 | FALSIFIED |
| 3 | Current verification | Yes | Yes | Yes | Yes | Yes | Lemma 2.1 operator identity, all d and PSD Gamma | VERIFIED |
| 4 | Current verification | Yes | Yes | Yes | Yes | Yes | Full Theorem 4.3 quantifiers and assumptions | VERIFIED |
| 5 | Current verification | Yes | Yes | Yes | Yes | Yes | Full Theorem 5.1 covariance, initialization, convergence, transfer, and Bayes contract | VERIFIED |
