# Cross-lingual invariance of the geometric features

**id.** cross-lingual-aesthetic-invariance
**kind.** result
**volume.** Geometric Aesthetics, Volume 13 of the Geometric Series

## definition

For the same book in English and in another language, the channel values computed in the fixed English PCA-128 basis agree. The mean Spearman correlation across language pairs is 0.712 for internal coherence, 0.710 for the Mahalanobis feature, and about 0.675 for the Hellinger, Bhattacharyya and Jensen-Shannon divergences.

**Example.** A mean correlation of 0.70 squares to 0.49, which is the volume's statement that about half the variance in the channel values is preserved across languages and half is not.

## equation

none

## conditions

- The corpus is 4,683 non-English Gutenberg books. Matched bundles, a book with its translation, formed at or above the threshold of 20 bundles per language in ten languages from six families (Germanic, Uralic, Romance, Hellenic, Italic-ancient, Constructed), from Finnish at 288 down to Latin at 20.
- Sinitic is absent because the Chinese Gutenberg texts are classical originals and not translations. The volume calls any claim of full linguistic universality premature.
- The invariance is partial. A correlation near 0.70 leaves about half the variance of the channel values unpreserved, and the volume says it does not claim gauge invariance in the strong sense.
- It is a result about feature values, not verdicts. Rating transfer from an English-trained model is R = 0.07 (n = 940, p = 0.033). Appendix E grants that LaBSE was trained to align translated sentences and answers that the features are cloud statistics, not sentence-pair similarity.

Conditions are curated in `volumes/geometric-aesthetics.toml` rather than read from a record.

## ledger

none. *standing.* Verified empirically in Appendix F (F12.1, F12.2, F12.4). Its reading as a Noether conservation law is marked analogy (F12.3).

## first stated

Section 17.5.2, [`geometric-aesthetics/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md:119-135`](https://github.com/ahb-sjsu/geometric-aesthetics/blob/dc255d3/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md#L119-L135). Setup in Section 17.5.1, [`geometric-aesthetics/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md:113-117`](https://github.com/ahb-sjsu/geometric-aesthetics/blob/dc255d3/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md#L113-L117). Online, [Geometric Aesthetics](https://erisml.org/geometric-aesthetics/chapter-17-empirical-evidence-for-geometric-aesthetics.html).

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

aesthetic-invariance-claim, aesthetic-internal-coherence, aesthetic-spectral-divergence-channel, aesthetic-falsification-criteria, spearman-correlation

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
