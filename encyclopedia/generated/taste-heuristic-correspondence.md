# Taste-heuristic correspondence

**id.** taste-heuristic-correspondence
**kind.** concept
**volume.** Geometric Aesthetics, Volume 13 of the Geometric Series

## definition

Proposition 11.1. The aesthetic tangent vector at a point, the sense of where a program should go next, is the negative metric-raised gradient of the heuristic $h$ of an A* search toward a goal region, $T^\mu = -g^{\mu\nu} \partial_\nu h$. Trained taste is read as a compiled heuristic.

**Example.** With the identity metric and heuristic h = x squared plus y squared, the gradient at the point (1, 2) is (2, 4), so the taste vector is (-2, -4) and points toward the goal at the origin.

**Known as, or related to prior art.** A* search with an admissible heuristic, and its bounded-suboptimal form (Pohl 1970, Pearl 1984, as the volume cites).

## equation

none

## conditions

- It presupposes the aesthetic search problem of Definition 11.1, with a state, a goal region, a task-dependent cost functional and stratum constraints.
- The volume calls it a consistency condition between the geometric and the computational reading, not a stipulation. Appendix F does not list it among its formal claims.
- Real taste is taken to be epsilon-admissible and not strictly admissible. Heuristics whose output depends on irrelevant features of the description are classed as gauge-variant, a symmetry failure.
- Engagement maximization is a greedy local search with no goal region and no accumulated cost. The volume predicts trapping in a local minimum and identifies that with the filter bubble.

Conditions are curated in `volumes/geometric-aesthetics.toml` rather than read from a record.

## ledger

none. *standing.* Posited, carried over from the search chapter of the Ethics volume. No experiment in the volume tests it.

## first stated

Section 11.3, [`geometric-aesthetics/book/src/chapter-11-aesthetic-reasoning-as-optimal-search.md:49-55`](https://github.com/ahb-sjsu/geometric-aesthetics/blob/7a5e20e/book/src/chapter-11-aesthetic-reasoning-as-optimal-search.md#L49-L55). The search problem is defined at [`geometric-aesthetics/book/src/chapter-11-aesthetic-reasoning-as-optimal-search.md:19-34`](https://github.com/ahb-sjsu/geometric-aesthetics/blob/7a5e20e/book/src/chapter-11-aesthetic-reasoning-as-optimal-search.md#L19-L34). Online, [Geometric Aesthetics](https://erisml.org/geometric-aesthetics/chapter-11-aesthetic-reasoning-as-optimal-search.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Aesthetics*, Volume 13 of the Geometric Series.

## related

aesthetic-manifold, aesthetic-regime, aesthetic-invariance-claim, heuristic-admissibility, heuristic-field

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
