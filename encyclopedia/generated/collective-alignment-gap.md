# Collective alignment gap

**id.** collective-alignment-gap
**kind.** concept
**volume.** Geometric AI, Volume 11 of the Geometric Series

## definition

The distance on the value manifold between the Nash equilibrium of several AI systems, in which each maximizes its own scalar reward, and their Bond Geodesic Equilibrium, in which each follows the value-aligned geodesic given the others. Theorem 18.1 says the gap is positive when some value dimension lies in every system's reward kernel.

**Example.** In the volume's fictional three-system scenario the components are 0.21 on fairness and 0.13 on institutional legitimacy, and the printed total of 0.34 is their sum. After the shared value tensor the printed gap is 0.04.

**Known as, or related to prior art.** The comparison point is the Nash equilibrium of game theory.

## equation

none

## conditions

- Theorem 18.1 is a one-directional implication, from a non-empty intersection of the individual kernels to a positive gap. The paragraph after it adds that an interaction between dimensions can lie in the collective kernel even when that intersection is empty.
- Theorem 18.1 has no proof in the chapter, and Appendix D says it is stated without proof.
- The proposed remedy is a shared value tensor with system-specific emphasis weights. The claim that the Nash equilibrium then converges to the Bond Geodesic Equilibrium is asserted, and Chapter 20 lists the matching containment question as open.
- The gap values printed (0.21 on fairness, 0.13 on institutional legitimacy, and a fall from 0.34 to 0.04) belong to a fictional three-system scenario.

Conditions are curated in `volumes/geometric-ai.toml` rather than read from a record.

## ledger

none. *standing.* A posited quantity resting on a theorem stated without proof. No value of it has been measured.

## first stated

Definition 18.3, Section 18.4, [`geometric-ai/manuscript/part_v/ch18_multi_agent.md:57-69`](https://github.com/ahb-sjsu/geometric-ai/blob/2cc8c63/manuscript/part_v/ch18_multi_agent.md#L57-L69), with Theorem 18.1 (Multi-Agent Divergence) at [`geometric-ai/manuscript/part_v/ch18_multi_agent.md:43-51`](https://github.com/ahb-sjsu/geometric-ai/blob/2cc8c63/manuscript/part_v/ch18_multi_agent.md#L43-L51) and the two equilibria at [`geometric-ai/manuscript/part_v/ch18_multi_agent.md:25-41`](https://github.com/ahb-sjsu/geometric-ai/blob/2cc8c63/manuscript/part_v/ch18_multi_agent.md#L25-L41). Online, [Geometric AI](https://erisml.org/geometric-ai/ch18_multi_agent.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric AI*, Volume 11 of the Geometric Series.

## related

bond-geodesic-equilibrium, bge-nash-relationship, reward-kernel, tensor-valued-objective, geodesic-distance

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
