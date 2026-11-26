# Educational Bond Index

**id.** educational-bond-index
**kind.** instrument
**volume.** Geometric Education, Volume 9 of the Geometric Series

## definition

For an institutional policy P and a student population S, the expected learning deviation of the path the policy allows, measured against each student's geodesic. The learning deviation of a path is the integral over time of its manifold distance from the geodesic. An index of zero means the policy imposes no deviation.

**Example.** For two students whose mean distances from their geodesics are 0.4 and 0.8, the index computed as in Appendix B.4 is the average, 0.6. In the volume's narrative the shares of the index are 45, 30, 15 and 10 percent, which sum to 100.

## equation

none

## conditions

- It is a property of the policy and not of the students. The volume says no real institution reaches zero.
- The computation needs an estimated learner metric, a computed geodesic and observed trajectories. The volume calls the metric estimate the most uncertain step.
- It is decomposed into access, heuristic, metric and residual parts. The volume gives no procedure for separating them.
- Section 18.5 states that no institution has performed the prospective test. The study in Section 13.5 is carried out by the volume's composite student and is narrative, not a record.

Conditions are curated in `volumes/geometric-education.toml` rather than read from a record.

## ledger

none. *standing.* A proposed instrument that has not been computed on data. The value 2.1 and the shares of 45, 30, 15 and 10 percent in Section 13.5 belong to the narrative of the composite student Alex.

## first stated

Definition 13.1, [`geometric-education/manuscript/part_iv/ch13_educational_bond_index.md:17-23`](https://github.com/ahb-sjsu/geometric-education/blob/89bcf86/manuscript/part_iv/ch13_educational_bond_index.md#L17-L23), with the computation in Section 13.3, [`geometric-education/manuscript/part_iv/ch13_educational_bond_index.md:91-97`](https://github.com/ahb-sjsu/geometric-education/blob/89bcf86/manuscript/part_iv/ch13_educational_bond_index.md#L91-L97). The online edition holds it in the notation table, [`geometric-education/manuscript/appendices/appendix_d_notation.md:50-53`](https://github.com/ahb-sjsu/geometric-education/blob/89bcf86/manuscript/appendices/appendix_d_notation.md#L50-L53), and as code in Appendix B.4, [`geometric-education/manuscript/appendices/appendix_b_code.md:89-121`](https://github.com/ahb-sjsu/geometric-education/blob/89bcf86/manuscript/appendices/appendix_b_code.md#L89-L121). Online, [Geometric Education](https://erisml.org/geometric-education/appendix_d_notation.html).

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

bond-index, legal-bond-index, learner-geodesic, inherited-heuristic, reasoning-geodesic-deviation, mahalanobis-distance

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
