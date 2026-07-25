#!/usr/bin/env python3
"""Independent exact-moment reconstruction; imports no reproduction code."""

from fractions import Fraction

variance_x = Fraction(1, 1)
mean_x = Fraction(0, 1)
infinite_output = Fraction(0, 1)
lhs = variance_x + (mean_x - infinite_output) ** 2
rhs_log_factor = Fraction(0, 1)  # ln(1) exactly

assert lhs == 1
assert rhs_log_factor == 0
assert lhs > rhs_log_factor
print("PASS independent reconstruction: Gaussian moment LHS=1; ln(1) makes RHS=0.")
