# DBSCAN

**id.** dbscan
**kind.** instrument

## definition

A clustering that calls a point a core point when at least a minimum number of points lie within a radius, grows clusters by reachability from core points, and leaves the rest as noise. Chapter 9.

## equation

Book equation 9.1.

    \mathrm{SSE}=\sum_{k=1}^{K}\sum_{i\in\mathcal C_k}\|x_i-c_k\|^{2},\qquad\text{the }P_C=I\text{ distortion summed within clusters}.

Book equation 0.19.

    L=I-D^{-1/2}AD^{-1/2},\qquad D=\operatorname{diag}(d_1,\dots,d_n),\qquad L\,u_k=\lambda_k u_k,\ \ 0=\lambda_1\le\lambda_2\le\cdots.

Book equation 10.3.

    N_k(x\mid Q)=\big|\{q\in Q:\ x\in\operatorname{top}_k(q)\}\big|,\qquad \text{anti-hub}:\ N_k(x)=0.

## ledger

- NEG-11. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain. `[refuted]`. `geometric-observation/claims/LEDGER.md:104` at 9f3829f.

## first stated

Ester, Kriegel, Sander, and Xu, a density-based algorithm for discovering clusters, 1996, as chapter 9 section 9.1 of *Data Mining as Observation* reads it.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 9 section 9.1 | the geodesic-rank reader discards the radius, row normalization is the angular projection | `geometric-observation\chapters\ch09_legibility.md:10-41`; `the-angular-observer\theorem.md:110-146` |
| chapter 10 section 10.1 | the four detector families | TSK 2e chapter 9 |

## failures and corrections

- NEG-11, `[refuted]`. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain.

## conditions

- A clustering that calls a point a core point when at least a minimum number of points lie within a radius, grows a cluster by reachability from core points, and leaves the rest as noise. A wider radius or a smaller count makes more core points, every reachability chain starts at a core point, and a point that is not a core point reaches nothing.
- Its read subspace is the density coordinate, the one the geodesic reader of a spectral embedding discards, so two clustering consumers of one embedding read complementary coordinates.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Dbscan.lean`, theorems `ball_mono`, `core_mono`, `core_anti`, `reach_from_core`, `noise_unreachable`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 9, 10.

## related

density, k-means, hierarchical-clustering, spectral-clustering, outlier

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
