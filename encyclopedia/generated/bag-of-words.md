# bag of words

**id.** bag-of-words
**kind.** concept

## definition

A representation of a document as a vector with one coordinate per vocabulary term holding that term's count. Chapter 12.

## equation

Book equation 0.36.

    w_{t,d}=\mathrm{tf}_{t,d}\cdot\ln\frac{N}{\mathrm{df}_t},\qquad \mathrm{tf}_{t,d}=\frac{\text{count of }t\text{ in }d}{\text{length of }d},\qquad \mathrm{df}_t=\text{documents containing }t.

Book equation 12.3.

    \text{validated}\iff \mathrm{AUROC}_{\text{cross}}-\max\big(\mathrm{AUROC}_{\text{untrained}},\ \mathrm{AUROC}_{\text{BoW}}\big)\ \ge\ 0.10.

## ledger

none

## first stated

Chapter 12 section 12.1 of *Data Mining as Observation*, with the program's bag-of-words null in `xbse/README.md:104-130` and the chapter 14 scorecard.

## measurements

none

## failures and corrections

none

## conditions

- A document as the vector of its term counts. Two documents that are rearrangements of each other have the same bag, so the bag is a quotient that declares word order irrelevant, the counts are nonnegative, and they sum to the document's length.
- As a null model it reads only counts, and an encoder is validated only when its held-out AUROC clears the bag's by the preregistered margin. The scorecard's bag scores lie between 0.46 and 0.54, near chance.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/BagOfWords.lean`, theorems `bag_perm`, `bag_example`, `bag_sum`, `bag_absent`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 0, 12, 14.

## related

tf-idf, cross-corpus-gate, quotient, nuisance

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
