# when hyperbolic embedding wins (Proposition 5.3)

**id.** hyperbolic-embedding-advantage-regime
**kind.** result
**volume.** Geometric Communication, Volume 7 of the Geometric Series

## definition

The advantage of a hyperbolic over a Euclidean embedding of a hierarchy grows with tree depth, with branching factor, and when the embedding dimension is fixed. It is negligible when the hierarchy is shallow (depth at most 3) and narrow (branching at most 4), when the dimension is unrestricted, or when the task does not depend on the tree.

**Example.** The coda taxonomy has 28 types and 3 distance levels in 16 dimensions, which the volume places in the negligible-advantage regime. There classical MDS reached a rank correlation of 0.79 and the Poincare embedding a lower one.

**Known as, or related to prior art.** The low-distortion tree embedding of Sarkar (2011) and the Poincare embeddings of Nickel and Kiela (2017), both cited by the chapter.

## equation

none

## conditions

- For the 28 sperm whale coda types in 16 dimensions the Euclidean baselines preserved taxonomic distance better. Classical MDS and PCA reached a Spearman correlation of 0.79, Isomap 0.77, and the Poincare embedding was lower. The chapter prints no value for it.
- The hyperbolic classifier reached 74.3% accuracy, which the chapter calls competitive with Euclidean baselines and not better. The split was random and not grouped by whale.
- The chapter says the decisive test would be a large hierarchy and that it has not run one. The scaling figure of Chapter 5 is simulated.

Conditions are curated in `volumes/geometric-communication.toml` rather than read from a record.

## ledger

none. *standing.* A proposition stated without proof, motivated by the cited tree-embedding theorems. On the volume's own two cases the hyperbolic embedding did not outperform Euclidean baselines, and the chapters say so.

## first stated

Proposition 5.3 and the paragraphs around it, [`geometric-communication/manuscript/part_ii/ch05_hyperbolic_embeddings.md:320-335`](https://github.com/ahb-sjsu/geometric-communication/blob/b0c1ca3/manuscript/part_ii/ch05_hyperbolic_embeddings.md#L320-L335), with the coda comparison in Section 7.2.2, [`geometric-communication/manuscript/part_iii/ch07_whale_communication.md:52-52`](https://github.com/ahb-sjsu/geometric-communication/blob/b0c1ca3/manuscript/part_iii/ch07_whale_communication.md#L52-L52). Online, [Geometric Communication](https://erisml.org/geometric-communication/ch05_hyperbolic_embeddings.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Communication*, Volume 7 of the Geometric Series.

## related

hyperbolic-attention-bias, spearman-correlation, distortion, embedding, split

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
