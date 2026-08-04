# Seal ledger

Append-only. One entry per sealed document. A seal is the triple
(registration ID, sealing commit, SHA-256 of the sealed file's content as
stored in git at that commit, i.e. LF line endings). Verify with:

    git show <commit>:<path> | sha256sum

| Registration ID | File | Sealing commit | SHA-256 | Date | Authorized by |
|---|---|---|---|---|---|
| PF0-FREEZE-001 | experiments/PF0-TOLERANCE-FREEZE.md | 2b13a17 | 16c22d3dff6411a78b5ffbb5d12411a2b0be94951bf4bd894f57741e7fa63cbf | 2026-08-04 | A. H. Bond (session instruction) |
| PEQO-FREEZE-002 | experiments/PEQO-INSTRUMENT-FREEZE.md | 5240f60 | aaa25c0fa7bc1b978eba65af5ba43e691129fc5d5fd10a51c6cccfb5c3329a2f | 2026-08-04 | A. H. Bond (session instruction) |
| PREREG-QO2-001 | experiments/PREREG-QO2-001.md | 106f25e | f95317ae23ccab9ed472d9a7749a1e70b2a4575a5c2bd123cfbfa2ee7af9b2a3 | 2026-08-04 | A. H. Bond (session instruction) |
| PREREG-QO3-001 | experiments/PREREG-QO3-001.md | 106f25e | 41e93bfcbd8e0dc070358534bfb37003a5f5f08e6a84f44fdf4ba5f491a31a9b | 2026-08-04 | A. H. Bond (session instruction) |
