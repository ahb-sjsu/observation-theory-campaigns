# reliability weight

**id.** reliability-weight
**kind.** concept

## definition

Zero or twice a validated encoder's held-out AUROC minus one, whichever is larger, used as that encoder's authority. It is a discrimination weight, and the calibration evidence is the expected calibration error reported beside it. Equation 0.38.

## equation

Book equation 0.38.

    w=\max\big(0,\ 2\cdot\mathrm{AUROC}-1\big).

Book equation 0.16.

    \mathrm{AUROC}=\Pr\big[s^{+}>s^{-}\big]\ +\ \tfrac12\Pr\big[s^{+}=s^{-}\big].

## ledger

none

## first stated

The moral-embedding program's calibrated authority, `gtc-prototype/docs/CALIBRATED_AUTHORITY.md:19-63` and `xbse/README.md:175-195`, and chapter 12 section 12.5 and chapter 14 section 14.2 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 12 section 12.5 | ECE 0.018 to 0.101 vs raw up to 0.223, reliability weight, audit binding | `xbse\README.md:175-195`; `gtc-prototype\docs\CALIBRATED_AUTHORITY.md:19-63` |
| chapter 14 section 14.2 | reliability weights and calibration errors per axis, the collapsed family's mean weight 0.559 against the general valence channel's own 0.735, the three design rules, 0.048 to 0.049 and 0.089 to 0.101 at 696 pairs | `gtc-prototype\docs\CALIBRATED_AUTHORITY.md:1-65` |

## failures and corrections

none

## conditions

- The weight is zero or twice the held-out AUROC minus one, whichever is larger, so it lies in the unit interval, is zero at chance and below, and is unchanged by any strictly monotone recalibration of the score.
- It is a discrimination weight and not a calibration weight. The expected calibration error is reported beside it, and an encoder below the untrained baseline gets weight zero whatever its calibration.
- One formula and one source. The registry that consumes the weights computes them from the recorded held-out AUROC and nothing else.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ReliabilityWeight.lean`, theorems `pair_le_one`, `aurocNum_le`, `auroc_le_one`, `weight_mem_unit`, `weight_eq_zero_of_le_half`, `weight_comp`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 0, 12, 14.

## related

monotone-invariance, harness, posited-versus-measured, certificate

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
