# Model Robustness Index as a profile

**id.** model-robustness-profile
**kind.** instrument
**volume.** Geometric Reasoning, Volume 3 of the Geometric Series

## definition

A vector with one component per perturbation type. Component $r_i$ is the average, over an evaluation set, of a consistency score between the model's output on an input and its output on the input perturbed by type $i$. The score lies between 0 and 1 and the components are not aggregated.

**Example.** A model whose verdict is unchanged on 3 of 4 inputs under reframing and on 4 of 4 under reordering has the profile (0.75, 1.00), with verdict agreement as the consistency score.

## equation

none

## conditions

- It is defined relative to a chosen set of perturbation types, an evaluation set and a consistency metric, and it changes with each choice.
- Tagged a modeling axiom. The volume says the MRI of Chapter 9 of Geometric Methods is a single weighted figure, the mean and the 75th and 95th percentiles of the error deviation with weights 0.5, 0.3 and 0.2, and that this chapter uses a profile instead, of which that figure is one summary.
- The correspondence with the corruption tensor, in which a component is 1 minus a normalized column norm, holds only for one stated consistency metric.
- The volume's composite track scores do aggregate. Their captions give them as weighted means of subtask scores. The weights were recovered by solving the tables and have not been confirmed against the benchmark code.

Conditions are curated in `volumes/geometric-reasoning.toml` rather than read from a record.

## ledger

none. *standing.* A defined measurement protocol. The profile values printed for five models are benchmark measurements, and the reading of the profile as a surface on a reasoning manifold is posited.

## first stated

Definition A10.1, [`geometric-reasoning/chapters/ch10_the_robustness_surface.md:516-524`](https://github.com/ahb-sjsu/geometric-reasoning/blob/149995b/chapters/ch10_the_robustness_surface.md#L516-L524), introduced in Section 10.2.1, [`geometric-reasoning/chapters/ch10_the_robustness_surface.md:74-84`](https://github.com/ahb-sjsu/geometric-reasoning/blob/149995b/chapters/ch10_the_robustness_surface.md#L74-L84). Online, [Geometric Reasoning](https://erisml.org/geometric-reasoning/ch10_the_robustness_surface.html).

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

corruption-tensor, robustness-adversarial-threshold, benchmark-scalar-irrecoverability, pareto-dominance

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
