# Apriori principle

**id.** apriori
**kind.** result

## definition

The statement that every subset of a frequent itemset is frequent, the contrapositive of anti-monotonicity. Chapter 5.

## equation

Book equation 5.3.

    X\subseteq Y\ \Longrightarrow\ s(X)\ge s(Y).

Book equation 5.1.

    s(X)=\frac{\sigma(X)}{N},\qquad c(X\to Y)=\frac{\sigma(X\cup Y)}{\sigma(X)}=\frac{s(X\cup Y)}{s(X)}.

## ledger

none

## first stated

Agrawal and Srikant, fast algorithms for mining association rules, 1994, as TSK chapter 5 presents it, and chapter 5 section 5.3 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 5 section 5.1 to 5.3, 5.5 | support, confidence, lift, the Apriori principle, FP-growth, closed and maximal itemsets, objective measures, Simpson's paradox, cross-support | TSK 2e chapter 5 |

## failures and corrections

none

## conditions

- Support cannot increase when an itemset grows, so an infrequent itemset has only infrequent supersets and every subset of a frequent itemset is frequent. This holds for any finite collection of transactions.
- The principle licenses pruning the lattice above an infrequent itemset without counting, and the count of candidates rather than the count of transactions decides whether the run finishes.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/SafePruning.lean`, theorems `support_anti`, `apriori`, `subset_of_frequent`, at observation-data-mining 2b00d80.

## used in

*Data Mining as Observation* chapters 5.

## related

safe-pruning, monotone-invariance

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns e448a13, theory-radar 37c4e6c, observation-data-mining 2b00d80, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
