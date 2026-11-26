# framing displacement (the 15.3 sigma effect)

**id.** cognitive-framing-displacement
**kind.** result
**volume.** Geometric Cognition, Volume 6 of the Geometric Series

## definition

On the T5 test, rewriting a scenario in a euphemistic or dramatic register with the moral facts fixed shifts each model's total harm score beyond its own re-judging noise. The volume reports the shift as 15.3 sigma, combined across five models by Fisher's method.

**Example.** For Gemini 2.5 Pro the volume prints a euphemistic drift of -14.1 on the 70-point scale against a control drift of 4.2. 14.1 / 70 is about 20 percent of the scale, and 14.1 / 4.2 is about 3.4 times the control.

## equation

none

## conditions

- The five models judge the same scenarios, so the per-model statistics are not fully independent. The volume says the combination is then anti-conservative and the true combined significance is lower than 15.3 sigma.
- The direction is not uniform. Claude's dramatic drift is -1.5, against +6.2 to +9.8 for the Gemini models.
- The figure was updated from an earlier 8.9 sigma after more scenario data and refined controls were included.

Conditions are curated in `volumes/geometric-cognition.toml` rather than read from a record.

## ledger

none. *standing.* The ledger grades the statistic exploratory (GC-11-S), since no registration predates the run and no result file or seed is in the repository. The reading as a framing effect in a social-cognitive dimension is held at posited (GC-11-I).

## first stated

Section 7.4, [`geometric-cognition/chapters/ch07_social_cognition.md:97-113`](https://github.com/ahb-sjsu/geometric-cognition/blob/3d5a346/chapters/ch07_social_cognition.md#L97-L113), with the statistic's construction in Technical Appendix 7B, [`geometric-cognition/chapters/ch07_social_cognition.md:357-373`](https://github.com/ahb-sjsu/geometric-cognition/blob/3d5a346/chapters/ch07_social_cognition.md#L357-L373). Online, [Geometric Cognition](https://erisml.org/geometric-cognition/ch07_social_cognition.html).

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

judgment-gauge-invariance, null-model, control, multiple-comparisons, sycophancy-gradient

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
