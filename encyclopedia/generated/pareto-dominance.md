# Pareto dominance

**id.** pareto-dominance
**kind.** concept
**volume.** Geometric Methods, Volume 1 of the Geometric Series

## definition

A configuration dominates another when it is no worse on every objective and strictly better on at least one. Two configurations of which neither dominates the other are mutually non-dominated, and the non-dominated set is the Pareto frontier.

**Example.** With two objectives to minimize, (2, 3) dominates (2, 4), and neither of (1, 5) and (3, 2) dominates the other.

**Known as, or related to prior art.** Pareto efficiency in economics and the non-dominated sorting of multi-objective optimization.

## equation

none

## conditions

- Every objective has a direction fixed in advance. The volume minimizes all of them.
- Dominance is a partial order. It ranks nothing inside the frontier, and a choice there needs a stated preference between the objectives.
- The frontier tables of Chapter 8 are posited illustrations. In the recorded run of Chapter 19 the frontier had two points, and one of them was a lucky draw on the test set.

Conditions are curated in `volumes/geometric-methods.toml` rather than read from a record.

## ledger

none. *standing.* A definition. Appendix C proves in writing that dominance is a strict partial order (Theorem C.7), and its Corollary C.7.1 was restated in the November 2026 review.

## first stated

Section 8.1.1, [`geometric-methods/chapters/chapter-08-pareto-optimization.md:14-20`](https://github.com/ahb-sjsu/geometric-methods/blob/65452de/chapters/chapter-08-pareto-optimization.md#L14-L20). Online, [Geometric Methods](https://erisml.org/geometric-methods/chapter-08-pareto-optimization.html).

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

budget, subset-enumeration, scalar-irrecoverability, defect-campaign-null-result

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
