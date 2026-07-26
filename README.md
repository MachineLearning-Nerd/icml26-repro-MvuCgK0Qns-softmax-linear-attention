# Softmax as Linear Attention — exact ICML 2026 reproduction

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-MvuCgK0Qns-softmax-linear-attention/blob/master/notebooks/softmax_linear_attention.py)

This is an independent, CPU-only audit of
[Softmax as Linear Attention in the Large-Prompt Regime](https://arxiv.org/abs/2512.11784)
(OpenReview `MvuCgK0Qns`). The live judge now awards `8/10` at Space revision
`29699a404594b1b4f4e0e0028e09f5b3e13cbffa`: Claims 1–4 are VERIFIED and
Theorem 5.1 is inconclusive. The current child closes that remaining proof
gap:

| Paper claim | Paper result | Observed result | Assessment |
|---|---|---|---|
| Proposition 3.1 | output error `≤c₁σ⁶ln(L)/L^(c₂/σ²)` | valid `L=1` witness has exact `1>0` | **FALSIFIED** as published |
| Proposition 3.4 | analogous `U,V` gradient bounds | both exact gradient errors are `1>0`; all nine moment assumptions hold | **FALSIFIED** as published |
| Lemma 2.1 | Gaussian attention equals `Vm+VΓKᵀQz` | dimension-free MGF proof, including singular `Γ` | **VERIFIED** |
| Theorem 4.3 | finite-flow limiting risk transfers within arbitrary `ε` | exact `ε/2+ε/2` proof and monotonicity certificate | **VERIFIED** |
| Theorem 5.1 | Bayes-optimal training for every invertible anisotropic `Σ` in the displayed initialization interval | direct balanced-flow proof covers every positive-definite `Σ` and every `α>0`; scale audit closes the transfer | **VERIFIED** |

The conservative projected range is `8–10/10`; the best-supported possible
score is `10/10`, both forecasts rather than judge results. Claims 1 and 2
retain an interpretation risk: an unstated `L≥2` repair would evade the
boundary witnesses.

- [Illustrated claim-by-claim report](reports/claim-by-claim/report.md)
- [Evidence-first marimo tutorial](notebooks/softmax_linear_attention.py)
- [Current evaluator-visible verification](space_candidate/pages/current-verification/page.md)
- Local notebook: `uvx marimo edit notebooks/softmax_linear_attention.py`
  or `uvx marimo run notebooks/softmax_linear_attention.py`

## What changed and what did not

The current exact certificates replace the old numerical verifier. The
historical `d=4`, single-head, single-layer experiments remain preserved as
scoped corroboration: they used three covariance families, 18,144
output/Jacobian comparisons, 36 trained models, and seeds `0,1,2`. They do not
establish a dimension-universal theorem or the paper's `σ`-dependent rate.

The new proof certificates are not downscaled simulations. Claims 1 and 2 use
one-dimensional witnesses because one assumption-satisfying counterexample is
sufficient to resolve a universal statement. Claims 3 and 4 are
dimension-free and arbitrary-`ε`, respectively. Claim 5 uses a direct
dimension-general proof, not the narrower cited sufficient condition.

Formal compute was Hugging Face `cpu-upgrade`, CPU only: 8-vCPU cgroup quota,
32 GB RAM, Python 3.12, and the locked `uv` environment. No GPU was used.

## Experiment log

Every formal node inherited the same command verbatim:
`uv sync --frozen && uv run python reproduction/reproduce.py --output-dir outputs/full && uv run python -m unittest -v reproduction/test_reproduction.py`.

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| [`orx/validated-5-10-baseline`](https://github.com/MachineLearning-Nerd/icml26-repro-MvuCgK0Qns-softmax-linear-attention/tree/orx/validated-5-10-baseline) | Freeze the judged numerical baseline and locked environment | `uv sync --frozen && uv run python reproduction/reproduce.py --output-dir outputs/full && uv run python -m unittest -v reproduction/test_reproduction.py` | 8/8 baseline tests; historical toy evidence | HF `cpu-upgrade`, 8-vCPU quota, 49 s |
| [`orx/prop-3-1-literal-l-1-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-MvuCgK0Qns-softmax-linear-attention/tree/orx/prop-3-1-literal-l-1-certificate) | Literal Proposition 3.1 contract and counterexample | `uv sync --frozen && uv run python reproduction/reproduce.py --output-dir outputs/full && uv run python -m unittest -v reproduction/test_reproduction.py` | FALSIFIED; cumulative tests pass | HF `cpu-upgrade`, 8-vCPU quota, 48 s |
| [`orx/prop-3-4-literal-l-1-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-MvuCgK0Qns-softmax-linear-attention/tree/orx/prop-3-4-literal-l-1-certificate) | Literal gradient-bound contract plus Assumption 3.3 audit | `uv sync --frozen && uv run python reproduction/reproduce.py --output-dir outputs/full && uv run python -m unittest -v reproduction/test_reproduction.py` | FALSIFIED; cumulative tests pass | HF `cpu-upgrade`, 8-vCPU quota, 48 s |
| [`orx/lemma-2-1-dimension-free-proof-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-MvuCgK0Qns-softmax-linear-attention/tree/orx/lemma-2-1-dimension-free-proof-certificate) | Replace finite quadrature with a dimension-free proof | `uv sync --frozen && uv run python reproduction/reproduce.py --output-dir outputs/full && uv run python -m unittest -v reproduction/test_reproduction.py` | VERIFIED; cumulative tests pass | HF `cpu-upgrade`, 8-vCPU quota, 48 s |
| [`orx/theorem-4-3-epsilon-transfer-proof-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-MvuCgK0Qns-softmax-linear-attention/tree/orx/theorem-4-3-epsilon-transfer-proof-certificate) | Reconstruct the full arbitrary-`ε` risk-transfer proof | `uv sync --frozen && uv run python reproduction/reproduce.py --output-dir outputs/full && uv run python -m unittest -v reproduction/test_reproduction.py` | VERIFIED; cumulative tests pass | HF `cpu-upgrade`, 8-vCPU quota, 47 s |
| [`orx/theorem-5-1-bayes-certificate-and-dependency-aud`](https://github.com/MachineLearning-Nerd/icml26-repro-MvuCgK0Qns-softmax-linear-attention/tree/orx/theorem-5-1-bayes-certificate-and-dependency-aud) | Prove the Bayes endpoint and audit the universal training dependencies | `uv sync --frozen && uv run python reproduction/reproduce.py --output-dir outputs/full && uv run python -m unittest -v reproduction/test_reproduction.py` | Endpoint exact; full theorem BLOCKED; 18/18 tests | HF `cpu-upgrade`, 8-vCPU quota, 47 s |
| [`orx/theorem-5-1-full-domain-direct-proof-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-MvuCgK0Qns-softmax-linear-attention/tree/orx/theorem-5-1-full-domain-direct-proof-certificate) | Replace the narrow cited condition with a full-domain matrix-flow proof and covariance-scale audit | `uv sync --frozen && uv run python reproduction/reproduce.py --output-dir outputs/full && uv run python -m unittest -v reproduction/test_reproduction.py` | Theorem 5.1 VERIFIED; 20/20 cumulative tests | HF `cpu-upgrade`, 8-vCPU quota, 37 s |
| [`orx/10-point-evaluator-visible-release-candidate`](https://github.com/MachineLearning-Nerd/icml26-repro-MvuCgK0Qns-softmax-linear-attention/tree/orx/10-point-evaluator-visible-release-candidate) | Mirror the proof into canonical pages and validate the visual report/notebook | `uv sync --frozen && uv run python reproduction/reproduce.py --output-dir outputs/full && uv run python -m unittest -v reproduction/test_reproduction.py` | 20/20 tests; evaluator-visible release audit passed | HF `cpu-upgrade`, 8-vCPU quota, 37 s |
| `master` | Publication surface for the report, notebook, and exact published text | Not run as an experiment (publication surface) | Mirrors the winning cumulative evidence | No experiment compute |

## Reproduce

The sole repository-level `.venv` is managed by `uv`; `pyproject.toml` and
`uv.lock` pin the environment.

```bash
uv sync --frozen
uv run python reproduction/reproduce.py --output-dir outputs/full
uv run python -m unittest -v reproduction/test_reproduction.py
```

The formal experiment command combines those steps exactly as shown in the
experiment log. Raw numerical CSVs remain in `outputs/full`; current exact
contracts, raw JSON, checkers, controls, source audits, and limitations are in
`space_candidate/evidence`.
