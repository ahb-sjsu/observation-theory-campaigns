# neighbourhood graph

**id.** neighbourhood-graph
**kind.** concept

## definition

A graph on a dataset that joins each row to its k nearest rows, or to every row within a radius. Chapter 0 section 0.10.

## equation

Book equation 0.19.

    L=I-D^{-1/2}AD^{-1/2},\qquad D=\operatorname{diag}(d_1,\dots,d_n),\qquad L\,u_k=\lambda_k u_k,\ \ 0=\lambda_1\le\lambda_2\le\cdots.

Book equation 0.20.

    \Psi_i=\left(\frac{u_k(i)}{\sqrt{\lambda_k\,d_i}}\right)_{k\ge2},\qquad \|\Psi_i-\Psi_j\|^{2}=R(i,j)=\frac{C(i,j)}{\operatorname{vol}(G)}.

Book equation 3.3.

    X_i=r_i\,\theta_i,\qquad r_i\ \to\ \frac1{\sqrt{d_i}},\qquad \theta_i=\frac{X_i}{\|X_i\|}\in S^{m-1}.

## ledger

- NEG-1. Fixed-scale, uniform-in-m bi-Lipschitz for the commute filter. `[refuted]`. `geometric-observation/claims/LEDGER.md:94` at 9f3829f.

## first stated

Chapter 0 section 0.10 of *Data Mining as Observation*, with the substrate table in `the-angular-observer/README.md:99-109`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.3 | resistance converges to 1 over d_i plus 1 over d_j, simplex argument, radius converges to 1 over root d_i | `the-angular-observer\theorem.md:110-146` |
| chapter 3 section 3.3 | substrate table | `the-angular-observer\README.md:99-109` |
| chapter 9 section 9.1 | the geodesic-rank reader discards the radius, row normalization is the angular projection | `geometric-observation\chapters\ch09_legibility.md:10-41`; `the-angular-observer\theorem.md:110-146` |
| chapter 9 section 9.2 | causal set 0.57 with dimension 2.9 to 10.7, small world 0.45, control 0.01, rung 4 decay 0.747 to 0.679 below 0.75 | `the-angular-observer\README.md:99-109`; `wolfram-observer-bridge\rung4_scaledm_result.json`; `wolfram-observer-bridge\review-2.txt` |

## failures and corrections

- NEG-1, `[refuted]`. Fixed-scale, uniform-in-m bi-Lipschitz for the commute filter.

## conditions

- A graph on a dataset that joins each row to its k nearest rows, or to every row within a radius. Every node of a k-nearest graph has out-degree k, the mutual neighbours of a node are at most k, and being mutual neighbours is symmetric.
- As the graph grows on a manifold its low Laplacian eigenvectors converge to the smoothest functions on the manifold, so the embedding becomes a picture of the manifold, and the hubs of the graph are a property of the queries that built it.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Graph.lean`, theorems `outDegree`, `mutual_symm`, `mutual_sub`, `mutualNbrs_card_le`, `mem_mutualNbrs`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 3, 9, 11.

## related

graph, degree, laplacian, spectral-embedding, geodesic-distance, hub

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
