# False termination region

**id.** false-termination-region
**kind.** result
**volume.** Geometric Reasoning, Volume 3 of the Geometric Series

## definition

The set of states outside the goal where the heuristic reads below the stopping threshold while the true distance to the goal is large. A search that halts when $h(x)$ falls below the threshold and enters this set stops outside the goal. The volume reads overconfidence as this underestimation of cost-to-go.

**Example.** With a stopping threshold of 1, a state where the heuristic reads 0.5 and the true distance to the goal is 3 lies in the region, since the search halts there 3 units short.

## equation

none

## conditions

- It assumes a satisficing search with a fixed threshold. The heuristic must underestimate the true cost-to-go by more than the threshold on a region that does not meet the goal.
- Tagged a conditional theorem. The identification of a model's stated confidence with the terminal value of an implicit heuristic is the volume's modeling step.
- The measured part is separate. All five models were overconfident on the calibration task, with expected calibration errors from 0.230 to 0.415.

Conditions are curated in `volumes/geometric-reasoning.toml` rather than read from a record.

## ledger

none. *standing.* A conditional statement about threshold search, given without a full proof. The calibration errors it is attached to are benchmark measurements, and the link between the two is posited.

## first stated

Proposition 3.1 and Corollary 3.1, [`geometric-reasoning/chapters/ch03_the_heuristic_field.md:439-441`](https://github.com/ahb-sjsu/geometric-reasoning/blob/881f075/chapters/ch03_the_heuristic_field.md#L439-L441), with the reading of overconfidence in Section 3.6.3, [`geometric-reasoning/chapters/ch03_the_heuristic_field.md:273-277`](https://github.com/ahb-sjsu/geometric-reasoning/blob/881f075/chapters/ch03_the_heuristic_field.md#L273-L277). Online, [Geometric Reasoning](https://erisml.org/geometric-reasoning/ch03_the_heuristic_field.html).

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

heuristic-field, heuristic-admissibility, expected-calibration-error, calibration, reasoning-basin-of-attraction

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
