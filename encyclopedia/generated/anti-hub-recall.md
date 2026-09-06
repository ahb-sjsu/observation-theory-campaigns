# anti-hub recall

**id.** anti-hub-recall
**kind.** instrument

## definition

Recall at k restricted to the rows that are rarely retrieved, the observer's outliers, reported as the minimum over strata so that a mean cannot hide the tail. Chapter 10.

## equation

Book equation 10.7.

    \text{verdict}=\min_{i:\ n_i\ge n_{\min},\ |Q_i|\ge q_{\min}}\ \mathrm{score}_i,\qquad \text{ABSTAIN otherwise}.

Book equation 11.3.

    \begin{gathered} \mathrm{recall}@k=\frac{\big|\text{returned top-}k\ \cap\ \text{true top-}k\big|}{k}, \\ \text{true top-}k\text{ computed from the uncompressed vectors}. \end{gathered}

Book equation 0.35.

    \mathrm{RH}=\sum_i\max\!\Big(0,\ \frac{N_i}{\sum_j N_j}-\frac1n\Big).

## ledger

- NEG-14. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe). `[refuted]`. `geometric-observation/claims/LEDGER.md:108` at 9f3829f.

## first stated

Chapter 10 section 10.2 of *Data Mining as Observation*, with the program's gate in `turboquant-pro/docs/HUBNESS_PRIMER.md:86-131` and the strata result in `turboquant-pro/docs/RESULTS_strata_phase23_gates.md`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 10 section 10.2 | anti-hubs as where compressed indexes fail first, aggregate recall barely moves | `turboquant-pro\docs\HUBNESS_PRIMER.md:86-131` |
| chapter 10 section 10.4 | first run, 350000 of 2391361 rows, 7 of 14 eligible, abstentions with 2 and 1 rows, Robin Hood 0.3447 to 0.4469 ratio 1.30 against 1.5, skew 2.68 to 4.40 ratio 1.64 against 3, 63 times sample range | `turboquant-pro\docs\RESULTS_multilingual_strata.md:1-55` |
| chapter 10 section 10.4 | second prediction inverted, transit 0.389 vs 0.291, centrality difference signs, share 0.473 vs 0.391, seven of thirteen backbone | `turboquant-pro\docs\RESULTS_multilingual_strata.md:55-90`; `turboquant-pro\docs\STRATA_RFC.md:98-130` |
| chapter 10 section 10.5 | Gate A design error, A prime skew 3.970 to 3.177, max 287 to 213, Robin Hood 0.372 to 0.261, fraction 0.117 to 0.079, compressed path 0.663 vs 0.90, seven strata, 0.62 to 0.69 vs 0.76 to 0.84 | `turboquant-pro\docs\RESULTS_strata_phase23_gates.md:1-45` |
| chapter 10 section 10.5 | rerank identical 0.6627, candidate coverage, depth curve 51 to 501, coverage 0.696 to 0.926, fidelity 0.663 to 0.702, originals rerank 0.923, 4096 bytes on 148 | `turboquant-pro\docs\RESULTS_strata_phase23_gates.md:45-110` |
| chapter 10 section 10.5 | fragile-first allocation 0.7118 vs 0.7251, targets up 0.004 to 0.034, redesigned allocator passed | `turboquant-pro\docs\RESULTS_strata_phase23_gates.md:110-125` |
| chapter 11 section 11.6 | anti-hub recall, p05, hub-rank correlation, hub-set overlap, the build gate | `turboquant-pro\docs\HUBNESS_PRIMER.md:86-131` |
| chapter 12 section 12.4 | seven of thirteen backbone areas under the translation-trained encoder, all local-hub under the general one | `turboquant-pro\docs\RESULTS_multilingual_strata.md:55-90` |

## failures and corrections

- NEG-14, `[refuted]`. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe).

## conditions

- Recall at k restricted to the rows that are rarely retrieved, the observer's outliers, reported as the minimum over strata so that a mean cannot hide the tail. It lies in the unit interval and is one exactly when every anti-hub's true neighbours are returned.
- Compressed indexes fail on anti-hubs first while aggregate recall barely moves, and the remedy that promotes isolated rows is the remedy that compression damages first, which is why the gate is a build gate and not a report line.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/RecallAtK.lean`, theorems `recallAtK_mem_unit`, `recallAtK_eq_one_iff`, `aggregate_le_of_failing`, `aggregate_example`, at observation-data-mining f05f3e7.

`lean/DataMiningAsObservation/Hubness.lean`, theorems `sum_count`, `sum_count_eq`, `count_congr`, `antiHub_iff`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 10, 11, 12.

## related

anti-hub, recall-at-k, min-over-strata, hub, stratification

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
