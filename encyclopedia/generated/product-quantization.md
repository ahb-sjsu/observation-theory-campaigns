# product quantization

**id.** product-quantization
**kind.** instrument

## definition

Splitting a vector into pieces and quantizing each piece with its own codebook. Chapter 11.

## equation

Book equation 11.3.

    \begin{gathered} \mathrm{recall}@k=\frac{\big|\text{returned top-}k\ \cap\ \text{true top-}k\big|}{k}, \\ \text{true top-}k\text{ computed from the uncompressed vectors}. \end{gathered}

Book equation 4.2.

    D(b)=\sum_i s_i\sigma_i^{2}\,2^{-2b_i},\qquad s_i=v_i^{\top}P_C\,v_i,\qquad b_i^{\star}=\max\!\Big(0,\ \tfrac12\log_2\frac{s_i\sigma_i^{2}}{\theta}\Big),\qquad \sum_i b_i^{\star}=B,

## ledger

- NEG-14. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe). `[refuted]`. `geometric-observation/claims/LEDGER.md:108` at 7d91883.

## first stated

Jégou, Douze, and Schmid, product quantization for nearest neighbor search, 2011, as chapter 11 section 11.3 of *Data Mining as Observation* presents it, with the program's comparisons in openvector-bench and turboquant-pro.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 10 section 10.4 | area map, boundary rule, hash, refuse not warn, intra and transit counts, area classes, abstention rule | `turboquant-pro\docs\STRATA_RFC.md:24-98` |
| chapter 10 section 10.4 | second prediction inverted, transit 0.389 vs 0.291, centrality difference signs, share 0.473 vs 0.391, seven of thirteen backbone | `turboquant-pro\docs\RESULTS_multilingual_strata.md:55-90`; `turboquant-pro\docs\STRATA_RFC.md:98-130` |

## failures and corrections

- NEG-14, `[refuted]`. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe).

## conditions

- Splitting a vector into pieces and quantizing each with its own codebook. The squared error of the whole is the sum of the pieces' errors, so the best code for the whole is the best code for each piece separately, and K entries per piece over M pieces address K to the M cells in M log₂ K bits.
- It is evaluated by recall at k per stratum and by the rank certificate, never by reconstruction error, and the anti-hub stratum is where it fails first.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ProductQuantization.lean`, theorems `sq_error_add`, `inf_add`, `bits_of_codebooks`, `table_row`, at observation-data-mining 81ea18c.

## used in

*Data Mining as Observation* chapters 0, 4, 8, 11, 13.

## related

recall-at-k, anti-hub, water-filling, rank-certificate

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 1aa8775, theory-radar 37c4e6c, observation-data-mining 81ea18c, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
