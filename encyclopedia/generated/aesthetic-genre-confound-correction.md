# Genre confound correction (books)

**id.** aesthetic-genre-confound-correction
**kind.** correction
**volume.** Geometric Aesthetics, Volume 13 of the Geometric Series

## definition

The books discovery result, R = 0.241 between cloud geometry and Goodreads rating on 4,998 books, was mostly genre. After residualizing rating against Library of Congress top-level genre the result is R = 0.093 (R squared 0.009, 6.5 sigma), and the volume reports that figure as the result.

**Example.** R squared falls from 0.241 squared, about 0.058, to 0.093 squared, about 0.009. The share removed is 1 minus 0.009 divided by 0.058, about 0.85, the volume's 85 percent.

## equation

none

## conditions

- 85 percent of the discovery R squared was genre confound. The volume's summary is that geometry carries additional signal beyond genre, not that geometry predicts rating.
- Within Fiction (n = 2,250) the signal reproduces at R = 0.131 (6.2 sigma). Within Non-fiction and History/Biography the result is null.
- The corpus is English-language Project Gutenberg books paired with average Goodreads rating, with author-disjoint 5-fold cross-validation and LaBSE embeddings.
- Section 17.8 says the effect is too small to predict the reception of an individual work and that no causal claim is made.

Conditions are curated in `volumes/geometric-aesthetics.toml` rather than read from a record.

## ledger

none. *standing.* Verified empirically in Appendix F (F17.1 to F17.5), with the nulls listed as nulls. The README calls the structural-channels finding the volume's one validated result and says it was pre-registered. The book chapters do not describe the registration.

## first stated

Section 17.4.2, [`geometric-aesthetics/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md:95-105`](https://github.com/ahb-sjsu/geometric-aesthetics/blob/dc255d3/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md#L95-L105). The discovery figure it corrects is at [`geometric-aesthetics/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md:84-93`](https://github.com/ahb-sjsu/geometric-aesthetics/blob/dc255d3/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md#L84-L93). Online, [Geometric Aesthetics](https://erisml.org/geometric-aesthetics/chapter-17-empirical-evidence-for-geometric-aesthetics.html).

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

lasso-on-spectrum-channel, aesthetic-regime, music-reception-geometry-result, confound, residualization, cross-validation

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
