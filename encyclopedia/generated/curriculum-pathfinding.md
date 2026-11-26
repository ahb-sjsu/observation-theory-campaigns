# curriculum as pathfinding

**id.** curriculum-pathfinding
**kind.** concept
**volume.** Geometric Education, Volume 9 of the Geometric Series

## definition

A curriculum is a planned path through the learner manifold, given by a sequence of courses as waypoints, from the incoming student's estimated state to the goal region set by the degree requirements. Designing it is A* search in which each course is an edge with a cost and prerequisites are hard constraints.

**Example.** Suppose a formal-first sequence of three courses costs a student 3, 4 and 5, and an applied-first sequence to the same goal region costs 2, 3 and 4. The totals are 12 and 9, so the minimum-cost curriculum for that student is the applied-first one, with the same number of courses.

**Known as, or related to prior art.** A* search for a minimum-cost path on a weighted graph.

## equation

none

## conditions

- Theorem 7.1 states that an admissible designer's heuristic gives the minimum-cost curriculum. The cost is total educational cost and not course count or time to degree.
- The planned path is not the student's actual trajectory. The gap between them, which the volume calls the learning deviation, depends on the true starting state, the student's own metric and the teaching.
- The starting state is estimated from placement tests and transcripts, which the volume says see mainly domain knowledge.
- Proposition 7.3, that more elective freedom raises transfer and creativity on average, is stated without data.

Conditions are curated in `volumes/geometric-education.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments. No education-domain instrument has been evaluated by the series' admission filter, and Chapter 18 states that the six predictions of Section 16.3 have not been tested and that no method for estimating the learner metric has been validated at scale.

## first stated

Definition 7.1, [`geometric-education/manuscript/part_ii/ch07_curriculum_pathfinding.md:18-22`](https://github.com/ahb-sjsu/geometric-education/blob/89bcf86/manuscript/part_ii/ch07_curriculum_pathfinding.md#L18-L22), with the search components and Theorem 7.1 at [`geometric-education/manuscript/part_ii/ch07_curriculum_pathfinding.md:26-42`](https://github.com/ahb-sjsu/geometric-education/blob/89bcf86/manuscript/part_ii/ch07_curriculum_pathfinding.md#L26-L42). Online, [Geometric Education](https://erisml.org/geometric-education/ch07_curriculum_pathfinding.html).

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

learner-geodesic, educational-boundary, educational-local-minimum, pedagogical-heuristic-admissibility, graph

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
