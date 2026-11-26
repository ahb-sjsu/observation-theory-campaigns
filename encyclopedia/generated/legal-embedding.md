# Legal embedding and dimension probes

**id.** legal-embedding
**kind.** instrument
**volume.** Geometric Law, Volume 5 of the Geometric Series

## definition

A function from legal documents to vectors of fixed dimension such that documents on the same legal issue have high cosine similarity and a change of wording or style moves the vector by less than a tolerance. Eight linear probes then read the eight legal dimension scores from the vector.

**Example.** With a tolerance of 0.05, an opinion and its plain-language restatement that embed 0.02 apart pass the style condition, and a pair 0.2 apart fails it. A probe whose linear score is 0 outputs 0.5, which the volume flags as uncertain.

**Known as, or related to prior art.** Sentence embeddings and linear probing classifiers.

## equation

none

## conditions

- The embedding is frozen at a fixed version and the probes are logistic regressions, so the same text always gives the same scores.
- Chapter 3 names the multilingual encoder LaBSE with 768 dimensions. Chapter 15 describes a legal-domain transformer for JurisGraph, the system of its running example.
- The probe accuracies the volume quotes, F1 from 0.74 to 0.91, are for the nine moral-dimension probes of the parent framework. For the legal probes it calls for about 200 expert-scored validation cases and at least 500 labeled cases per dimension.
- The front matter classes AI implementation as speculation or extension, and Chapter 4 states that the scoring and calibration programme has not yet been executed on legal data.

Conditions are curated in `volumes/geometric-law.toml` rather than read from a record.

## ledger

none. *standing.* This is the one corner the README of 2026-07-14 reports as instrumented. It says the legal text embedding LeBSE is validated in the xbse admission filter on US case law, with labels from the CourtListener citation graph, and that this covers structure preservation in legal text embeddings and not the book's broader jurisprudential claims. The chapters do not mention LeBSE or report that test.

## first stated

Chapter 15, [`geometric-law/chapters/ch15_ai_legal.md:56-66`](https://github.com/ahb-sjsu/geometric-law/blob/c05fb6b/chapters/ch15_ai_legal.md#L56-L66), with the formal conditions at [`geometric-law/chapters/ch15_ai_legal.md:475-485`](https://github.com/ahb-sjsu/geometric-law/blob/c05fb6b/chapters/ch15_ai_legal.md#L475-L485). The pipeline first appears in Chapter 3, [`geometric-law/chapters/ch03_judicial_complex.md:253-261`](https://github.com/ahb-sjsu/geometric-law/blob/c05fb6b/chapters/ch03_judicial_complex.md#L253-L261). Online, [Geometric Law](https://erisml.org/geometric-law/ch15_ai_legal.html).

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

embedding, encoder, eight-legal-dimensions, logistic-regression, legal-bond-index, posited-versus-measured

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
