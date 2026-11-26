# Clinical-moral boundaries

**id.** clinical-moral-boundaries
**kind.** concept
**volume.** Geometric Medicine, Volume 8 of the Geometric Series

## definition

Thresholds on the clinical decision complex where the decision regime changes discontinuously, each with a penalty added to the weight of any action that crosses it. Five are defined, namely harm, futility, consent, abandonment and sacred value. The sacred-value penalty is infinite, and the others are finite in at least some settings.

**Example.** Take a harm penalty of 10 and a futility penalty of 20, both inside the volume's typical ranges of 5 to 20 and 10 to 30. An action that crosses both adds 30 to its edge weight, and an action that crosses the sacred-value boundary has infinite weight whatever else it gains. The sum is arithmetic from the definition.

## equation

none

## conditions

- The penalty ranges are given as typical calibrations in normalized units. They are not measured, and Section 4.12 says they must be calibrated for specific clinical populations.
- The consent penalty is about infinite for a competent patient outside an emergency and drops to a finite value in an emergency or when the patient lacks capacity.
- The harm penalty is high but finite, so a minimum-cost path may pass through harm, as in surgery.
- Later chapters use penalties outside the five, for example a trust penalty and a justice penalty in Theorem 10.1, without adding them to this definition.

Conditions are curated in `volumes/geometric-medicine.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, and says a clinical instrument is plausible but has not been built or gated. Its Section 18.9 says the framework has no direct empirical validation and the clinical Bond Index has not been computed from clinical data, and its front matter says the covariance matrix has not been estimated, so every number in these entries is an illustration unless the entry says otherwise.

## first stated

Definition 4.3, [`geometric-medicine/manuscript/part_ii/ch04_clinical_manifold.md:165-175`](https://github.com/ahb-sjsu/geometric-medicine/blob/4578fc5/manuscript/part_ii/ch04_clinical_manifold.md#L165-L175). Online, [Geometric Medicine](https://erisml.org/geometric-medicine/ch04_clinical_manifold.html).

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

clinical-edge-weight, clinical-decision-complex, absorbing-stratum, clinical-moral-injury, clinical-heuristic-admissibility

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
