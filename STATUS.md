# Status — Softmax as Linear Attention

**Updated:** 2026-08-16
**Paper:** [Softmax as Linear Attention in the Large-Prompt Regime: a Measure-based Perspective](https://arxiv.org/abs/2512.11784v2)
**OpenReview:** `MvuCgK0Qns`
**Collection status:** `VERIFIED_SCOPED_WITH_FALSIFIED_LITERAL_CLAIMS_AND_LIVE_SCORE_PENDING`

## Current conclusion

The repository contains a complete, scoped evidence packet for all five
audited paper claims. Propositions 3.1 and 3.4 are falsified as literally
written by exact `L=1` witnesses. Lemma 2.1 and Theorem 4.3 have
dimension-free or arbitrary-`epsilon` proof certificates. Theorem 5.1 in the
judged version, corresponding to Theorem 5.2 in arXiv v2, has a direct
full-domain balanced-gradient-flow proof and a finite-covariance transfer
audit.

The older Claim 5 packet remains available because it records a real
dependency gap found during the audit. The newer full-domain packet closes
that gap; it does not erase the historical route.

## Evaluator state

- Historical live score: **8/10**
- Judged Space revision: `29699a404594b1b4f4e0e0028e09f5b3e13cbffa`
- Published candidate revision: `e69cfc1d71736a13a805d985d6254c7da8e65a5b`
- New live score: **not claimed**
- Forecast: `8--10/10`, with `10/10` only a forecast

## Reproduction state

- Formal Claim 5 run: HF `cpu-upgrade`, 8-CPU quota
- Scientific run ID: `fa29e4cb-51dc-4ede-93c6-40a6517816f4`
- Scientific run Git SHA: `64130159f3df3a0053280ffde22bb70a7c791265`
- Recorded regression result: **20/20**
- Runtime: Python 3.12, NumPy 2.3.5, SciPy 1.17.1
- GPU used: **no**

## Main entry points

- [README](README.md) — paper, verdicts, branch guide, citation, and thank-you note
- [claims.json](claims.json) — machine-readable five-claim ledger
- [CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md) — source-to-verdict production paths
- [SOURCE_AUDIT.md](SOURCE_AUDIT.md) and [SOURCE_MANIFEST.md](SOURCE_MANIFEST.md) — source/version boundary
- [BRANCH_AUDIT.md](BRANCH_AUDIT.md) — final branch names and legacy mapping
- [EVIDENCE_MANIFEST.json](EVIDENCE_MANIFEST.json) — release manifest
- [verify_final.py](verify_final.py) — lightweight fail-closed repository check

## Open limitations

1. The `L=1` counterexamples do not decide a repaired theorem with an
   explicit sufficiently-large-prompt domain.
2. Theorem 4.3 and the full-domain Claim 5 result are qualitative; no
   numerical `L(epsilon)` is claimed.
3. Historical finite-prompt experiments support intuition and consistency but
   do not replace the theorem proofs.
4. The source version, repository commit, Space revisions, and local
   environment are part of every verdict and should be rechecked before
   extending any claim.
