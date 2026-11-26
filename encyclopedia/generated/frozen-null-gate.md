# frozen-null gate

**id.** frozen-null-gate
**kind.** instrument
**volume.** Geometric Methods, Volume 1 of the Geometric Series

## definition

A pass mark set as a margin over nulls, which are versions of the instrument that cannot contain the effect. The gate passes when the score of the system under test, minus the highest null score on the same held-out data, is at least the margin $\delta$. Nulls, margin and date are committed before the run.

**Example.** With a score of 0.62 for the system and 0.48 and 0.55 for two nulls, the difference from the higher null is 0.07, below a margin of 0.10, so the gate fails. By the volume's figure, a margin of one standard error lets a system with no effect pass about 16% of the time.

## equation

none

## conditions

- The margin is sized in units of noise. With a margin of z standard errors of the difference under no effect, a system with no effect passes with probability 1 minus the standard normal distribution function at z.
- A bar of this kind may be tightened later. It may not be loosened.
- A null can depend on a design quantity, as the hubness null depends on the query budget. Hold that quantity fixed, or model the null and remove it, and confirm the removal by measurement.
- The rule is normative. The volume classes the method itself as exploratory until programmes other than its author's have used it and reported what broke.

Conditions are curated in `volumes/geometric-methods.toml` rather than read from a record.

## ledger

none. *standing.* A rule of method, not a finding. Its normative source is the Claim Ledger Specification PE-CLS-1.0, which governs where the chapter differs from it.

## first stated

Section 21.3, [`geometric-methods/chapters/chapter-21-measurement-discipline.md:67-73`](https://github.com/ahb-sjsu/geometric-methods/blob/65452de/chapters/chapter-21-measurement-discipline.md#L67-L73). Online, [Geometric Methods](https://erisml.org/geometric-methods/chapter-21-measurement-discipline.html).

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

null-model, bar, gate, preregistration, sealed, query-budget

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
