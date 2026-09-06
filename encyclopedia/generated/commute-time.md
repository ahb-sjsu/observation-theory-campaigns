# commute time

**id.** commute-time
**kind.** concept

## definition

The expected number of steps a random walk on a graph needs to go from one node to another and back. A particular scaling of the spectral embedding makes Euclidean distance equal it. Equation 0.20.

## equation

Book equation 0.20.

    \Psi_i=\left(\frac{u_k(i)}{\sqrt{\lambda_k\,d_i}}\right)_{k\ge2},\qquad \|\Psi_i-\Psi_j\|^{2}=R(i,j)=\frac{C(i,j)}{\operatorname{vol}(G)}.

Book equation 0.19.

    L=I-D^{-1/2}AD^{-1/2},\qquad D=\operatorname{diag}(d_1,\dots,d_n),\qquad L\,u_k=\lambda_k u_k,\ \ 0=\lambda_1\le\lambda_2\le\cdots.

Book equation 3.3.

    X_i=r_i\,\theta_i,\qquad r_i\ \to\ \frac1{\sqrt{d_i}},\qquad \theta_i=\frac{X_i}{\|X_i\|}\in S^{m-1}.

## ledger

- NEG-1. Fixed-scale, uniform-in-m bi-Lipschitz for the commute filter. `[refuted]`. `geometric-observation/claims/LEDGER.md:94` at 9f3829f.

## first stated

Chapter 0 section 0.10 of *Data Mining as Observation*, equation 0.20, with von Luxburg, Radl, and Hein, 2014, read in chapter 3 section 3.3 and the program's collapse proof in `the-angular-observer/theorem.md:110-146`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.3 | resistance converges to 1 over d_i plus 1 over d_j, simplex argument, radius converges to 1 over root d_i | `the-angular-observer\theorem.md:110-146` |
| chapter 3 section 3.3 | the self-refuted v0.8 claim, NEG-1 | `the-angular-observer\README.md:170-175`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-1 |
| chapter 9 section 9.1 | the geodesic-rank reader discards the radius, row normalization is the angular projection | `geometric-observation\chapters\ch09_legibility.md:10-41`; `the-angular-observer\theorem.md:110-146` |

## failures and corrections

- NEG-1, `[refuted]`. Fixed-scale, uniform-in-m bi-Lipschitz for the commute filter.

## conditions

- The expected number of steps a random walk on a graph needs to go from one node to another and back, the hitting time there plus the hitting time back, so it is symmetric and zero from a node to itself. Its scaling by the graph's volume is the resistance, and a particular scaling of the spectral embedding makes Euclidean distance equal it.
- On a large neighbourhood graph of a shape of dimension three or more the resistance converges to one over each degree, so it depends on two nodes only through their degrees and carries no geometry, which is why the magnitude of the spectral embedding is degree noise. The program's own first claim of a commute-metric form was self-refuted, NEG-1.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/CommuteTime.lean`, theorems `commute_symm`, `commute_self`, `resistance_symm`, `commute_eq_resistance_mul`, `collapsed_congr`, `collapsed_const`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 0, 3.

## related

spectral-embedding, laplacian, geodesic-distance, degree, graph

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
