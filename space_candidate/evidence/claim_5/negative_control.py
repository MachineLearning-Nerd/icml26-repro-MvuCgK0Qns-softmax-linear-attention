#!/usr/bin/env python3
"""Wrong anisotropic inverse must not be labeled Bayes optimal."""

from fractions import Fraction as F

sigma = [F(1), F(2)]
w = [F(1), F(1)]
x = [F(1), F(1)]
prediction = sum(w[i] * sigma[i] * x[i] for i in range(2))
label = sum(w[i] * x[i] for i in range(2))
error = (prediction - label) ** 2
if error == 0:
    print("UNEXPECTED: wrong anisotropic matrix attained zero error")
    raise SystemExit(0)
print(
    f"EXPECTED REJECTION: replacing Sigma^-1 by I gives prediction {prediction}, "
    f"label {label}, squared error {error}."
)
raise SystemExit(1)
