# Evaluator-blind review — full-domain round 2

Date: 2026-07-26

This repeat review began again from `README.md` in the fresh staged tree. It
checked the evaluator-visible rubric independently of the internal experiment
tree: current verifier precedence, exact claim contracts, inline results,
downloadable raw records, pinned command and environment, provenance, controls,
limitations, and historical preservation.

## Release visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | `pages/current-verification/page.md` | Yes | Yes | Yes | Yes | Yes | Yes | FALSIFIED |
| 2 | `pages/current-verification/page.md` | Yes | Yes | Yes | Yes | Yes | Yes | FALSIFIED |
| 3 | `pages/current-verification/page.md` | Yes | Yes | Yes | Yes | Yes | Yes | VERIFIED |
| 4 | `pages/current-verification/page.md` | Yes | Yes | Yes | Yes | Yes | Yes | VERIFIED |
| 5 | `pages/current-verification/page.md` | Yes | Yes | Yes | Yes | Yes | Yes | VERIFIED |

Additional findings:

- `current-verification` is first in `logbook.json`.
- The new `claim_5_full` packet is the obvious current Claim 5 verifier.
- The rejected Claim 5 dependency audit is explicitly labeled historical and
  remains reachable.
- All 20 cumulative tests and the evaluator-facing release audit passed on HF
  `cpu-upgrade`; the exact accepted SHAs, run IDs, 8.0-CPU quota, and runtimes
  are inline.
- The fixed command is identical for every experiment node.
- The exact 98 paths opened are recorded in
  `blind-review-full-domain-opened-files.txt`.

## Conclusions that could not be verified

- None.

**Round result: PASS.**
