# Jacobian

**id.** jacobian
**kind.** concept

## definition

The matrix of partial derivatives of a vector-valued consumer, whose transpose times itself averages to the read operator. A discrete stage has none. Chapter 0 section 0.5 and chapter 12.

## equation

Book equation 0.9.

    P_C=\mathbb E\!\left[g\,g^{\top}\right],\qquad g=\nabla C(x).

Book equation 2.1.

    P_{C_2\circ C_1}(x)=J_1(x)^{\top}\,P_{C_2}\big(C_1(x)\big)\,J_1(x),\qquad \operatorname{rank}P_{C_2\circ C_1}(x)\le\operatorname{rank}P_{C_2}\big(C_1(x)\big)\quad\text{at each row } x.

Book equation 0.11.

    P_C(x)=J(x)^{\top}G\big(C(x)\big)\,J(x),\qquad J(x)=\frac{\partial C}{\partial x}(x),\qquad \bar P_{C,\mu}=\mathbb E_{\mu}\!\left[P_C(x)\right].

## ledger

- OT-7. The damage form, trace pairing, rank, and loading covariance are GL(d)-invariant under `P' = A⁻ᵀPA⁻¹`, while spectrum, effective rank, principal angles, and water-filling are O(d)-only — consumer-weighted damage is a geometric scalar, and P3's cliff cannot be bought down by reparameterization. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:30` at 9f3829f.

## first stated

Chapter 0 section 0.5 and chapter 2 section 2.2 of *Data Mining as Observation*, with the pullback composition and the rank bound in `geometric-observation/chapters/ch06_mathematical_preliminaries.md:10-27`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.2 | read subspace small, operator local, pullback composition, rank cannot increase | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:7-48`; `geometric-observation\chapters\ch06_mathematical_preliminaries.md:10-27` |
| chapter 12 section 12.2 | pullback composition and the rank bound | `geometric-observation\chapters\ch06_mathematical_preliminaries.md:10-27`; chapter 2 of this book |

## failures and corrections

none

## conditions

- The matrix of partial derivatives of a vector-valued consumer, whose transpose times itself averages to the read operator. Along a chain of stages the rank of the composed operator is at most the rank of either stage, and a stage that identifies two inputs identifies them for every stage after it.
- Chunking and indexing have no Jacobian, since a document goes to a set of pieces and a query to a candidate list, and what survives without a derivative is the statement about distinctions.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Pipeline.lean`, theorems `quotient_inherited`, `quotient_inherited_chain`, `rank_comp_le_first`, `rank_comp_le_second`, at observation-data-mining f05f3e7.

`lean/DataMiningAsObservation/ReadOperator.lean`, theorems `rank_one_reads_one_direction`, `readOp_mulVec`, `quad_readOp`, `quad_readOp_nonneg`, `readOp_mulVec_eq_zero_iff`, `readOp_diag`, `readOp_offdiag`, `readOp_symm`, `readOp_neg`, `affine_const_along_nuisance`, `readOp_affine`, `readOp_sqLength_basis`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 0, 2, 12.

## related

read-operator, pipeline, sensitivity, hessian, retrieval-augmented-pipeline

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
