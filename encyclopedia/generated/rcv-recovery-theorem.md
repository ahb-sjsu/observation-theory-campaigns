# RCV Recovery Theorem

**id.** rcv-recovery-theorem
**kind.** result
**volume.** Geometric Politics, Volume 10 of the Geometric Series

## definition

In an election with $k$ candidates on a $d$-dimensional preference manifold, plurality keeps ordinal information along one axis and ranked-choice voting keeps it along $\min(d, k-1)$ axes. The recovery ratios are $1/d$ and $\min(d, k-1)/d$.

**Example.** With six dimensions and five candidates, plurality has ratio $1/6$, about 17 percent, and ranked choice has $\min(6, 4)/6 = 4/6$, about 67 percent. With three candidates ranked choice has $2/6$, about 33 percent.

**Known as, or related to prior art.** Ranked-choice voting is also called instant-runoff voting.

## equation

none

## conditions

- The recovery is ordinal and partial. Cardinal intensity is lost, and the Democratic Irrecoverability Theorem still applies.
- Positions on dimensions that do not affect any candidate ranking stay invisible, as they are under plurality.
- Chapters 5 and 15 list 45 percent of information preserved for ranked choice in the five-candidate District 7 example. The formula of this theorem gives 4 of 6 for that case, and the volume does not reconcile the two figures.
- The Alaska 2022, New York City 2021 and Maine 2018 elections are read through the theorem after the fact. They are not tests of it.

Conditions are curated in `volumes/geometric-politics.toml` rather than read from a record.

## ledger

none. *standing.* A theorem with a proof written in the chapter, which counts independent pairwise comparisons. The information percentages listed elsewhere in the volume are illustrations.

## first stated

Theorem 7 of Chapter 13, [`geometric-politics/manuscript/part_iv/ch13_ranked_choice.md:35-47`](https://github.com/ahb-sjsu/geometric-politics/blob/436c5b5/manuscript/part_iv/ch13_ranked_choice.md#L35-L47). The ratios are repeated in Appendix C.3, [`geometric-politics/manuscript/appendices/appendix_c_voting.md:85-87`](https://github.com/ahb-sjsu/geometric-politics/blob/436c5b5/manuscript/appendices/appendix_c_voting.md#L85-L87). Online, [Geometric Politics](https://erisml.org/geometric-politics/appendix_c_voting.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Politics*, Volume 10 of the Geometric Series.

## related

democratic-irrecoverability-theorem, manifold-condorcet-winner, political-bond-index, geometrized-arrow-theorem

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
