# Reward Irrecoverability Theorem

**id.** reward-irrecoverability-theorem
**kind.** result
**volume.** Geometric AI, Volume 11 of the Geometric Series

## definition

Any continuously differentiable scalar reward R on a value manifold of dimension d at least 2 is not injective and has no left inverse. Its kernel has dimension $d-1$ at almost every point. Where the manifold is non-compact along the kernel directions, policies within any epsilon of maximum reward lie at unbounded distance from the value-aligned policy.

**Example.** On two dimensions let the reward be the sum of the coordinates. The states (0.9, 0.1) and (0.1, 0.9) both score 1.0, so the reward cannot be inverted. With d = 9 the kernel has dimension 9 less 1, which is 8.

**Known as, or related to prior art.** The volume sets it beside Goodhart's law and calls Goodhart contingent and the theorem necessary.

## equation

none

## conditions

- The reward must be continuously differentiable and the manifold must have dimension at least 2. Parts (i), (ii) and (iv) need nothing more.
- Part (iii), unbounded divergence, carries the hypothesis that the manifold is non-compact along the kernel directions of the reward, and Appendix D.1 adds completeness. The proof sketch says that on the normalized chart of Chapter 4, where every attribute value lies in [0, 1], the divergence is bounded by the diameter of the manifold.
- The theorem bounds what a scalar can carry. The volume says the exploitation might not occur in practice if capability is limited or other constraints bind.
- The seven predictions on the kernel and near-kernel dimensions of ARIA belong to a scenario the volume labels illustrative. It counts five full and two partial confirmations.

Conditions are curated in `volumes/geometric-ai.toml` rather than read from a record.

## ledger

none. *standing.* Stated as a theorem with a written proof in Appendix D.1, as the reinforcement-learning instance of the Scalar Irrecoverability Theorem of Geometric Reasoning. The README classes the volume as posited, so the theorem is about the posited manifold and is not a measurement of any deployed system.

## first stated

Theorem 5.1, Section 5.1, [`geometric-ai/manuscript/part_ii/ch05_reward_irrecoverability.md:36-46`](https://github.com/ahb-sjsu/geometric-ai/blob/a628e38/manuscript/part_ii/ch05_reward_irrecoverability.md#L36-L46), with the proof in Appendix D.1, [`geometric-ai/manuscript/appendices/appendix_d_proofs.md:7-30`](https://github.com/ahb-sjsu/geometric-ai/blob/a628e38/manuscript/appendices/appendix_d_proofs.md#L7-L30). Online, [Geometric AI](https://erisml.org/geometric-ai/ch05_reward_irrecoverability.html).

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

scalar-irrecoverability-theorem, moral-scalar-irrecoverability, benchmark-scalar-irrecoverability, reward-kernel, rlhf-irrecoverability, tensor-valued-objective

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
