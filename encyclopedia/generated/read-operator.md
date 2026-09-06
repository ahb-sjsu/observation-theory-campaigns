# read operator

**id.** read-operator
**kind.** concept

## definition

The average outer product of a consumer's sensitivity over a dataset, an average of local linearizations whose kernel is the set of directions unread at almost every row of the workload. Its range is the read subspace and its kernel is the nuisance. Equations 0.9 and 0.11.

## equation

Book equation 0.9.

    P_C=\mathbb E\!\left[g\,g^{\top}\right],\qquad g=\nabla C(x).

Book equation 0.11.

    P_C(x)=J(x)^{\top}G\big(C(x)\big)\,J(x),\qquad J(x)=\frac{\partial C}{\partial x}(x),\qquad \bar P_{C,\mu}=\mathbb E_{\mu}\!\left[P_C(x)\right].

Book equation 2.1.

    P_{C_2\circ C_1}(x)=J_1(x)^{\top}\,P_{C_2}\big(C_1(x)\big)\,J_1(x),\qquad \operatorname{rank}P_{C_2\circ C_1}(x)\le\operatorname{rank}P_{C_2}\big(C_1(x)\big)\quad\text{at each row } x.

Book equation 6.1.

    s(x)=w\cdot x+b,\qquad P_C=\mathbb E\big[\sigma'(s)^{2}\big]\,w\,w^{\top},\qquad \operatorname{rank}P_C=1.

## ledger

- OT-7. The damage form, trace pairing, rank, and loading covariance are GL(d)-invariant under `P' = A⁻ᵀPA⁻¹`, while spectrum, effective rank, principal angles, and water-filling are O(d)-only — consumer-weighted damage is a geometric scalar, and P3's cliff cannot be bought down by reparameterization. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:30` at 9f3829f.
- GO-1. The consumer's invariant/nuisance split is identifiable ex ante from the consumer functional. `[predicted]`. `geometric-observation/claims/LEDGER.md:62` at 9f3829f.
- GO-EC-3. A read operator recovered from a black-box consumer by query-only finite-difference probing, composed with the Kalman covariance as tr(P̂_C Σ), prospectively selects sensors that improve the held-out consumer at matched budgets with probe cost charged — capturing 94.6% of the known analytic optimum's gain on the positive-control arm (gate ≥ 75%) and improving 16.3% over the best consumer-agnostic policy on non-analytic consumers (gate ≥ 8%), with trace-matched ordering carried by the composition at 86.9% over 61 pairs (gate ≥ 65%). `[predicted]`. `geometric-observation/claims/LEDGER.md:162` at 9f3829f.

## first stated

Volume 14, chapters 4 and 5, `geometric-observation/chapters/ch04_the_observer_triple.md:9-60` and `geometric-observation/chapters/ch05_the_read_metric_and_the_quotient.md:7-48`, DOI 10.5281/zenodo.21776291.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.2 | the observer triple, read subspace, nuisance, same read operator means same read geometry | `geometric-observation\chapters\ch04_the_observer_triple.md:9-60`; `geometric-observation\OBSERVATION.md:1-10` |
| chapter 2 section 2.2 | read subspace small, operator local, pullback composition, rank cannot increase | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:7-48`; `geometric-observation\chapters\ch06_mathematical_preliminaries.md:10-27` |
| chapter 2 section 2.2 | read distortion controls but is not a complete rank statistic, twelve of twelve, one middle pair misordered, NEG-9 | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:49-75` |
| chapter 2 section 2.3 | refusal regimes, selection consumers read order, recurrences compound | `readscope\readscope\regimes.py:1-60` |
| chapter 6 section 6.1 | the classifier row of the consumer table, the output metric makes a different observer | `geometric-observation\chapters\ch04_the_observer_triple.md:60-135` |
| chapter 6 section 6.1 | selection consumers have zero sensitivity almost everywhere | `readscope\readscope\regimes.py:1-60` |
| chapter 6 section 6.2 | planted probe, overlap 0.936 vs 0.059, twelve of twelve, reconstruction 0.40, five of five | `geometric-observation\claims\LEDGER.md` row GO-1 |
| chapter 11 section 11.7 | GO-1 overlap 0.936 vs 0.059, flip 12 of 12, reconstruction 0.40 | `geometric-observation\claims\LEDGER.md` row GO-1; `geometric-observation\chapters\ch10_the_blind_probe.md:34-52` |

## failures and corrections

- `geometric-observation/chapters/ch05_the_read_metric_and_the_quotient.md:42-47` at 9f3829f. **Operating-point dependence.** $P_C$ is a *local* object — it depends on $x_0$ through $J$. For a linear consumer it is global; for a nonlinear one it varies over $X$, and the honest version of every result carries $P_C$ as a field, not a constant. The blind probe of Chapter 10 recovers $P_C$ *at* an operating point precisely because it is local; averaging it over a data distribution gives the $\bar P_C$ that enters the alignment law $\kappa$ (Chapter 12).

## conditions

- Each local operator is positive semidefinite, so the kernel of the workload average is the intersection of the local kernels up to sets of rows of measure zero, and an average-null direction is locally unread at almost every row of that workload.
- The average depends on the workload it was taken over and is written with that workload where the difference matters.
- Its off-diagonal entries are co-sensitivities, how two features' sensitivities vary together across rows, and not interactions, which are cross-partials and live in the Hessian.
- The metric in the vector-output form is the local geometry of the output metric where that metric has a local quadratic representation. A dataset-level loss has none, and the operator is then taken on the score with the identity geometry.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ReadOperator.lean`, theorems `rank_one_reads_one_direction`, `readOp_mulVec`, `quad_readOp`, `quad_readOp_nonneg`, `readOp_mulVec_eq_zero_iff`, `readOp_diag`, `readOp_offdiag`, `readOp_symm`, `readOp_neg`, `affine_const_along_nuisance`, `readOp_affine`, `readOp_sqLength_basis`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 4, 6, 7, 8, 11, 12, 13, 14.

## related

read-distortion, quotient, identity-reader, blind-probe, flip

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
