# Legal Bond Index (LBI)

**id.** legal-bond-index
**kind.** instrument
**volume.** Geometric Law, Volume 5 of the Geometric Series

## definition

An index with two kinds of form. The book's transformation forms take the mean, over test cases and bond-preserving transformations, of the size of the change in the legal outcome under the transformation, in the appendix divided by the size of the original outcome. A value of 0 is perfect invariance, and these forms are theoretical and have not been computed on legal data. The one form that has been measured is the matched-neighborhood ratio, the mean score gap between an individual and the $k$ nearest neighbors of the other group divided by the mean gap to the $k$ nearest neighbors of the same group, which is centered on 1.

**Example.** Sentences of 100, 50 and 80 months that become 110, 50 and 72 under a transformation change by 0.10, 0 and 0.10 of the original, so the normalized index is 0.20 / 3, about 0.067. For the measured form the chapter gives mean gaps at k = 20 of 2.323 deciles to neighbors of the other race and 2.215 to neighbors of the same race, and 2.323 / 2.215 is 1.049.

## equation

none

## conditions

- A transformation form needs a transformed version of each test case. The volume says submitting transformed cases to a real court is impractical, and that for AI legal systems the index is directly computable.
- The measured form was computed for COMPAS recidivism scores on the public Broward County file, for 5,278 defendants matched on six recorded predictors. For race the ratio lies between 1.041 and 1.069 across six neighborhood scales and is 1.049 at k = 20. Under specifications that force matching parity it falls to between 1.00 and 1.02. For sex it is not distinguishable from 1 at scales up to 20.
- The measurement comes from the paper The Legal Bond Index by Bond, accepted by the Journal of Science and Law and in press. The chapter says the paper makes no use of the book's framework, that the object measured is the score of an algorithm and not the judgment of a court, and that every finding is conditional on the measured predictors, which are a subset of those COMPAS uses.
- The paper describes the measured index as a research-stage screening signal and not a validated audit standard, and proposes no threshold. The chapter says an index above 1 does not show that the algorithm uses race and does not establish a violation of any legal rule.
- The scales cannot be converted. The chapter says a ratio of 1.049 is not an index of 0.049, and that it cannot be set beside 0.155, the illustrative 0.19 and 0.08, or the 0.05 threshold of Chapter 15.
- The 0.155 baseline is the Bond Index of Geometric Ethics, from 20,030 normative evaluations. The volume says it is not a standard for legal systems and that for the forms it defines the legal baseline remains unmeasured. The corrections record of 2026-11-26 lists the source of 0.155 as unresolved.
- The figure of about 0.19 for federal sentencing restates the Sentencing Commission's 19.1% as a relative change. The chapter says it is not a computation of the index from case data. The per-judge and per-district figures in the running example are illustrative.
- The transformation forms vary across chapters. Chapters 5 and 8 state the mean absolute change with a range of 0 to 1, the Chapter 8 appendix divides by the original outcome, and Chapter 15 uses Mahalanobis distances between system outputs with a suggested threshold of 0.05. The chapter says their values are not directly comparable, and the book has not fixed which of them is the definition.

Conditions are curated in `volumes/geometric-law.toml` rather than read from a record.

## ledger

none. *standing.* One form has been measured, once. The matched-neighborhood ratio was computed for the scores of one algorithm on one public dataset, in a paper that is accepted and in press, and the chapter reports it as a screening diagnostic and not as a test of the book's framework. The transformation forms the book defines are theoretical and have not been computed on legal data.

## first stated

Chapter 8, [`geometric-law/chapters/ch08_equal_protection.md:226-250`](https://github.com/ahb-sjsu/geometric-law/blob/1e50dfc/chapters/ch08_equal_protection.md#L226-L250), with the normalized form at [`geometric-law/chapters/ch08_equal_protection.md:631-635`](https://github.com/ahb-sjsu/geometric-law/blob/1e50dfc/chapters/ch08_equal_protection.md#L631-L635) and the measured form in the section The Measured Form of the Index, [`geometric-law/chapters/ch08_equal_protection.md:276-405`](https://github.com/ahb-sjsu/geometric-law/blob/1e50dfc/chapters/ch08_equal_protection.md#L276-L405). Chapter 5 states it first in brief, [`geometric-law/chapters/ch05_hohfeldian_group.md:321-331`](https://github.com/ahb-sjsu/geometric-law/blob/1e50dfc/chapters/ch05_hohfeldian_group.md#L321-L331). Online, [Geometric Law](https://erisml.org/geometric-law/ch08_equal_protection.html).

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

judicial-bond-invariance-principle, gauge-violation-tensor, equal-protection-gauge-invariance, paired, disparate-impact-ratio

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
