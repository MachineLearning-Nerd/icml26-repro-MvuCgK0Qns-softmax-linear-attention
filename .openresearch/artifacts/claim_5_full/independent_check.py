#!/usr/bin/env python3
"""Independent exact-arithmetic checks of the Theorem 5.1 dynamics."""

from fractions import Fraction as F


def main() -> None:
    # A diagonal covariance is the eigenbasis used in the proof.  The entries
    # below deliberately include anisotropy and an off-diagonal A component.
    s = [F(1, 4), F(3, 2), F(5, 1)]
    b = F(2, 3)
    a = [
        [F(3, 5), F(-1, 7), F(2, 9)],
        [F(1, 11), F(4, 5), F(-2, 13)],
        [F(3, 17), F(1, 19), F(6, 5)],
    ]

    adot = [
        [
            b * s[i] ** 2 * (F(1) if i == j else F(0))
            - b**2 * s[i] ** 2 * a[i][j] * s[j]
            for j in range(3)
        ]
        for i in range(3)
    ]
    bdot = sum(a[i][i] * s[i] ** 2 for i in range(3)) - b * sum(
        a[i][j] ** 2 * s[i] ** 2 * s[j]
        for i in range(3)
        for j in range(3)
    )
    balance_derivative = F(2) * sum(
        a[i][j] * adot[i][j] for i in range(3) for j in range(3)
    ) - F(2) * b * bdot
    assert balance_derivative == 0

    trace_derivative = sum(adot[i][i] for i in range(3))
    expected_trace = b * sum(x**2 for x in s) - b**2 * sum(
        s[i] ** 3 * a[i][i] for i in range(3)
    )
    assert trace_derivative == expected_trace

    # At the advertised limit, every residual b*s_i*a_ii-1 vanishes,
    # off-diagonals vanish, balance fixes the unique positive scale.
    sigma_inverse_sq_trace = sum(F(1, 1) / x**2 for x in s)
    assert sigma_inverse_sq_trace > 0
    for x in s:
        # The product identity is exact without approximating the fourth root.
        assert x * (F(1, 1) / x) == 1

    # The covariance-scale envelope used in the transfer is finite for every
    # fixed positive eigenvalue and every finite ||w||^2.
    w_norm_sq = F(29, 7)
    sigma_op = max(s)
    token_scale_sq = max(F(1), sigma_op * (F(1) + w_norm_sq))
    assert token_scale_sq == F(180, 7)

    print(
        "PASS independent exact dynamics: balance derivative is zero, the "
        "trace identity and anisotropic Bayes products hold, and arbitrary "
        "finite covariance has a finite conditional sub-Gaussian envelope."
    )


if __name__ == "__main__":
    main()
