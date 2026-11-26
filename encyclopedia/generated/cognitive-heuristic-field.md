# heuristic field

**id.** cognitive-heuristic-field
**kind.** concept
**volume.** Geometric Cognition, Volume 6 of the Geometric Series

## definition

A smooth real-valued function $h$ on the cognitive manifold that assigns each state an estimate of the cost of reaching the goal state, approximating the geodesic distance to it. System 1 processing follows its negative gradient.

**Example.** On a line with the goal at 0 and $h(x) = |x|$, the state 3 has estimated cost 3 and the negative gradient points toward 0. If $h$ also had a dip at 5, a gradient-following search started at 6 would stop at 5 and never reach the goal.

**Known as, or related to prior art.** The heuristic function of A* search, which the volume's notation table gives as $f(x) = g(x) + h(x)$.

## equation

none

## conditions

- The field is an estimate and can be wrong. A local minimum of $h$ far from the true goal traps gradient-following search, which the volume calls premature convergence.
- The volume reads framing, anchoring and sycophancy as corruption of the field. Those readings are interpretations on benchmark axes, and the ledger holds each interpretation at posited.
- Chapter 17 lists measuring the field from neural activations as an open question.

Conditions are curated in `volumes/geometric-cognition.toml` rather than read from a record.

## ledger

none. *standing.* The README's status block of 2026-09-13 calls the book a domain exposition at posited, graded by a claim ledger converted from the manuscript with debt ratio 1.0, so every row is retrospective and no gate has been sealed in the repository. The ledger grades the benchmark statistics exploratory because their primary run records are not in the repository, and it holds every interpretation at posited because the admission filter xbse ruled the cognitive instrument inadmissible on 2026-07-14.

## first stated

Definition 3.7, [`geometric-cognition/chapters/ch03_cognitive_manifold.md:164-168`](https://github.com/ahb-sjsu/geometric-cognition/blob/93e39e2/chapters/ch03_cognitive_manifold.md#L164-L168). Online, [Geometric Cognition](https://erisml.org/geometric-cognition/ch03_cognitive_manifold.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Cognition*, Volume 6 of the Geometric Series.

## related

cognitive-manifold, curvature-triggered-transition, geodesic-distance, gradient, geometric-defect-taxonomy

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
