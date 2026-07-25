#!/usr/bin/env python3
"""Prepare the exact text-only upload allowlist and preservation audit."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


TEXT_SUFFIXES = {"", ".css", ".html", ".js", ".json", ".md", ".py", ".svg", ".txt"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_manifest(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split(maxsplit=1)
        result[relative.removeprefix("./")] = digest
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--protected-manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    candidate = args.candidate.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)

    old = parse_manifest(args.protected_manifest)
    new_paths = {
        str(path.relative_to(candidate)): path
        for path in candidate.rglob("*")
        if path.is_file()
    }
    missing = sorted(set(old) - set(new_paths))
    if missing:
        raise SystemExit(f"FAIL old/new filename subset: missing {missing}")

    new_hashes = {relative: sha256(path) for relative, path in new_paths.items()}
    hash_locations: dict[str, list[str]] = {}
    for relative, digest in new_hashes.items():
        hash_locations.setdefault(digest, []).append(relative)

    unpreserved = {
        relative: digest
        for relative, digest in old.items()
        if digest not in hash_locations
    }
    if unpreserved:
        raise SystemExit(f"FAIL historical content preservation: {unpreserved}")

    upload = sorted(
        relative
        for relative, digest in new_hashes.items()
        if relative not in old or old[relative] != digest
    )
    non_text = [relative for relative in upload if Path(relative).suffix.lower() not in TEXT_SUFFIXES]
    if non_text:
        raise SystemExit(f"FAIL non-text upload path: {non_text}")

    allowlist_path = output / "upload-allowlist.txt"
    manifest_path = output / "upload-manifest.sha256"
    all_manifest_path = output / "candidate-manifest.sha256"
    allowlist_path.write_text("".join(f"{relative}\n" for relative in upload), encoding="utf-8")
    manifest_path.write_text(
        "".join(f"{new_hashes[relative]}  {relative}\n" for relative in upload),
        encoding="utf-8",
    )
    all_manifest_path.write_text(
        "".join(f"{new_hashes[relative]}  {relative}\n" for relative in sorted(new_hashes)),
        encoding="utf-8",
    )

    changed_old = sorted(relative for relative in old if old[relative] != new_hashes[relative])
    preserved_lines = []
    for relative in changed_old:
        locations = ", ".join(sorted(hash_locations[old[relative]]))
        preserved_lines.append(f"| `{relative}` | `{old[relative]}` | `{locations}` |")
    audit = [
        "# Old/new Space preservation audit",
        "",
        f"- Judged file count: **{len(old)}**",
        f"- Candidate file count: **{len(new_paths)}**",
        "- Old filename set is a subset of the candidate filename set: **PASS**",
        "- Every judged content hash remains somewhere in the candidate: **PASS**",
        f"- Text-only upload path count: **{len(upload)}**",
        "- Binary additions or modifications in the upload allowlist: **none**",
        "",
        "Changed canonical files whose original bytes are preserved additively:",
        "",
        "| Canonical path | Judged SHA-256 | Preserved candidate path |",
        "|---|---|---|",
        *preserved_lines,
        "",
    ]
    (output / "old-new-subset-check.md").write_text("\n".join(audit), encoding="utf-8")
    print(
        f"PASS manifest: {len(old)} judged paths remain; all judged hashes are preserved; "
        f"{len(upload)} text-only paths prepared."
    )


if __name__ == "__main__":
    main()
