# Moral decision complex

**id.** moral-decision-complex
**kind.** concept
**volume.** Geometric Ethics, Volume 2 of the Geometric Series

## definition

A weighted simplicial complex built from the moral manifold. A vertex is a morally relevant state with a nine-dimensional attribute vector, an edge is an available action with a non-negative weight for its total moral cost, and a higher simplex is a bundle of jointly executed actions whose cost may differ from the sum of its edges.

**Example.** Three states A, B, C with action weights A to B = 2, B to C = 3 and A to C = 6. The minimum-weight path from A to C goes through B at cost 2 + 3 = 5, which is less than 6. The weights are illustrative.

## equation

none

## conditions

- The volume tags the definition as a Modeling Axiom.
- Evidence status of the metric (Section 8.10a, added in v1.28). The covariance that sets the edge weights is a modeling choice, and no measurement in the volume shows a metric predicting moral judgements better than the boundary penalties alone. Every statement that uses the covariance is a statement about a model whose metric has not been tested.
- Proposition 8.5 relates the complex to the continuous manifold as the grid is refined. It is tagged Proved, and the v1.28 change notes record an open finding on the proof of its part (i) as written. For that reason v1.29 gave it no row in Appendix F.
- Each domain volume instantiates the complex with its own dimensions, covariance and penalties. Those choices are not fixed here.

Conditions are curated in `volumes/geometric-ethics.toml` rather than read from a record.

## ledger

none. *standing.* Tagged Modeling Axiom in the text, and listed as a Modeling Axiom in Appendix F as of v1.29. The ledger has no row for Definition 8.12.

## first stated

Definition 8.12, Section 8.10a, [`geometric-ethics/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html:1264-1276`](https://github.com/ahb-sjsu/geometric-ethics/blob/401b9a5/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html#L1264-L1276). Online, [Geometric Ethics](https://erisml.org/book/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Ethics*, Volume 2 of the Geometric Series.

## related

moral-decision-edge-weight, moral-metric-evidence-status, moral-manifold, geometric-decision-cost, graph

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
