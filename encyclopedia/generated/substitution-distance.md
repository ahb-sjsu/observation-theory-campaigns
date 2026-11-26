# substitution distance

**id.** substitution-distance
**kind.** instrument
**volume.** Geometric Gastronomy, Volume 12 of the Geometric Series

## definition

Replacing ingredient j by j' at amount $a_j$ moves the dish, to first order, by $\Delta\mathbf{f} \approx a_j(\mathbf{f}_{j'} - \mathbf{f}_j)$. The substitution is safe when this displacement is short in the flavor metric. Agreement on one coordinate, such as sourness, does not guarantee a short distance.

**Example.** On the axes (sour, citrus aroma) let lime be (4, 3), lemon (4, 2.5) and distilled vinegar (4.5, 0). At amount 2 with a Euclidean metric the lemon swap moves the dish by 2 times 0.5 = 1. The vinegar swap moves it by 2 times the length of (0.5, -3), about 6.1. The lemon and vinegar case is the volume's and the vectors are illustrative.

## equation

none

## conditions

- Tagged a modeling axiom, to first order. It ignores curvature corrections and the nonlinearities of downstream operators.
- It assumes the substitute passes through the same downstream operators. A substitution near the source of a long branch can grow through each transformation, and one near the sink does not.
- It rests on the additive model of a dish as a weighted sum of ingredient vectors, which the volume says is linear only locally.

Conditions are curated in `volumes/geometric-gastronomy.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, with no gastronomy instrument evaluated by the series' admission filter (xbse) and the nearest evaluated perceptual domains, aesthetics and music, rated inadmissible to medium. Its claims are to be read as theory at licensed strength and not as validated measurement, and the chapters tag each statement as a modeling axiom, empirical, a conjecture or a theorem.

## first stated

Section 8.6, [`geometric-gastronomy/chapters/ch08_recipe_as_geometric_construction.md:94-100`](https://github.com/ahb-sjsu/geometric-gastronomy/blob/dfbfdbb/chapters/ch08_recipe_as_geometric_construction.md#L94-L100). Online, [Geometric Gastronomy](https://erisml.org/geometric-gastronomy/ch08_recipe_as_geometric_construction.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Gastronomy*, Volume 12 of the Geometric Series.

## related

flavor-riemannian-metric, euclidean-distance, vector, flavor-space, inverse-flavor-problem

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
