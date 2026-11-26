# Clinical friction

**id.** clinical-friction
**kind.** concept
**volume.** Geometric Medicine, Volume 8 of the Geometric Series

## definition

The total cost of a path on the clinical decision complex, the sum of the clinical edge weights of its steps. It splits into distance friction, the sum of the covariance-weighted terms, and boundary friction, the sum of the boundary penalties crossed.

**Example.** A path of three actions with weights 0.5, 10.25 and 1.25 has friction 12. If the only boundary crossed is one with penalty 10 on the second action, boundary friction is 10 and distance friction is 2. The numbers are arithmetic from the definition.

## equation

none

## conditions

- Friction is a property of a path and not of a case. A clinically difficult case can have a low-friction minimum path.
- The volume calls distance friction reducible by better treatments and boundary friction structural.
- It inherits the unestimated covariance matrix and the uncalibrated boundary penalties of the edge weight.

Conditions are curated in `volumes/geometric-medicine.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, and says a clinical instrument is plausible but has not been built or gated. Its Section 18.9 says the covariance matrix has not been estimated and the clinical Bond Index has not been computed from clinical data, so every number in these entries is an illustration unless the entry says otherwise.

## first stated

Definition 4.6, [`geometric-medicine/manuscript/part_ii/ch04_clinical_manifold.md:277-281`](https://github.com/ahb-sjsu/geometric-medicine/blob/c220ac9/manuscript/part_ii/ch04_clinical_manifold.md#L277-L281), with the decomposition at [`geometric-medicine/manuscript/part_ii/ch04_clinical_manifold.md:289-295`](https://github.com/ahb-sjsu/geometric-medicine/blob/c220ac9/manuscript/part_ii/ch04_clinical_manifold.md#L289-L295). Online, [Geometric Medicine](https://erisml.org/geometric-medicine/ch04_clinical_manifold.html).

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

clinical-edge-weight, clinical-geodesic, clinical-bond-index, moral-residue-of-contraction, legal-friction

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
