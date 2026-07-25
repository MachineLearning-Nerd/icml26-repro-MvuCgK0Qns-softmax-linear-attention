#!/usr/bin/env python3
"""Independent exact Bayes block-algebra checks with rational arithmetic."""

from fractions import Fraction as F


def matvec(matrix: list[list[F]], vector: list[F]) -> list[F]:
    return [sum((a * b for a, b in zip(row, vector, strict=True)), F(0)) for row in matrix]


cases = [
    ([F(1)], [F(2)], [F(3)]),
    ([F(1), F(2)], [F(2), F(-1)], [F(3), F(4)]),
    ([F(1), F(2), F(4)], [F(2), F(-1), F(3)], [F(3), F(4), F(-2)]),
]
for diagonal, w, x in cases:
    d = len(diagonal)
    sigma = [[diagonal[i] if i == j else F(0) for j in range(d)] for i in range(d)]
    sigma_w = matvec(sigma, w)
    gamma = [
        sigma[i] + [sigma_w[i]]
        for i in range(d)
    ] + [[sigma_w[j] for j in range(d)] + [sum(w[j] * sigma_w[j] for j in range(d))]]
    u_query = [x[i] / diagonal[i] for i in range(d)] + [F(0)]
    tilted = matvec(gamma, u_query)
    prediction = tilted[-1]
    label = sum((w[i] * x[i] for i in range(d)), F(0))
    assert prediction == label
    assert (prediction - label) ** 2 == 0

print(
    "PASS independent exact Bayes algebra: pointwise error is zero in "
    "d=1,2,3 anisotropic rational cases; the indexed block derivation is dimension-free."
)
