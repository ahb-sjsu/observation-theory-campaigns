# Clinical heuristic admissibility

**id.** clinical-heuristic-admissibility
**kind.** result
**volume.** Geometric Medicine, Volume 8 of the Geometric Series

## definition

A clinical moral heuristic estimates the remaining cost from a state as the sum over boundaries of the penalty $\beta_k$ times the probability that the remaining path crosses boundary $k$. If each penalty is at most the true cost of crossing, the heuristic never overestimates the remaining cost, and A* search finds the clinical geodesic.

**Example.** Suppose one boundary has a trained penalty of 10, a true crossing cost of 15, and a probability of 0.5 of being crossed on the remaining path. The heuristic gives 5, the true expected boundary cost is 7.5, and the heuristic is admissible. With a trained penalty of 20 it gives 10 and overestimates. The numbers are arithmetic from the definition.

**Known as, or related to prior art.** Admissibility of an A* heuristic, with the optimality result of Hart, Nilsson and Raphael (1968).

## equation

none

## conditions

- The hypothesis is that training calibrates each penalty as a lower bound on the true cost of crossing. The volume assumes this and does not measure it.
- The proof uses the fact that the heuristic ignores the remaining distance cost, which is non-negative.
- When a penalty exceeds the true cost somewhere, the heuristic is inadmissible and the search may avoid the optimal path. The volume names moral injury, defensive medicine and personal trauma as mechanisms.

Conditions are curated in `volumes/geometric-medicine.toml` rather than read from a record.

## ledger

none. *standing.* A theorem with a short proof in Section 7.1, conditional on the calibration hypothesis. Section 18.9 gives the underlying pathfinding model the status formally developed, behaviorally plausible, not directly validated.

## first stated

Theorem 7.1, [`geometric-medicine/manuscript/part_ii/ch07_heuristic_spectrum.md:26-32`](https://github.com/ahb-sjsu/geometric-medicine/blob/c220ac9/manuscript/part_ii/ch07_heuristic_spectrum.md#L26-L32). Online, [Geometric Medicine](https://erisml.org/geometric-medicine/ch07_heuristic_spectrum.html).

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

heuristic-admissibility, heuristic-field, clinical-heuristic-hierarchy, clinical-moral-boundaries, clinical-geodesic, euclidean-heuristic-admissibility

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
