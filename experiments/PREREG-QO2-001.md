# Preregistration QO2-001: the flip on fresh scenarios

**Status:** draft, unsealed. No run governed by this document has been
executed. Sealing is the project owner's action; the sealing commit and
blob hash go to `experiments/SEALS.md`, after which no field below may
change.

**Registration ID:** PREREG-QO2-001 (assigned at seal)

## Claim

In the declared model class, at every declared coupling point, at the
budget where the fidelity-optimal encoder subset excludes the flux site,
the task-optimized arm achieves strictly lower held-out task distortion
and strictly higher held-out infidelity than the fidelity-optimized arm,
with margins of at least 0.01 on both axes. This is the flip. The claim is
refutable at each coupling point independently.

## Scope

Model class: 8-qubit open-chain Ising H = -J sum ZZ - h sum X, thermal
reference at beta = 0.5, outside region = sites 4..7, flux site = reduced
index 0 (chain site 4), strong site = reduced index 2 (chain site 6).
Coupling points: (J, h) in {(1.0, 2.0), (0.8, 1.8), (1.2, 2.2)}. The
point (1.0, 2.0) is the primary point; the other two are secondary
robustness points and cannot rescue a primary failure.

Task functional: transverse-field energy density -h X on the flux site
(declared, identical to the sealed instrument's QO-1/QO-2 declaration).
Encoder family: keep a subset S of the 4 outside qubits with |S| = k,
decode by reattaching vacuum marginals; budget = stored qubit slots;
exhaustive search over subsets; no optimizer. Anti-arm: the T-arm encoder
with the flux qubit Z-pinched before storage at identical budget.

Exclusions: no scenario angle used in the exploratory run of 2026-08-04
(training 0.6/0.9/1.2 x 0.1/0.2/0.3, held-out 0.75/1.05 x 0.15/0.25) may
appear in either grid below. The exploratory record
`results/qo2-flip.json` is superseded for claim purposes by the run
governed here and retains its exploratory label.

## Manifest

Scenario states apply exp(i theta_s Z) on the strong site and
exp(i theta_w Z) on the flux site.

- Training grid: theta_s in {0.55, 0.85, 1.15}, theta_w in
  {0.12, 0.22, 0.32} (9 states).
- Held-out grid: theta_s in {0.70, 1.00, 1.30}, theta_w in
  {0.08, 0.18, 0.28} (9 states).

Budgets: k in {1, 2, 3}. All computations are deterministic; there are no
seeds. Manifest hash: the SHA-256 of the runner file at the sealed
commit, recorded in the evidence record as code_commit.

## Primary outcome

The flip indicator at the primary coupling point, at the smallest budget
k* whose fidelity-optimal training subset excludes the flux site:
T-arm held-out task distortion < F-arm held-out task distortion - 0.01
AND T-arm held-out infidelity > F-arm held-out infidelity + 0.01. If the
fidelity-optimal subset contains the flux site at every budget, the
primary outcome is undefined and the run is reported as a scope failure,
not a pass.

## Secondary outcomes

Cannot rescue a failed primary: the flip indicator at the secondary
coupling points; persistence of the flip across every budget below the
collapse budget; collapse of the flip (both arms within 0.01 on task) at
the first budget whose fidelity-optimal subset contains the flux site;
contiguity of the flip region.

## Instrument controls

All bars of PEQO-FREEZE-002 apply, in particular B5, B6, B7, B10, B12,
and B13. The two-qubit analytic flip control in the test suite must pass.
The anti-arm must be strictly worst on held-out task distortion at every
budget and coupling point, else that (point, budget) cell is
uninterpretable and reported as such; an uninterpretable primary cell
voids the run.

## Estimator

The committed code path `python/qo2_flip.py` at the sealed commit,
modified only by the declared grids and coupling points above, executed
on Atlas in the committed venv with single-threaded BLAS. Task distortion
is the absolute error of the flux functional; infidelity is one minus
Uhlmann fidelity; arms are selected on the training grid only.

## Falsification bar

The claim is refuted at a coupling point if, at the defined k*, the T-arm
fails either margin on held-out states. Refutation at the primary point
refutes the preregistered claim. The bar does not move; margins are fixed
at 0.01.

## Missing-data rule

Every (coupling point, budget, arm, state) cell receives a value. Any
non-finite divergence, fidelity, or functional voids the run under B6,
and the void is reported.

## Multiple-comparison rule

Fixed hierarchy: primary point first, then secondary points in the listed
order. No correction is applied because the primary claim is a single
preregistered comparison.

## Stopping rule

The manifest is fixed and exhaustive. No sequential analysis, no visual
stopping.

## Resource envelope

Single Atlas process, single-threaded BLAS, expected minutes. No NRP
objects. No thermal-relevant load.

## Evidence record

One JSON record per run with the full grid results, code commit,
dependency versions, hostname, and SHA-256 hashes, appended to
`results/` and never rewritten.

## Interpretation ceiling

If the claim passes everywhere it earns [demonstrated-in-model] for this
model class and encoder family. It licenses no statement about other
model classes, about optimized continuous encoder families, about
physical gravity, or about quantum advantage of any kind.
