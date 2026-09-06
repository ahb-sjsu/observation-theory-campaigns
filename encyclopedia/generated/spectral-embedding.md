# spectral embedding

**id.** spectral-embedding
**kind.** instrument

## definition

The coordinates a node receives from its values in the first few nontrivial eigenvectors of the graph Laplacian. Clustering those coordinates is spectral clustering. Chapter 3.

## equation

Book equation 0.19.

    L=I-D^{-1/2}AD^{-1/2},\qquad D=\operatorname{diag}(d_1,\dots,d_n),\qquad L\,u_k=\lambda_k u_k,\ \ 0=\lambda_1\le\lambda_2\le\cdots.

Book equation 0.20.

    \Psi_i=\left(\frac{u_k(i)}{\sqrt{\lambda_k\,d_i}}\right)_{k\ge2},\qquad \|\Psi_i-\Psi_j\|^{2}=R(i,j)=\frac{C(i,j)}{\operatorname{vol}(G)}.

Book equation 3.3.

    X_i=r_i\,\theta_i,\qquad r_i\ \to\ \frac1{\sqrt{d_i}},\qquad \theta_i=\frac{X_i}{\|X_i\|}\in S^{m-1}.

## ledger

- NEG-1. Fixed-scale, uniform-in-m bi-Lipschitz for the commute filter. `[refuted]`. `geometric-observation/claims/LEDGER.md:94` at 8c6986b.

## first stated

Ng, Jordan, and Weiss, on spectral clustering, 2002, as chapter 3 section 3.3 of *Data Mining as Observation* reads it, with the program's angular reading in `the-angular-observer/theorem.md:110-146`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.3 | resistance converges to 1 over d_i plus 1 over d_j, simplex argument, radius converges to 1 over root d_i | `the-angular-observer\theorem.md:110-146` |
| chapter 3 section 3.3 | row normalization is the projection onto the read subspace of the geodesic-rank consumer | `geometric-observation\chapters\ch09_legibility.md:31-41`; `geometric-observation\chapters\ch03_historical_precursors.md:98-110` |
| chapter 9 section 9.1 | the geodesic-rank reader discards the radius, row normalization is the angular projection | `geometric-observation\chapters\ch09_legibility.md:10-41`; `the-angular-observer\theorem.md:110-146` |

## failures and corrections

- NEG-1, `[refuted]`. Fixed-scale, uniform-in-m bi-Lipschitz for the commute filter.

## conditions

- The coordinates a node receives from its values in the first few nontrivial eigenvectors of the graph Laplacian. Row normalization puts every embedded row on the unit sphere, leaves the cosine between rows unchanged, and ignores a positive rescaling of a row, so it is the projection onto the read subspace of the geodesic-rank consumer.
- Its magnitude converges to degree noise and its angle keeps the geodesics, so the cosine between embedded rows is the right similarity and the Euclidean distance the wrong one. Clustering the normalized coordinates is spectral clustering, and a density reader of the same embedding reads the complementary coordinate.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/SpectralEmbedding.lean`, theorems `dot_self_nonneg`, `rowNormalize_unit`, `dot_rowNormalize`, `rowNormalize_smul`, at observation-data-mining 17f3e9f.

`lean/DataMiningAsObservation/Laplacian.lean`, theorems `quad_eq`, `quad_nonneg`, `quad_const`, `quad_pos_of_edge`, at observation-data-mining 17f3e9f.

## used in

*Data Mining as Observation* chapters 0, 3, 9.

## related

laplacian, commute-time, geodesic-distance, degree, recognizer

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 8c6986b, observation-theory-campaigns 553a902, theory-radar 37c4e6c, observation-data-mining 17f3e9f, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
