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

#### HD-0 results (run 2026-08-05, record sha df840be16409...)

Verdict PASS, all four items. Mass 194 and both momentum components
integer-exact at every step, the double reversal reproduces the
initial state bit for bit, and the rotated evolution equals the
evolved rotation bit for bit. The observational entropy rises 0.637
bits from the ordered start and the reversed run retraces the
forward curve with maximum deviation exactly zero, the rise is the
observer's, the substrate forgets nothing. The recorded curve
oscillates between fillings rather than rising monotonically, the
blob sloshes on the torus, HPP's known anisotropy already visible
to the coarse consumer, an early instrument note for HD-1.

### HD-1: Exact transport instrument

Declared shear and sound initial profiles. Measured, decay rates
and dispersion against declared predictions, the viscosity
instrument validated on exact controls.

#### HD-1 protocol (declared 2026-08-05, before the run)

HPP on a 64 torus, base occupancy 0.3 per channel, ensembles of 100
declared seeded realizations, 400 steps. Shear, the north and south
occupancies are modulated as 0.3 plus and minus 0.06 sin(2 pi k
x / 64), transverse momentum decaying diffusively. Sound, all four
occupancies modulated together, a standing density wave. The
projected mode amplitude is the ensemble mean of the sine-mode
overlap, the shear rate is the log-slope over steps 50 to 350, and
the sound frequency comes from the zero-crossing spacing of the
oscillating amplitude.

Bars, deliberately scaling-based, no Boltzmann coefficient is
assumed. H1, the shear mode decays, the amplitude at step 350 is
below 0.9 of the amplitude at step 50, and the rates fitted on the
two half-windows agree within twenty percent. H2, diffusive
scaling, the k = 2 shear rate over the k = 1 rate lies in [3.4,
4.6]. H3, sound dispersion, the measured frequency at k = 1 lies
within fifteen percent of k_phys divided by sqrt 2, and the k = 2
over k = 1 frequency ratio lies in [1.85, 2.15]. H4, mass and both
momentum components integer-exact in every realization at every
step. The measured viscosity and sound speed are recorded as
values, with the Boltzmann-level comparison noted as comparison
only. All four or HD-1 fails. Exploratory label,
results/hd1-transport.json.

#### HD-1 results (run 2026-08-05, record sha 0a60c7ef5698...)

Verdict FAIL on the shear items, and the failure is the
substrate's own physics, exactly measured. The shear amplitude did
not decay at all, decay ratio exactly 1.0 at both wavenumbers with
fitted rates at the 1e-18 floating floor. The cause is HPP's known
spurious conservation laws, the head-on collision exchanges a
north-south pair for an east-west pair, both with zero net momentum
at the site, and streaming keeps each mover on its line, so the
transverse momentum of every column and the longitudinal momentum
of every row are separately conserved and a shear mode can never
relax. The instrument measured the pathology that motivated the
FHP model. The sound sector passed, measured sound speed 1.008 and
1.012 of the lattice prediction at the two wavenumbers, dispersion
ratio 2.008, and conservation was integer-exact throughout.

#### HD-1b protocol (declared 2026-08-05, before the run)

The FAIL is converted into exact bars. S1, the per-column
transverse momentum vector of the shear ensemble is integer-exact
constant at every step, and the per-row longitudinal momentum
vector likewise, the two spurious invariants measured as exact
conservation laws rather than inferred from a stalled fit. S2, the
sound bars of HD-1 unchanged. The diffusive-scaling bar is
withdrawn as unmeasurable on this substrate, viscosity requires a
substrate without the spurious invariants, deferred to the HD-2
design which will declare the FHP hexagonal gas. Exploratory
label, results/hd1b-transport.json.

#### HD-1b results (run 2026-08-05, record sha cff6ae81ffaa...)

Verdict PASS, all three items. The per-column transverse momentum
vector and the per-row longitudinal momentum vector are
integer-exact constant at every one of 400 steps across the full
ensemble, the two spurious invariants are now measured
conservation laws, and the frozen shear mode of HD-1 is their
corollary. The sound sector repeats its pass, measured sound speed
1.008 and 1.012 of the lattice prediction, dispersion ratio 2.008,
conservation integer-exact. The transport instrument is validated
on the observables this substrate can relax, and the viscosity
question moves to the FHP design of HD-2 with the pathology on
record rather than discovered downstream.

### HD-2: The prescription gate for viscosity

A declared family of coarse-graining prescriptions (cell size,
window shape, sampling cadence). Measured, whether the extracted
transport coefficient is prescription-invariant or
prescription-borne, WM-2h transplanted. Either outcome is a result.

#### HD-2 protocol (declared 2026-08-05, before the run)

The substrate is FHP-I on a triangular lattice, the hexagonal gas
that HD-1b's pathology record demanded. 64 rows by 64 columns in
even-r offset coordinates, pointy layout, periodic in both
directions, six boolean channels per site with directions i = 0 to
5 at angles 60 i degrees, unit vectors with x components (1, 1/2,
-1/2, -1, -1/2, 1/2) and y components (0, s3, s3, 0, -s3, -s3)
where s3 = sqrt(3)/2. The declared coordinate convention, x_phys =
c + 0.5 (r mod 2), y_phys = -r s3, so row r-1 is up, toward +y.
Neighbor tables, for even r the six neighbors E NE NW W SW SE are
(r, c+1), (r-1, c), (r-1, c-1), (r, c-1), (r+1, c-1), (r+1, c),
and for odd r they are (r, c+1), (r-1, c+1), (r-1, c), (r, c-1),
(r+1, c), (r+1, c+1). Collisions, FHP-I. Head-on two-body, exactly
channels i and i+3 mod 6 occupied and the other four empty rotates
the pair to i+1 and i+4 on even time steps and to i-1 and i+2 on
odd time steps, deterministic alternating chirality. Three-body
symmetric, exactly channels 0, 2, 4 occupied and the others empty
becomes 1, 3, 5, and vice versa. Every other configuration is
unchanged. An update is collide then stream. Momentum is tracked
integer-exactly, twice the x momentum via channel components (2,
1, -1, -2, -1, 1) and the y momentum in units of s3 via (0, 1, 1,
0, -1, -1).

Geometry self-tests, bars that must pass before any physics is
read. T1, a single particle in channel i evolved 6 full steps has
physical displacement exactly 6 e_i, for every i, in the declared
convention. T2, one step in each direction 0 through 5 in sequence
returns to the start site, from an even-row start and from an
odd-row start. T3, total mass and both integer momentum components
are conserved exactly at every step of every physics realization.

The shear instrument. An ensemble of M = 50 seeded realizations,
seed 20260820 + k, T = 300 steps, base occupancy f0 = 0.35 per
channel. The occupancy of channel i at a site with physical
coordinate x_phys is f0 + 0.10 (e_i y component / s3) sin(2 pi k
x_phys / 64), k in {1, 2}, sampled Bernoulli per site and channel
with the probability clipped to [0, 1]. The observable is the
per-column (by c index) sum over rows of the integer y momentum in
s3 units, ensemble averaged, projected onto sin(2 pi k c / 64)
with the 2/L normalization of HD-1. Rates are the log-slope of the
absolute amplitude over declared windows, steps 30 to 250 for k =
1 and steps 15 to 120 for k = 2, with half-window consistency
required within twenty-five percent.

Bars. H2a, the shear decays, the k = 1 amplitude at step 250 is
below 0.9 of the amplitude at step 30, and the two half-window
rates agree within twenty-five percent of the full-window rate at
both wavenumbers. H2b, diffusive scaling, the k = 2 rate over the
k = 1 rate lies in [3.0, 5.0]. H2c, T1 through T3 all exact.

The prescription gate. Nine declared prescriptions are applied to
the same stored k = 1 per-column momentum series, the field
estimated from raw sites, from 4-column cell averages, and from
8-column cell averages, crossed with sampling cadences of 1, 2,
and 4 steps. A cell average replaces each column's value by the
mean over its block of columns before the same sine projection,
and a cadence uses every Nth stored frame, the fitted per-frame
slope divided by the cadence so every rate is per unit time, all
nine fitted over the same declared step window. Item H2d, the
declared hypothesis, the extracted rate is
prescription-invariant, the spread across the nine, max minus
min, is at most ten percent of the mean, since linear averaging
and subsampling preserve an exponential mode's rate. Either
outcome is a result. H2d is a finding with a declared directional
bar, recorded individually, and the VERDICT is computed from H2a,
H2b, and H2c only, this split is declared here.

The measured viscosity nu = rate / k_phys squared, k_phys = 2 pi
k / 64 with unit lattice spacing in x, is recorded as a value,
and any Boltzmann-level number placed beside it is comparison
only, never a bar. Runner python/hd2_fhp_viscosity.py, schema
hd2-fhp-viscosity-v1, exploratory label,
results/hd2-fhp-viscosity.json.

#### HD-2 results (run 2026-08-06, record sha de87e1801b4b...)

Verdict PASS, all three items. The geometry is exact, the six-step
displacement equals 6 e_i in every channel, the six-direction
hexagon closes from both row parities, and mass with both integer
momentum components is conserved exactly in every realization at
every step. The shear that HPP froze relaxes on FHP, the k = 1
amplitude falls to 0.170 of its window start and the k = 2
amplitude to 0.027, rates 0.008114 and 0.036818 with half-window
agreement inside the twenty-five percent bar at both wavenumbers,
and the rate ratio 4.538 sits in the declared diffusive band [3.0,
5.0]. The measured viscosity is 0.842 at k = 1 and 0.955 at k = 2,
beside the FHP-I Boltzmann estimate 0.742, comparison only. The
gate, the nine declared prescriptions on the same stored series
give rates from 0.008107 to 0.008113, a spread of 0.07 percent of
the mean against the ten percent bar, so H2d records
prescription-invariant. The contrast with WM-2h is the finding, an
exponential hydrodynamic mode's rate survives every declared
linear cell average and every subsampling cadence, while the
growth rule's bookkeeping did not survive a change of match order,
so which observables a prescription can touch is itself a measured
distinction, not a slogan. Dissipation declared-or-absent moves to
HD-3 with a validated viscous substrate in hand.

### HD-3: Dissipation declared-or-absent

An EG-6-style gate. Measured, whether any declared coarse
observable of the reversible substrate obeys a strict dissipative
law, or whether every apparent dissipation is an accounting of the
consumer's reversal reach, PE-4 at the level of transport.

#### HD-3 protocol (declared 2026-08-06, before the run)

The substrate is HD-2's FHP-I gas unchanged, the same 64 by 64
even-r offset triangular torus, six channels, head-on pairs
rotated +60 degrees on even steps and -60 on odd steps, the
symmetric three-body flip, collide then stream, imported from the
HD-2 runner rather than reimplemented. One shear ensemble at k =
1, M = 50 seeded realizations, seed 20260825, f0 = 0.35, amplitude
0.10, T = 300 steps, and the projected shear amplitude a(t) is
HD-2's observable exactly, the ensemble-mean per-column integer y
momentum in s3 units projected onto sin(2 pi c / 64) with the 2/L
normalization.

The gate. D1, exact invertibility. An FHP-I update is a bijection,
so the exact inverse step is declared, un-stream by pulling every
channel back along its own direction, then invert the collision at
the recorded parity, head-on pairs rotate -60 degrees where the
forward step rotated +60 and +60 where it rotated -60, and the
three-body flip is its own inverse, which is the HD-2 collision at
flipped time parity. The forward run is evolved T steps with the
parity sequence recorded, the inverse steps are applied in reverse
order, and the bar is that the initial state is recovered bit for
bit in every realization. D2, the Loschmidt account. a(t) is
recorded on the forward run, where HD-2 measured decay at rate
0.0081, and on the inverse run, and the bar is that the
inverse-run amplitude sequence equals the forward sequence
reversed exactly, float for float, since a deterministic bijection
projecting identical integer states must match bitwise. The
"dissipated" mode is then exactly recoverable and no strict
dissipative law governs the coarse observable, the apparent decay
is the observer's accounting, not a substrate law. D3, the
reversal-reach clause, PE-4 at the transport level. One declared
bit is flipped in the state at time T, channel 0, row 32, column
32, realization 0, before inverting. The bar, the perturbed
inverse run fails to recover the initial amplitude, the returned
amplitude at time 0 for realization 0 alone is at most half that
realization's true initial amplitude, computed per realization,
while the other 49 untouched realizations still return bit for
bit, a control inside the item. The per-step divergence, the
Hamming distance between the perturbed-inverse and true-inverse
states of realization 0, is sampled every 30 steps to record the
lightcone flood.

Verdict from D1, D2, D3, all three or HD-3 fails. The reading to
record with the results, dissipation on this substrate is
declared-or-absent in the consumer, exactly PE-4's lesson at the
level of transport, the coarse mode's decay is recoverable by any
observer with exact reversal reach and irrecoverable after the
loss of one bit. Runner python/hd3_dissipation_gate.py, schema
hd3-dissipation-gate-v1, exploratory label,
results/hd3-dissipation-gate.json.

#### HD-3 results (run 2026-08-06, record sha d3f5fafa7cb7...)

Verdict PASS, all three items. The declared inverse recovers the
initial state bit for bit in all 50 realizations, and the
inverse-run amplitude sequence equals the forward sequence
reversed with maximum deviation exactly zero, float for float. The
forward amplitude fell from 25.31 to 2.15, ratio 0.085, the HD-2
viscous decay reproduced on the new seed, and every one of those
"dissipated" numbers came back on the way in, so no strict
dissipative law governs the coarse observable, the decay is the
observer's accounting. One flipped bit at time T destroys it, the
perturbed inverse returns realization 0 at amplitude 0.437 against
a true initial 24.04, return ratio 0.018 against the 0.5 bar,
while the 49 untouched realizations return bit for bit, the
control inside the item. The Hamming divergence floods, 1 bit at
the flip, 3047 by 30 inverse steps, 11007 by 60, then a plateau
near 11200, which is the full decorrelation value 2 f (1 - f)
times the 24576 bits of a realization, about 11182, the lightcone
fills the torus and the perturbed trajectory becomes a stranger to
the true one. The reading declared before the run stands measured,
dissipation on this substrate is declared-or-absent in the
consumer, exactly PE-4's lesson at the level of transport, the
coarse mode's decay is recoverable by any observer with exact
reversal reach and irrecoverable after the loss of one bit.

## 5. Evidence discipline and non-claims

Seals, labels, append-only records, and falsification bars as in
CAMPAIGN.md. Substrate, exact finite models in Python on Atlas.
Nothing in this track is a claim about any physical fluid.
