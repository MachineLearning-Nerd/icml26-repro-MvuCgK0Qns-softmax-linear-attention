#!/usr/bin/env python3
"""Generate and verify exact, theorem-calibrated claim evidence."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = ROOT / ".openresearch" / "artifacts"
CANDIDATE_ROOT = ROOT / "space_candidate" / "evidence"


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
    artifact = ARTIFACT_ROOT / "claim_1"
    candidate = CANDIDATE_ROOT / "claim_1"
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
    artifact.mkdir(parents=True, exist_ok=True)
    raw = artifact / "raw_result.json"
    raw.write_text(json.dumps(result, indent=2) + "\n")
    verifier_output = run_checked(artifact / "verify_claim_1.py", "--raw", str(raw))
    independent_output = run_checked(artifact / "independent_check.py")
    control_output = run_checked(artifact / "negative_control.py", expected=1)
    (artifact / "verifier_output.txt").write_text(verifier_output)
    (artifact / "independent_checker_output.txt").write_text(independent_output)
    (artifact / "negative_control_output.txt").write_text(control_output)
    result["runtime"]["certificate_wall_seconds"] = time.perf_counter() - start
    raw.write_text(json.dumps(result, indent=2) + "\n")

    candidate.mkdir(parents=True, exist_ok=True)
    for path in artifact.iterdir():
        if path.is_file():
            shutil.copy2(path, candidate / path.name)

    print("=== EXACT CLAIM 1 CERTIFICATE ===")
    print(raw.read_text())
    print("=== CLAIM 1 VERIFIER OUTPUT ===")
    print(verifier_output, end="")
    print("=== CLAIM 1 INDEPENDENT CHECKER OUTPUT ===")
    print(independent_output, end="")
    print("=== CLAIM 1 NEGATIVE CONTROL OUTPUT (EXPECTED EXIT 1) ===")
    print(control_output, end="")
    return result


def run_claim_2_certificate() -> dict:
    artifact = ARTIFACT_ROOT / "claim_2"
    candidate = CANDIDATE_ROOT / "claim_2"
    start = time.perf_counter()
    git_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    moments = {"0": 1, "4": 3, "8": 105}
    moment_bounds = {
        f"M_{p}_{q}": moments[str(p)] * moments[str(q)]
        for p in (0, 4, 8)
        for q in (0, 4, 8)
    }
    result = {
        "claim_id": 2,
        "git_sha": git_sha,
        "source": {
            "url": "https://ar5iv.labs.arxiv.org/html/2512.11784",
            "retrieved_utc_date": "2026-07-25",
            "sha256": "6ae468a4032e920d159b609a78f1860bdf90004c7a692df60c601d9e3c9ff4c2",
            "proposition_anchor": "S3.Thmtheorem4",
            "assumption_anchor": "S3.Thmtheorem3",
        },
        "statement_scope": {
            "literal_prompt_domain": "positive integer L; no lower-bound qualifier appears",
            "V_bound": (
                "E[||grad_V T[mu_hat_L]-grad_V T[mu]||^2_L2(nu)] "
                "<= c1*sigma^6*ln(L)/L^(c2/sigma^2)"
            ),
            "U_bound": (
                "E[||grad_U T[mu_hat_L]-grad_U T[mu]||^2_L2(nu)] "
                "<= c1*sigma^12*ln(L)^2/L^(c2/sigma^2)"
            ),
            "constants": "there exist c1,c2>0 depending only on d,U,V",
        },
        "witness": {
            "d": 1,
            "L": 1,
            "mu": "N(0,1)",
            "nu": "N(0,1)",
            "sigma": 1,
            "U": 0,
            "V": 1,
        },
        "assumptions": {
            "mu_centered_sigma_subgaussian": True,
            "nu_centered_1_subgaussian": True,
            "sigma_at_least_1": True,
            "assumption_3_3_all_nine_moment_bounds_finite": True,
            "iid_empirical_prompt": True,
        },
        "assumption_3_3_audit": {
            "orders": [0, 4, 8],
            "absolute_gaussian_moments": moments,
            "chosen_finite_bounds_at_U_0": moment_bounds,
            "derivation": (
                "At U=0 the exponential tilt is 1, so the left side is "
                "E|X|^p E|Z|^q. With sigma=1, choosing M_pq equal to that "
                "finite product satisfies every p,q bound with equality."
            ),
        },
        "exact_calculation": {
            "finite_V_gradient_L1": "X",
            "population_V_gradient_at_U0": "0",
            "V_lhs": "E[X^2] = 1",
            "V_lhs_exact": "1",
            "V_rhs_exact_for_all_positive_c1_c2": "0",
            "finite_U_gradient_L1": "0",
            "population_U_gradient_at_U0_V1": "Z",
            "U_lhs": "E[Z^2] = 1",
            "U_lhs_exact": "1",
            "U_rhs_exact_for_all_positive_c1_c2": "0",
            "both_strict_contradictions": True,
        },
        "verdict": "FALSIFIED",
        "interpretation_risk": (
            "The certificate contradicts the literal displayed proposition. "
            "If an unstated restriction L>=2 or sufficiently large L was intended, "
            "that repaired statement is not falsified by this witness."
        ),
        "negative_control": {
            "mu": "delta_0",
            "nu": "delta_0",
            "L": 1,
            "V_lhs_exact": "0",
            "U_lhs_exact": "0",
            "both_rhs_exact": "0",
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
    artifact.mkdir(parents=True, exist_ok=True)
    raw = artifact / "raw_result.json"
    raw.write_text(json.dumps(result, indent=2) + "\n")
    verifier_output = run_checked(artifact / "verify_claim_2.py", "--raw", str(raw))
    independent_output = run_checked(artifact / "independent_check.py")
    control_output = run_checked(artifact / "negative_control.py", expected=1)
    (artifact / "verifier_output.txt").write_text(verifier_output)
    (artifact / "independent_checker_output.txt").write_text(independent_output)
    (artifact / "negative_control_output.txt").write_text(control_output)
    result["runtime"]["certificate_wall_seconds"] = time.perf_counter() - start
    raw.write_text(json.dumps(result, indent=2) + "\n")

    candidate.mkdir(parents=True, exist_ok=True)
    for path in artifact.iterdir():
        if path.is_file():
            shutil.copy2(path, candidate / path.name)

    print("=== EXACT CLAIM 2 CERTIFICATE ===")
    print(raw.read_text())
    print("=== CLAIM 2 VERIFIER OUTPUT ===")
    print(verifier_output, end="")
    print("=== CLAIM 2 INDEPENDENT CHECKER OUTPUT ===")
    print(independent_output, end="")
    print("=== CLAIM 2 NEGATIVE CONTROL OUTPUT (EXPECTED EXIT 1) ===")
    print(control_output, end="")
    return result


def run_claim_3_certificate() -> dict:
    artifact = ARTIFACT_ROOT / "claim_3"
    candidate = CANDIDATE_ROOT / "claim_3"
    start = time.perf_counter()
    git_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    # Dimension-free coefficient check of the only algebraic step in completing
    # the square. Keys name invariant scalar contractions, not coordinates.
    lhs_coefficients = {
        "a^T m": Fraction(1),
        "a^T B g": Fraction(1),
        "g^T g": Fraction(-1, 2),
    }
    rhs_coefficients = {
        "a^T m": Fraction(1),
        "a^T B g": Fraction(1),  # g^T B^T a by scalar-transpose symmetry
        "g^T g": Fraction(-1, 2),
        "a^T B B^T a": Fraction(1, 2) - Fraction(1, 2),
    }
    rhs_coefficients = {
        key: value for key, value in rhs_coefficients.items() if value != 0
    }
    coefficient_json = {
        key: f"{value.numerator}/{value.denominator}"
        for key, value in lhs_coefficients.items()
    }
    result = {
        "claim_id": 3,
        "git_sha": git_sha,
        "source": {
            "url": "https://ar5iv.labs.arxiv.org/html/2512.11784",
            "retrieved_utc_date": "2026-07-25",
            "sha256": "6ae468a4032e920d159b609a78f1860bdf90004c7a692df60c601d9e3c9ff4c2",
            "anchor": "S2.Thmtheorem1",
        },
        "statement_scope": {
            "domain": (
                "every dimension d, Gaussian mu=N(m,Gamma) with positive-"
                "semidefinite covariance Gamma, compatible real K,Q,V, and z in R^d"
            ),
            "identity": "T^{K,Q,V}[mu](z) = V m + V Gamma K^T Q z",
        },
        "assumptions": {
            "mu_is_gaussian": True,
            "Gamma_is_positive_semidefinite_including_singular_case": True,
            "matrices_and_vector_are_dimension_compatible": True,
            "attention_denominator_is_finite_and_positive": True,
        },
        "proof_certificate": {
            "representation": "X=m+B G, G~N(0,I_r), Gamma=B B^T; valid for every PSD Gamma",
            "score_vector": "a=K^T Q z",
            "completion_of_square": (
                "a^T(m+B g)-||g||^2/2 = a^T m+||B^T a||^2/2"
                "-||g-B^T a||^2/2"
            ),
            "normalizer": "E exp(a^T X)=exp(a^T m+a^T Gamma a/2)",
            "differentiated_normalizer": (
                "E[X exp(a^T X)]=(m+Gamma a)"
                "*exp(a^T m+a^T Gamma a/2)"
            ),
            "ratio": "E[V X exp(a^T X)]/E[exp(a^T X)]=V(m+Gamma a)",
            "substitution": "a=K^T Q z gives V m+V Gamma K^T Q z",
        },
        "symbolic_checks": {
            "abstract_completion_square_lhs_coefficients": coefficient_json,
            "abstract_completion_square_rhs_coefficients": coefficient_json,
            "coefficient_identity": lhs_coefficients == rhs_coefficients,
            "quadratic_form_substitution": "||B^T a||^2=a^T B B^T a=a^T Gamma a",
            "gradient_of_log_normalizer": "m+Gamma a",
            "normalizer_cancels_exactly": True,
        },
        "verdict": "VERIFIED",
        "negative_control": {
            "measure": "Rademacher on {-1,+1}",
            "d": 1,
            "m": 0,
            "Gamma": 1,
            "a": 2,
            "true_attention": "tanh(2)",
            "gaussian_formula": "2",
            "formula_is_rejected": True,
            "expected_detector_exit": 1,
        },
        "limitations": (
            "This certificate verifies the exact operator identity in the judged "
            "claim. The additional pushforward-distribution formula in the lemma "
            "is audited separately but is not required by the imported Claim 3."
        ),
        "runtime": {
            "estimated_active_cores": 1,
            "selected_backend": "hf",
            "selected_flavor": "cpu-upgrade",
            **cpu_quota(),
        },
    }
    artifact.mkdir(parents=True, exist_ok=True)
    raw = artifact / "raw_result.json"
    raw.write_text(json.dumps(result, indent=2) + "\n")
    verifier_output = run_checked(artifact / "verify_claim_3.py", "--raw", str(raw))
    independent_output = run_checked(artifact / "independent_check.py")
    control_output = run_checked(artifact / "negative_control.py", expected=1)
    (artifact / "verifier_output.txt").write_text(verifier_output)
    (artifact / "independent_checker_output.txt").write_text(independent_output)
    (artifact / "negative_control_output.txt").write_text(control_output)
    result["runtime"]["certificate_wall_seconds"] = time.perf_counter() - start
    raw.write_text(json.dumps(result, indent=2) + "\n")

    candidate.mkdir(parents=True, exist_ok=True)
    for path in artifact.iterdir():
        if path.is_file():
            shutil.copy2(path, candidate / path.name)

    print("=== EXACT CLAIM 3 CERTIFICATE ===")
    print(raw.read_text())
    print("=== CLAIM 3 VERIFIER OUTPUT ===")
    print(verifier_output, end="")
    print("=== CLAIM 3 INDEPENDENT CHECKER OUTPUT ===")
    print(independent_output, end="")
    print("=== CLAIM 3 NEGATIVE CONTROL OUTPUT (EXPECTED EXIT 1) ===")
    print(control_output, end="")
    return result


if __name__ == "__main__":
    run_claim_1_certificate()
    run_claim_2_certificate()
    run_claim_3_certificate()
