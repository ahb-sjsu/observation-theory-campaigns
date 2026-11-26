# Bond geodesic

**id.** bond-geodesic
**kind.** concept
**volume.** Geometric Economics, Volume 4 of the Geometric Series

## definition

The minimum-cost path on the economic decision complex from an initial state to a goal region, where the cost of a path is the sum of its edge weights and each edge weight is the Mahalanobis term plus the penalties of the boundaries crossed.

**Example.** Two paths to the goal with edge weights 1 + 4 = 5 and 2 + 2 = 4. The second is the Bond geodesic. A third path that crosses a boundary with infinite penalty costs infinity and is excluded.

**Known as, or related to prior art.** A shortest path in a weighted graph, which the volume computes by A* search.

## equation

none

## conditions

- It is the discrete analogue of a Riemannian geodesic. In the smooth limit the volume identifies it with a geodesic of the metric given by the inverse covariance.
- It needs the covariance matrix and the boundary penalties as inputs. The volume says the framework does not supply those measurements.
- Edge weights are squared Mahalanobis terms, so the volume notes that two half steps cost half as much as one full step and the path favors gradual transitions.
- A path that crosses a boundary with infinite penalty has infinite cost and is never the geodesic when a finite-cost path exists.

Conditions are curated in `volumes/geometric-economics.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status block of 2026-07-14 calls the volume a posited framework, speculative theory awaiting instruments, and says that no economics instrument has been evaluated by the series' admission filter and that none passes its gate. Its claims are to be read as theory at licensed strength and not as validated measurement, and the chapters tag each claim as established mathematics, empirical, modeling axiom, conditional theorem or speculation.

## first stated

Definition 18, Chapter 7, [`geometric-economics/chapters/ch07_bond_geodesic_equilibrium.md:40-48`](https://github.com/ahb-sjsu/geometric-economics/blob/a4483e7/chapters/ch07_bond_geodesic_equilibrium.md#L40-L48). Online, [Geometric Economics](https://erisml.org/geometric-economics/ch07_bond_geodesic_equilibrium.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Economics*, Volume 4 of the Geometric Series.

## related

economic-decision-complex, bond-geodesic-equilibrium, moral-economic-boundary, geodesic-distance, geometric-decision-cost

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
