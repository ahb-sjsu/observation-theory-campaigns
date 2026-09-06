# sum of squared errors

**id.** sum-of-squared-errors
**kind.** concept

## definition

The sum over rows of the squared distance to the row's cluster centre, the validity index k-means minimizes. Chapter 0 section 0.15.

## equation

Book equation 9.1.

    \mathrm{SSE}=\sum_{k=1}^{K}\sum_{i\in\mathcal C_k}\|x_i-c_k\|^{2},\qquad\text{the }P_C=I\text{ distortion summed within clusters}.

Book equation 0.30.

    \mathrm{SSE}=\sum_{k}\sum_{i\in\mathcal C_k}\|x_i-c_k\|^{2},\qquad s_i=\frac{b_i-a_i}{\max(a_i,b_i)}.

Book equation 4.2.

    D(b)=\sum_i s_i\sigma_i^{2}\,2^{-2b_i},\qquad s_i=v_i^{\top}P_C\,v_i,\qquad b_i^{\star}=\max\!\Big(0,\ \tfrac12\log_2\frac{s_i\sigma_i^{2}}{\theta}\Big),\qquad \sum_i b_i^{\star}=B,

## ledger

- GO-3. The certificate's vacuity threshold predicts where single-stage retrieval dies. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:65` at 9f3829f.

## first stated

Chapter 0 section 0.15 and chapter 9 section 9.1 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 9 section 9.4 | explained ratios, effective rank 5.19 of 8, convergence with a second method, property of the representation not the space | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:10-18` |
| chapter 10 section 10.1 | the four detector families | TSK 2e chapter 9 |

## failures and corrections

none

## conditions

- The sum over rows of the squared distance to the row's cluster centre, the validity index k-means minimizes. The error about any centre is the error about the mean plus the count times the squared distance between the two, so the mean minimizes it, and it is the identity reader's distortion summed within clusters.
- Two clusterings of the same rows with the same sum of squared errors can be read oppositely by a consumer that weighs directions unequally.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/KMeans.lean`, theorems `sse_decomposition`, `mean_minimizes`, `assign_nearest`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/ReconstructionError.lean`, theorems `recon_nonneg`, `recon_eq_zero_iff`, `recon_sum`, `recon_proj`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 9.

## related

k-means, validity-index, reconstruction-error, identity-reader, silhouette

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
