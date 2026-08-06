# RG Track: Renormalization as Consumer Structure

**Status:** design draft, unsealed, non-claim-bearing. Chip 🔵 RG.
Everything is measured in declared exact finite models.

## 1. Question

A block-spin coarse-graining is a declared consumer, a channel from
microstates to coarse variables. The renormalization group studies
what survives repeated application of that channel. The track
question is which parts of the standard renormalization story are
properties of the substrate and which are properties of the declared
channel. Is universality consumer-relative or invariant. Is the
relevant-irrelevant split a channel property. Does a task-optimized
coarse-graining beat the fidelity-optimal one at predicting
long-distance observables, the campaign's flip in renormalization
form.

## 2. Anchors (verified citations to be completed before any seal)

Kadanoff block spins, Wilson's renormalization group, the exactness
of decimation for the one-dimensional Ising chain, and the known
generation of longer-range couplings by majority-rule blocking.
Each enters as a replication target or a comparison, never as an
inserted answer.

## 3. Anti-circularity contract

No coarse Hamiltonian form is assumed where representability is the
measured question. Channels, models, and observables are declared
before claim-bearing runs. A claimed invariance must hold across the
full declared channel family or the claim fails.

## 4. Experiments

### RG-0: Exact coarse-graining instrument layer

One-dimensional Ising ring, exact by transfer matrix and by full
enumeration. Protocol declared 2026-08-05, before the run.

C1 route agreement, free energy from transfer-matrix eigenvalues
equals full enumeration for N = 12 at K = 0.3 and K = 0.7 within
1e-12. C2 decimation exactness, the marginal distribution of every
other spin of a 12-ring at K = 0.5 equals the 6-ring Ising
distribution at K' = atanh(tanh^2 K) within 1e-12 in every
configuration probability. C3 correlation-length flow, xi(K') =
xi(K)/2 within 1e-12, with xi = -1/ln tanh K. C4 channel
dependence of representability, majority-rule blocks of three on a
12-ring at K = 0.6 produce a coarse distribution whose
nearest-neighbor Ising fit (coupling matched exactly to the coarse
nearest-neighbor correlator on the 4-ring) mispredicts the coarse
next-nearest correlator by at least 1e-4, while the decimation
channel's full-distribution residual stays below 1e-12. The same
substrate is representable or not representable in the coarse
family depending only on the declared channel. C5 flow composition,
decimating twice equals one decimation at the composed coupling
within 1e-12. All five or RG-0 fails. Exploratory label,
results/rg0-instrument.json.

### RG-1: Channel-family invariance of long-distance structure

Two-dimensional Ising on narrow strips, exact by transfer matrix. A
declared family of channels (decimation, majority, task-optimized).
Measured, which long-distance quantities are invariant across the
family and which are channel artifacts.

### RG-2: The flip in renormalization form

Fidelity-optimal versus task-optimal coarse-grainings at fixed
budget, the task being prediction of declared long-distance
observables. QO-2 and GD-2 transplanted.

### RG-3: Universality gate

Distinct declared microscopic models under one declared channel.
Measured, do their coarse theories converge, and is the convergence
channel-relative. Either outcome is a result.

### RG-4: Relevance as a channel property

Declared perturbations to the microscopic model. Measured, whether
growth or decay of a perturbation under the flow depends on the
declared channel.

## 5. Evidence discipline and non-claims

Seals, labels, append-only records, and falsification bars as in
CAMPAIGN.md. Substrate, exact finite models in Python on Atlas.
Nothing in this track is a claim about any experimental material
system.
