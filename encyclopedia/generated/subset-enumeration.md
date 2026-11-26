# subset enumeration

**id.** subset-enumeration
**kind.** instrument
**volume.** Geometric Methods, Volume 1 of the Geometric Series

## definition

Optimize and score every subset of the n parameter dimensions up to a maximum size, holding the dimensions outside the subset at an inactive sentinel value. The number of subsets of size 1 to k is the sum of the binomial coefficients n choose j for j from 1 to k.

**Example.** For the volume's 5 feature groups there are 5, 10, 10, 5 and 1 subsets of sizes 1 to 5, which is 31 in all and 30 with the size capped at 4.

## equation

none

## conditions

- Full enumeration is practical only for about 15 dimensions or fewer, depending on the cost of one evaluation. A cap on subset size trades completeness for tractability.
- The statement that subsets larger than four add little is the volume's expectation, not a measurement, and the tables of Chapter 11 are posited.
- A best subset chosen on the data that score it is not a finding. In the recorded run of Chapter 19 the winner won on one test module, and over 20 redraws of the generator 15 different subsets won.

Conditions are curated in `volumes/geometric-methods.toml` rather than read from a record.

## ledger

none. *standing.* The README's status note of 2026-07-14 calls this volume the series' metrology discipline, a method that is normative and not a finding. Its Section 21.8 (November 2026) classes each result as proved, posited, or measured on a recorded run, and the tables of Chapters 1, 8, 9, 11 and 12 are posited illustrations.

## first stated

Chapter 11, [`geometric-methods/chapters/chapter-11-subset-enumeration.md:6-8`](https://github.com/ahb-sjsu/geometric-methods/blob/371478c/chapters/chapter-11-subset-enumeration.md#L6-L8), with the counts in Section 11.1.1, [`geometric-methods/chapters/chapter-11-subset-enumeration.md:18-36`](https://github.com/ahb-sjsu/geometric-methods/blob/371478c/chapters/chapter-11-subset-enumeration.md#L18-L36). Online, [Geometric Methods](https://erisml.org/geometric-methods/chapter-11-subset-enumeration.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Methods*, Volume 1 of the Geometric Series.

## related

pareto-dominance, pairwise-interaction-matrix, sweep, defect-campaign-null-result, split

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
