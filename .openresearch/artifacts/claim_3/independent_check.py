#!/usr/bin/env python3
"""Independent sparse-polynomial reconstruction with exact rational coefficients."""

from __future__ import annotations

from fractions import Fraction

Monomial = tuple[str, ...]
Polynomial = dict[Monomial, Fraction]


def add(*polynomials: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def scale(polynomial: Polynomial, factor: Fraction) -> Polynomial:
    return {
        monomial: coefficient * factor
        for monomial, coefficient in polynomial.items()
        if coefficient * factor
    }


def product(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            result[monomial] = (
                result.get(monomial, Fraction(0))
                + left_coefficient * right_coefficient
            )
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def variable(name: str) -> Polynomial:
    return {(name,): Fraction(1)}


def dot(left: list[Polynomial], right: list[Polynomial]) -> Polynomial:
    return add(*(product(x, y) for x, y in zip(left, right, strict=True)))


def mat_t_vec(matrix: list[list[Polynomial]], vector: list[Polynomial]) -> list[Polynomial]:
    return [
        add(*(product(matrix[i][j], vector[i]) for i in range(len(matrix))))
        for j in range(len(matrix[0]))
    ]


checks = 0
for d in (1, 2, 3, 4, 8, 16):
    # Rectangular B with r<d for d>1 explicitly covers singular Gamma.
    rank = 1 if d == 1 else max(1, d - 1)
    a = [variable(f"a{i}") for i in range(d)]
    m = [variable(f"m{i}") for i in range(d)]
    g = [variable(f"g{j}") for j in range(rank)]
    b = [[variable(f"B{i}_{j}") for j in range(rank)] for i in range(d)]
    b_t_a = mat_t_vec(b, a)
    b_g = [
        add(*(product(b[i][j], g[j]) for j in range(rank)))
        for i in range(d)
    ]

    lhs = add(dot(a, m), dot(a, b_g), scale(dot(g, g), Fraction(-1, 2)))
    shifted = [add(g[j], scale(b_t_a[j], Fraction(-1))) for j in range(rank)]
    rhs = add(
        dot(a, m),
        scale(dot(b_t_a, b_t_a), Fraction(1, 2)),
        scale(dot(shifted, shifted), Fraction(-1, 2)),
    )
    assert lhs == rhs
    checks += len(set(lhs) | set(rhs))

print(
    "PASS independent exact-polynomial reconstruction: "
    f"completion of square matched in d=1,2,3,4,8,16 across {checks} coefficients, "
    "including singular covariances."
)
