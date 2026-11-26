# Lasso-on-spectrum channel

**id.** lasso-on-spectrum-channel
**kind.** instrument
**volume.** Geometric Aesthetics, Volume 13 of the Geometric Series

## definition

Compute the per-component variances of a work's cloud in a fixed 128-component PCA basis learned from a reference corpus, then fit an L1-regularized linear model from those variances to the reception target. The nonzero coefficients name the PCA directions that align with reception.

**Example.** In the books experiment 71 of the 128 PCA coordinates get nonzero weight, so the L1 penalty set the other 57 coefficients to zero.

**Known as, or related to prior art.** Lasso regression (L1-regularized least squares) applied to PCA variance features.

## equation

none

## conditions

- In the books experiment 71 of 128 coordinates receive nonzero weight, and on inspection they read as genre axes. The channel therefore exposes the genre confound as well as predicting.
- Appendix F counts about 30 of the 71 axes as having interpretable genre or form correlates (F14.2).
- In music the channel gives R = 0.302 raw and R = 0.177 after genre residualization.
- The selected axes depend on the regression target, the corpus and the encoder. Chapter 6 and Chapter 17 both give the selection as 71 of 128 axes. They still differ on the feature, since Chapter 17 regresses on the per-component variances and Chapter 6 and the Appendix B code on the mean projections, and the volume's corrections record of 2026-11-26 lists this as unresolved.

Conditions are curated in `volumes/geometric-aesthetics.toml` rather than read from a record.

## ledger

none. *standing.* A measured instrument. The interpretation of the selected axes is post-hoc inspection, and their reading as discovered canonical directions in Chapter 14 is posited.

## first stated

Section 17.3.4, [`geometric-aesthetics/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md:70-78`](https://github.com/ahb-sjsu/geometric-aesthetics/blob/dc255d3/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md#L70-L78). Online, [Geometric Aesthetics](https://erisml.org/geometric-aesthetics/chapter-17-empirical-evidence-for-geometric-aesthetics.html).

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

aesthetic-genre-confound-correction, music-reception-geometry-result, collective-aesthetic-tensor, principal-component-analysis, explained-variance

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
