# Clinical decision complex

**id.** clinical-decision-complex
**kind.** concept
**volume.** Geometric Medicine, Volume 8 of the Geometric Series

## definition

A weighted simplicial complex on which clinical decisions are pathfinding problems. Each vertex is a clinical state with an attribute vector of nine clinical-moral scores, each edge is an available clinical action with a non-negative weight, and each higher simplex is a care bundle whose cost is evaluated as a unit.

**Example.** In the volume's intubation example the current state is a vertex with attribute vector (0.25, 0.5, 0.5, 0.2, 0.4, 0.3, 0.4, 0.6, 0.3), and intubation is an edge to the vertex (0.35, 0.5, 0.4, 0.1, 0.3, 0.2, 0.2, 0.7, 0.25). The outcomes score rises by 0.10 and the dignity score falls by 0.20.

**Known as, or related to prior art.** A weighted simplicial complex. The volume gives it as the clinical instance of the moral manifold of Geometric Ethics.

## equation

none

## conditions

- It is a simplicial complex and not a smooth manifold. The volume writes clinical manifold informally and means this complex.
- The nine dimensions are inherited from the moral manifold of Geometric Ethics, and each score lies between 0 and 1. Section 4.13 calls the nine-dimensional structure a model and an open empirical question.
- Section 4.13 says the complex is not a bedside calculator and does not produce unique solutions, because the covariance matrix, the boundary penalties and the goal region must be estimated from data.
- The covariance matrix has not been estimated. Section 18.9 gives the nine-dimensional claim the status theoretically grounded, empirically untested at scale.

Conditions are curated in `volumes/geometric-medicine.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, and says a clinical instrument is plausible but has not been built or gated. Its Section 18.9 says the covariance matrix has not been estimated and the clinical Bond Index has not been computed from clinical data, so every number in these entries is an illustration unless the entry says otherwise.

## first stated

Definition 4.1, [`geometric-medicine/manuscript/part_ii/ch04_clinical_manifold.md:28-36`](https://github.com/ahb-sjsu/geometric-medicine/blob/c220ac9/manuscript/part_ii/ch04_clinical_manifold.md#L28-L36). Online, [Geometric Medicine](https://erisml.org/geometric-medicine/ch04_clinical_manifold.html).

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

moral-decision-complex, nine-dimension-moral-chart, clinical-edge-weight, clinical-moral-boundaries, clinical-geodesic, moral-manifold

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
