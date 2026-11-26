# Spectral divergence from a corpus prior

**id.** aesthetic-spectral-divergence-channel
**kind.** instrument
**volume.** Geometric Aesthetics, Volume 13 of the Geometric Series

## definition

Fit a Gaussian to a work's embeddings and another to a reference corpus, both in a PCA subspace, and compute five divergences between them. They are Kullback-Leibler, Jensen-Shannon, Hellinger, Bhattacharyya, and the Mahalanobis distance of the work's mean from the prior mean.

**Example.** In one dimension, a work with mean 2 against a prior with mean 0 and variance 4 has Mahalanobis distance 2 divided by the prior standard deviation 2, which is 1.

## equation

none

## conditions

- Both distributions are modeled as multivariate Gaussians. Section 5.7 calls the per-work Gaussian an approximation.
- In the books discovery run each divergence registers at roughly 8 sigma against rating. That run is before genre control.
- In music the Hellinger member saturated near 1.0 and the divergences were recomputed in a 32-dimensional subspace.
- The prior is fitted on the English books corpus and is not neutral. A different corpus gives different distances.
- Appendix B says its code sketch computes a symmetrized Kullback-Leibler divergence under the name js, not the Jensen-Shannon divergence, and does not record which form produced the reported numbers. The volume's corrections record of 2026-11-26 lists this as open.

Conditions are curated in `volumes/geometric-aesthetics.toml` rather than read from a record.

## ledger

none. *standing.* A measured instrument. The closed forms of the divergences are marked proved in Appendix F (F4.2 to F4.5), and the 8 sigma figure is a discovery-run measurement that precedes the genre control.

## first stated

Section 17.3.1, [`geometric-aesthetics/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md:35-47`](https://github.com/ahb-sjsu/geometric-aesthetics/blob/dc255d3/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md#L35-L47). Online, [Geometric Aesthetics](https://erisml.org/geometric-aesthetics/chapter-17-empirical-evidence-for-geometric-aesthetics.html).

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

aesthetic-hellinger-saturation, aesthetic-genre-confound-correction, cross-lingual-aesthetic-invariance, kl-divergence, mahalanobis-distance, principal-component-analysis

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
