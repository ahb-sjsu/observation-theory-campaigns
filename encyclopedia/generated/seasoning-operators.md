# seasoning operators (salt, acid, fat, heat)

**id.** seasoning-operators
**kind.** concept
**volume.** Geometric Gastronomy, Volume 12 of the Geometric Series

## definition

Four maps from flavor space to itself. Salt stretches the savory component by a factor $\lambda > 1$, as $T(\mathbf{f}) = \mathbf{f} + (\lambda - 1)P_{sav}\mathbf{f}$. Acid rotates the vector toward a brightness axis. Fat is a low-pass filter on the temporal flavor curve. Heat is a flow that releases volatiles at temperature-dependent rates. They do not commute.

**Example.** Take the vector (3, 4) with the savory subspace as the first axis and $\lambda = 1.5$. Salt gives (4.5, 4). On the vector (0, 4), which has no savory component, the same operator changes nothing, the volume's point that salt cannot make a savory direction from nothing. The numbers are illustrative.

**Known as, or related to prior art.** The four elements of Nosrat's Salt, Fat, Acid, Heat (2017).

## equation

none

## conditions

- Each operator is tagged a modeling axiom. The forms are posited, and none is fitted to data.
- Salt cannot create a savory direction the dish lacks, and its factor is bounded. Past the bound the dish moves toward the salt vertex and the no-rotation approximation fails.
- The four are a generating set with approximate inverses, not a basis of a vector space. The volume calls the basis imperfect, since heat bundles a thermal flow with a trigeminal translation.
- The inverses are lossy. Salt can be added and cannot be cleanly removed.

Conditions are curated in `volumes/geometric-gastronomy.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, with no gastronomy instrument evaluated by the series' admission filter (xbse) and the nearest evaluated perceptual domains, aesthetics and music, rated inadmissible to medium. Its claims are to be read as theory at licensed strength and not as validated measurement, and the chapters tag each statement as a modeling axiom, empirical, a conjecture or a theorem. Since the corrections of 2026-11-26 the analyses the volume describes carry the tag that no run is recorded for this volume, and their outcomes are worded as predictions.

## first stated

Chapter 6, [`geometric-gastronomy/chapters/ch06_the_algebra_of_seasoning.md:24-24`](https://github.com/ahb-sjsu/geometric-gastronomy/blob/1b6657d/chapters/ch06_the_algebra_of_seasoning.md#L24-L24), with the generating set and its non-commutation in Section 6.5, [`geometric-gastronomy/chapters/ch06_the_algebra_of_seasoning.md:90-96`](https://github.com/ahb-sjsu/geometric-gastronomy/blob/1b6657d/chapters/ch06_the_algebra_of_seasoning.md#L90-L96). Online, [Geometric Gastronomy](https://erisml.org/geometric-gastronomy/ch06_the_algebra_of_seasoning.html).

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

seasoning-fixed-point, cooking-non-commutativity, projection, anisotropic, flavor-space

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
