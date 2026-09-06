# concentrated

**id.** concentrated
**kind.** concept

## definition

Of a spectrum, having a few eigenvalues that carry most of the total. Chapter 0 section 0.4.

## equation

Book equation 0.7.

    r_{\mathrm{eff}}=\frac{\big(\sum_i\lambda_i\big)^{2}}{\sum_i\lambda_i^{2}}.

Book equation 0.5.

    \Sigma\,v_i=\lambda_i v_i,\qquad \Sigma=\sum_{i=1}^{d}\lambda_i\,v_i v_i^{\top},\qquad v_i\cdot v_j=0\ (i\ne j).

## ledger

- OT-7. The damage form, trace pairing, rank, and loading covariance are GL(d)-invariant under `P' = A⁻ᵀPA⁻¹`, while spectrum, effective rank, principal angles, and water-filling are O(d)-only — consumer-weighted damage is a geometric scalar, and P3's cliff cannot be bought down by reparameterization. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:30` at 8c6986b.

## first stated

Chapter 0 section 0.4 of *Data Mining as Observation*, with the allocation report's concentration caution in `turboquant-pro/turboquant_pro/read_allocation.py:244-307`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 4 section 4.2 | effective rank as participation ratio, energy rank | `readscope\readscope\spectrum.py:35-70` |
| chapter 4 section 4.2 | allocation report, gain over uniform, concentration caution below effective rank 2 | `turboquant-pro\turboquant_pro\read_allocation.py:244-307` |

## failures and corrections

none

## conditions

- Of a spectrum, having a few eigenvalues that carry most of the total. If one eigenvalue carries a fraction f of the total, the effective rank is at most one over f squared, so half the mass in one direction gives effective rank at most four.
- The allocation report warns below effective rank two, which is the same statement read from the rank side, and an allocation over a concentrated spectrum spends almost everything on one direction.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Concentrated.lean`, theorems `sq_le_sum_sq`, `effRank_le_of_fraction`, `effRank_le_four`, at observation-data-mining 17f3e9f.

## used in

*Data Mining as Observation* chapters 0, 3, 4, 6, 10, 11, 13.

## related

spectrum, effective-rank, water-filling, isotropic

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 8c6986b, observation-theory-campaigns 553a902, theory-radar 37c4e6c, observation-data-mining 17f3e9f, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
