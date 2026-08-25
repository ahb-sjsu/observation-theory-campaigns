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
| PREREG-EC7-003 | experiments/PREREG-EC7-003.md | 49ddef5 | 9ccbf32374107618034d21919a15b452ef06c2b623ed0b1dcc28c43283edccee | 2026-08-19 | A. H. Bond (session instruction) |
| PREREG-DR1-001 | experiments/PREREG-DR1-001.md | 4a3a304 | 12909466f579449f4832935341946f4760b8e6b9d7e858cb258ba97c61b262f0 | 2026-08-19 | A. H. Bond (session instruction) |
| PREREG-DR2-001 (post-run wording clarification @357a9a2, VI-14) | experiments/PREREG-DR2-001.md | 997c31f | 3284c9ea6cfc3fba4be35aaa6a35cbf00e49f188a0acfdadc1ce53f3f218ce83 | 2026-08-19 | A. H. Bond (session instruction) |
| PREREG-DR3-001 (post-run wording clarification @357a9a2, VI-15) | experiments/PREREG-DR3-001.md | b7ed62b | b05064481a319982f38476987694b4b64c451ba154b99a8fa6e3555800fdc0cc | 2026-08-19 | A. H. Bond (session instruction) |
| PREREG-LM1-001 | experiments/PREREG-LM1-001.md | 2a66fa5 | ce016794a366620afc4b496f1c48dc5bef5e0aa4309114fcd941e0a116fc68e3 | 2026-08-19 | A. H. Bond (session instruction) |
| PREREG-LM1-002 | experiments/PREREG-LM1-002.md | 9ef831b | c04c4bdb3c4dcd47278441061c0c7844b3d265b15fce805cea648118c8c6f448 | 2026-08-20 | A. H. Bond (session instruction) |
| PREREG-LM1-003 | experiments/PREREG-LM1-003.md | 011bc61 | f7bb68d38ad1da7478e87fecc88f6e2983bf83a10ffb9d698f24de45fb5cf340 | 2026-08-20 | A. H. Bond (session instruction) |
| PREREG-LM2-001 | experiments/PREREG-LM2-001.md | 253c1f3 | 3fa548fcb78ba65261f751665b37cda9663975ef18aaf4ae8198b1acda6d921b | 2026-08-20 | A. H. Bond (session instruction) |
| PREREG-LM2-002 | experiments/PREREG-LM2-002.md | f1ebcb1 | bef642971b15406d8afcc577a390c8e4163a4231a549298821f7815463e5a50b | 2026-08-20 | A. H. Bond (session instruction) |
| PREREG-DB1-001 | experiments/PREREG-DB1-001.md | cecb0e9 | 8fdebe65dfa9da5382e58b2dc61e6aa48398b40896c3ae5b581f595c35f9dc56 | 2026-08-21 | A. H. Bond (session instruction) |
| PREREG-DB2-001 | experiments/PREREG-DB2-001.md | 9ba55bc | 51a7ef133e274615b1eb4137e498ef6a6da9e57a678cb12271ddd8af74534d0a | 2026-08-21 | A. H. Bond (session instruction) |
| PREREG-DB3-001 | experiments/PREREG-DB3-001.md | 846a18d | 5ad9e7d33802a37a1dbeb9977d809bf895dcb8da20faba6c2bdbcdf04355edd9 | 2026-08-23 | A. H. Bond (session instruction) |

## Re-homed freshness cells (sealed in `network-governor`; cross-repo provenance)

Sealed in the `network-governor` repo before the 2026-08-24 re-home; **preserved,
not re-issued**. The sealing commit is a `network-governor` commit (prefix `ng:`);
the SHA-256 is of the sealed prereg content at that commit (LF line endings). The
prereg's path in network-governor equals its re-homed path below. Verify:
`git -C ../network-governor show <ng-commit>:<path> | sha256sum`.

| Registration ID | File (here) | NG sealing commit | SHA-256 (NG prereg content) | Date | Authorized by |
|---|---|---|---|---|---|
| XPROTO-PG | analysis/pgrep/PREREG-XPROTO-PG.md | ng:ba46687 | 640122c8848c52658f2b6871b0a47b0a268598c4b5454445e0f0a172cca791d3 | 2026-08-20 | A. H. Bond |
| XPROTO-MG | analysis/mongo/PREREG-XPROTO-MG.md | ng:e0a7a67 | 2ca041128e3a53724a24008e5fe490a53d8ddb88bd24a90711938ec75eae4a7c | 2026-08-21 | A. H. Bond |
| XPROTO-PGX | analysis/pgx/PREREG-XPROTO-PGX.md | ng:e0a7a67 | 81e726bad8a01614a64e702f0e4a092f728a0b16b94d8ff6d21dceff33181de1 | 2026-08-21 | A. H. Bond |
| XPROTO-GEO | analysis/geofleet/PREREG-XPROTO-GEO.md | ng:89557b8 | e18b1ded70a38f95167caf6e52b34aefa63415304db06b42383f0b18e7833819 | 2026-08-22 | A. H. Bond |
| XPROTO-ZK | analysis/zk/PREREG-XPROTO-ZK.md | ng:b36f433 | 000cd35ebbfb1ce5a528b55df61eec906bb01d7e0864318b4b4ac1e4ff2f350c | 2026-08-24 | A. H. Bond |
| XPROTO-CSI | analysis/csi/PREREG-XPROTO-CSI.md | ng:fda9148 | 683d86ec681a7788a4a9f1b75ea2d06ff2595e1288425323b11dc98206eaca92 | 2026-08-23 | A. H. Bond |
| XPROTO-BEAM | analysis/beam/PREREG-XPROTO-BEAM.md | ng:fda9148 | 13b18f159133ab2c8edb15ec2f18039b3892f4b9b374f9eea754545f19d6d281 | 2026-08-23 | A. H. Bond |
| XPROTO-AICSI | analysis/aicsi/PREREG-XPROTO-AICSI.md | ng:fda9148 | cf513425588de3214858ab48ac5aea30ba547a144fbdc01cbeaddfde3dd4f9d0 | 2026-08-23 | A. H. Bond |
| XPROTO-HO | analysis/ho/PREREG-XPROTO-HO.md | ng:fda9148 | 6763dfbe6afa8d600348828b96a0c3d2b80e3db7ada1660fa50635c8764e73f0 | 2026-08-23 | A. H. Bond |

### Freshness cells sealed natively in this repo

Sealed here after the re-home; the sealing commit is in **this** repo (no `ng:`
prefix). Verify: `git show <commit>:<path> | sha256sum`.

| Registration ID | File | Sealing commit | SHA-256 | Date | Authorized by |
|---|---|---|---|---|---|
| XPROTO-URLLC | analysis/urllc/PREREG-XPROTO-URLLC.md | 6375ebd | ea79ecb79b2adf7bced62e18b0df922680dd27a3cffa41b1bbbe46eb4686ce68 | 2026-08-24 | A. H. Bond |
| XPROTO-PHY | analysis/phy/PREREG-XPROTO-PHY.md | 6375ebd | 48998923768207f9311476ebdf56bdb1aef86949198fd5e9abdbc63548ee8eac | 2026-08-24 | A. H. Bond |
| XPROTO-QOT | analysis/qot/PREREG-XPROTO-QOT.md | 8bb6e5b | 90a99d36095c23f07f013964dcb7e613048f8ebfc7539e59596961cfade7dbb0 | 2026-08-25 | A. H. Bond |
| XPROTO-QOT-ML | analysis/qot/PREREG-XPROTO-QOT-ML.md | 8bb6e5b | 62129055bbb2db178877b40f057ccdc5246f121206d1ceec76e6554012af90d5 | 2026-08-25 | A. H. Bond |
| XPROTO-GRID | analysis/grid/PREREG-XPROTO-GRID.md | b61f7f1 | 3deecdb5897e45f5cd2f6a68a18e5041554039df7749ce48952980204a08cb8f | 2026-08-25 | A. H. Bond |
| XPROTO-LLM | analysis/llm/PREREG-XPROTO-LLM.md | b61f7f1 | 2b4889a693f6e0899ec22dc81187321001d409d2f921c02c0cce912f906739ed | 2026-08-25 | A. H. Bond |
