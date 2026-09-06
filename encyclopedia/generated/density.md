# density

**id.** density
**kind.** concept

## definition

The local crowding of rows around a point, the coordinate the geodesic reader of a spectral embedding discards and DBSCAN and the density detector read. Chapter 3 section 3.3 and chapter 9.

## equation

Book equation 3.3.

    X_i=r_i\,\theta_i,\qquad r_i\ \to\ \frac1{\sqrt{d_i}},\qquad \theta_i=\frac{X_i}{\|X_i\|}\in S^{m-1}.

Book equation 0.19.

    L=I-D^{-1/2}AD^{-1/2},\qquad D=\operatorname{diag}(d_1,\dots,d_n),\qquad L\,u_k=\lambda_k u_k,\ \ 0=\lambda_1\le\lambda_2\le\cdots.

Book equation 9.1.

    \mathrm{SSE}=\sum_{k=1}^{K}\sum_{i\in\mathcal C_k}\|x_i-c_k\|^{2},\qquad\text{the }P_C=I\text{ distortion summed within clusters}.

## ledger

- NEG-1. Fixed-scale, uniform-in-m bi-Lipschitz for the commute filter. `[refuted]`. `geometric-observation/claims/LEDGER.md:94` at 9f3829f.
- NEG-11. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain. `[refuted]`. `geometric-observation/claims/LEDGER.md:104` at 9f3829f.

## first stated

Chapter 3 section 3.3 of *Data Mining as Observation*, with the radius-against-degree measurement in `the-angular-observer/README.md:135-139`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.3 | radius against degree correlation 0.92 to 0.99 | `the-angular-observer\README.md:135-139` |
| chapter 9 section 9.1 | the geodesic-rank reader discards the radius, row normalization is the angular projection | `geometric-observation\chapters\ch09_legibility.md:10-41`; `the-angular-observer\theorem.md:110-146` |
| chapter 10 section 10.1 | the four detector families | TSK 2e chapter 9 |

## failures and corrections

- NEG-1, `[refuted]`. Fixed-scale, uniform-in-m bi-Lipschitz for the commute filter.
- NEG-11, `[refuted]`. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain.

## conditions

- The local crowding of rows around a point, which on a neighbourhood graph is the degree. The radius of the spectral embedding converges to one over the square root of the degree, so the geodesic reader discards the density and DBSCAN and the density detector read it. A wider radius or a smaller count makes more core points, and the sum of degrees is twice the edge count.
- The radius-against-degree correlation was 0.92 to 0.99 across substrates, and the quotient that removed density to restore invariant fidelity was refuted four times, NEG-11.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Dbscan.lean`, theorems `ball_mono`, `core_mono`, `core_anti`, `reach_from_core`, `noise_unreachable`, at observation-data-mining 5bb2c0d.

`lean/DataMiningAsObservation/Degree.lean`, theorems `sum_degrees`, `degree_lt_card`, `sum_degrees_even`, `average_degree`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 3, 8, 9, 10, 11.

## related

degree, spectral-embedding, dbscan, geodesic-distance, hubness

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
