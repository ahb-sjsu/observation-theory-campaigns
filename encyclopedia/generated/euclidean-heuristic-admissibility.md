# admissibility of the Euclidean heuristic under a Mahalanobis metric

**id.** euclidean-heuristic-admissibility
**kind.** result
**volume.** Geometric Methods, Volume 1 of the Geometric Series

## definition

In A* search with Mahalanobis edge weights, the straight-line Euclidean distance to the goal never overestimates the true cost exactly when every eigenvalue of the inverse covariance is at least 1. Otherwise scale it by the square root of the smallest eigenvalue, or use the Mahalanobis distance to the goal as the heuristic.

**Example.** In the volume's posited covariance the Consequences axis has variance 25, so a Euclidean step of 1 along it has Mahalanobis length 0.2. The Euclidean heuristic says 1 and overestimates. For a diagonal covariance the matching eigenvalue of the inverse is 0.04, and scaling by its square root gives 0.2.

**Known as, or related to prior art.** Admissible heuristics for A* search, after Hart, Nilsson and Raphael (1968).

## equation

none

## conditions

- The metric tensor is a constant inverse covariance, so the space is flat and anisotropic, not curved.
- The scaled heuristic is admissible and often very loose. The Mahalanobis heuristic is exact for one step and ignores boundary penalties, so it can fall far below the true cost where a boundary lies on the path.
- The covariance the chapter applies it to, with variances from 0.25 to 25, is posited. No record supports its values.

Conditions are curated in `volumes/geometric-methods.toml` rather than read from a record.

## ledger

none. *standing.* Proposition 6.1 is proved in the text. The covariance, penalties and scaling functions of Chapter 6 that it is applied to are posited (Section 21.8).

## first stated

Proposition 6.1, [`geometric-methods/chapters/chapter-06-pathfinding-on-manifolds.md:61-67`](https://github.com/ahb-sjsu/geometric-methods/blob/65452de/chapters/chapter-06-pathfinding-on-manifolds.md#L61-L67), with the corrected heuristics in Section 6.2.2, [`geometric-methods/chapters/chapter-06-pathfinding-on-manifolds.md:71-81`](https://github.com/ahb-sjsu/geometric-methods/blob/65452de/chapters/chapter-06-pathfinding-on-manifolds.md#L71-L81). Online, [Geometric Methods](https://erisml.org/geometric-methods/chapter-06-pathfinding-on-manifolds.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Methods*, Volume 1 of the Geometric Series.

## related

mahalanobis-distance, eigenvalue-eigenvector, geodesic-distance, anisotropic, degenerate-balance-coordinate

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
