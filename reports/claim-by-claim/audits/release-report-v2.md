Previous live judged score: `8/10`

Conservative projected score range after the proposed change: **8–10/10**

Best-supported possible new score: **10/10 (forecast, not a judge result)**

# Final release report v2

## Claim summary

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| Proposition 3.1 | 2/2 | 2/2 | HIGH | FALSIFIED | Live judge accepted the exact `L=1` contradiction. Risk: an evaluator could infer an unstated large-`L` domain. |
| Proposition 3.4 | 2/2 | 2/2 | HIGH | FALSIFIED | Live judge accepted the exact output- and gradient-bound contradictions under all nine audited assumptions. Same unstated-domain interpretation risk. |
| Lemma 2.1 | 2/2 | 2/2 | HIGH | VERIFIED | Dimension-free Gaussian MGF proof, exact symbolic checker, and non-Gaussian control. |
| Theorem 4.3 | 2/2 | 2/2 | HIGH | VERIFIED | Arbitrary-`ε` finite-horizon transfer proof plus monotonic finite-flow risk. |
| Theorem 5.1 | 0/2 | 2/2 | HIGH | VERIFIED | Direct full-domain matrix-gradient-flow proof for every positive-definite `Σ` and every `α>0`, plus arbitrary-covariance scale transfer. New evaluator validation is the remaining risk. |

Current total score: **8/10 live judged**

Conservative projected total score range: **8–10/10**

Best-supported possible total score: **10/10 forecast**

Claims 1–4 are unchanged from the preceding live verdict. Claim 5 changes from
inconclusive to a direct `VERIFIED` certificate. No claim remains `BLOCKED`.
The exact publication action is an additive, text-only Hugging Face API commit
to the existing `DineshAI/MvuCgK0Qns` Space, followed by an exact-revision
download and a GitHub `master` mirror. Only a future live verdict can change
the score.

## Pre-upload evaluator summary

| Claim | Status | Expected points | Confidence | Expected evaluator status |
|---|---|---:|---|---|
| Proposition 3.1 | FALSIFIED | 2/2 | HIGH | Full credit retained |
| Proposition 3.4 | FALSIFIED | 2/2 | HIGH | Full credit retained |
| Lemma 2.1 | VERIFIED | 2/2 | HIGH | Full credit retained |
| Theorem 4.3 | VERIFIED | 2/2 | HIGH | Full credit retained |
| Theorem 5.1 | VERIFIED | 2/2 | HIGH | Candidate for full credit |

## Winning experiment

- Scientific branch:
  `orx/theorem-5-1-full-domain-direct-proof-certificate`
- Scientific Git SHA:
  `64130159f3df3a0053280ffde22bb70a7c791265`
- Scientific HF run: `fa29e4cb-51dc-4ede-93c6-40a6517816f4`
- Evaluator-visible branch:
  `orx/10-point-evaluator-visible-release-candidate`
- Evaluator-visible Git SHA:
  `2cf14723924197cb375b727d228631fa0e10ed16`
- Evaluator-visible HF run: `af8297d4-fd11-4529-a905-b37f19153959`
- Result: **20/20 cumulative tests and release audit passed**
- Selected compute: HF `cpu-upgrade`
- Estimated active need before each run: one CPU core, under five minutes
- Actual allocation: 8.0 CPUs from
  `cpu.max="800000 100000"`; no GPU
- Runtime: 37 seconds for each of the two new runs

## Exact fixed experiment command

```bash
uv sync --frozen && uv run python reproduction/reproduce.py --output-dir outputs/full && uv run python -m unittest -v reproduction/test_reproduction.py
```

## Commands executed for the v2 release audit

```bash
orx exp status 499d41c0-5827-4f5e-b409-d115ee98c9b3
orx exp status 074e5536-4a61-4e3b-b863-b421824b6425
orx exp status 83e0abf3-296d-4139-afbc-e14b75c9a5e4
orx runs 5f03f31c-b406-4db9-8f39-9c8709636f10
hf download DineshAI/MvuCgK0Qns --repo-type space --revision 29699a404594b1b4f4e0e0028e09f5b3e13cbffa --local-dir <fresh-live-directory> --quiet
uv run python reproduction/audit_release.py --candidate <fresh-staged-directory>
uvx --from marimo==0.23.15 marimo check notebooks/softmax_linear_attention.py
```

Publication used a parent-locked `HfApi.create_commit` with
`repo_id="DineshAI/MvuCgK0Qns"`, `repo_type="space"`, parent
`29699a404594b1b4f4e0e0028e09f5b3e13cbffa`, and exactly the 100 operations
listed in `upload-allowlist-v2.txt`. The exact published revision is
`e69cfc1d71736a13a805d985d6254c7da8e65a5b`.

Post-publication verification used:

```bash
hf download DineshAI/MvuCgK0Qns --repo-type space --revision e69cfc1d71736a13a805d985d6254c7da8e65a5b --local-dir <fresh-published-directory> --quiet
uv run python reproduction/audit_release.py --candidate <fresh-published-directory>
```

The 100 allowlisted hashes matched, all 95 prior live paths remained present,
and the resulting Space tree contained 110 files after excluding downloader
cache files. Credentials and generated wrappers were never printed.

## Evidence and release paths

- Scientific packet:
  `.openresearch/artifacts/claim_5_full/`
- Evaluator-visible packet:
  `space_candidate/evidence/claim_5_full/`
- Canonical current page:
  `space_candidate/pages/current-verification/page.md`
- Visual report:
  `reports/claim-by-claim/report.md`
- Tutorial notebook:
  `notebooks/softmax_linear_attention.py`
- Blind reviews:
  `reports/claim-by-claim/audits/blind-review-full-domain-round-1.md` and
  `blind-review-full-domain-round-2.md`
- Live/candidate subset proof:
  `reports/claim-by-claim/audits/old-new-subset-check-v2.md`
- Exact text upload list:
  `reports/claim-by-claim/audits/upload-allowlist-v2.txt`
- Candidate hashes:
  `reports/claim-by-claim/audits/upload-manifest-v2.sha256`
- Secret scan:
  `reports/claim-by-claim/audits/secret-scan-v2.md`
- Post-publication verification:
  `reports/claim-by-claim/audits/postpublication-v2.md`

The protected live file set has 95 paths; the staged post-commit tree has 110,
with zero missing live paths. The exact upload allowlist contains 100 text
paths and no binary files. Existing static assets remain untouched.
