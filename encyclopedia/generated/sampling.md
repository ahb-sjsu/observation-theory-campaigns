# sampling

**id.** sampling
**kind.** instrument

## definition

Choosing which rows to read. The standard error of a sample mean falls as one over the square root of the sample size. Chapter 2 section 2.7.

## equation

Book equation 0.18.

    \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2},\qquad \frac{\widehat{\operatorname{Var}}_{\mathrm{NB}}}{\hat\sigma^{2}/J}=1+J\,\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}.

Book equation 8.2.

    \begin{gathered} \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2}, \\ J=1000,\ \frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}=\frac14\ \Rightarrow\ 1+250=251,\ \ \sqrt{251}=15.84. \end{gathered}

Book equation 2.1.

    P_{C_2\circ C_1}(x)=J_1(x)^{\top}\,P_{C_2}\big(C_1(x)\big)\,J_1(x),\qquad \operatorname{rank}P_{C_2\circ C_1}(x)\le\operatorname{rank}P_{C_2}\big(C_1(x)\big)\quad\text{at each row } x.

## ledger

- NEG-14. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe). `[refuted]`. `geometric-observation/claims/LEDGER.md:108` at 9f3829f.

## first stated

Chapter 2 section 2.7 of *Data Mining as Observation*, with the first strata run's sample in `turboquant-pro/docs/STRATA_RFC.md:24-98`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 4 section 4.7 | ESL 7.10.2 numbers | Hastie, Tibshirani, Friedman, ESL 2e, section 7.10.2; chapter 8 of this book |
| chapter 8 section 8.1 | ESL 7.10.2 numbers (N=50, p=5000, 100 selected, 3 percent vs 50 percent) | Hastie, Tibshirani, Friedman, ESL 2e, section 7.10.2 |
| chapter 10 section 10.4 | area map, boundary rule, hash, refuse not warn, intra and transit counts, area classes, abstention rule | `turboquant-pro\docs\STRATA_RFC.md:24-98` |
| chapter 10 section 10.4 | second prediction inverted, transit 0.389 vs 0.291, centrality difference signs, share 0.473 vs 0.391, seven of thirteen backbone | `turboquant-pro\docs\RESULTS_multilingual_strata.md:55-90`; `turboquant-pro\docs\STRATA_RFC.md:98-130` |

## failures and corrections

- NEG-14, `[refuted]`. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe).

## conditions

- Choosing which rows to read. A sample's mean lies between its smallest and largest row, the standard error of the mean falls as one over the square root of the sample size, and a sample too thin to score is abstained on rather than averaged in.
- Sampling and aggregation are design choices that decide what the reader can see, and the first strata run read 350000 of 2391361 rows and abstained on the strata with two rows and one.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/StandardError.lean`, theorems `se_pos`, `se_quarter`, `se_antitone`, `se_tendsto_zero`, `thousand_folds`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/Ensemble.lean`, theorems `average_between`, `sq_average_le`, `average_const`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14.

## related

standard-error, aggregation, bootstrap, seed, stratification

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
