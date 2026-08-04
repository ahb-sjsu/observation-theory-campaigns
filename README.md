# Projection-Fold Pair Creation

A falsification-first research campaign about what a lower-dimensional
observer sees when smooth hidden dynamics is watched through a singular
projection. The founding question is whether apparent particle-antiparticle
creation can arise as a fold of the map from a hidden evolution parameter
to observed time, and whether any honest local dynamics can predict fold
statistics, including the Schwinger exponent, without inserting the
answer. The campaign has since grown an entropy track, a quantum
observation track, and an entropic-geometry track, all under one evidence
discipline.

## Status at a glance (2026-08-04)

Three papers are published on Zenodo:

- **Entropy Across Singular Projections: Fiber Multiplicity, Caustics,
  and Observer-Relative Information.**
  DOI 10.5281/zenodo.21789011. The fold theorem (multiplicity jumps by
  two, signed count conserved), closed-form branch entropies (exactly one
  bit at a fold slice, exactly one and one half bits at the double-fold
  symmetric slice, zero for degenerate monotone maps), the caustic
  resolution-scaling law, and a reversible ensemble whose observed
  entropy swings 2.07 bits with zero hidden information loss.
- **Consumer-Relative Quantum Distinguishability on Causal Boundaries.**
  Concept DOI 10.5281/zenodo.21789046 (v2 at 10.5281/zenodo.21789929).
  The consumer channel and task layer over quantum relative entropy,
  exact classical anchors, a consumer hierarchy whose distinguishability
  distribution moves with the excitation sector, a task-versus-fidelity
  flip at scarce budgets, and a consumer-family consistency requirement
  that constrains couplings exactly when observers share events. The
  flip and family results are [demonstrated-in-model] under sealed
  preregistrations PREREG-QO2-001 and PREREG-QO3-001.
- **The Pair-Creation Threshold of Impulsive Stueckelberg-Horwitz-Piron
  Scattering Is a Cayley-Transform Pole.**
  DOI 10.5281/zenodo.21790096. An exact replication of Land,
  arXiv:1604.01625, plus three proved propositions: the published
  impulsive midpoint closure is the Cayley transform of the reduced kick
  generator, continuous accumulation of the same generator conserves a
  hyperbolic form and never reverses coordinate time, and beyond the
  pole the Cayley image lies in a disconnected group component no
  continuous flow reaches. The published threshold is the pole.

Experiment status:

| Experiment | Status |
|---|---|
| PF-0 instrument net (N0/P0/P1/D0/M0/S0/E0) | passed, sealed as PF0-FREEZE-001 |
| PF-1 structural stability | done, persistence and eps^2 perturbation-theory match |
| PF-2 generic Hamiltonian negative control | done, fold counts measure-set (all 10^4 members identical) |
| PF-3 prior-art replication (Land 2016) | done, exact, two preserved findings |
| PF-4 Schwinger challenge | designed (experiments/PF4-DESIGN.md), not sealed |
| PF-5..PF-7 | designed in CAMPAIGN.md, gated |
| PE-0/PE-1 entropy instruments | passing, sealed under PEQO-FREEZE-002 |
| PE-2 reversible fold cycle | done |
| PE-3..PE-5 | designed |
| QO-0/QO-1 quantum instruments | passing, sealed under PEQO-FREEZE-002 |
| QO-2 flip, QO-3 consumer family | [demonstrated-in-model] under sealed preregs |
| EG-0..EG-5 entropic geometry | designed, gated on open questions |

Four seals are in the ledger (`experiments/SEALS.md`), each a
registration ID, sealing commit, and SHA-256 blob hash: two instrument
freezes and two preregistrations. Both preregistered claims passed on
grids fully disjoint from their exploratory runs.

## Package map

- `experiments/CAMPAIGN.md` - the PF campaign design and evidence rules.
- `experiments/ENTROPY-TRACK.md` - PE track: entropy across singular
  projections, three-entropies discipline, PE-0..PE-5.
- `experiments/QUANTUM-OBSERVATION-BRIDGE.md` - QO track: consumer
  channels, the flip, the consumer-family quantifier.
- `experiments/ENTROPIC-GEOMETRY-TRACK.md` - EG track: gravity-adjacent
  design with the area-law gate as expected stopping point.
- `experiments/PF3-PROVENANCE.md` - line-by-line provenance of the Land
  replication and its two findings.
- `experiments/PF4-DESIGN.md` - the sealed-challenge design with the
  closure-prescription clause C1-C5.
- `experiments/PF0-TOLERANCE-FREEZE.md`, `PEQO-INSTRUMENT-FREEZE.md`,
  `PREREG-QO2-001.md`, `PREREG-QO3-001.md`, `SEALS.md` - the sealed
  layer.
- `matlab/` - Atlas MATLAB instruments and pilots (`+pf` package,
  `run_p0_instrument_net.m`, `run_pe0_entropy_controls.m`, sweeps).
- `python/` - reference implementations, quantum instruments, governed
  prereg runners, the Land replication, 46 tests.
- `paper/` - three RevTeX papers with compiled PDFs; `make_figdata.py`
  regenerates every figure table from committed evidence.
- `results/` - append-only hashed JSON evidence records.
- `nrp/` - Kubernetes Job and PVC templates for NRP ensembles.

## Reproducing

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r python/requirements.txt
pytest -q python/tests            # 46 tests
python python/qo0_instrument.py   # quantum instrument + anchors
python python/pe2_reversible_cycle.py
python python/shp_land2016.py     # Land replication + findings
python paper/make_figdata.py      # regenerate all figure data
```

MATLAB (Atlas): `addpath(genpath('matlab'))` then
`run_p0_instrument_net`, `run_pe0_entropy_controls`,
`run_p1_structural_stability`, `run_p2_toy_hamiltonian`.

Every claim-bearing number in the papers traces to a record in
`results/` or recomputes deterministically from committed code. Seals
verify with `git show <commit>:<path> | sha256sum` against
`experiments/SEALS.md`.

## Evidence discipline

1. Seal hypotheses, estimators, and falsification bars before
   claim-bearing runs; sealed documents are hash-ledgered and any edit
   voids the seal.
2. Count every trajectory; no conditioning on successful folds,
   arrivals, or detections.
3. Validate every instrument against exact null and positive controls;
   instrument defects found in shakedowns become standing controls
   (seven so far, from no-signalling nulls to the Cayley trap).
4. Keep an append-only record sufficient for independent recomputation.
5. A clean negative is a result. The expected outcome of the Schwinger
   challenge remains a disciplined negative.

## Evidence labels

`[proved]` mathematics, `[replicated]` published benchmarks,
`[demonstrated-in-model]` sealed simulation bars passed,
`[exploratory]` unsealed work, `[refuted]` a sealed claim failed.
No simulation result is labeled evidence that physical spacetime is a
projection, and the quantum track adds its own standing sentence: the
consumer does not create anything physical by choosing what to observe.
