# reconstruction error

**id.** reconstruction-error
**kind.** concept

## definition

The squared length of the difference between a row and its approximation, the identity reader's distortion. Chapter 1 section 1.4.

## equation

Book equation 4.2.

    D(b)=\sum_i s_i\sigma_i^{2}\,2^{-2b_i},\qquad s_i=v_i^{\top}P_C\,v_i,\qquad b_i^{\star}=\max\!\Big(0,\ \tfrac12\log_2\frac{s_i\sigma_i^{2}}{\theta}\Big),\qquad \sum_i b_i^{\star}=B,

Book equation 1.1.

    O=(C,\ G,\ B).

Book equation 0.5.

    \Sigma\,v_i=\lambda_i v_i,\qquad \Sigma=\sum_{i=1}^{d}\lambda_i\,v_i v_i^{\top},\qquad v_i\cdot v_j=0\ (i\ne j).

## ledger

- GO-2 (neg. half: not reconstruction). At matched bits, downstream preservation is not controlled by reconstruction error. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:63` at 9f3829f.
- GO-6. At matched rate, output coding ≤ surrogate ≤ reconstruction on the consumer metric; the output–reconstruction gap is governed by the $\ker P_C$ entropy share, and the surrogate–output gap vanishes as rate grows. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:68` at 9f3829f.
- NEG-4. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL. `[refuted]`. `geometric-observation/claims/LEDGER.md:97` at 9f3829f.

## first stated

Chapter 1 section 1.4 and chapter 4 section 4.1 of *Data Mining as Observation*, with the identity slice in `geometric-observation/chapters/ch02_failure_of_observer_free_measurement.md:1-40`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.4 | three virtues one vice, the identity slice | `geometric-observation\chapters\ch02_failure_of_observer_free_measurement.md:1-40` |
| chapter 3 section 3.2 | traces 2.0, diagonals 0.3 and 1.7, consumers at 15 and 75 degrees, distortion 0.39 vs 1.61, 4.1 to one, computed not drawn | `observation-theory\assets\make_flip_figure.py:4-24,107-119` |
| chapter 4 section 4.2 | GO-6, d 8 and r 4, output at or below surrogate at or below reconstruction at every rate, about 500 times, gap 0.41 to 0.005, isotropic control collapses | `geometric-observation\claims\LEDGER.md` row GO-6; `geometric-observation\chapters\ch07_cost.md` |

## failures and corrections

- NEG-4, `[refuted]`. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL.

## conditions

- The squared length of the difference between a row and its approximation, the identity reader's distortion. It is nonnegative, zero exactly when the approximation is the row, a sum of per-coordinate squared errors, and for a projection onto a unit direction it is the squared length less the squared component along it.
- A reconstruction cosine of 0.995 sat beside a perplexity of ten thousand, recalibration improved reconstruction and worsened the consumer, and at matched reconstruction the consumer-aware code won in twelve of twelve domains.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ReconstructionError.lean`, theorems `recon_nonneg`, `recon_eq_zero_iff`, `recon_sum`, `recon_proj`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/ReadDistortion.lean`, theorems `read_distortion`, `identity_reader`, `quad_one`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 1, 4, 6, 7, 8, 11, 12, 13.

## related

identity-reader, read-distortion, distortion, principal-component-analysis, flip-the

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
