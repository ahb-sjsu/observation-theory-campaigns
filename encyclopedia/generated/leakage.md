# leakage

**id.** leakage
**kind.** concept

## definition

Any information in the training data that could only be known after the decision, or any identifier that lets the model recognize a row it will be tested on. Chapter 8.

## equation

Book equation 8.1.

    O_{\mathrm{harness}}=\big(C_{\mathrm{score}},\ G_{\mathrm{metric}},\ B=\text{folds}\times\text{samples}\times\text{seeds}\big).

## ledger

- NEG-2. Reconstruction cosine as a proxy for key quality. `[refuted]`. `geometric-observation/claims/LEDGER.md:95` at 7d91883.

## first stated

Chapter 8 section 8.1 of *Data Mining as Observation*, with the ESL example of selection before the split, Hastie, Tibshirani, and Friedman, section 7.10.2.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 4 section 4.7 | ESL 7.10.2 numbers | Hastie, Tibshirani, Friedman, ESL 2e, section 7.10.2; chapter 8 of this book |
| chapter 8 section 8.1 | ESL 7.10.2 numbers (N=50, p=5000, 100 selected, 3 percent vs 50 percent) | Hastie, Tibshirani, Friedman, ESL 2e, section 7.10.2 |
| chapter 8 section 8.1 | G1 339.9 vs 71.9 same corpus, real about 61, rounds 1 to 4 at 300 to 420, three families falsified | `openvector-bench\results\QUERY_COUPLING_ARTIFACT.md:1-20` |

## failures and corrections

- NEG-2, `[refuted]`. Reconstruction cosine as a proxy for key quality.

## conditions

- Leakage is any information in the training data that could only be known after the decision, or any identifier that lets the model recognize a row it will be tested on. It is a property of the harness's read subspace, not of the model.
- Selecting features on the whole data and then cross-validating leaks the test fold into the selection, and the reported error can fall from the true rate to a fraction of it, as the ESL example shows.
- Coupling between the queries and the corpus of a retrieval benchmark is leakage of the same kind, and the program's hubness numbers moved by a factor of several when the coupling was removed.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Leakage.lean`, theorems `errors_lookup_eq_zero`, `lookup_default`, at observation-data-mining 51c193c.

## used in

*Data Mining as Observation* chapters 1, 2, 4, 8.

## related

harness, preregistration, sealed, hubness

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns f206f90, theory-radar 37c4e6c, observation-data-mining 51c193c, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
