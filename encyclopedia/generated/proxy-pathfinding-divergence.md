# Proxy pathfinding divergence

**id.** proxy-pathfinding-divergence
**kind.** result
**volume.** Geometric Medicine, Volume 8 of the Geometric Series

## definition

When a proxy decides for a patient, the search runs on the patient's complex with the proxy's heuristic. The distance between the proxy's path and the patient's own is at most a constant $K$ times the largest difference between the two heuristics, and no calibration can guarantee that difference is small without direct knowledge of the patient's heuristic.

**Example.** If the constant is 2 and the proxy's and the patient's heuristics differ by at most 3 at any state, the bound on the distance between their paths is 2 times 3 = 6. In the volume's case the son sets the futility penalty to 0 where the patient might have set it high. The numbers 2 and 3 are arithmetic from the statement.

## equation

none

## conditions

- The constant is said to depend on the curvature of the clinical decision complex. Neither the constant nor the distance between two paths is defined.
- The theorem is stated without a proof.
- It applies when the patient lacks capacity, so the patient's heuristic cannot be observed directly. The volume's remedy is to elicit the patient's values indirectly before major decisions.

Conditions are curated in `volumes/geometric-medicine.toml` rather than read from a record.

## ledger

none. *standing.* Labelled a theorem and stated without proof. The volume reads it as a structural limitation, that proxy pathfinding is fundamentally uncertain.

## first stated

Theorem 9.1, [`geometric-medicine/manuscript/part_iii/ch09_clinical_cases.md:280-286`](https://github.com/ahb-sjsu/geometric-medicine/blob/6c8c4c4/manuscript/part_iii/ch09_clinical_cases.md#L280-L286), after Definition 9.2 at [`geometric-medicine/manuscript/part_iii/ch09_clinical_cases.md:266-270`](https://github.com/ahb-sjsu/geometric-medicine/blob/6c8c4c4/manuscript/part_iii/ch09_clinical_cases.md#L266-L270). Online, [Geometric Medicine](https://erisml.org/geometric-medicine/ch09_clinical_cases.html).

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

clinical-geodesic, clinical-heuristic-admissibility, heuristic-field, consent-gauge-invariance

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
