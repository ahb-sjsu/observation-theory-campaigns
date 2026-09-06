# ensemble

**id.** ensemble
**kind.** instrument

## definition

A scorer that averages or votes several scorers. Its average lies between its members and its squared error is at most their mean squared error. Chapter 7.

## equation

Book equation 6.1.

    s(x)=w\cdot x+b,\qquad P_C=\mathbb E\big[\sigma'(s)^{2}\big]\,w\,w^{\top},\qquad \operatorname{rank}P_C=1.

Book equation 0.18.

    \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2},\qquad \frac{\widehat{\operatorname{Var}}_{\mathrm{NB}}}{\hat\sigma^{2}/J}=1+J\,\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}.

Book equation 8.2.

    \begin{gathered} \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2}, \\ J=1000,\ \frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}=\frac14\ \Rightarrow\ 1+250=251,\ \ \sqrt{251}=15.84. \end{gathered}

## ledger

none

## first stated

Breiman, bagging predictors, 1996, as chapter 7 section 7.1 of *Data Mining as Observation* reads it, with the fair comparison in `constraint-gap/review/INDETERMINATES.md:1-40`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 6 section 6.3 | the five-dataset table, breast cancer 0.955 to 0.963, the pattern, DOI 10.5281/zenodo.20660206 | `theory-radar\README.md:100-140` |
| chapter 7 section 7.1 | bagging variance, out-of-bag estimation, random forests, importances, AdaBoost | Hastie, Tibshirani, Friedman, ESL 2e chapters 15 and 10.1; TSK 2e 4.10 |
| chapter 7 section 7.3 | the five-dataset outcomes | `theory-radar\README.md:100-140` |
| chapter 7 section 7.4 | nine to three, seventeen indeterminate, five analyses zero resolved, three re-encode the correction | `constraint-gap\review\INDETERMINATES.md:1-40` |

## failures and corrections

none

## conditions

- A scorer that averages or votes several scorers. Its average lies between the smallest and the largest member, its squared error is at most the mean of the members' squared errors, and a constant ensemble is its constant. That arithmetic is why bagging reduces variance.
- Whether an ensemble beats a formula is a measured question and not a principle, and the comparison is fair only inside one fold protocol with the Nadeau and Bengio correction applied, where nine wins to three became three wins, seventeen ties, and eleven losses.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Ensemble.lean`, theorems `average_between`, `sq_average_le`, `average_const`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 0, 6, 7.

## related

boosting, decision-tree, formula-classifier, standard-error, nadeau-and-bengio-correction

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
