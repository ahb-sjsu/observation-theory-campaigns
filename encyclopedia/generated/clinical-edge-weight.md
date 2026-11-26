# Clinical edge weight

**id.** clinical-edge-weight
**kind.** concept
**volume.** Geometric Medicine, Volume 8 of the Geometric Series

## definition

The cost of one clinical action. It is the quadratic form $\Delta a^T \Sigma^{-1} \Delta a$ in the change of the patient's nine-component attribute vector, with $\Sigma$ the 9 by 9 clinical-moral covariance matrix, plus the sum of the penalties $\beta_k$ of the clinical-moral boundaries the action crosses.

**Example.** The volume's illustration for intubating a patient with advanced dementia has a change vector with squared Euclidean length 0.1025, an assumed covariance-weighted term of about 0.15, and a consent penalty of 10, so the weight is 0.15 + 10 = 10.15. Supportive care crosses no boundary and weighs about 0.05. Both totals are the volume's and are marked illustrative.

## equation

none

## conditions

- The volume calls the quadratic form the Mahalanobis distance. The formula has no square root.
- The covariance matrix has 45 independent entries and the theorems are said to hold for any positive-definite one. None of the entries has been estimated, and Section 4.5.2 says the framework runs on the qualitative structure until it is.
- With the identity as covariance matrix the first term reduces to the Euclidean form.
- The two worked weights of Section 4.4.3 are marked illustrative by the volume.

Conditions are curated in `volumes/geometric-medicine.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, and says a clinical instrument is plausible but has not been built or gated. Its Section 18.8 says the covariance matrix has not been estimated and the clinical Bond Index has not been computed from clinical data, so every number in these entries is an illustration unless the entry says otherwise.

## first stated

Definition 4.2, [`geometric-medicine/manuscript/part_ii/ch04_clinical_manifold.md:146-150`](https://github.com/ahb-sjsu/geometric-medicine/blob/ecde39b/manuscript/part_ii/ch04_clinical_manifold.md#L146-L150). Online, [Geometric Medicine](https://erisml.org/geometric-medicine/ch04_clinical_manifold.html).

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

mahalanobis-distance, moral-decision-edge-weight, clinical-moral-boundaries, clinical-friction, covariance-matrix

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
