# Embedding cloud of a work

**id.** aesthetic-embedding-cloud
**kind.** concept
**volume.** Geometric Aesthetics, Volume 13 of the Geometric Series

## definition

The set $X(W)$ of vectors obtained by cutting a work $W$ into units (paragraphs, audio frames, image patches) and passing each unit through a fixed pretrained encoder. The work is treated as this cloud and not as a single point.

**Example.** The volume's cases are a 300-paragraph novel under LaBSE, which gives 300 points in 768 dimensions, and a 30-second clip under MERT at 1.5 frames per second, which gives 45 points in 1024 dimensions.

## equation

none

## conditions

- The encoder is a modeling choice. The volume uses LaBSE (768 dimensions) for text and MERT-v1-330M layer 7 (1024 dimensions) for music, and it says the empirical claims depend on these encoders.
- Images are named as compatible with the framework but the empirical chapters report on text and music only.
- The mean and covariance summaries discard the order of the units. Order is kept only in the trajectory features.
- Section 16.2 limits the construction to artifacts an encoder can embed. Live performance and conceptual art fall outside it.

Conditions are curated in `volumes/geometric-aesthetics.toml` rather than read from a record.

## ledger

none. *standing.* A construction, with encoders fixed by choice. The claim that aesthetic features of a work are geometric features of its cloud is called a candidate claim in Section 17.2.

## first stated

Section 5.2, [`geometric-aesthetics/book/src/chapter-05-the-aesthetic-manifold.md:41-45`](https://github.com/ahb-sjsu/geometric-aesthetics/blob/dc255d3/book/src/chapter-05-the-aesthetic-manifold.md#L41-L45). Restated in Section 17.2, [`geometric-aesthetics/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md:19-25`](https://github.com/ahb-sjsu/geometric-aesthetics/blob/dc255d3/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md#L19-L25). Online, [Geometric Aesthetics](https://erisml.org/geometric-aesthetics/chapter-5-the-aesthetic-manifold.html).

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

aesthetic-manifold, aesthetic-tensor-hierarchy, embedding, encoder, covariance-matrix

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
