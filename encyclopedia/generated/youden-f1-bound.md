# Youden F1 bound

**id.** youden-f1-bound
**kind.** correction

## definition

none

## equation

Book equation 5.4.

    \begin{gathered} F_1^{\max}\ \le\ \sup_{t\in[J,\,1]}\ \frac{2t\pi}{t\pi+\pi+(t-J)(1-\pi)},\qquad J=\max_{\tau}\big(\mathrm{TPR}-\mathrm{FPR}\big),\qquad \pi=\text{prevalence}, \\ J\le 2A-1\ \text{when the ROC curve is concave, and not in general.} \end{gathered}

## ledger

none

## first stated

The AUROC form, theorem "AUROC-F1 Bound" in `theory-radar/paper/astar_paper.tex` and the derivation in `theory-radar/src/symbolic_search/_auroc_proof.py`, repository DOI 10.5281/zenodo.20660206. The corrected form at theory-radar 1b3d105.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 5 section 5.4 | Monotone Invariance and AUROC invariance theorems, the AUROC to F1 bound via the Youden index, stated in the source for every ROC curve and corrected in the book to concave curves, with the counterexample at AUROC 0.75 and F1 0.857 | `theory-radar\paper\astar_paper.tex:94-170`; `theory-radar\paper\theory_radar_paper.tex:290-304` |
| chapter 5 section 5.4 | seven thresholds up to 0.75, eight datasets, 56 conditions, zero admissibility violations, reductions 70 to 99.1 percent | `theory-radar\paper\astar_paper.tex:170-200` |
| chapter 5 section 5.4 | the rerun of 2026-09-03 and 2026-09-04, pre-filter counts 2576 of 8700 and 413 of 1560, ceiling violations 812 and 412, Youden pruning 199 and 38, A* optima 0.958 and 0.694 in strict and fast modes, Youden mode short by 0.006 and 0.002 | `theory-radar\results\rerun_youden_2026_09_03.json`; `theory-radar\ERRATA.md` |
| chapter 6 section 6.3 | Monotone Invariance Theorem and its proof | `theory-radar\paper\theory_radar_paper.tex:290-304`; `theory-radar\paper\astar_paper.tex:94-110` |

Rerun of the A* paper's pruning tables by `theory-radar/rerun_youden_2026_09_03.py`. Part A is depth-2 pairwise enumeration on eight datasets, exhaustive against the AUROC pre-filter at seven thresholds and against Youden pruning. Part B is the depth-3 A* search with 50,000 expansions in strict mode (no pre-filter), the published fast mode (AUROC pre-filter at 0.52), and the youden mode.

Part A, recorded at commit aedc053 of theory-radar.
| Dataset, depth 2 pairs | Pairs | Exhaustive F1 | AUROC pre-filter at 0.75, evaluated, admissible | Youden pruning, evaluated, admissible | Pairs whose F1 exceeds the AUROC ceiling |
|---|---|---|---|---|---|
| Circles (2) | 20 | 0.9960 | 4, yes | 7, yes | 14 |
| Moons (2) | 20 | 0.8330 | 2, yes | 2, yes | 3 |
| Breast Cancer (30) | 8700 | 0.9542 | 2576, yes | 199, yes | 812 |
| Wine (13), class 0 vs rest | 1560 | 0.9204 | 413, yes | 38, yes | 412 |
| Synthetic (10) | 900 | 0.9556 | 10, yes | 7, yes | 18 |
| Synthetic (20) | 3800 | 0.9460 | 8, yes | 8, yes | 57 |
| Synthetic (30) | 8700 | 0.9637 | 8, yes | 8, yes | 61 |
| Synthetic (40) | 15600 | 0.9425 | 32, yes | 8, yes | 125 |

Part B.
| Dataset | strict F1 and formula | fast F1 | youden F1 and formula | expansions strict, fast, youden |
|---|---|---|---|---|
| Circles (2) | 0.9965, (x1 hypot x2) | 0.9965 | 0.9965, (x1 hypot x2) | 1626, 540, 87 |
| Moons (2) | 0.8927, (neg(x1) max x2) | 0.8927 | 0.8927, (neg(x1) max x2) | 1626, 1386, 86 |
| Synthetic (20) | 1.0000, (x0 hypot x1) | 1.0000 | 1.0000, (x0 hypot x1) | 50000, 50000, 465 |
| Breast Cancer (10) | 0.9578, ((f1 min f2) + f7) | 0.9578 | 0.9516, ((f3 + f7) min f6) | 50000, 50000, 841 |
| Diabetes (8) | 0.6937, ((d5 min d7) + d1) | 0.6937 | 0.6921, ((d1 + d7) min d5) | 50000, 46307, 192 |

## failures and corrections

- `theory-radar/ERRATA.md:3-75` at 37c4e6c. ## 2026-09-03. The AUROC to F1 bound holds only for concave ROC curves **What was claimed.** Theorem "AUROC-F1 Bound" in `paper/astar_paper.tex`, the derivation in `src/symbolic_search/_auroc_proof.py`, and the pruning bounds in `run_astar_v2.py` and `src/symbolic_search/_heuristic_dag.py` all rested on the statement that any ROC curve with area A has maximum Youden index J = max(TPR − FPR) at most 2A − 1. **Why it is wrong.** The statement holds for concave ROC curves (equivalently, scores whose likelihood ratio is monotone), because a concave curve lies above the two chords through its Youden point and so has area at least (1 + J)/2. It fails for non-concave curves. Counterexample, found by an external reviewer of the companion textbook: rank three quarters of the positives above every negative and the remaining quarter below every negative. AUROC is 0.75, the maximum Youden index is 0.75, and at prevalence one half the best thresholded F1 is 0.857, above the 0.80 the AUROC form of the ceiling allows. The sound ceiling for that score, from J = 0.75, is 0.889, and the score sits under it. The `auroc_f1_bound` formula in `run_astar_v2.py`, 2Aπ/(Aπ + (1 − A)(1 − π)), is not a valid upper bound either: at prevalence 0.1 the same score reaches F1 0.857 against a "bound" of 0.5. **Consequence for reported results.** The searches that used these bounds to prune could have discarded a candidate formula whose ROC curve was not concave and whose true best F1 exceeded the computed ceiling. The formulas and wins reported by those runs are therefore what a pruned search found, and are lower bounds on what an unpruned search would find. The Monotone Invariance Theorem and the results that do not depend on the AUROC bound are unaffected. **Correction.** The sound form of the ceiling substitutes the measured maximum Youden index of the candidate's own scores for 2A − 1. It holds for every score, costs the same sort as AUROC, and is what `max_f1_for_youden` and `youden_f1_bound` now compute. The AUROC form is retained under its original names with a docstring stating the concavity condition, and the pruning sites now use the measured index. A rerun of the published searches under the corrected bound was done on 2026-09-03 and 2026-09-04, `rerun_youden_2026_09_03.py`, results in `results/rerun_youden_2026_09_03.json`, run on the Atlas workstation, CPU only. **Rerun, part A, the pre-filter admissibility table (`tab:auroc`).** Depth-2 pairwise enumeration on the eight datasets, exhaustive against the AUROC pre-filter at the seven published thresholds, with the sound Youden ceiling beside it. The evaluation counts under the pre-filter reproduce the published table (Breast Cancer 8700 pairs, 2576 evaluated at 0.75; Wine 1560, 413; Circles 20, 4; Moons 20, 2). The pre-filter lost no optimum on any dataset at any threshold, which is what the paper reported. That was luck of the data, not the theorem: the retracted ceiling sat below the F1 a pair formula actually reach

## conditions

- The Youden form holds for every score with a finite sample.
- The AUROC form holds for concave ROC curves, and as a pruning bound it is safe only there.
- Inside a tree search either form bounds the formula itself and not its descendants, so pruning a subtree by its root's ceiling is a heuristic in both cases.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/YoudenF1.lean`, theorems `f1_eq`, `f1_le_of_youden`, `auroc_eq`, `youden_eq`, `youden_exceeds_auroc_form`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 5.

## related

monotone-invariance, formula-search, safe-pruning, apriori

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
