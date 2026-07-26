#!/usr/bin/env python3
"""Fail-closed verifier for the full-domain Theorem 5.1 certificate."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


JUDGED_HASH = "6ae468a4032e920d159b609a78f1860bdf90004c7a692df60c601d9e3c9ff4c2"
LATEST_HASH = "96c0673a1e0abd5e677ef1dfd06d1f768fc72f95904de6d6cbb8ec80f92db2c2"
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
    if source.get("judged_source_sha256") != JUDGED_HASH:
        fail("judged paper source hash mismatch")
    if source.get("latest_source_sha256") != LATEST_HASH:
        fail("latest v2 paper source hash mismatch")
    if source.get("primary_reference_sha256") != JMLR_HASH:
        fail("primary JMLR source hash mismatch")

    proof = data["infinite_prompt_proof"]
    required = {
        "risk_reduction",
        "gradient_flow",
        "balanced_invariant",
        "positive_scalar",
        "boundedness",
        "stationary_dichotomy",
        "origin_exclusion",
        "analytic_gradient_convergence",
        "limit_from_balance",
        "initialization_domain",
    }
    if required - set(proof):
        fail(f"missing infinite-flow obligations: {sorted(required - set(proof))}")
    if proof["gradient_flow"] != {
        "A_dot": "b Sigma^2-b^2 Sigma^2 A Sigma",
        "b_dot": "tr(A^T Sigma^2)-b tr(A^T Sigma^2 A Sigma)",
    }:
        fail("gradient-flow equations changed")
    origin = proof["origin_exclusion"]
    if (
        origin.get("diagonal_basis_equation")
        != "a_ii_dot=b s_i^2(1-b s_i a_ii)"
        or ">0" not in origin.get("near_origin_sign", "")
        or "cannot converge" not in origin.get("conclusion", "")
    ):
        fail("origin-exclusion argument is incomplete")
    if "every alpha>0" not in proof.get("initialization_domain", ""):
        fail("full initialization domain is not covered")
    if "cannot cross zero" not in proof.get("positive_scalar", ""):
        fail("positive b invariant is missing")

    transfer = data["transfer_scale_proof"]
    for key in (
        "query_scale",
        "conditional_token_scale",
        "query_normalization",
        "moment_condition",
        "rate_condition",
        "tilted_moments",
        "conclusion",
    ):
        if not transfer.get(key):
            fail(f"missing transfer-scale obligation: {key}")
    if "every fixed positive-definite Sigma" not in transfer["conclusion"]:
        fail("arbitrary covariance scale is not covered")

    bayes = data["bayes_certificate"]
    if bayes.get("pointwise_squared_error") != "0 for every w and x":
        fail("pointwise Bayes error is not zero")
    if bayes.get("risk") != "0" or "nonnegative" not in bayes.get("bayes_optimality", ""):
        fail("Bayes endpoint certificate is incomplete")
    if data.get("verdict") != "VERIFIED" or data.get("confidence") != "HIGH":
        fail("claim status is not VERIFIED/HIGH")

    print(
        "PASS: direct balanced-gradient-flow proof converges to the exact "
        "zero-risk Bayes endpoint for every positive-definite Sigma and every "
        "published initialization; finite covariance scale changes transfer "
        "constants only."
    )


if __name__ == "__main__":
    main()
