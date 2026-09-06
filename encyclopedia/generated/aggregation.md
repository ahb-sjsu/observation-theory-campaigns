# aggregation

**id.** aggregation
**kind.** concept

## definition

Combining rows or groups into one number. An average lies between its members, and an aggregate over strata can pass a bar that one stratum fails and can reverse the sign every group shows. Chapter 2 section 2.7 and chapter 10 section 10.4.

## equation

Book equation 10.7.

    \text{verdict}=\min_{i:\ n_i\ge n_{\min},\ |Q_i|\ge q_{\min}}\ \mathrm{score}_i,\qquad \text{ABSTAIN otherwise}.

Book equation 14.5.

    \mathrm{FC}_g=\Pr\big[y=\text{violation}\ \big|\ \hat y=\text{clear},\ g\big],\qquad \text{verdict}=\max_{g:\ n_g\ge n_{\min}}\mathrm{FC}_g,\qquad \text{ABSTAIN otherwise}.

Book equation 8.2.

    \begin{gathered} \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2}, \\ J=1000,\ \frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}=\frac14\ \Rightarrow\ 1+250=251,\ \ \sqrt{251}=15.84. \end{gathered}

## ledger

- NEG-14. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe). `[refuted]`. `geometric-observation/claims/LEDGER.md:108` at 9f3829f.
- GO-B-Llama. Trained frontier LLM (Llama-3.2-3B), softmax-attention consumer — blind probe on real post-RoPE keys `[predicted]`. `geometric-observation/claims/LEDGER.md:115` at 9f3829f.
- GO-B-Llama-rematch. Trained frontier LLM (Llama-3.2-3B), softmax-attention consumer — recon-matched dissociation on real post-RoPE keys `[predicted]`. `geometric-observation/claims/LEDGER.md:118` at 9f3829f.

## first stated

Chapter 2 section 2.7 and chapter 10 section 10.4 of *Data Mining as Observation*, with the aggregate staleness rate of chapter 13 section 13.3.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.7 | the aggregate staleness rate describing neither reader | chapter 13 of this book, section 13.3 |
| chapter 10 section 10.2 | anti-hubs as where compressed indexes fail first, aggregate recall barely moves | `turboquant-pro\docs\HUBNESS_PRIMER.md:86-131` |
| chapter 10 section 10.4 | area map, boundary rule, hash, refuse not warn, intra and transit counts, area classes, abstention rule | `turboquant-pro\docs\STRATA_RFC.md:24-98` |
| chapter 10 section 10.4 | second prediction inverted, transit 0.389 vs 0.291, centrality difference signs, share 0.473 vs 0.391, seven of thirteen backbone | `turboquant-pro\docs\RESULTS_multilingual_strata.md:55-90`; `turboquant-pro\docs\STRATA_RFC.md:98-130` |
| chapter 11 section 11.6 | anti-hub recall, p05, hub-rank correlation, hub-set overlap, the build gate | `turboquant-pro\docs\HUBNESS_PRIMER.md:86-131` |

## failures and corrections

- NEG-14, `[refuted]`. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe).

## conditions

- Combining rows or groups into one number, a mean, a sum, or a rate. An average lies between the smallest and largest member, a weighted aggregate over strata can pass a bar while one stratum fails it, and an aggregate can reverse the sign every group shows.
- Aggregate recall barely moves while anti-hubs fail, the aggregate staleness rate describes neither reader, and the report takes the worst group and counts the groups too thin to score.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Ensemble.lean`, theorems `average_between`, `sq_average_le`, `average_const`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/Simpson.lean`, theorems `pooled_eq_weighted`, `reversal`, `no_reversal_of_equal_sizes`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/RecallAtK.lean`, theorems `recallAtK_mem_unit`, `recallAtK_eq_one_iff`, `aggregate_le_of_failing`, `aggregate_example`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 2, 5, 8, 10, 11, 12, 13.

## related

min-over-strata, simpsons-paradox, stratification, anti-hub-recall, sampling

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
