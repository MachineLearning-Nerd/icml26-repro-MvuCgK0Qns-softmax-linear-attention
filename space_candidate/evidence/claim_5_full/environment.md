# Environment and compute

- Environment manager: `uv`
- Python: `3.12.*`
- Lock: repository `uv.lock`, installed with `uv sync --frozen`
- Formal backend: Hugging Face
- Flavor: `cpu-upgrade` (8 advertised vCPUs, 32 GB RAM)
- Estimated active cores before run: 1
- Actual allocation is recorded from Linux `cpu.max`; the expected quota is
  `800000 100000`, or 8.0 CPUs.
- GPU used: no
- The exact certificate took the wall-clock duration recorded in
  `raw_result.json`.
