# Music reception result (FMA-Medium)

**id.** music-reception-geometry-result
**kind.** result
**volume.** Geometric Aesthetics, Volume 13 of the Geometric Series

## definition

On 24,801 FMA-Medium tracks with MERT embeddings and log listens as target, Lasso on the PCA spectrum gives R = 0.302 raw and R = 0.177 (28.3 sigma) after genre residualization. Hand features fall to R = 0.043 after residualization.

**Example.** For the spectrum channel R squared is 0.302 squared, about 0.091, before genre control and 0.177 squared, about 0.031, after it, so about two thirds of that channel's raw R squared was genre.

## equation

none

## conditions

- 91 percent of the hand-feature R squared is genre, and Appendix F gives about 66 percent for the spectrum Lasso. The raw hand-feature figure was first R = 0.124 and is reported as R = 0.098 after the Hellinger fix. With the residual of 0.043 neither gives 91 percent, and the volume's corrections record of 2026-11-26 lists the raw value behind the 91 percent as open.
- Within genre the signal holds for Rock, Electronic, Hip-Hop and Pop (R from 0.139 to 0.185). Classical (R = -0.013, n = 584) and Jazz (R = 0.031, n = 384) are null, and the volume says it does not know why.
- Listens conflate quality with promotion, genre popularity and platform effects. The volume calls them the only large-scale reception signal available for the corpus.
- On the 5,233 tracks with Echonest annotations the MERT features beat Spotify's 8 acoustic features (R = 0.225 and 0.151 against 0.103, bootstrap p = 0.001). The clips are 30 seconds and the folds are artist-disjoint.

Conditions are curated in `volumes/geometric-aesthetics.toml` rather than read from a record.

## ledger

none. *standing.* Verified empirically in Appendix F (F21.1 to F21.5), with the Classical and Jazz nulls listed. It is a correlation on one corpus with one encoder and one reception proxy.

## first stated

Section 17.6.2, [`geometric-aesthetics/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md:153-170`](https://github.com/ahb-sjsu/geometric-aesthetics/blob/dc255d3/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md#L153-L170). Setup in Section 17.6.1, [`geometric-aesthetics/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md:149-151`](https://github.com/ahb-sjsu/geometric-aesthetics/blob/dc255d3/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md#L149-L151). Online, [Geometric Aesthetics](https://erisml.org/geometric-aesthetics/chapter-17-empirical-evidence-for-geometric-aesthetics.html).

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

aesthetic-genre-confound-correction, lasso-on-spectrum-channel, aesthetic-hellinger-saturation, cross-modality-sign-flip, residualization, confound

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
