# Eight legal dimensions

**id.** eight-legal-dimensions
**kind.** concept
**volume.** Geometric Law, Volume 5 of the Geometric Series

## definition

Eight axes along which a legal state is scored. They are entitlement structure, factual nexus, procedural posture, statutory authority, constitutional conformity, precedential constraint, remedial scope and public interest. The eight scores of a case form its attribute vector.

**Example.** The volume's illustrative vector for Crawford v. Marion County is (0.7, 0.5, 0.9, 0.5, 0.7, 0.8, 0.6, 0.7), so it scores 0.9 on procedural posture and 0.5 on statutory authority.

## equation

none

## conditions

- The volume says the choice of eight is a modeling decision, not a derivation from first principles and not the unique correct decomposition. Chapter 1 tags it as a modeling axiom.
- Dimensions may be added or merged. The stated requirement is several non-redundant axes of legal variation, and the later theorems are said to hold for any finite-dimensional attribute space.
- The scores are to come from linear probes on a text embedding, trained on expert labels. Chapter 4 states that this programme has not yet been executed on legal data.
- Chapter 15 requires that no pair of predicted scores correlate above 0.7 on held-out cases. Otherwise the probes are retrained or the dimensions redefined.

Conditions are curated in `volumes/geometric-law.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic status of 2026-07-14 calls the volume a posited framework with one instrumented corner. That corner is the legal text embedding LeBSE, validated in the xbse admission filter on US case law with labels from the CourtListener citation graph, and the README says this covers structure preservation in legal text embeddings and not the book's broader jurisprudential claims, which remain posited theory at licensed strength.

## first stated

Chapter 3, [`geometric-law/chapters/ch03_judicial_complex.md:44-86`](https://github.com/ahb-sjsu/geometric-law/blob/1021d65/chapters/ch03_judicial_complex.md#L44-L86). Online, [Geometric Law](https://erisml.org/geometric-law/ch03_judicial_complex.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Law*, Volume 5 of the Geometric Series.

## related

judicial-complex, legal-mahalanobis-distance, legal-embedding, covariance-matrix

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
