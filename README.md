# Softmax as Linear Attention in the Large-Prompt Regime

Independent ICML 2026 reproduction and evidence audit for:

> **Softmax as Linear Attention in the Large-Prompt Regime: a Measure-based Perspective**

Paper authors: **Etienne Boursier** and **Claire Boyer**
Paper: [arXiv:2512.11784v2](https://arxiv.org/abs/2512.11784) · OpenReview
`MvuCgK0Qns`
Final repository: [MachineLearning-Nerd/icml26-softmax-linear-attention](https://github.com/MachineLearning-Nerd/icml26-softmax-linear-attention)
Previous repository name: `icml26-repro-MvuCgK0Qns-softmax-linear-attention`

**Collection status:** `VERIFIED_SCOPED_WITH_FALSIFIED_LITERAL_CLAIMS_AND_LIVE_SCORE_PENDING`

This repository is an independent audit. It does not claim to be the authors'
official implementation, and it does not claim a new evaluator score. It
preserves the historical judged result, makes every current claim contract
explicit, and links each conclusion to a producer, an independent checker, a
negative control, and raw evidence.

## Results at a glance

| Paper claim | Current verdict | How the verdict is produced |
| --- | --- | --- |
| Proposition 3.1 | `FALSIFIED_AS_WRITTEN` | A valid `d=1, L=1` Gaussian witness gives exact error `1`, while the literal `ln(L)` bound is `0`; an independent checker reproduces the contradiction. |
| Proposition 3.4 | `FALSIFIED_AS_WRITTEN` | A valid `d=1, L=1, U=0, V=1` witness gives both exact gradient errors `1` while both literal bounds are `0`; all nine moment conditions are checked. |
| Lemma 2.1 | `VERIFIED_SCOPED` | A dimension-free Gaussian exponential-tilt derivation is checked for singular and nonsingular covariance, then reconstructed independently over 380 exact polynomial coefficients. |
| Theorem 4.3 | `VERIFIED_SCOPED` | An independent checker reconstructs the arbitrary-`epsilon` `epsilon/2 + epsilon/2` order chain, finite-horizon comparison, and gradient-flow risk monotonicity. |
| Theorem 5.1 in the judged version / Theorem 5.2 in arXiv v2 | `VERIFIED_SCOPED_FULL_DOMAIN` | A direct balanced matrix-gradient-flow proof covers every positive-definite covariance and the full stated initialization domain; a covariance-scale transfer closes the finite-prompt step. |

Claims 1 and 2 are successful falsifications of the statements as literally
published, not failed software tests. If the intended theorem silently
requires `L >= 2` or sufficiently large `L`, that is an interpretation or
revision issue and is recorded as a limitation. Claims 3--5 are scoped to the
source versions and assumptions recorded in `SOURCE_MANIFEST.md`.

## Historical evaluator result

The historical live evaluator awarded **8/10** at judged Space revision
`29699a404594b1b4f4e0e0028e09f5b3e13cbffa`. The published candidate revision
`e69cfc1d71736a13a805d985d6254c7da8e65a5b` contains the full-domain Claim 5
certificate and passed the post-publication preservation checks. No new live
judge result is claimed here; `8--10/10` and `10/10` are forecasts only.

## Evidence workflow

Every current claim follows the same chain:

1. The paper source and theorem anchor are pinned by hash.
2. A `claim_contract.json` states the literal quantifiers, assumptions, and
   acceptance condition.
3. A producer writes a raw result with the source hash, Git SHA, environment,
   and limitations.
4. A separately implemented checker reconstructs the key calculation without
   importing the reproduction implementation.
5. A negative control is expected to fail for a specified reason.
6. The verdict is published only when the packet and its fail-closed verifier
   agree.

The packets are under
`space_candidate/evidence/claim_1`, `claim_2`, `claim_3`, `claim_4`, and
`claim_5_full`. The old `claim_5` packet is retained as a historical blocked
dependency audit; it is not the current Claim 5 verdict.

| Claim | Producer and raw evidence | Independent check | Negative control |
| --- | --- | --- | --- |
| Proposition 3.1 | `claim_1/reproduce.py` output and `raw_result.json` | `claim_1/independent_check.py` | `delta_0` control rejects zero-error data |
| Proposition 3.4 | `claim_2/reproduce.py` output and `raw_result.json` | `claim_2/independent_check.py` | `delta_0` control rejects zero-gradient data |
| Lemma 2.1 | `claim_3/raw_result.json` and exact polynomial reconstruction | `claim_3/independent_check.py` | Rademacher attention rejects the Gaussian affine formula |
| Theorem 4.3 | `claim_4/raw_result.json` and order-chain certificate | `claim_4/independent_check.py` | Non-monotone risk control rejects finite-time closeness alone |
| Theorem 5.1 / 5.2 | `claim_5_full/raw_result.json` and direct proof certificate | `claim_5_full/independent_check.py` | Unbalanced initialization control rejects the stationary dichotomy |

The canonical summary of this mapping is
[CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md), and the machine-readable release
manifest is [EVIDENCE_MANIFEST.json](EVIDENCE_MANIFEST.json).

## Branch guide

The public branch names describe the evidence rather than the automation
system that produced them. The exact legacy-to-final mapping and pre-cleanup
tips are preserved in [BRANCH_AUDIT.md](BRANCH_AUDIT.md).

| Final branch | Purpose |
| --- | --- |
| [main](https://github.com/MachineLearning-Nerd/icml26-softmax-linear-attention/tree/main) | Paper-first publication surface, current README, manifests, report, and cumulative evidence |
| [baseline/judged-8-of-10](https://github.com/MachineLearning-Nerd/icml26-softmax-linear-attention/tree/baseline/judged-8-of-10) | Historical judged baseline and locked numerical environment |
| [audit/claim-1-prop-3-1](https://github.com/MachineLearning-Nerd/icml26-softmax-linear-attention/tree/audit/claim-1-prop-3-1) | Literal Proposition 3.1 boundary witness |
| [audit/claim-2-prop-3-4](https://github.com/MachineLearning-Nerd/icml26-softmax-linear-attention/tree/audit/claim-2-prop-3-4) | Literal Proposition 3.4 and Assumption 3.3 audit |
| [proof/claim-3-lemma-2-1](https://github.com/MachineLearning-Nerd/icml26-softmax-linear-attention/tree/proof/claim-3-lemma-2-1) | Dimension-free Gaussian identity proof |
| [proof/claim-4-theorem-4-3](https://github.com/MachineLearning-Nerd/icml26-softmax-linear-attention/tree/proof/claim-4-theorem-4-3) | Arbitrary-`epsilon` risk-transfer proof |
| [audit/claim-5-dependency-gap](https://github.com/MachineLearning-Nerd/icml26-softmax-linear-attention/tree/audit/claim-5-dependency-gap) | Historical Bayes endpoint and blocked dependency audit |
| [proof/claim-5-full-domain](https://github.com/MachineLearning-Nerd/icml26-softmax-linear-attention/tree/proof/claim-5-full-domain) | Full-domain balanced gradient-flow proof |
| [release/evaluator-visible](https://github.com/MachineLearning-Nerd/icml26-softmax-linear-attention/tree/release/evaluator-visible) | Evaluator-visible report and verification release |
| [release/10-point-candidate](https://github.com/MachineLearning-Nerd/icml26-softmax-linear-attention/tree/release/10-point-candidate) | Candidate release containing the full Claim 5 evidence |
| [release/final-publication](https://github.com/MachineLearning-Nerd/icml26-softmax-linear-attention/tree/release/final-publication) | Final publication manifest and preservation audits |

No branch name is evidence by itself. The branch is a reproducibility route;
the claim packet, raw result, checker, control, and source audit are the
evidence.

## Reproduce the recorded experiment

The locked environment and formal command are:

~~~bash
uv sync --frozen
uv run python reproduction/reproduce.py --output-dir outputs/full
uv run python -m unittest -v reproduction/test_reproduction.py
~~~

The exact cumulative command historically used for each experiment was:

~~~bash
uv sync --frozen && uv run python reproduction/reproduce.py --output-dir outputs/full && uv run python -m unittest -v reproduction/test_reproduction.py
~~~

The lightweight cross-file release check is:

~~~bash
uv run python verify_final.py
~~~

The formal Claim 5 run passed **20/20** tests at scientific Git SHA
`64130159f3df3a0053280ffde22bb70a7c791265` in HF run
`fa29e4cb-51dc-4ede-93c6-40a6517816f4`. The environment was CPU-only:
Python 3.12, NumPy 2.3.5, SciPy 1.17.1, and an 8-CPU HF
`cpu-upgrade` allocation. No GPU was used.

## Citation

~~~bibtex
@misc{boursier2026softmax,
  title         = {Softmax as Linear Attention in the Large-Prompt Regime: a Measure-based Perspective},
  author        = {Boursier, Etienne and Boyer, Claire},
  year          = {2026},
  eprint        = {2512.11784},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG},
  url           = {https://arxiv.org/abs/2512.11784}
}
~~~

Please also cite this audit with the metadata in
[CITATION.cff](CITATION.cff) when reusing its evidence or scripts.

## Thank you

Thank you to **Etienne Boursier** and **Claire Boyer** for making the paper,
its mathematical statements, and the surrounding research direction available
for careful independent study. This repository is intended as a respectful,
traceable reproduction and audit: disagreements are recorded against explicit
source versions and assumptions, and positive results are limited to the
evidence that was actually checked.

## Scope and limitations

- The two `L=1` results are literal-contract falsifications; they do not prove
  that a repaired, sufficiently-large-prompt statement is false.
- Theorem 4.3 is qualitative and does not produce a numerical
  `L(epsilon)`.
- Theorem 5.1 / 5.2 is a proof certificate for the stated population
  gradient-flow model and initialization domain; it does not claim a finite
  experimental rate beyond the recorded transfer argument.
- Historical finite-prompt CSVs are retained as corroboration and are not
  presented as universal theorem proofs.
- The pinned official repository is provenance only. The current audit imports
  no official implementation module; the clean-room boundary is documented in
  [SOURCE_AUDIT.md](SOURCE_AUDIT.md).
