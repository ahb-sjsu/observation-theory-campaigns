# Democratic Irrecoverability Theorem

**id.** democratic-irrecoverability-theorem
**kind.** result
**volume.** Geometric Politics, Volume 10 of the Geometric Series

## definition

A voting function maps the positions of $n$ voters on a $d$-dimensional preference manifold to an outcome space of lower dimension. It is then non-injective, no function of the outcome recovers the preferences, and the fraction of manifold information destroyed is at least $(d - \dim \mathcal{O})/d$.

**Example.** With six dimensions and a single-winner outcome of dimension 1, at least $(6-1)/6$, about 83 percent, of the manifold information is destroyed. With four effective dimensions the bound is $3/4$, or 75 percent.

## equation

none

## conditions

- The outcome space must have lower dimension than the preference manifold. The supporting Lemma 1 is stated with the weaker hypothesis that the outcome dimension is below $n$ times $d$.
- The bound depends on $d$. Chapter 18 notes that with an effective dimensionality of 4 the plurality bound falls from 83 percent to 75 percent.
- Part (c) treats the preference configuration as a random variable and bounds mutual information by the entropy of the outcome. The percentages of information preserved that the chapter lists for five voting systems in District 7 are illustrations and not outputs of the theorem.

Conditions are curated in `volumes/geometric-politics.toml` rather than read from a record.

## ledger

none. *standing.* A theorem with a proof written in the chapter, inside a volume that is posited as a whole. The volume calls it the political instance of the Scalar Irrecoverability Theorem of Geometric Reasoning, which it cites as Theorem 13.1 of that book, a conditional theorem.

## first stated

Theorem 1 of Chapter 5, [`geometric-politics/manuscript/part_ii/ch05_voting_contraction.md:53-59`](https://github.com/ahb-sjsu/geometric-politics/blob/8f4a831/manuscript/part_ii/ch05_voting_contraction.md#L53-L59), after Definition 2 of the voting function at [`geometric-politics/manuscript/part_ii/ch05_voting_contraction.md:28-37`](https://github.com/ahb-sjsu/geometric-politics/blob/8f4a831/manuscript/part_ii/ch05_voting_contraction.md#L28-L37). Online, [Geometric Politics](https://erisml.org/geometric-politics/ch05_voting_contraction.html).

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

scalar-irrecoverability, political-preference-manifold, rcv-recovery-theorem, geometrized-arrow-theorem, political-bond-index, binary-verdict-irrecoverability

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
