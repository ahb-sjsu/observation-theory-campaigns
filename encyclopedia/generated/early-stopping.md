# early stopping

**id.** early-stopping
**kind.** instrument

## definition

Halting a boosting run when a held-out score stops improving. The rule reads the held-out fold, so it is a harness and the round count is a fitted parameter. Chapter 7 section 7.5.

## equation

Book equation 8.1.

    O_{\mathrm{harness}}=\big(C_{\mathrm{score}},\ G_{\mathrm{metric}},\ B=\text{folds}\times\text{samples}\times\text{seeds}\big).

Book equation 8.2.

    \begin{gathered} \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2}, \\ J=1000,\ \frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}=\frac14\ \Rightarrow\ 1+250=251,\ \ \sqrt{251}=15.84. \end{gathered}

## ledger

- NEG-4. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL. `[refuted]`. `geometric-observation/claims/LEDGER.md:97` at 9f3829f.

## first stated

Chapter 7 section 7.5 of *Data Mining as Observation*, after ESL 10.12.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 6 section 6.4 | the reviewer's revision plan, drop sigma, bounded claim, 19 at 200 by 5 vs 11 at 20 by 5, rerun in progress | `theory-radar\paper\REVISION_PLAN.md:1-60` |
| chapter 6 section 6.5 | loading weights and stability across folds requested | `theory-radar\paper\REVISION_PLAN.md` issue 6 |
| chapter 7 section 7.2 | second-order leaf values, logistic curvature | ESL 2e 10.9 to 10.13; XGBoost introduction to boosted trees |

## failures and corrections

- NEG-4, `[refuted]`. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL.

## conditions

- Halting a boosting or gradient run when a held-out score stops improving. The stopping rule reads the held-out fold, so the fold it reads is no longer held out for the reported score, and a scorer that has read the test fold scores it perfectly.
- Early stopping is a harness. The round count it picks is a fitted parameter, and the report states which fold picked it and which fold scored it.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Leakage.lean`, theorems `errors_lookup_eq_zero`, `lookup_default`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/CrossValidation.lean`, theorems `sizes_sum`, `accuracy_weighted`, `accuracy_mean_of_equal`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 7.

## related

harness, leakage, cross-validation, boosting, split

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
