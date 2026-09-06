# witness

**id.** witness
**kind.** concept

## definition

An independent measurement of whether a certificate's claim was true. Chapter 13.

## equation

Book equation 0.26.

    \mathrm{FC}=\Pr\big[W\ \text{refutes}\ \big|\ \mathcal C_t\ \text{clears}\big],\qquad \text{coverage}=\Pr\big[\mathcal C_t\ \text{clears}\big].

Book equation 13.1.

    \mathrm{FC}=\Pr\big[W\ \text{refutes}\ \big|\ \mathcal C_t\ \text{clears}\big],\qquad d_O(\Delta)=\operatorname{tr}\big(P_C\,M_{\mathrm{drift}}(\Delta)\big),\qquad M_{\mathrm{drift}}(\Delta)=\mathbb E\big[\delta_\Delta\delta_\Delta^{\top}\big].

## ledger

none

## first stated

Volume 14, chapter 19, `geometric-observation/chapters/ch19_the_certificate_that_ages.md:61-76`, and the freshness program's umbrella document `observation-theory-campaigns/experiments/FRESHNESS-PROGRAM.md`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 12 section 12.6 | XPROTO-LLM, benchmark 0.909, 0.920, 0.909, thirty slices, target 0.8, naive 0.333, aware 0.033, spread 0.380, deployment mean 0.736, six bars on three seeds, sealed 2026-08-25 at b61f7f1 | `observation-theory-campaigns\experiments\LLM-EVAL-TRACK.md:1-50`; `observation-theory-campaigns\analysis\llm\XPROTO-LLM-graded.json`; `observation-theory-campaigns\experiments\SEALS.md:85` |
| chapter 13 section 13.3 | ZooKeeper hot 0.99 cold 0.01 witnessed 0.0, Postgres 0.50 to 0.06, MongoDB 0.47 to 0.03, production Postgres 0.47 to 0.02, real substrates, disjoint seeds | `observation-theory-campaigns\experiments\DATABASE-FRESHNESS-TRACK.md:1-45` |
| chapter 13 section 13.3 | BGP 0.351, IS-IS 0.184, OSPF 0.083, second collector | `observation-theory-campaigns\analysis\mongo\PREREG-XPROTO-MG.md:42`; `observation-theory-campaigns\experiments\ROUTING-TELEMETRY-TRACK.md:130-150`; `geometric-observation\BOOK-OUTLINE.md:75` |
| chapter 13 section 13.3 | radio 0.27 to 0.42 naive to 0.055 to 0.13, neural reconstruction 0.28 to 0.13 | `observation-theory-campaigns\experiments\RADIO-FRESHNESS-TRACK.md:20-35` |
| chapter 13 section 13.4 | refuted fit 0.177 T_coh R² 0.915, 0.15 threshold vs 0.10 claim, fresh baseline 0.113, do not cite | `observation-theory-campaigns\analysis\csi\CSI-refreshfloor.json:2,111-114`; `observation-theory-campaigns\experiments\RADIO-FRESHNESS-TRACK.md:41-47` |

From `observation-theory-campaigns/experiments/DATABASE-FRESHNESS-TRACK.md` at 0c2e3f9.

- line 23. XPROTO-PG (analysis/pgrep) | Postgres, recovery_min_apply_delay | WAL LSN | ~0.50 → ~0.06
- line 24. XPROTO-MG (analysis/mongo) | MongoDB delayed secondary | oplog ts | ~0.47 → ~0.03
- line 25. XPROTO-PGX (analysis/pgx) | production PG, netem lag | WAL LSN, pg_stat_statements footprint | ~0.47 → ~0.02
- line 27. XPROTO-ZK (analysis/zk) | ZooKeeper 3.9 ensemble | zxid, sync() | hot 0.99 / cold 0.01, witnessed 0.0

From `observation-theory-campaigns/experiments/RADIO-FRESHNESS-TRACK.md` at 0c2e3f9.

- line 25. XPROTO-CSI (analysis/csi) | CQI → MCS | HARQ | 0.34–0.37 → 0.10 (OLLA) | ✅ 08-23
- line 26. XPROTO-BEAM (analysis/beam) | mmWave beam index | HARQ | 0.31 → 0.02 (BFR) | ✅ 08-23
- line 27. XPROTO-AICSI (analysis/aicsi) | neural-CSI recon (turboquant bridge) | precoder/HARQ | recon wins yet 0.28 → 0.13 | ✅ 08-23, scope-corrected 08-25 ⚠️
- line 28. XPROTO-HO (analysis/ho) | RSRP → serving cell | RLF | 0.31–0.44 → 0.09–0.12 | ✅ 08-23
- line 30. XPROTO-PHY (analysis/phy) | PMI / RI / TA | HARQ | 0.27–0.42 → 0.055–0.13 | ✅ 08-24

## failures and corrections

none

## conditions

- A witness is independent of the certificate it grades. A certificate that grades itself has no witness.
- The witness is the consumer's own outcome or a measurement of it, so the same certificate has a different witness for each consumer, as the hot and cold readers of one replica show.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Certificate.lean`, theorems `falseClear_mul_coverage`, `coverage_empty`, `falseClear_mem_unit`, `minOverStrata_passes_iff`, `minOverStrata_le_weighted_mean`, at observation-data-mining 17f3e9f.

## used in

*Data Mining as Observation* chapters 0, 12, 13, 14.

## related

certificate, false-clear-rate, coverage

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 01e53bc, observation-theory-campaigns 0c2e3f9, theory-radar 37c4e6c, observation-data-mining 17f3e9f, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
