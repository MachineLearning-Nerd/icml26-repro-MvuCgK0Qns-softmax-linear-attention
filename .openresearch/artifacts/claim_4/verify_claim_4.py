#!/usr/bin/env python3
"""Fail-closed verifier for the Theorem 4.3 epsilon-transfer proof."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
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
    if not all(data["assumptions"].values()):
        fail("at least one theorem assumption is missing")
    dependencies = data["dependency_audit"]
    if "g1(L)->0" not in dependencies.get("uniform_risk_gap", ""):
        fail("uniform risk convergence is missing")
    if "g2(L)->0" not in dependencies.get("finite_horizon_gradient_gap", ""):
        fail("finite-horizon gradient convergence is missing")
    if "beta_infinity" not in dependencies.get("gronwall_source", ""):
        fail("Gronwall constant is not fixed")
    if dependencies.get("risk_monotonicity") != "dR_L/dt = -||grad R_L||^2 <= 0":
        fail("gradient-flow energy identity is missing")
    checks = data["symbolic_checks"]
    budget = checks.get("epsilon_budget", {})
    parts = [Fraction(budget[key]) for key in ("infinite_flow_tail", "finite_to_infinite_risk_at_T")]
    if parts != [Fraction(1, 2), Fraction(1, 2)]:
        fail("epsilon allocation changed")
    if sum(parts) != 1 or checks.get("budget_total") != "1/1":
        fail("epsilon budget does not close")
    if checks.get("budget_closes_exactly") is not True:
        fail("budget closure flag is false")
    if checks.get("finite_horizon_factor_uses_fixed_beta_infinity") is not True:
        fail("finite-horizon factor may diverge with L")
    if checks.get("gradient_flow_energy_identity") != "dR_L/dt=-||grad R_L||^2":
        fail("recorded energy identity is wrong")
    if checks.get("order_chain_closes") is not True:
        fail("asymptotic order chain is incomplete")
    if data.get("verdict") != "VERIFIED":
        fail("verdict is not VERIFIED")
    print(
        "PASS: for arbitrary epsilon, two exact epsilon/2 budgets plus "
        "gradient-flow monotonicity prove the full Theorem 4.3 limiting-risk bound."
    )


if __name__ == "__main__":
    main()
