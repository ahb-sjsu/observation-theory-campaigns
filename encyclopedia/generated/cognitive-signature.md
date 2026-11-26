# cognitive signature and signature distance

**id.** cognitive-signature
**kind.** instrument
**volume.** Geometric Cognition, Volume 6 of the Geometric Series

## definition

The vector of a model's normalized subtask scores, compared between models by Euclidean distance. Each subtask is rescaled so that the worst of the five models is 0 and the best is 1, with lower-is-better subtasks inverted.

**Example.** Signatures (1, 0) and (0, 1) have the same mean, 0.5, and a distance of the square root of 2, about 1.41. The volume's matrix prints 0.58 for Gemini 3 Flash and Gemini 2.5 Flash, its closest pair, and 1.03 for Claude and Gemini 2.0 Flash, its farthest.

## equation

none

## conditions

- The normalization uses the minimum and maximum across the five tested models, so a signature is relative to that set.
- Euclidean distance weights all subtasks equally. The volume names weighted, cosine and rank-based distances as alternatives that change the structure of the space.
- The ledger grades the claim of five distinct profile shapes exploratory (GC-16) and leaves the predictability of a signature from architecture open (GC-21).
- The signature distances of Section 16.10 rest on 21-score vectors the volume does not print, drafted beside table values that have since been corrected. The corrections record of 2026-11-26 lists them as still open.

Conditions are curated in `volumes/geometric-cognition.toml` rather than read from a record.

## ledger

none. *standing.* The README's status block of 2026-09-13 calls the book a domain exposition at posited, graded by a claim ledger converted from the manuscript with debt ratio 1.0, so every row is retrospective and no gate has been sealed in the repository. The ledger grades the benchmark statistics exploratory because their primary run records are not in the repository, and it holds every interpretation at posited because the admission filter xbse ruled the cognitive instrument inadmissible on 2026-07-14.

## first stated

Definitions 16.1 and 16.2, [`geometric-cognition/chapters/ch16_five_signatures.md:299-309`](https://github.com/ahb-sjsu/geometric-cognition/blob/93e39e2/chapters/ch16_five_signatures.md#L299-L309), with the normalization in Technical Appendix 16A, [`geometric-cognition/chapters/ch16_five_signatures.md:370-378`](https://github.com/ahb-sjsu/geometric-cognition/blob/93e39e2/chapters/ch16_five_signatures.md#L370-L378). Online, [Geometric Cognition](https://erisml.org/geometric-cognition/ch16_five_signatures.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Cognition*, Volume 6 of the Geometric Series.

## related

cognitive-profile-tensor, scalar-irrecoverability-theorem, capability-frontier-convergence, euclidean-distance, standardization

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
