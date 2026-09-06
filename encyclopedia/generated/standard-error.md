# standard error

**id.** standard-error
**kind.** concept

## definition

The spread of an estimate across repeated samples. Chapter 0 section 0.9.

## equation

Book equation 0.18.

    \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2},\qquad \frac{\widehat{\operatorname{Var}}_{\mathrm{NB}}}{\hat\sigma^{2}/J}=1+J\,\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}.

Book equation 8.2.

    \begin{gathered} \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2}, \\ J=1000,\ \frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}=\frac14\ \Rightarrow\ 1+250=251,\ \ \sqrt{251}=15.84. \end{gathered}

## ledger

none

## first stated

Chapter 0 section 0.9 of *Data Mining as Observation*, with the program's own inflation in `constraint-gap/review/FINDINGS.md:1-35`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 6 section 6.4 | the uncorrected t stored as sigma, 251 and 15.84, nine wins to three, seven, eight, 3 wins 17 ties 11 losses on 31 datasets, the three-way inconsistency | `constraint-gap\review\FINDINGS.md:1-35`; `constraint-gap\README.md:57-76` |
| chapter 8 section 8.5 | variance inflation 251, SE inflation 15.84, J_eff 3.98, about 62 needed, 3 of 9 at full, 7 at half, 8 at a third | `constraint-gap\review\FINDINGS.md:1-35` |

## failures and corrections

none

## conditions

- The spread of an estimate across repeated samples, the spread of one draw over the square root of the number of independent draws. It is positive, falls as the draws grow, halves only when the draws quadruple, and tends to zero.
- Dependent draws do not shrink it this way. A thousand repeated folds shrink the naive standard error by a factor near 31.6 and the corrected one by 15.84 less, which is the Nadeau and Bengio correction.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/StandardError.lean`, theorems `se_pos`, `se_quarter`, `se_antitone`, `se_tendsto_zero`, `thousand_folds`, at observation-data-mining 8d30d9d.

## used in

*Data Mining as Observation* chapters 0, 6, 7, 8, 13, 14.

## related

nadeau-and-bengio-correction, harness, multiple-comparisons, preregistration

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 425c17a, theory-radar 37c4e6c, observation-data-mining 8d30d9d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
