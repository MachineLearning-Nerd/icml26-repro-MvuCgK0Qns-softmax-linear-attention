#!/usr/bin/env python3
"""Generate and verify exact, theorem-calibrated claim evidence."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / ".openresearch" / "artifacts" / "claim_1"
CANDIDATE = ROOT / "space_candidate" / "evidence" / "claim_1"


def cpu_quota() -> dict[str, int | float | str | None]:
    cpu_max = Path("/sys/fs/cgroup/cpu.max")
    if not cpu_max.exists():
        return {"cpu_max": None, "quota_cpus": None}
    raw = cpu_max.read_text().strip()
    quota, period = raw.split()
    if quota == "max":
        return {"cpu_max": raw, "quota_cpus": None}
    return {"cpu_max": raw, "quota_cpus": int(quota) / int(period)}


def run_checked(script: Path, *args: str, expected: int = 0) -> str:
    proc = subprocess.run(
        [sys.executable, str(script), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    combined = proc.stdout + proc.stderr
    if proc.returncode != expected:
        raise RuntimeError(
            f"{script.name} returned {proc.returncode}, expected {expected}\n{combined}"
        )
    return combined


def run_claim_1_certificate() -> dict:
    start = time.perf_counter()
    git_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    result = {
        "claim_id": 1,
        "git_sha": git_sha,
        "source": {
            "url": "https://ar5iv.labs.arxiv.org/html/2512.11784",
            "retrieved_utc_date": "2026-07-25",
            "sha256": "6ae468a4032e920d159b609a78f1860bdf90004c7a692df60c601d9e3c9ff4c2",
            "anchor": "S3.Thmtheorem1",
        },
        "statement_scope": {
            "literal_prompt_domain": "positive integer L; no lower-bound qualifier appears",
            "bound": "E[||T[mu_hat_L]-T[mu]||^2_L2(nu)] <= c1*sigma^6*ln(L)/L^(c2/sigma^2)",
            "constants": "there exist c1,c2>0 depending only on d,V,K,Q,M",
        },
        "witness": {
            "d": 1,
            "L": 1,
            "mu": "N(0,1)",
            "nu": "N(0,1)",
            "sigma": 1,
            "K": 0,
            "Q": 1,
            "V": 1,
            "M": 1,
        },
        "assumptions": {
            "mu_centered_sigma_subgaussian": True,
            "nu_centered_1_subgaussian": True,
            "sigma_at_least_1": True,
            "infinite_attention_L4_at_most_sigma2_M": True,
            "iid_empirical_prompt": True,
        },
        "exact_calculation": {
            "finite_attention_L1": "X",
            "infinite_attention": "0",
            "lhs": "E_X E_Z[(X-0)^2] = E[X^2] = 1",
            "lhs_exact": "1",
            "rhs": "c1*1^6*ln(1)/1^(c2/1^2) = 0",
            "rhs_exact_for_all_positive_c1_c2": "0",
            "strict_contradiction": True,
        },
        "verdict": "FALSIFIED",
        "interpretation_risk": (
            "The certificate contradicts the literal displayed proposition. "
            "If an unstated restriction L>=2 or sufficiently large L was intended, "
            "that repaired statement is not falsified by this witness."
        ),
        "negative_control": {
            "mu": "delta_0",
            "L": 1,
            "lhs_exact": "0",
            "rhs_exact": "0",
            "strict_contradiction": False,
            "expected_detector_exit": 1,
        },
        "runtime": {
            "estimated_active_cores": 1,
            "selected_backend": "hf",
            "selected_flavor": "cpu-upgrade",
            **cpu_quota(),
        },
    }
    ARTIFACT.mkdir(parents=True, exist_ok=True)
    raw = ARTIFACT / "raw_result.json"
    raw.write_text(json.dumps(result, indent=2) + "\n")
    verifier_output = run_checked(ARTIFACT / "verify_claim_1.py", "--raw", str(raw))
    independent_output = run_checked(ARTIFACT / "independent_check.py")
    control_output = run_checked(ARTIFACT / "negative_control.py", expected=1)
    (ARTIFACT / "verifier_output.txt").write_text(verifier_output)
    (ARTIFACT / "independent_checker_output.txt").write_text(independent_output)
    (ARTIFACT / "negative_control_output.txt").write_text(control_output)
    result["runtime"]["certificate_wall_seconds"] = time.perf_counter() - start
    raw.write_text(json.dumps(result, indent=2) + "\n")

    CANDIDATE.mkdir(parents=True, exist_ok=True)
    for path in ARTIFACT.iterdir():
        if path.is_file():
            shutil.copy2(path, CANDIDATE / path.name)

    print("=== EXACT CLAIM 1 CERTIFICATE ===")
    print(raw.read_text())
    print("=== CLAIM 1 VERIFIER OUTPUT ===")
    print(verifier_output, end="")
    print("=== CLAIM 1 INDEPENDENT CHECKER OUTPUT ===")
    print(independent_output, end="")
    print("=== CLAIM 1 NEGATIVE CONTROL OUTPUT (EXPECTED EXIT 1) ===")
    print(control_output, end="")
    return result


if __name__ == "__main__":
    run_claim_1_certificate()
