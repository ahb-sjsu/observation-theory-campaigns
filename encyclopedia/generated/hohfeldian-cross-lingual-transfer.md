# cross-lingual transfer of Hohfeldian classification (BIP experiment)

**id.** hohfeldian-cross-lingual-transfer
**kind.** result
**volume.** Geometric Communication, Volume 7 of the Geometric Series

## definition

An encoder with an adversarially trained bond space, trained on 3.9 million Hebrew and Aramaic passages, classified the Hohfeldian relation (Right, Duty, Liberty, No-Right) of 68,000 English Dear Abby letters with macro F1 of 44.5%, against a chance level of 25% and an in-distribution ceiling of 79.99% from mixed training.

**Example.** From the volume's figures, 44.5 divided by 79.99 is 0.556, the transfer efficiency of 55.6%. The transfer F1 exceeds the four-class chance level by 44.5 - 25 = 19.5 points.

## equation

none

## conditions

- The chapter states a 95% interval of 42.1% to 46.9%, an accuracy of 50.7%, and a transfer efficiency of 55.6% (transfer F1 over control F1). The labels were assigned by pattern matching on deontic words such as must, may and entitled, a method the chapter calls deliberately noisy.
- The encoder was pretrained on more than 50 languages, Hebrew and English among them. The chapter says a test with two independent monolingual encoders remains future work.
- The chapter says the experiment shows invariance of relational structure, not of substantive moral conclusions, and that the claim is bounded by the traditions tested.
- The per-language table of Section 11.3.2 gives 41.5% for English. The volume's corrections record of 2026-11-26 lists the difference from the 44.5% of Section 11.3.1 as unresolved.
- A language probe on the bond space is reported at 0.0% accuracy, below the 25% chance level. The chapter now says that an accuracy below chance is not chance and that the figure does not by itself show the bond space carries no linguistic information.

Conditions are curated in `volumes/geometric-communication.toml` rather than read from a record.

## ledger

none. *standing.* An experiment the chapter reports with intervals and limitations. Under the README's status note of 2026-07-14 no instrument of this volume has passed the series' admission filter.

## first stated

Section 11.3.1, [`geometric-communication/manuscript/part_v/ch11_cross_lingual.md:183-196`](https://github.com/ahb-sjsu/geometric-communication/blob/22f0bb0/manuscript/part_v/ch11_cross_lingual.md#L183-L196), with the control ceiling in Section 11.3.4, [`geometric-communication/manuscript/part_v/ch11_cross_lingual.md:219-226`](https://github.com/ahb-sjsu/geometric-communication/blob/22f0bb0/manuscript/part_v/ch11_cross_lingual.md#L219-L226). Online, [Geometric Communication](https://erisml.org/geometric-communication/ch11_cross_lingual.html).

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

gradient-reversal-layer, bond-index, communication-bond-invariance-principle, chance-level, leakage, selective-path-dependence

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
