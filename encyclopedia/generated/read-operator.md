# read operator

**id.** read-operator
**kind.** concept

![The averaged outer product of the sensitivity with itself.](../figures/read-operator.svg)

## definition

The average outer product of a consumer's sensitivity over a dataset, an average of local linearizations whose kernel is the set of directions unread at almost every row of the workload. Its range is the read subspace and its kernel is the nuisance. Equations 0.9 and 0.11.

**Example.** The affine consumer 3x1 + 4x2 has read operator with rows (9, 12) and (12, 16) at every row.

**Known as, or related to prior art.** In the scalar Euclidean-output case the read operator is the active-subspace matrix of Constantine and Gleich, the covariance of the gradient. What the program adds is the pullback through the output metric, the observer triple, the budget, and the audit discipline.

## equation

Book equation 0.9.

    P_C=\mathbb E\!\left[g\,g^{\top}\right],\qquad g=\nabla C(x).

Book equation 0.11.

    P_C(x)=J(x)^{\top}G\big(C(x)\big)\,J(x),\qquad J(x)=\frac{\partial C}{\partial x}(x),\qquad \bar P_{C,\mu}=\mathbb E_{\mu}\!\left[P_C(x)\right].

Book equation 2.1.

    P_{C_2\circ C_1}(x)=J_1(x)^{\top}\,P_{C_2}\big(C_1(x)\big)\,J_1(x),\qquad \operatorname{rank}P_{C_2\circ C_1}(x)\le\operatorname{rank}P_{C_2}\big(C_1(x)\big)\quad\text{at each row } x.

Book equation 6.1.

    s(x)=w\cdot x+b,\qquad P_C=\mathbb E\big[\sigma'(s)^{2}\big]\,w\,w^{\top},\qquad \operatorname{rank}P_C=1.

## conditions

- Each local operator is positive semidefinite, so the kernel of the workload average is the intersection of the local kernels up to sets of rows of measure zero, and an average-null direction is locally unread at almost every row of that workload.
- The average depends on the workload it was taken over and is written with that workload where the difference matters.
- Its off-diagonal entries are co-sensitivities, how two features' sensitivities vary together across rows, and not interactions, which are cross-partials and live in the Hessian.
- The metric in the vector-output form is the local geometry of the output metric where that metric has a local quadratic representation. A dataset-level loss has none, and the operator is then taken on the score with the identity geometry.

Conditions are curated in `entries.toml` rather than read from a record.

## ledger

- *measures.* GO-EC-3 `[predicted]`. A read operator recovered from a black-box consumer by query-only finite-difference probing, composed with the Kalman covariance as tr(P̂_C Σ), prospectively selects sensors that improve the held-out consumer at matched budgets with probe … [`geometric-observation/claims/LEDGER.md:162`](https://github.com/ahb-sjsu/geometric-observation/blob/0792c84/claims/LEDGER.md#L162).

## first stated

Volume 14, chapters 4 and 5, `geometric-observation/chapters/ch04_the_observer_triple.md:9-60` and `geometric-observation/chapters/ch05_the_read_metric_and_the_quotient.md:7-48`, DOI 10.5281/zenodo.21776291.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.2 | the observer triple, read subspace, nuisance, same read operator means same read geometry | [`geometric-observation/chapters/ch04_the_observer_triple.md:9-60`](https://github.com/ahb-sjsu/geometric-observation/blob/0792c84/chapters/ch04_the_observer_triple.md#L9-L60); [`geometric-observation/OBSERVATION.md:1-10`](https://github.com/ahb-sjsu/geometric-observation/blob/0792c84/OBSERVATION.md#L1-L10) |

## failures and corrections

- [`geometric-observation/chapters/ch05_the_read_metric_and_the_quotient.md:42-47`](https://github.com/ahb-sjsu/geometric-observation/blob/0792c84/chapters/ch05_the_read_metric_and_the_quotient.md#L42-L47) at 0792c84. **Operating-point dependence.** $P_C$ is a *local* object — it depends on $x_0$ through $J$. For a linear consumer it is global; for a nonlinear one it varies over $X$, and the honest version of every result carries $P_C$ as a field, not a constant. The blind probe of Chapter 10 recovers $P_C$ *at* an operating point precisely because it is local; averaging it over a data distribution gives the $\bar P_C$ that enters the alignment law $\kappa$ (Chapter 12).

## invariance envelope

none declared


## machine checked

[`lean/DataMiningAsObservation/ReadOperator.lean`](https://github.com/ahb-sjsu/observation-data-mining/blob/95af30c/lean/DataMiningAsObservation/ReadOperator.lean), theorems `rank_one_reads_one_direction`, `readOp_mulVec`, `quad_readOp`, `quad_readOp_nonneg`, `readOp_mulVec_eq_zero_iff`, `readOp_diag`, `readOp_offdiag`, `readOp_symm`, `readOp_neg`, `affine_const_along_nuisance`, `readOp_affine`, `readOp_sqLength_basis`, at observation-data-mining 95af30c; what the check covers is stated in the book's [appendix C](https://github.com/ahb-sjsu/observation-data-mining/blob/95af30c/chapters/machine_checked.md).

## used in

*Data Mining as Observation* chapters 0, 1, 2, 4, 6, 7, 8, 11, 12, 13, 14.

## related

read-distortion, quotient, identity-reader, blind-probe, flip

## see also

Ledger rows that cite the entry's records without naming it: OT-7, GO-1.

Sources-table rows that share a record with the entry without naming it: chapter 2 section 2.2, chapter 2 section 2.3, chapter 6 section 6.1, chapter 6 section 6.2, chapter 11 section 11.7.

## status

Generated 2026-09-08 by `encyclopedia/generate.py`; book at observation-data-mining 95af30c; the commit of every record is listed in the encyclopedia's provenance.
