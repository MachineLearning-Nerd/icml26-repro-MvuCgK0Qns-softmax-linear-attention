# Environment and compute

- Python: exactly 3.12.x through `uv.lock`
- Environment: the sole repository `.venv`, created by `uv sync --frozen`
- Backend/flavor: Hugging Face `cpu-upgrade`
- Published allocation: 8 vCPU, 32 GB RAM, 50 GB ephemeral storage
- Estimated active cores: 1
- Actual schedulable allocation: 8.0 CPUs
- Cgroup quota: `cpu.max="800000 100000"`
- Host affinity: 64 logical CPUs (not the allocation)
- GPU: none
- Container: `ghcr.io/astral-sh/uv:python3.12-bookworm`

Final cumulative rerun: HF run `386f81f8-b501-47eb-9906-dc4de0278066`,
Git SHA `ab03d8e28985c00899253218175049cb32eb0077`, 47 seconds overall;
this exact certificate took 0.209 seconds. Estimated cost contribution under
one-minute billing: `$0.0005`.
