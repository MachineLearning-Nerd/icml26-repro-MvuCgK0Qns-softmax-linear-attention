# Live/candidate Space preservation audit v2

Date: 2026-07-26

- Live judged revision: `29699a404594b1b4f4e0e0028e09f5b3e13cbffa`
- Live file count after excluding the downloader cache: **95**
- Staged post-commit file count: **110**
- Live filename set is a subset of the staged post-commit set: **PASS**
- Missing live paths: **0**
- Proposed upload paths: **100**
- Proposed binary uploads: **0**
- Existing static and binary Space assets are left untouched by the additive
  text-only commit.

The original judged revision
`2f4196b0ec25bad9979ac21e92543168c33090a9` also remains byte-preserved under
`historical/judged-2f4196b0/`, as established by the prior preservation audit.
The prior blocked Claim 5 packet remains at `evidence/claim_5/` and is reachable
through the page labeled `Historical rejected baseline for Claim 5`; the
current verifier is the additive `evidence/claim_5_full/` packet.

**Subset result: PASS.**
