# quotient

**id.** quotient
**kind.** concept

## definition

The space of data with a set of transformations declared not to matter, so that two rows differing only by such a transformation are the same point. Every distance is a distance on some quotient. Equation 0.12.

## equation

Book equation 0.12a.

    x\sim_C x'\quad\Longleftrightarrow\quad d_G\big(C(x),C(x')\big)=0.

Book equation 0.12b.

    x\sim_{\bar P_{C,\mu}} x'\quad\Longleftrightarrow\quad x-x'\in\ker\bar P_{C,\mu}.

## ledger

- GO-1. The consumer's invariant/nuisance split is identifiable ex ante from the consumer functional. `[predicted]`. `geometric-observation/claims/LEDGER.md:62` at 9f3829f.
- GO-5. An α=1 density/hubness quotient restores invariant fidelity in ≥1 non-spectral domain. `[refuted]`. `geometric-observation/claims/LEDGER.md:67` at 9f3829f.
- NEG-6. Relative per-channel-demeaned error norm is the quotient-tangential quantity that controls softmax-KL. `[refuted]`. `geometric-observation/claims/LEDGER.md:99` at 9f3829f.

## first stated

Volume 14, chapter 5, `geometric-observation/chapters/ch05_the_read_metric_and_the_quotient.md:78-90`, DOI 10.5281/zenodo.21776291, and chapter 3 section 3.1 of *Data Mining as Observation*, where every similarity measure induces a distance on some quotient.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.2 | read subspace small, operator local, pullback composition, rank cannot increase | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:7-48`; `geometric-observation\chapters\ch06_mathematical_preliminaries.md:10-27` |
| chapter 2 section 2.2 | read distortion controls but is not a complete rank statistic, twelve of twelve, one middle pair misordered, NEG-9 | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:49-75` |
| chapter 3 section 3.6 | GO-5 refuted in four attempts, under 2 percent, control 0.015 vs 0.019, alpha hurts in direct and quantized retrieval, NEG-11 | `geometric-observation\claims\LEDGER.md` rows GO-5 and NEG-11; `geometric-observation\experiments\GO5-diffusion-distance-NOTES.md` |
| chapter 6 section 6.2 | planted probe, overlap 0.936 vs 0.059, twelve of twelve, reconstruction 0.40, five of five | `geometric-observation\claims\LEDGER.md` row GO-1 |
| chapter 11 section 11.7 | GO-1 overlap 0.936 vs 0.059, flip 12 of 12, reconstruction 0.40 | `geometric-observation\claims\LEDGER.md` row GO-1; `geometric-observation\chapters\ch10_the_blind_probe.md:34-52` |

## failures and corrections

- GO-5, `[refuted]`. An α=1 density/hubness quotient restores invariant fidelity in ≥1 non-spectral domain.
- NEG-6, `[refuted]`. Relative per-channel-demeaned error norm is the quotient-tangential quantity that controls softmax-KL.

## conditions

- The equivalence x related to x' when their difference lies in the kernel of the read operator is exact for an affine consumer with a fixed output geometry.
- Three things are kept apart. Exact equivalence, that the consumer's outputs agree under its output metric. A local null direction, in the kernel of the operator at one row. A workload-common null direction, in the kernel of the workload average, unread at almost every row. For a nonlinear consumer the third does not deliver the first, and cosine similarity is the case, whose radial direction turns with the row.
- An invertible transform identifies no two rows and forms no quotient. It changes the geometry a reader sees. Discretization changes the quotient.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ReadOperator.lean`, theorems `rank_one_reads_one_direction`, `readOp_mulVec`, `quad_readOp`, `quad_readOp_nonneg`, `readOp_mulVec_eq_zero_iff`, `readOp_diag`, `readOp_offdiag`, `readOp_symm`, `readOp_neg`, `affine_const_along_nuisance`, `readOp_affine`, `readOp_sqLength_basis`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 5, 6, 8, 9, 11, 12.

## related

read-operator, identity-reader, flip, hubness

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
