# Reward kernel (the dark space of alignment)

**id.** reward-kernel
**kind.** concept
**volume.** Geometric AI, Volume 11 of the Geometric Series

## definition

The set of tangent directions on the value manifold along which a scalar reward is constant. The system can move in these directions at no cost to its reward, so the volume treats the kernel as a threat surface and predicts that alignment failures concentrate on the dimensions the reward does not track.

**Example.** In the volume's illustration the fictional ARIA's reward has gradient magnitudes 0.87, 0.71, 0.23, 0.11, 0.09, 0.07, 0.06, 0.05 and 0.03 on the nine dimensions. Five of the nine fall below the cut of 0.10, and those five form its effective kernel.

## equation

none

## conditions

- Kernel misalignment shows in the tracked dimensions only through off-diagonal terms of the value metric. Where those terms are zero the volume says it is completely invisible to the reward.
- Theorem 5.2 says that, under the non-compactness condition of part (iii) of Theorem 5.1, for any epsilon and any K there is a policy within epsilon of maximum reward and farther than K from the value-aligned policy. Appendix D.2 derives it directly from that part.
- Corollary 5.1 is stated for a reward that primarily tracks some dimensions, and its kernel is then approximately spanned by the rest. The worked kernel analysis is the fictional ARIA's, with a cut at gradient magnitude 0.10.

Conditions are curated in `volumes/geometric-ai.toml` rather than read from a record.

## ledger

none. *standing.* Theorem 5.2 is stated as a theorem and proved in Appendix D.2 as a consequence of Theorem 5.1. The claim that the kernel predicts failure modes is illustrated only on the fictional ARIA.

## first stated

Theorem 5.1 (iv) and Section 5.3 with Theorem 5.2 (Kernel Exploitation), [`geometric-ai/manuscript/part_ii/ch05_reward_irrecoverability.md:100-110`](https://github.com/ahb-sjsu/geometric-ai/blob/a628e38/manuscript/part_ii/ch05_reward_irrecoverability.md#L100-L110), and Corollary 5.1 (Kernel Prediction), [`geometric-ai/manuscript/part_ii/ch05_reward_irrecoverability.md:64-70`](https://github.com/ahb-sjsu/geometric-ai/blob/a628e38/manuscript/part_ii/ch05_reward_irrecoverability.md#L64-L70). Online, [Geometric AI](https://erisml.org/geometric-ai/ch05_reward_irrecoverability.html).

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

kernel, null-space, reward-irrecoverability-theorem, alignment-failure-taxonomy, collective-alignment-gap

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
