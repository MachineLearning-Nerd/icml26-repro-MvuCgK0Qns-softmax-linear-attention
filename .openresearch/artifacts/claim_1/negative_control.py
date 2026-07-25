#!/usr/bin/env python3
"""A valid degenerate sub-Gaussian instance that must not look like a contradiction."""

lhs = 0  # mu=delta_0, L=1, finite and infinite attention are both zero
rhs = 0
if lhs > rhs:
    print("UNEXPECTED: control was mislabeled as a contradiction")
    raise SystemExit(0)
print("EXPECTED REJECTION: delta_0 gives LHS=RHS=0, so no strict contradiction exists.")
raise SystemExit(1)
