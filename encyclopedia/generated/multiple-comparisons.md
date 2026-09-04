# multiple comparisons

**id.** multiple-comparisons
**kind.** concept

## definition

The inflation of false positives when many hypotheses are tested and the best is reported. The Bonferroni correction divides the threshold by the number of tests. Chapter 0 section 0.9.

## equation

Book equation 8.3.

    \Pr[\text{at least one of } m\text{ null tests passes}]=1-(1-\alpha)^{m},\qquad \alpha_{\mathrm{Bonferroni}}=\frac{\alpha}{m}.

## ledger

none

## first stated

Chapter 0 section 0.9 and chapter 8 section 8.5 of *Data Mining as Observation*, with the program's own case in `constraint-gap/review/FINDINGS.md:1-35`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 6 section 6.4 | the uncorrected t stored as sigma, 251 and 15.84, nine wins to three, seven, eight, 3 wins 17 ties 11 losses on 31 datasets, the three-way inconsistency | `constraint-gap\review\FINDINGS.md:1-35`; `constraint-gap\README.md:57-76` |
| chapter 6 section 6.4 | five analyses negative, 0.2 percent of floor, twelve times the band, learning-curve redesign | `constraint-gap\README.md:57-76`; `constraint-gap\review\REDESIGN.md:1-45` |
| chapter 7 section 7.3 | correlation negative 0.59 at p 4.8e-4 with size, negative 0.562 at p 0.001 with the ensemble's score, predictive 0.345 and 0.589, interval negative 0.165 to 0.125, the one-line summary | `constraint-gap\review\INDETERMINATES.md:60-80`; `constraint-gap\review\REDESIGN.md:45-70` |
| chapter 7 section 7.4 | the redesign, grid 50 to N, ten folds, twenty repetitions, crossing size, the 800-row boundary declared in advance, seventeen at median 0.006 and p 0.964, store the folds | `constraint-gap\review\REDESIGN.md:1-110` |
| chapter 8 section 8.5 | variance inflation 251, SE inflation 15.84, J_eff 3.98, about 62 needed, 3 of 9 at full, 7 at half, 8 at a third | `constraint-gap\review\FINDINGS.md:1-35` |
| chapter 8 section 8.5 | 9/3/19 to 3/17/11, five negative analyses, 0.2 percent of floor, twelve times the band, learning-curve redesign | `constraint-gap\README.md:57-76`; `constraint-gap\review\REDESIGN.md` |

## failures and corrections

none

## conditions

- Test many hypotheses and report the best, and the reported score is the maximum of many noisy draws, at least any single draw. Ten thousand null tests at five percent pass five hundred by chance, forty pass two, and the expected passes grow without bound in the number of tests.
- The Bonferroni correction divides the threshold by the number of tests and keeps the family-wise rate under the target, and a preregistration that names one look needs no correction.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/MultipleComparisons.lean`, theorems `max_ge_each`, `book_numbers`, `corrected_family_rate`, `expectedPasses_unbounded`, at observation-data-mining 2b1108b.

## used in

*Data Mining as Observation* chapters 0, 5, 8.

## related

harness, nadeau-and-bengio-correction, preregistration, formula-search

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 4d22223, theory-radar 37c4e6c, observation-data-mining 2b1108b, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
