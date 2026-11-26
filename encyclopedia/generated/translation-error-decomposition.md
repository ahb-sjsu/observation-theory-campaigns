# translation error decomposition

**id.** translation-error-decomposition
**kind.** result
**volume.** Geometric Communication, Volume 7 of the Geometric Series

## definition

The error of a translation system on a source text is written as a sum of three parts. Intrinsic holonomy is the minimum loss over all paths, fixed by the curvature of the content manifold. Path error is the extra holonomy of a path that is not the geodesic. Chart error comes from the system's imperfect representation of the two languages.

**Example.** If the intrinsic holonomy were 0.05, the path error 0.10 and the chart error 0.08, the total would be 0.23, and better path selection could remove at most 0.10 of it. The three values are chosen for the arithmetic and are not the volume's.

## equation

none

## conditions

- It presupposes the content manifold with a metric, its Levi-Civita connection, and languages as charts, all of which the volume posits.
- The holonomy part is called irreducible and is nonzero only where the source meaning lies outside the flat overlap of the two charts. The other two parts are called reducible.
- The path error is bounded through Proposition 10.2 by the maximum curvature times the area between the two paths, to leading order.
- The three parts are not measured separately anywhere in the volume.

Conditions are curated in `volumes/geometric-communication.toml` rather than read from a record.

## ledger

none. *standing.* A proposition with a short proof inside the posited geometry. No experiment in the volume separates the three terms.

## first stated

Proposition 10.3, [`geometric-communication/manuscript/part_iv/ch10_translation.md:312-322`](https://github.com/ahb-sjsu/geometric-communication/blob/8184f3a/manuscript/part_iv/ch10_translation.md#L312-L322). Online, [Geometric Communication](https://erisml.org/geometric-communication/ch10_translation.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Communication*, Volume 7 of the Geometric Series.

## related

translation-loop-residual, language-chart, moral-parallel-transport, curvature, geodesic-distance

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
