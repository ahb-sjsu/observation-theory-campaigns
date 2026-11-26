# empty quadrant (metacognition)

**id.** metacognitive-empty-quadrant
**kind.** result
**volume.** Geometric Cognition, Volume 6 of the Geometric Series

## definition

In the plane of self-monitoring accuracy (M3) and effort scaling index (M4), split at a threshold on each axis, no tested model lies in Quadrant I, where both exceed the threshold. The volume reads the gap as a structural constraint.

**Example.** With the appendix's threshold of 0.25, Gemini 2.5 Pro at (0.500, 0.000) is in Quadrant II and Gemini 2.0 Flash at (0.042, 0.827) is in Quadrant IV. Their differences are 0.458 on M3 and -0.827 on M4, as the volume prints.

## equation

none

## conditions

- Section 9.7 tabulates four models. Technical Appendix 9B gives their M3 and M4 correlation as about -0.98, with p about 0.02 on two degrees of freedom, and says four chosen models are not a random sample.
- The appendix uses a threshold of 0.25, and the volume says the midpoints of 0.5 and the medians leave the same quadrant empty. In the table of Section 9.7 the quadrant is not empty for a threshold below 0.149.
- The volume says that with so few models a sampling artifact cannot be excluded. The structural constraint and the topological hole are its interpretations, and it frames the hole with the words if this interpretation is correct.
- M3 and M4 values for the same models differ between chapters. Gemini 3 Flash has M3 of 0.149 in Section 9.7 and 0.250 in Section 16.7, and Gemini 2.5 Flash has 0.111 in the first and 0.167 in the second.

Conditions are curated in `volumes/geometric-cognition.toml` rather than read from a record.

## ledger

none. *standing.* The ledger grades the observation exploratory (GC-20), with its primary artifacts not in the repository.

## first stated

Section 9.8, [`geometric-cognition/chapters/ch09_metacognition.md:193-205`](https://github.com/ahb-sjsu/geometric-cognition/blob/93e39e2/chapters/ch09_metacognition.md#L193-L205), with Definition 9.5, [`geometric-cognition/chapters/ch09_metacognition.md:217-224`](https://github.com/ahb-sjsu/geometric-cognition/blob/93e39e2/chapters/ch09_metacognition.md#L217-L224). Online, [Geometric Cognition](https://erisml.org/geometric-cognition/ch09_metacognition.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Cognition*, Volume 6 of the Geometric Series.

## related

metacognitive-recovery-ceiling, capability-frontier-convergence, cognitive-signature, threshold

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
