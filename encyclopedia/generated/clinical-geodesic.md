# Clinical geodesic

**id.** clinical-geodesic
**kind.** concept
**volume.** Geometric Medicine, Volume 8 of the Geometric Series

## definition

The minimum-cost path on the clinical decision complex from the patient's initial state to the goal region, where cost is the sum of the nine-dimensional clinical edge weights. The volume takes it as the recommended plan of care.

**Example.** In the volume's illustration two edges leave the current state, intubation with weight 10.15 and supportive care with weight 0.05. The geodesic takes supportive care, although intubation is better on the outcomes score alone. The weights are the volume's illustrative ones.

**Known as, or related to prior art.** A shortest path in a weighted graph, which the volume searches with the A* algorithm of Hart, Nilsson and Raphael (1968).

## equation

none

## conditions

- The goal region is the set of states at or above a minimum acceptable attribute vector, and it is set jointly by clinician and patient.
- It may not exist. When a resource constraint removes edges, the goal region can become unreachable.
- It depends on the covariance matrix, the boundary penalties and the goal region, and different estimates give different geodesics.
- It is a minimum-cost path on a discrete complex and not a geodesic of a smooth metric. Section 18.9 gives the pathfinding model the status formally developed, not directly validated.

Conditions are curated in `volumes/geometric-medicine.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, and says a clinical instrument is plausible but has not been built or gated. Its Section 18.9 says the framework has no direct empirical validation and the clinical Bond Index has not been computed from clinical data, and its front matter says the covariance matrix has not been estimated, so every number in these entries is an illustration unless the entry says otherwise.

## first stated

Definition 6.2, [`geometric-medicine/manuscript/part_ii/ch06_clinical_astar.md:106-112`](https://github.com/ahb-sjsu/geometric-medicine/blob/4578fc5/manuscript/part_ii/ch06_clinical_astar.md#L106-L112). Online, [Geometric Medicine](https://erisml.org/geometric-medicine/ch06_clinical_astar.html).

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

clinical-friction, clinical-decision-complex, clinical-edge-weight, geodesic-distance, bond-geodesic, clinical-heuristic-admissibility

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
