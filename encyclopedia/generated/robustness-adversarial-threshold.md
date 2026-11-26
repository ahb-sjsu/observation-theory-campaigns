# Adversarial threshold

**id.** robustness-adversarial-threshold
**kind.** instrument
**volume.** Geometric Reasoning, Volume 3 of the Geometric Series

## definition

For one perturbation type, the smallest intensity $\epsilon^*$ at which performance falls more than a chosen tolerance $\delta$ below its unperturbed value. It is found by binary search on the intensity, and the vector of thresholds over perturbation types is the threshold profile.

**Example.** With a baseline of 0.90 and a tolerance of 0.10, a performance of 0.85 at intensity 0.2 and 0.78 at intensity 0.4 puts the threshold between 0.2 and 0.4, and the next probe is at 0.3.

## equation

none

## conditions

- It needs a perturbation family with a continuous intensity and a user-chosen tolerance. Binary search also assumes that performance falls as intensity rises.
- The volume ran no threshold search. Its evidence is indirect, a reading of four sycophancy rates at one fixed intensity as models below, near or past their thresholds.
- This reading replaces the continuous sycophancy parameter of Chapter 6 with model-specific thresholds, and the volume does not reconcile the two.

Conditions are curated in `volumes/geometric-reasoning.toml` rather than read from a record.

## ledger

none. *standing.* A proposed procedure. No threshold is measured in the volume.

## first stated

Section 10.4.1, [`geometric-reasoning/chapters/ch10_the_robustness_surface.md:177-185`](https://github.com/ahb-sjsu/geometric-reasoning/blob/149995b/chapters/ch10_the_robustness_surface.md#L177-L185), with the search procedure at [`geometric-reasoning/chapters/ch10_the_robustness_surface.md:220-230`](https://github.com/ahb-sjsu/geometric-reasoning/blob/149995b/chapters/ch10_the_robustness_surface.md#L220-L230). Online, [Geometric Reasoning](https://erisml.org/geometric-reasoning/ch10_the_robustness_surface.html).

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

model-robustness-profile, sycophancy-parameter, threshold, sweep

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
