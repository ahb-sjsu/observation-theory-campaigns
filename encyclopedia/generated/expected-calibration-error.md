# expected calibration error

**id.** expected-calibration-error
**kind.** instrument

## definition

The average over score bins of the absolute difference between the mean score and the fraction of positives in the bin. Equation 0.29.

## equation

Book equation 0.29.

    \mathrm{ECE}=\sum_b\frac{n_b}{n}\,\big|\bar s_b-\bar y_b\big|.

Book equation 0.38.

    w=\max\big(0,\ 2\cdot\mathrm{AUROC}-1\big).

Book equation 14.2.

    \mathrm{coverage\ difference}_c=\mathrm{AUROC}_c(\text{embedding})-\mathrm{AUROC}_c(\text{validated axes}),\qquad \text{floor}\approx0.08\ \text{to}\ 0.12.

## ledger

- NEG-4. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL. `[refuted]`. `geometric-observation/claims/LEDGER.md:97` at 8c6986b.

## first stated

Chapter 0 section 0.14 of *Data Mining as Observation*, equation 0.29, with the program's per-encoder errors in `xbse/README.md:175-195` and `gtc-prototype/docs/CALIBRATED_AUTHORITY.md:19-63`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 12 section 12.5 | ECE 0.018 to 0.101 vs raw up to 0.223, reliability weight, audit binding | `xbse\README.md:175-195`; `gtc-prototype\docs\CALIBRATED_AUTHORITY.md:19-63` |
| chapter 14 section 14.2 | reliability weights and calibration errors per axis, the collapsed family's mean weight 0.559 against the general valence channel's own 0.735, the three design rules, 0.048 to 0.049 and 0.089 to 0.101 at 696 pairs | `gtc-prototype\docs\CALIBRATED_AUTHORITY.md:1-65` |

## failures and corrections

- NEG-4, `[refuted]`. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL.

## conditions

- The average over score bins, weighted by bin size, of the absolute difference between the bin's mean score and its fraction of positives. It lies in the unit interval, it is zero exactly when every bin's mean score equals its positive fraction, and a calibrated scorer has error zero.
- The program's validated encoders carry errors of 0.018 to 0.101 on held-out splits against raw values up to 0.223, and the reliability weight that gates an encoder's authority is computed beside it.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Calibration.lean`, theorems `ece_nonneg`, `ece_le_one`, `ece_eq_zero_iff`, `ece_of_calibrated`, at observation-data-mining 17f3e9f.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14.

## related

calibration, reliability-weight, auroc, threshold

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 8c6986b, observation-theory-campaigns 553a902, theory-radar 37c4e6c, observation-data-mining 17f3e9f, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
