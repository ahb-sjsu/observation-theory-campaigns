# Nadeau and Bengio correction

**id.** nadeau-and-bengio-correction
**kind.** correction

## definition

The inflation of the variance of a repeated cross-validation estimate by one plus the ratio of test to training size times the number of repeats, because the folds are not independent. Equation 0.18.

## equation

Book equation 0.18.

    \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2},\qquad \frac{\widehat{\operatorname{Var}}_{\mathrm{NB}}}{\hat\sigma^{2}/J}=1+J\,\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}.

Book equation 8.2.

    \begin{gathered} \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2}, \\ J=1000,\ \frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}=\frac14\ \Rightarrow\ 1+250=251,\ \ \sqrt{251}=15.84. \end{gathered}

## ledger

none

## first stated

Nadeau and Bengio, inference for the generalization error, 2003, as chapter 8 cites it, applied to the program's own comparison in `constraint-gap/review/FINDINGS.md:1-35` and chapter 8 section 8.5 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 6 section 6.4 | the uncorrected t stored as sigma, 251 and 15.84, nine wins to three, seven, eight, 3 wins 17 ties 11 losses on 31 datasets, the three-way inconsistency | `constraint-gap\review\FINDINGS.md:1-35`; `constraint-gap\README.md:57-76` |
| chapter 6 section 6.4 | the reviewer's revision plan, drop sigma, bounded claim, 19 at 200 by 5 vs 11 at 20 by 5, rerun in progress | `theory-radar\paper\REVISION_PLAN.md:1-60` |
| chapter 6 section 6.4 | five analyses negative, 0.2 percent of floor, twelve times the band, learning-curve redesign | `constraint-gap\README.md:57-76`; `constraint-gap\review\REDESIGN.md:1-45` |
| chapter 6 section 6.5 | loading weights and stability across folds requested | `theory-radar\paper\REVISION_PLAN.md` issue 6 |
| chapter 7 section 7.3 | correlation negative 0.59 at p 4.8e-4 with size, negative 0.562 at p 0.001 with the ensemble's score, predictive 0.345 and 0.589, interval negative 0.165 to 0.125, the one-line summary | `constraint-gap\review\INDETERMINATES.md:60-80`; `constraint-gap\review\REDESIGN.md:45-70` |
| chapter 7 section 7.4 | the redesign, grid 50 to N, ten folds, twenty repetitions, crossing size, the 800-row boundary declared in advance, seventeen at median 0.006 and p 0.964, store the folds | `constraint-gap\review\REDESIGN.md:1-110` |
| chapter 8 section 8.5 | variance inflation 251, SE inflation 15.84, J_eff 3.98, about 62 needed, 3 of 9 at full, 7 at half, 8 at a third | `constraint-gap\review\FINDINGS.md:1-35` |
| chapter 8 section 8.5 | 9/3/19 to 3/17/11, five negative analyses, 0.2 percent of floor, twelve times the band, learning-curve redesign | `constraint-gap\README.md:57-76`; `constraint-gap\review\REDESIGN.md` |
| chapter 8 section 8.5 | three-way inconsistency, lines 544, 548 to 556, 755 | `constraint-gap\review\FINDINGS.md:7-31` against `theory-radar\paper\theory_radar_v6_submission.tex` |

## failures and corrections

- `theory-radar/paper/REVISION_PLAN.md:39-45` at 37c4e6c. **Fix:** - Drop "σ significance" everywhere - Report: mean ΔF1, std, 95% CI, and corrected resampled t-statistic - Table columns: "Test F1", "GB F1", "ΔF1", "95% CI", "Direction" - Text: "the formula outperforms GB by ΔF1=0.031, 95% CI [0.028, 0.034]" - Add Nadeau-Bengio corrected t-test (accounts for CV fold correlation) - Keep effect size as supplementary but don't call it "σ"

## conditions

- Repeated cross-validation folds share training data, so the naive variance of a mean difference is multiplied by one plus the fold count times the test-to-train ratio. The corrected variance is never below the naive one and the inflation grows without bound in the fold count.
- With a thousand folds at a ratio of one quarter the inflation is 251, the standard error grows by 15.84, and about four folds' worth of independent evidence remain. The program's nine wins became three under it, with seventeen indeterminate.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/NadeauBengio.lean`, theorems `correctedVar_eq`, `naiveVar_le_correctedVar`, `inflation_unbounded`, `book_numbers`, at observation-data-mining 7eba709.

## used in

*Data Mining as Observation* chapters 0, 6, 7, 8.

## related

harness, formula-search, preregistration, multiple-comparisons

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns f5585e7, theory-radar 37c4e6c, observation-data-mining 7eba709, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
