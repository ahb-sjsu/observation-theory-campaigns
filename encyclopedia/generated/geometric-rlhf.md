# Geometric RLHF

**id.** geometric-rlhf
**kind.** instrument
**volume.** Geometric AI, Volume 11 of the Geometric Series

## definition

A training protocol in which raters score responses on individual value dimensions, the value metric is fitted to those scores by inverse optimization under the constraint that it be symmetric positive-definite, and the policy is trained to minimize geodesic deviation from the value-aligned trajectory.

**Example.** With d = 9 the metric has 9 times 8 over 2, which is 36, off-diagonal components. Rating k = 3 dimensions per interaction gives 3 pairs each time, so 12 interactions give only 36 observed pairs and the volume's condition asks for far more than that.

**Known as, or related to prior art.** An extension of reinforcement learning from human feedback to per-dimension ratings and multi-objective optimization.

## equation

none

## conditions

- Rating all nine dimensions on every interaction is called impractical. The volume asks about 2 or 3 dimensions per interaction and says the metric is estimable when the observed pairwise relationships far exceed the $d(d-1)/2$ metric components.
- In practice the geodesic objective is replaced by a weighted multi-objective optimization with a KL penalty toward a reference policy.
- The stated costs (2.4 times the rater effort, about 1.5 times the training compute) and the reported gains come from the fictional ARIA-G run of 10,000 interactions with 15 raters. Chapter 20 calls the chapter a proof of concept and leaves the precision of the estimated metric open.

Conditions are curated in `volumes/geometric-ai.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status block of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, whose alignment thesis is theory at licensed strength and not validated measurement. It adds that no alignment instrument has been evaluated under the xbse admission filter, and the front matter says that ARIA, the system whose numbers fill the chapter tables, is fictional.

## first stated

Chapter 16, [`geometric-ai/manuscript/part_iv/ch16_geometric_rlhf.md:22-26`](https://github.com/ahb-sjsu/geometric-ai/blob/2363455/manuscript/part_iv/ch16_geometric_rlhf.md#L22-L26) (Definition 16.1), [`geometric-ai/manuscript/part_iv/ch16_geometric_rlhf.md:36-44`](https://github.com/ahb-sjsu/geometric-ai/blob/2363455/manuscript/part_iv/ch16_geometric_rlhf.md#L36-L44) (metric learning) and [`geometric-ai/manuscript/part_iv/ch16_geometric_rlhf.md:74-86`](https://github.com/ahb-sjsu/geometric-ai/blob/2363455/manuscript/part_iv/ch16_geometric_rlhf.md#L74-L86) (Definition 16.2). Online, [Geometric AI](https://erisml.org/geometric-ai/ch16_geometric_rlhf.html).

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

rlhf-irrecoverability, value-metric, tensor-valued-objective, reasoning-geodesic-deviation

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
