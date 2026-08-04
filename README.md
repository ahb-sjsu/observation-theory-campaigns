# Projection-Fold Pair Creation

A computational research package for testing whether apparent particle-antiparticle
creation can arise when smooth trajectories in a hidden state manifold are observed
through a singular projection into spacetime.

## Status

**Proposal and instrumentation package. No physical pair-production claim is made.**

The mathematically exact statement is kinematic: a nondegenerate fold of the
coordinate-time map changes the number of intersections with a constant-time slice
by two, with opposite orientation indices. The research question is whether an
independently specified local dynamics can predict the *statistics* of those folds,
including the Schwinger exponent, conservation laws, and covariance, without
inserting those answers into the projection or sampling law.

## Package map

- `paper/` - readable RevTeX manuscript and compiled PDF.
- `experiments/CAMPAIGN.md` - staged Atlas/NRP experiment regime.
- `experiments/PREREG-TEMPLATE.md` - claim-bearing preregistration template.
- `experiments/manifest-example.csv` - example scenario grid.
- `matlab/` - Atlas/MATLAB pilots, analytic controls, ODE event detection, and sweeps.
- `python/` - container-friendly reference implementation for Atlas or NRP.
- `nrp/` - Kubernetes Job and PVC templates plus deployment notes.
- `results/` - intentionally empty except for `.gitkeep`; generated evidence belongs here.

## Fast start: MATLAB on Atlas

From the package root in MATLAB:

```matlab
addpath(genpath('matlab'));
run_p0_fold_baseline;
run_p1_structural_stability;
run_p2_toy_hamiltonian;
schwinger_instanton_baseline;
```

For a parallel parameter sweep:

```matlab
run_manifest_atlas('experiments/manifest-example.csv', 'results/matlab');
```

The scripts use `parfor` when Parallel Computing Toolbox is available and fall back
to an ordinary loop otherwise.

## Fast start: Python

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r python/requirements.txt
pytest -q python/tests
python python/generate_manifest.py --output experiments/manifest.jsonl
python python/run_trial.py --scenario-json '{"model":"analytic_fold","t_obs":1.0}' --output results/smoke.json
python python/reduce_campaign.py --input results --output results/summary.json
```

## Evidence discipline

The campaign inherits five non-negotiable rules from the accompanying research
program:

1. Seal hypotheses, estimators, and falsification bars before claim-bearing runs.
2. Count every trajectory; no conditioning on successful folds, arrivals, or detections.
3. Validate the instrument against exact null and positive controls.
4. Keep an append-only record sufficient for independent recomputation.
5. Treat a clean negative as a result, not as a failed campaign.

The Hubness-Bell audit is the methodological precedent: it retained the attractive
reframing, rejected the unsupported mechanism, and preserved an instrument error
alongside the corrected verdict.

## Build the paper

```bash
cd paper
./build.sh
```

Or use the repository-level PDF helper described in the generated source notes.
