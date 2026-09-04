# min-over-strata

**id.** min-over-strata
**kind.** concept

## definition

The rule that a verdict over several groups is the worst group's verdict, with abstention counted as a verdict, never the average. Chapter 10.

## equation

Book equation 10.7.

    \text{verdict}=\min_{i:\ n_i\ge n_{\min},\ |Q_i|\ge q_{\min}}\ \mathrm{score}_i,\qquad \text{ABSTAIN otherwise}.

Book equation 14.5.

    \mathrm{FC}_g=\Pr\big[y=\text{violation}\ \big|\ \hat y=\text{clear},\ g\big],\qquad \text{verdict}=\max_{g:\ n_g\ge n_{\min}}\mathrm{FC}_g,\qquad \text{ABSTAIN otherwise}.

## ledger

- NEG-14. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe). `[refuted]`. `geometric-observation/claims/LEDGER.md:108` at 7d91883.

## first stated

The compression program's stratified evaluation, STRATA, in turboquant-pro, DOI 10.5281/zenodo.20660087, and chapter 10 section 10.4 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.6 | ball-growth heat a missing-mean artifact, eleven campaigns, 3 of 12 to 11 of 12 cells | `openvector-bench\README.md:160-170`; `openvector-bench\results\RC13_VERDICT.md:1-20` |
| chapter 3 section 3.5 | Poisson null, hub excess, budget parameter | `openvector-bench\openvector_bench\hubness.py:41-100` |
| chapter 3 section 3.5 | query mass best single feature at every K for all four responses, seven features add at most 20 percent, threshold 1.25 on three of four, zero of four, 1000 real queries, 1024 dimensions | `openvector-bench\results\R13_STAGE0_RESULT.md:40-50`; `openvector-bench\results\R13_STAGE1_RESULT.md:1-40` |
| chapter 8 section 8.1 | G1 339.9 vs 71.9 same corpus, real about 61, rounds 1 to 4 at 300 to 420, three families falsified | `openvector-bench\results\QUERY_COUPLING_ARTIFACT.md:1-20` |
| chapter 8 section 8.4 | gate meta-rule, relative contrast discriminates nothing | `openvector-bench\openvector_bench\score_rc1.py:1-14`; `turboquant-pro\docs\RESEARCH_ROADMAP.md:133-160` |
| chapter 8 section 8.7 | RC-7 five of ten, band 0.076 vs 0.19, gate missed by 0.007, 2.4 times, eight-block rule | `openvector-bench\paper\profile\PROFILE_PAPER.md:576-598`; `openvector-bench\results\RC7_VERDICT.md` |
| chapter 8 section 8.10 | the AI-assistant boundary, fresh-context passes | `geometric-observation\chapters\ch15_registration_first.md`; `geometric-observation\chapters\ch17_open_problems_and_the_keystone_theorem.md:85-96` |
| chapter 10 section 10.2 | five kinds, balanced accuracy 0.611, 0.718, 0.684, the category table, per-category 0.57 to 0.82, the sweep, pigeonhole floor | `openvector-bench\results\R13_STAGE1_RESULT.md:40-75` |
| chapter 10 section 10.2 | half 2 failed, at most 1.28 times against 2, withdrawal and its scope | `openvector-bench\results\R13_STAGE1_RESULT.md:75-110` |
| chapter 10 section 10.4 | area map, boundary rule, hash, refuse not warn, intra and transit counts, area classes, abstention rule | `turboquant-pro\docs\STRATA_RFC.md:24-98` |
| chapter 10 section 10.4 | first run, 350000 of 2391361 rows, 7 of 14 eligible, abstentions with 2 and 1 rows, Robin Hood 0.3447 to 0.4469 ratio 1.30 against 1.5, skew 2.68 to 4.40 ratio 1.64 against 3, 63 times sample range | `turboquant-pro\docs\RESULTS_multilingual_strata.md:1-55` |
| chapter 10 section 10.4 | second prediction inverted, transit 0.389 vs 0.291, centrality difference signs, share 0.473 vs 0.391, seven of thirteen backbone | `turboquant-pro\docs\RESULTS_multilingual_strata.md:55-90`; `turboquant-pro\docs\STRATA_RFC.md:98-130` |
| chapter 10 section 10.5 | Gate A design error, A prime skew 3.970 to 3.177, max 287 to 213, Robin Hood 0.372 to 0.261, fraction 0.117 to 0.079, compressed path 0.663 vs 0.90, seven strata, 0.62 to 0.69 vs 0.76 to 0.84 | `turboquant-pro\docs\RESULTS_strata_phase23_gates.md:1-45` |
| chapter 10 section 10.5 | rerank identical 0.6627, candidate coverage, depth curve 51 to 501, coverage 0.696 to 0.926, fidelity 0.663 to 0.702, originals rerank 0.923, 4096 bytes on 148 | `turboquant-pro\docs\RESULTS_strata_phase23_gates.md:45-110` |
| chapter 10 section 10.5 | fragile-first allocation 0.7118 vs 0.7251, targets up 0.004 to 0.034, redesigned allocator passed | `turboquant-pro\docs\RESULTS_strata_phase23_gates.md:110-125` |
| chapter 11 section 11.4 | 0.999 against own ranking vs 0.592 against fp32 truth, three truth layers, difficulty strata | `openvector-bench\README.md:60-96` |
| chapter 11 section 11.4 | R80 table, 25x probe depth, 92 percent own cell, one third cross-article, 0.53 matches same-article share, relative contrast discriminates nothing | `openvector-bench\results\R80_ANN.md:1-40`; `turboquant-pro\docs\RESEARCH_ROADMAP.md:133-160` |
| chapter 11 section 11.6 | query mass best single feature at every K for all four responses, seven features add at most 20 percent at 12 leaves, threshold 1.25 on three of four, zero of four, 1000 real queries, 1024 dimensions | `openvector-bench\results\R13_STAGE0_RESULT.md:40-50`; `openvector-bench\results\R13_STAGE1_RESULT.md:1-40` |
| chapter 12 section 12.2 | recall 0.999 vs 0.592, the derived death point within 6 percent across fourteen corpora | `openvector-bench\README.md:60-96`; `geometric-observation\claims\LEDGER.md` row GO-3 |
| chapter 12 section 12.4 | seven of thirteen backbone areas under the translation-trained encoder, all local-hub under the general one | `turboquant-pro\docs\RESULTS_multilingual_strata.md:55-90` |
| chapter 13 section 13.1 | one hundred billion vectors on a preemptible fleet, systems result not a tier, corpus rejected by the admission battery | `openvector-bench\README.md:250-263` |
| chapter 13 section 13.1 | twelve-figure corpus about 128 TB, kilobyte manifest | `openvector-bench\README.md:60-80` |

## failures and corrections

- NEG-14, `[refuted]`. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe).

## conditions

- A verdict over several groups is the worst group's verdict, with a group too small to score counted as an abstention and reported, never averaged away.
- The first stratified run made two wrong predictions, and the record carries them at the size of the result.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

none

## used in

*Data Mining as Observation* chapters 0, 10, 11, 14.

## related

false-clear-rate, coverage, hubness, certificate

## status

Generated 2026-09-03 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 140daf2, theory-radar 37c4e6c, observation-data-mining 64c1765, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
