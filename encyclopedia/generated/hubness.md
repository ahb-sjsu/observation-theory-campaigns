# hubness

**id.** hubness
**kind.** result

## definition

A row retrieved as a nearest neighbour far more often than chance allows. The book shows hubness is almost entirely a property of the queries and the reader, not of the corpus. Chapters 3 and 10.

## equation

Book equation 0.17.

    \Pr[X\ge c]=1-\sum_{i<c}e^{-\mu}\frac{\mu^{i}}{i!},\qquad c^{\star}=\max\{c:\ n\Pr[X\ge c]\ge 1\},\qquad \mu=\frac{n_q\,k}{n}.

Book equation 0.35.

    \mathrm{RH}=\sum_i\max\!\Big(0,\ \frac{N_i}{\sum_j N_j}-\frac1n\Big).

Book equation 10.3.

    N_k(x\mid Q)=\big|\{q\in Q:\ x\in\operatorname{top}_k(q)\}\big|,\qquad \text{anti-hub}:\ N_k(x)=0.

## ledger

- GO-5. An α=1 density/hubness quotient restores invariant fidelity in ≥1 non-spectral domain. `[refuted]`. `geometric-observation/claims/LEDGER.md:67` at 7d91883.
- NEG-15 (Bell boundary). *Query-conditioned hubness supplies a mechanism for Bell-inequality violation without action at a distance.* Refuted as a mechanism; the settings-as-queries reframing survives only as vocabulary. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:93` at 7d91883.
- NEG-11. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain. `[refuted]`. `geometric-observation/claims/LEDGER.md:104` at 7d91883.

## first stated

Radovanović, Nanopoulos, and Ivanović for the phenomenon. The observation program's reading, that hubness is almost entirely a property of the queries and the reader rather than the corpus, in openvector-bench and turboquant-pro, and in chapter 3 section 3.5 and chapter 10 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.6 | ball-growth heat a missing-mean artifact, eleven campaigns, 3 of 12 to 11 of 12 cells | `openvector-bench\README.md:160-170`; `openvector-bench\results\RC13_VERDICT.md:1-20` |
| chapter 3 section 3.5 | Poisson null, hub excess, budget parameter | `openvector-bench\openvector_bench\hubness.py:41-100` |
| chapter 3 section 3.5 | query mass best single feature at every K for all four responses, seven features add at most 20 percent, threshold 1.25 on three of four, zero of four, 1000 real queries, 1024 dimensions | `openvector-bench\results\R13_STAGE0_RESULT.md:40-50`; `openvector-bench\results\R13_STAGE1_RESULT.md:1-40` |
| chapter 3 section 3.6 | Bell audit, max S 2.00000 across 72 configurations, d 3 to 128, correlation negative 0.036, post-selected 2.7308, controls 2.748, 2.386, 3.174, seed 20260817, sealed at 6e825d8 | `geometric-observation\articles\2026-08-03-hubness-does-not-weaken-bell.md:1-60`; `geometric-observation\claims\LEDGER.md` row NEG-15; `geometric-observation\results\GO-bell-geometry-audit.json` |
| chapter 8 section 8.1 | G1 339.9 vs 71.9 same corpus, real about 61, rounds 1 to 4 at 300 to 420, three families falsified | `openvector-bench\results\QUERY_COUPLING_ARTIFACT.md:1-20` |
| chapter 8 section 8.4 | gate meta-rule, relative contrast discriminates nothing | `openvector-bench\openvector_bench\score_rc1.py:1-14`; `turboquant-pro\docs\RESEARCH_ROADMAP.md:133-160` |
| chapter 8 section 8.7 | RC-7 five of ten, band 0.076 vs 0.19, gate missed by 0.007, 2.4 times, eight-block rule | `openvector-bench\paper\profile\PROFILE_PAPER.md:576-598`; `openvector-bench\results\RC7_VERDICT.md` |
| chapter 10 section 10.2 | five kinds, balanced accuracy 0.611, 0.718, 0.684, the category table, per-category 0.57 to 0.82, the sweep, pigeonhole floor | `openvector-bench\results\R13_STAGE1_RESULT.md:40-75` |
| chapter 10 section 10.2 | half 2 failed, at most 1.28 times against 2, withdrawal and its scope | `openvector-bench\results\R13_STAGE1_RESULT.md:75-110` |
| chapter 10 section 10.4 | area map, boundary rule, hash, refuse not warn, intra and transit counts, area classes, abstention rule | `turboquant-pro\docs\STRATA_RFC.md:24-98` |
| chapter 10 section 10.4 | second prediction inverted, transit 0.389 vs 0.291, centrality difference signs, share 0.473 vs 0.391, seven of thirteen backbone | `turboquant-pro\docs\RESULTS_multilingual_strata.md:55-90`; `turboquant-pro\docs\STRATA_RFC.md:98-130` |
| chapter 11 section 11.4 | 0.999 against own ranking vs 0.592 against fp32 truth, three truth layers, difficulty strata | `openvector-bench\README.md:60-96` |
| chapter 11 section 11.4 | R80 table, 25x probe depth, 92 percent own cell, one third cross-article, 0.53 matches same-article share, relative contrast discriminates nothing | `openvector-bench\results\R80_ANN.md:1-40`; `turboquant-pro\docs\RESEARCH_ROADMAP.md:133-160` |
| chapter 11 section 11.6 | query mass best single feature at every K for all four responses, seven features add at most 20 percent at 12 leaves, threshold 1.25 on three of four, zero of four, 1000 real queries, 1024 dimensions | `openvector-bench\results\R13_STAGE0_RESULT.md:40-50`; `openvector-bench\results\R13_STAGE1_RESULT.md:1-40` |
| chapter 12 section 12.2 | recall 0.999 vs 0.592, the derived death point within 6 percent across fourteen corpora | `openvector-bench\README.md:60-96`; `geometric-observation\claims\LEDGER.md` row GO-3 |
| chapter 13 section 13.1 | one hundred billion vectors on a preemptible fleet, systems result not a tier, corpus rejected by the admission battery | `openvector-bench\README.md:250-263` |
| chapter 13 section 13.1 | twelve-figure corpus about 128 TB, kilobyte manifest | `openvector-bench\README.md:60-80` |

## failures and corrections

- GO-5, `[refuted]`. An α=1 density/hubness quotient restores invariant fidelity in ≥1 non-spectral domain.
- NEG-11, `[refuted]`. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain.

## conditions

- A hub is a row retrieved as a nearest neighbour far more often than the Poisson null allows, and the ceiling of that null is derived from the query count, the neighbourhood size, and the corpus size.
- Hubness is measured against a query workload and belongs to it. The two corpus-side mechanisms that were registered to explain it were refuted under seal.
- Anti-hubs come in kinds, and one kind is manufactured by the query budget through the pigeonhole floor, so a count of never-retrieved rows changes with the number of slots per row.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Hubness.lean`, theorems `sum_count`, `sum_count_eq`, `count_congr`, `antiHub_iff`, at observation-data-mining 7199131.

## used in

*Data Mining as Observation* chapters 0, 1, 3, 5, 10, 11, 12, 13.

## related

quotient, certificate, rank-certificate, min-over-strata

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns e062d3e, theory-radar 37c4e6c, observation-data-mining 7199131, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
