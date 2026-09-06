# chance level

**id.** chance-level
**kind.** concept

## definition

The value a rank statistic reaches on average under a random ranking. Zero for a correlation, one half for AUROC. Chapter 0 section 0.8.

## equation

Book equation 0.16.

    \mathrm{AUROC}=\Pr\big[s^{+}>s^{-}\big]\ +\ \tfrac12\Pr\big[s^{+}=s^{-}\big].

Book equation 0.15.

    \tau=\frac{\#\{\text{concordant pairs}\}-\#\{\text{discordant pairs}\}}{n(n-1)/2}.

Book equation 0.38.

    w=\max\big(0,\ 2\cdot\mathrm{AUROC}-1\big).

## ledger

none

## first stated

Chapter 0 section 0.8 of *Data Mining as Observation*, with the program's chance-overlap reporting in `readscope/readscope/metrics.py:31-99`.

## measurements

none

## failures and corrections

none

## conditions

- The value a rank statistic reaches under a ranking that carries no information. A constant score ties every pair, so its AUROC is one half when both classes are present, its Kendall correlation with any score is zero, and its reliability weight is zero.
- Every reading the probe reports comes with its chance overlap beside it, and a gate subtracts the chance level before it counts a margin.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ChanceLevel.lean`, theorems `aurocNum_const`, `auroc_const`, `weight_const`, `tau_const`, at observation-data-mining 1c6cd64.

## used in

*Data Mining as Observation* chapters 0, 3, 6, 11.

## related

reliability-weight, cross-corpus-gate, kendall-correlation, harness

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 09cc919, theory-radar 37c4e6c, observation-data-mining 1c6cd64, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
