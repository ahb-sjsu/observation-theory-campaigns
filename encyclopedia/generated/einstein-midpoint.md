# Einstein midpoint

**id.** einstein-midpoint
**kind.** instrument
**volume.** Geometric Methods, Volume 1 of the Geometric Series

## definition

The weighted centroid of points on the Poincare ball of curvature minus c. It is the average in the Klein model with each point weighted by its Lorentz factor, carried back to the ball. In ball coordinates it is the Mobius half of $\sum_i w_i \lambda_i x_i / \sum_i w_i (\lambda_i - 1)$, with $\lambda_i = 2/(1 - c\|x_i\|^2)$.

**Example.** For the points (0.9, 0) and (0, 0) in the unit ball with equal weights, the midpoint lies at radius tanh(0.5 artanh 0.9), about 0.627. The shortcut that averages ball coordinates weighted by 1/(1 - 0.81) and 1 gives 0.756. Both values are the volume's.

## equation

none

## conditions

- The points lie in the open ball, where c times the squared norm is below 1, and the weights are non-negative.
- Proposition 3.1 states that the midpoint lies in the ball, reduces to the Euclidean weighted mean as c goes to 0, and for two points with equal weights is the midpoint of their geodesic. The text gives a proof sketch.
- Weighting the ball coordinates by $1/(1 - c\|x\|^2)$ and averaging them directly is not a hyperbolic midpoint. The November 2026 review corrected the chapter's formula.

Conditions are curated in `volumes/geometric-methods.toml` rather than read from a record.

## ledger

none. *standing.* Proved, and checked against an independent computation in `formal/matlab/volume_checks.m` (Section 21.8).

## first stated

Section 3.6.1, [`geometric-methods/chapters/chapter-03-hyperbolic-geometry.md:530-554`](https://github.com/ahb-sjsu/geometric-methods/blob/371478c/chapters/chapter-03-hyperbolic-geometry.md#L530-L554). Online, [Geometric Methods](https://erisml.org/geometric-methods/chapter-03-hyperbolic-geometry.html).

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

geodesic-distance, curvature, manifold, mean-median

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
