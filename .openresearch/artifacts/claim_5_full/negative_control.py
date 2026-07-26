#!/usr/bin/env python3
"""Reject use of the balanced proof on an unbalanced initialization."""

from fractions import Fraction as F


def main() -> None:
    b0 = F(1)
    a0_frobenius_sq = F(1, 4)
    if a0_frobenius_sq != b0**2:
        print(
            "EXPECTED REJECTION: ||A(0)||_F^2-b(0)^2 is not zero, so the "
            "balanced stationary dichotomy cannot certify this control."
        )
        raise SystemExit(1)
    print("UNEXPECTED: unbalanced initialization accepted")


if __name__ == "__main__":
    main()
