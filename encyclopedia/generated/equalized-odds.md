# equalized odds

**id.** equalized-odds
**kind.** concept

## definition

The requirement that the true-positive rate and the false-positive rate be the same across groups. Equation 0.37.

## equation

Book equation 0.37.

    \mathrm{DI}=\frac{\Pr[\hat y=1\mid g=a]}{\Pr[\hat y=1\mid g=b]},\qquad \text{equalized odds}:\ \mathrm{TPR}_a=\mathrm{TPR}_b,\ \mathrm{FPR}_a=\mathrm{FPR}_b.

## ledger

none

## first stated

Chapter 0 section 0.18 and chapter 14 section 14.6 of *Data Mining as Observation*, where fairness cannot be had three ways.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 14 section 14.1 | the re-gate table, prediction before result, both reports kept, binding nulls, 7 of 9 inside the interval, rights as a hard rule | `gtc-prototype\docs\REGATE.md:1-70` |

## failures and corrections

none

## conditions

- Equal true-positive and false-positive rates across groups. A group's favourable rate is its true-positive rate times its base rate plus its false-positive rate times the rest, so under equalized odds the favourable rates agree exactly when the base rates do, given that the classifier separates at all.
- Equalized odds and parity of outcomes therefore conflict whenever the base rates differ. With rates 0.8 and 0.2 and base rates one half and one tenth the favourable rates are 0.5 and 0.26, a ratio below four fifths.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/EqualizedOdds.lean`, theorems `parity_of_equal_base`, `favourable_sub`, `parity_iff_equal_base`, `example_conflict`, at observation-data-mining 49fcb16.

## used in

*Data Mining as Observation* chapters 0, 3, 10, 12, 14.

## related

disparate-impact-ratio, calibration, min-over-strata, certificate

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 27b21e4, theory-radar 37c4e6c, observation-data-mining 49fcb16, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
