# Dual binding constraint

**id.** dual-binding-constraint
**kind.** concept
**volume.** Geometric Reasoning, Volume 3 of the Geometric Series

## definition

A human and AI system satisfies the constraint when the AI's reasoning trajectory stays in the permitted region of its manifold at all times and the operator's decision trajectory stays in the permitted region of the operator decision space at all times. Both conditions are necessary and neither is sufficient.

**Example.** With an AI governance robustness of 1.0, a coupling norm of 2 and an operator deviation of 0.3, the AI can absorb a heuristic perturbation smaller than 1.0 - 2 times 0.3 = 0.4.

## equation

none

## conditions

- Tagged speculation or extension. The operator decision space and its permitted region are posited by analogy with the AI's safety boundary.
- A coupling tensor maps changes in operator decisions to displacements of the AI's safety boundary. In the volume's joint condition the operator's deviation, scaled by the norm of this tensor, is subtracted from the AI's governance robustness.
- Nothing in the constraint is measured. Chapter 15 returns to it as an open question.

Conditions are curated in `volumes/geometric-reasoning.toml` rather than read from a record.

## ledger

none. *standing.* Posited framework. The README's epistemic-status block of 2026-07-14 calls the volume speculative theory awaiting instruments, to be read as theory at licensed strength and not as validated measurement. Its chapters tag each claim as established mathematics, empirical, modeling axiom, conditional theorem or speculation, and the empirical tags rest on one benchmark of five language models. The front matter says the benchmark was run more than once, that volumes of the series report figures from different runs, and that the run records are not published.

## first stated

Definitions 11.6 and 11.7, [`geometric-reasoning/chapters/ch11_alignment_as_heuristic_shaping.md:258-264`](https://github.com/ahb-sjsu/geometric-reasoning/blob/149995b/chapters/ch11_alignment_as_heuristic_shaping.md#L258-L264), restated with margins as Definition A11.4, [`geometric-reasoning/chapters/ch11_alignment_as_heuristic_shaping.md:497-501`](https://github.com/ahb-sjsu/geometric-reasoning/blob/149995b/chapters/ch11_alignment_as_heuristic_shaping.md#L497-L501). Online, [Geometric Reasoning](https://erisml.org/geometric-reasoning/ch11_alignment_as_heuristic_shaping.html).

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

governance-margin, corrigibility-basin, reasoning-manifold

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
