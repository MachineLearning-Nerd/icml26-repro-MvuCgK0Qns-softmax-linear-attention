# Current verification

This is the current verifier. It supersedes the verifier at judged Space
revision `2f4196b0ec25bad9979ac21e92543168c33090a9`, whose pages are preserved as
**Historical rejected baseline**.

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

Raw result: [raw_result.json](../../evidence/claim_1/raw_result.json)  
Contract: [claim_contract.json](../../evidence/claim_1/claim_contract.json)  
Executable verifier: [verify_claim_1.py](../../evidence/claim_1/verify_claim_1.py)  
Independent checker output: [independent_checker_output.txt](../../evidence/claim_1/independent_checker_output.txt)  
Negative-control output: [negative_control_output.txt](../../evidence/claim_1/negative_control_output.txt)

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

## Evaluator-visible evidence matrix — in-progress candidate

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | Current verification | Yes | Yes | Yes | Yes | Yes | Literal Proposition 3.1 | FALSIFIED |
| 2 | Pending | No | No | No | No | No | Pending | BLOCKED |
| 3 | Pending | No | No | No | No | No | Pending | BLOCKED |
| 4 | Pending | No | No | No | No | No | Pending | BLOCKED |
| 5 | Pending | No | No | No | No | No | Pending | BLOCKED |
