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
| PREREG-PF4-001 | experiments/PREREG-PF4-001.md | 0277ce5 | 592fe7a26b36ed0d668dd506236804a883d39755d0e07635fbb2a6b9dbc99535 | 2026-08-04 | A. H. Bond (session instruction) |
| PREREG-PF4-002 | experiments/PREREG-PF4-002.md | 7f8d799 | fbba4d75ffecde249f20600ae9dfc720b781f68588e6db413dca386aa165d439 | 2026-08-04 | A. H. Bond (session instruction) |
| PREREG-PF4-003 | experiments/PREREG-PF4-003.md | 84bd95d | 87b932eaafd0a1e022a48e1f2089b9b260c6f217b75531e086257f2211a70902 | 2026-08-04 | A. H. Bond (session instruction) |
| PREREG-PF5-001 | experiments/PREREG-PF5-001.md | 15b4971 | 7e77e730d3477b1ed08ac03b796e684bdadfcd6b336eebc9f80c1b2b5ad62fcf | 2026-08-06 | A. H. Bond (session instruction) |
