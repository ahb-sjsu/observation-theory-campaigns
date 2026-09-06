# disparate impact ratio

**id.** disparate-impact-ratio
**kind.** concept

## definition

The rate of a favourable decision in one group divided by the rate in another. Equation 0.37.

## equation

Book equation 0.37.

    \mathrm{DI}=\frac{\Pr[\hat y=1\mid g=a]}{\Pr[\hat y=1\mid g=b]},\qquad \text{equalized odds}:\ \mathrm{TPR}_a=\mathrm{TPR}_b,\ \mathrm{FPR}_a=\mathrm{FPR}_b.

Book equation 14.5.

    \mathrm{FC}_g=\Pr\big[y=\text{violation}\ \big|\ \hat y=\text{clear},\ g\big],\qquad \text{verdict}=\max_{g:\ n_g\ge n_{\min}}\mathrm{FC}_g,\qquad \text{ABSTAIN otherwise}.

## ledger

none

## first stated

Chapter 0 section 0.18 and chapter 14 section 14.6 of *Data Mining as Observation*, with the per-group verdict of equation 14.5.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 14 section 14.1 | the re-gate table, prediction before result, both reports kept, binding nulls, 7 of 9 inside the interval, rights as a hard rule | `gtc-prototype\docs\REGATE.md:1-70` |

## failures and corrections

none

## conditions

- The ratio of the favourable-decision rate in one group to the rate in another. It is one exactly when the rates agree, it inverts when the groups are swapped, and the four-fifths rule is a statement about the rate gap.
- The book's verdict is per group with a null, the worst group's false-clear rate over the groups large enough to score, which clears a bar exactly when every scored group does and is never below the pooled rate.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/DisparateImpact.lean`, theorems `ratio_eq_one_iff`, `ratio_swap`, `four_fifths_iff`, `verdict_le_iff`, `weighted_le_verdict`, at observation-data-mining 1c6cd64.

## used in

*Data Mining as Observation* chapters 0, 14.

## related

equalized-odds, min-over-strata, false-clear-rate, abstention

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 09cc919, theory-radar 37c4e6c, observation-data-mining 1c6cd64, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
