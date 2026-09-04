# balanced accuracy

**id.** balanced-accuracy
**kind.** concept

## definition

The mean of the per-class recalls, so that a large class cannot hide a small one. Equation 0.34.

## equation

Book equation 0.34.

    \mathrm{BA}=\frac1K\sum_{k=1}^{K}\frac{\text{correct in class }k}{\text{rows in class }k}.

Book equation 10.7.

    \text{verdict}=\min_{i:\ n_i\ge n_{\min},\ |Q_i|\ge q_{\min}}\ \mathrm{score}_i,\qquad \text{ABSTAIN otherwise}.

## ledger

- NEG-11. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain. `[refuted]`. `geometric-observation/claims/LEDGER.md:104` at 7d91883.

## first stated

Chapter 0 section 0.14 of *Data Mining as Observation*, with the program's use in the anti-hub category table, `openvector-bench/results/R13_STAGE1_RESULTS.md`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.5 | query mass best single feature at every K for all four responses, seven features add at most 20 percent, threshold 1.25 on three of four, zero of four, 1000 real queries, 1024 dimensions | `openvector-bench\results\R13_STAGE0_RESULT.md:40-50`; `openvector-bench\results\R13_STAGE1_RESULT.md:1-40` |
| chapter 10 section 10.2 | five kinds, balanced accuracy 0.611, 0.718, 0.684, the category table, per-category 0.57 to 0.82, the sweep, pigeonhole floor | `openvector-bench\results\R13_STAGE1_RESULT.md:40-75` |
| chapter 10 section 10.2 | half 2 failed, at most 1.28 times against 2, withdrawal and its scope | `openvector-bench\results\R13_STAGE1_RESULT.md:75-110` |
| chapter 11 section 11.6 | query mass best single feature at every K for all four responses, seven features add at most 20 percent at 12 leaves, threshold 1.25 on three of four, zero of four, 1000 real queries, 1024 dimensions | `openvector-bench\results\R13_STAGE0_RESULT.md:40-50`; `openvector-bench\results\R13_STAGE1_RESULT.md:1-40` |

## failures and corrections

- NEG-11, `[refuted]`. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain.

## conditions

- The mean of the per-class recalls, between the worst class and the best. Plain accuracy is the size-weighted mean of the same recalls, so a class of 990 rows recalled perfectly and a class of 10 never recalled give accuracy 0.99 and balanced accuracy 0.5.
- The book prefers the min over classes to the mean where a verdict is at stake, since a mean can still hide one failing class among many.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/BalancedAccuracy.lean`, theorems `min_le_balanced`, `balanced_le_max`, `hidden_class`, at observation-data-mining 51c193c.

## used in

*Data Mining as Observation* chapters 0, 10.

## related

min-over-strata, anti-hub, abstention, harness

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns f206f90, theory-radar 37c4e6c, observation-data-mining 51c193c, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
