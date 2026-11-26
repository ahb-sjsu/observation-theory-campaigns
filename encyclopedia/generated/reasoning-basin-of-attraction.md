# Basin of attraction of a reasoning minimum

**id.** reasoning-basin-of-attraction
**kind.** concept
**volume.** Geometric Reasoning, Volume 3 of the Geometric Series

## definition

The set of states from which gradient flow on the evaluation function converges to a given local minimum. Its depth is the lowest value of the function on the basin's boundary minus the value at the minimum. A dead zone is different. It is a flat region with a near-zero gradient and no minimum.

**Example.** For the function (x^2 - 1)^2 on the line, the minima are at -1 and 1, the basin of 1 is every x above 0, and its depth is the value 1 at x = 0 minus the value 0 at x = 1.

**Known as, or related to prior art.** Basins of attraction of gradient flow in dynamical systems and optimization.

## equation

none

## conditions

- It assumes a smooth evaluation function with isolated local minima on a Riemannian reasoning manifold. The basins then partition the manifold up to a set of measure zero.
- The definition is standard dynamics. That a model's premature convergence is a trajectory settling in such a basin is the volume's posited reading.
- No basin depth, radius or exit angle is measured in the volume.

Conditions are curated in `volumes/geometric-reasoning.toml` rather than read from a record.

## ledger

none. *standing.* Posited framework. The README's epistemic-status block of 2026-07-14 calls the volume speculative theory awaiting instruments, to be read as theory at licensed strength and not as validated measurement. Its chapters tag each claim as established mathematics, empirical, modeling axiom, conditional theorem or speculation, and the empirical tags rest on one benchmark of five language models.

## first stated

Definition 7.1, [`geometric-reasoning/chapters/ch07_local_minima_and_dead_zones.md:381-385`](https://github.com/ahb-sjsu/geometric-reasoning/blob/881f075/chapters/ch07_local_minima_and_dead_zones.md#L381-L385), with dead zones defined in Section 7.5, [`geometric-reasoning/chapters/ch07_local_minima_and_dead_zones.md:189-195`](https://github.com/ahb-sjsu/geometric-reasoning/blob/881f075/chapters/ch07_local_minima_and_dead_zones.md#L189-L195). Online, [Geometric Reasoning](https://erisml.org/geometric-reasoning/ch07_local_minima_and_dead_zones.html).

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

prompt-recovery-ceiling, false-termination-region, corrigibility-basin, heuristic-field, gradient

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
