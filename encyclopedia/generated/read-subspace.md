# read subspace

**id.** read-subspace
**kind.** concept

## definition

The directions of the data a consumer can distinguish, spanned by the eigenvectors of its read operator with nonzero eigenvalue. Chapter 0 section 0.5.

## equation

Book equation 0.9.

    P_C=\mathbb E\!\left[g\,g^{\top}\right],\qquad g=\nabla C(x).

Book equation 2.1.

    P_{C_2\circ C_1}(x)=J_1(x)^{\top}\,P_{C_2}\big(C_1(x)\big)\,J_1(x),\qquad \operatorname{rank}P_{C_2\circ C_1}(x)\le\operatorname{rank}P_{C_2}\big(C_1(x)\big)\quad\text{at each row } x.

Book equation 6.1.

    s(x)=w\cdot x+b,\qquad P_C=\mathbb E\big[\sigma'(s)^{2}\big]\,w\,w^{\top},\qquad \operatorname{rank}P_C=1.

## ledger

- OT-3. Under subspace-confined second-order transcripts, fewer than d directions cannot identify a hidden leading eigenspace (theorem, adaptive to d−2 / oblivious to d−1); a known k₀-dim exclusion moves the cliff to exactly d−k₀ and never softens it. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:31` at 7d91883.
- NEG-12. (Gate B, prospective, real LLM) On a trained frontier attention layer the blind probe recovers the read operator above the sealed bar *and* projection beats reconstruction. `[refuted]`. `geometric-observation/claims/LEDGER.md:105` at 7d91883.
- GO-B-Llama. Trained frontier LLM (Llama-3.2-3B), softmax-attention consumer — blind probe on real post-RoPE keys `[predicted]`. `geometric-observation/claims/LEDGER.md:115` at 7d91883.
- GO-B-Llama-rematch. Trained frontier LLM (Llama-3.2-3B), softmax-attention consumer — recon-matched dissociation on real post-RoPE keys `[predicted]`. `geometric-observation/claims/LEDGER.md:118` at 7d91883.
- GO-B-Llama-rematch. Trained frontier LLM (Llama-3.2-3B), softmax-attention consumer — recon-matched dissociation on real post-RoPE keys `[predicted]`. `geometric-observation/claims/LEDGER.md:118` at 7d91883.

## first stated

Volume 14, chapter 5, `geometric-observation/chapters/ch05_the_read_metric_and_the_quotient.md:7-48`, DOI 10.5281/zenodo.21776291, where the read subspace is the range of the read operator.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.2 | read subspace small, operator local, pullback composition, rank cannot increase | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:7-48`; `geometric-observation\chapters\ch06_mathematical_preliminaries.md:10-27` |
| chapter 2 section 2.2 | read distortion controls but is not a complete rank statistic, twelve of twelve, one middle pair misordered, NEG-9 | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:49-75` |
| chapter 6 section 6.2 | real model, median 0.567 vs bar 0.60, about 4.5 times chance, heads at 0.815 and 0.958, sixteen of sixteen both, two of three triggers, NEG-12, later rematch four of four | `geometric-observation\claims\LEDGER.md` rows GO-B-Llama and NEG-12; `geometric-observation\chapters\ch16_honest_negatives.md:73-81` |
| chapter 11 section 11.7 | confinement theorem, side information moves the cliff to d minus k0, noisy cliff proved then measured | `readscope\PRINCIPLES.md:112-142`; `geometric-observation\crucible\OT3-THEOREM.md`; `geometric-observation\crucible\OT3-NOISY-THEOREM.md` |

## failures and corrections

- NEG-12, `[refuted]`. (Gate B, prospective, real LLM) On a trained frontier attention layer the blind probe recovers the read operator above the sealed bar *and* projection beats reconstruction.

## conditions

- The read subspace is spanned by the eigenvectors of the read operator with nonzero eigenvalue, and it is small. A linear classifier reads one direction, an attention head a handful, and the input has hundreds or thousands.
- Pointwise, a scalar-output consumer reads one direction at each row, and the averaged operator can still have full rank, as the consumer that reads the squared length of a row shows.
- Recovering it from a black box costs two consumer calls per input dimension per row and is a cliff at the full dimension.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ReadOperator.lean`, theorems `rank_one_reads_one_direction`, `readOp_mulVec`, `quad_readOp`, `quad_readOp_nonneg`, `readOp_mulVec_eq_zero_iff`, `readOp_diag`, `readOp_offdiag`, `readOp_symm`, `readOp_neg`, `affine_const_along_nuisance`, `readOp_affine`, `readOp_sqLength_basis`, at observation-data-mining ea18182.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 6, 7, 9, 10, 11, 12, 13.

## related

nuisance, read-operator, blind-probe, budget-cliff

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 4a95b35, theory-radar 37c4e6c, observation-data-mining ea18182, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
