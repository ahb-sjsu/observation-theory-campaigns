# food-pairing hypothesis as cosine similarity

**id.** food-pairing-cosine-hypothesis
**kind.** concept
**volume.** Geometric Gastronomy, Volume 12 of the Geometric Series

## definition

Represent each ingredient by a binary compound vector, with a 1 for each compound it contains. The food-pairing hypothesis is then the claim that pairing quality rises with the cosine of two such vectors, the number of shared compounds divided by the square roots of the two compound counts.

**Example.** An ingredient with 4 compounds and one with 9, sharing 3, have cosine 3 / (2 times 3) = 0.5. Two ingredients with no shared compound have cosine 0. The counts are illustrative.

**Known as, or related to prior art.** The food-pairing hypothesis of Blumenthal and Benzi, tested on recipe data by Ahn, Ahnert, Bagrow and Barabasi (2011).

## equation

none

## conditions

- The volume calls the hypothesis half a theory. It describes similarity pairing, which the volume places in Western cuisine, and it does not describe complementarity.
- In the flavor network of Ahn et al. (2011) East Asian cuisines pair ingredients that share fewer compounds than chance, so the hypothesis is not a universal law.
- The binary vector ignores concentration and odor thresholds. The volume's phrase is that presence is not perception.
- A single scalar angle cannot separate echoing from completing. The volume adds span and curvature terms to it.

Conditions are curated in `volumes/geometric-gastronomy.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, with no gastronomy instrument evaluated by the series' admission filter (xbse) and the nearest evaluated perceptual domains, aesthetics and music, rated inadmissible to medium. Its claims are to be read as theory at licensed strength and not as validated measurement, and the chapters tag each statement as a modeling axiom, empirical, a conjecture or a theorem. Since the corrections of 2026-11-26 the analyses the volume describes carry the tag that no run is recorded for this volume, and their outcomes are worded as predictions.

## first stated

Section 4.1, [`geometric-gastronomy/chapters/ch04_similarity_and_complementarity.md:32-36`](https://github.com/ahb-sjsu/geometric-gastronomy/blob/b43823b/chapters/ch04_similarity_and_complementarity.md#L32-L36). Online, [Geometric Gastronomy](https://erisml.org/geometric-gastronomy/ch04_similarity_and_complementarity.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Gastronomy*, Volume 12 of the Geometric Series.

## related

cosine, bag-of-words, hub, western-eastern-pairing-asymmetry, pairing-alignment-span-curvature

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
