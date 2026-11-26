# Political metric

**id.** political-metric
**kind.** concept
**volume.** Geometric Politics, Volume 10 of the Geometric Series

## definition

A Riemannian metric tensor $g_{ij}(p)$ on the political preference manifold that gives the cost of moving a position along dimensions $i$ and $j$ at the point $p$. It is anisotropic and position-dependent, so equal coordinate steps can cost different amounts.

**Example.** Take a diagonal metric with cost 1 on the economic dimension and cost 4 on the social dimension. A unit step on the social dimension has length $\sqrt{4} = 2$, twice the length of a unit step on the economic dimension.

## equation

none

## conditions

- The metric is posited. Chapter 18 says estimating it, its off-diagonal terms and its curvature is an open problem that needs trade-off and intensity questions that existing surveys do not ask.
- In practice the volume replaces the geodesic distance with the Mahalanobis distance computed from the electorate's covariance matrix. It gives this as an approximation for a region of roughly constant curvature.
- The echo-chamber case of Chapter 11 is a degenerate limit in which the graded metric becomes a step function, zero inside the group and infinite outside it.

Conditions are curated in `volumes/geometric-politics.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, and says a political-argument instrument is plausible but has not been built or gated. District 7, the source of nearly every number in the volume, is a fictional district, and Chapter 18 says precise estimation of the manifold needs larger and richer datasets than currently exist.

## first stated

Chapter 4, [`geometric-politics/manuscript/part_ii/ch04_preference_manifold.md:56-64`](https://github.com/ahb-sjsu/geometric-politics/blob/8f4a831/manuscript/part_ii/ch04_preference_manifold.md#L56-L64). Online, [Geometric Politics](https://erisml.org/geometric-politics/ch04_preference_manifold.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Politics*, Volume 10 of the Geometric Series.

## related

metric, mahalanobis-distance, geodesic-distance, sacred-value-singularity, political-preference-manifold

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
