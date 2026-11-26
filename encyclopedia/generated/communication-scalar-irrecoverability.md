# Communication Scalar Irrecoverability

**id.** communication-scalar-irrecoverability
**kind.** result
**volume.** Geometric Communication, Volume 7 of the Geometric Series

## definition

For any scalar evaluation $\phi$ of a communicative act, each level set $\phi^{-1}(r)$ is a submanifold of the communication manifold of codimension at most 1, so it has dimension dim(S) + dim(P) + dim(C) - 1. The scalar value alone does not recover the act's position in the discarded directions.

**Example.** If the signal, pragmatic and content factors had 20, 4 and 10 dimensions, a level set of one score would have 20 + 4 + 10 - 1 = 33 dimensions. The factor sizes are chosen for the arithmetic and are not the volume's.

## equation

none

## conditions

- Chapter 3 says the statement follows from the dimensional mismatch between the manifold and the real line. Chapter 1 defers the proof to the parent theorem of Geometric Reasoning.
- The form of Theorem 1.1 needs quality profiles that are mutually Pareto-non-dominated across d independent dimensions. Its corollary says k scalar metrics with k below d still do not recover the profile.
- The corollary requires independent measurements. The chapter says BLEU, METEOR and chrF++ are nearly parallel projections.
- The examples in the theorem (a BLEU score of 0.35, a sentiment score of +0.8, a word error rate of 5%) are illustrations, not measurements.

Conditions are curated in `volumes/geometric-communication.toml` rather than read from a record.

## ledger

none. *standing.* A theorem stated with an argument from dimension counting. The volume has no written proof of its own and refers to Geometric Reasoning, Chapter 13.

## first stated

Theorem 3.1, [`geometric-communication/manuscript/part_i/ch03_communication_manifold.md:389-395`](https://github.com/ahb-sjsu/geometric-communication/blob/8184f3a/manuscript/part_i/ch03_communication_manifold.md#L389-L395), and in profile form as Theorem 1.1, [`geometric-communication/manuscript/part_i/ch01_perplexity_trap.md:174-176`](https://github.com/ahb-sjsu/geometric-communication/blob/8184f3a/manuscript/part_i/ch01_perplexity_trap.md#L174-L176). Online, [Geometric Communication](https://erisml.org/geometric-communication/ch03_communication_manifold.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Communication*, Volume 7 of the Geometric Series.

## related

scalar-irrecoverability, benchmark-scalar-irrecoverability, communication-manifold, projection, pareto-dominance, signal-scalar-gauge-trilemma

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
