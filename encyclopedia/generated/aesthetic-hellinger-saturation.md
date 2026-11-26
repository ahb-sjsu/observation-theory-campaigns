# Hellinger saturation in music

**id.** aesthetic-hellinger-saturation
**kind.** correction
**volume.** Geometric Aesthetics, Volume 13 of the Geometric Series

## definition

In the music corpus the Hellinger feature saturated to about 1.0, because a Gaussian was being fitted to about 45 audio tokens per clip in a 128-dimensional PCA subspace. The volume recomputed the divergences in a 32-dimensional subspace and used the Bhattacharyya divergence directly as a check.

**Example.** With about 45 tokens per clip the sample covariance has rank at most 44, which is less than the 128 dimensions of the first fit and more than the 32 dimensions of the refit.

## equation

none

## conditions

- The cause is few samples in many dimensions. It applies to 30-second clips and not to the books corpus.
- The hand-feature result changed with the fix, from R = 0.124 to R = 0.098, and the volume reports the lower number.
- The volume says the substantive findings are unchanged and that the sign flip persists after the fix.

Conditions are curated in `volumes/geometric-aesthetics.toml` rather than read from a record.

## ledger

none. *standing.* A reported measurement failure and its repair. Section 17.7 lists the raw Hellinger feature in music among the features that were discarded.

## first stated

Section 17.6.1, [`geometric-aesthetics/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md:151`](https://github.com/ahb-sjsu/geometric-aesthetics/blob/a32666e/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md#L151). Its cause is given in Section 5.2, [`geometric-aesthetics/book/src/chapter-05-the-aesthetic-manifold.md:59`](https://github.com/ahb-sjsu/geometric-aesthetics/blob/a32666e/book/src/chapter-05-the-aesthetic-manifold.md#L59). Online, [Geometric Aesthetics](https://erisml.org/geometric-aesthetics/chapter-17-empirical-evidence-for-geometric-aesthetics.html).

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

aesthetic-spectral-divergence-channel, music-reception-geometry-result, cross-modality-sign-flip, gaussian, covariance-matrix

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
