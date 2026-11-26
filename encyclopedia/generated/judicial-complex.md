# Judicial complex

**id.** judicial-complex
**kind.** concept
**volume.** Geometric Law, Volume 5 of the Geometric Series

## definition

The judicial complex $\mathcal{K}$ is a directed weighted simplicial complex. Each decided case is a vertex carrying a vector of eight legal dimension scores, a court level and a date. A directed edge with an asymmetric non-negative weight runs from a cited case to the citing case, and a set of mutually citing cases that establish a doctrine is a higher simplex.

**Example.** In the volume's illustrative mini-complex, five voter ID cases are the vertices and six citations are the directed edges, one of which runs from Crawford (Supreme Court, 2008) to Judge Rivera's district case of 2026.

**Known as, or related to prior art.** Citation networks of case law and the simplicial complexes of algebraic topology.

## equation

none

## conditions

- The front matter classes the structural choices of the model as modeling axioms, and Chapter 16 calls the complex a model of legal reasoning and not a replica.
- Citation edges respect time, so the citation subgraph is acyclic. Binding authority runs from a higher court to a lower one, and the reverse direction has high or infinite cost.
- The continuum limit to a Riemannian manifold is used as a theoretical tool. The discrete complex is primary and every computation on it is finite.
- Chapter 4 states that scoring a case corpus and calibrating the weights has not yet been executed on legal data. The five-case complex in Chapter 3 is an illustration.

Conditions are curated in `volumes/geometric-law.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic status of 2026-07-14 calls the volume a posited framework with one instrumented corner. That corner is the legal text embedding LeBSE, validated in the xbse admission filter on US case law with labels from the CourtListener citation graph, and the README says this covers structure preservation in legal text embeddings and not the book's broader jurisprudential claims, which remain posited theory at licensed strength.

## first stated

Chapter 3, the formal construction, [`geometric-law/chapters/ch03_judicial_complex.md:130-142`](https://github.com/ahb-sjsu/geometric-law/blob/1e50dfc/chapters/ch03_judicial_complex.md#L130-L142), with the tuple form in the appendix, [`geometric-law/chapters/ch03_judicial_complex.md:426-431`](https://github.com/ahb-sjsu/geometric-law/blob/1e50dfc/chapters/ch03_judicial_complex.md#L426-L431). Online, [Geometric Law](https://erisml.org/geometric-law/ch03_judicial_complex.html).

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

eight-legal-dimensions, legal-edge-weight, legal-friction, graph, manifold

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
