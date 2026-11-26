# Consistent group augmentation

**id.** group-consistent-augmentation
**kind.** instrument
**volume.** Geometric Reasoning, Volume 3 of the Geometric Series

## definition

Training-data augmentation by a task's symmetry group in which the same group element is applied to every component of a training example. The task symmetry group is the largest group of input transformations that leave the ground-truth label unchanged. Applying the element to some components and not others is inconsistent augmentation.

**Example.** The symmetry group of a square grid has 8 elements, 4 rotations and 4 reflections, so one input and output grid pair yields 8 consistent variants when each element is applied to both grids.

**Known as, or related to prior art.** Data augmentation by a symmetry group, as in invariant and equivariant learning. The volume attributes the consistency principle to Geometric Methods, Chapter 13.

## equation

none

## conditions

- The symmetry group must be known for the task. The volume lists six groups for six task types, one of them the identity alone.
- The claim that training on the augmented set yields an invariant function holds in the limit of sufficient capacity and training.
- Definition 14.2 holds the label fixed while the group acts on the input, and the consistency principle and Definition 14.3 apply the same element to input and output together. The volume relates the two. The fixed-label form is the case in which the group acts trivially on labels.
- The volume reports parse rates and data expansion for its pipeline. It reports no measured gain in invariance or accuracy from the augmentation.

Conditions are curated in `volumes/geometric-reasoning.toml` rather than read from a record.

## ledger

none. *standing.* An engineering practice the volume implemented. The framing of it as restoring a broken gauge symmetry of a reasoning manifold is posited, and no before-and-after invariance measurement is given.

## first stated

Section 14.1, the consistency principle, [`geometric-reasoning/chapters/ch14_from_theory_to_engineering.md:48-52`](https://github.com/ahb-sjsu/geometric-reasoning/blob/b645f23/chapters/ch14_from_theory_to_engineering.md#L48-L52), and Definitions 14.1 and 14.2 with Proposition 14.1, [`geometric-reasoning/chapters/ch14_from_theory_to_engineering.md:366-370`](https://github.com/ahb-sjsu/geometric-reasoning/blob/b645f23/chapters/ch14_from_theory_to_engineering.md#L366-L370). Online, [Geometric Reasoning](https://erisml.org/geometric-reasoning/ch14_from_theory_to_engineering.html).

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

reasoning-gauge-transformation, reasoning-bond-invariance-principle, fine-tuning, quotient

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
