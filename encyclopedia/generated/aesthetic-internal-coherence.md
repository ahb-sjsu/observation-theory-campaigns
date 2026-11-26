# Internal coherence (pair_sim_mean)

**id.** aesthetic-internal-coherence
**kind.** instrument
**volume.** Geometric Aesthetics, Volume 13 of the Geometric Series

## definition

The mean cosine similarity over all pairs of embeddings in a work's cloud. High values mean the work keeps returning to a narrow region of content space, and low values mean it ranges widely.

**Example.** A work with three units whose pairwise cosine similarities are 0.9, 0.5 and 0.4 has pair_sim_mean equal to 1.8 divided by 3, which is 0.6.

## equation

none

## conditions

- The statistic carries no built-in sign. Whether coherence goes with higher or lower reception is left to measurement.
- In books it correlates with Goodreads rating at $\rho = +0.126$ (8.4 sigma). In music it correlates with log listens at $\rho = -0.076$.
- Its value transfers across translations of the same book at a mean Spearman correlation of 0.712.
- Values are relative to the encoder. Section 17.8 says other encoders would give different values and, in principle, different signs.

Conditions are curated in `volumes/geometric-aesthetics.toml` rather than read from a record.

## ledger

none. *standing.* A measured instrument on two corpora. The sign of its association with reception reversed between books and music.

## first stated

Section 17.3.2, [`geometric-aesthetics/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md:49-57`](https://github.com/ahb-sjsu/geometric-aesthetics/blob/7a5e20e/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md#L49-L57). Online, [Geometric Aesthetics](https://erisml.org/geometric-aesthetics/chapter-17-empirical-evidence-for-geometric-aesthetics.html).

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

cross-modality-sign-flip, cross-lingual-aesthetic-invariance, aesthetic-trajectory-channel, cosine, spearman-correlation

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
