# seed

**id.** seed
**kind.** concept

## definition

The number that fixes a run's randomness, so that two runs with the same seed are one run and only runs with different seeds measure variance. Chapter 8.

## equation

Book equation 0.18.

    \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2},\qquad \frac{\widehat{\operatorname{Var}}_{\mathrm{NB}}}{\hat\sigma^{2}/J}=1+J\,\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}.

Book equation 8.2.

    \begin{gathered} \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2}, \\ J=1000,\ \frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}=\frac14\ \Rightarrow\ 1+250=251,\ \ \sqrt{251}=15.84. \end{gathered}

Book equation 8.1.

    O_{\mathrm{harness}}=\big(C_{\mathrm{score}},\ G_{\mathrm{metric}},\ B=\text{folds}\times\text{samples}\times\text{seeds}\big).

## ledger

- NEG-14. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe). `[refuted]`. `geometric-observation/claims/LEDGER.md:108` at 9f3829f.

## first stated

Chapter 8 section 8.1 of *Data Mining as Observation*, with the disjoint-seed rule of the database freshness track in `observation-theory-campaigns/experiments/DATABASE-FRESHNESS-TRACK.md`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 4 section 4.4 | GO-4 budget inversion, fixed m 10 rises, matched m 121, 126, 159 collapses, 3 seeds | `geometric-observation\claims\LEDGER.md` row GO-4 |
| chapter 13 section 13.3 | ZooKeeper hot 0.99 cold 0.01 witnessed 0.0, Postgres 0.50 to 0.06, MongoDB 0.47 to 0.03, production Postgres 0.47 to 0.02, real substrates, disjoint seeds | `observation-theory-campaigns\experiments\DATABASE-FRESHNESS-TRACK.md:1-45` |

## failures and corrections

- NEG-14, `[refuted]`. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe).

## conditions

- The number that fixes a run's randomness, so that two runs with the same seed are one run and only runs with different seeds measure variance. The standard error over n seeds falls as one over the square root of n, and a paired comparison across seeds has smaller variance than an unpaired one exactly when the two arms covary.
- A preregistration names its seeds before the run, the freshness tracks used disjoint seeds for the two arms, and a claim replicated on one seed is replicated once.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/StandardError.lean`, theorems `se_pos`, `se_quarter`, `se_antitone`, `se_tendsto_zero`, `thousand_folds`, at observation-data-mining 5bb2c0d.

`lean/DataMiningAsObservation/Bootstrap.lean`, theorems `mean_sub`, `var_sub`, `paired_lt_iff`, `cov_comm`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 4, 6, 7, 8, 9, 11, 12, 13.

## related

harness, standard-error, bootstrap, preregistration, sealed

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
