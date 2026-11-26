# Finsler metric of the decision manifold

**id.** economic-finsler-metric
**kind.** concept
**volume.** Geometric Economics, Volume 4 of the Geometric Series

## definition

A cost function F(x, v) of position x and direction v that uses one inverse covariance matrix for gain directions and another for loss directions, so that F(x, v) and F(x, -v) differ. The loss-aversion coefficient at x is the ratio F(x, -v) / F(x, v).

**Example.** If a direction v has quadratic form 1 under the gain matrix and 4 under the loss matrix, the lengths are 1 and 2 and the coefficient is 2. Equal matrices give a coefficient of 1.

**Known as, or related to prior art.** Finsler geometry, which the volume cites from Bao, Chern and Shen.

## equation

none

## conditions

- Tagged a modeling axiom. The gain and loss metric tensors are not estimated in the volume.
- The tangent space at each point is split into a gain cone and a loss cone by the sign of the net change on the salient dimensions.
- Within one cone and for small displacements it reduces to the Mahalanobis metric. When the gain and loss matrices are equal it is the Mahalanobis metric and the coefficient is one.

Conditions are curated in `volumes/geometric-economics.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status block of 2026-07-14 calls the volume a posited framework, speculative theory awaiting instruments, and says that no economics instrument has been evaluated by the series' admission filter and that none passes its gate. Its claims are to be read as theory at licensed strength and not as validated measurement, and the chapters tag each claim as established mathematics, empirical, modeling axiom, conditional theorem or speculation.

## first stated

Section 4.10, [`geometric-economics/chapters/ch04_economic_metric.md:396-412`](https://github.com/ahb-sjsu/geometric-economics/blob/ab7b319/chapters/ch04_economic_metric.md#L396-L412), with the formal statement in the technical appendix, [`geometric-economics/chapters/ch04_economic_metric.md:449-461`](https://github.com/ahb-sjsu/geometric-economics/blob/ab7b319/chapters/ch04_economic_metric.md#L449-L461). Online, [Geometric Economics](https://erisml.org/geometric-economics/ch04_economic_metric.html).

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

economic-metric-tensor, geometric-loss-aversion-coefficient, mahalanobis-distance, metric

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
