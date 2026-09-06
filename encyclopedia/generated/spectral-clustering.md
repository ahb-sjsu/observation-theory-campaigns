# spectral clustering

**id.** spectral-clustering
**kind.** instrument

## definition

Clustering the rows of the row-normalized spectral embedding, which reads the angle and discards the density. Chapter 3 section 3.3 and chapter 9.

## equation

Book equation 0.19.

    L=I-D^{-1/2}AD^{-1/2},\qquad D=\operatorname{diag}(d_1,\dots,d_n),\qquad L\,u_k=\lambda_k u_k,\ \ 0=\lambda_1\le\lambda_2\le\cdots.

Book equation 0.20.

    \Psi_i=\left(\frac{u_k(i)}{\sqrt{\lambda_k\,d_i}}\right)_{k\ge2},\qquad \|\Psi_i-\Psi_j\|^{2}=R(i,j)=\frac{C(i,j)}{\operatorname{vol}(G)}.

Book equation 3.3.

    X_i=r_i\,\theta_i,\qquad r_i\ \to\ \frac1{\sqrt{d_i}},\qquad \theta_i=\frac{X_i}{\|X_i\|}\in S^{m-1}.

## ledger

- GO-3. The certificate's vacuity threshold predicts where single-stage retrieval dies. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:65` at 9f3829f.
- NEG-1. Fixed-scale, uniform-in-m bi-Lipschitz for the commute filter. `[refuted]`. `geometric-observation/claims/LEDGER.md:94` at 9f3829f.

## first stated

Ng, Jordan, and Weiss, on spectral clustering, 2002, as chapter 3 section 3.3 and chapter 9 section 9.1 of *Data Mining as Observation* read it, with the angular reading in `the-angular-observer/theorem.md:110-146`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.3 | resistance converges to 1 over d_i plus 1 over d_j, simplex argument, radius converges to 1 over root d_i | `the-angular-observer\theorem.md:110-146` |
| chapter 9 section 9.1 | the geodesic-rank reader discards the radius, row normalization is the angular projection | `geometric-observation\chapters\ch09_legibility.md:10-41`; `the-angular-observer\theorem.md:110-146` |
| chapter 9 section 9.2 | the recognizer's mechanism, low multiplets and angular distances, dimension before shape by Weyl's law, refusal, the growth gotcha | `geometric-observation\chapters\ch11_the_recognizer.md:1-95` |

## failures and corrections

- NEG-1, `[refuted]`. Fixed-scale, uniform-in-m bi-Lipschitz for the commute filter.

## conditions

- Clustering the rows of the row-normalized spectral embedding, which reads the angle and discards the density. Row normalization puts every row on the unit sphere, keeps the cosine between rows, and ignores a positive rescaling, and the Laplacian's quadratic form is nonnegative, zero on constants, and positive across any edge.
- Ng, Jordan, and Weiss normalized because it improved results, and chapter 3 says why. The Euclidean distance in the embedding converges to degree noise and the angle keeps the geodesics.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/SpectralEmbedding.lean`, theorems `dot_self_nonneg`, `rowNormalize_unit`, `dot_rowNormalize`, `rowNormalize_smul`, at observation-data-mining 5bb2c0d.

`lean/DataMiningAsObservation/Laplacian.lean`, theorems `quad_eq`, `quad_nonneg`, `quad_const`, `quad_pos_of_edge`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 0, 3, 9.

## related

spectral-embedding, laplacian, k-means, recognizer, geodesic-distance

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
