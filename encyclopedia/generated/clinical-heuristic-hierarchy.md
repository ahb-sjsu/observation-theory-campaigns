# Four-category hierarchy of clinical heuristics

**id.** clinical-heuristic-hierarchy
**kind.** concept
**volume.** Geometric Medicine, Volume 8 of the Geometric Series

## definition

A grading of a clinical heuristic $h$ against the true remaining cost $h^*$. It is strictly admissible when it is far below $h^*$, epsilon-admissible when $h \le (1 + \varepsilon) h^*$ for a small $\varepsilon$, inadmissible when it exceeds $h^*$ somewhere, and gauge-variant when its value changes under a meaning-preserving re-description of the situation.

**Example.** Let the true remaining cost be 10 and take epsilon as 0.1, the volume's figure for a clinician at the start of a career. An estimate of 10.5 is within 11 and is epsilon-admissible, with paths costing at most 1.1 times the optimum. An estimate of 15 is inadmissible. An estimate that reads 8 for continue the drug and 12 for do not stop the drug is gauge-variant.

**Known as, or related to prior art.** Admissible and bounded-suboptimal heuristics of A* search. The fourth category is the framing effect of the decision literature.

## equation

none

## conditions

- An epsilon-admissible heuristic gives paths that cost at most $(1 + \varepsilon)$ times the optimal cost.
- The volume reserves the label cognitive bias for the gauge-variant category, with omission bias as its first example.
- The values of epsilon quoted for trainees and experienced clinicians are not measured. Proposition 7.5, that moral injury raises epsilon on the violated dimension only, is given as a testable prediction.
- As written, a heuristic that overestimates slightly meets both the epsilon-admissible and the inadmissible definitions. The volume separates them by whether the error is small.

Conditions are curated in `volumes/geometric-medicine.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, and says a clinical instrument is plausible but has not been built or gated. Its Section 18.9 says the covariance matrix has not been estimated and the clinical Bond Index has not been computed from clinical data, so every number in these entries is an illustration unless the entry says otherwise.

## first stated

Section 7.2, Definitions 7.1 to 7.4, [`geometric-medicine/manuscript/part_ii/ch07_heuristic_spectrum.md:38-90`](https://github.com/ahb-sjsu/geometric-medicine/blob/c220ac9/manuscript/part_ii/ch07_heuristic_spectrum.md#L38-L90). Online, [Geometric Medicine](https://erisml.org/geometric-medicine/ch07_heuristic_spectrum.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Medicine*, Volume 8 of the Geometric Series.

## related

clinical-heuristic-admissibility, heuristic-admissibility, reasoning-gauge-transformation, consent-gauge-invariance, clinical-moral-injury

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
