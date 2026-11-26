# RLHF Irrecoverability

**id.** rlhf-irrecoverability
**kind.** result
**volume.** Geometric AI, Volume 11 of the Geometric Series

## definition

The pipeline of reinforcement learning from human feedback contracts a rater's d-dimensional evaluation to a binary preference, the preferences to a scalar reward model, and the reward to a policy. The composition is irrecoverable, so no amount of training data restores what the first stage discarded.

**Example.** A rater finds response A better on welfare and response B better on honesty and on dignity, and picks A. The record is one preference. With d = 9 the first stage keeps 1 dimension and discards the other 8.

**Known as, or related to prior art.** A statement about reinforcement learning from human feedback (RLHF).

## equation

none

## conditions

- It is a corollary of Theorem 5.1 and holds under that theorem's conditions.
- The volume says this does not make the method useless. It yields alignment along the dimensions that raters and reward model jointly capture and leaves the kernel unconstrained.
- The partial alignment cannot be completed without information the pipeline does not collect. Chapter 16 proposes collecting it as per-dimension feedback.

Conditions are curated in `volumes/geometric-ai.toml` rather than read from a record.

## ledger

none. *standing.* A corollary stated without a separate proof. It rests on the Reward Irrecoverability Theorem and on the volume's three-stage description of the pipeline.

## first stated

Corollary 5.2, Section 5.2.2, [`geometric-ai/manuscript/part_ii/ch05_reward_irrecoverability.md:72-88`](https://github.com/ahb-sjsu/geometric-ai/blob/2cc8c63/manuscript/part_ii/ch05_reward_irrecoverability.md#L72-L88). Online, [Geometric AI](https://erisml.org/geometric-ai/ch05_reward_irrecoverability.html).

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

reward-irrecoverability-theorem, reward-kernel, geometric-rlhf, tensor-valued-objective

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
