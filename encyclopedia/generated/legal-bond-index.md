# Legal Bond Index (LBI)

**id.** legal-bond-index
**kind.** instrument
**volume.** Geometric Law, Volume 5 of the Geometric Series

## definition

The mean, over test cases and bond-preserving transformations, of the size of the change in the legal outcome under the transformation divided by the size of the original outcome. A value of 0 is perfect invariance, and the index can be split by transformation type, such as race or sex.

**Example.** Sentences of 100, 50 and 80 months that become 110, 50 and 72 under a transformation change by 0.10, 0 and 0.10 of the original, so the normalized index is 0.20 / 3, about 0.067.

## equation

none

## conditions

- It needs a transformed version of each test case. The volume says submitting transformed cases to a real court is impractical, and that for AI legal systems the index is directly computable.
- The 0.155 baseline is the Bond Index of Geometric Ethics, from 20,030 normative evaluations. The volume says it is not a standard for legal systems and that the legal baseline remains to be measured.
- The volume says Sentencing Commission data suggests a racial index of about 0.19 for federal sentencing and does not give the computation. The per-judge and per-district figures in its running example illustrate the method.
- The definition varies across chapters. Chapters 5 and 8 state it unnormalized with a range of 0 to 1, the Chapter 8 appendix divides by the original outcome, and Chapter 15 uses Mahalanobis distances between system outputs with a suggested threshold of 0.05.

Conditions are curated in `volumes/geometric-law.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic status of 2026-07-14 calls the volume a posited framework with one instrumented corner. That corner is the legal text embedding LeBSE, validated in the xbse admission filter on US case law with labels from the CourtListener citation graph, and the README says this covers structure preservation in legal text embeddings and not the book's broader jurisprudential claims, which remain posited theory at licensed strength.

## first stated

Chapter 8, [`geometric-law/chapters/ch08_equal_protection.md:220-246`](https://github.com/ahb-sjsu/geometric-law/blob/1021d65/chapters/ch08_equal_protection.md#L220-L246), with the normalized form at [`geometric-law/chapters/ch08_equal_protection.md:472-476`](https://github.com/ahb-sjsu/geometric-law/blob/1021d65/chapters/ch08_equal_protection.md#L472-L476). Chapter 5 states it first in brief, [`geometric-law/chapters/ch05_hohfeldian_group.md:311-319`](https://github.com/ahb-sjsu/geometric-law/blob/1021d65/chapters/ch05_hohfeldian_group.md#L311-L319). Online, [Geometric Law](https://erisml.org/geometric-law/ch08_equal_protection.html).

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

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
