#!/usr/bin/env python3
"""Fail-closed audit of the evaluator-visible text release surface."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SECRET_PATTERNS = {
    "Hugging Face token": re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    "GitHub token": re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "OpenAI token": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}
PACKET_FILES = {
    "EVAL.md",
    "claim_contract.json",
    "command.txt",
    "environment.md",
    "independent_check.py",
    "independent_checker_output.txt",
    "limitations.md",
    "method.md",
    "negative_control.py",
    "negative_control_output.txt",
    "raw_result.json",
    "source_audit.md",
    "verifier_output.txt",
}
FIXED_COMMAND = (
    "uv sync --frozen && uv run python reproduction/reproduce.py "
    "--output-dir outputs/full && uv run python -m unittest -v "
    "reproduction/test_reproduction.py"
)


def fail(message: str) -> None:
    print(f"RELEASE AUDIT FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def local_link(source: Path, target: str, root: Path) -> Path | None:
    target = target.split("#", 1)[0].strip()
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None
    if "/" not in target and Path(target).suffix == "":
        # Mathematical prose such as T[mu](z) is valid text but resembles a
        # Markdown link to the bare symbol "z".
        return None
    resolved = (source.parent / target).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        fail(f"link escapes candidate root: {source.relative_to(root)} -> {target}")
    return resolved


def traverse(root: Path) -> set[Path]:
    queue = [root / "README.md"]
    visited: set[Path] = set()
    while queue:
        path = queue.pop(0)
        if path in visited:
            continue
        if not path.is_file():
            fail(f"missing reachable file: {path.relative_to(root)}")
        visited.add(path)
        if path.suffix.lower() not in {".md", ".txt", ".json", ".py"}:
            continue
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            resolved = local_link(path, match.group(1), root)
            if resolved is not None and resolved not in visited:
                queue.append(resolved)
    return visited


def run_check(command: list[str], expected_code: int, expected_output: Path) -> None:
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode != expected_code:
        fail(
            f"{' '.join(command)} exited {result.returncode}, expected {expected_code}; "
            f"stderr={result.stderr.strip()}"
        )
    observed = result.stdout.strip()
    expected = expected_output.read_text(encoding="utf-8").strip()
    if observed != expected:
        fail(f"output mismatch for {' '.join(command)}")


def audit_claim(root: Path, claim: int, reachable: set[Path]) -> None:
    packet_name = "claim_5_full" if claim == 5 else f"claim_{claim}"
    packet = root / "evidence" / packet_name
    missing = sorted(PACKET_FILES - {path.name for path in packet.iterdir() if path.is_file()})
    if missing:
        fail(f"claim {claim} packet missing {missing}")
    verifier = packet / f"verify_claim_{claim}.py"
    if not verifier.is_file():
        fail(f"claim {claim} verifier missing")
    required_reachable = {packet / name for name in PACKET_FILES} | {verifier}
    hidden = sorted(str(path.relative_to(root)) for path in required_reachable - reachable)
    if hidden:
        fail(f"claim {claim} evidence not reachable from README: {hidden}")

    raw = packet / "raw_result.json"
    run_check(
        [sys.executable, str(verifier), "--raw", str(raw)],
        0,
        packet / "verifier_output.txt",
    )
    run_check(
        [sys.executable, str(packet / "independent_check.py")],
        0,
        packet / "independent_checker_output.txt",
    )
    run_check(
        [sys.executable, str(packet / "negative_control.py")],
        1,
        packet / "negative_control_output.txt",
    )
    if (packet / "command.txt").read_text(encoding="utf-8").strip() != FIXED_COMMAND:
        fail(f"claim {claim} command differs from the fixed contract")
    provenance = (
        (packet / "environment.md").read_text(encoding="utf-8")
        + "\n"
        + raw.read_text(encoding="utf-8")
    )
    for required in ("cpu-upgrade", "8.0", "cpu.max", "exact certificate took"):
        if required not in provenance:
            fail(f"claim {claim} provenance lacks {required}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    args = parser.parse_args()
    root = args.candidate.resolve()
    if not root.is_dir():
        fail("candidate directory does not exist")

    logbook = json.loads((root / "logbook.json").read_text(encoding="utf-8"))
    if logbook.get("space_id") != "DineshAI/MvuCgK0Qns":
        fail("logbook targets the wrong Space")
    children = logbook["root"]["children"]
    if not children or children[0].get("slug") != "current-verification":
        fail("current verifier is not first in logbook navigation")
    if not any(child.get("title") == "Historical rejected baseline" for child in children):
        fail("historical baseline label is missing")

    reachable = traverse(root)
    current = (root / "pages/current-verification/page.md").read_text(encoding="utf-8")
    for claim, verdict in {
        1: "FALSIFIED",
        2: "FALSIFIED",
        3: "VERIFIED",
        4: "VERIFIED",
        5: "VERIFIED",
    }.items():
        audit_claim(root, claim, reachable)
        row_pattern = re.compile(rf"\|\s*{claim}\s*\|[^\n]*\|\s*{verdict}\s*\|")
        if not row_pattern.search(current):
            fail(f"visibility matrix lacks claim {claim} verdict {verdict}")

    for required in (
        FIXED_COMMAND,
        "64130159f3df3a0053280ffde22bb70a7c791265",
        "20/20",
        "8.0 CPUs",
        "Historical rejected baseline",
    ):
        if required not in current:
            fail(f"current page lacks provenance item: {required}")

    historical_claim_5 = root / "evidence" / "claim_5"
    preserved = {historical_claim_5 / name for name in PACKET_FILES} | {
        historical_claim_5 / "verify_claim_5.py"
    }
    missing_historical = sorted(
        str(path.relative_to(root)) for path in preserved if not path.is_file()
    )
    if missing_historical:
        fail(f"historical Claim 5 packet missing: {missing_historical}")
    hidden_historical = sorted(
        str(path.relative_to(root)) for path in preserved - reachable
    )
    if hidden_historical:
        fail(f"historical Claim 5 packet not reachable: {hidden_historical}")

    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {
            ".md",
            ".txt",
            ".json",
            ".py",
            ".html",
            ".css",
            ".js",
            ".svg",
            "",
        }:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                fail(f"possible {name} in {path.relative_to(root)}")

    print(
        "PASS release audit: canonical traversal reaches all five complete packets; "
        "verifiers/checkers/controls return expected codes and outputs; "
        "navigation, provenance, logbook JSON, and secret scan pass."
    )


if __name__ == "__main__":
    main()
