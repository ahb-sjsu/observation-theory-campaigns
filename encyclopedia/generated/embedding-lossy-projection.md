# ingredient embedding as a lossy projection

**id.** embedding-lossy-projection
**kind.** correction
**volume.** Geometric Gastronomy, Volume 12 of the Geometric Series

## definition

An ingredient embedding assigns each food one fixed vector. The volume models it as a lossy projection $\Pi$ that quotients out concentration, matrix context and time. Two foods with the same embedding can taste different, and no operation on the projected vector recovers what was discarded.

**Example.** Describe a food by a pair (direction, dose) and let the embedding keep the direction only. A blue cheese at dose 1 and the same cheese at dose 10 map to the same vector, so no function of the embedding tells them apart. This is the volume's case of the two blue cheeses, with illustrative doses.

## equation

none

## conditions

- Tagged a modeling axiom. It applies to compound vectors and to recipe-trained embeddings such as word2vec on ingredient lists.
- The volume says an embedding answers which directions, which neighbors and which feasible partners. It does not answer how much, in what form, in what order or against what background.
- The irrecoverability is cited from the scalar irrecoverability result of Volume 4 and is not proved in this volume.
- The statements that 10 to 15 principal components recover most of the variance, and that a 12-dimensional prefix predicts pairing nearly as well as the full vector, are tagged expected results with no run recorded for this volume. Appendix D.3 expects 20 to 30 components for the same purpose, and the volume's corrections record of 2026-11-26 lists the difference as unresolved.

Conditions are curated in `volumes/geometric-gastronomy.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, with no gastronomy instrument evaluated by the series' admission filter (xbse) and the nearest evaluated perceptual domains, aesthetics and music, rated inadmissible to medium. Its claims are to be read as theory at licensed strength and not as validated measurement, and the chapters tag each statement as a modeling axiom, empirical, a conjecture or a theorem. Since the corrections of 2026-11-26 the analyses the volume describes carry the tag that no run is recorded for this volume, and their outcomes are worded as predictions.

## first stated

Section 10.6, [`geometric-gastronomy/chapters/ch10_flavor_embeddings.md:100-108`](https://github.com/ahb-sjsu/geometric-gastronomy/blob/b43823b/chapters/ch10_flavor_embeddings.md#L100-L108). Online, [Geometric Gastronomy](https://erisml.org/geometric-gastronomy/ch10_flavor_embeddings.html).

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

quotient, projection, scalar-irrecoverability, embedding, null-space, flavor-space

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
