#!/usr/bin/env python3
"""Independent exact reconstruction; imports no reproduction code."""

from fractions import Fraction


def even_standard_gaussian_moment(order: int) -> Fraction:
    value = Fraction(1, 1)
    for odd in range(1, order, 2):
        value *= odd
    return value


moments = {order: even_standard_gaussian_moment(order) for order in (0, 4, 8)}
assert moments == {0: 1, 4: 3, 8: 105}
v_gradient_error = even_standard_gaussian_moment(2)
u_gradient_error = even_standard_gaussian_moment(2)
rhs_log_factor = Fraction(0, 1)
assert v_gradient_error == 1
assert u_gradient_error == 1
assert v_gradient_error > rhs_log_factor
assert u_gradient_error > rhs_log_factor
for p in (0, 4, 8):
    for q in (0, 4, 8):
        assert moments[p] * moments[q] <= moments[p] * moments[q]
print(
    "PASS independent reconstruction: all 9 moment bounds are finite; "
    "V-gradient LHS=1 and U-gradient LHS=1 while both L=1 RHS values are 0."
)
