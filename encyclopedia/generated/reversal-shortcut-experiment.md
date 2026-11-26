# gradient reversal shortcut experiment

**id.** reversal-shortcut-experiment
**kind.** result
**volume.** Geometric Methods, Volume 1 of the Geometric Series

## definition

On synthetic spectrograms in which the recording condition predicts the coda type 90% of the time, full gradient reversal lowered the domain head's training accuracy from 95.9% to 37.7%. A probe fitted afterwards still recovered the condition 99.9% of the time, and accuracy on the shifted test stayed at chance.

**Example.** P3 required the probe's accuracy to fall by at least 15 points under full reversal. It was 99.9% without reversal and 99.9% with it, a fall of 0.0, so P3 failed. The numbers are from the volume's recorded run.

**Known as, or related to prior art.** The finding of Elazar and Goldberg (2018) that an adversary at chance is compatible with a representation from which a fresh classifier recovers the attribute.

## equation

none

## conditions

- Three predictions with thresholds were written into the script before it ran. P1 and P2 held and P3 failed.
- Every setting was at chance on the shifted test, 16.7% to 17.6%, so no model learned the true signal. The experiment cannot say whether reversal helps a model that is able to learn it.
- The data are synthetic, each setting was run with three seeds, and the setting lambda 0.5 was run without a prediction.
- The section replaces an earlier version that used random data with random labels, a test that could not fail.

Conditions are curated in `volumes/geometric-methods.toml` rather than read from a record.

## ledger

none. *standing.* Three predictions registered in the script before it ran, graded on one recorded run of 16 November 2026. One of the three failed. Priority is shown by file hash, not by version-control ancestry (Section 21.8).

## first stated

Section 14.9, [`geometric-methods/chapters/chapter-14-gradient-reversal.md:774-791`](https://github.com/ahb-sjsu/geometric-methods/blob/d910c92/chapters/chapter-14-gradient-reversal.md#L774-L791). Online, [Geometric Methods](https://erisml.org/geometric-methods/chapter-14-gradient-reversal.html).

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

gradient-reversal-layer, preregistration, nuisance, chance-level, admissibility-checks, linear-classifier

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
