#!/usr/bin/env python3
"""Finite-time closeness without monotonicity must not prove an asymptotic bound."""

comparison_time = 1
risk_at_comparison = 0
risk_later = 10 - comparison_time
if risk_later <= risk_at_comparison:
    print("UNEXPECTED: non-monotone control was accepted")
    raise SystemExit(0)
print(
    "EXPECTED REJECTION: R_L(T)=0 but R_L(10)=9 when monotonicity is removed; "
    "finite-horizon closeness alone does not imply the limiting-risk bound."
)
raise SystemExit(1)
