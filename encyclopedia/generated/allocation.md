# allocation

**id.** allocation
**kind.** instrument

## definition

The assignment of a bit budget across directions. Water-filling gives directions below the water no bits, and the allocation report warns below effective rank two. Chapter 4 section 4.2.

## equation

Book equation 4.2.

    D(b)=\sum_i s_i\sigma_i^{2}\,2^{-2b_i},\qquad s_i=v_i^{\top}P_C\,v_i,\qquad b_i^{\star}=\max\!\Big(0,\ \tfrac12\log_2\frac{s_i\sigma_i^{2}}{\theta}\Big),\qquad \sum_i b_i^{\star}=B,

Book equation 0.7.

    r_{\mathrm{eff}}=\frac{\big(\sum_i\lambda_i\big)^{2}}{\sum_i\lambda_i^{2}}.

Book equation 4.6.

    \kappa=\operatorname{tr}\big(\bar P_C\,\bar\Sigma_x\big)\in[0,1],\qquad \kappa\to1\ \text{is the coupling null (no flip)}.

## ledger

- GO-4. Fixed-budget verdicts invert under budget-matched observation, per the wavelength mechanism. `[replicated]`. `geometric-observation/claims/LEDGER.md:66` at 9f3829f.
- GO-6. At matched rate, output coding ≤ surrogate ≤ reconstruction on the consumer metric; the output–reconstruction gap is governed by the $\ker P_C$ entropy share, and the surrogate–output gap vanishes as rate grows. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:68` at 9f3829f.

## first stated

Chapter 4 section 4.2 of *Data Mining as Observation*, with the allocation report in `turboquant-pro/turboquant_pro/read_allocation.py:244-307`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 4 section 4.2 | water-filling formula, directions below the water get no bits, the surrogate caveat | `readscope\readscope\allocate.py:1-100` |
| chapter 4 section 4.2 | allocation report, gain over uniform, concentration caution below effective rank 2 | `turboquant-pro\turboquant_pro\read_allocation.py:244-307` |
| chapter 10 section 10.5 | fragile-first allocation 0.7118 vs 0.7251, targets up 0.004 to 0.034, redesigned allocator passed | `turboquant-pro\docs\RESULTS_strata_phase23_gates.md:110-125` |

## failures and corrections

none

## conditions

- The assignment of a bit budget across directions. Water-filling gives directions below the water no bits, the allocation report states its gain over uniform and warns below effective rank two, and a spectrum with half its mass in one direction has effective rank at most four.
- The fragile-first allocation read 0.7118 against 0.7251 and was redesigned, and the budget inversion of GO-4 shows an allocation at fixed m rising while the matched-m allocation collapses.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/WaterFilling.lean`, theorems `contribution_eq_water`, `terms_mul`, `two_sqrt_le`, `distortion2_ge`, `distortion2_eq_of_equal`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/EffectiveRank.lean`, theorems `sq_sum_le`, `effRank_le`, `sum_sq_le_sq_sum`, `one_le_effRank`, `effRank_const`, `effRank_single`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 4, 10, 11.

## related

water-filling, budget, effective-rank, concentrated, bit

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
