# Post-publication verification v2

Date: 2026-07-26

- Existing Space: `DineshAI/MvuCgK0Qns`
- Parent revision:
  `29699a404594b1b4f4e0e0028e09f5b3e13cbffa`
- Published revision:
  `e69cfc1d71736a13a805d985d6254c7da8e65a5b`
- Publication method: one parent-locked Hugging Face API commit containing
  only the 100 UTF-8 paths in `upload-allowlist-v2.txt`
- Binary uploads: none
- Deleted paths: none

## Exact-revision verification

A fresh empty-directory download of the published revision produced 110 Space
files after excluding the downloader cache. All 100 allowlisted hashes matched
`upload-manifest-v2.sha256`. All 95 paths from the previously judged live
revision remained present, with zero missing paths.

The fail-closed audit returned:

```text
PASS release audit: canonical traversal reaches all five complete packets; verifiers/checkers/controls return expected codes and outputs; navigation, provenance, logbook JSON, and secret scan pass.
```

The canonical traversal begins at `README.md`. The current verification page
and `claim_5_full` packet are obvious before the historical rejected Claim 5
packet. Every displayed verdict and number is linked to raw JSON, and every
current verifier/checker/control reproduced its recorded output and exit code.

**Post-publication result: PASS.**
