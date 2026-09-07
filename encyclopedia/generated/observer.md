# observer

**id.** observer
**kind.** concept

![A consumer, an output metric, and a budget.](../figures/observer.svg)

## definition

A consumer, its output metric, and its budget, written as the triple in equation 1.1. Naming all three is what every later chapter checks.

**Example.** A cosine ranker with rank order as its metric and 1000 candidates as its budget is one observer.

**Known as, or related to prior art.** The observer triple extends the active-subspace matrix with an output metric, a budget, and an audit discipline.

## equation

Book equation 1.1.

    O=(C,\ G,\ B).

Book equation 0.11.

    P_C(x)=J(x)^{\top}G\big(C(x)\big)\,J(x),\qquad J(x)=\frac{\partial C}{\partial x}(x),\qquad \bar P_{C,\mu}=\mathbb E_{\mu}\!\left[P_C(x)\right].

## conditions

- An observer is a consumer, its output metric, and its budget. The consumer and the local geometry of its output metric determine the read operator. The budget bounds what of it can be measured and used and changes it only by changing the consumer.
- Two consumers with the same read operator on the same workload share a read geometry and are not thereby the same observer, since the consumer stays part of the triple and a sign change reverses every ranking.
- The output metric is a loss on the consumer's output. Where it has a local quadratic representation, that local geometry enters the read operator. A dataset-level loss has none, and the read operator is then taken on the score with the identity geometry.

Conditions are curated in `entries.toml` rather than read from a record.

## ledger

none

## first stated

Volume 14, chapter 4, `geometric-observation/chapters/ch04_the_observer_triple.md:9-60`, and `geometric-observation/OBSERVATION.md:1-10`, DOI 10.5281/zenodo.21776291. Version 1.0 of the theory was declared on 2026-08-18 in `geometric-observation/crucible/DECLARATION-V1.md`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.2 | the observer triple, read subspace, nuisance, same read operator means same read geometry | [`geometric-observation/chapters/ch04_the_observer_triple.md:9-60`](https://github.com/ahb-sjsu/geometric-observation/blob/0792c84/chapters/ch04_the_observer_triple.md#L9-L60); [`geometric-observation/OBSERVATION.md:1-10`](https://github.com/ahb-sjsu/geometric-observation/blob/0792c84/OBSERVATION.md#L1-L10) |
| chapter 6 section 6.1 | the classifier row of the consumer table, the output metric makes a different observer | [`geometric-observation/chapters/ch04_the_observer_triple.md:60-135`](https://github.com/ahb-sjsu/geometric-observation/blob/0792c84/chapters/ch04_the_observer_triple.md#L60-L135) |

## failures and corrections

none

## machine checked

[`lean/DataMiningAsObservation/ReadOperator.lean`](https://github.com/ahb-sjsu/observation-data-mining/blob/95af30c/lean/DataMiningAsObservation/ReadOperator.lean), theorems `rank_one_reads_one_direction`, `readOp_mulVec`, `quad_readOp`, `quad_readOp_nonneg`, `readOp_mulVec_eq_zero_iff`, `readOp_diag`, `readOp_offdiag`, `readOp_symm`, `readOp_neg`, `affine_const_along_nuisance`, `readOp_affine`, `readOp_sqLength_basis`, at observation-data-mining 95af30c; what the check covers is stated in the book's [appendix C](https://github.com/ahb-sjsu/observation-data-mining/blob/95af30c/chapters/machine_checked.md).

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13.

## related

read-operator, quotient, read-distortion, certificate

## see also

Book equations stated beside the entry's terms, not defining it: 0.9.

Ledger rows that cite the entry's records without naming it: OT-7, GO-1.

Sources-table rows that share a record with the entry without naming it: chapter 1 section 1.2, chapter 1 section 1.3, chapter 1 section 1.5, chapter 8 section 8.8, chapter 8 section 8.10, chapter 11 section 11.7, chapter 11 section 11.9.

## status

Generated 2026-09-07 by `encyclopedia/generate.py`; book at observation-data-mining 95af30c; the commit of every record is listed in the encyclopedia's provenance.
