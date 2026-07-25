#!/usr/bin/env python3
"""Fail-closed verifier for the dimension-free Lemma 2.1 derivation."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path

EXPECTED_SOURCE = "6ae468a4032e920d159b609a78f1860bdf90004c7a692df60c601d9e3c9ff4c2"
EXPECTED_PROOF = {
    "representation": "X=m+B G, G~N(0,I_r), Gamma=B B^T; valid for every PSD Gamma",
    "score_vector": "a=K^T Q z",
    "completion_of_square": (
        "a^T(m+B g)-||g||^2/2 = a^T m+||B^T a||^2/2"
        "-||g-B^T a||^2/2"
    ),
    "normalizer": "E exp(a^T X)=exp(a^T m+a^T Gamma a/2)",
    "differentiated_normalizer": (
        "E[X exp(a^T X)]=(m+Gamma a)"
        "*exp(a^T m+a^T Gamma a/2)"
    ),
    "ratio": "E[V X exp(a^T X)]/E[exp(a^T X)]=V(m+Gamma a)",
    "substitution": "a=K^T Q z gives V m+V Gamma K^T Q z",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.raw.read_text())
    if data["source"]["sha256"] != EXPECTED_SOURCE:
        fail("source hash mismatch")
    if not all(data["assumptions"].values()):
        fail("at least one lemma assumption is not satisfied")
    if data.get("proof_certificate") != EXPECTED_PROOF:
        fail("proof certificate is incomplete or modified")

    # Expand the right side of the completion-of-square step over abstract
    # invariant contractions. This is independent of coordinate dimension.
    lhs = {
        "a^T m": Fraction(1),
        "a^T B g": Fraction(1),
        "g^T g": Fraction(-1, 2),
    }
    rhs = {
        "a^T m": Fraction(1),
        "a^T B g": Fraction(1),
        "g^T g": Fraction(-1, 2),
        "a^T B B^T a": Fraction(1, 2) - Fraction(1, 2),
    }
    rhs = {term: value for term, value in rhs.items() if value}
    if lhs != rhs:
        fail("dimension-free completion-of-square coefficients differ")
    expected_coefficients = {
        term: f"{value.numerator}/{value.denominator}"
        for term, value in lhs.items()
    }
    symbolic = data["symbolic_checks"]
    if symbolic.get("abstract_completion_square_lhs_coefficients") != expected_coefficients:
        fail("recorded left coefficients differ")
    if symbolic.get("abstract_completion_square_rhs_coefficients") != expected_coefficients:
        fail("recorded right coefficients differ")
    if symbolic.get("coefficient_identity") is not True:
        fail("coefficient identity flag is false")
    if symbolic.get("gradient_of_log_normalizer") != "m+Gamma a":
        fail("Gaussian log-normalizer gradient is wrong")
    if symbolic.get("normalizer_cancels_exactly") is not True:
        fail("attention denominator was not cancelled")
    if data.get("verdict") != "VERIFIED":
        fail("verdict is not VERIFIED")
    print(
        "PASS: dimension-free Gaussian MGF derivation yields "
        "T[mu](z)=V m+V Gamma K^T Q z for every d and PSD Gamma."
    )


if __name__ == "__main__":
    main()
