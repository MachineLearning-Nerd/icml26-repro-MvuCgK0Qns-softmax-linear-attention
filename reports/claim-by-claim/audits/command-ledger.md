# Reproduction and release command ledger

This ledger records the state-changing, evidence-producing, and release-gate
commands used in the campaign. Read-only orientation used `rg`, `rg --files`,
`sed`, `find`, `du`, `df`, `env | cut`, `git status`, `git log`,
`git branch -a`, `git worktree list`, `sha256sum`, `file`, `cmp`, and
`orx ... status/runs/desc/logs` against the paths and IDs recorded below.
No secret values or generated job wrappers were printed.

## Startup and sources

```bash
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx projects --json
orx runs 5f03f31c-b406-4db9-8f39-9c8709636f10
git rev-parse HEAD
git status --short
curl -L --fail --user-agent OpenResearch-Reproduction/1.0 https://ar5iv.labs.arxiv.org/html/2512.11784
curl -L --fail --user-agent OpenResearch-Reproduction/1.0 https://www.jmlr.org/papers/volume25/23-1042/23-1042.pdf
hf download DineshAI/MvuCgK0Qns --type space --revision 2f4196b0ec25bad9979ac21e92543168c33090a9
```

The paper HTML hash was
`6ae468a4032e920d159b609a78f1860bdf90004c7a692df60c601d9e3c9ff4c2`;
the JMLR reference hash was
`3612edf523d550dfc549d1d47a0294f2bd2da7642bddfa56b8d4a0fa0bd93446`.
The verdict dataset was downloaded at commit
`0eb104445f62eff61382a1836be6189d8bfeb823` and filtered only by
`space_id=="DineshAI/MvuCgK0Qns"`.

## Fixed experiment command

Every formal node executed exactly:

```bash
uv sync --frozen && uv run python reproduction/reproduce.py --output-dir outputs/full && uv run python -m unittest -v reproduction/test_reproduction.py
```

Every successful launch used:

```bash
orx exp run <experiment-id> --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm --timeout 600
orx exp wait <experiment-id> --timeout 480
orx logs <run-id>
```

The experiment/run pairs were:

| Experiment | Run | Result | Seconds |
|---|---|---|---:|
| `03c7bab1-7228-4c6d-a1f1-037ec8d5b3d7` | `053114e0-74aa-45b2-b94e-64775cb0877c` | baseline pass | 49 |
| `69cd0900-3b34-4405-8a93-8f1c995038ad` | `9d57f61c-1b73-487e-8a5a-52d605bde7f3` | Claim 1 cumulative pass | 48 |
| `6ea7fa9c-b2e2-4965-a1b4-b31c55f3465e` | `80d467e5-b372-487e-8a5a-52d605bde7f3` | Claim 2 cumulative pass | 48 |
| `e222a3cc-bfaf-4977-8ffe-d4ee05d7f1a5` | `19c05090-10a5-430d-843b-f5b75d4ea19a` | Claim 3 cumulative pass | 48 |
| `12eeda25-2547-4fcf-abf4-ef5cb6181d6f` | `60d2806f-6048-46d3-b17c-1917e70287af` | Claim 4 cumulative pass | 47 |
| `72d3d918-14bc-4843-b74c-168670a48d00` | `386f81f8-b501-47eb-9906-dc4de0278066` | Claim 5 cumulative pass | 47 |
| `57f17b39-1f6d-4853-8665-7ef150cccb91` | `9630e46c-34be-4c7a-8939-836e3c50f07f` | release gate, 19/19 pass | 53 |

Two non-scientific setup attempts failed before evidence was accepted:
`6cbdb941-d41b-448b-bdef-561c4db7130e` (`uv` missing from the first image)
and `5998679d-20e0-40d3-9372-25019c70cf2f` (initial Claim 1 packaging error).

## Local bounded checks and report generation

```bash
uv run python space_candidate/evidence/claim_5/verify_claim_5.py --raw space_candidate/evidence/claim_5/raw_result.json
uv run python space_candidate/evidence/claim_5/independent_check.py
uv run python space_candidate/evidence/claim_5/negative_control.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run python reproduction/make_report_figures.py --data-dir outputs/full --output-dir reports/claim-by-claim/images
uv run marimo check --fix notebooks/softmax_linear_attention.py
uv run marimo check --strict notebooks/softmax_linear_attention.py
uv run python reproduction/audit_release.py --candidate space_candidate
uv run python -m unittest -v reproduction/test_reproduction.py
uv run python reproduction/blind_review.py --candidate <fresh-candidate> --round <round> --output <audit.md>
uv run python reproduction/prepare_release_manifest.py --candidate <fresh-candidate> --protected-manifest <protected-file-manifest.sha256> --output-dir <audits>
```

The first blind review intentionally exited nonzero with 41 missing
discoverability conclusions. The fixed second, prepublication third, and
postpublication fourth reviews exited zero. A diagnostic
`uv run marimo format ...` was rejected because that subcommand does not exist;
`marimo check --fix` was used instead. A bare `python -m json.tool` diagnostic
was unavailable outside the managed environment; all Python validation used
`uv run python`. Initial candidate copying inherited read-only protected-file
permissions; only the candidate copy was made writable before overlaying it.

## Git and release

Each experiment branch used the standard sequence:

```bash
git fetch origin
git checkout <orx-branch>
git add <scoped-paths>
git commit -m <scoped-message>
git push -u origin <orx-branch>
```

The exact release branch was committed and pushed at
`bbe74167d7aa8426b01d4fd55fd608397ac657de`. Publication used the audited
external script with SHA-256
`65cb3a7a301f0626820e23c919a50ecfc558912424dcb68441c119b97cc28476`:

```bash
uv run python <audits>/publish_space.py --candidate <fresh-candidate> --allowlist <upload-allowlist.txt> --manifest <upload-manifest.sha256>
```

The script called `HfApi.create_commit` with `repo_type="space"`,
`revision="main"`, and
`parent_commit="2f4196b0ec25bad9979ac21e92543168c33090a9"`. It added or replaced
only the 78 allowlisted text paths and performed no deletion.

Postpublication commands:

```bash
hf download DineshAI/MvuCgK0Qns --type space --revision 29699a404594b1b4f4e0e0028e09f5b3e13cbffa --local-dir <fresh-published-directory> --quiet
sha256sum -c <upload-manifest.sha256>
sha256sum -c <candidate-manifest.sha256>
uv run python reproduction/audit_release.py --candidate <fresh-published-directory>
uv run python reproduction/blind_review.py --candidate <fresh-published-directory> --round 4-postpublish --output <audit.md>
git merge --ff-only bbe74167d7aa8426b01d4fd55fd608397ac657de
```

The final GitHub publication commit and push are recorded in the report status
once completed.
