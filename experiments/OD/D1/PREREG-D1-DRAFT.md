# PREREG D1 (DRAFT, NOT SEALED): identifiability at a budget, finite-sample form

Status: draft. Nothing here is a registered claim until Section 8 is executed. Gate D1 of the
OD track (`experiments/DISCOVERY-TRACK.md`). Second design; the first is recorded in Section 7.

## 1. Claim under test

Theorem 2 of `geometric-evaluation-theory/articles/2026-09-09-identifiability-at-a-budget.md`,
machine-checked as gate D0 (`geometric-evaluation-theory/lean/GET/Identifiability.lean`, commit
9604c44): a perturbation of size rho along a direction v is distinguishable at budget B exactly
when v^T P v > B^2 / rho^2, so the number of identifiable eigen-directions is
d_obs(B, rho) = #{i : lambda_i > B^2 / rho^2}, antitone in B. The theorem is a statement about
one direction at a time, and the gate measures its two finite-sample consequences:

(A) Single-parameter probes. An experimenter who perturbs one coordinate at a time, in a basis
that is not the eigenbasis, learns exactly which coordinates are identifiable at (B, rho), a
bracket on each diagonal entry from a ladder of sizes, and nothing about off-diagonal entries.
This is the identifiability setting of inverse problems, one parameter at a time.

(B) Mixed probes. An experimenter who perturbs in random directions on the sphere of radius rho
learns the whole operator, every eigenvalue above and below the threshold, whenever the sphere
crosses the ellipsoid {delta : delta^T P delta = B^2}, that is when
lambda_min rho^2 < B^2 < lambda_max rho^2 with lambda_min the smallest eigenvalue including
zero (with a kernel the ellipsoid is a cylinder the sphere always meets), and learns nothing
when it does not, because the oracle is then constant. Recovery in finite samples needs the
crossing to be substantial: the gate calls a cell well-crossed when the median evaluator sees
both oracle answers in at least a tenth of its queries, and grades full recovery there only. The budget hides small eigenvalues from single-direction probes and
not from mixed ones.

## 2. World

Read operators of declared spectrum in a random orthonormal frame, three worlds: n = 5 with
spectrum (4, 2, 0.5, 0.1, 0) and a kernel; n = 8 with (8, 4, 2, 1, 0.25, 0.05, 0, 0), two kernel
directions; n = 8 at full rank (8, 4, 2, 1, 0.5, 0.25, 0.1, 0.05). rho = 1. Budget ladder
B in 0.25, 0.5, 1, 1.5, 2 (thresholds 0.0625, 0.25, 1, 2.25, 4). The oracle answers whether
delta^T P delta exceeds B^2 and nothing else.

World A: the probe basis is the coordinate basis of the random frame's ambient space, so the
diagonal entries P_ii are generic mixtures of the eigenvalues; probes at sizes 0.125, 0.25, 0.5,
1 along each coordinate and its negative. World B: perturbations of size rho in uniformly
random directions, on a ladder of 60, 120, 240, 480, 960 queries per evaluator. 20 evaluators
per cell, each with its own frame and queries. A World B evaluator whose oracle is constant is
recorded as such and not graded; the crossing test says when that must happen.

## 3. Estimators

World A: no estimator. The verdict for coordinate i at (B, rho) is the oracle's answer to the
probe of size rho along e_i; the bracket on P_ii is [B^2 / r_hi^2, B^2 / r_lo^2] with r_lo the
largest size found indistinguishable and r_hi the smallest found distinguishable. Both follow
from Theorem 2 read along e_i, and the gate checks them against the truth exactly.

World B: the analytic centre of the set of positive semidefinite operators consistent with the
answers, the maximiser of the summed log slacks (q_j / B^2 - 1 for a distinguishable query,
1 - q_j / B^2 otherwise), inside the declared cap P <= 1000 (B^2 / rho^2) I, which keeps the set
bounded in a direction the answers bound only from below; a convex program solved by cvxpy
1.9.2 with Clarabel, SCS as fallback. It is a canonical point of the feasible set, which
shrinks to the truth as queries accumulate near the boundary. Nothing about the true operator
enters; the cap is a declared prior on the eigenvalue range, inactive in every world here.

## 4. Errors and chance

World A: the fraction of evaluators in which every coordinate's verdict matches the theorem's
inequality, and in which every diagonal entry lies in its bracket. World B: along each true
eigenvector the estimated form against the eigenvalue, relative to max(lambda_i, threshold),
split above and below the threshold; the Frobenius relative error of the operator; the
top-subspace angle. Chance per evaluator: the same quantities for the true spectrum in a random
frame, median over 64 draws.

## 5. Bars (REC FIXED FROM THE PILOT before sealing; Section 7)

- A1, single-parameter probes. In every world and budget, every evaluator's verdicts and
  brackets are exact (fraction 1.0). This is Theorem 2 read along a coordinate and is expected
  to be exact; a single failure is a counterexample to the theorem or a defect in the oracle.
- B1, full recovery under crossing. In every well-crossed World B cell, at the largest query
  count, the median Frobenius relative error is at most REC times its
  chance median, and the same for the medians of the above-threshold and the below-threshold
  eigenvalue errors separately, so that the below-threshold eigenvalues are shown to be
  recovered by mixed probes.
- B2, no crossing, no recovery. In every World B cell whose interval excludes B^2, the oracle
  is constant for every evaluator.
- B3, monotone. The median Frobenius error is non-increasing over the query ladder (5 percent
  for ties).

Pass: A1, B1, B2, B3 hold in every cell. Fail: any World A verdict mismatch in more than half
the evaluators of a cell (the theorem's inequality is wrong), or a crossing cell whose median
Frobenius error exceeds half its chance at the largest query count (mixed probes do not reveal
the operator), or a non-crossing cell with a non-constant oracle. Otherwise INDETERMINATE.

## 6. What falsifies

A coordinate reported identifiable whose diagonal entry is below the threshold, or the reverse;
an operator that mixed probes at radius rho cannot recover although the sphere crosses its
ellipsoid; below-threshold eigenvalues left at chance by mixed probes; a non-constant oracle
where the crossing condition fails.

## 7. Self-test, first pilot, second pilot

Self-test (Atlas 2026-09-09, `--selftest`): World A verdicts and brackets exact at B = 0.5 and
1; World B under crossing at B = 1 and 1.5, Frobenius errors 0.050 and 0.072 with 800 queries,
below-threshold eigenvalues at 0.00 to 0.10 relative error; at B = 0.5, where B^2 = 0.25 sits
low against the typical form on the sphere so few queries land near the boundary, 0.287;
at B = 2.5 the oracle is constant as the crossing test says.

First pilot (`pilot_v1.json`, 75 cells, 2026-09-09 06:51 to 06:56 UTC). The first design read
Theorem 2 as an operator statement and predicted that mixed probes recover only the
above-threshold directions. The pilot refuted that reading before any seal: at B from 1 to 2
the max-margin estimator recovered the count exactly and the above-threshold eigenvalues to a
few percent, and it recovered the below-threshold eigenvalues to 3 to 10 percent of chance as
well. The geometry explains it, the sphere of radius rho traces the whole ellipsoid where it
crosses it. The same pilot showed the max-margin estimator degenerate where the feasible set
was wide (n = 8 at B = 0.25 and 0.5, errors at or beyond chance, kernel directions pushed above
the threshold), and a minimal-trace estimator tried next biased every eigenvalue down; the
analytic centre replaced both. The two-world design of this document followed. Nothing from
the first pilot fixes a bar here.

Second pilot, first launch (2026-09-09 07:03 UTC, stopped after four cells): World A exact in
all 20 evaluators at n = 5, B = 0.25; World B at n = 5, B = 0.25 was non-constant in 6 to 11 of
20 evaluators although the crossing test said no crossing, because the test used the smallest
positive eigenvalue and the world has a kernel, and the few kernel-side answers left the
analytic centre nearly unbounded (errors in the thousands). Corrected before continuing: the
crossing test counts the kernel, the estimator carries the declared cap, and full recovery is
graded in well-crossed cells only.

Second pilot (`pilot.json`): every cell of Section 2. REC is fixed as the largest ratio of a
graded median (Frobenius, above, below) to its chance median over the crossing cells at the
largest query count, rounded up to two decimals, and at most 0.5; if any crossing cell exceeds
0.5, that cell's budget is recorded as too far from the sphere's typical form for the query
ladder and the cell is excluded from B1 by name before sealing. Recorded here with the values.

## 8. Sealing procedure

1. D0 checked with no `sorry`. Done.
2. Second pilot on Atlas; fix REC and any named exclusions; commit `pilot.json`.
3. Rename this file to `PREREG-D1.md`, commit, record its blob hash in the track document and
   the README status ledger.
4. Run on the run seed, grade with `d1_grade.py --rec REC`, commit `results.json` and
   `grade.json` as executed, enter the registry tests in `claims/transformations/OD.toml`.
