# Cross-modality sign flip

**id.** cross-modality-sign-flip
**kind.** result
**volume.** Geometric Aesthetics, Volume 13 of the Geometric Series

## definition

Two channels have opposite signs of association with reception in books and in music. Internal coherence is positive for book rating ($\rho = +0.126$) and negative for music listens ($\rho = -0.076$). Mean step size is negative for books ($\rho = -0.096$) and positive for music ($\rho = +0.071$).

**Example.** The volume's table gives pair_sim_mean a correlation of +0.126 with book rating and -0.076 with music listens. The two have opposite signs, and so do -0.096 and +0.071 for step_mean.

## equation

none

## conditions

- Two modalities only. The targets also differ (Goodreads rating for books, log listens for music), and so do the encoders (LaBSE and MERT).
- The volume has not ruled out that the flip comes from the encoders. Section 17.9 and Appendix E.4 keep that as a legitimate alternative reading.
- Appendix E says the flip was checked after the Hellinger fix and persists. Section 12.5 says the flips are not reported on genre-residualized targets.
- Extension of the pattern to film, visual art or architecture is marked conjectured in Appendix F (F22.1, F29.4). The README lists cross-modal sign flips among the reasons the AesBSE instrument was ruled inadmissible.

Conditions are curated in `volumes/geometric-aesthetics.toml` rather than read from a record.

## ledger

none. *standing.* Verified empirically in Appendix F (F21.6, F21.7). The reading that books reward continuity and music rewards contrast is the volume's interpretation, and Chapter 12 treats the flip as a broken symmetry of its invariance claim.

## first stated

Section 17.6.3, [`geometric-aesthetics/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md:172-189`](https://github.com/ahb-sjsu/geometric-aesthetics/blob/dc255d3/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md#L172-L189). Stated as Claim 17.2 at [`geometric-aesthetics/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md:201-203`](https://github.com/ahb-sjsu/geometric-aesthetics/blob/dc255d3/book/src/chapter-17-empirical-evidence-for-geometric-aesthetics.md#L201-L203). Online, [Geometric Aesthetics](https://erisml.org/geometric-aesthetics/chapter-17-empirical-evidence-for-geometric-aesthetics.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Aesthetics*, Volume 13 of the Geometric Series.

## related

aesthetic-internal-coherence, aesthetic-trajectory-channel, aesthetic-invariance-claim, aesthetic-regime, aesthetic-falsification-criteria, flip

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
