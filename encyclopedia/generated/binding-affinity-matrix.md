# binding affinity matrix

**id.** binding-affinity-matrix
**kind.** concept
**volume.** Geometric Gastronomy, Volume 12 of the Geometric Series

## definition

The matrix $A$ with one row per receptor type (about 400) and one column per chemical species (about 10,000), whose entry $A_{ij}$ is the affinity of receptor i for molecule j. Transduction is modeled as $\mathbf{r} = A\mathbf{c}$. Chemical variation in the null space of $A$ is odorless and tasteless, and distinct stimuli with the same image are metamers.

**Example.** Take one receptor with affinities (2, 1) for two species. The stimuli (1, 0) and (0, 2) both give response 2, so they are metamers, and their difference (1, -2) lies in the null space. At the volume's sizes, about 400 rows against about 10,000 columns leave a null space of dimension at least 9,600. The small numbers are illustrative.

## equation

none

## conditions

- Tagged a modeling axiom, valid within the sub-saturating regime of each receptor. Real dose-response curves are sigmoidal, and the linear form fails at saturation.
- Competitive binding and state-dependent receptors, such as miraculin switching the sweet receptor to acid activation, change the entries with context. The volume calls the linear map the tangent-plane approximation.
- The matrix is wide and rank-deficient, so the map from chemistry to receptor response is far from injective. It is also sparse and structured, which the volume uses to argue for the second compression to 10 to 30 perceptual dimensions.

Conditions are curated in `volumes/geometric-gastronomy.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, with no gastronomy instrument evaluated by the series' admission filter (xbse) and the nearest evaluated perceptual domains, aesthetics and music, rated inadmissible to medium. Its claims are to be read as theory at licensed strength and not as validated measurement, and the chapters tag each statement as a modeling axiom, empirical, a conjecture or a theorem. Since the corrections of 2026-11-26 the analyses the volume describes carry the tag that no run is recorded for this volume, and their outcomes are worded as predictions.

## first stated

Section 2.3, [`geometric-gastronomy/chapters/ch02_the_receptor_basis.md:54-64`](https://github.com/ahb-sjsu/geometric-gastronomy/blob/1b6657d/chapters/ch02_the_receptor_basis.md#L54-L64). Online, [Geometric Gastronomy](https://erisml.org/geometric-gastronomy/ch02_the_receptor_basis.html).

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

null-space, kernel, quotient, matrix, read-operator, flavor-space

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
