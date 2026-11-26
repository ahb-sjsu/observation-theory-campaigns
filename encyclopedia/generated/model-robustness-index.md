# Model Robustness Index (MRI)

**id.** model-robustness-index
**kind.** instrument
**volume.** Geometric Methods, Volume 1 of the Geometric Series

## definition

Multiply each parameter by an independent log-normal factor, and for each draw record $\omega$, the absolute change in the model's error from baseline. The index is 0.5 times the mean of $\omega$ plus 0.3 times its 75th percentile plus 0.2 times its 95th percentile. Lower is more robust.

**Example.** With a mean of 0.8, a 75th percentile of 1.4 and a 95th percentile of 3.1, the index is 0.40 + 0.42 + 0.62 = 1.44. These are the volume's hypothetical values.

## equation

none

## conditions

- The defaults are 300 draws and a log-scale standard deviation of 0.5, with perturbed values clamped to the range 0.001 to 1,000,000. The volume asks for the index at several scales.
- An index of exactly zero can mean that the evaluation function cannot see the perturbation. In the recorded run of Chapter 19 it was zero because the function reads only whether each parameter is below 1000.
- The values in Chapter 9 are hypothetical. The recorded values are those of Chapter 19, which are exploratory.
- The Decoder Robustness Index of Section 10.5 applies the same formula to perturbations of the input signal, with a graded semantic distance in place of the change in error.

Conditions are curated in `volumes/geometric-methods.toml` rather than read from a record.

## ledger

none. *standing.* A definition. Appendix C states the convergence of the empirical index as Theorem C.6, proved in writing, and the worked values of Chapter 9 are posited.

## first stated

Sections 9.2.1 and 9.2.2, [`geometric-methods/chapters/chapter-09-adversarial-robustness.md:83-102`](https://github.com/ahb-sjsu/geometric-methods/blob/371478c/chapters/chapter-09-adversarial-robustness.md#L83-L102). Online, [Geometric Methods](https://erisml.org/geometric-methods/chapter-09-adversarial-robustness.html).

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

sensitivity, percentile, defect-campaign-null-result, admissibility-checks, pairwise-interaction-matrix

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
