# individual variation as a rotation of the receptor basis

**id.** receptor-basis-rotation
**kind.** concept
**volume.** Geometric Gastronomy, Volume 12 of the Geometric Series

## definition

Heritable receptor variation is modeled as a near-identity linear transformation $R$ of the reference affinity matrix, so an individual's basis is $A' = RA$ and their receptor vector is $\mathbf{r}' = R\mathbf{r}$. For a single-receptor polymorphism the action is approximately a rotation in the plane of the affected axis and its perceptual neighbors, together with a change of gain along that axis where the polymorphism rescales it.

**Example.** Let $R$ multiply the bitter coordinate by 2 and leave the rest fixed. A dish at bitter 1 in the reference frame reads as 2 for that eater, so a target of 1 needs a reference-frame design at 0.5, the pre-image under the inverse. The factor 2 is illustrative.

## equation

none

## conditions

- Tagged a modeling axiom. The rotation is an approximation for single-receptor polymorphisms such as TAS2R38 and OR6A2, where $R$ rescales or reorients one coordinate and leaves the others fixed. The volume notes that a rotation preserves length and cannot by itself represent a gain change.
- Variation in receptor density and gain is a second form that changes resolution and not orientation. The volume treats it separately as effective flavor dimensionality.
- Personalized design in Section 13.5 replaces the target by its pre-image $R^{-1}\mathbf{f}^\star$, an argument that needs only that $R$ is invertible. The volume conjectures that the binding constraint is measuring $R$ for one eater with enough fidelity, not the optimization.

Conditions are curated in `volumes/geometric-gastronomy.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, with no gastronomy instrument evaluated by the series' admission filter (xbse) and the nearest evaluated perceptual domains, aesthetics and music, rated inadmissible to medium. Its claims are to be read as theory at licensed strength and not as validated measurement, and the chapters tag each statement as a modeling axiom, empirical, a conjecture or a theorem. Since the corrections of 2026-11-26 the analyses the volume describes carry the tag that no run is recorded for this volume, and their outcomes are worded as predictions.

## first stated

Section 2.5, [`geometric-gastronomy/chapters/ch02_the_receptor_basis.md:99-99`](https://github.com/ahb-sjsu/geometric-gastronomy/blob/b43823b/chapters/ch02_the_receptor_basis.md#L99-L99), and its inverse use in Section 13.5, [`geometric-gastronomy/chapters/ch13_designing_flavors.md:90-90`](https://github.com/ahb-sjsu/geometric-gastronomy/blob/b43823b/chapters/ch13_designing_flavors.md#L90-L90). Online, [Geometric Gastronomy](https://erisml.org/geometric-gastronomy/ch02_the_receptor_basis.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Gastronomy*, Volume 12 of the Geometric Series.

## related

orthogonal-matrix, basis, effective-flavor-dimensionality, binding-affinity-matrix, inverse-flavor-problem

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
