from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from reproduction.reproduce import finite_attention


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "full"


class ReproductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = json.loads((OUT / "summary.json").read_text())
        cls.quad = pd.read_csv(OUT / "quadrature_identity.csv")
        cls.rates = pd.read_csv(OUT / "concentration_rates.csv")
        cls.trajectory = pd.read_csv(OUT / "trajectory_gradients.csv")
        cls.bayes = pd.read_csv(OUT / "bayes_transfer.csv")
        cls.trained = pd.read_csv(OUT / "trained_models.csv")

    def test_gaussian_affine_identity(self):
        self.assertEqual(len(self.quad), 48)
        self.assertLess(self.quad.max_abs_error.max(), 1e-11)

    def test_non_gaussian_boundary(self):
        control = self.s["claim_1"]["rademacher_negative_control"]
        self.assertAlmostEqual(control["rademacher_output"], np.tanh(2.0), places=14)
        self.assertGreater(control["absolute_residual"], 1.0)

    def test_output_and_jacobian_concentration(self):
        self.assertEqual(len(self.rates), 9)
        self.assertTrue((self.rates.slope < -0.75).all())
        self.assertTrue((self.rates.slope > -1.25).all())
        self.assertTrue((self.rates.r_squared > 0.94).all())
        self.assertTrue((self.rates.reduction_16_to_1024 > 25).all())

    def test_analytic_jacobians_against_finite_differences(self):
        rng = np.random.default_rng(7); d = 3
        x = rng.normal(size=(80, d)); z = rng.normal(size=d)
        u = rng.normal(scale=.12, size=(d, d)); v = rng.normal(scale=.4, size=(d, d))
        out, ju, jv = finite_attention(x, z, u, v); eps = 1e-6
        numerical_u = np.empty_like(ju); numerical_v = np.empty_like(jv)
        for k in range(d * d):
            up = u.copy(); um = u.copy(); up.flat[k] += eps; um.flat[k] -= eps
            numerical_u[:, k] = (finite_attention(x, z, up, v)[0] - finite_attention(x, z, um, v)[0]) / (2 * eps)
            vp = v.copy(); vm = v.copy(); vp.flat[k] += eps; vm.flat[k] -= eps
            numerical_v[:, k] = (finite_attention(x, z, u, vp)[0] - finite_attention(x, z, u, vm)[0]) / (2 * eps)
        np.testing.assert_allclose(ju, numerical_u, rtol=2e-6, atol=2e-8)
        np.testing.assert_allclose(jv, numerical_v, rtol=2e-6, atol=2e-8)

    def test_gradient_stability_along_trajectory(self):
        self.assertEqual(len(self.trajectory), 24)
        self.assertTrue((self.trajectory.gradient_mse_L1024 < self.trajectory.gradient_mse_L16).all())

    def test_exact_bayes_transfer(self):
        self.assertLess(self.bayes.operator_identity_max_error.max(), 2e-15)
        self.assertLess(self.bayes.infinite_risk.max(), 1e-28)
        for _, group in self.bayes.groupby("regime"):
            self.assertGreater(group.iloc[0].finite_softmax_risk / group.iloc[-1].finite_softmax_risk, 100)

    def test_trained_models_approach_linear_solution(self):
        self.assertEqual(len(self.trained), 36)
        agg = self.trained.groupby(["regime", "prompt_length"], as_index=False).mean(numeric_only=True)
        for _, group in agg.groupby("regime"):
            self.assertGreater(group.iloc[0].finite_softmax_risk / group.iloc[-1].finite_softmax_risk, 30)
            self.assertGreater(group.iloc[0].parameter_distance_squared / group.iloc[-1].parameter_distance_squared, 10)

    def test_complete_cpu_outputs(self):
        expected = {"quadrature_identity.csv", "concentration_trials.csv", "concentration_aggregate.csv",
                    "concentration_rates.csv", "trajectory_gradients.csv", "bayes_transfer.csv",
                    "trained_models.csv", "softmax_linear_evidence.png", "claim_evidence.csv",
                    "summary.json", "source_manifest.json"}
        self.assertTrue(expected.issubset({p.name for p in OUT.iterdir()}))
        self.assertTrue(self.s["compute"]["cpu_only"]); self.assertFalse(self.s["compute"]["gpu_used"])

    def test_claim_1_exact_falsification_is_fail_closed(self):
        artifact = ROOT / ".openresearch" / "artifacts" / "claim_1"
        raw = artifact / "raw_result.json"
        verifier = artifact / "verify_claim_1.py"
        accepted = subprocess.run(
            [sys.executable, str(verifier), "--raw", str(raw)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
        with tempfile.TemporaryDirectory() as directory:
            tampered = Path(directory) / "tampered.json"
            payload = json.loads(raw.read_text())
            payload["exact_calculation"]["lhs_exact"] = "0"
            tampered.write_text(json.dumps(payload))
            rejected = subprocess.run(
                [sys.executable, str(verifier), "--raw", str(tampered)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        self.assertNotEqual(rejected.returncode, 0)

    def test_claim_1_independent_checker_and_negative_control(self):
        artifact = ROOT / ".openresearch" / "artifacts" / "claim_1"
        independent = subprocess.run(
            [sys.executable, str(artifact / "independent_check.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        control = subprocess.run(
            [sys.executable, str(artifact / "negative_control.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(independent.returncode, 0, independent.stdout + independent.stderr)
        self.assertEqual(control.returncode, 1, control.stdout + control.stderr)


if __name__ == "__main__":
    unittest.main()
