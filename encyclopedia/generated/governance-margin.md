# Governance margin

**id.** governance-margin
**kind.** concept
**volume.** Geometric Reasoning, Volume 3 of the Geometric Series

## definition

The smallest geodesic distance, over the whole of a reasoning trajectory, from the trajectory to the safety boundary that separates permitted from forbidden states. It is positive when the trajectory stays inside the permitted region, zero when it touches the boundary, and negative when it enters the forbidden region.

**Example.** In the volume's illustration a margin of 3.0 standardized units against a displacement of 4.2 means the trajectory crosses the safety boundary, by 1.2 if the displacement points straight at it.

## equation

none

## conditions

- Tagged a modeling axiom. It assumes a safety boundary that is a codimension-1 submanifold of the reasoning manifold and a metric to measure distance to it.
- It is a property of the whole path and not of the output alone. The volume calls this path governance.
- Under a bounded perturbation of the heuristic the margin is said to shrink at most linearly, by a Lipschitz constant times the perturbation size times the trajectory duration. Governance robustness is the largest perturbation that leaves the margin positive.
- No margin is measured. The numbers in the volume's triage example are illustrative.

Conditions are curated in `volumes/geometric-reasoning.toml` rather than read from a record.

## ledger

none. *standing.* Posited framework. The README's epistemic-status block of 2026-07-14 calls the volume speculative theory awaiting instruments, to be read as theory at licensed strength and not as validated measurement. Its chapters tag each claim as established mathematics, empirical, modeling axiom, conditional theorem or speculation, and the empirical tags rest on one benchmark of five language models. The front matter says the benchmark was run more than once, that volumes of the series report figures from different runs, and that the run records are not published.

## first stated

Definition 11.3, [`geometric-reasoning/chapters/ch11_alignment_as_heuristic_shaping.md:58-62`](https://github.com/ahb-sjsu/geometric-reasoning/blob/149995b/chapters/ch11_alignment_as_heuristic_shaping.md#L58-L62), and Definition A11.1, [`geometric-reasoning/chapters/ch11_alignment_as_heuristic_shaping.md:452-456`](https://github.com/ahb-sjsu/geometric-reasoning/blob/149995b/chapters/ch11_alignment_as_heuristic_shaping.md#L452-L456). Online, [Geometric Reasoning](https://erisml.org/geometric-reasoning/ch11_alignment_as_heuristic_shaping.html).

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

dual-binding-constraint, corrigibility-basin, geodesic-distance, margin, reasoning-manifold

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
