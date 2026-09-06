# challenge set

**id.** challenge-set
**kind.** instrument

## definition

A test collection built so that a shortcut which passes the benchmark fails on it. Chapter 12.

## equation

Book equation 14.2.

    \mathrm{coverage\ difference}_c=\mathrm{AUROC}_c(\text{embedding})-\mathrm{AUROC}_c(\text{validated axes}),\qquad \text{floor}\approx0.08\ \text{to}\ 0.12.

## ledger

- NEG-15 (Bell boundary). *Query-conditioned hubness supplies a mechanism for Bell-inequality violation without action at a distance.* Refuted as a mechanism; the settings-as-queries reframing survives only as vocabulary. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:93` at 01e53bc.

## first stated

Chapter 12 section 12.6 and chapter 14 section 14.3 of *Data Mining as Observation*, with the program's identity-attack and euphemism sets in `gtc-prototype/docs/SPECTRUM_FINDINGS.md:66-99`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 6 section 6.4 | five analyses negative, 0.2 percent of floor, twelve times the band, learning-curve redesign | `constraint-gap\README.md:57-76`; `constraint-gap\review\REDESIGN.md:1-45` |
| chapter 7 section 7.3 | correlation negative 0.59 at p 4.8e-4 with size, negative 0.562 at p 0.001 with the ensemble's score, predictive 0.345 and 0.589, interval negative 0.165 to 0.125, the one-line summary | `constraint-gap\review\INDETERMINATES.md:60-80`; `constraint-gap\review\REDESIGN.md:45-70` |
| chapter 7 section 7.4 | the redesign, grid 50 to N, ten folds, twenty repetitions, crossing size, the 800-row boundary declared in advance, seventeen at median 0.006 and p 0.964, store the folds | `constraint-gap\review\REDESIGN.md:1-110` |
| chapter 8 section 8.5 | 9/3/19 to 3/17/11, five negative analyses, 0.2 percent of floor, twelve times the band, learning-curve redesign | `constraint-gap\README.md:57-76`; `constraint-gap\review\REDESIGN.md` |

## failures and corrections

none

## conditions

- A test collection built so that a shortcut which passes the benchmark fails on it. Every finite benchmark admits a shortcut, the lookup that returns the stored label for every benchmark row, and two scorers that agree on every benchmark row have the same benchmark error whatever they do elsewhere.
- A challenge set is any collection on which the shortcut and the intended rule disagree, which can only lie outside the benchmark, and on it the shortcut's error is positive while its benchmark error is zero.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ChallengeSet.lean`, theorems `shortcut_passes`, `shortcut_fails`, `benchmark_blind`, `challenge_outside`, at observation-data-mining 424e077.

## used in

*Data Mining as Observation* chapters 0, 9, 11, 12.

## related

leakage, harness, deployment-mismatch, preregistration

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 01e53bc, observation-theory-campaigns 55ee1c6, theory-radar 37c4e6c, observation-data-mining 424e077, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
