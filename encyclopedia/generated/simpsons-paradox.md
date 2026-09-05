# Simpson's paradox

**id.** simpsons-paradox
**kind.** concept

## definition

A reversal of a comparison when groups are combined, which the book reads as an aggregation quotient. Chapter 5.

## equation

Book equation 10.7.

    \text{verdict}=\min_{i:\ n_i\ge n_{\min},\ |Q_i|\ge q_{\min}}\ \mathrm{score}_i,\qquad \text{ABSTAIN otherwise}.

## ledger

none

## first stated

TSK chapter 5 on objective measures, as chapter 5 section 5.5 of *Data Mining as Observation* reads it, an aggregation quotient.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 5 section 5.1 to 5.3, 5.5 | support, confidence, lift, the Apriori principle, FP-growth, closed and maximal itemsets, objective measures, Simpson's paradox, cross-support | TSK 2e chapter 5 |

## failures and corrections

none

## conditions

- A pooled rate is the size-weighted mean of the group rates, so pooling is a quotient that declares the group labels irrelevant, and it can reverse a comparison that holds in every group when the groups have different sizes under the two arms.
- With equal group sizes under both arms the pooled comparison agrees with a comparison that holds in every group. The book's answer is the min-over-strata verdict, which never pools.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Simpson.lean`, theorems `pooled_eq_weighted`, `reversal`, `no_reversal_of_equal_sizes`, at observation-data-mining 43ea852.

## used in

*Data Mining as Observation* chapters 5.

## related

quotient, min-over-strata, abstention, deployment-mismatch

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns b331d4f, theory-radar 37c4e6c, observation-data-mining 43ea852, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
