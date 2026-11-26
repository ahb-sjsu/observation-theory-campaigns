# learner geodesic

**id.** learner-geodesic
**kind.** concept
**volume.** Geometric Education, Volume 9 of the Geometric Series

## definition

The path from a student's current state to the goal region that minimizes total learning cost, the integral of $\sqrt{g_{ij} \dot{\gamma}^i \dot{\gamma}^j}$ along the path. The goal region is the set of states at or above a minimum acceptable attribute vector.

**Example.** Suppose two routes reach the goal region. One has segments of cost 2 and 3 and the other has segments of cost 1.5 and 4.5. The totals are 5 and 6, so of the two the first is the geodesic even though its first segment costs more.

## equation

none

## conditions

- The geodesic is in general not a straight line, and it differs between students because the cost of a transition depends on the student's position.
- The goal is a region and not a point. The university, the employer and the student may each define a different one.
- The manifold changes as the student traverses it, so the optimal path at one time may not be optimal later.
- It is a posited object. Computing it needs the learner metric, which the volume has not estimated from data.

Conditions are curated in `volumes/geometric-education.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments. No education-domain instrument has been evaluated by the series' admission filter, and Chapter 18 states that the six predictions of Section 16.3 have not been tested and that no method for estimating the learner metric has been validated at scale.

## first stated

Definition 4.2, [`geometric-education/manuscript/part_ii/ch04_learner_manifold.md:161-165`](https://github.com/ahb-sjsu/geometric-education/blob/7bf76da/manuscript/part_ii/ch04_learner_manifold.md#L161-L165), with the goal region in Definition 4.4, [`geometric-education/manuscript/part_ii/ch04_learner_manifold.md:221-223`](https://github.com/ahb-sjsu/geometric-education/blob/7bf76da/manuscript/part_ii/ch04_learner_manifold.md#L221-L223). Online, [Geometric Education](https://erisml.org/geometric-education/ch04_learner_manifold.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Education*, Volume 9 of the Geometric Series.

## related

geodesic-distance, learner-metric, learner-manifold, assessment-geodesic-divergence, curriculum-pathfinding, bond-geodesic

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
