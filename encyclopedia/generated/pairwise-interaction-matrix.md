# pairwise interaction matrix

**id.** pairwise-interaction-matrix
**kind.** concept
**volume.** Geometric Methods, Volume 1 of the Geometric Series

## definition

Let $\Delta_i$ be the rise in error from removing dimension i alone. The pairwise interaction $\Phi_{ij}$ is the rise from removing both i and j, minus $\Delta_i + \Delta_j$. A positive value marks a redundant pair, each standing in for the other. A negative value marks a complementary pair, each needing the other.

**Example.** In the volume's illustration, two copies of one signal cost 0 to remove singly and 1 to remove together, so the interaction is 1 - 0 = +1. Two halves of an exclusive-or cost 1 each and 1 together, so it is 1 - 2 = -1.

## equation

none

## conditions

- The matrix is symmetric with zero diagonal and costs 1 + n + n(n-1)/2 evaluations for n dimensions.
- Ablation from the full model is blind to redundant pairs, and adding dimensions one at a time is blind to complementary pairs.
- The two identities of Section 12.4.2 that tie the matrix to the gains of a build-up sequence hold exactly only when the evaluation function has no interactions above second order.
- The sign convention was corrected in the November 2026 review. The matrix printed in Section 12.2.2 is hypothetical.

Conditions are curated in `volumes/geometric-methods.toml` rather than read from a record.

## ledger

none. *standing.* A definition. The identities of Section 12.4.2 are proved and checked symbolically in `formal/matlab/volume_checks.m`, and the tables of Chapter 12 are posited.

## first stated

Section 12.1.3, [`geometric-methods/chapters/chapter-12-compositional-testing.md:76-94`](https://github.com/ahb-sjsu/geometric-methods/blob/65452de/chapters/chapter-12-compositional-testing.md#L76-L94). Online, [Geometric Methods](https://erisml.org/geometric-methods/chapter-12-compositional-testing.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Methods*, Volume 1 of the Geometric Series.

## related

sensitivity, subset-enumeration, model-robustness-index, independence

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
