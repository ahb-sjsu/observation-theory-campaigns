# lift

**id.** lift
**kind.** concept

## definition

Confidence divided by the consequent's support, so that lift one is the independence baseline. It fails at low support. Chapter 5.

## equation

Book equation 5.2.

    \mathrm{lift}(X\to Y)=\frac{c(X\to Y)}{s(Y)}=\frac{s(X\cup Y)}{s(X)\,s(Y)}.

Book equation 5.1.

    s(X)=\frac{\sigma(X)}{N},\qquad c(X\to Y)=\frac{\sigma(X\cup Y)}{\sigma(X)}=\frac{s(X\cup Y)}{s(X)}.

## ledger

none

## first stated

TSK chapter 5 on objective measures, as chapter 5 section 5.1 of *Data Mining as Observation* states it.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 5 section 5.1 to 5.3, 5.5 | support, confidence, lift, the Apriori principle, FP-growth, closed and maximal itemsets, objective measures, Simpson's paradox, cross-support | TSK 2e chapter 5 |

## failures and corrections

none

## conditions

- Confidence over the consequent's support, the joint support over the product of the two supports. It is one under independence, symmetric in the two itemsets, and bounded by the reciprocal of the consequent's support.
- It fails at low support. One transaction in N containing both items, and neither elsewhere, gives lift N, which is why the rules with the highest lift are the ones chapter 8's multiple-comparison rule applies to.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Lift.lean`, theorems `lift_indep`, `lift_symm`, `lift_le_inv`, `lift_single`, at observation-data-mining 8d458b2.

## used in

*Data Mining as Observation* chapters 5.

## related

apriori, multiple-comparisons, safe-pruning, harness

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 429cc9d, theory-radar 37c4e6c, observation-data-mining 8d458b2, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
