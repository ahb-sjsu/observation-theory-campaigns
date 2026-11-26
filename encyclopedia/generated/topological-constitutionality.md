# Topological constitutionality

**id.** topological-constitutionality
**kind.** result
**volume.** Geometric Law, Volume 5 of the Geometric Series

## definition

The constitutional subcomplex is the part of the judicial complex whose vertices and simplices satisfy every constitutional predicate. A statute is called constitutional if and only if adding it leaves all path homology groups of that subcomplex unchanged, which the volume restates as creating no new non-trivial directed cycle.

**Example.** In the volume's running example the Digital Privacy Act adds two edges that create two new non-trivial directed cycles in the constitutional subcomplex, so the first path homology group changes and the statute is ruled unconstitutional.

**Known as, or related to prior art.** Path homology of directed graphs, which the volume attributes to Grigor'yan, Lin, Muranov and Yau.

## equation

none

## conditions

- The front matter classes the use of path homology for constitutionality as a modeling axiom. The theorem has a proof sketch.
- The same chapter states completeness as a conjecture. If the conjecture is false, preserved path homology is a necessary condition and not a sufficient one, and the appendix's full statement claims three one-directional parts only.
- Building the subcomplex requires deciding which vertices satisfy each predicate and how a statute changes the graph. The volume says this legal judgment cannot be fully automated.
- For a finite directed graph the groups are computable by Smith normal form of the boundary matrices. Chapter 16 leaves open whether the fundamental group detects inconsistencies that path homology misses.

Conditions are curated in `volumes/geometric-law.toml` rather than read from a record.

## ledger

none. *standing.* A conditional theorem with a proof sketch, whose if-and-only-if form the chapter also poses as a conjecture. The volume's applications of it are worked examples and not computations on a case corpus.

## first stated

Chapter 7, the subcomplex at [`geometric-law/chapters/ch07_constitutional_topology.md:32-45`](https://github.com/ahb-sjsu/geometric-law/blob/1021d65/chapters/ch07_constitutional_topology.md#L32-L45), the theorem at [`geometric-law/chapters/ch07_constitutional_topology.md:99-103`](https://github.com/ahb-sjsu/geometric-law/blob/1021d65/chapters/ch07_constitutional_topology.md#L99-L103), and the completeness conjecture at [`geometric-law/chapters/ch07_constitutional_topology.md:187-191`](https://github.com/ahb-sjsu/geometric-law/blob/1021d65/chapters/ch07_constitutional_topology.md#L187-L191). Online, [Geometric Law](https://erisml.org/geometric-law/ch07_constitutional_topology.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Law*, Volume 5 of the Geometric Series.

## related

judicial-complex, legal-wilson-loop, due-process-quotient-regularity, equal-protection-gauge-invariance

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
