#!/usr/bin/env python3
"""Fail-closed, lightweight verification for the final repository surface."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_REPO = "MachineLearning-Nerd/icml26-softmax-linear-attention"
EXPECTED_REMOTE = f"https://github.com/{EXPECTED_REPO}.git"
CANONICAL_NAME = "MachineLearning-Nerd"
CANONICAL_EMAIL = "MachineLearning-Nerd@users.noreply.github.com"
EXPECTED_BRANCHES = [
    "main",
    "baseline/judged-8-of-10",
    "audit/claim-1-prop-3-1",
    "audit/claim-2-prop-3-4",
    "proof/claim-3-lemma-2-1",
    "proof/claim-4-theorem-4-3",
    "audit/claim-5-dependency-gap",
    "proof/claim-5-full-domain",
    "release/evaluator-visible",
    "release/10-point-candidate",
    "release/final-publication",
]
CURRENT_DOCS = [
    "README.md",
    "STATUS.md",
    "claims.json",
    "CLAIM_EVIDENCE.md",
    "SOURCE_AUDIT.md",
    "SOURCE_MANIFEST.md",
    "ENVIRONMENT.md",
    "CITATION.cff",
    "reports/claim-by-claim/report.md",
]
EXPECTED_PDF_SHA256 = (
    "3e1c12c82e55e253f2933c139a676b1a642e552637a17ca273e3f0dc47423ede"
)


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def load(path: str):
    return json.loads(read(path))


errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


require(not git("status", "--porcelain").strip(), "working tree is not clean")
require(
    git("symbolic-ref", "--short", "HEAD").strip() == "main",
    "HEAD is not on main",
)
remote = git("remote", "get-url", "origin").strip()
require(remote.rstrip("/") == EXPECTED_REMOTE, f"origin is {remote!r}")

local_branches = sorted(
    line.strip()
    for line in git("for-each-ref", "--format=%(refname:short)", "refs/heads").splitlines()
    if line.strip()
)
require(local_branches == sorted(EXPECTED_BRANCHES), "local branch inventory differs")

for path in CURRENT_DOCS + ["EVIDENCE_MANIFEST.json", "verify_final.py"]:
    require((ROOT / path).is_file(), f"missing required file: {path}")

for path in CURRENT_DOCS:
    text = read(path)
    require(
        "https://github.com/MachineLearning-Nerd/icml26-repro-MvuCgK0Qns-softmax-linear-attention"
        not in text,
        f"old repository URL remains in current document: {path}",
    )
    require("orx/" not in text, f"legacy branch prefix remains in current document: {path}")

readme = read("README.md")
require(EXPECTED_REPO in readme, "README does not identify the final repository")
require("CITATION" in readme and "Thank you" in readme, "README missing citation/thanks")
require("FALSIFIED_AS_WRITTEN" in readme, "README missing literal falsification status")
require("VERIFIED_SCOPED_FULL_DOMAIN" in readme, "README missing full-domain status")

manifest = load("EVIDENCE_MANIFEST.json")
require(
    manifest["repository"]["final_name"] == "icml26-softmax-linear-attention",
    "manifest final name is wrong",
)
require(
    manifest["repository"]["canonical_identity"]
    == f"{CANONICAL_NAME} <{CANONICAL_EMAIL}>",
    "manifest canonical identity is wrong",
)
require(manifest["branch_inventory"] == EXPECTED_BRANCHES, "manifest branches differ")
require(
    manifest["collection_status"]
    == "VERIFIED_SCOPED_WITH_FALSIFIED_LITERAL_CLAIMS_AND_LIVE_SCORE_PENDING",
    "manifest collection status is wrong",
)

claims = load("claims.json")
require([item["id"] for item in claims] == ["claim_1", "claim_2", "claim_3", "claim_4", "claim_5"], "claim IDs differ")
require(
    [item["status"] for item in claims]
    == [
        "FALSIFIED_AS_WRITTEN",
        "FALSIFIED_AS_WRITTEN",
        "VERIFIED_SCOPED",
        "VERIFIED_SCOPED",
        "VERIFIED_SCOPED_FULL_DOMAIN",
    ],
    "claim status ledger differs",
)

paper_hash = hashlib.sha256((ROOT / "paper.pdf").read_bytes()).hexdigest()
require(paper_hash == EXPECTED_PDF_SHA256, "paper PDF hash differs")

summary = load("outputs/full/summary.json")
require(summary["claim_1"]["quadrature_cases"] == 48, "summary Claim 1 cases differ")
require(summary["claim_2"]["query_metric_comparisons"] == 18144, "summary Claim 2 comparisons differ")
require(summary["claim_3"]["trained_models"] == 36, "summary Claim 3 model count differs")
require(summary["compute"]["gpu_used"] is False, "summary reports GPU use")

packet_expectations = {
    "claim_1": ("FALSIFIED", "PASS", "EXPECTED REJECTION"),
    "claim_2": ("FALSIFIED", "PASS", "EXPECTED REJECTION"),
    "claim_3": ("VERIFIED", "PASS", "EXPECTED REJECTION"),
    "claim_4": ("VERIFIED", "PASS", "EXPECTED REJECTION"),
    "claim_5": ("BLOCKED", "PASS", "EXPECTED REJECTION"),
    "claim_5_full": ("VERIFIED", "PASS", "EXPECTED REJECTION"),
}
for packet, (target, checker_token, control_token) in packet_expectations.items():
    packet_root = ROOT / "space_candidate" / "evidence" / packet
    contract = json.loads((packet_root / "claim_contract.json").read_text(encoding="utf-8"))
    require(contract["verdict_target"] == target, f"{packet} contract target differs")
    checker = (packet_root / "independent_checker_output.txt").read_text(encoding="utf-8")
    control = (packet_root / "negative_control_output.txt").read_text(encoding="utf-8")
    require(checker_token in checker, f"{packet} independent checker is not PASS")
    require(control_token in control, f"{packet} negative control is not recorded")

claim_5_full = load("space_candidate/evidence/claim_5_full/raw_result.json")
require(claim_5_full["verdict"] == "VERIFIED", "full Claim 5 raw verdict differs")
require(
    claim_5_full["accepted_scientific_run"]["tests"] == "20/20",
    "full Claim 5 test record differs",
)

identity_lines = git("log", "--all", "--format=%an%x09%ae%x09%cn%x09%ce").splitlines()
for line in identity_lines:
    fields = line.split("\t")
    require(
        len(fields) == 4
        and fields[0] == CANONICAL_NAME
        and fields[1] == CANONICAL_EMAIL
        and fields[2] == CANONICAL_NAME
        and fields[3] == CANONICAL_EMAIL,
        f"non-canonical commit identity: {line}",
    )
commit_bodies = git("log", "--all", "--format=%B")
require("co-authored-by:" not in commit_bodies.lower(), "co-author trailer remains")

if errors:
    print(json.dumps({"status": "FAIL", "errors": errors}, indent=2))
    sys.exit(1)

print(
    json.dumps(
        {
            "status": "PASS",
            "repository": EXPECTED_REPO,
            "default_branch": "main",
            "branch_count": len(EXPECTED_BRANCHES),
            "paper_sha256": paper_hash,
            "claim_statuses": [item["status"] for item in claims],
            "canonical_identity": f"{CANONICAL_NAME} <{CANONICAL_EMAIL}>",
        },
        indent=2,
    )
)
