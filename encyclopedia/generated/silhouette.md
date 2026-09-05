# silhouette

**id.** silhouette
**kind.** concept

## definition

For a row, the difference between its mean distance to the nearest other cluster and its mean distance to its own cluster, divided by the larger of the two. Equation 0.30.

## equation

Book equation 0.30.

    \mathrm{SSE}=\sum_{k}\sum_{i\in\mathcal C_k}\|x_i-c_k\|^{2},\qquad s_i=\frac{b_i-a_i}{\max(a_i,b_i)}.

Book equation 9.1.

    \mathrm{SSE}=\sum_{k=1}^{K}\sum_{i\in\mathcal C_k}\|x_i-c_k\|^{2},\qquad\text{the }P_C=I\text{ distortion summed within clusters}.

## ledger

none

## first stated

Rousseeuw, silhouettes, 1987, as TSK chapter 7 presents it and chapter 0 section 0.15 states it, and chapter 9 of *Data Mining as Observation*, where it is one validity index among those the recognizer replaces.

## measurements

none

## failures and corrections

none

## conditions

- For a row, the difference between its mean distance to the nearest other cluster and its mean distance to its own cluster, over the larger of the two. It lies between minus one and one, is positive exactly when the row is closer to its own cluster, and is unchanged when every distance is scaled by the same factor.
- It is computed under the identity reader on the distances it is given, so it validates a clustering for that reader and not for a consumer that reads other directions, which is why chapter 9 asks the recognizer to name the manifold instead.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Silhouette.lean`, theorems `silhouette_mem`, `silhouette_pos_iff`, `silhouette_scale`, `silhouette_self`, at observation-data-mining 43ea852.

## used in

*Data Mining as Observation* chapters 0, 9, 10.

## related

recognizer, vacuity-threshold, identity-reader, quotient

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns b331d4f, theory-radar 37c4e6c, observation-data-mining 43ea852, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
