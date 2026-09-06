# false-clear rate

**id.** false-clear-rate
**kind.** concept

## definition

The fraction of the decisions a certificate cleared in which the witness said otherwise, conditional on clearing and reported beside the certificate's coverage. Equation 0.26.

## equation

Book equation 0.26.

    \mathrm{FC}=\Pr\big[W\ \text{refutes}\ \big|\ \mathcal C_t\ \text{clears}\big],\qquad \text{coverage}=\Pr\big[\mathcal C_t\ \text{clears}\big].

Book equation 13.1.

    \mathrm{FC}=\Pr\big[W\ \text{refutes}\ \big|\ \mathcal C_t\ \text{clears}\big],\qquad d_O(\Delta)=\operatorname{tr}\big(P_C\,M_{\mathrm{drift}}(\Delta)\big),\qquad M_{\mathrm{drift}}(\Delta)=\mathbb E\big[\delta_\Delta\delta_\Delta^{\top}\big].

Book equation 12.4.

    \begin{gathered} \mathrm{FC}_{\text{naive}}=\Pr\big[\mathrm{acc}_s<\text{target}\ \big|\ \text{benchmark}\ge\text{target}\big]=\frac1S\sum_{s=1}^{S}\mathbf 1\big[\mathrm{acc}_s<\text{target}\big] \\ \text{when the benchmark clears, so that the naive certificate's coverage is 1.} \end{gathered}

## ledger

none

## first stated

Volume 14 chapter 19, `geometric-observation/chapters/ch19_the_certificate_that_ages.md:61-76`, and the freshness program's umbrella document `observation-theory-campaigns/experiments/FRESHNESS-PROGRAM.md`, re-homed into the campaigns repository on 2026-08-24.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 12 section 12.6 | XPROTO-LLM, benchmark 0.909, 0.920, 0.909, thirty slices, target 0.8, naive 0.333, aware 0.033, spread 0.380, deployment mean 0.736, six bars on three seeds, sealed 2026-08-25 at b61f7f1 | `observation-theory-campaigns\experiments\LLM-EVAL-TRACK.md:1-50`; `observation-theory-campaigns\analysis\llm\XPROTO-LLM-graded.json`; `observation-theory-campaigns\experiments\SEALS.md:85` |
| chapter 13 section 13.3 | ZooKeeper hot 0.99 cold 0.01 witnessed 0.0, Postgres 0.50 to 0.06, MongoDB 0.47 to 0.03, production Postgres 0.47 to 0.02, real substrates, disjoint seeds | `observation-theory-campaigns\experiments\DATABASE-FRESHNESS-TRACK.md:1-45` |
| chapter 13 section 13.3 | BGP 0.351, IS-IS 0.184, OSPF 0.083, second collector | `observation-theory-campaigns\analysis\mongo\PREREG-XPROTO-MG.md:42`; `observation-theory-campaigns\experiments\ROUTING-TELEMETRY-TRACK.md:130-150`; `geometric-observation\BOOK-OUTLINE.md:75` |
| chapter 13 section 13.3 | radio 0.27 to 0.42 naive to 0.055 to 0.13, neural reconstruction 0.28 to 0.13 | `observation-theory-campaigns\experiments\RADIO-FRESHNESS-TRACK.md:20-35` |
| chapter 13 section 13.4 | refuted fit 0.177 T_coh R² 0.915, 0.15 threshold vs 0.10 claim, fresh baseline 0.113, do not cite | `observation-theory-campaigns\analysis\csi\CSI-refreshfloor.json:2,111-114`; `observation-theory-campaigns\experiments\RADIO-FRESHNESS-TRACK.md:41-47` |
| chapter 13 section 13.4 | sealed correction, 0.5 dB calibration, floors 4/6/4, 2/2/3, 1, slopes 0.1008, 0.1398, 0.1086, R² 0.7376, 0.9218, 0.6174, bars B1 to B4 and MC1 to MC4 all true, seeds 20260827 to 20260829, sealed 1d3de4a | `observation-theory-campaigns\analysis\csi\PREREG-XPROTO-CSI-SWEEP2.md:1-60`; `observation-theory-campaigns\analysis\csi\XPROTO-CSI-SWEEP2-graded.json`; `observation-theory-campaigns\experiments\SEALS.md:90` |

From `observation-theory-campaigns/experiments/DATABASE-FRESHNESS-TRACK.md` at 429cc9d.

- line 23. XPROTO-PG (analysis/pgrep) | Postgres, recovery_min_apply_delay | WAL LSN | ~0.50 → ~0.06
- line 24. XPROTO-MG (analysis/mongo) | MongoDB delayed secondary | oplog ts | ~0.47 → ~0.03
- line 25. XPROTO-PGX (analysis/pgx) | production PG, netem lag | WAL LSN, pg_stat_statements footprint | ~0.47 → ~0.02
- line 27. XPROTO-ZK (analysis/zk) | ZooKeeper 3.9 ensemble | zxid, sync() | hot 0.99 / cold 0.01, witnessed 0.0

From `observation-theory-campaigns/experiments/RADIO-FRESHNESS-TRACK.md` at 429cc9d.

- line 25. XPROTO-CSI (analysis/csi) | CQI → MCS | HARQ | 0.34–0.37 → 0.10 (OLLA) | ✅ 08-23
- line 26. XPROTO-BEAM (analysis/beam) | mmWave beam index | HARQ | 0.31 → 0.02 (BFR) | ✅ 08-23
- line 27. XPROTO-AICSI (analysis/aicsi) | neural-CSI recon (turboquant bridge) | precoder/HARQ | recon wins yet 0.28 → 0.13 | ✅ 08-23, scope-corrected 08-25 ⚠️
- line 28. XPROTO-HO (analysis/ho) | RSRP → serving cell | RLF | 0.31–0.44 → 0.09–0.12 | ✅ 08-23
- line 30. XPROTO-PHY (analysis/phy) | PMI / RI / TA | HARQ | 0.27–0.42 → 0.055–0.13 | ✅ 08-24

## failures and corrections

- `observation-theory-campaigns/experiments/RADIO-FRESHNESS-TRACK.md:33-39` at 429cc9d. ⚠️ **XPROTO-AICSI scope correction (2026-08-25).** The v1 seal stands for what it tested, but the reconstruction-vs-consumer dissociation does **not** survive the community-standard substrate. On real 3GPP CDL-C with a CsiNet-class codec the NMSE-optimal codec reconstructs near-perfectly (NMSE ≈ 0.03) and false-clears 0.0 on all seeds; the pre-registered kill fired. See `analysis/aicsi/PREREG-XPROTO-AICSI-V2.md` (REFUTED AT SHAKEDOWN, NOT SEALED, kept negative). This is a scope correction, not a retraction. Do not headline the AICSI row; WCNC §III-C is dropped.
- `observation-theory-campaigns/experiments/RADIO-FRESHNESS-TRACK.md:41-50` at 429cc9d. **The age horizon** (`analysis/csi/`, XPROTO-CSI-SWEEP2 sealed 2026-08-27, graded PASS): at the calibrated 0.10 budget the largest compliant report period is a few TTI at 10 Hz and 1 TTI at 50 Hz and above, so there is no proportionality law to fit. The earlier `CSI-refreshfloor.*` claim of a floor ≈ 0.177·T_coh (R²=0.915) was an **unsealed exploration** measured at a relaxed 0.15 threshold against the 0.10 target, with a fresh baseline that never met the budget. It is refuted; the record is kept, not cited. Separately, the optimal linear predictor cannot beat the one-coherence-time wall (Gaussian fading → Wiener optimal), and that wall sits well outside the budget horizon. The **RAN governor** (`analysis/ran`) is the reference O-RAN rApp core: observe→measure false-clear→refresh at the floor→escalate (diversity / re-route).
- `geometric-observation/chapters/ch19_the_certificate_that_ages.md:69-76` at 7d91883. — the rate at which a clearance is wrong, conditional on the certificate having cleared, reported beside the certificate's coverage. (An earlier draft wrote the joint probability $\Pr[\text{clears} \wedge \text{refutes}]$; the joint rate is the product of the two and is what a naive certificate that clears everything reports, since its coverage is one. Corrected 2026-09-03.) A certificate whose false-clear rate exceeds the target it purports to guarantee is **vacuous** for that consumer, however confident it looks. FC is measurable wherever a witness exists, which — per the table — is nearly everywhere it matters.

## conditions

- A witness must exist. Where none exists the rate is not measurable and the certificate is unassessed, not safe.
- The rate is per consumer, given per read operator, slice, group, or footprint, never as one aggregate.
- Coverage is reported with it. A witnessed certificate clears fewer decisions than a naive one, and the two numbers are read together.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Certificate.lean`, theorems `falseClear_mul_coverage`, `coverage_empty`, `falseClear_mem_unit`, `minOverStrata_passes_iff`, `minOverStrata_le_weighted_mean`, at observation-data-mining 8d458b2.

## used in

*Data Mining as Observation* chapters 0, 12, 13, 14.

## related

certificate, witness, coverage, coherence-time, refresh-floor, min-over-strata

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 429cc9d, theory-radar 37c4e6c, observation-data-mining 8d458b2, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
