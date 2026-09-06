# bootstrap

**id.** bootstrap
**kind.** instrument

## definition

An estimate of a confidence interval made by resampling the data with replacement many times and recomputing the statistic each time. A paired bootstrap resamples the same rows for two methods at once so that shared sampling variation cancels. Chapter 0 section 0.9.

## equation

Book equation 8.2.

    \begin{gathered} \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2}, \\ J=1000,\ \frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}=\frac14\ \Rightarrow\ 1+250=251,\ \ \sqrt{251}=15.84. \end{gathered}

Book equation 0.18.

    \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2},\qquad \frac{\widehat{\operatorname{Var}}_{\mathrm{NB}}}{\hat\sigma^{2}/J}=1+J\,\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}.

## ledger

none

## first stated

Efron, bootstrap methods, 1979, as chapter 0 section 0.9 states it, with the program's paired form in the flip comparisons of Volume 14 and the constraint-gap review.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 6 section 6.4 | the uncorrected t stored as sigma, 251 and 15.84, nine wins to three, seven, eight, 3 wins 17 ties 11 losses on 31 datasets, the three-way inconsistency | `constraint-gap\review\FINDINGS.md:1-35`; `constraint-gap\README.md:57-76` |
| chapter 8 section 8.5 | variance inflation 251, SE inflation 15.84, J_eff 3.98, about 62 needed, 3 of 9 at full, 7 at half, 8 at a third | `constraint-gap\review\FINDINGS.md:1-35` |

## failures and corrections

none

## conditions

- An interval estimated by resampling the data with replacement and recomputing the statistic each time. A paired bootstrap resamples the same rows for two methods at once, and the variance of the difference is the sum of the two variances minus twice their covariance, so pairing narrows the interval exactly when the two scores covary positively across rows.
- Resampling rows does not undo dependence between folds, which is the correction's job, and the bootstrap's interval is only as wide as the sample it resamples.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Bootstrap.lean`, theorems `mean_sub`, `var_sub`, `paired_lt_iff`, `cov_comm`, at observation-data-mining 1c6cd64.

## used in

*Data Mining as Observation* chapters 0, 6, 7, 11, 12, 14.

## related

confidence-interval, standard-error, nadeau-and-bengio-correction, harness

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 09cc919, theory-radar 37c4e6c, observation-data-mining 1c6cd64, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
