# itemset

**id.** itemset
**kind.** concept

## definition

A set of items that appear together in a transaction. A closed itemset has no superset with the same support and a maximal one has no frequent superset. Chapter 5.

## equation

Book equation 5.1.

    s(X)=\frac{\sigma(X)}{N},\qquad c(X\to Y)=\frac{\sigma(X\cup Y)}{\sigma(X)}=\frac{s(X\cup Y)}{s(X)}.

Book equation 5.3.

    X\subseteq Y\ \Longrightarrow\ s(X)\ge s(Y).

## ledger

none

## first stated

Agrawal, Imieliński, and Swami, mining association rules, 1993, as TSK chapter 5 presents it and chapter 5 section 5.1 of *Data Mining as Observation* states it.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 5 section 5.1 to 5.3, 5.5 | support, confidence, lift, the Apriori principle, FP-growth, closed and maximal itemsets, objective measures, Simpson's paradox, cross-support | TSK 2e chapter 5 |

## failures and corrections

none

## conditions

- A set of items that appear together in a transaction. Its support lies in the unit interval, the empty itemset has support one, a superset has support at most that of a subset, and the support of a union is at most the smaller of the two supports.
- A closed itemset has no strict superset with the same support and a maximal frequent itemset has no frequent strict superset, and every maximal frequent itemset is closed, since a superset with the same support would be frequent too.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ItemSet.lean`, theorems `supportFrac_mem_unit`, `supportFrac_empty`, `supportFrac_anti`, `supportFrac_union_le`, `closed_of_maximal`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 5.

## related

support, apriori, safe-pruning, confidence

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
