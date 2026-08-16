# Reproduction environment

The environment below is the recorded environment for the formal evidence
run. uv.lock is the dependency authority; this file is the human-readable
summary.

| Field | Recorded value |
| --- | --- |
| Backend | Hugging Face cpu-upgrade |
| CPU quota | 8.0 CPUs (cpu.max=800000 100000) |
| RAM flavor | 32 GB advertised |
| GPU | none |
| Python | 3.12.x; formal summary 3.12.13 |
| NumPy | 2.3.5 |
| SciPy | 1.17.1 |
| Platform | Linux x86_64 |
| Scientific run | fa29e4cb-51dc-4ede-93c6-40a6517816f4 |
| Scientific Git SHA | 64130159f3df3a0053280ffde22bb70a7c791265 |
| Recorded test result | 20/20 |

## Commands

~~~bash
uv sync --frozen
uv run python reproduction/reproduce.py --output-dir outputs/full
uv run python -m unittest -v reproduction/test_reproduction.py
uv run python verify_final.py
~~~

The first three commands are the historical reproduction command. The last
command is a lightweight cross-file and provenance check; it does not replace
the scientific test suite.

## Compute boundary

The exact certificates use deterministic symbolic, algebraic, or analytic
checks. The preserved finite-prompt suite uses seeds 0, 1, and 2. The
historical summary reports 23.259566236985847 seconds for the local full
summary and the formal Claim 5 certificate records 37 seconds on the HF run.
No GPU result is included.
