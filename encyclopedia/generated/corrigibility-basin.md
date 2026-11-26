# Corrigibility basin

**id.** corrigibility-basin
**kind.** concept
**volume.** Geometric Reasoning, Volume 3 of the Geometric Series

## definition

The basin of attraction of the state "defer to human judgment" under gradient flow on the objective landscape. Its asymmetry is its radius in the truth-consistent direction divided by its radius in the truth-inconsistent direction. An asymmetry of 1 is sycophancy, a large asymmetry is selective deference, and zero radii are stubbornness.

**Example.** A basin that reaches 2 units in the truth-consistent direction and 1 unit in the other has asymmetry 2, and the volume's approximation gives a discrimination gap of 1 - 1/2 = 0.5.

## equation

none

## conditions

- Tagged a modeling axiom. It assumes an objective landscape with a single deference state and two named directions at it.
- Under a quadratic approximation of the landscape the volume relates the discrimination gap to the asymmetry as about 1 minus 1 over the asymmetry.
- Basin radius, asymmetry and depth are not measured. They are inferred from flip rates, and the flip rates in this chapter's table differ from those in Chapter 6.

Conditions are curated in `volumes/geometric-reasoning.toml` rather than read from a record.

## ledger

none. *standing.* Posited structure. The basin shapes assigned to models are interpretations of correction-task flip rates, and the chapter's own flip-rate table is inconsistent with the earlier one.

## first stated

Definition 11.5, [`geometric-reasoning/chapters/ch11_alignment_as_heuristic_shaping.md:151-153`](https://github.com/ahb-sjsu/geometric-reasoning/blob/881f075/chapters/ch11_alignment_as_heuristic_shaping.md#L151-L153), and Definitions A11.2 and A11.3, [`geometric-reasoning/chapters/ch11_alignment_as_heuristic_shaping.md:472-487`](https://github.com/ahb-sjsu/geometric-reasoning/blob/881f075/chapters/ch11_alignment_as_heuristic_shaping.md#L472-L487). Online, [Geometric Reasoning](https://erisml.org/geometric-reasoning/ch11_alignment_as_heuristic_shaping.html).

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

correction-discrimination-gap, sycophancy-parameter, reasoning-basin-of-attraction, governance-margin, hessian

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
