# PREREG D1 (DRAFT, NOT SEALED): identifiability at a budget, finite-sample form

Status: draft. Nothing here is a registered claim until Section 8 is executed. Gate D1 of the
OD track (`experiments/DISCOVERY-TRACK.md`).

## 1. Claim under test

Theorem 2 of `geometric-evaluation-theory/articles/2026-09-09-identifiability-at-a-budget.md`,
machine-checked in `geometric-evaluation-theory/lean/GET/Identifiability.lean` (gate D0): at
budget B a direction v is identifiable for perturbations of size rho exactly when
v^T P v > B^2 / rho^2, the kernel of P is identifiable at no budget, and the number of
identifiable eigen-directions d_obs(B, rho) = #{i : lambda_i > B^2 / rho^2} is non-increasing
in B. The finite-sample form measured here: an estimator that sees only the distinguishability
oracle at budget B recovers exactly the directions the theorem calls identifiable, and nothing
else, with error falling as the number of queries grows.

## 2. World

Synthetic read operators P of declared spectrum in a random orthonormal frame, three worlds:
n = 5 with spectrum (4, 2, 0.5, 0.1, 0) straddling every threshold of the ladder with a
kernel; n = 8 with spectrum (8, 4, 2, 1, 0.25, 0.05, 0, 0), two kernel directions; n = 8 at
full rank (8, 4, 2, 1, 0.5, 0.25, 0.1, 0.05). Perturbation size rho = 1. Budget ladder
B in 0.25, 0.5, 1, 1.5, 2, so thresholds B^2 / rho^2 of 0.0625, 0.25, 1, 2.25, 4 and predicted
d_obs of (4, 3, 2, 1, 1), (6, 5, 4, 2, 1), (8, 6, 4, 2, 1) for the three worlds. Queries are
perturbations of size rho in uniformly random directions, on a ladder of 30, 60, 120, 240,
480 per evaluator; the oracle answers whether delta^T P delta exceeds B^2 and nothing else.
20 evaluators per cell (world, B, query count), each with its own frame and queries. Pilot and
run seeds in `prereg_config.json`. A cell whose oracle is constant over an evaluator's queries
(every query distinguishable or none) skips that evaluator and records why.

## 3. Estimator

The max-margin semidefinite program on the oracle answers: maximise t over P_hat positive
semidefinite subject to delta^T P_hat delta >= B^2 (1 + t) for distinguishable queries and
<= B^2 (1 - t) for indistinguishable ones, t <= 1. The scale is fixed by B^2. cvxpy 1.9.2 with
Clarabel, SCS as fallback. Nothing about the true operator enters the estimator.

## 4. Errors and chance

Along each true eigenvector v_i the estimated form v_i^T P_hat v_i is compared to lambda_i,
relative to max(lambda_i, threshold). A direction is recovered when its relative error is at
most the recovery tolerance 0.25. The estimated count d_est is the number of eigenvalues of
P_hat above the threshold by more than the tolerance. The top-subspace angle is the largest
principal angle between the true above-threshold eigenspace and P_hat's top d_obs
eigenspace. Chance per evaluator: the same quantities for an operator with the true spectrum
in a random frame, median over 64 draws.

## 5. Bars (factors FIXED FROM THE PILOT before sealing; Section 7)

Per cell, over its graded evaluators:
- P1, the count. d_est = d_obs for at least FRAC of evaluators at the largest query count,
  and the fraction is non-decreasing over the query ladder (one inversion of at most 5 points
  allowed).
- P2, the identifiable directions. Median relative error of above-threshold directions at
  the largest query count at most REC times its chance median, and the median top-subspace
  angle at most REC times its chance median.
- P3, the unrevealed directions. Median relative error of below-threshold directions at
  least UNREV times its chance median, and no evaluator estimates a below-threshold direction
  above the threshold by more than the tolerance in more than 10 percent of evaluators.
- P4, the kernel. No evaluator estimates a kernel direction above the threshold by more than
  the tolerance in more than 10 percent of evaluators.
- P5, monotone. The median above-threshold error is non-increasing over the query ladder.

Pass: P1 to P5 in every cell. Fail: a cell at the largest query count in which the count
matches for fewer than half the evaluators (the count law is wrong), or in which more than 30
percent of evaluators push a below-threshold or kernel direction above the threshold (the
unrevealed claim is wrong). Otherwise INDETERMINATE.

## 6. What falsifies

An estimator that recovers directions below the threshold from oracle answers alone, or a
recovered count that departs from d_obs at large query counts, or failure to recover
above-threshold directions at the largest battery.

## 7. Self-test and pilot

Self-test, Atlas 2026-09-09: SELFTEST PASS on the n = 5 world at B = 0.5, 1, 1.5 with 600
queries: d_est = d_obs = 3, 2, 1; above-threshold relative errors at most 0.13; below-threshold
and kernel estimates at 0.03 to 0.89 of the threshold and never above it; top-subspace angles
2.7, 1.9, 1.0 degrees.

Pilot: every cell on the pilot seed. FRAC is fixed as the smallest count-match fraction at the
largest query count over cells, rounded down to one decimal and at least 0.8; REC as the
largest ratio of a recovered-direction median to its chance median at the largest query
count, rounded up to two decimals and at most 0.5; UNREV = 0.5. Recorded here.

## 8. Sealing procedure

1. D0 checked with no `sorry` (the theorem the gate tests is machine-checked first).
2. Pilot on Atlas; fix FRAC and REC; commit `pilot.json`.
3. Rename this file to `PREREG-D1.md`, commit, record its blob hash in the track document and
   the README status ledger.
4. Run on the run seed, grade with `d1_grade.py`, commit `results.json` and `grade.json` as
   executed, enter the registry test in `claims/transformations/OD.toml`.
