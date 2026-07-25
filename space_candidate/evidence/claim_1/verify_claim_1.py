#!/usr/bin/env python3
"""Fail-closed verifier for the literal Proposition 3.1 counterexample."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

EXPECTED_SOURCE = "6ae468a4032e920d159b609a78f1860bdf90004c7a692df60c601d9e3c9ff4c2"


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
    witness = data["witness"]
    expected = {"d": 1, "L": 1, "sigma": 1, "K": 0, "Q": 1, "V": 1, "M": 1}
    for key, value in expected.items():
        if witness.get(key) != value:
            fail(f"witness field {key} changed")
    if not all(data["assumptions"].values()):
        fail("at least one stated assumption is not satisfied")
    calc = data["exact_calculation"]
    if calc.get("lhs_exact") != "1":
        fail("left-hand side is not the exact Gaussian second moment 1")
    if calc.get("rhs_exact_for_all_positive_c1_c2") != "0":
        fail("right-hand side is not zero at L=1")
    if calc.get("strict_contradiction") is not True:
        fail("strict contradiction flag is false")
    if data.get("verdict") != "FALSIFIED":
        fail("verdict is not FALSIFIED")
    print("PASS: assumptions hold; exact LHS=1 > RHS=0 for every c1,c2>0.")


if __name__ == "__main__":
    main()
