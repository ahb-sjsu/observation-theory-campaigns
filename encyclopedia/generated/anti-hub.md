# anti-hub

**id.** anti-hub
**kind.** concept

## definition

A row that is never or almost never retrieved as anyone's nearest neighbour. Chapter 10 names five kinds and shows one is manufactured by the query budget. Chapters 3 and 10.

## equation

Book equation 10.3.

    N_k(x\mid Q)=\big|\{q\in Q:\ x\in\operatorname{top}_k(q)\}\big|,\qquad \text{anti-hub}:\ N_k(x)=0.

Book equation 10.7.

    \text{verdict}=\min_{i:\ n_i\ge n_{\min},\ |Q_i|\ge q_{\min}}\ \mathrm{score}_i,\qquad \text{ABSTAIN otherwise}.

## ledger

- NEG-11. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain. `[refuted]`. `geometric-observation/claims/LEDGER.md:104` at 7d91883.
- NEG-14. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe). `[refuted]`. `geometric-observation/claims/LEDGER.md:108` at 7d91883.

## first stated

Radovanović, Nanopoulos, and Ivanović, hubs in space, 2010, as chapter 3 cites it, with the program's five kinds in turboquant-pro, `turboquant-pro/docs/HUBNESS_PRIMER.md:86-131`, and chapter 10 section 10.2 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.5 | 78 vs 369, density correlation about 0.67, 8 percent vs 34 percent, centering vs mutual-proximity rescaling | `turboquant-pro\docs\HUBNESS_PRIMER.md:38-59,140-160` |
| chapter 8 section 8.10 | the AI-assistant boundary, fresh-context passes | `geometric-observation\chapters\ch15_registration_first.md`; `geometric-observation\chapters\ch17_open_problems_and_the_keystone_theorem.md:85-96` |
| chapter 10 section 10.2 | anti-hubs as where compressed indexes fail first, aggregate recall barely moves | `turboquant-pro\docs\HUBNESS_PRIMER.md:86-131` |
| chapter 10 section 10.3 | abstain below 2.5 k | `turboquant-pro\docs\HUBNESS_PRIMER.md:140-160` |
| chapter 10 section 10.4 | area map, boundary rule, hash, refuse not warn, intra and transit counts, area classes, abstention rule | `turboquant-pro\docs\STRATA_RFC.md:24-98` |
| chapter 10 section 10.4 | first run, 350000 of 2391361 rows, 7 of 14 eligible, abstentions with 2 and 1 rows, Robin Hood 0.3447 to 0.4469 ratio 1.30 against 1.5, skew 2.68 to 4.40 ratio 1.64 against 3, 63 times sample range | `turboquant-pro\docs\RESULTS_multilingual_strata.md:1-55` |
| chapter 10 section 10.4 | second prediction inverted, transit 0.389 vs 0.291, centrality difference signs, share 0.473 vs 0.391, seven of thirteen backbone | `turboquant-pro\docs\RESULTS_multilingual_strata.md:55-90`; `turboquant-pro\docs\STRATA_RFC.md:98-130` |
| chapter 10 section 10.5 | Gate A design error, A prime skew 3.970 to 3.177, max 287 to 213, Robin Hood 0.372 to 0.261, fraction 0.117 to 0.079, compressed path 0.663 vs 0.90, seven strata, 0.62 to 0.69 vs 0.76 to 0.84 | `turboquant-pro\docs\RESULTS_strata_phase23_gates.md:1-45` |
| chapter 10 section 10.5 | rerank identical 0.6627, candidate coverage, depth curve 51 to 501, coverage 0.696 to 0.926, fidelity 0.663 to 0.702, originals rerank 0.923, 4096 bytes on 148 | `turboquant-pro\docs\RESULTS_strata_phase23_gates.md:45-110` |
| chapter 10 section 10.5 | fragile-first allocation 0.7118 vs 0.7251, targets up 0.004 to 0.034, redesigned allocator passed | `turboquant-pro\docs\RESULTS_strata_phase23_gates.md:110-125` |
| chapter 11 section 11.6 | count of ten, hubs and anti-hubs, max 78 vs 369, density correlation about 0.67, 8 percent vs 34 percent, abstain below 2.5k, centering vs mutual-proximity rescaling | `turboquant-pro\docs\HUBNESS_PRIMER.md:1-60,60-170` |
| chapter 11 section 11.6 | anti-hub recall, p05, hub-rank correlation, hub-set overlap, the build gate | `turboquant-pro\docs\HUBNESS_PRIMER.md:86-131` |
| chapter 11 section 11.6 | the centroid-injection attack | `turboquant-pro\docs\HUBNESS_PRIMER.md:168-197`, citing arXiv 2604.05480 |
| chapter 12 section 12.4 | seven of thirteen backbone areas under the translation-trained encoder, all local-hub under the general one | `turboquant-pro\docs\RESULTS_multilingual_strata.md:55-90` |

## failures and corrections

- NEG-11, `[refuted]`. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain.
- NEG-14, `[refuted]`. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe).

## conditions

- An anti-hub is a row no query retrieves, and chapter 10 names five kinds, of which one is manufactured by the query budget rather than by the corpus.
- Anti-hubs are where compressed indexes fail first, since quantization rounds away the fine distinctions by which they are found, while aggregate recall barely moves, which is why recall is reported per stratum with the anti-hub stratum named.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Hubness.lean`, theorems `sum_count`, `sum_count_eq`, `count_congr`, `antiHub_iff`, at observation-data-mining 8d30d9d.

## used in

*Data Mining as Observation* chapters 3, 10, 11, 12.

## related

hubness, poisson-ceiling, min-over-strata, rank-certificate

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 425c17a, theory-radar 37c4e6c, observation-data-mining 8d30d9d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
