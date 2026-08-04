# Seal ledger

Append-only. One entry per sealed document. A seal is the triple
(registration ID, sealing commit, SHA-256 of the sealed file's content as
stored in git at that commit, i.e. LF line endings). Verify with:

    git show <commit>:<path> | sha256sum

| Registration ID | File | Sealing commit | SHA-256 | Date | Authorized by |
|---|---|---|---|---|---|
| PF0-FREEZE-001 | experiments/PF0-TOLERANCE-FREEZE.md | 2b13a17 | 16c22d3dff6411a78b5ffbb5d12411a2b0be94951bf4bd894f57741e7fa63cbf | 2026-08-04 | A. H. Bond (session instruction) |
| PEQO-FREEZE-002 | experiments/PEQO-INSTRUMENT-FREEZE.md | 5240f60 | aaa25c0fa7bc1b978eba65af5ba43e691129fc5d5fd10a51c6cccfb5c3329a2f | 2026-08-04 | A. H. Bond (session instruction) |
