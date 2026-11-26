# Legal phase transition (overruling as graph surgery)

**id.** legal-phase-transition
**kind.** concept
**volume.** Geometric Law, Volume 5 of the Geometric Series

## definition

Overruling a precedent is a discrete graph surgery. The old precedent's weight deformation is removed from every nearby edge and the new precedent's is added, which changes shortest paths discontinuously. Its cost is the sum, over the cases that relied on the old precedent, of each case's weight times the size of its weight change.

**Example.** Two relying cases with weights 3 and 1 whose edge weights change by 0.5 and 2 give an overruling cost of 3 x 0.5 + 1 x 2 = 3.5.

## equation

none

## conditions

- The volume's criterion is that a precedent is overruled when the holonomy around its doctrinal loop exceeds a tolerance and the benefit exceeds the reliance cost. Neither threshold is given a value.
- A first-order transition flips a holding. A second-order transition changes a rule continuously with a jump in its rate of change, and the volume's example is the erosion of Bivens.
- The volume offers the model as an explanation of why overruling is rare and comes in clusters. It reports no test of the criterion.

Conditions are curated in `volumes/geometric-law.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic status of 2026-07-14 calls the volume a posited framework with one instrumented corner. That corner is the legal text embedding LeBSE, validated in the xbse admission filter on US case law with labels from the CourtListener citation graph, and the README says this covers structure preservation in legal text embeddings and not the book's broader jurisprudential claims, which remain posited theory at licensed strength.

## first stated

Chapter 9, [`geometric-law/chapters/ch09_stare_decisis.md:118-134`](https://github.com/ahb-sjsu/geometric-law/blob/c05fb6b/chapters/ch09_stare_decisis.md#L118-L134), with the general definition and the critical point at [`geometric-law/chapters/ch09_stare_decisis.md:218-240`](https://github.com/ahb-sjsu/geometric-law/blob/c05fb6b/chapters/ch09_stare_decisis.md#L218-L240). Online, [Geometric Law](https://erisml.org/geometric-law/ch09_stare_decisis.html).

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

precedential-weight-deformation, legal-wilson-loop, legal-geometric-pathologies, threshold

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
