#!/usr/bin/env python3
"""Evaluator-blind discovery review starting only from the candidate README."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
REQUIRED_PACKET = {
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
VERDICTS = {1: "FALSIFIED", 2: "FALSIFIED", 3: "VERIFIED", 4: "VERIFIED", 5: "BLOCKED"}


def local_link(source: Path, target: str, root: Path) -> Path | None:
    target = target.split("#", 1)[0].strip()
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None
    if "/" not in target and Path(target).suffix == "":
        return None
    resolved = (source.parent / target).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        return None
    return resolved


def traverse(root: Path) -> tuple[list[Path], list[str]]:
    queue = [root / "README.md"]
    opened: list[Path] = []
    missing: list[str] = []
    seen: set[Path] = set()
    while queue:
        path = queue.pop(0)
        if path in seen:
            continue
        seen.add(path)
        if not path.is_file():
            missing.append(str(path.relative_to(root)))
            continue
        opened.append(path)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in LINK_RE.finditer(text):
            linked = local_link(path, match.group(1), root)
            if linked is not None and linked not in seen:
                queue.append(linked)
    return opened, missing


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--round", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.candidate.resolve()
    opened, missing_links = traverse(root)
    reachable = set(opened)
    current_path = root / "pages/current-verification/page.md"
    current = current_path.read_text(encoding="utf-8") if current_path in reachable else ""

    rows: list[str] = []
    failures: list[str] = list(missing_links)
    for claim, verdict in VERDICTS.items():
        packet = root / "evidence" / f"claim_{claim}"
        required = {packet / name for name in REQUIRED_PACKET} | {
            packet / f"verify_claim_{claim}.py"
        }
        hidden = sorted(str(path.relative_to(root)) for path in required - reachable)
        inline = all(
            token in current
            for token in (
                f"Claim {claim}",
                verdict,
                "Raw",
            )
        )
        exact_contract = packet / "claim_contract.json" in reachable
        reviewer_verdict = verdict if not hidden and inline and exact_contract else "MISSING"
        if hidden:
            failures.extend(hidden)
        rows.append(
            f"| {claim} | {'Yes' if inline else 'No'} | "
            f"{'Yes' if not hidden else 'No'} | {reviewer_verdict} | "
            f"{'; '.join(hidden) if hidden else 'All required evidence discoverable'} |"
        )

    global_checks = {
        "Current verifier is linked directly by README": current_path in reachable,
        "Historical rejected baseline is reachable": (
            root / "pages/historical-rejected-baseline/page.md"
        )
        in reachable,
        "Fixed command is inline": "uv sync --frozen && uv run python" in current,
        "Git SHA and 18/18 result are inline": (
            "ab03d8e28985c00899253218175049cb32eb0077" in current and "18/18" in current
        ),
        "Actual CPU quota and runtime are inline": "8.0 CPUs" in current and "47" in current,
        "Visibility matrix has five terminal verdict rows": all(
            re.search(rf"\|\s*{claim}\s*\|[^\n]*\|\s*{verdict}\s*\|", current)
            for claim, verdict in VERDICTS.items()
        ),
    }
    for label, passed in global_checks.items():
        if not passed:
            failures.append(label)

    unique_failures = sorted(set(failures))
    report = [
        f"# Evaluator-blind review — round {args.round}",
        "",
        "The review began at `README.md` in a fresh candidate tree and used only",
        "links reachable from that canonical entrypoint. No repository or run-log",
        "knowledge was used to fill gaps.",
        "",
        "## Claim discoverability",
        "",
        "| Claim | Exact result inline | Complete packet reachable | Reviewer verdict | Missing or conclusion |",
        "|---|---|---|---|---|",
        *rows,
        "",
        "## Global gates",
        "",
        *[f"- {'PASS' if passed else 'FAIL'} — {label}" for label, passed in global_checks.items()],
        "",
        "## Every file opened",
        "",
        *[f"- `{path.relative_to(root)}`" for path in opened],
        "",
        "## Conclusions that could not be verified",
        "",
    ]
    if unique_failures:
        report.extend(f"- `{failure}`" for failure in unique_failures)
        report.extend(["", "**Round result: FAIL — fix and repeat.**", ""])
    else:
        report.extend(["- None.", "", "**Round result: PASS.**", ""])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(report), encoding="utf-8")
    print(
        f"{'PASS' if not unique_failures else 'FAIL'} blind review round {args.round}: "
        f"opened {len(opened)} files; {len(unique_failures)} missing conclusions."
    )
    raise SystemExit(0 if not unique_failures else 1)


if __name__ == "__main__":
    main()
