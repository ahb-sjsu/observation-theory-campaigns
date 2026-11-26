# pedagogical heuristic and its admissibility

**id.** pedagogical-heuristic-admissibility
**kind.** concept
**volume.** Geometric Education, Volume 9 of the Geometric Series

## definition

The pedagogical heuristic $h_T(x)$ is the teacher's estimate of the geodesic distance from the student's state x to the nearest point of the goal region. It is admissible when $h_T(x)$ is at most that distance for every x, and epsilon-admissible when it exceeds the distance by at most a small epsilon.

**Example.** If the true distance to the goal is 10, an estimate of 8 is admissible. An estimate of 10.5 is not admissible and is epsilon-admissible for epsilon equal to 1. An estimate of 13 is neither.

**Known as, or related to prior art.** Admissible heuristics for A* search, after Hart, Nilsson and Raphael (1968). The volume ties the calibration of the heuristic to Shulman's pedagogical content knowledge (1986).

## equation

none

## conditions

- Theorem 6.1 states that A* search with an admissible heuristic finds the learner geodesic. The volume gives it as a direct instantiation of the A* optimality theorem of Geometric Reasoning.
- With an epsilon-admissible heuristic the teaching path is within epsilon of optimal.
- The volume's prose reads the admissible case as a teacher who never judges a student ready too early, and the inadmissible case, written $h_T(x) > d(x, G) + \epsilon$, as a teacher who overestimates readiness. The inequality and the prose do not agree, and the volume's corrections record of 2026-11-26 lists the choice between them as unresolved.
- The mapping of master, competent and miscalibrated teachers onto the three grades is posited. No teacher's heuristic has been measured.

Conditions are curated in `volumes/geometric-education.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments. No education-domain instrument has been evaluated by the series' admission filter, and Chapter 18 states that the six predictions of Section 16.3 have not been tested and that no method for estimating the learner metric has been validated at scale.

## first stated

Definitions 6.1 and 6.2 with Theorem 6.1, [`geometric-education/manuscript/part_ii/ch06_teaching_geodesic.md:24-28`](https://github.com/ahb-sjsu/geometric-education/blob/085dda1/manuscript/part_ii/ch06_teaching_geodesic.md#L24-L28) and [`geometric-education/manuscript/part_ii/ch06_teaching_geodesic.md:50-56`](https://github.com/ahb-sjsu/geometric-education/blob/085dda1/manuscript/part_ii/ch06_teaching_geodesic.md#L50-L56), with the weaker grades in Sections 6.2.2 and 6.2.3, [`geometric-education/manuscript/part_ii/ch06_teaching_geodesic.md:62-70`](https://github.com/ahb-sjsu/geometric-education/blob/085dda1/manuscript/part_ii/ch06_teaching_geodesic.md#L62-L70). Online, [Geometric Education](https://erisml.org/geometric-education/ch06_teaching_geodesic.html).

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

heuristic-admissibility, educational-heuristic-field, euclidean-heuristic-admissibility, gauge-variant-pedagogical-heuristic, learner-geodesic

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
