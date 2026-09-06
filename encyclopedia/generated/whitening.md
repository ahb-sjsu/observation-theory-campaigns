# whitening

**id.** whitening
**kind.** concept

## definition

Rescaling data so that its covariance becomes the identity. Equation 0.6.

## equation

Book equation 0.6.

    x_{\mathrm w}=\Sigma^{-1/2}(x-\mu),\qquad \Sigma^{-1/2}=\sum_i\lambda_i^{-1/2}\,v_i v_i^{\top}.

Book equation 0.5.

    \Sigma\,v_i=\lambda_i v_i,\qquad \Sigma=\sum_{i=1}^{d}\lambda_i\,v_i v_i^{\top},\qquad v_i\cdot v_j=0\ (i\ne j).

## ledger

- GO-2 (neg. half: not reconstruction). At matched bits, downstream preservation is not controlled by reconstruction error. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:63` at 7d91883.

## first stated

Chapter 0 section 0.2 of *Data Mining as Observation*, with the program's whitened code in Volume 14 chapter 8, `geometric-observation/chapters/ch08_value.md:84-97`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.5 | whitened code wins at every budget | `geometric-observation\chapters\ch08_value.md:84-97` |
| chapter 4 section 4.3 | whitened code on whale 0.83, 0.85, 0.97 vs 0.41, 0.80, 0.89 | `geometric-observation\chapters\ch08_value.md:84-97` |

## failures and corrections

none

## conditions

- Rescaling data so that its covariance becomes the identity. In the covariance's eigenbasis each coordinate is divided by the square root of its eigenvalue, each whitened coordinate then has unit variance, and the squared length of a whitened row is the Mahalanobis form.
- Whitening is a change of reader, not a change of data. The whitened code won at every budget on the whale corpus because the consumer read the whitened directions, and the same code under a different consumer has no such guarantee.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Whitening.lean`, theorems `whiten_unit_variance`, `whiten_sq_sum`, at observation-data-mining 8d458b2.

## used in

*Data Mining as Observation* chapters 0, 2, 4, 10.

## related

mahalanobis-distance, identity-reader, read-operator, water-filling

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 429cc9d, theory-radar 37c4e6c, observation-data-mining 8d458b2, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
