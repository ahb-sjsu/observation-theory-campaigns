# Tensor-valued objective

**id.** tensor-valued-objective
**kind.** concept
**volume.** Geometric AI, Volume 11 of the Geometric Series

## definition

A vector-valued reward with one component per value dimension, in place of a single scalar. When a decision needs a scalar, the contraction $\sum_\mu w_\mu r^\mu$ is a separate, explicit and auditable step. With d independent components the reward has trivial kernel.

**Example.** With weights (0.5, 0.5) the reward vectors (0.9, 0.1) and (0.5, 0.5) both contract to 0.5. The scalar is the same and the tensors differ, which is why the contraction is logged with the tensor.

## equation

none

## conditions

- Corollary 5.3 requires the d components to be linearly independent, and a left inverse exists when the reward is injective. A component that is missing or dependent restores a kernel.
- Chapter 14 says the contraction weights and method are parameters set by governance and not learned features. Chapter 16 derives the weights of its practical objective from the learned metric, notes the difference from Chapter 14, and compares the two in Section 16.6.
- Any contraction to a scalar is itself lossy. The architecture answers this by logging the tensor, the contraction and the residue for every output.
- The chapter points to the MoralTensor class of the ErisML library as a running implementation. The README says such artifacts are real and separately validated while the alignment thesis is not validated measurement.

Conditions are curated in `volumes/geometric-ai.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status block of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, whose alignment thesis is theory at licensed strength and not validated measurement. It adds that no alignment instrument has been evaluated under the xbse admission filter, and the front matter says that ARIA, the system whose numbers fill the chapter tables, is fictional.

## first stated

Definition 14.1, Section 14.3, [`geometric-ai/manuscript/part_iv/ch14_constitutional_geometry.md:70-80`](https://github.com/ahb-sjsu/geometric-ai/blob/a628e38/manuscript/part_iv/ch14_constitutional_geometry.md#L70-L80), with Corollary 5.3 (Tensor Sufficiency) at [`geometric-ai/manuscript/part_ii/ch05_reward_irrecoverability.md:154-158`](https://github.com/ahb-sjsu/geometric-ai/blob/a628e38/manuscript/part_ii/ch05_reward_irrecoverability.md#L154-L158). Online, [Geometric AI](https://erisml.org/geometric-ai/ch14_constitutional_geometry.html).

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

reward-irrecoverability-theorem, reward-kernel, structural-containment-architecture, constitutional-geometry, geometric-rlhf

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
