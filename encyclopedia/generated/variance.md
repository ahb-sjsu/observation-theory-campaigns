# variance

**id.** variance
**kind.** concept

## definition

The mean squared deviation of a column from its mean, the identity reader's measure of spread. Chapter 0 section 0.3.

## equation

Book equation 0.5.

    \Sigma\,v_i=\lambda_i v_i,\qquad \Sigma=\sum_{i=1}^{d}\lambda_i\,v_i v_i^{\top},\qquad v_i\cdot v_j=0\ (i\ne j).

Book equation 0.7.

    r_{\mathrm{eff}}=\frac{\big(\sum_i\lambda_i\big)^{2}}{\sum_i\lambda_i^{2}}.

Book equation 9.1.

    \mathrm{SSE}=\sum_{k=1}^{K}\sum_{i\in\mathcal C_k}\|x_i-c_k\|^{2},\qquad\text{the }P_C=I\text{ distortion summed within clusters}.

## ledger

- OT-7. The damage form, trace pairing, rank, and loading covariance are GL(d)-invariant under `P' = A⁻ᵀPA⁻¹`, while spectrum, effective rank, principal angles, and water-filling are O(d)-only — consumer-weighted damage is a geometric scalar, and P3's cliff cannot be bought down by reparameterization. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:30` at 9f3829f.

## first stated

Chapter 0 section 0.3 of *Data Mining as Observation*, with the program's spectrum tools in `readscope/readscope/spectrum.py:35-70`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 4 section 4.2 | effective rank as participation ratio, energy rank | `readscope\readscope\spectrum.py:35-70` |
| chapter 9 section 9.4 | explained ratios, effective rank 5.19 of 8, convergence with a second method, property of the representation not the space | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:10-18` |

## failures and corrections

none

## conditions

- The weighted mean of the squared deviation of a column from its weighted mean. It is nonnegative, equals the mean square less the squared mean, is zero for a constant column, scales with the square of a rescaling, and with positive weights is zero only for a constant column.
- Variance is the identity reader's measure of spread. A direction with large variance and no group structure pulls principal components and k-means centres alike, and whether a consumer reads that direction is a separate question.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Variance.lean`, theorems `variance_nonneg`, `variance_eq`, `variance_const`, `variance_smul`, `eq_mean_of_variance_eq_zero`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 14.

## related

covariance-matrix, explained-variance, standardization, spectrum, effective-rank

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
