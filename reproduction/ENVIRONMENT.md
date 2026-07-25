# Execution environment

- Python 3.12 with exact packages locked by `pyproject.toml` and `uv.lock`.
- One repository-level `.venv`, created by `uv sync --frozen`.
- Formal OpenResearch runs use Hugging Face `cpu-upgrade` (8 vCPU, 32 GB);
  the workload is estimated to keep one core active and uses no GPU.
- Official repository pinned at `8fa49b308eaac168bc4edcdc06f26703ac4520f8` for provenance only.
- Independent reproduction imports no official module.
