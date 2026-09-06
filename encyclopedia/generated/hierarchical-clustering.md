# hierarchical clustering

**id.** hierarchical-clustering
**kind.** instrument

## definition

A clustering that merges the closest pair of clusters at each step, under a linkage that reads the nearest pair, the farthest, or the average, so that merge heights never decrease. Chapter 9.

## equation

Book equation 9.1.

    \mathrm{SSE}=\sum_{k=1}^{K}\sum_{i\in\mathcal C_k}\|x_i-c_k\|^{2},\qquad\text{the }P_C=I\text{ distortion summed within clusters}.

Book equation 3.1.

    \begin{gathered} d_O(u)=u^{\top}\Sigma\,u, \qquad u=(\cos15^\circ,\ \sin15^\circ), \\ \Sigma_1=\operatorname{diag}(0.3,1.7),\ \Sigma_2=\operatorname{diag}(1.7,0.3), \qquad d_O=0.394\ \text{vs}\ 1.606. \end{gathered}

## ledger

none

## first stated

Chapter 9 section 9.1 of *Data Mining as Observation*, after TSK chapter 7.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 9 section 9.1 | the geodesic-rank reader discards the radius, row normalization is the angular projection | `geometric-observation\chapters\ch09_legibility.md:10-41`; `the-angular-observer\theorem.md:110-146` |
| chapter 10 section 10.1 | the four detector families | TSK 2e chapter 9 |

## failures and corrections

none

## conditions

- A clustering that merges the closest pair of clusters at each step under a linkage that reads the nearest pair, the farthest pair, or the average. When the merged pair was the closest at some height, no updated distance falls below it, so the merge heights never decrease, single linkage is never above complete, and average linkage lies between them.
- The dendrogram inherits the distance's quotient at every level, so the tree is a certificate about the chosen quotient and not about the data.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Hierarchical.lean`, theorems `single_ge`, `complete_ge`, `average_ge`, `single_le_complete`, `average_between`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 9.

## related

k-means, dbscan, euclidean-distance, validity-index, quotient

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
