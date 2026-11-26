# Trajectory geometry channel

**id.** aesthetic-trajectory-channel
**kind.** instrument
**volume.** Geometric Aesthetics, Volume 13 of the Geometric Series

## definition

Summaries of the ordered path a work traces through embedding space. They are the mean step size between adjacent units, the recurrence rate of returns near earlier points, the discrete curvature at each unit, and the lag-1 autocorrelation of the top three PCA coordinates.

**Example.** A work whose three units sit at 0, 3 and 4 on a line takes steps of 3 and 1, so its mean step size is 2.

## equation

none

## conditions

- The features need the order of the units, which the mean and covariance summaries discard.
- In the books discovery run the features contribute at 3 to 6 sigma each. Section 10.9 says the effect shrinks substantially under within-genre residualization.
- The mean step size has opposite signs in the two modalities, $\rho = -0.096$ in books and $\rho = +0.071$ in music.
- Section 17.9 says the channel has no semantic interpretation yet beyond pacing and return to theme. The volume does not claim to have estimated manifold curvature from it.

Conditions are curated in `volumes/geometric-aesthetics.toml` rather than read from a record.

## ledger

none. *standing.* Measured features. Their reading as evidence of curvature or holonomy is posited, and Appendix F marks empirical holonomy as not yet implemented.

## first stated

Section 17.3.3, [`geometric-aesthetics/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md:59-68`](https://github.com/ahb-sjsu/geometric-aesthetics/blob/a32666e/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md#L59-L68). Online, [Geometric Aesthetics](https://erisml.org/geometric-aesthetics/chapter-17-empirical-evidence-for-geometric-aesthetics.html).

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

aesthetic-internal-coherence, cross-modality-sign-flip, style-holonomy, aesthetic-tensor-hierarchy, curvature

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
