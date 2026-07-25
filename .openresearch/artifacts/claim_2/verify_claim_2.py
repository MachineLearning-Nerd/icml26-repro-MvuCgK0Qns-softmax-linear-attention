#!/usr/bin/env python3
"""Fail-closed verifier for the literal Proposition 3.4 counterexample."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

EXPECTED_SOURCE = "6ae468a4032e920d159b609a78f1860bdf90004c7a692df60c601d9e3c9ff4c2"
EXPECTED_MOMENTS = {"0": 1, "4": 3, "8": 105}


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
    expected = {"d": 1, "L": 1, "sigma": 1, "U": 0, "V": 1}
    for key, value in expected.items():
        if witness.get(key) != value:
            fail(f"witness field {key} changed")
    if not all(data["assumptions"].values()):
        fail("at least one stated assumption is not satisfied")
    audit = data["assumption_3_3_audit"]
    if audit.get("absolute_gaussian_moments") != EXPECTED_MOMENTS:
        fail("Gaussian moment table changed")
    bounds = audit.get("chosen_finite_bounds_at_U_0", {})
    for p in (0, 4, 8):
        for q in (0, 4, 8):
            if bounds.get(f"M_{p}_{q}") != EXPECTED_MOMENTS[str(p)] * EXPECTED_MOMENTS[str(q)]:
                fail(f"Assumption 3.3 bound M_{p}_{q} is invalid")
    calc = data["exact_calculation"]
    expected_exact = {
        "V_lhs_exact": "1",
        "V_rhs_exact_for_all_positive_c1_c2": "0",
        "U_lhs_exact": "1",
        "U_rhs_exact_for_all_positive_c1_c2": "0",
    }
    for key, value in expected_exact.items():
        if calc.get(key) != value:
            fail(f"{key} is not {value}")
    if calc.get("both_strict_contradictions") is not True:
        fail("both strict contradictions were not established")
    if data.get("verdict") != "FALSIFIED":
        fail("verdict is not FALSIFIED")
    print(
        "PASS: Assumption 3.3 holds; exact V- and U-gradient errors "
        "each have LHS=1 > RHS=0 for every c1,c2>0."
    )


if __name__ == "__main__":
    main()
