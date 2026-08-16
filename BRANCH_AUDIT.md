# Branch audit

The final branch names describe the scientific role of each route. The legacy
names and tips below are retained so that the cleanup is auditable.

## Final public inventory

The intended final public inventory is exactly:

1. main
2. baseline/judged-8-of-10
3. audit/claim-1-prop-3-1
4. audit/claim-2-prop-3-4
5. proof/claim-3-lemma-2-1
6. proof/claim-4-theorem-4-3
7. audit/claim-5-dependency-gap
8. proof/claim-5-full-domain
9. release/evaluator-visible
10. release/10-point-candidate
11. release/final-publication

No legacy automation-prefixed branch should remain on GitHub after publication.

## Legacy-to-final mapping

The tips here are the legacy tips before the canonical author/committer
rewrite. The final verifier checks the resulting branch inventory and
canonical identities after rewrite.

| Final branch | Legacy branch | Legacy tip before rewrite | Role |
| --- | --- | --- | --- |
| main | master | 3c99cc5bb9b8a2d8a8b53ff2c7322708f6c07d6f | Publication surface |
| baseline/judged-8-of-10 | orx/validated-5-10-baseline | cb11fc2e8f9c2799ec00cbf9b4edb5adfe056607 | Historical judged baseline |
| audit/claim-1-prop-3-1 | orx/prop-3-1-literal-l-1-certificate | 11c4b34776950455d80f38e72a9988dbd50684ba | Proposition 3.1 boundary witness |
| audit/claim-2-prop-3-4 | orx/prop-3-4-literal-l-1-certificate | f870b70810cba489c3f3ecfcc288de211a3694db | Proposition 3.4 audit |
| proof/claim-3-lemma-2-1 | orx/lemma-2-1-dimension-free-proof-certificate | 131cc86a48fc20236b14e867cb6a8259e279ae96 | Lemma 2.1 proof |
| proof/claim-4-theorem-4-3 | orx/theorem-4-3-epsilon-transfer-proof-certificate | 3032eee545c94a36cfd834934ee34e0c2f965910 | Theorem 4.3 proof |
| audit/claim-5-dependency-gap | orx/theorem-5-1-bayes-certificate-and-dependency-aud | ab03d8e28985c00899253218175049cb32eb0077 | Historical blocked route |
| proof/claim-5-full-domain | orx/theorem-5-1-full-domain-direct-proof-certificate | 64130159f3df3a0053280ffde22bb70a7c791265 | Full-domain Claim 5 proof |
| release/evaluator-visible | orx/evaluator-visible-release-candidate | bbe74167d7aa8426b01d4fd55fd608397ac657de | Evaluator-visible release |
| release/10-point-candidate | orx/10-point-evaluator-visible-release-candidate | 2cf14723924197cb375b727d228631fa0e10ed16 | Candidate release |
| release/final-publication | orx/final-additive-space-publication | e5b0092e99abc35be3f447418cf48c15a02a597b | Publication manifest |

The old Claim 5 dependency-audit branch is deliberately not deleted from
history; it is renamed to audit/claim-5-dependency-gap so readers can inspect
why the direct proof was added.

## Cleanup invariants

- All reachable commits use author and committer
  MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>.
- No reachable commit contains a Co-authored-by: trailer.
- The GitHub default branch is main.
- The public branch inventory contains only the eleven final names above.
- The final repository name is icml26-softmax-linear-attention.
