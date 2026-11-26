# Aesthetic manifold

**id.** aesthetic-manifold
**kind.** concept
**volume.** Geometric Aesthetics, Volume 13 of the Geometric Series

## definition

The space whose points are probability distributions on a modality-specific embedding space. A work is the distribution induced by its embedding cloud, the corpus is a reference distribution, and distances are divergences between distributions. In practice the volume works on the Gaussian submanifold of means and covariances.

**Example.** With embedding dimension d = 2 the Gaussian submanifold has dimension d + d(d+1)/2 = 2 + 3 = 5, two numbers for the mean and three for the symmetric covariance.

**Known as, or related to prior art.** The statistical manifold of information geometry, with the Fisher information metric on the Gaussian family.

## equation

none

## conditions

- The definition is marked informal. Appendix F lists the claim that the space is a Riemannian manifold with a positive-definite metric everywhere as conjectured (F5.3), with differentiable structure, metric smoothness and geodesic completeness not established.
- What Appendix F counts as verified is a finite-sample check. Pairwise feature distances on 4,998 books were strictly positive and satisfied the triangle inequality on sampled triples.
- The Gaussian fit keeps only the first two moments. Section 5.7 says embedding clouds are heavy-tailed and multi-modal, and it assigns the remainder to the trajectory level of the tensor hierarchy.
- Distances depend on the corpus chosen as prior. Section 5.4 says a different prior rearranges the absolute distances.

Conditions are curated in `volumes/geometric-aesthetics.toml` rather than read from a record.

## ledger

none. *standing.* Posited structure. Appendix F marks the manifold claim conjectured and marks only the finite-sample distance checks verified empirically.

## first stated

Definition 5.1 and the Gaussian restriction, [`geometric-aesthetics/book/src/chapter-05-the-aesthetic-manifold.md:27-35`](https://github.com/ahb-sjsu/geometric-aesthetics/blob/dc255d3/book/src/chapter-05-the-aesthetic-manifold.md#L27-L35). Online, [Geometric Aesthetics](https://erisml.org/geometric-aesthetics/chapter-5-the-aesthetic-manifold.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Aesthetics*, Volume 13 of the Geometric Series.

## related

aesthetic-embedding-cloud, aesthetic-tensor-hierarchy, aesthetic-regime, manifold, kl-divergence, gaussian

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
