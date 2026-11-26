# fusion as a geodesic between cuisines

**id.** fusion-geodesic
**kind.** concept
**volume.** Geometric Gastronomy, Volume 12 of the Geometric Series

## definition

A fusion dish is modeled as a point on the geodesic between two cuisine distributions under the Wasserstein metric on Gaussians. The means interpolate linearly and the covariances along a curved path of valid covariances. A mixture $(1-t)\,p_A + t\,p_B$ is bimodal and is not fusion. Curdling is leaving the support of both parents.

**Example.** In one dimension, two Gaussians with means 0 and 10 and standard deviations 1 and 3 have a Wasserstein midpoint with mean 5 and standard deviation 2, a single cloud. Their half-and-half mixture also has mean 5 and keeps two modes, near 0 and near 10. The numbers are illustrative.

**Known as, or related to prior art.** Displacement interpolation in optimal transport, the Wasserstein geodesic between Gaussian distributions.

## equation

none

## conditions

- Tagged a modeling axiom. It treats each cuisine as a Gaussian with a mean and a covariance.
- Interpolation is stable on dimensions where both covariances have support. Where one cuisine has variance and the other has none, the volume says the transport map has nothing to transport to.
- The mole and dashi case is the chapter's running example. No distance or covariance is computed for it.

Conditions are curated in `volumes/geometric-gastronomy.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, with no gastronomy instrument evaluated by the series' admission filter (xbse) and the nearest evaluated perceptual domains, aesthetics and music, rated inadmissible to medium. Its claims are to be read as theory at licensed strength and not as validated measurement, and the chapters tag each statement as a modeling axiom, empirical, a conjecture or a theorem. Since the corrections of 2026-11-26 the analyses the volume describes carry the tag that no run is recorded for this volume, and their outcomes are worded as predictions.

## first stated

Section 9.4, [`geometric-gastronomy/chapters/ch09_the_eigenvalues_of_a_kitchen.md:60-64`](https://github.com/ahb-sjsu/geometric-gastronomy/blob/b43823b/chapters/ch09_the_eigenvalues_of_a_kitchen.md#L60-L64). Online, [Geometric Gastronomy](https://erisml.org/geometric-gastronomy/ch09_the_eigenvalues_of_a_kitchen.html).

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

cuisine-flavor-eigenvectors, geodesic-distance, covariance-matrix, positive-semidefinite, gaussian

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
