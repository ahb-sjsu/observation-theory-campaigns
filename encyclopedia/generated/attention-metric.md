# attention metric

**id.** attention-metric
**kind.** concept
**volume.** Geometric Cognition, Volume 6 of the Geometric Series

## definition

A positive-definite symmetric bilinear form $g$ on each tangent space of the cognitive manifold whose components are set by attention allocation. A dimension with a larger attention weight has higher resolution, so states that differ along it are farther apart and easier to tell apart.

**Example.** With attention weight 4 on color and 1 on shape and no cross terms, a unit step along color has squared length 4 and a unit step along shape has squared length 1. On the A4 divided attention test the volume prints 0.571 for Claude and 1.000 for Gemini 3 Flash, a gap of 0.429.

**Known as, or related to prior art.** A Riemannian metric tensor. Section 4.11 of the volume connects it to Fisher information.

## equation

none

## conditions

- The ledger holds the claim that attention is the metric at posited (GC-3).
- Under divided attention a fixed budget W is spread over k targets, so each target receives W/k and less resolution than under selective attention.
- The volume reads benchmark scores as constraints on the metric through a model. Its eccentricity estimates of about 4.2 for Claude and 1.1 for Gemini 3 Flash assume a harmonic mean of per-dimension performance and a sigmoid in the attention weight.

Conditions are curated in `volumes/geometric-cognition.toml` rather than read from a record.

## ledger

none. *standing.* The README's status block of 2026-09-13 calls the book a domain exposition at posited, graded by a claim ledger converted from the manuscript with debt ratio 1.0, so every row is retrospective and no gate has been sealed in the repository. The ledger grades the benchmark statistics exploratory because their primary run records are not in the repository, and it holds every interpretation at posited because the admission filter xbse ruled the cognitive instrument inadmissible on 2026-07-14.

## first stated

Definition 4.1, [`geometric-cognition/chapters/ch04_attention_metric.md:51-55`](https://github.com/ahb-sjsu/geometric-cognition/blob/585fc4e/chapters/ch04_attention_metric.md#L51-L55), with the weights written out at [`geometric-cognition/chapters/ch04_attention_metric.md:65-67`](https://github.com/ahb-sjsu/geometric-cognition/blob/585fc4e/chapters/ch04_attention_metric.md#L65-L67). Online, [Geometric Cognition](https://erisml.org/geometric-cognition/ch04_attention_metric.html).

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

metric, positive-definite, cognitive-manifold, working-memory-tangent-space, mahalanobis-distance

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
