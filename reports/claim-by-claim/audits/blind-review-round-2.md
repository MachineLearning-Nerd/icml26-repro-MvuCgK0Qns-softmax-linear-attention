# Evaluator-blind review — round 2

The review began at `README.md` in a fresh candidate tree and used only
links reachable from that canonical entrypoint. No repository or run-log
knowledge was used to fill gaps.

## Claim discoverability

| Claim | Exact result inline | Complete packet reachable | Reviewer verdict | Missing or conclusion |
|---|---|---|---|---|
| 1 | Yes | Yes | FALSIFIED | All required evidence discoverable |
| 2 | Yes | Yes | FALSIFIED | All required evidence discoverable |
| 3 | Yes | Yes | VERIFIED | All required evidence discoverable |
| 4 | Yes | Yes | VERIFIED | All required evidence discoverable |
| 5 | Yes | Yes | BLOCKED | All required evidence discoverable |

## Global gates

- PASS — Current verifier is linked directly by README
- PASS — Historical rejected baseline is reachable
- PASS — Fixed command is inline
- PASS — Git SHA and 18/18 result are inline
- PASS — Actual CPU quota and runtime are inline
- PASS — Visibility matrix has five terminal verdict rows

## Every file opened

- `README.md`
- `pages/current-verification/page.md`
- `pages/historical-rejected-baseline/page.md`
- `evidence/claim_1/raw_result.json`
- `evidence/claim_1/claim_contract.json`
- `evidence/claim_1/verify_claim_1.py`
- `evidence/claim_1/verifier_output.txt`
- `evidence/claim_1/independent_check.py`
- `evidence/claim_1/independent_checker_output.txt`
- `evidence/claim_1/negative_control.py`
- `evidence/claim_1/negative_control_output.txt`
- `evidence/claim_1/source_audit.md`
- `evidence/claim_1/method.md`
- `evidence/claim_1/command.txt`
- `evidence/claim_1/environment.md`
- `evidence/claim_1/limitations.md`
- `evidence/claim_1/EVAL.md`
- `evidence/claim_2/raw_result.json`
- `evidence/claim_2/claim_contract.json`
- `evidence/claim_2/verify_claim_2.py`
- `evidence/claim_2/verifier_output.txt`
- `evidence/claim_2/independent_check.py`
- `evidence/claim_2/independent_checker_output.txt`
- `evidence/claim_2/negative_control.py`
- `evidence/claim_2/negative_control_output.txt`
- `evidence/claim_2/source_audit.md`
- `evidence/claim_2/method.md`
- `evidence/claim_2/command.txt`
- `evidence/claim_2/environment.md`
- `evidence/claim_2/limitations.md`
- `evidence/claim_2/EVAL.md`
- `evidence/claim_3/raw_result.json`
- `evidence/claim_3/claim_contract.json`
- `evidence/claim_3/verify_claim_3.py`
- `evidence/claim_3/verifier_output.txt`
- `evidence/claim_3/independent_check.py`
- `evidence/claim_3/independent_checker_output.txt`
- `evidence/claim_3/negative_control.py`
- `evidence/claim_3/negative_control_output.txt`
- `evidence/claim_3/source_audit.md`
- `evidence/claim_3/method.md`
- `evidence/claim_3/command.txt`
- `evidence/claim_3/environment.md`
- `evidence/claim_3/limitations.md`
- `evidence/claim_3/EVAL.md`
- `evidence/claim_4/raw_result.json`
- `evidence/claim_4/claim_contract.json`
- `evidence/claim_4/verify_claim_4.py`
- `evidence/claim_4/verifier_output.txt`
- `evidence/claim_4/independent_check.py`
- `evidence/claim_4/independent_checker_output.txt`
- `evidence/claim_4/negative_control.py`
- `evidence/claim_4/negative_control_output.txt`
- `evidence/claim_4/source_audit.md`
- `evidence/claim_4/method.md`
- `evidence/claim_4/command.txt`
- `evidence/claim_4/environment.md`
- `evidence/claim_4/limitations.md`
- `evidence/claim_4/EVAL.md`
- `evidence/claim_5/raw_result.json`
- `evidence/claim_5/claim_contract.json`
- `evidence/claim_5/verify_claim_5.py`
- `evidence/claim_5/verifier_output.txt`
- `evidence/claim_5/independent_check.py`
- `evidence/claim_5/independent_checker_output.txt`
- `evidence/claim_5/negative_control.py`
- `evidence/claim_5/negative_control_output.txt`
- `evidence/claim_5/source_audit.md`
- `evidence/claim_5/method.md`
- `evidence/claim_5/command.txt`
- `evidence/claim_5/environment.md`
- `evidence/claim_5/limitations.md`
- `evidence/claim_5/EVAL.md`
- `pages/00-scored-evidence-summary/page.md`
- `pages/claim-1-gaussian-affine-limit/page.md`
- `pages/claim-2-concentration-and-gradient-stability/page.md`
- `pages/claim-3-optimization-transfer/page.md`
- `pages/methods-tests-and-provenance/page.md`
- `pages/limitations-and-negative-controls/page.md`
- `pages/conclusion/page.md`
- `historical/judged-2f4196b0/README.md`
- `historical/judged-2f4196b0/logbook.json`
- `historical/judged-2f4196b0/index.md`

## Conclusions that could not be verified

- None.

**Round result: PASS.**
