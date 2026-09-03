# OT empirical validation map — kernels × public datasets

Maintained registry (started 2026-09-02). The rigor lives in the machinery,
not the data: every entry gets the same pipeline (shakedown with pre-stated
predictions → prereg with the V2 instrument: cross-fit qualification,
single-domain units, matched-null arms, honest constants, seed discipline →
seal → graded as executed). A dataset earns a row only if a sealed bar could
run on it.

## Kernel 1 — consumer-relative dissociation (gain iff decodable + misaligned)

| dataset | consumers | status / note |
|---|---|---|
| 20NG + MiniLM, Social-Chem + LaBSE | topic/length/valence/foundations probes | DONE (construction + V1 FAIL + V2 drafted) |
| xbse per-axis corpora | validated-axis distilled probes | V2 confirmatory pool (seals 09-03) |
| BEIR / MS MARCO | retrieval → QA consumers | natural CR-ANN expansion; thick prior art (rerankers), delineate hard |
| MovieLens / Amazon reviews | rating vs genre vs helpfulness readers | cheap; recommender misalignment is natural |

## Kernel 2 — no observer-independent faithfulness (OT-UMAP)

| dataset | consumers | status / note |
|---|---|---|
| 20NG MiniLM | topic / length / pc200 | DONE (inversion core held, 7a5b7f7) |
| **single-cell RNA-seq (Tabula Sapiens, 10x PBMC)** | marker-gene panels vs cell-type classifiers vs trajectory readers | **TOP PICK**: lands inside a live controversy (Chari–Pachter, "specious art of single-cell genomics") with superb public data; the inversion claim says both sides of that fight are right, for different consumers — a result the field is primed to receive |
| CLIP / ImageNet embeddings | attribute vs class vs caption readers | visual twin, easy |

## Kernel 3 — freshness / refresh-floor laws (flip onset, L* ~ (d/σ)²)

| dataset | consumers | status / note |
|---|---|---|
| Binance bulk ticks | threshold monitors at d bps | RUNNING tonight (4cf6dd7) |
| RIPE RIS/Atlas | quiescence certificates | D8 family (V1b collecting) |
| **space-track TLEs / public ephemerides** | conjunction screeners at different miss-distance thresholds | **TOP PICK**: catastrophic-threshold consumers, genuinely first-passage dynamics, unusual venue (AMOS/JSR), staleness incidents documented (stale TLE → bad screening) |
| GTFS-realtime transit feeds | headway/transfer decisions | cheap, charming, public |
| CAISO/ERCOT OASIS LMP feeds | dispatch/curtailment thresholds | bridges to EC-grid |
| USGS earthquake feeds | early-warning thresholds | seconds-scale; overlaps kernel 4 |

## Kernel 4 — value of observation (rank-one identity, sensor value)

| dataset | consumers | status / note |
|---|---|---|
| case39/case118 (pandapower) | thermal/interface/contingency | DONE shakedown (all 5 pass); AC false-clear next |
| **USGS stream gauges + NWS flood stages** | flood-warning thresholds per gauge basin | **TOP PICK**: the false-clear endpoint is a *warning missed*; gauge networks are being defunded, so "which gauge is worth keeping, for whom" is a live policy question with public data |
| NOAA ISD weather stations | forecast consumers (frost/aviation/fire) | same shape; reanalysis gives truth |
| PurpleAir/EPA AQ sensors | health-alert thresholds | dense network, cheap |
| seismic station networks (IRIS) | magnitude vs early-warning readers | placement literature exists; delineate |

## Kernel 5 — monitor false-clears in the consumer metric (CR-I-EIP shape)

| dataset | consumers | status / note |
|---|---|---|
| HF model zoo (Qwen/TinyLlama/…) | patch-response reads | prereg drafted, seals 09-03 |
| vision models + corruption benchmarks | robustness monitors | second modality when the LM family is sealed |

## Kernel 6 — deontic geometry (Hohfeld)

| dataset | consumers | status / note |
|---|---|---|
| Social-Chem / ETHICS / MFRC | foundations, valence | DONE (quarter-turn NOT FOUND; V4 stands) |
| CourtListener / ECHR judgment corpora | rights-position readers | natural jural text — exactly what the quarter-turn paper names as the stronger instrument; owner's home domain |

## Standing discipline

- Sweep before build in mined domains (finance rule); build-then-sweep is
  tolerable only where the domain literature is thin.
- Zero live exposure anywhere; public/historical data only.
- Every campaign inherits the CR-ANN post-mortem instrument fixes.
- One campaign in flight per kernel at a time; the seals queue is the
  bottleneck, not the data.
