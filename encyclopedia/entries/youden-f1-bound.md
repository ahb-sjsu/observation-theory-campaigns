# Youden F1 bound

**id.** youden-f1-bound
**kind.** correction

## definition

The best thresholded F1 a score can reach is bounded by its Youden index, the largest
difference between true-positive and false-positive rates over all thresholds and both
threshold directions. The bound holds for every score. The form that replaces the Youden
index by two times AUROC minus one holds only when the ROC curve is concave, which is the
case when the score's likelihood ratio is monotone, and it is false in general. This entry is
a correction because the theory-radar paper and code had asserted the AUROC form for every
ROC curve.

## equation

    F1_max ≤ sup_{t ∈ [J, 1]}  2tπ / ( tπ + π + (t − J)(1 − π) ),   J = max_τ (TPR − FPR),

with π the prevalence. The step from J to the ceiling is that at any threshold
FPR ≥ TPR − J. The step from AUROC to J, J ≤ 2A − 1, needs concavity, because a concave curve
lies above the two chords through its Youden point and so has area at least (1 + J)/2. Book
equation 5.4.

## ledger

none. The result is a theorem with a stated condition, not a measured claim, and its status
is carried by the erratum below and by the machine-checked Monotone Invariance Theorem it sits
beside.

## first stated

The AUROC form, theorem "AUROC-F1 Bound", `theory-radar/paper/astar_paper.tex`, and the
derivation in `theory-radar/src/symbolic_search/_auroc_proof.py`, repository DOI
10.5281/zenodo.20660206. The corrected form, with the concavity hypothesis and the remark
recording the correction, at theory-radar 1b3d105.

## measurements

The counterexample, from the external review of *Data Mining as Observation* on 2026-09-03.
Rank three quarters of the positives above every negative and the remaining quarter below
every negative. AUROC is 0.75, the Youden index is 0.75, and at prevalence one half the best
thresholded F1 is 0.857, above the 0.80 the AUROC form allows. The sound ceiling with J = 0.75
is 0.889.

Rerun of the theory-radar A* paper's pruning tables under the corrected bound, 2026-09-03,
`theory-radar/rerun_youden_2026_09_03.py`, results in `theory-radar/results/rerun_youden_2026_09_03.json`.

| Dataset, depth 2 pairs | Pairs | Exhaustive F1 | AUROC pre-filter at 0.75, evaluated, admissible | Youden pruning, evaluated, admissible | Pairs whose F1 exceeds the AUROC ceiling |
|---|---|---|---|---|---|
| Circles (2) | 20 | 0.9960 | 4, yes | 7, yes | 14 |
| Moons (2) | 20 | 0.8330 | 2, yes | 2, yes | 3 |
| Breast Cancer (30) | 8700 | 0.9542 | 2576, yes | 199, yes | 812 |
| Wine (13), class 0 against the rest | 1560 | 0.9204 | 413, yes | 38, yes | 412 |
| Synthetic (10) | 900 | 0.9556 | 10, yes | 7, yes | 18 |
| Synthetic (20) | 3800 | 0.9460 | 8, yes | 8, yes | 57 |

The evaluation counts under the AUROC pre-filter reproduce the published table. The last
column is the number of formulas on which the retracted theorem's ceiling sat below the F1
the formula actually reached, which is the number of times the theorem was wrong on that
dataset. The pre-filter lost no optimum on these datasets because the winning formulas had
concave enough ROC curves, not because the theorem held. The A* search at depth 3 in strict,
fast, and youden modes is part B of the same rerun and is recorded in the results file.

## failures and corrections

- 2026-09-03. Theorem stated without the concavity hypothesis in the A* paper, the proof
  module, and the pruning bounds of two runners. Found by the external reviewer of the
  companion textbook. Corrected in theory-radar 1b3d105 with `ERRATA.md`, the paper restated
  with the hypothesis, and the pruning sites moved to the measured Youden index. A one
  direction Youden index in the first correction was itself corrected at aedc053, since the
  F1 sweep it bounds thresholds in either direction.
- The `auroc_f1_bound` formula of `run_astar_v2.py`, 2Aπ/(Aπ + (1 − A)(1 − π)), was not a
  valid bound either. At prevalence 0.1 the counterexample score reaches F1 0.857 against a
  claimed ceiling of 0.5. Retired at 1b3d105 and now raises if called.
- The main theory-radar comparison, the thirty-one-dataset table, did not use the bound. Its
  pipeline prunes with a fold-local meta-learned rule validated with zero false negatives.
  The bound entered the record through the A* companion paper only.

## conditions

- The Youden form holds for every score with a finite sample.
- The AUROC form holds for concave ROC curves, and as a pruning bound it is safe only there.
- As a pruning rule inside a tree search, either form bounds the formula itself and not its
  descendants, so pruning a subtree by its root's ceiling is a heuristic in both cases. The
  correction makes the leaf test sound, not the subtree test.

## machine checked

none for the bound itself. The Monotone Invariance Theorem beside it, that a strictly
monotone transform leaves AUROC and optimal thresholded F1 unchanged, is checked in
`observation-data-mining/lean/DataMiningAsObservation/MonotoneInvariance.lean`.

## used in

- theory-radar, the A* companion paper and the search modes `fast` and `youden`.
- *Data Mining as Observation* chapter 5 section 5.4, which prints the counterexample, and the
  answer key for chapter 5.

## related

monotone-invariance, formula-search, safe-pruning, apriori

## status

Hand-filled 2026-09-03 from theory-radar at aedc053 and observation-data-mining at a0b20ff,
with part B of the rerun pending at the time of writing. Not yet generated.
