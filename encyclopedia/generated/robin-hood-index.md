# Robin Hood index

**id.** robin-hood-index
**kind.** instrument

## definition

The fraction of a total count that would have to move from points above the mean to points below it to make every count equal. Equation 0.35.

## equation

Book equation 0.35.

    \mathrm{RH}=\sum_i\max\!\Big(0,\ \frac{N_i}{\sum_j N_j}-\frac1n\Big).

Book equation 10.4.

    \text{never retrieved}\ \ge\ 1-\frac{|Q|\,k}{n}\qquad\text{whenever}\quad |Q|\,k<n.

## ledger

- NEG-14. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe). `[refuted]`. `geometric-observation/claims/LEDGER.md:108` at 7d91883.

## first stated

Hoover's index of concentration, applied to neighbour counts in turboquant-pro's strata design, `turboquant-pro/docs/STRATA_RFC.md:24-98`, and chapter 0 section 0.16 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 10 section 10.4 | area map, boundary rule, hash, refuse not warn, intra and transit counts, area classes, abstention rule | `turboquant-pro\docs\STRATA_RFC.md:24-98` |
| chapter 10 section 10.4 | second prediction inverted, transit 0.389 vs 0.291, centrality difference signs, share 0.473 vs 0.391, seven of thirteen backbone | `turboquant-pro\docs\RESULTS_multilingual_strata.md:55-90`; `turboquant-pro\docs\STRATA_RFC.md:98-130` |

## failures and corrections

- NEG-14, `[refuted]`. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe).

## conditions

- The fraction of the total count that would have to move from points above the mean to points below it to make every count equal, the excess above the mean over the total, which is half the total absolute deviation over the total. It is nonnegative, zero exactly at equality, at most one, and unchanged by a common scaling of the counts.
- The strata design reports it per area beside the skew, and the first run's ratio of 1.30 against a bar of 1.5 is the number the abstention rule was written around.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/RobinHood.lean`, theorems `sum_dev`, `excess_eq_half_abs`, `robinHood_nonneg`, `robinHood_eq_zero_iff`, `robinHood_le_one`, `robinHood_scale`, at observation-data-mining 43ea852.

## used in

*Data Mining as Observation* chapters 0, 10.

## related

hubness, anti-hub, poisson-ceiling, abstention

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 97b2015, theory-radar 37c4e6c, observation-data-mining 43ea852, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
