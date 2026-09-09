# PREREG D1: identifiability at a budget, finite-sample form

Status: SEALED 2026-09-09 by the rename to `PREREG-D1.md`; blob hash recorded in
`experiments/DISCOVERY-TRACK.md` and the README status ledger. Gate D1 of the OD track. Second
design; the first is recorded in Section 7.

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
learns the whole operator, every eigenvalue above and below the threshold, up to the pencil
P(s) = s P + (1 - s) c I with c = B^2 / rho^2 (article Proposition 2: every member of the pencil
answers every query at that radius as P does, and when c is strictly inside the spectrum and not
an eigenvalue nothing else does), whenever the sphere crosses the ellipsoid
{delta : delta^T P delta = B^2}, that is when lambda_min rho^2 < B^2 < lambda_max rho^2 with
lambda_min the smallest eigenvalue including zero (with a kernel the ellipsoid is a cylinder the
sphere always meets), and learns nothing when it does not, because the oracle is then constant.
The registered estimator returns the end of the pencil (article Corollary 4): P itself when P
has a kernel, and when P is positive definite the member P* = s* P + (1 - s*) c I with
s* = c / (c - lambda_min), whose smallest eigenvalue is zero, so in that world the estimate is
predicted to sit nearer P* than P. Recovery in finite samples needs the crossing to be
substantial: the gate calls a cell well-crossed when the median evaluator sees both oracle
answers in at least a tenth of its queries, and grades recovery there only. The budget hides
small eigenvalues from single-direction probes and not from mixed ones.

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
enters; the cap is a declared prior on the eigenvalue range, above every eigenvalue of every
world here; it can bind the analytic centre of a poorly crossed cell, which is one reason such
cells are not graded. Along the pencil the objective is increasing in s, so the centre returns
the pencil's end, and the record carries the estimate's error against that end beside its error
against P.

## 4. Errors and chance

World A: the fraction of evaluators in which every coordinate's verdict matches the theorem's
inequality, and in which every diagonal entry lies in its bracket. World B: along each true
eigenvector the estimated form against the eigenvalue, relative to max(lambda_i, threshold),
split above and below the threshold; the Frobenius relative error of the operator; the same
Frobenius error against the pencil's end P*; the top-subspace angle. Chance per evaluator: the same quantities for the true spectrum in a random
frame, median over 64 draws.

## 5. Bars (REC = 0.30, fixed from the second pilot; Section 7)

- A1, single-parameter probes. In every world and budget, every evaluator's verdicts and
  brackets are exact (fraction 1.0). This is Theorem 2 read along a coordinate and is expected
  to be exact; a single failure is a counterexample to the theorem or a defect in the oracle.
- B1, full recovery under crossing. In every well-crossed World B cell, at the largest query
  count, the median Frobenius relative error is at most REC times its
  chance median, and the same for the medians of the above-threshold and the below-threshold
  eigenvalue errors separately, so that the below-threshold eigenvalues are shown to be
  recovered by mixed probes.
- B2, no crossing, no recovery. In every World B cell whose interval excludes B^2, the oracle
  is constant for every evaluator. The bar binds in one direction: a constant oracle in a cell
  whose interval contains B^2 is a thin crossing, recorded and not failed.
- B3, monotone. In every well-crossed cell the median Frobenius error is non-increasing over
  the query ladder (5 percent for ties).
- B4, the pencil's end. In every well-crossed cell of the positive definite world, at the
  largest query count, the median Frobenius error against P* is at most the median error against
  P.

Pass: A1, B1, B2, B3, B4 hold in every cell they bind. Fail: any World A verdict mismatch in
more than half the evaluators of a cell (the theorem's inequality is wrong), or a well-crossed
cell whose median Frobenius error exceeds half its chance at the largest query count (mixed
probes do not reveal the operator), or a non-crossing cell with a non-constant oracle. Otherwise
INDETERMINATE, which includes a B4 miss, since the pencil bias is a few percent of P in the
graded cells and can sit under the finite-sample error at this ladder.

## 6. What falsifies

A coordinate reported identifiable whose diagonal entry is below the threshold, or the reverse;
an operator that mixed probes at radius rho cannot recover, up to the pencil, although the
sphere crosses its ellipsoid substantially; below-threshold eigenvalues left at chance by mixed
probes; a non-constant oracle where the crossing condition fails; in the positive definite world
an analytic centre nearer P than the pencil's end.

## 7. Self-test, pilots, pencil probe

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

Second pilot, first launch (`pilot_v2a.json`, 2026-09-09 07:03 UTC, stopped after four cells): World A exact in
all 20 evaluators at n = 5, B = 0.25; World B at n = 5, B = 0.25 was non-constant in 6 to 11 of
20 evaluators although the crossing test said no crossing, because the test used the smallest
positive eigenvalue and the world has a kernel, and the few kernel-side answers left the
analytic centre nearly unbounded (errors in the thousands). Corrected before continuing: the
crossing test counts the kernel, the estimator carries the declared cap, and full recovery is
graded in well-crossed cells only.

Second pilot (`pilot_v2.json`, `pilot_v2.log`, seed 20260913, 90 cells, Atlas 2026-09-09 07:10 to
07:27 UTC, code as committed at d6e84ce): every cell of Section 2. REC was declared before this
pilot as the largest ratio of a graded median (Frobenius, above, below) to its chance median over
the well-crossed cells at the largest query count, rounded up to two decimals, and at most 0.5,
with any well-crossed cell above 0.5 excluded from B1 by name. World A: verdicts and brackets
exact in every evaluator of all fifteen cells. World B at 960 queries: the well-crossed cells
(median answer balance 0.14 to 0.42) are B = 1 and B = 1.5 in all three worlds; there the
Frobenius medians are 0.055 to 0.225 of chance, the above-threshold medians 0.042 to 0.299 of
chance and the below-threshold medians 0.018 to 0.159 of chance, the largest ratio 0.299 at
n = 8 full rank, B = 1, above threshold, so REC = 0.30 and no cell is excluded; the Frobenius
median falls monotonically along the query ladder in each of the six. Poorly crossed cells,
median answer balance 0.00 to 0.07: B = 0.25 and 0.5 in every world, where B^2 sits low against
the typical form on the sphere so nearly every answer is "distinguishable", and B = 2 at n = 8,
where nearly every answer is "indistinguishable"; there the analytic centre ranges from 0.22 to
48 times chance, reported and not graded, as the rule declared before this pilot says. Constant
oracle in all 20 evaluators: n = 5 at B = 2, where B^2 = 4 = lambda_max rho^2 and the theory
predicts it, and n = 8 full rank at B = 0.25, where the interval contains B^2 (lambda_min = 0.05
below 0.0625) but the crossing is so thin that 960 random directions in each of 20 evaluators all
answered "distinguishable": the crossing condition is necessary for a non-constant oracle and not
sufficient in finite samples, and B2 is stated in the one direction that is a theorem.

Pencil probe (`d1_pencil_probe.py`, `pencil_probe.json`, Atlas 2026-09-09, seed 7, four
evaluators and 2000 queries per cell, B = 1 and 1.5 in the three worlds, queries at one radius,
at radii 1 and 1.5, and at radii 1 and 0.7). Written after the second pilot to test what the
pilot's small full-rank errors hid: answers at one radius identify P only up to the pencil, and
the analytic centre should return the pencil's end. In the two worlds with a kernel the end is P
and the errors against P and P* coincide (0.014 to 0.119). In the positive definite world the
estimate is nearer P* than P in all six cells (against P 0.039 to 0.163, against P* 0.026 to
0.123; s* = 1.053 at B = 1 and 1.023 at B = 1.5). Two radii did not visibly improve on one at
2000 queries, the pencil bias being under the finite-sample error there, so the design keeps one
radius and registers the pencil as B4 rather than adding a second radius. Article Proposition 2
and Corollary 4 were written from this probe.

Third pilot (`pilot.json`, `pilot.log`, seed 20260913, 90 cells, Atlas 2026-09-09 07:57 to 08:14
UTC, the code of this commit): the second pilot rerun on the final workload, whose changes are
record-only (the theoretical crossing on skipped rows, the estimate's eigen-forms, its error
against the pencil's end). Every field the second pilot had reproduces exactly, graded medians
and chance medians alike, so REC = 0.30 stands on the second pilot as declared. The new fields:
in the positive definite world at 960 queries the estimate is nearer P* than P in 20 of 20
evaluators at B = 1 (Frobenius median 0.256 against P, 0.214 against P*, s* = 1.053) and in 20
of 20 at B = 1.5 (0.125 against 0.111, s* = 1.023), so B4 is registered as a graded bar. The
median estimated eigen-forms along the true eigenvectors at B = 1 are 10.09, 4.72, 2.23, 0.97,
0.30, 0.02, 0.01, 0.01 against the pencil's end 8.37, 4.16, 2.05, 1.00, 0.47, 0.21, 0.05, 0.00
and the truth 8, 4, 2, 1, 0.5, 0.25, 0.1, 0.05: the finite-sample centre overshoots the end on
the three smallest eigenvalues, which is the direction the objective pushes, and B4 compares
whole operators, not eigenvalues. In the two worlds with a kernel P* = P and the two errors
coincide by construction. A1 exact in every evaluator of every World A cell, as before.

## 8. Sealing procedure

1. D0 checked with no `sorry`. Done.
2. Second pilot on Atlas; REC fixed at 0.30, no exclusions; pencil probe; third pilot on the
   final code reproducing the second; `pilot.json`, `pilot_v2a.json`, `pencil_probe.json`
   committed. Done.
3. Rename this file to `PREREG-D1.md`, commit, record its blob hash in the track document and
   the README status ledger. Done by this commit.
4. Run on the run seed, grade with `d1_grade.py --rec 0.30`, commit `results.json` and
   `grade.json` as executed, enter the registry tests in `claims/transformations/OD.toml`.
