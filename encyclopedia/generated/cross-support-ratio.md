# cross-support ratio

**id.** cross-support-ratio
**kind.** concept

## definition

The smallest item support in an itemset over the largest, with a threshold below which the itemset is discarded. Chapter 5.

## equation

Book equation 5.3.

    X\subseteq Y\ \Longrightarrow\ s(X)\ge s(Y).

Book equation 5.1.

    s(X)=\frac{\sigma(X)}{N},\qquad c(X\to Y)=\frac{\sigma(X\cup Y)}{\sigma(X)}=\frac{s(X\cup Y)}{s(X)}.

## ledger

none

## first stated

TSK chapter 5 on cross-support patterns, as chapter 5 section 5.5 of *Data Mining as Observation* states it.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 5 section 5.1 to 5.3, 5.5 | support, confidence, lift, the Apriori principle, FP-growth, closed and maximal itemsets, objective measures, Simpson's paradox, cross-support | TSK 2e chapter 5 |

## failures and corrections

none

## conditions

- The smallest item support in an itemset over the largest. It lies in the unit interval, is one exactly when every item has the same support, and adding an item can only lower it, so a threshold on it prunes supersets safely in chapter 5's sense.
- It is a property of the item supports alone and says nothing about the itemset's own support, so it discards an itemset for pairing a common item with a rare one, not for being rare.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/CrossSupport.lean`, theorems `ratio_mem_unit`, `ratio_eq_one_iff`, `ratio_anti`, at observation-data-mining 7199131.

## used in

*Data Mining as Observation* chapters 5.

## related

apriori, safe-pruning, lift, multiple-comparisons

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns e062d3e, theory-radar 37c4e6c, observation-data-mining 7199131, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
