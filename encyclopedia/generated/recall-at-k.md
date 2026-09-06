# recall at k

**id.** recall-at-k
**kind.** concept

## definition

The fraction of a query's true k nearest neighbours that an index returned. Equation 11.3.

## equation

Book equation 11.3.

    \begin{gathered} \mathrm{recall}@k=\frac{\big|\text{returned top-}k\ \cap\ \text{true top-}k\big|}{k}, \\ \text{true top-}k\text{ computed from the uncompressed vectors}. \end{gathered}

Book equation 10.7.

    \text{verdict}=\min_{i:\ n_i\ge n_{\min},\ |Q_i|\ge q_{\min}}\ \mathrm{score}_i,\qquad \text{ABSTAIN otherwise}.

## ledger

- NEG-14. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe). `[refuted]`. `geometric-observation/claims/LEDGER.md:108` at 9f3829f.
- GO-B-Llama. Trained frontier LLM (Llama-3.2-3B), softmax-attention consumer — blind probe on real post-RoPE keys `[predicted]`. `geometric-observation/claims/LEDGER.md:115` at 9f3829f.
- GO-B-Llama-rematch. Trained frontier LLM (Llama-3.2-3B), softmax-attention consumer — recon-matched dissociation on real post-RoPE keys `[predicted]`. `geometric-observation/claims/LEDGER.md:118` at 9f3829f.

## first stated

Chapter 11 section 11.3 of *Data Mining as Observation*, with the program's stratified form in turboquant-pro, `turboquant-pro/docs/HUBNESS_PRIMER.md:86-131`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.5 | 78 vs 369, density correlation about 0.67, 8 percent vs 34 percent, centering vs mutual-proximity rescaling | `turboquant-pro\docs\HUBNESS_PRIMER.md:38-59,140-160` |
| chapter 10 section 10.2 | anti-hubs as where compressed indexes fail first, aggregate recall barely moves | `turboquant-pro\docs\HUBNESS_PRIMER.md:86-131` |
| chapter 10 section 10.3 | abstain below 2.5 k | `turboquant-pro\docs\HUBNESS_PRIMER.md:140-160` |
| chapter 11 section 11.6 | count of ten, hubs and anti-hubs, max 78 vs 369, density correlation about 0.67, 8 percent vs 34 percent, abstain below 2.5k, centering vs mutual-proximity rescaling | `turboquant-pro\docs\HUBNESS_PRIMER.md:1-60,60-170` |
| chapter 11 section 11.6 | anti-hub recall, p05, hub-rank correlation, hub-set overlap, the build gate | `turboquant-pro\docs\HUBNESS_PRIMER.md:86-131` |
| chapter 11 section 11.6 | the centroid-injection attack | `turboquant-pro\docs\HUBNESS_PRIMER.md:168-197`, citing arXiv 2604.05480 |

## failures and corrections

- NEG-14, `[refuted]`. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe).

## conditions

- The fraction of a query's true k nearest neighbours, computed from the uncompressed vectors, that the index returned. It lies in the unit interval and is one exactly when the returned list is the true list.
- The aggregate over queries is a weighted mean over strata, so a stratum that fails entirely moves it by no more than its weight. That is why the anti-hub stratum is reported on its own, and why aggregate recall is never an acceptance metric on its own.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/RecallAtK.lean`, theorems `recallAtK_mem_unit`, `recallAtK_eq_one_iff`, `aggregate_le_of_failing`, `aggregate_example`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 10, 11, 12.

## related

anti-hub, min-over-strata, rank-certificate, hubness

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
