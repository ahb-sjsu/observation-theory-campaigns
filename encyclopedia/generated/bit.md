# bit

**id.** bit
**kind.** concept

## definition

The unit of a budget. A direction quantized with b bits is stored at one of two to the power b levels. Chapter 0 section 0.7.

## equation

Book equation 0.13.

    D(b)=\sum_i s_i v_i\,4^{-b_i},\qquad b_i=\max\!\Big(0,\ \tfrac12\log_2\frac{s_i v_i}{\theta}\Big),\qquad \sum_i b_i=B.

Book equation 4.2.

    D(b)=\sum_i s_i\sigma_i^{2}\,2^{-2b_i},\qquad s_i=v_i^{\top}P_C\,v_i,\qquad b_i^{\star}=\max\!\Big(0,\ \tfrac12\log_2\frac{s_i\sigma_i^{2}}{\theta}\Big),\qquad \sum_i b_i^{\star}=B,

## ledger

- GO-4. Fixed-budget verdicts invert under budget-matched observation, per the wavelength mechanism. `[replicated]`. `geometric-observation/claims/LEDGER.md:66` at 9f3829f.
- GO-7. A stored description's description rate and its conditional Landauer reset content are operationally separate resources: the same finite-$n$ code index needing $\hat R\approx0.67$ bits/symbol to describe is fully recoverable from retained side information at bin rate $0.26=0.39\hat R$, fails increasingly below its conditional content, and fails absolutely (err 1.00 at every bin rate) without $S$. `[replicated]`. `geometric-observation/claims/LEDGER.md:69` at 9f3829f.

## first stated

Chapter 0 section 0.7 of *Data Mining as Observation*, with the program's matched-bits comparisons in Volume 14 and turboquant-pro.

## measurements

none

## failures and corrections

none

## conditions

- The unit of a budget. A direction quantized with b bits is stored at one of two to the b levels, so one more bit doubles the levels, halves a uniform quantizer's step, and quarters the squared error of the high-rate model, and bits add across directions since the levels multiply.
- Every flip comparison is at matched bits, since a code that spends more bits is a different budget and not a better reader.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Bit.lean`, theorems `levels_succ`, `levels_add`, `step_succ`, `sqError_succ`, `sqError_antitone`, `levels_zero`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 4, 6, 10, 11, 12, 13, 14.

## related

budget, water-filling, flip, landauers-principle

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
