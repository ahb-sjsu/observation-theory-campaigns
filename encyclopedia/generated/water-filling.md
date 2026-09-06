# water-filling

**id.** water-filling
**kind.** concept

## definition

The allocation of a bit budget across directions that gives each direction half the log of its sensitivity-weighted variance over a common water level, and nothing to directions under the water. Equation 0.13.

## equation

Book equation 0.13.

    D(b)=\sum_i s_i v_i\,4^{-b_i},\qquad b_i=\max\!\Big(0,\ \tfrac12\log_2\frac{s_i v_i}{\theta}\Big),\qquad \sum_i b_i=B.

Book equation 4.2.

    D(b)=\sum_i s_i\sigma_i^{2}\,2^{-2b_i},\qquad s_i=v_i^{\top}P_C\,v_i,\qquad b_i^{\star}=\max\!\Big(0,\ \tfrac12\log_2\frac{s_i\sigma_i^{2}}{\theta}\Big),\qquad \sum_i b_i^{\star}=B,

## ledger

none

## first stated

Shannon's power allocation across channels, applied with a consumer's sensitivity in place of a signal's power in readscope and turboquant-pro, and chapter 0 section 0.7 and chapter 4 section 4.2 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.3 | refusal regimes, selection consumers read order, recurrences compound | `readscope\readscope\regimes.py:1-60` |
| chapter 2 section 2.4 | C-7, sixteen points in 128 dimensions, rank fifteen, near ten to the eleventh nats, refuses when samples do not exceed dimension, warns below five per dimension, loading is a property of two distributions | `readscope\SPEC.md:653-680` |
| chapter 2 section 2.4 | C-7b, 92.1 percent, fit range 0.89 to 91.64, 15 percent inside, maximum 1.9e12, endpoint attenuation 0.437, 202 of 240 at 1.0, refuses to extrapolate, loading is a warning | `readscope\SPEC.md:680-720`; `readscope\readscope\loading.py:136-219` |
| chapter 2 section 2.6 | 0.647 published, 1.000 recovered, weighted vs unweighted median 0.796 range 0.678 to 0.985, probe 1.000 on every cell, 36 cells, one cell at 0.985 | `readscope\SPEC.md:410-450` |
| chapter 2 section 2.6 | C-10, 24 to 576 queries, reference rank 24 to 128, 0.821 to 0.703 vs 0.647, 68 percent of distance closed, 0.174 to 0.056, probe 1.000000 on 16 cells, residual uncontrolled | `readscope\SPEC.md:450-500` |
| chapter 3 section 3.4 | chance overlap rank over dim reported with every reading | `readscope\README.md:200-222`; `readscope\readscope\metrics.py:31-99` |
| chapter 4 section 4.2 | water-filling formula, directions below the water get no bits, the surrogate caveat | `readscope\readscope\allocate.py:1-100` |
| chapter 4 section 4.2 | effective rank as participation ratio, energy rank | `readscope\readscope\spectrum.py:35-70` |
| chapter 4 section 4.4 | GO-4 budget inversion, fixed m 10 rises, matched m 121, 126, 159 collapses, 3 seeds | `geometric-observation\claims\LEDGER.md` row GO-4 |
| chapter 4 section 4.5 | GloVe table, 73 percent at 64 components, 0.685 vs 0.862 and 0.866, 0.906 at matched bytes, 0.989 at 37 bytes, 768 to 256 keeps about 99 percent, the 95 percent rule | `turboquant-pro\benchmarks\RESULTS_glove.md:1-40` |
| chapter 6 section 6.1 | selection consumers have zero sensitivity almost everywhere | `readscope\readscope\regimes.py:1-60` |
| chapter 8 section 8.3 | C-8 D5 mean absolute error 0.0000, every reading 1.000, C-7b saturation, the F-21 rule | `readscope\CALIBRATION.md` F-21 (about line 519) |
| chapter 8 section 8.4 | C-11c paired null, rank 2 positional 0.385 vs null 0.572, 0.615 vs 0.224, 14 of 16 cells, scope 16 cells one 3B model 192 positions | `readscope\SPEC.md:806-857`; `readscope\calibration\records\c11c-operator-drift.json` |
| chapter 11 section 11.7 | k over d table 1, 2, 2, 16, 16, 16 | `readscope\README.md:118-141`; `readscope\SPEC.md:243-285`, record `readscope\calibration\records\c2e-budget-law.json` |
| chapter 11 section 11.7 | rank-independent, 0.646 vs 0.366 at half dimension, never 0.90 below k equals d | `readscope\CALIBRATION.md:419-434` F-15 |
| chapter 11 section 11.7 | C-15 equal budget, 3072 observations, medians 0.02, 0.11, 0.05, 0.04, 1.0, 1.0, margin 0.883 vs 0.3, 0.062 to 0.057 at 8x | `readscope\SPEC.md:285-323`, record `readscope\calibration\records\c15-budget-surface.json`, `readscope\calibration\DECLARATION-C15.md` |
| chapter 11 section 11.7 | confinement theorem, side information moves the cliff to d minus k0, noisy cliff proved then measured | `readscope\PRINCIPLES.md:112-142`; `geometric-observation\crucible\OT3-THEOREM.md`; `geometric-observation\crucible\OT3-NOISY-THEOREM.md` |
| chapter 11 section 11.7 | 124 cells at resolution 1.000 at k over d 1.25, five families, linearity partial | `readscope\README.md:200-222` |
| chapter 11 section 11.9 | drift at rank one 0.667 vs null 0.933, sixteen cells | `readscope\CALIBRATION.md:600-660` F-24; `readscope\calibration\records\c11c-operator-drift.json` |
| chapter 11 section 11.9 | C-12 four bars, 40 documents, 512 tokens, 13.4 point difference, teacher forcing removes it, negative 0.015 vs 0.005, Spearman negative 0.13 at p 0.45, sign test p 0.42, verdict FAIL, feedback compounding | `readscope\calibration\records\c12-longgen-drift-sym.json`; `readscope\calibration\DECLARATION-C12.md` at commit `90e2ce2`; `readscope\SPEC.md:806-825` |

## failures and corrections

none

## conditions

- The closed form assumes a uniform quantizer at high rate, so that each bit quarters the squared error, and directions taken as the eigenvectors of the covariance so that their errors add.
- The sensitivity of each direction is read in that same eigenbasis, as the quadratic form of the read operator along the eigenvector, and pairing the eigenvalues of the two matrices is valid only when they share an eigenbasis.
- Coarse quantizers, unequal codebook steps, and errors not spread evenly depart from the formula, and chapter 4 reports where a measured allocation did.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/WaterFilling.lean`, theorems `contribution_eq_water`, `terms_mul`, `two_sqrt_le`, `distortion2_ge`, `distortion2_eq_of_equal`, at observation-data-mining 17f3e9f.

## used in

*Data Mining as Observation* chapters 0, 4.

## related

read-operator, read-distortion, alignment, flip

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 01e53bc, observation-theory-campaigns 0c2e3f9, theory-radar 37c4e6c, observation-data-mining 17f3e9f, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
