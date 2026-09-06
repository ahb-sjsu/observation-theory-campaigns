# transaction

**id.** transaction
**kind.** concept

## definition

One row of a market-basket table, the set of items bought together. Chapter 5 section 5.1.

## equation

Book equation 5.1.

    s(X)=\frac{\sigma(X)}{N},\qquad c(X\to Y)=\frac{\sigma(X\cup Y)}{\sigma(X)}=\frac{s(X\cup Y)}{s(X)}.

Book equation 5.3.

    X\subseteq Y\ \Longrightarrow\ s(X)\ge s(Y).

## ledger

none

## first stated

Agrawal, Imieliński, and Swami, mining association rules, 1993, as chapter 5 section 5.1 of *Data Mining as Observation* reads it.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 5 section 5.1 to 5.3, 5.5 | support, confidence, lift, the Apriori principle, FP-growth, closed and maximal itemsets, objective measures, Simpson's paradox, cross-support | TSK 2e chapter 5 |

## failures and corrections

none

## conditions

- One row of a market-basket table, the set of items bought together. The support of an itemset counts the transactions that contain it, it cannot rise as the itemset grows, and the support fraction lies in the unit interval.
- A transaction is the unit the consumer reads in chapter 5, and which items count as the same is the quotient the pattern report has to name.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ItemSet.lean`, theorems `supportFrac_mem_unit`, `supportFrac_empty`, `supportFrac_anti`, `supportFrac_union_le`, `closed_of_maximal`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/SafePruning.lean`, theorems `support_anti`, `apriori`, `subset_of_frequent`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 1, 5, 13.

## related

itemset, support, confidence, apriori-principle, anti-monotonicity

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
