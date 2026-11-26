# Corruption tensor

**id.** corruption-tensor
**kind.** concept
**volume.** Geometric Reasoning, Volume 3 of the Geometric Series

## definition

The first-order response of a system's final judgment to task-irrelevant perturbations. Entry $C_{ij}$ gives the displacement of judgment dimension $i$ per unit intensity of perturbation direction $j$. It is the Jacobian of the judgment endpoint with respect to the perturbation intensities, taken at zero perturbation.

**Example.** With one perturbation direction whose column is (4, -2) and an intensity of 0.5, the first-order displacement of the judgment is (2, -1).

## equation

none

## conditions

- The tensor is tagged a modeling axiom. It is a linear response and holds to first order in the perturbation intensity.
- It is specific to a model and is not symmetric in general. A column of zeros marks a perturbation the system is invariant to.
- The benchmark probes three columns, for framing, emotional anchoring and sensory distractors. The volume says mapping the full tensor remains an open empirical program.
- No entry of the tensor is reported as a number. The data are significance levels and score drifts that the volume reads as projections of columns.

Conditions are curated in `volumes/geometric-reasoning.toml` rather than read from a record.

## ledger

none. *standing.* The tensor is posited. What is measured is displacement under three perturbation types on five models, reported with combined significance of 8.9, 6.8 and 4.6 sigma, and no significant displacement under gender swap or evaluation order.

## first stated

Definition 5.1, [`geometric-reasoning/chapters/ch05_heuristic_corruption.md:326-334`](https://github.com/ahb-sjsu/geometric-reasoning/blob/881f075/chapters/ch05_heuristic_corruption.md#L326-L334), introduced in Section 5.5, [`geometric-reasoning/chapters/ch05_heuristic_corruption.md:172-182`](https://github.com/ahb-sjsu/geometric-reasoning/blob/881f075/chapters/ch05_heuristic_corruption.md#L172-L182). Online, [Geometric Reasoning](https://erisml.org/geometric-reasoning/ch05_heuristic_corruption.html).

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

jacobian, heuristic-field, model-robustness-profile, reasoning-bond-invariance-principle, nuisance, singular-value-decomposition

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
