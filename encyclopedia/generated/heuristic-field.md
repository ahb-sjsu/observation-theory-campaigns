# Heuristic field

**id.** heuristic-field
**kind.** concept
**volume.** Geometric Reasoning, Volume 3 of the Geometric Series

## definition

A smooth function $h$ from the reasoning manifold to the non-negative reals that estimates the cost of reaching the goal region from each state. It is zero on the goal region and positive elsewhere, and its negative gradient is the direction the search follows.

**Example.** On the half line of states x at or above 0 with the goal at 0 and unit cost per unit distance, the field h(x) = x gives h(3) = 3, and its negative gradient points toward 0.

**Known as, or related to prior art.** The heuristic function of A* search, restated as a scalar field. The volume compares it to a potential energy surface and a loss landscape.

## equation

none

## conditions

- Tagged a modeling axiom. That a reasoning system's guidance is one scalar field on a manifold is a structural choice of the volume.
- Smoothness is assumed so that the gradient exists. The integral curves of the negative gradient approximate geodesics only when the heuristic equals the true cost-to-go.
- For language models the field is implicit. Chapter 15 lists measuring it from activations as an open question.

Conditions are curated in `volumes/geometric-reasoning.toml` rather than read from a record.

## ledger

none. *standing.* Posited framework. The README's epistemic-status block of 2026-07-14 calls the volume speculative theory awaiting instruments, to be read as theory at licensed strength and not as validated measurement. Its chapters tag each claim as established mathematics, empirical, modeling axiom, conditional theorem or speculation, and the empirical tags rest on one benchmark of five language models.

## first stated

Section 3.1.2, [`geometric-reasoning/chapters/ch03_the_heuristic_field.md:35-45`](https://github.com/ahb-sjsu/geometric-reasoning/blob/b645f23/chapters/ch03_the_heuristic_field.md#L35-L45), with the formal definition at [`geometric-reasoning/chapters/ch03_the_heuristic_field.md:417-417`](https://github.com/ahb-sjsu/geometric-reasoning/blob/b645f23/chapters/ch03_the_heuristic_field.md#L417-L417). Online, [Geometric Reasoning](https://erisml.org/geometric-reasoning/ch03_the_heuristic_field.html).

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

reasoning-manifold, heuristic-admissibility, false-termination-region, corruption-tensor, gradient

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
