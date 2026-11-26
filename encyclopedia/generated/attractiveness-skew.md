# attractiveness skew

**id.** attractiveness-skew
**kind.** instrument
**volume.** Geometric Methods, Volume 1 of the Geometric Series

## definition

Model the retrieval count of a point as Poisson with mean $\rho w$, where w is its attractiveness, with mean one. Solve the variance and third central moment of the counts for those of w, and report $\mu_3(w)/\mathrm{Var}(w)^{3/2}$, a hubness measure that does not contain the query budget.

**Example.** Counts with mean 2 and variance 6 give an attractiveness variance of (6 - 2)/4 = 1. Counts with mean 2 and variance 2 give 0, and the estimator returns no value.

## equation

none

## conditions

- The estimator returns no value when the variance of the counts is at or below the budget, which is when the budget is too small to resolve any structure.
- On a fixed corpus with a known skew of 9.85 the estimate stayed between 9.84 and 10.02 across budgets of 0.5 to 4, while the raw skewness ranged from 2.46 to 5.59.
- Two simpler statistics formed by dividing by a null were believed free of the budget. Measured under two protocols, their slopes changed sign.
- An invariant estimator does not protect against a biased sample. The claim that hubness in the real corpus rises with corpus size was withdrawn when queries and corpus were found to come from different files of an ordered dataset.

Conditions are curated in `volumes/geometric-methods.toml` rather than read from a record.

## ledger

none. *standing.* The moment identities are proved and checked symbolically. The measurements are demonstrated or exploratory as each source file states, and one claim built on them was withdrawn, not refuted.

## first stated

Section 17.11.2, [`geometric-methods/chapters/chapter-17-scaling.md:503-513`](https://github.com/ahb-sjsu/geometric-methods/blob/371478c/chapters/chapter-17-scaling.md#L503-L513), with the withdrawn claim at [`geometric-methods/chapters/chapter-17-scaling.md:540-540`](https://github.com/ahb-sjsu/geometric-methods/blob/371478c/chapters/chapter-17-scaling.md#L540-L540). Online, [Geometric Methods](https://erisml.org/geometric-methods/chapter-17-scaling.html).

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

query-budget, hubness, hub, poisson-distribution, skewness, withdrawn-versus-refuted

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
