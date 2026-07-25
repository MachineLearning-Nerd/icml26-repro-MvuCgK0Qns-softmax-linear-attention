# Old/new Space preservation audit

- Judged file count: **20**
- Candidate file count: **95**
- Old filename set is a subset of the candidate filename set: **PASS**
- Every judged content hash remains somewhere in the candidate: **PASS**
- Text-only upload path count: **78**
- Binary additions or modifications in the upload allowlist: **none**

Changed canonical files whose original bytes are preserved additively:

| Canonical path | Judged SHA-256 | Preserved candidate path |
|---|---|---|
| `README.md` | `182d38b3562a404ffb83e76867965da911aee47d2171d6fdb61f97de246a1621` | `historical/judged-2f4196b0/README.md` |
| `logbook.json` | `a78d8dc130ed4a899a3400d2e07f733592ff2316c71073b0c219cfb1e758b793` | `historical/judged-2f4196b0/logbook.json` |
| `pages/index.md` | `917f7cf4d7d170201e3ab912fb34d020091feb7a53651cafd99210842179b90f` | `historical/judged-2f4196b0/index.md` |
