# kernel

**id.** kernel
**kind.** concept

## definition

The directions a matrix sends to zero. The kernel of the read operator is the nuisance. Chapter 0 section 0.5.

## equation

Book equation 0.9.

    P_C=\mathbb E\!\left[g\,g^{\top}\right],\qquad g=\nabla C(x).

Book equation 0.12a.

    x\sim_C x'\quad\Longleftrightarrow\quad d_G\big(C(x),C(x')\big)=0.

Book equation 0.12b.

    x\sim_{\bar P_{C,\mu}} x'\quad\Longleftrightarrow\quad x-x'\in\ker\bar P_{C,\mu}.

## ledger

- OT-7. The damage form, trace pairing, rank, and loading covariance are GL(d)-invariant under `P' = A⁻ᵀPA⁻¹`, while spectrum, effective rank, principal angles, and water-filling are O(d)-only — consumer-weighted damage is a geometric scalar, and P3's cliff cannot be bought down by reparameterization. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:30` at 9f3829f.
- GO-6. At matched rate, output coding ≤ surrogate ≤ reconstruction on the consumer metric; the output–reconstruction gap is governed by the $\ker P_C$ entropy share, and the surrogate–output gap vanishes as rate grows. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:68` at 9f3829f.

## first stated

Chapter 0 section 0.5 and section 0.6 of *Data Mining as Observation*, with the kernel entropy share in `geometric-observation/claims/LEDGER.md` row GO-6.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.2 | read subspace small, operator local, pullback composition, rank cannot increase | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:7-48`; `geometric-observation\chapters\ch06_mathematical_preliminaries.md:10-27` |
| chapter 4 section 4.2 | GO-6, d 8 and r 4, output at or below surrogate at or below reconstruction at every rate, about 500 times, gap 0.41 to 0.005, isotropic control collapses | `geometric-observation\claims\LEDGER.md` row GO-6; `geometric-observation\chapters\ch07_cost.md` |

## failures and corrections

none

## conditions

- The directions a matrix sends to zero. The kernel of the read operator is the nuisance, the directions the consumer never reads, and a direction is in it exactly when every row's sensitivity is orthogonal to it. The kernel's dimension is the dimension less the rank.
- The reconstruction coder spends bits on the kernel and the output coder does not, and the gap between them is governed by the share of the error's entropy that lies in the kernel.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ReadOperator.lean`, theorems `rank_one_reads_one_direction`, `readOp_mulVec`, `quad_readOp`, `quad_readOp_nonneg`, `readOp_mulVec_eq_zero_iff`, `readOp_diag`, `readOp_offdiag`, `readOp_symm`, `readOp_neg`, `affine_const_along_nuisance`, `readOp_affine`, `readOp_sqLength_basis`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/Rank.lean`, theorems `rank_le_width`, `rank_le_height`, `rank_outer_le_one`, `rank_mul_le`, `rank_zero`, `rank_transpose`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 4, 6, 11.

## related

nuisance, read-operator, read-subspace, quotient, rank

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
