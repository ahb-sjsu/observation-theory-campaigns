# query budget

**id.** query-budget
**kind.** concept
**volume.** Geometric Methods, Volume 1 of the Geometric Series

## definition

The mean number of retrieval slots per point, $\rho = n_q k / n$, when $n_q$ queries each return k neighbours from n points. A corpus with no hub structure still shows a k-occurrence skewness of $1/\sqrt{\rho}$, so the null of a hubness reading rises as the budget falls.

**Example.** With 10,000 queries, 10 neighbours each and 200,000 points, the budget is 100,000/200,000 = 0.5 and the null skewness is 1 over the square root of 0.5, about 1.41. The volume's measured skewness in that cell is 1.79.

## equation

none

## conditions

- The null assumes every point is equally likely to be returned, so its count is close to Poisson with mean equal to the budget.
- Every count statistic is quoted with its budget, and a comparison made at two budgets compares two nulls.
- The volume's rule is to keep the budget at 2 or more where a decision depends on the count. Below that the null dominates every statistic.
- The measured table is from one corpus, 1024-dimensional embeddings of Wikipedia passages in the openvector-bench repository, and is not peer reviewed.

Conditions are curated in `volumes/geometric-methods.toml` rather than read from a record.

## ledger

none. *standing.* The identities of Section 17.11 are proved and checked symbolically in `formal/matlab/ch17_neighbourhood_stats.m`. The measurements are demonstrated or exploratory, as each source file states.

## first stated

Section 17.11.2, [`geometric-methods/chapters/chapter-17-scaling.md:482-490`](https://github.com/ahb-sjsu/geometric-methods/blob/65452de/chapters/chapter-17-scaling.md#L482-L490). Online, [Geometric Methods](https://erisml.org/geometric-methods/chapter-17-scaling.html).

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

hubness, anti-hub, poisson-ceiling, skewness, attractiveness-skew, null-model

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
