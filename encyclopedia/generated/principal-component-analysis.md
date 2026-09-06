# principal component analysis

**id.** principal-component-analysis
**kind.** instrument

## definition

Projection of the data onto the eigenvectors of its covariance with the largest eigenvalues, the reduction that minimizes reconstruction error for the identity reader. Chapter 4.

## equation

Book equation 0.5.

    \Sigma\,v_i=\lambda_i v_i,\qquad \Sigma=\sum_{i=1}^{d}\lambda_i\,v_i v_i^{\top},\qquad v_i\cdot v_j=0\ (i\ne j).

Book equation 0.7.

    r_{\mathrm{eff}}=\frac{\big(\sum_i\lambda_i\big)^{2}}{\sum_i\lambda_i^{2}}.

Book equation 4.2.

    D(b)=\sum_i s_i\sigma_i^{2}\,2^{-2b_i},\qquad s_i=v_i^{\top}P_C\,v_i,\qquad b_i^{\star}=\max\!\Big(0,\ \tfrac12\log_2\frac{s_i\sigma_i^{2}}{\theta}\Big),\qquad \sum_i b_i^{\star}=B,

## ledger

- GO-1. The consumer's invariant/nuisance split is identifiable ex ante from the consumer functional. `[predicted]`. `geometric-observation/claims/LEDGER.md:62` at 8c6986b.
- GO-6. At matched rate, output coding ≤ surrogate ≤ reconstruction on the consumer metric; the output–reconstruction gap is governed by the $\ker P_C$ entropy share, and the surrogate–output gap vanishes as rate grows. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:68` at 8c6986b.

## first stated

Pearson, on lines and planes of closest fit, 1901, and Hotelling, 1933, as chapter 4 section 4.1 of *Data Mining as Observation* reads them, with the program's truncation record in `turboquant-pro/benchmarks/RESULTS_glove.md:1-40`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 4 section 4.2 | effective rank as participation ratio, energy rank | `readscope\readscope\spectrum.py:35-70` |
| chapter 4 section 4.5 | GloVe table, 73 percent at 64 components, 0.685 vs 0.862 and 0.866, 0.906 at matched bytes, 0.989 at 37 bytes, 768 to 256 keeps about 99 percent, the 95 percent rule | `turboquant-pro\benchmarks\RESULTS_glove.md:1-40` |
| chapter 4 section 4.5 | truncation claim reproducible, loses on compact sets | `turboquant-pro\CLAIMS.md:28-49` |
| chapter 11 section 11.5 | 9.6x at recall 0.999 CI-gated on GloVe 1.18M; 32x at 0.9993 on private 199k LaBSE, ties OPQ, beats RaBitQ, 20x build; 27.7x and 114x reported; PCA truncation loses on compact sets; 20x at 199k and 4x at 1M over OPQ; RaBitQ builds in under a second | `turboquant-pro\CLAIMS.md:28-49` |

## failures and corrections

none

## conditions

- Projection of the data onto the eigenvectors of its covariance with the largest eigenvalues. The variance along a unit direction lies between the smallest and the largest eigenvalue, a basis direction attains its own eigenvalue, and the error of keeping the first k components is the sum of the dropped eigenvalues.
- It is the reduction that minimizes reconstruction error for the identity reader, which weighs all directions equally, which is to say for no particular reader at all. At matched reconstruction the consumer-aware code beat it in twelve of twelve domains, and truncation loses on compact sets.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/PCA.lean`, theorems `varAlong_basis`, `varAlong_le`, `varAlong_ge`, `dropped_eq`, `dropped_nonneg`, at observation-data-mining 17f3e9f.

## used in

*Data Mining as Observation* chapters 0, 1, 4, 6, 12.

## related

covariance-matrix, explained-variance, effective-rank, projection, identity-reader, flip-the

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 8c6986b, observation-theory-campaigns 553a902, theory-radar 37c4e6c, observation-data-mining 17f3e9f, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
