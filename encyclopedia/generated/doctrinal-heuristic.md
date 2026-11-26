# Doctrinal heuristic

**id.** doctrinal-heuristic
**kind.** concept
**volume.** Geometric Law, Volume 5 of the Geometric Series

## definition

A legal doctrine read as an A* heuristic. It is a non-negative function on cases that estimates the remaining legal friction to the goal region, computed as the sum of the estimated costs of the claim's elements not yet established. It is admissible when no element's estimate exceeds its true proving cost.

**Example.** In the volume's illustration McDonnell Douglas estimates 2.0 + 0.5 + 4.0 = 6.5 friction units from the start and direct evidence estimates 8.0, so A* explores the McDonnell Douglas path first.

**Known as, or related to prior art.** Admissible heuristics in A* search, with precedent in the role of a pattern database.

## equation

none

## conditions

- With an admissible heuristic, A* returns the minimum-friction argument. That is the standard A* guarantee, and the volume's proof assumes that element costs add.
- Overestimation breaks admissibility. Underestimation keeps it and weakens the guidance, down to the zero heuristic, which the volume identifies with a totality of the circumstances test.
- The volume calls balancing tests circular heuristics and says a novel legal question has no precomputed heuristic at all.
- The element costs are posited. The friction units in the chapter's comparison of McDonnell Douglas with direct evidence are illustrative.

Conditions are curated in `volumes/geometric-law.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic status of 2026-07-14 calls the volume a posited framework with one instrumented corner. That corner is the legal text embedding LeBSE, validated in the xbse admission filter on US case law with labels from the CourtListener citation graph, and the README says this covers structure preservation in legal text embeddings and not the book's broader jurisprudential claims, which remain posited theory at licensed strength.

## first stated

Chapter 6, the definition at [`geometric-law/chapters/ch06_precedent_heuristic.md:86-90`](https://github.com/ahb-sjsu/geometric-law/blob/1e50dfc/chapters/ch06_precedent_heuristic.md#L86-L90), admissibility at [`geometric-law/chapters/ch06_precedent_heuristic.md:129-137`](https://github.com/ahb-sjsu/geometric-law/blob/1e50dfc/chapters/ch06_precedent_heuristic.md#L129-L137), and the appendix form at [`geometric-law/chapters/ch06_precedent_heuristic.md:353-363`](https://github.com/ahb-sjsu/geometric-law/blob/1e50dfc/chapters/ch06_precedent_heuristic.md#L353-L363). Online, [Geometric Law](https://erisml.org/geometric-law/ch06_precedent_heuristic.html).

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

legal-friction, judicial-complex, legal-geometric-pathologies, precedential-weight-deformation

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
