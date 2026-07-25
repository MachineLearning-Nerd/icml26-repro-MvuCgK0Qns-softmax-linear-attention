#!/usr/bin/env python3
"""Valid degenerate measures that must not look like gradient contradictions."""

v_lhs = u_lhs = v_rhs = u_rhs = 0
if v_lhs > v_rhs or u_lhs > u_rhs:
    print("UNEXPECTED: control was mislabeled as a contradiction")
    raise SystemExit(0)
print(
    "EXPECTED REJECTION: delta_0 gives zero gradient errors and zero bounds, "
    "so neither strict contradiction exists."
)
raise SystemExit(1)
