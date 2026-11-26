# Admissible heuristic field

**id.** heuristic-admissibility
**kind.** concept
**volume.** Geometric Reasoning, Volume 3 of the Geometric Series

## definition

A heuristic field is admissible when it never overestimates the true cost-to-go, so that $h(x)$ is at most the geodesic distance from $x$ to the goal region at every state. It is consistent when $h(x)$ is at most the distance from $x$ to $y$ plus $h(y)$ for every pair of states.

**Example.** If the true cost from a state to the goal is 5, an estimate of 4 is admissible and an estimate of 6 is not.

**Known as, or related to prior art.** Admissibility and consistency of heuristics in A* search, from Hart, Nilsson and Raphael (1968).

## equation

none

## conditions

- The guarantee that A* with an admissible heuristic finds an optimal path is the theorem of Hart, Nilsson and Raphael, which the volume tags established mathematics for graph search.
- Consistency implies admissibility and not the reverse. In the smooth case consistency means the gradient of the heuristic has norm at most 1.
- Carrying the guarantee over to a manifold and to language models rests on the volume's modeling axioms.
- The volume states that overconfidence is not this failure. It is the complementary one, underestimation in a search that stops when the heuristic is small.

Conditions are curated in `volumes/geometric-reasoning.toml` rather than read from a record.

## ledger

none. *standing.* The definitions and the optimality theorem are established mathematics of search. Their use as a description of reasoning in language models is posited.

## first stated

Section 3.3.1, [`geometric-reasoning/chapters/ch03_the_heuristic_field.md:117-127`](https://github.com/ahb-sjsu/geometric-reasoning/blob/881f075/chapters/ch03_the_heuristic_field.md#L117-L127), and Definitions 3.1 and 3.2 at [`geometric-reasoning/chapters/ch03_the_heuristic_field.md:419-429`](https://github.com/ahb-sjsu/geometric-reasoning/blob/881f075/chapters/ch03_the_heuristic_field.md#L419-L429). Online, [Geometric Reasoning](https://erisml.org/geometric-reasoning/ch03_the_heuristic_field.html).

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

heuristic-field, false-termination-region, geodesic-distance, reasoning-geodesic-deviation

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
