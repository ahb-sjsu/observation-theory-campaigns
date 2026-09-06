# sensitivity

**id.** sensitivity
**kind.** concept

## definition

The vector of partial derivatives of a consumer with respect to each coordinate of its input, at one point. Equation 0.8.

## equation

Book equation 0.8.

    g_j\;\approx\;\frac{C(x+h\,e_j)-C(x-h\,e_j)}{2h},\qquad j=1,\dots,d.

Book equation 0.11.

    P_C(x)=J(x)^{\top}G\big(C(x)\big)\,J(x),\qquad J(x)=\frac{\partial C}{\partial x}(x),\qquad \bar P_{C,\mu}=\mathbb E_{\mu}\!\left[P_C(x)\right].

Book equation 14.4.

    \text{attribution}_j(x)\approx g_j(x)\,\delta_j,\qquad \overline{\text{importance}}_j\approx\big(P_C\big)_{jj}=\mathbb E\big[g_j^{2}\big].

## ledger

- NEG-14. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe). `[refuted]`. `geometric-observation/claims/LEDGER.md:108` at 7d91883.
- GO-EC-3. A read operator recovered from a black-box consumer by query-only finite-difference probing, composed with the Kalman covariance as tr(P̂_C Σ), prospectively selects sensors that improve the held-out consumer at matched budgets with probe cost charged — capturing 94.6% of the known analytic optimum's gain on the positive-control arm (gate ≥ 75%) and improving 16.3% over the best consumer-agnostic policy on non-analytic consumers (gate ≥ 8%), with trace-matched ordering carried by the composition at 86.9% over 61 pairs (gate ≥ 65%). `[predicted]`. `geometric-observation/claims/LEDGER.md:162` at 7d91883.

## first stated

Volume 14, chapter 5, `geometric-observation/chapters/ch05_the_read_metric_and_the_quotient.md:7-48`, DOI 10.5281/zenodo.21776291, as the gradient of the consumer at a row.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.2 | read subspace small, operator local, pullback composition, rank cannot increase | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:7-48`; `geometric-observation\chapters\ch06_mathematical_preliminaries.md:10-27` |
| chapter 2 section 2.2 | read distortion controls but is not a complete rank statistic, twelve of twelve, one middle pair misordered, NEG-9 | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:49-75` |
| chapter 2 section 2.3 | refusal regimes, selection consumers read order, recurrences compound | `readscope\readscope\regimes.py:1-60` |
| chapter 6 section 6.1 | selection consumers have zero sensitivity almost everywhere | `readscope\readscope\regimes.py:1-60` |

## failures and corrections

- NEG-14, `[refuted]`. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe).

## conditions

- The sensitivity of a consumer at a row is the vector of partial derivatives of its output with respect to each coordinate, measurable without the formula by a central finite difference at two calls per coordinate.
- The read operator is the workload average of the sensitivity's outer product, so its diagonal is the expected squared sensitivity to each feature and its off-diagonal entries are co-sensitivities, not interactions.
- A gradient-based attribution estimates the sensitivity. Permutation importance, partial dependence, and Shapley values measure other things.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ReadOperator.lean`, theorems `rank_one_reads_one_direction`, `readOp_mulVec`, `quad_readOp`, `quad_readOp_nonneg`, `readOp_mulVec_eq_zero_iff`, `readOp_diag`, `readOp_offdiag`, `readOp_symm`, `readOp_neg`, `affine_const_along_nuisance`, `readOp_affine`, `readOp_sqLength_basis`, at observation-data-mining 7eba709.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 4, 6, 7, 8, 11, 14.

## related

read-operator, consumer, blind-probe, read-subspace

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns f5585e7, theory-radar 37c4e6c, observation-data-mining 7eba709, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
