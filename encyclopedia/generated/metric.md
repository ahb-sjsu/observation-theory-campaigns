# metric

**id.** metric
**kind.** concept

## definition

A rule for the distance between two rows or two outputs. A distance is a choice of what to ignore, and a local metric on an output is a positive semidefinite matrix. Chapter 3 section 3.1 and chapter 0 section 0.5.

## equation

Book equation 3.1.

    \begin{gathered} d_O(u)=u^{\top}\Sigma\,u, \qquad u=(\cos15^\circ,\ \sin15^\circ), \\ \Sigma_1=\operatorname{diag}(0.3,1.7),\ \Sigma_2=\operatorname{diag}(1.7,0.3), \qquad d_O=0.394\ \text{vs}\ 1.606. \end{gathered}

Book equation 0.11.

    P_C(x)=J(x)^{\top}G\big(C(x)\big)\,J(x),\qquad J(x)=\frac{\partial C}{\partial x}(x),\qquad \bar P_{C,\mu}=\mathbb E_{\mu}\!\left[P_C(x)\right].

Book equation 1.1.

    O=(C,\ G,\ B).

## ledger

- GO-EC-3. A read operator recovered from a black-box consumer by query-only finite-difference probing, composed with the Kalman covariance as tr(P̂_C Σ), prospectively selects sensors that improve the held-out consumer at matched budgets with probe cost charged — capturing 94.6% of the known analytic optimum's gain on the positive-control arm (gate ≥ 75%) and improving 16.3% over the best consumer-agnostic policy on non-analytic consumers (gate ≥ 8%), with trace-matched ordering carried by the composition at 86.9% over 61 pairs (gate ≥ 65%). `[predicted]`. `geometric-observation/claims/LEDGER.md:162` at 9f3829f.

## first stated

Chapter 3 section 3.1 and chapter 0 section 0.5 of *Data Mining as Observation*, with the read metric in `geometric-observation/chapters/ch05_the_read_metric_and_the_quotient.md:7-48`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.2 | read subspace small, operator local, pullback composition, rank cannot increase | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:7-48`; `geometric-observation\chapters\ch06_mathematical_preliminaries.md:10-27` |
| chapter 3 section 3.2 | traces 2.0, diagonals 0.3 and 1.7, consumers at 15 and 75 degrees, distortion 0.39 vs 1.61, 4.1 to one, computed not drawn | `observation-theory\assets\make_flip_figure.py:4-24,107-119` |

## failures and corrections

none

## conditions

- A rule for the distance between two rows, or between two outputs. A distance function is a choice of what to ignore, and the local metric on a consumer's output is the positive semidefinite matrix that says how a small change is scored. The squared Euclidean distance is symmetric and zero exactly between equal rows.
- A dataset-level loss, accuracy, F1, or a rank correlation is not a local metric and cannot be inserted into the read-operator formula, and the same two codes get opposite verdicts from two metrics.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/EuclideanDistance.lean`, theorems `distSq_eq_quad_one`, `distSq_comm`, `distSq_eq_zero_iff`, `ranking_flips`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/OutputMetric.lean`, theorems `neg_reverses`, `readOp_of_neg`, `cost_flips`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14.

## related

output-metric, euclidean-distance, read-operator, quotient, geodesic-distance

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
