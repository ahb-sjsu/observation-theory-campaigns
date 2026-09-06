# observer

**id.** observer
**kind.** concept

## definition

A consumer, its output metric, and its budget, written as the triple in equation 1.1. Naming all three is what every later chapter checks.

## equation

Book equation 1.1.

    O=(C,\ G,\ B).

Book equation 0.9.

    P_C=\mathbb E\!\left[g\,g^{\top}\right],\qquad g=\nabla C(x).

Book equation 0.11.

    P_C(x)=J(x)^{\top}G\big(C(x)\big)\,J(x),\qquad J(x)=\frac{\partial C}{\partial x}(x),\qquad \bar P_{C,\mu}=\mathbb E_{\mu}\!\left[P_C(x)\right].

## ledger

- OT-7. The damage form, trace pairing, rank, and loading covariance are GL(d)-invariant under `P' = A⁻ᵀPA⁻¹`, while spectrum, effective rank, principal angles, and water-filling are O(d)-only — consumer-weighted damage is a geometric scalar, and P3's cliff cannot be bought down by reparameterization. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:30` at 9f3829f.
- GO-1. The consumer's invariant/nuisance split is identifiable ex ante from the consumer functional. `[predicted]`. `geometric-observation/claims/LEDGER.md:62` at 9f3829f.

## first stated

Volume 14, chapter 4, `geometric-observation/chapters/ch04_the_observer_triple.md:9-60`, and `geometric-observation/OBSERVATION.md:1-10`, DOI 10.5281/zenodo.21776291. Version 1.0 of the theory was declared on 2026-08-18 in `geometric-observation/crucible/DECLARATION-V1.md`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.2 | the observer triple, read subspace, nuisance, same read operator means same read geometry | `geometric-observation\chapters\ch04_the_observer_triple.md:9-60`; `geometric-observation\OBSERVATION.md:1-10` |
| chapter 1 section 1.2 | the consumer table | `geometric-observation\OBSERVATION.md:19-29` |
| chapter 1 section 1.3 | no-consumer is a precondition, coupling is a true null, every verdict budget-relative | `geometric-observation\OBSERVATION.md:31-40` |
| chapter 1 section 1.5 | the Bell boundary | `geometric-observation\OBSERVATION.md:35-40`; `geometric-observation\claims\LEDGER.md` row NEG-15 |
| chapter 1 section 1.5 | the six classes and the ledger rule | `geometric-observation\PROTOCOL.md:58-75`; `geometric-observation\OBSERVATION.md:43-45` |
| chapter 6 section 6.1 | the classifier row of the consumer table, the output metric makes a different observer | `geometric-observation\chapters\ch04_the_observer_triple.md:60-135` |
| chapter 8 section 8.8 | declaration drafted 2026-08-17, sealed 2026-08-18, one count corrected, G2 | `geometric-observation\crucible\DECLARATION-V1.md:1-20`; `geometric-observation\crucible\OT-CRUCIBLE-4.md:31-35` |
| chapter 8 section 8.10 | the six classes | `geometric-observation\PROTOCOL.md:58-75` |
| chapter 11 section 11.7 | C-15 equal budget, 3072 observations, medians 0.02, 0.11, 0.05, 0.04, 1.0, 1.0, margin 0.883 vs 0.3, 0.062 to 0.057 at 8x | `readscope\SPEC.md:285-323`, record `readscope\calibration\records\c15-budget-surface.json`, `readscope\calibration\DECLARATION-C15.md` |
| chapter 11 section 11.9 | C-12 four bars, 40 documents, 512 tokens, 13.4 point difference, teacher forcing removes it, negative 0.015 vs 0.005, Spearman negative 0.13 at p 0.45, sign test p 0.42, verdict FAIL, feedback compounding | `readscope\calibration\records\c12-longgen-drift-sym.json`; `readscope\calibration\DECLARATION-C12.md` at commit `90e2ce2`; `readscope\SPEC.md:806-825` |

## failures and corrections

none

## conditions

- An observer is a consumer, its output metric, and its budget. The consumer and the local geometry of its output metric determine the read operator. The budget bounds what of it can be measured and used and changes it only by changing the consumer.
- Two consumers with the same read operator on the same workload share a read geometry and are not thereby the same observer, since the consumer stays part of the triple and a sign change reverses every ranking.
- The output metric is a loss on the consumer's output. Where it has a local quadratic representation, that local geometry enters the read operator. A dataset-level loss has none, and the read operator is then taken on the score with the identity geometry.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ReadOperator.lean`, theorems `rank_one_reads_one_direction`, `readOp_mulVec`, `quad_readOp`, `quad_readOp_nonneg`, `readOp_mulVec_eq_zero_iff`, `readOp_diag`, `readOp_offdiag`, `readOp_symm`, `readOp_neg`, `affine_const_along_nuisance`, `readOp_affine`, `readOp_sqLength_basis`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13.

## related

read-operator, quotient, read-distortion, certificate

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
