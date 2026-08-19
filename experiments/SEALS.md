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
| PREREG-PF5-002 | experiments/PREREG-PF5-002.md | 69b594d | 53a08c5ccc082f6cad913e0a9e957edc690f1145ad7217f70a13a388eb2e6917 | 2026-08-06 | A. H. Bond (session instruction) |
| PREREG-PF6-001 | experiments/PREREG-PF6-001.md | 8160039 | 7299902bc0adcc79ac5ce1a6eb4922612e292bf620e727da9303c49661544c3f | 2026-08-06 | A. H. Bond (session instruction) |
| PREREG-PF6-002 | experiments/PREREG-PF6-002.md | 5ecda35 | 3a42ce4ce8f22748ce0c9b90a4cdc3c04fc16a607314d3615aaca3264d898602 | 2026-08-06 | A. H. Bond (session instruction) |
| PREREG-PF4-009 | experiments/PREREG-PF4-009.md | c2d4522 | 58dba9e4c2a112310565d14cc4cd86b2675e0d57f298d0fc1a302e75f78cc282 | 2026-08-07 | A. H. Bond (session instruction) |
| GENERATOR-G1 | experiments/GENERATOR-G1.md | 5150771 | 99f953d948ce88ba3f1264009bacab0b8ee97e47529739266c793258e27f2761 | 2026-08-07 | A. H. Bond (session instruction) |
| GENERATOR-DOMAIN-POOL | experiments/GENERATOR-DOMAIN-POOL.md | 5150771 | c3e814a05753cf9fc050390900a908b181fd0f5f9b26c778f5c2398611ac85dd | 2026-08-07 | A. H. Bond (session instruction) |
| GENERATOR-DOMAIN-POOL-V2 | experiments/GENERATOR-DOMAIN-POOL-V2.md | 9e16022 | 9503db7ed2254a870f3770b5b2d84dcc4071b4d842213a222aa1c18b09ed0ea6 | 2026-08-07 | A. H. Bond (session instruction) |
| GENERATOR-DOMAIN-POOL-V3 | experiments/GENERATOR-DOMAIN-POOL-V3.md | a5589ae | 1589b0670d3aa6d5a6c161e8e3bf3735711475e4c7941e8103f789be9e5022c1 | 2026-08-07 | A. H. Bond (session instruction) |
| FORMAL-SYSTEMS-TRACK (sealed unrun) | experiments/FORMAL-SYSTEMS-TRACK.md | 39f514e | d6e8578b0e7b482ed621ba86e15b5fd5a045318f79887fb1ee497332b2cfc293 | 2026-08-07 | A. H. Bond (session instruction) |
| GENERATOR-G2 (governing, supersedes G1) | experiments/GENERATOR-G2.md | dbe2aa7 | dce0477c4eb66c7310f5108933a58edd2ed083e20b16857168f3faafc1ff03be | 2026-08-07 | A. H. Bond (session instruction) |
| PREREG-UN1-001 | experiments/PREREG-UN1-001.md | b549a29 | 3c22bc0d0ed56369acae9b5da816a46381768c6b589ccbd799d006112e5ae317 | 2026-08-07 | A. H. Bond (session instruction) |
| PREREG-UN1-002 | experiments/PREREG-UN1-002.md | ce0b05a | f1e1ac999210f42b2820243d976ae16c3fba135bc64ab9120328abb659b7c25d | 2026-08-07 | A. H. Bond (session instruction) |
| GO-P-2026-087 (migrated; orig. seal geometric-observation@63a6f56) | experiments/GO-P-2026-087-blind-recovery-scheduling.md | 897fd96 | eaf66f590d63bd2187338880fb7a066fbd99f8c97280cac3909cf8d999eb619e | 2026-08-19 | A. H. Bond (session instruction) |
| GO-P-2026-088 (migrated; orig. seal @705f068, amendment @7e68dba) | experiments/GO-P-2026-088-consumer-flip-sensing.md | 897fd96 | d172d1aba8b2ed28409d08d213dfb4e991ffcdf535a2274a7227e9d1e1ef0335 | 2026-08-19 | A. H. Bond (session instruction) |
| GO-P-2026-089 (migrated; orig. seal @705f068) | experiments/GO-P-2026-089-operational-trigger.md | 897fd96 | b69e446cf62f0859669bd9cc79e02722aadcaad683544a9bce0cb32e96040e26 | 2026-08-19 | A. H. Bond (session instruction) |
| PREREG-EC5-001 | experiments/PREREG-EC5-001.md | d77dbd9 | c501af6b17b8607befa3d2451f622b8463e687133963b59bdbbf3d95c89882cf | 2026-08-19 | A. H. Bond (session instruction) |
| PREREG-EC6-001 | experiments/PREREG-EC6-001.md | e773056 | f32b3d30d8fa77df8a1569ca259a302082929323851886783429688a1b576312 | 2026-08-19 | A. H. Bond (session instruction) |
| PREREG-EC7-001 | experiments/PREREG-EC7-001.md | e773056 | 05c994bff7735f029423c443dd1d989921272e0bf21bcdf2e8371e3f54e891f2 | 2026-08-19 | A. H. Bond (session instruction) |
| PREREG-EC7-002 | experiments/PREREG-EC7-002.md | 3f953c4 | feb475635e5a57566334ddc41a3c130f18c90c8efea8d361258495d36f5ba8b8 | 2026-08-19 | A. H. Bond (session instruction) |
