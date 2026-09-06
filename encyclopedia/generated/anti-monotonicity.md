# anti-monotonicity

**id.** anti-monotonicity
**kind.** concept

## definition

The property that support cannot increase when an itemset grows, which licenses Apriori to prune every superset of an infrequent itemset without loss. Chapter 5.

## equation

Book equation 5.1.

    s(X)=\frac{\sigma(X)}{N},\qquad c(X\to Y)=\frac{\sigma(X\cup Y)}{\sigma(X)}=\frac{s(X\cup Y)}{s(X)}.

Book equation 5.3.

    X\subseteq Y\ \Longrightarrow\ s(X)\ge s(Y).

## ledger

none

## first stated

Agrawal and Srikant, fast algorithms for mining association rules, 1994, as chapter 5 section 5.3 of *Data Mining as Observation* reads it.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 5 section 5.1 to 5.3, 5.5 | support, confidence, lift, the Apriori principle, FP-growth, closed and maximal itemsets, objective measures, Simpson's paradox, cross-support | TSK 2e chapter 5 |
| chapter 5 section 5.3 | the transferable idea as a course learning outcome | instructor working documents, not public [@bond2026course], `ECE_514-01_FA26_session-outlines.md:117-136` |

## failures and corrections

none

## conditions

- The property that support cannot increase when an itemset grows, since every transaction containing the larger set contains the smaller. It licenses Apriori to prune every superset of an infrequent itemset without loss, because no frequent itemset can lie above an infrequent one.
- The license is a statement about the measure and not about the data, and the book's sidebar carries it to thresholds outside itemsets, where the analogous license is the ceiling on a score that a Youden bound supplies.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/SafePruning.lean`, theorems `support_anti`, `apriori`, `subset_of_frequent`, at observation-data-mining 17f3e9f.

`lean/DataMiningAsObservation/ItemSet.lean`, theorems `supportFrac_mem_unit`, `supportFrac_empty`, `supportFrac_anti`, `supportFrac_union_le`, `closed_of_maximal`, at observation-data-mining 17f3e9f.

## used in

*Data Mining as Observation* chapters 5.

## related

apriori-principle, support, safe-pruning, itemset

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 8c6986b, observation-theory-campaigns 553a902, theory-radar 37c4e6c, observation-data-mining 17f3e9f, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
