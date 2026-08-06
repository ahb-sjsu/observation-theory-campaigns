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

#### RG-0 results (run 2026-08-05, record sha e191e2b095eb...)

Verdict PASS, all five items. Route agreement exact, decimation
exact to 4.2e-17 in every configuration probability with the
closed-form coupling flow, the correlation length halves exactly,
and the flow composes exactly. The channel-dependence item is
sharp, the majority-rule coarse distribution's best
nearest-neighbor fit mispredicts the next-nearest correlator by
0.0260, two hundred sixty times the bar, while the decimation
channel's full-distribution residual on the same substrate is
4.2e-17. The same microscopic model is exactly representable in the
coarse family under one declared channel and measurably not under
another, the track's seed measured.

### RG-1: Channel-family invariance of long-distance structure

Two-dimensional Ising on narrow strips, exact by transfer matrix. A
declared family of channels. Measured, which long-distance
quantities are invariant across the family and which are channel
artifacts.

#### RG-1 protocol (declared 2026-08-05, before the run)

Substrate, the two-dimensional Ising model on a width-4 periodic
cylinder at K = 0.3, exact by the symmetric 16 by 16 column
transfer matrix. Channel family, four declared column functionals,
decimation (the first spin), majority (ties broken to the first
spin), the adjacent pair product, and the column parity. The
long-distance quantity is the decay rate of the connected
correlator of the channel output along the cylinder, measured from
exact correlator ratios at separations 8 through 16, with a second
route through direct transfer-matrix powers required to agree to
1e-10.

The declared structure to be tested. The transfer matrix commutes
with the global spin flip, so its eigenvectors split into odd and
even sectors, and a channel's correlator is exactly a sum over the
eigenvectors its output couples to. Decimation and majority are odd
functionals, the pair product and the parity are even. A correlator
ratio at finite separation carries subleading terms, so the bars
are on exact sector selection, which proves the asymptotic rate.
Bars. B1, each odd channel's amplitude onto every even eigenvector
beyond the ground state is at most 1e-12 while its amplitude onto
the leading odd eigenvector is at least 1e-6, so its decay rate is
exactly the leading odd eigenvalue ratio. B2, the same for the two
even channels with the sectors exchanged, disconnected part
subtracted, rate exactly the leading subdominant even ratio. B0,
the eigen-sum correlator and the direct transfer-matrix-power
correlator agree to 1e-10 in relative terms at separations 8
through 16. B3, the two sector rates are measurably different,
ratio recorded. B4, amplitudes within a sector differ across
channels, spread recorded, measurement with no bar. The
reading, the decay rate is invariant within a symmetry sector and
the declared channel selects which sector's invariant the observer
sees, correlation length itself is consumer-selected, not
consumer-invented. Exploratory label,
results/rg1-channel-family.json.

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
