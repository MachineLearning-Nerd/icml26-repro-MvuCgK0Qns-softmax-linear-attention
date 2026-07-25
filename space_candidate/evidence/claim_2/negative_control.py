#!/usr/bin/env python3
"""Valid degenerate measures that must not look like gradient contradictions."""

# mu=nu=delta_0, U=0, V=1, L=1. Both finite and population gradients vanish.
v_lhs = 0
u_lhs = 0
v_rhs = 0
u_rhs = 0
if v_lhs > v_rhs or u_lhs > u_rhs:
    print("UNEXPECTED: control was mislabeled as a contradiction")
    raise SystemExit(0)
print(
    "EXPECTED REJECTION: delta_0 gives zero gradient errors and zero bounds, "
    "so neither strict contradiction exists."
)
raise SystemExit(1)
