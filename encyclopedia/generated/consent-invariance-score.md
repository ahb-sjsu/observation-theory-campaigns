# Consent invariance score

**id.** consent-invariance-score
**kind.** instrument
**volume.** Geometric Medicine, Volume 8 of the Geometric Series

## definition

For a set of $m$ meaning-preserving transformations of the clinical information, the share of them under which the patient's decision stays the same. A score of 1 means the decision is invariant under all tested transformations, and 0 means it changes under every one.

**Example.** A patient is tested under 5 reframings and keeps the same decision under 4 of them. The score is 4 / 5 = 0.8, which just meets the volume's example threshold of 0.8, and the one failed reframing shows where more explanation is needed. The count of 5 is arithmetic from the definition.

## equation

none

## conditions

- The score depends on which transformations are in the set, and it says nothing about transformations not tested.
- It is proposed as a supplement to the legal consent checklist and not a replacement.
- The threshold of 0.8 is given as an example of an institutional standard. No study with the score is reported. The pilot of Section 17.6 is labelled an illustrative scenario with invented numbers.

Conditions are curated in `volumes/geometric-medicine.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, and says a clinical instrument is plausible but has not been built or gated. Its Section 18.9 says the covariance matrix has not been estimated and the clinical Bond Index has not been computed from clinical data, so every number in these entries is an illustration unless the entry says otherwise.

## first stated

Definition 8.4, [`geometric-medicine/manuscript/part_ii/ch08_consent_gauge.md:265-269`](https://github.com/ahb-sjsu/geometric-medicine/blob/c220ac9/manuscript/part_ii/ch08_consent_gauge.md#L265-L269). Online, [Geometric Medicine](https://erisml.org/geometric-medicine/ch08_consent_gauge.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Medicine*, Volume 8 of the Geometric Series.

## related

consent-gauge-invariance, medical-bond-invariance-principle, bond-index, paraphrase-class

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
