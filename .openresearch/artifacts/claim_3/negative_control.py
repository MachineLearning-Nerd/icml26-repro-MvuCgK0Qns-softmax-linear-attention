#!/usr/bin/env python3
"""Non-Gaussian measure for which the Gaussian affine formula must be rejected."""

import math

true_attention = math.tanh(2.0)
gaussian_prediction = 2.0
if math.isclose(true_attention, gaussian_prediction, rel_tol=0.0, abs_tol=1e-12):
    print("UNEXPECTED: Rademacher control matched the Gaussian formula")
    raise SystemExit(0)
print(
    "EXPECTED REJECTION: Rademacher attention tanh(2)="
    f"{true_attention:.16f}, not the Gaussian affine prediction 2."
)
raise SystemExit(1)
