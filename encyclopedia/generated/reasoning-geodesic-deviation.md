# Geodesic deviation of a reasoning trajectory

**id.** reasoning-geodesic-deviation
**kind.** concept
**volume.** Geometric Reasoning, Volume 3 of the Geometric Series

## definition

The cost of a reasoning trajectory minus the cost of the geodesic that joins the same endpoints. The optimal trajectory is the path from the problem state to the goal region that minimizes the cost functional. The deviation is never negative and is zero only for a geodesic.

**Example.** In the volume's illustrative triage example the geodesic costs about 2.1 nats and the corrupted trajectory about 4.6 nats, so the deviation is 4.6 - 2.1 = 2.5 nats.

**Known as, or related to prior art.** Path length excess over the shortest path. It is not the geodesic deviation equation of differential geometry, which describes how nearby geodesics separate.

## equation

none

## conditions

- Tagged a modeling axiom. It needs a cost metric on the reasoning manifold, which the volume posits and does not measure.
- It measures the efficiency of the path and not whether the answer is right. A lucky shortcut can be accurate and still have a large deviation.
- The volume computes it only in illustrations. Its one empirical pointer is framework-switching efficiency, which it calls a proxy.

Conditions are curated in `volumes/geometric-reasoning.toml` rather than read from a record.

## ledger

none. *standing.* Posited framework. The README's epistemic-status block of 2026-07-14 calls the volume speculative theory awaiting instruments, to be read as theory at licensed strength and not as validated measurement. Its chapters tag each claim as established mathematics, empirical, modeling axiom, conditional theorem or speculation, and the empirical tags rest on one benchmark of five language models.

## first stated

Definitions 4.1 and 4.2, [`geometric-reasoning/chapters/ch04_geodesics_and_optimal_reasoning.md:92-98`](https://github.com/ahb-sjsu/geometric-reasoning/blob/881f075/chapters/ch04_geodesics_and_optimal_reasoning.md#L92-L98). Online, [Geometric Reasoning](https://erisml.org/geometric-reasoning/ch04_geodesics_and_optimal_reasoning.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Reasoning*, Volume 3 of the Geometric Series.

## related

reasoning-manifold, geodesic-distance, heuristic-field, nat

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
