# learner metric

**id.** learner-metric
**kind.** concept
**volume.** Geometric Education, Volume 9 of the Geometric Series

## definition

A symmetric positive-definite tensor field $g_{ij}(x)$ on the learner manifold. The squared length of a small step is $ds^2 = \sum_{i,j} g_{ij}(x) dx^i dx^j$, read as the educational effort of that transition. In practice the volume takes it as the inverse of the 6 by 6 learner covariance matrix, which gives a Mahalanobis distance.

**Example.** A symmetric 6 by 6 covariance matrix has 6 diagonal and 15 off-diagonal entries, 21 in all, as the volume counts. With the identity as covariance, two states that differ by 0.3 on one dimension and 0.4 on another are at distance 0.5.

**Known as, or related to prior art.** The Mahalanobis distance, with the inverse covariance matrix as a constant metric.

## equation

none

## conditions

- The metric depends on position. The same increment of knowledge costs less for a student with strong knowledge and metacognition than for a student weak in both, and the volume calls this dependence curvature.
- Chapter 10 adds that the metric also differs between two students at the same position. A uniform metric is an approximation the volume accepts only for a homogeneous population, content on one dimension, and a short course.
- No covariance matrix is printed. The volume describes three cross terms in words and says the matrix is to be estimated from data.
- Section 10.4 states that no current adaptive learning system estimates the 6 by 6 metric or computes a geodesic from it.

Conditions are curated in `volumes/geometric-education.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments. No education-domain instrument has been evaluated by the series' admission filter, and Chapter 18 states that the six predictions of Section 16.3 have not been tested and that no method for estimating the learner metric has been validated at scale.

## first stated

Definition 4.1 and Section 4.4.1, [`geometric-education/manuscript/part_ii/ch04_learner_manifold.md:129-141`](https://github.com/ahb-sjsu/geometric-education/blob/7bf76da/manuscript/part_ii/ch04_learner_manifold.md#L129-L141), with the dependence on the individual student in Section 10.1, [`geometric-education/manuscript/part_iii/ch10_personalized_learning.md:18-20`](https://github.com/ahb-sjsu/geometric-education/blob/7bf76da/manuscript/part_iii/ch10_personalized_learning.md#L18-L20). Online, [Geometric Education](https://erisml.org/geometric-education/ch04_learner_manifold.html).

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

mahalanobis-distance, covariance-matrix, positive-definite, curvature, learner-manifold, legal-mahalanobis-distance

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
