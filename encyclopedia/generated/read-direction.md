# read direction

**id.** read-direction
**kind.** concept

## definition

An eigenvector of the read operator with a nonzero eigenvalue, a direction the consumer is sensitive to. Chapter 2 section 2.2.

## equation

Book equation 0.9.

    P_C=\mathbb E\!\left[g\,g^{\top}\right],\qquad g=\nabla C(x).

Book equation 6.1.

    s(x)=w\cdot x+b,\qquad P_C=\mathbb E\big[\sigma'(s)^{2}\big]\,w\,w^{\top},\qquad \operatorname{rank}P_C=1.

Book equation 4.2.

    D(b)=\sum_i s_i\sigma_i^{2}\,2^{-2b_i},\qquad s_i=v_i^{\top}P_C\,v_i,\qquad b_i^{\star}=\max\!\Big(0,\ \tfrac12\log_2\frac{s_i\sigma_i^{2}}{\theta}\Big),\qquad \sum_i b_i^{\star}=B,

## ledger

- GO-1. The consumer's invariant/nuisance split is identifiable ex ante from the consumer functional. `[predicted]`. `geometric-observation/claims/LEDGER.md:62` at 9f3829f.
- GO-2 (pos. half: consumer-projected covariance *controls*). Downstream preservation is controlled by the error covariance projected on the consumer's read subspace, tr(P_C·Σ_δ). `[replicated]`. `geometric-observation/claims/LEDGER.md:64` at 9f3829f.

## first stated

Chapter 2 section 2.2 and chapter 4 section 4.3 of *Data Mining as Observation*, with the control that destroys the read direction in `geometric-observation/chapters/ch08_value.md:40-70`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.4 | the flip sealed in twelve domains and three physics, held in at least five domains and all three | `geometric-observation\chapters\ch08_value.md:40-70`; `geometric-observation\claims\LEDGER.md` rows GO-2, GO-B-AV163, D3, 038 |
| chapter 4 section 4.3 | acoustic 148 of 201, 201 of 201, 152 of 201; seismic 13 of 17, 17 of 17, 13 of 17; whale 0.934 vs 0.883, 2 times, 300 of 300; at least 5 domains and 3 physics; battery prediction met | `geometric-observation\chapters\ch08_value.md:40-70`; `geometric-observation\claims\LEDGER.md` rows GO-B-AV163, D3, 038 |
| chapter 6 section 6.2 | planted probe, overlap 0.936 vs 0.059, twelve of twelve, reconstruction 0.40, five of five | `geometric-observation\claims\LEDGER.md` row GO-1 |
| chapter 6 section 6.2 | whale clan classifier, 8718 codas, 0.934 vs 0.883, reconstructs twice as well, 300 of 300 | `geometric-observation\chapters\ch08_value.md:40-70`; `geometric-observation\claims\LEDGER.md` row 038 |
| chapter 11 section 11.7 | GO-1 overlap 0.936 vs 0.059, flip 12 of 12, reconstruction 0.40 | `geometric-observation\claims\LEDGER.md` row GO-1; `geometric-observation\chapters\ch10_the_blind_probe.md:34-52` |

## failures and corrections

none

## conditions

- An eigenvector of the read operator with a nonzero eigenvalue, a direction the consumer is sensitive to. An affine consumer has exactly one, its weight vector, the projection onto a read direction is idempotent, and its residual is orthogonal to it.
- The code that puts the whole error on the read direction is the worst, the control that destroys the read direction is confirmed worst, and no code of a given total error can be read as more than the total.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ReadOperator.lean`, theorems `rank_one_reads_one_direction`, `readOp_mulVec`, `quad_readOp`, `quad_readOp_nonneg`, `readOp_mulVec_eq_zero_iff`, `readOp_diag`, `readOp_offdiag`, `readOp_symm`, `readOp_neg`, `affine_const_along_nuisance`, `readOp_affine`, `readOp_sqLength_basis`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/Projection.lean`, theorems `proj_proj`, `dot_sub_proj`, `proj_sq_le`, `proj_add_orth`, `proj_add`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 2, 3, 4, 6, 8, 11, 12.

## related

read-subspace, read-operator, sensitivity, nuisance, projection

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
