# split

**id.** split
**kind.** instrument

## definition

A partition of the rows into a part the model is fit on and a part it is scored on. A scorer that has read the test part scores it perfectly. Chapter 8 section 8.1.

## equation

Book equation 8.1.

    O_{\mathrm{harness}}=\big(C_{\mathrm{score}},\ G_{\mathrm{metric}},\ B=\text{folds}\times\text{samples}\times\text{seeds}\big).

Book equation 8.2.

    \begin{gathered} \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2}, \\ J=1000,\ \frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}=\frac14\ \Rightarrow\ 1+250=251,\ \ \sqrt{251}=15.84. \end{gathered}

Book equation 12.3.

    \text{validated}\iff \mathrm{AUROC}_{\text{cross}}-\max\big(\mathrm{AUROC}_{\text{untrained}},\ \mathrm{AUROC}_{\text{BoW}}\big)\ \ge\ 0.10.

## ledger

- NEG-4. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL. `[refuted]`. `geometric-observation/claims/LEDGER.md:97` at 9f3829f.
- GO-B-legal (035→036). Legal-citation retrieval (CourtListener), cosine-ranking consumer, LaBSE embeddings — real large corpus, non-physical consumer `[predicted]`. `geometric-observation/claims/LEDGER.md:119` at 9f3829f.

## first stated

Chapter 8 section 8.1 of *Data Mining as Observation*, with the virgin split in `geometric-observation/chapters/ch10_the_blind_probe.md:100-118`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 4 section 4.7 | ESL 7.10.2 numbers | Hastie, Tibshirani, Friedman, ESL 2e, section 7.10.2; chapter 8 of this book |
| chapter 6 section 6.4 | the uncorrected t stored as sigma, 251 and 15.84, nine wins to three, seven, eight, 3 wins 17 ties 11 losses on 31 datasets, the three-way inconsistency | `constraint-gap\review\FINDINGS.md:1-35`; `constraint-gap\README.md:57-76` |
| chapter 8 section 8.1 | ESL 7.10.2 numbers (N=50, p=5000, 100 selected, 3 percent vs 50 percent) | Hastie, Tibshirani, Friedman, ESL 2e, section 7.10.2 |
| chapter 8 section 8.5 | variance inflation 251, SE inflation 15.84, J_eff 3.98, about 62 needed, 3 of 9 at full, 7 at half, 8 at a third | `constraint-gap\review\FINDINGS.md:1-35` |
| chapter 12 section 12.3 | 041 non-oracle, frozen LSA TF-IDF to SVD 100 train-only, AUROC 0.975 vs 0.910, flip tied, magnitude overshot, partial | `geometric-observation\chapters\ch10_the_blind_probe.md:100-118`; `geometric-observation\claims\LEDGER.md` row GO-B-blind 041 |

## failures and corrections

- NEG-4, `[refuted]`. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL.

## conditions

- A partition of the rows into a part the model is fit on and a part it is scored on. The parts' sizes add to the row count, a row in the test part is not in the training part, and a scorer that has read the test part scores it perfectly, which is leakage.
- The virgin split of the non-oracle test raised the flip's margin to 0.796 against 0.780, and the split is fixed before any transform is fit, since an imputation fit on all rows reads the test part.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/CrossValidation.lean`, theorems `sizes_sum`, `accuracy_weighted`, `accuracy_mean_of_equal`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/Leakage.lean`, theorems `errors_lookup_eq_zero`, `lookup_default`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14.

## related

cross-validation, leakage, harness, seed, stratification

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
