# Softmax as linear attention — ICML 2026 reproduction

Independent CPU reproduction for OpenReview `MvuCgK0Qns` / arXiv `2512.11784`.
It checks the Gaussian infinite-prompt identity, finite output and exact
Jacobian concentration, gradient stability along an optimization path, and
transfer to the exact linear-limit solution across three covariance families.

```bash
uv venv --python 3.12
uv pip install --python .venv/bin/python -r reproduction/requirements-cpu.txt
.venv/bin/python reproduction/reproduce.py --output-dir outputs/full
.venv/bin/python -m unittest -v reproduction/test_reproduction.py
```

The experiment is CPU-only and imports no official module. All raw comparisons,
trained-model rows, source pins, limitations, and tests are retained.
