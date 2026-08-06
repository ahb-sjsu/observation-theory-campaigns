# HD Track: Dissipation as Consumer Structure

**Status:** design draft, unsealed, non-claim-bearing. Chip 🟠 HD.
Everything is measured in declared exact finite models.

## 1. Question

Reversible lattice gases flow, at coarse scales, into hydrodynamics
with dissipative coefficients. Dissipation from a reversible
substrate is the PE track's result at the level of transport. The
track question is whether the dissipative coefficient is a property
of the substrate or of the declared coarse-graining prescription,
the WM-2h question asked of viscosity, and whether the second-law
appearance at coarse scale is entirely the observer's, the
Loschmidt control made mechanical.

## 2. Anchors (verified citations to be completed before any seal)

The HPP lattice gas of Hardy, de Pazzis, and Pomeau, its exact
conservation laws and reversibility, and the known anisotropy of
its hydrodynamic limit. Each enters as a replication target or a
comparison, never as an inserted answer.

## 3. Anti-circularity contract

No transport coefficient is inserted. Initial conditions, update
rules, and coarse-graining prescriptions are declared before
claim-bearing runs.

## 4. Experiments

### HD-0: Exact lattice-gas instrument layer

HPP on a 16 by 16 torus, four boolean velocity channels per site,
streaming plus the head-on collision rule, a declared blob initial
condition with a seeded sparse background. Protocol declared
2026-08-05, before the run.

C1 exact conservation, total mass and both momentum components are
integer-exact at every one of 200 steps. C2 bit-exact
reversibility, reversing all velocities after 200 steps and
evolving 200 more, then reversing again, reproduces the initial
state bit for bit. C3 observational entropy, the declared 4 by 4
cell coarse-graining's count-distribution entropy rises from the
ordered start by at least 0.3 bits over the forward run, and on the
reversed run the entropy curve retraces the forward curve exactly,
step for step, the rise is the observer's, the substrate forgets
nothing. C4 symmetry equivariance, rotating the initial state by
ninety degrees and evolving equals evolving and then rotating, bit
for bit, with the channel relabeling included. All four or HD-0
fails. Exploratory label, results/hd0-instrument.json.

### HD-1: Exact transport instrument

Declared shear and sound initial profiles. Measured, decay rates
and dispersion against declared predictions, the viscosity
instrument validated on exact controls.

### HD-2: The prescription gate for viscosity

A declared family of coarse-graining prescriptions (cell size,
window shape, sampling cadence). Measured, whether the extracted
transport coefficient is prescription-invariant or
prescription-borne, WM-2h transplanted. Either outcome is a result.

### HD-3: Dissipation declared-or-absent

An EG-6-style gate. Measured, whether any declared coarse
observable of the reversible substrate obeys a strict dissipative
law, or whether every apparent dissipation is an accounting of the
consumer's reversal reach, PE-4 at the level of transport.

## 5. Evidence discipline and non-claims

Seals, labels, append-only records, and falsification bars as in
CAMPAIGN.md. Substrate, exact finite models in Python on Atlas.
Nothing in this track is a claim about any physical fluid.
