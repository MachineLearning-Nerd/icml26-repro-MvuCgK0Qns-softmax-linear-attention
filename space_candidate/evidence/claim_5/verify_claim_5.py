#!/usr/bin/env python3
"""Fail-closed BLOCKED verifier for Theorem 5.1."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path

PAPER_HASH = "6ae468a4032e920d159b609a78f1860bdf90004c7a692df60c601d9e3c9ff4c2"
JMLR_HASH = "3612edf523d550dfc549d1d47a0294f2bd2da7642bddfa56b8d4a0fa0bd93446"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.raw.read_text())
    source = data["source"]
    if source.get("paper_sha256") != PAPER_HASH:
        fail("paper source hash mismatch")
    if source.get("primary_reference_sha256") != JMLR_HASH:
        fail("primary JMLR source hash mismatch")
    sub = data["verified_subcertificate"]
    if sub.get("pointwise_squared_error") != "0 for every w and x":
        fail("pointwise Bayes error is not zero")
    if sub.get("risk") != "0":
        fail("Bayes risk subcertificate is not zero")
    if "nonnegative" not in sub.get("bayes_optimality", ""):
        fail("Bayes lower bound is missing")
    gaps = data["dependency_gap_certificate"]
    if gaps.get("domain_implication_holds") is not False:
        fail("covariance-domain gap was hidden")
    witness = gaps["condition_implication_counterexample"]
    if (
        witness.get("d") != 1
        or Fraction(witness.get("Sigma_op")) != Fraction(1, 4)
        or Fraction(witness.get("alpha")) != 4
        or witness.get("paper_condition_holds") is not True
        or Fraction(witness.get("jmlr_left_side")) != 4
        or witness.get("jmlr_condition_holds") is not False
    ):
        fail("initialization implication witness is invalid")
    if gaps.get("is_counterexample_to_theorem") is not False:
        fail("a proof gap was mislabeled as theorem falsification")
    if len(data.get("research_routes", {})) != 3:
        fail("three distinct research routes were not recorded")
    if data.get("verdict") != "BLOCKED" or data.get("confidence") != "MEDIUM":
        fail("honest BLOCKED/MEDIUM status changed")
    print(
        "BLOCKED: Bayes-zero limit algebra is exact, but the published universal "
        "Sigma/alpha domain is not covered by the cited convergence and assumption audits."
    )
    raise SystemExit(2)


if __name__ == "__main__":
    main()
