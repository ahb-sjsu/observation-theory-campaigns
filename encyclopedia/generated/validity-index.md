# validity index

**id.** validity-index
**kind.** concept

## definition

A score for a clustering computed without labels. Chapter 9.

## equation

Book equation 9.1.

    \mathrm{SSE}=\sum_{k=1}^{K}\sum_{i\in\mathcal C_k}\|x_i-c_k\|^{2},\qquad\text{the }P_C=I\text{ distortion summed within clusters}.

Book equation 0.30.

    \mathrm{SSE}=\sum_{k}\sum_{i\in\mathcal C_k}\|x_i-c_k\|^{2},\qquad s_i=\frac{b_i-a_i}{\max(a_i,b_i)}.

## ledger

- GO-3. The certificate's vacuity threshold predicts where single-stage retrieval dies. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:65` at 01e53bc.

## first stated

TSK chapter 7 on cluster validity, as chapter 9 section 9.1 of *Data Mining as Observation* reads it, an output metric that needs a null.

## measurements

none

## failures and corrections

none

## conditions

- A score for a clustering computed without labels. The silhouette is the case, in the interval from minus one to one, positive exactly when a row is closer to its own cluster, and unchanged by a common rescaling of the distances.
- A validity index is an output metric and needs a null, since it is computed under the identity reader on the distances it is given, which is why chapter 9 asks the recognizer to name the manifold or certify that none is present.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Silhouette.lean`, theorems `silhouette_mem`, `silhouette_pos_iff`, `silhouette_scale`, `silhouette_self`, at observation-data-mining 17f3e9f.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14.

## related

silhouette, recognizer, vacuity-threshold, null-model

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 01e53bc, observation-theory-campaigns 0c2e3f9, theory-radar 37c4e6c, observation-data-mining 17f3e9f, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
