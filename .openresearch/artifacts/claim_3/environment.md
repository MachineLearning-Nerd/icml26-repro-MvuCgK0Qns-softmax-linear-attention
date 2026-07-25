# Environment and compute

- Python: exactly 3.12.x through `uv.lock`
- Environment: the sole repository `.venv`, created by `uv sync --frozen`
- Backend/flavor: Hugging Face `cpu-upgrade`
- Published allocation: 8 vCPU, 32 GB RAM, 50 GB ephemeral storage
- Estimated active cores: 1
- GPU: none
- Container: `ghcr.io/astral-sh/uv:python3.12-bookworm`

The run records cgroup CPU quota, visible logical CPUs, Git SHA, and wall time.
