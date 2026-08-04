# Author notes

## What is complete

- Five-page RevTeX paper draft with a theorem, model boundary, campaign, and
  implementation section.
- Exact analytic controls in MATLAB and Python.
- Conserved Hamiltonian toy negative control.
- Circular worldline-instanton action baseline.
- Atlas-oriented MATLAB parameter-sweep driver.
- NRP-ready CPU Job templates and a vectorized CuPy/NumPy ensemble path.
- Preregistration template and evidence-record design.
- Python unit tests: 5 passed.
- PDF compiled and visually preflighted.

## What was not executed here

MATLAB is not installed in the artifact-generation environment. The MATLAB scripts
were written and inspected but must receive a first shakedown on Atlas before any
result is interpreted. That shakedown should be exploratory and should begin with
PF-0 only.

The SHP prior-art replication is specified but not implemented because the chosen
published configuration, equations, and convention mapping need to be selected and
transcribed carefully from the source paper. It should be a separate commit with a
line-by-line provenance note.

No Schwinger-rate result has been generated. The supplied S0 script verifies only
the reduced circular instanton action.

## Recommended first 48 hours

1. Run `run_p0_fold_baseline.m` on Atlas and compare its console output with the
   Python tests.
2. Run `run_p2_toy_hamiltonian.m`; verify event locations manually and halve
   `MaxStep` twice.
3. Run `run_manifest_atlas` on the four-row example manifest.
4. Containerize and run one NRP CPU smoke Job.
5. Compare the same scenario across MATLAB `ode45`, Python velocity Verlet, and the
   vectorized fixed-step implementation.
6. Only then freeze PF-0 tolerances and draft the first sealed preregistration.

## Paper strategy

The current manuscript is best treated as a methods/proposal draft. A results paper
should not be submitted until it contains:

- PF-0 instrument results;
- PF-1 structural-stability results;
- a clear negative or positive result from the generic Hamiltonian control;
- one SHP replication; and
- the sealed PF-4 Schwinger challenge.

The strongest likely first paper is a disciplined negative: projection folds are a
stable kinematic representation, but generic local hidden dynamics does not recover
Schwinger scaling without inserting equivalent large-deviation structure.

## Language to avoid

- "Spacetime is degenerate." The projection or time functional is singular at the
  fold; spacetime need not be.
- "High dimension causes pairs." A fold requires only an independent evolution
  parameter. High dimension matters only if it predicts fold statistics.
- "Opposite orientation proves opposite electric charge." Charge assignment is an
  additional model hypothesis.
- "The simulation explains pair production." A branch plot is kinematics. The
  physical gate is held-out rate, conservation, covariance, gauge independence,
  and quantum structure.
