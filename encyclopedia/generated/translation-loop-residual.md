# translation loop residual

**id.** translation-loop-residual
**kind.** instrument
**volume.** Geometric Communication, Volume 7 of the Geometric Series

## definition

For a text t and a chain of translations that returns to the starting language with result $\hat{t}$, the residual is $\rho(t) = 1 - \mathrm{sim}(t, \hat{t})$, where sim is a semantic similarity measure on the starting language. The volume uses it as a proxy for sectional curvature and as the empirical counterpart of holonomy.

**Example.** A round trip that returns a text with similarity 0.92 to the original has a residual of 1 - 0.92 = 0.08, the volume's mean for commercial records. Its mean for private letters, 0.31, is about 3.9 times that.

**Known as, or related to prior art.** Round-trip or back-translation evaluation in machine translation.

## equation

none

## conditions

- The value depends on the chosen similarity measure and on the translation systems in the chain. In the Old Assyrian run the similarity was chrF++ on the Akkadian transliteration and the return leg was a backtranslation by the trained model.
- The chapter reports mean residuals of 0.08 for commercial records, 0.14 for contracts, 0.23 for legal proceedings and 0.31 for private letters over 1,561 pairs, with F(3, 1557) = 142.7.
- Reading the residual as curvature of the content manifold is the volume's interpretation. The residual also contains the errors of the systems in the chain, which the chapter's own decomposition calls path error and chart error.
- A second table gives residuals with and without the hyperbolic attention bias. Chapter 9 says it does not report final numbers for that ablation.

Conditions are curated in `volumes/geometric-communication.toml` rather than read from a record.

## ledger

none. *standing.* A defined quantity with one reported run. The identification with curvature is posited, in the sense of the README's status note of 2026-07-14.

## first stated

Definition 10.7 and the genre table, [`geometric-communication/manuscript/part_iv/ch10_translation.md:196-213`](https://github.com/ahb-sjsu/geometric-communication/blob/8184f3a/manuscript/part_iv/ch10_translation.md#L196-L213). Online, [Geometric Communication](https://erisml.org/geometric-communication/ch10_translation.html).

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

language-chart, translation-error-decomposition, moral-holonomy, curvature, hyperbolic-attention-bias

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
