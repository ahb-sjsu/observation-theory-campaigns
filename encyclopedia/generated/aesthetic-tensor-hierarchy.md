# Aesthetic tensor hierarchy

**id.** aesthetic-tensor-hierarchy
**kind.** concept
**volume.** Geometric Aesthetics, Volume 13 of the Geometric Series

## definition

Four levels of description of a work's embedding cloud. Level 1 is the mean displacement from the corpus prior, Level 2 the covariance with its divergences and internal coherence, Level 3 the trajectory statistics of the ordered sequence, and Level 4 the axes selected by Lasso on the PCA spectrum. A scalar rating sits below all four.

**Example.** In the ladder the volume expects for its books discovery run, Level 1 alone gives R of about 0.08, adding Level 2 gives 0.18, adding Level 3 gives 0.21 and adding Level 4 gives the measured 0.24 of the combined model, so the expected increments are 0.10, 0.03 and 0.03.

## equation

none

## conditions

- Higher levels can be contracted to a scalar prediction but a scalar does not reconstruct the levels above it.
- Levels 1 to 3 are computed in closed form from the cloud. Level 4 is learned and needs a target such as rating or listens, so it depends on that target.
- The values of R per level (about 0.08, 0.18, 0.21, 0.24) are given in Section 6.7 as an expectation and not a measurement, since Chapter 17 does not record the level-by-level fits. Only the 0.24 of the combined model is measured, in the books discovery run before genre control, and the volume attributes 85 percent of that run's R squared to genre.
- Appendix F marks rank-2 and higher tensors on the manifold as conjectured pending the smooth-manifold claim (F6.3).

Conditions are curated in `volumes/geometric-aesthetics.toml` rather than read from a record.

## ledger

none. *standing.* A posited organization of measured features. Only the combined model of the uncontrolled books run is measured, the per-level increments are an expectation, and the tensor objects on the manifold are conjectured in Appendix F.

## first stated

Section 6.1, [`geometric-aesthetics/book/src/chapter-06-the-tensor-hierarchy.md:11-20`](https://github.com/ahb-sjsu/geometric-aesthetics/blob/dc255d3/book/src/chapter-06-the-tensor-hierarchy.md#L11-L20). Online, [Geometric Aesthetics](https://erisml.org/geometric-aesthetics/chapter-6-the-tensor-hierarchy.html).

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

aesthetic-embedding-cloud, aesthetic-spectral-divergence-channel, aesthetic-internal-coherence, aesthetic-trajectory-channel, lasso-on-spectrum-channel, aesthetic-scalar-irrecoverability

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
