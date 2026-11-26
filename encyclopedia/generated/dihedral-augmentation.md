# D4 augmentation and the orbit-stabilizer count

**id.** dihedral-augmentation
**kind.** instrument
**volume.** Geometric Methods, Volume 1 of the Geometric Series

## definition

Apply the eight rotations and reflections of the square, the dihedral group D4, to a grid, and use the resulting orbit as equivalent training examples. The number of distinct grids in the orbit times the number of group elements that leave the grid unchanged is 8.

**Example.** A grid left unchanged by the identity and the half turn only has 2 such elements, so its orbit has 8/2 = 4 distinct grids.

**Known as, or related to prior art.** Data augmentation by a symmetry group, with the orbit-stabilizer theorem and Burnside's lemma.

## equation

none

## conditions

- The target function must be invariant under the group. Augmentation encourages a model to learn that invariance and does not guarantee it.
- For an input and output pair the same transform is applied to both, or the augmented pair encodes a different rule.
- A grid with internal symmetry yields duplicates. A grid of orbit size 2 among grids of orbit size 8 is overrepresented by a factor of 4 unless the duplicates are removed.
- The eightfold reduction of the hypothesis space is stated only up to factors that depend on the structure of the group action.

Conditions are curated in `volumes/geometric-methods.toml` rather than read from a record.

## ledger

none. *standing.* The README's status note of 2026-07-14 calls this volume the series' metrology discipline, a method that is normative and not a finding. Its Section 21.8 (November 2026) classes each result as proved, posited, or measured on a recorded run, and the tables of Chapters 1, 8, 9, 11 and 12 are posited illustrations.

## first stated

Chapter 13, [`geometric-methods/chapters/chapter-13-group-theoretic-augmentation.md:10-12`](https://github.com/ahb-sjsu/geometric-methods/blob/371478c/chapters/chapter-13-group-theoretic-augmentation.md#L10-L12), with the orbit-stabilizer count in Section 13.6.1, [`geometric-methods/chapters/chapter-13-group-theoretic-augmentation.md:301-305`](https://github.com/ahb-sjsu/geometric-methods/blob/371478c/chapters/chapter-13-group-theoretic-augmentation.md#L301-L305). Online, [Geometric Methods](https://erisml.org/geometric-methods/chapter-13-group-theoretic-augmentation.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Methods*, Volume 1 of the Geometric Series.

## related

quotient, nuisance, paraphrase-class, gradient-reversal-layer

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
