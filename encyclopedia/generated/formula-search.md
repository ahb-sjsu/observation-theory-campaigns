# formula search

**id.** formula-search
**kind.** instrument

## definition

A score written as a short expression in the features, such as the smaller of two features plus a third, with a threshold. Chapter 6.

## equation

Book equation 6.2.

    \begin{gathered} \max_{\tau,\ \mathrm{dir}}F_1\!\Big(\mathbf 1\big[\mathrm{dir}\big(g(f(X)),\tau\big)\big],\,y\Big)=\max_{\tau,\ \mathrm{dir}}F_1\!\Big(\mathbf 1\big[\mathrm{dir}\big(f(X),\tau\big)\big],\,y\Big) \\ \text{for every strictly monotone } g. \end{gathered}

Book equation 5.4.

    \begin{gathered} F_1^{\max}\ \le\ \sup_{t\in[J,\,1]}\ \frac{2t\pi}{t\pi+\pi+(t-J)(1-\pi)},\qquad J=\max_{\tau}\big(\mathrm{TPR}-\mathrm{FPR}\big),\qquad \pi=\text{prevalence}, \\ J\le 2A-1\ \text{when the ROC curve is concave, and not in general.} \end{gathered}

Book equation 7.4.

    \begin{gathered} \Pr[\text{formula beats boosting on a new dataset}]=0.345\ \text{overall}, \\ 0.589\ \text{for } N<800, \qquad \text{predictive interval }[-0.165,\ +0.125]. \end{gathered}

Book equation 7.6.

    \begin{gathered} \Delta F_1^{(i)}(n)=\alpha_i+\beta\,\log n+\varepsilon, \\ n_{\mathrm{cross}}^{(i)}=\text{the training size at which the ensemble overtakes the formula}. \end{gathered}

## ledger

none

## first stated

theory-radar, DOI 10.5281/zenodo.20660206, `theory-radar/README.md`, with the corrected comparison in the constraint-gap review, `constraint-gap/review/REDESIGN.md:1-110`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 5 section 5.4 | Monotone Invariance and AUROC invariance theorems, the AUROC to F1 bound via the Youden index, stated in the source for every ROC curve and corrected in the book to concave curves, with the counterexample at AUROC 0.75 and F1 0.857 | `theory-radar\paper\astar_paper.tex:94-170`; `theory-radar\paper\theory_radar_paper.tex:290-304` |
| chapter 5 section 5.4 | seven thresholds up to 0.75, eight datasets, 56 conditions, zero admissibility violations, reductions 70 to 99.1 percent | `theory-radar\paper\astar_paper.tex:170-200` |
| chapter 5 section 5.4 | the rerun of 2026-09-03 and 2026-09-04, pre-filter counts 2576 of 8700 and 413 of 1560, ceiling violations 812 and 412, Youden pruning 199 and 38, A* optima 0.958 and 0.694 in strict and fast modes, Youden mode short by 0.006 and 0.002 | `theory-radar\results\rerun_youden_2026_09_03.json`; `theory-radar\ERRATA.md` |
| chapter 5 section 5.4 | learned pruning 88 to 99.6 percent with zero false negatives | `theory-radar\README.md:88-100` |
| chapter 6 section 6.3 | depth three, ten binary and eight unary operations, exact optimal F1 by sort and sweep, beam, projections | `theory-radar\README.md:50-100,140-200` |
| chapter 6 section 6.3 | Monotone Invariance Theorem and its proof | `theory-radar\paper\theory_radar_paper.tex:290-304`; `theory-radar\paper\astar_paper.tex:94-110` |
| chapter 6 section 6.3 | 88 to 99.6 percent pruned with zero false negatives, fair protocol, 200 by 5 folds | `theory-radar\README.md:88-100` |
| chapter 6 section 6.3 | the five-dataset table, breast cancer 0.955 to 0.963, the pattern, DOI 10.5281/zenodo.20660206 | `theory-radar\README.md:100-140` |
| chapter 6 section 6.4 | the uncorrected t stored as sigma, 251 and 15.84, nine wins to three, seven, eight, 3 wins 17 ties 11 losses on 31 datasets, the three-way inconsistency | `constraint-gap\review\FINDINGS.md:1-35`; `constraint-gap\README.md:57-76` |
| chapter 6 section 6.4 | the reviewer's revision plan, drop sigma, bounded claim, 19 at 200 by 5 vs 11 at 20 by 5, rerun in progress | `theory-radar\paper\REVISION_PLAN.md:1-60` |
| chapter 6 section 6.4 | five analyses negative, 0.2 percent of floor, twelve times the band, learning-curve redesign | `constraint-gap\README.md:57-76`; `constraint-gap\review\REDESIGN.md:1-45` |
| chapter 6 section 6.5 | loading weights and stability across folds requested | `theory-radar\paper\REVISION_PLAN.md` issue 6 |
| chapter 7 section 7.3 | the five-dataset outcomes | `theory-radar\README.md:100-140` |
| chapter 7 section 7.3 | correlation negative 0.59 at p 4.8e-4 with size, negative 0.562 at p 0.001 with the ensemble's score, predictive 0.345 and 0.589, interval negative 0.165 to 0.125, the one-line summary | `constraint-gap\review\INDETERMINATES.md:60-80`; `constraint-gap\review\REDESIGN.md:45-70` |
| chapter 7 section 7.4 | nine to three, seventeen indeterminate, five analyses zero resolved, three re-encode the correction | `constraint-gap\review\INDETERMINATES.md:1-40` |
| chapter 7 section 7.4 | the floor within 0.2 percent, fold ratios 1.334 and 1.937, width 0.945 and 0.921, 8 to 11 percent, closest at 1.68 | `constraint-gap\review\INDETERMINATES.md:40-60` |
| chapter 7 section 7.4 | heterogeneity 93 to 95 percent, Q 446 on 30, scale 0.063, band 0.005, ROPE 0.073, shrinkage 0.1746 to 0.0997 at 42.9 percent | `constraint-gap\review\INDETERMINATES.md:55-95` |
| chapter 7 section 7.4 | the redesign, grid 50 to N, ten folds, twenty repetitions, crossing size, the 800-row boundary declared in advance, seventeen at median 0.006 and p 0.964, store the folds | `constraint-gap\review\REDESIGN.md:1-110` |
| chapter 8 section 8.4 | real 1.038 [0.958, 1.118], rotated 1.019 [0.903, 1.353], smooth 2.804 withdrawn, second attempt 0.184 | `constraint-gap-measurements\notes\negative_control.md:1-50` |
| chapter 8 section 8.5 | variance inflation 251, SE inflation 15.84, J_eff 3.98, about 62 needed, 3 of 9 at full, 7 at half, 8 at a third | `constraint-gap\review\FINDINGS.md:1-35` |
| chapter 8 section 8.5 | 9/3/19 to 3/17/11, five negative analyses, 0.2 percent of floor, twelve times the band, learning-curve redesign | `constraint-gap\README.md:57-76`; `constraint-gap\review\REDESIGN.md` |
| chapter 8 section 8.5 | three-way inconsistency, lines 544, 548 to 556, 755 | `constraint-gap\review\FINDINGS.md:7-31` against `theory-radar\paper\theory_radar_v6_submission.tex` |
| chapter 8 section 8.9 | twenty-seven errors, four in checking tools | `constraint-gap-measurements\README.md:273-282` |

## failures and corrections

- `theory-radar/ERRATA.md:3-75` at 37c4e6c. ## 2026-09-03. The AUROC to F1 bound holds only for concave ROC curves **What was claimed.** Theorem "AUROC-F1 Bound" in `paper/astar_paper.tex`, the derivation in `src/symbolic_search/_auroc_proof.py`, and the pruning bounds in `run_astar_v2.py` and `src/symbolic_search/_heuristic_dag.py` all rested on the statement that any ROC curve with area A has maximum Youden index J = max(TPR − FPR) at most 2A − 1. **Why it is wrong.** The statement holds for concave ROC curves (equivalently, scores whose likelihood ratio is monotone), because a concave curve lies above the two chords through its Youden point and so has area at least (1 + J)/2. It fails for non-concave curves. Counterexample, found by an external reviewer of the companion textbook: rank three quarters of the positives above every negative and the remaining quarter below every negative. AUROC is 0.75, the maximum Youden index is 0.75, and at prevalence one half the best thresholded F1 is 0.857, above the 0.80 the AUROC form of the ceiling allows. The sound ceiling for that score, from J = 0.75, is 0.889, and the score sits under it. The `auroc_f1_bound` formula in `run_astar_v2.py`, 2Aπ/(Aπ + (1 − A)(1 − π)), is not a valid upper bound either: at prevalence 0.1 the same score reaches F1 0.857 against a "bound" of 0.5. **Consequence for reported results.** The searches that used these bounds to prune could have discarded a candidate formula whose ROC curve was not concave and whose true best F1 exceeded the computed ceiling. The formulas and wins reported by those runs are therefore what a pruned search found, and are lower bounds on what an unpruned search would find. The Monotone Invariance Theorem and the results that do not depend on the AUROC bound are unaffected. **Correction.** The sound form of the ceiling substitutes the measured maximum Youden index of the candidate's own scores for 2A − 1. It holds for every score, costs the same sort as AUROC, and is what `max_f1_for_youden` and `youden_f1_bound` now compute. The AUROC form is retained under its original names with a docstring stating the concavity condition, and the pruning sites now use the measured index. A rerun of the published searches under the corrected bound was done on 2026-09-03 and 2026-09-04, `rerun_youden_2026_09_03.py`, results in `results/rerun_youden_2026_09_03.json`, run on the Atlas workstation, CPU only. **Rerun, part A, the pre-filter admissibility table (`tab:auroc`).** Depth-2 pairwise enumeration on the eight datasets, exhaustive against the AUROC pre-filter at the seven published thresholds, with the sound Youden ceiling beside it. The evaluation counts under the pre-filter reproduce the published table (Breast Cancer 8700 pairs, 2576 evaluated at 0.75; Wine 1560, 413; Circles 20, 4; Moons 20, 2). The pre-filter lost no optimum on any dataset at any threshold, which is what the paper reported. That was luck of the data, not the theorem: the retracted ceiling sat below the F1 a pair formula actually reach
- `theory-radar/paper/REVISION_PLAN.md:39-45` at 37c4e6c. **Fix:** - Drop "σ significance" everywhere - Report: mean ΔF1, std, 95% CI, and corrected resampled t-statistic - Table columns: "Test F1", "GB F1", "ΔF1", "95% CI", "Direction" - Text: "the formula outperforms GB by ΔF1=0.031, 95% CI [0.028, 0.034]" - Add Nadeau-Bengio corrected t-test (accounts for CV fold correlation) - Keep effect size as supplementary but don't call it "σ"

## conditions

- The search enumerates short expressions over the features and scores each by its optimal thresholded F1, pruning monotone unary nodes by the Monotone Invariance Theorem and, in the A* companion, leaves by an F1 ceiling.
- Its first comparison reported nine wins that became three under the Nadeau and Bengio correction, with seventeen datasets indeterminate, and the record carries the retraction at the size of the result.
- The main comparison used a fold-local meta-learned pruning rule and never rested on the AUROC form of the ceiling. The A* companion did, and the rerun shows what that cost, nothing on those datasets.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/MonotoneInvariance.lean`, theorems `aurocNum_comp`, `auroc_comp`, `predicted_comp`, `predictedBelow_comp`, `sweptF1_comp`, `sweptF1Below_comp`, `optF1_comp`, at observation-data-mining 2b00d80.

`lean/DataMiningAsObservation/YoudenF1.lean`, theorems `f1_eq`, `f1_le_of_youden`, `auroc_eq`, `youden_eq`, `youden_exceeds_auroc_form`, at observation-data-mining 2b00d80.

## used in

*Data Mining as Observation* chapters 0, 5, 6, 7, 14.

## related

monotone-invariance, safe-pruning, youden-f1-bound, read-operator

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns e448a13, theory-radar 37c4e6c, observation-data-mining 2b00d80, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
