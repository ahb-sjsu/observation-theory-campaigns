# geodesic divergence of the assessment-optimal path

**id.** assessment-geodesic-divergence
**kind.** result
**volume.** Geometric Education, Volume 9 of the Geometric Series

## definition

The path that maximizes a scalar assessment G at each step differs from the learner geodesic to the goal. The divergence, the integral over the path parameter of the manifold distance between the two paths, is strictly positive whenever G is not proportional to the distance-to-goal function.

**Example.** In the volume's illustration Ethan ends at (0.90, 0.55, 0.40, 0.50, 0.40, 0.30) with a 3.7 average and Alex at (0.70, 0.90, 0.80, 0.75, 0.85, 0.70) with 3.2. The coordinate sums are 3.05 and 4.70, so the higher score goes with the lower sum, as Corollary 5.3.2 says.

## equation

none

## conditions

- The two paths coincide only when the gradient of G is parallel to the gradient of the distance to the goal, that is when the assessment weights match the true educational costs up to a scalar multiple.
- The theorem also states that the divergence grows without bound as the dimension increases. The text supports this with the remark that a scalar captures at most one direction in d.
- Corollary 5.3.2 concludes that a student who maximizes G ends with a higher score and a lower sum across all dimensions than a student on the geodesic.
- The four-year trajectories of Alex and Ethan that illustrate it are posited, with composite students.

Conditions are curated in `volumes/geometric-education.toml` rather than read from a record.

## ledger

none. *standing.* Stated as a theorem. The text says the proof uses the calculus of variations and gives the argument in prose, with no displayed derivation. No trajectory data support it.

## first stated

Theorem 5.3, [`geometric-education/manuscript/part_ii/ch05_assessment_contraction.md:72-80`](https://github.com/ahb-sjsu/geometric-education/blob/7bf76da/manuscript/part_ii/ch05_assessment_contraction.md#L72-L80), with Corollaries 5.3.1 and 5.3.2 at [`geometric-education/manuscript/part_ii/ch05_assessment_contraction.md:108-118`](https://github.com/ahb-sjsu/geometric-education/blob/7bf76da/manuscript/part_ii/ch05_assessment_contraction.md#L108-L118). Online, [Geometric Education](https://erisml.org/geometric-education/ch05_assessment_contraction.html).

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

gpa-irrecoverability-theorem, learner-geodesic, reasoning-geodesic-deviation, gradient, educational-ai-no-escape

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
