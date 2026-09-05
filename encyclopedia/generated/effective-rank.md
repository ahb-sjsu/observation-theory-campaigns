# effective rank

**id.** effective-rank
**kind.** concept

## definition

The number of directions a matrix really uses, the square of the sum of its eigenvalues over the sum of their squares, with no cutoff to choose. Equation 0.7.

## equation

Book equation 0.7.

    r_{\mathrm{eff}}=\frac{\big(\sum_i\lambda_i\big)^{2}}{\sum_i\lambda_i^{2}}.

Book equation 4.2.

    D(b)=\sum_i s_i\sigma_i^{2}\,2^{-2b_i},\qquad s_i=v_i^{\top}P_C\,v_i,\qquad b_i^{\star}=\max\!\Big(0,\ \tfrac12\log_2\frac{s_i\sigma_i^{2}}{\theta}\Big),\qquad \sum_i b_i^{\star}=B,

## ledger

- OT-7. The damage form, trace pairing, rank, and loading covariance are GL(d)-invariant under `P' = A⁻ᵀPA⁻¹`, while spectrum, effective rank, principal angles, and water-filling are O(d)-only — consumer-weighted damage is a geometric scalar, and P3's cliff cannot be bought down by reparameterization. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:30` at 7d91883.

## first stated

The participation ratio of a spectrum, applied to read operators in readscope, `readscope/readscope/spectrum.py:35-70`, and chapter 0 section 0.4 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 4 section 4.2 | effective rank as participation ratio, energy rank | `readscope\readscope\spectrum.py:35-70` |
| chapter 4 section 4.2 | allocation report, gain over uniform, concentration caution below effective rank 2 | `turboquant-pro\turboquant_pro\read_allocation.py:244-307` |
| chapter 9 section 9.4 | explained ratios, effective rank 5.19 of 8, convergence with a second method, property of the representation not the space | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:10-18` |
| chapter 14 section 14.3 | floor 0.08 to 0.12, balanced resample 3001 items, identity attack 0.237 with interval 0.20 to 0.28 on 289, sexual 0.204, threat 0.093 retracted, first pass 18 positives, 87.7 and 1.4 percent | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:20-64` |
| chapter 14 section 14.3 | contraction 0.779 to 0.863, 77 of 1600, 4.8 percent, 0.872 to 0.863, weight 2.69 | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:66-99` |
| chapter 14 section 14.5 | the contraction formula fairness minus the general component | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:90-99` |
| chapter 14 section 14.7 | 51 percent moderated at 80 and 95 percent precision on the balanced set | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:84-88` |

## failures and corrections

none

## conditions

- The effective rank is the square of the sum of the eigenvalues over the sum of their squares, between one and the dimension for a nonnegative spectrum, with no cutoff to choose.
- It is not invariant under a change of basis of the input, unlike the trace pairing and the rank, and the ledger row that says so is the one that licenses comparing read operators across coordinate systems.
- An allocation over a spectrum with effective rank below two concentrates on one direction, and the allocation report says so before giving a gain.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/EffectiveRank.lean`, theorems `sq_sum_le`, `effRank_le`, `sum_sq_le_sq_sum`, `one_le_effRank`, `effRank_const`, `effRank_single`, at observation-data-mining 43ea852.

## used in

*Data Mining as Observation* chapters 0, 4, 9, 11, 14.

## related

read-operator, read-subspace, water-filling, recognizer

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns b331d4f, theory-radar 37c4e6c, observation-data-mining 43ea852, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
