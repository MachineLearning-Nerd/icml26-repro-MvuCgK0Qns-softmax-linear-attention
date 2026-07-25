#!/usr/bin/env python3
import json
import sys
from pathlib import Path

data = json.loads(Path(__file__).with_name("raw_result.json").read_text())
required = {
    "source_sha256": "6ae468a4032e920d159b609a78f1860bdf90004c7a692df60c601d9e3c9ff4c2",
    "assumptions_satisfied": True,
    "lhs_exact": "1",
    "rhs_exact_for_all_positive_c1_c2": "0",
    "strict_contradiction": True,
    "verdict": "FALSIFIED",
}
for key, expected in required.items():
    if data.get(key) != expected:
        print(f"FAIL: {key}", file=sys.stderr)
        raise SystemExit(1)
print("PASS: assumptions hold; exact LHS=1 > RHS=0 for every c1,c2>0.")
