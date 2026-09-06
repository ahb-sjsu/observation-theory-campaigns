# nuisance

**id.** nuisance
**kind.** concept

## definition

The directions of the data a consumer cannot distinguish, the kernel of its read operator. Chapter 1.

## equation

Book equation 0.12a.

    x\sim_C x'\quad\Longleftrightarrow\quad d_G\big(C(x),C(x')\big)=0.

Book equation 0.12b.

    x\sim_{\bar P_{C,\mu}} x'\quad\Longleftrightarrow\quad x-x'\in\ker\bar P_{C,\mu}.

## ledger

- GO-1. The consumer's invariant/nuisance split is identifiable ex ante from the consumer functional. `[predicted]`. `geometric-observation/claims/LEDGER.md:62` at 9f3829f.
- NEG-6. Relative per-channel-demeaned error norm is the quotient-tangential quantity that controls softmax-KL. `[refuted]`. `geometric-observation/claims/LEDGER.md:99` at 9f3829f.
- NEG-7. Per-channel quantization is universally the invariant-preserving arm for softmax-key attention (a compressor property). `[refuted]`. `geometric-observation/claims/LEDGER.md:100` at 9f3829f.

## first stated

Volume 14, chapter 5, `geometric-observation/chapters/ch05_the_read_metric_and_the_quotient.md:7-48`, DOI 10.5281/zenodo.21776291, where the nuisance is the kernel of the read operator.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.2 | read subspace small, operator local, pullback composition, rank cannot increase | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:7-48`; `geometric-observation\chapters\ch06_mathematical_preliminaries.md:10-27` |
| chapter 2 section 2.2 | read distortion controls but is not a complete rank statistic, twelve of twelve, one middle pair misordered, NEG-9 | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:49-75` |
| chapter 6 section 6.2 | planted probe, overlap 0.936 vs 0.059, twelve of twelve, reconstruction 0.40, five of five | `geometric-observation\claims\LEDGER.md` row GO-1 |
| chapter 11 section 11.7 | GO-1 overlap 0.936 vs 0.059, flip 12 of 12, reconstruction 0.40 | `geometric-observation\claims\LEDGER.md` row GO-1; `geometric-observation\chapters\ch10_the_blind_probe.md:34-52` |

## failures and corrections

- NEG-6, `[refuted]`. Relative per-channel-demeaned error norm is the quotient-tangential quantity that controls softmax-KL.
- NEG-7, `[refuted]`. Per-channel quantization is universally the invariant-preserving arm for softmax-key attention (a compressor property).

## conditions

- The nuisance is the kernel of the workload-averaged read operator, the set of directions unread at almost every row of that workload, since the kernel of the average is the intersection of the local kernels.
- For a nonlinear consumer a null direction can turn with the row, so the nuisance of the average is not a global equivalence of inputs, and cosine similarity's radial direction is the case.
- A transform is safe when the reader it produces still resolves the read subspace, and discretization is safe only when the values it merges differ in nuisance directions.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ReadOperator.lean`, theorems `rank_one_reads_one_direction`, `readOp_mulVec`, `quad_readOp`, `quad_readOp_nonneg`, `readOp_mulVec_eq_zero_iff`, `readOp_diag`, `readOp_offdiag`, `readOp_symm`, `readOp_neg`, `affine_const_along_nuisance`, `readOp_affine`, `readOp_sqLength_basis`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 1, 2, 3, 6, 9, 11, 12, 13.

## related

read-subspace, read-operator, quotient, identity-reader

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
