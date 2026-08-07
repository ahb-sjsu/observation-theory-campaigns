# PF Campaign: Projection Folds and Apparent Pair Creation

**Status:** design draft, unsealed, non-claim-bearing.

## 1. Question

Can a smooth, local dynamics on a hidden manifold, observed through a singular
projection into spacetime, produce apparent particle-antiparticle pair events with
the quantitative structure of physical pair production?

The campaign separates three claims that must not be conflated:

1. **Kinematic claim:** a nondegenerate time fold produces two projected branches
   with opposite orientation indices. This is a theorem.
2. **Dynamical claim:** a specified local hidden dynamics produces such folds with
   a stable, non-arbitrary rate. This is empirical within the model.
3. **Physical claim:** the rate and observables reproduce quantum field theory,
   including the Schwinger exponent, conservation, covariance, and quantum
   statistics. This is a much higher bar.

A successful kinematic demonstration is not evidence for the physical claim.

## 2. Model class

Let the hidden state be `z(tau)` in a smooth manifold `M`. An observation map

\[
\pi:M\rightarrow \mathbb{R}^{1,3}
\]

produces the spacetime curve

\[
x^\mu(\tau)=\pi^\mu(z(\tau)).
\]

For a detector or observer with time functional

\[
T_u(x)=u_\mu x^\mu,
\]

a projected pair event occurs at a nondegenerate critical point

\[
\frac{d}{d\tau}T_u(x(\tau))=0,
\qquad
\frac{d^2}{d\tau^2}T_u(x(\tau))\ne 0.
\]

Locally, the time map has normal form

\[
T_u-t_0=\sigma(\tau-\tau_0)^2,
\qquad \sigma\in\{+1,-1\}.
\]

Across the fold, the unsigned number of intersections with a constant-time slice
changes by two. The signed intersection number does not change because the two
branches have opposite signs of `dT_u/dtau`.

### Important scope correction

The projection becomes singular relative to the chosen time slicing. Spacetime
itself need not be degenerate. A single extra evolution parameter is enough for
the fold; high dimension becomes relevant only if it predicts the distribution,
stability, or dynamics of folds.

## 3. Anti-circularity contract

A candidate model may not contain, directly or through an equivalent fitted term:

- a command to create a fold at the desired rate;
- the Schwinger exponent `pi*m^2/abs(qE)` as an input probability;
- a loss function fitted to the target rate on the same parameter range used for
  evaluation;
- postselection on trajectories that fold, escape, arrive, or resemble particles;
- observer-specific coordinate choices that are not transformed with the observer;
- energy or charge assigned only after examining the desired branch pairing.

The model may contain local fields, a metric, a Hamiltonian or action, a projection,
and a source distribution fixed before the claim-bearing sweep.

## 4. Instrument net

A null result is interpretable only after the measurement stack passes all controls.

| Control | Construction | Required result |
|---|---|---|
| N0 monotone time | `t(tau)=tau` | zero folds and one branch on every regular slice |
| P0 exact fold | `t(tau)=tau^2`, `x(tau)=v*tau` | branch count `0 -> 1 -> 2`; signed count remains zero |
| P1 annihilation fold | `t(tau)=-tau^2` | branch count `2 -> 1 -> 0` |
| D0 degenerate critical point | `t(tau)=tau^3` | no false classification as a nondegenerate pair fold |
| M0 double fold | `t(tau)=tau^3-tau` | both critical points found with correct orientation changes |
| S0 Schwinger action | `S(R)=2*pi*m*R-pi*abs(qE)*R^2` | minimizer `R=m/abs(qE)`, action `pi*m^2/abs(qE)` |
| E0 conserved toy | Hamiltonian oscillator/coupling model | relative energy drift below sealed numerical tolerance |

No claim-bearing run begins until every control passes at every numerical precision
used by the campaign.

## 5. Experiments

### PF-0: Exact fold and branch-count instrumentation

**Question.** Does the code recover the local fold theorem without false positives?

**Method.** Evaluate the exact controls above; solve for all preimages of each
observation time; compare numerical event locations with analytic roots.

**Primary witnesses.** Event-location error, branch-count error, orientation-index
error, signed-count invariance.

**Falsification bar.** Any missed simple fold, any cubic critical point classified as
a fold, or any violation of signed-count conservation outside the sealed tolerance
invalidates the instrument.

**Substrate.** MATLAB on Atlas first; Python replication on Atlas and NRP.

---

### PF-1: Structural stability of projection folds

**Question.** Does the apparent pair survive small perturbations of trajectory and
projection as singularity theory predicts?

**Method.** Perturb the coefficients of the exact fold with bounded random smooth
terms. Sweep perturbation norm, integration tolerance, sample density, and detector
slicing. Fit the local branch separation law

\[
\Delta x(t)\propto |t-t_0|^{1/2}.
\]

**Primary witnesses.** Fold persistence probability, fitted exponent, critical-point
condition number, false-split and missed-split rates.

**Predicted result.** Simple folds persist under small perturbations; degenerate
critical points split into the stable singularities allowed by the perturbation.

**Falsification bar.** The measured square-root law or persistence region disagrees
with the analytic control after numerical-error correction.

**Substrate.** MATLAB `parfor` on Atlas for the pilot; NRP CPU jobs for large
ensembles.

---

### PF-2: Generic local Hamiltonian dynamics

**Question.** Do folds arise generically under a local conserved dynamics, and what
controls their flux?

**Model.** Begin with an explicitly nonrelativistic toy Hamiltonian

\[
H=\frac12(p_t^2+p_x^2+p_u^2)
+\frac12\omega_t^2t^2
+\frac12\omega_u^2u^2
+\frac{\lambda}{4}u^4
+gEt u.
\]

The observed coordinate time satisfies `dt/dtau=p_t`; folds occur when `p_t=0`
with nonzero acceleration. This model is an instrumented negative control, not a
candidate theory of QED.

**Primary witnesses.** Fold rate, fold-type balance, energy drift, branch lifetime,
and dependence on initial-condition measure.

**Expected result.** Folds occur, but their rate is model- and measure-dependent and
does not exhibit a universal Schwinger law.

**Falsification bar for the physical mechanism.** If the apparent result disappears
under matched changes of initial-condition measure, time slicing, or integrator, the
mechanism is classified as sampling or coordinate artifact.

**Substrate.** MATLAB on Atlas for exact event detection; vectorized Python on NRP
for the ensemble.

---

### PF-3: Replication of a Stueckelberg-Horwitz-Piron pair trajectory

**Question.** Can the campaign reproduce an existing off-shell classical pair event
with its stated conservation laws?

**Method.** Implement one published SHP configuration before modifying it. Record
all equations, parameter conventions, initial conditions, and gauge fields. Compare
worldline geometry and conserved total quantities with the published case.

**Primary witnesses.** Worldline reversal in coordinate time, event locations,
field-plus-particle energy-momentum accounting, and reproduction error.

**Falsification bar.** Failure to reproduce the selected published case prevents any
novel extension from being interpreted.

**Substrate.** MATLAB on Atlas; independent Python implementation.

---

### PF-4: Schwinger scaling challenge

**Question.** Does a candidate hidden-manifold dynamics predict the nonperturbative
field, mass, and charge dependence of pair production?

For a constant electric field, the leading semiclassical target is

\[
\log \Gamma = \mathrm{const}-\frac{\pi m^2}{|qE|}
\]

up to known prefactors and unit conventions.

**Design.**

1. Fix the candidate action, projection, initial-condition measure, and fold
   classifier.
2. Use a training region only to calibrate one overall time/volume scale and, if
   unavoidable, one prefactor.
3. Hold out contiguous ranges of `E`, `m`, and `q`, plus combinations not present in
   training.
4. Compare the candidate against preregistered alternatives: polynomial threshold,
   Arrhenius-type exponential in a different variable, power law, and flexible
   spline with complexity penalty.

**Primary witnesses.** Held-out log-likelihood, slope of `log Gamma` versus
`m^2/abs(qE)`, residual structure, and rate stability under numerical refinement.

**Falsification bar.** The candidate fails if the held-out slope excludes `-pi`, if
a simpler alternative predicts better, or if the apparent exponential is produced
by an initial-condition weight or stopping rule equivalent to the target law.

**Substrate.** NRP GPU or CPU ensemble jobs. MATLAB on Atlas independently reduces a
sample of raw trajectories.

---

### PF-5: Conservation and complete accounting

**Question.** Is the apparent pair event compatible with conservation rather than a
branch-counting illusion?

**Requirements.**

- Every trajectory is counted, including no-fold, escape, recrossing, and numerical
  failure outcomes.
- The underlying Hamiltonian or action balance is checked continuously.
- Any orientation-based charge assignment is declared before runs.
- In a dynamical field model, energy gained by projected branches is matched by
  field-energy loss.

**Primary witnesses.** Total energy-momentum residual, signed orientation index,
charge balance, and missing-trajectory count.

**Falsification bar.** Any unexplained creation of conserved quantities, or a result
that depends on deleting unsuccessful trajectories, rejects the model.

#### PF5-001 sealed gate run, results (2026-08-06, record sha 073f6e692253...)

Verdict PASS on every sealed bar, and the pass does not test the intended claim.
All eight cells are evaluable, every census sums exactly to 20000 with zero missing
trajectories, the maximum relative energy residual across cells is 6.1e-7 against
the 1e-5 bar, and the path-degree rule holds at every generic level on all 96
declared polyline members with zero failures and zero refused levels. The census
also records zero reversing trajectories in every cell, all 160000 members
transmitted. The sealed claim concerns the accounting of apparent pair events, and
this grid contains none, so what the run certifies is the accounting machinery on
transmitted trajectories, not the conservation of pair events.

The named error is the manifest, not the instrument. PREREG-PF5-001 declared a
product grid of gaps against fields, while PF4-002 placed its cells by bisecting to
declared targets, which is how that manifest landed in the regime where reversals
occur. The sealed verdict stands as recorded, and the gate's content question is
carried by PF5-002 with probe-placed cells. This repeats PF4-003's lesson at the
level of the gate, a manifest must be verified to contain the events its claim is
about, and the rule now applies to gate runs as well as summit runs.

#### PF5-002, in preparation

The placement probe (`python/pf5_placement_probe.py`, unsealed) bisects the field at
each declared gap to land the reversing fraction inside the declared window 0.02 to
0.30, recording the selected field and the measured fraction per cell.
PREREG-PF5-002 binds only cells whose probe fraction lies in that window, keeps
every bar of PREREG-PF5-001 unchanged, and adds one bar, the reversing count per
bound cell must exceed zero in the governed run, so a vacuous pass cannot recur.

---

### PF-6: Observer, Lorentz, and gauge audit

**Question.** Is the claimed event physical or a coordinate-specific fold?

**Method.** Transform the complete setup, including detector time functional,
initial state, fields, and projection. For electromagnetic models, repeat in gauge
potentials producing the same field tensor.

**Primary witnesses.** Transformation of event worldpoints, invariant rate per
four-volume, detector response, and gauge-equivalent result identity.

**Falsification bar.** A rate that changes under a passive coordinate transformation
or gauge change is rejected. Observer-dependent particle number may be retained
only if a physical detector model predicts the corresponding difference.

---

### PF-7: Quantum-structure ceiling tests

**Question.** Can the model reproduce more than a classical worldline picture?

**Targets.** Scalar versus spinor rates, multipair statistics, Pauli blocking,
interference in pulsed fields, and backreaction.

**Interpretation.** Failure does not invalidate the kinematic fold theorem. It caps
the model as a classical representation rather than an alternative to quantum field
theory.

**Substrate.** NRP GPUs for path ensembles or lattice/quantum simulations; outside
the first claim-bearing paper unless PF-4 to PF-6 pass.

### PF-8: The decay gate (design only, declared 2026-08-05, gated)

**Question.** Can folding account for particle decay, one particle becoming two?

**The parity obstruction, already in the sealed evidence.** A fold changes the
observed unsigned branch count by exactly two and the signed count by exactly
zero. PF-0 measured this, branch counts 0 to 1 to 2 with signed count 0, and the
PF-5 charge rule makes it mechanical, charge is sign(dt/dtau) and generic level
crossings of a continuous worldline come in pairs (Whitney genericity of fold
singularities). A same-species decay, one particle to two, is a branch-count
change of plus one, odd parity. For complete continuous worldlines under generic
projections this is excluded, not missed. Folding imitates pair creation
precisely because pairs are what folds make.

**What folding can imitate.** Parity-even decay-like events. The zigzag one-to-
three event, parent plus created pair, reads as decay whenever the products are
misidentified or one product is unobserved.

**The loophole, and the campaign question.** A consumer blind to one branch class
reads a one-to-three fold event as one-to-two, apparent odd parity with missing
energy, which is exactly the phenomenology of decays with unobserved neutrinos.
The PE track's invisible-leak result is the same structure. PF-8a bars, declared
now. A complete observer records zero odd events across the full census,
mechanical parity audit. A declared blind observer's odd-event rate must be
predicted exactly by its detector model, the PF-6 lawful-observer clause, or the
run fails. Apparent decay in this model is a measurement of consumer blindness,
never a property of the worldline.

**PF-8b, lifetime statistics.** Real decay is memoryless, exponential survival.
Fold statistics are measure-borne, the PF-2 lesson, so the first-fold-time
distribution of a declared ensemble should be whatever the declared measure
says and memorylessness should require declared Poisson structure, an expected
negative with the measured shape recorded either way.

**Gate.** Design only. Runs only after the PF4-003 harvest and the sealed PF-5
and PF-6 gate runs, in sequence position after PF-6, sharing PF-7's substrate
options.

#### PF-8 protocol, declared 2026-08-06 before the run

Both mandatory gates cleared, so PF-8 is ungated and this is its concrete
protocol. The run is exploratory and unsealed. Runner `python/pf8_decay_gate.py`,
record `results/pf8-decay-gate.json`, schema `pf8-decay-gate-v1`. Instruments are
frozen and unmodified, `integrate` and `fold_count` from `python/pf6_covariance.py`,
`census_run` and `signed_count_rule` from `python/pf5_accounting.py`, and
`polyline_level_crossings` from `python/projection_fold.py`.

**The probe, and what it changed.** The standing rule is that a registration
must cite a probe verifying event presence per bound cell and member.
`python/pf8_blind_probe.py` ran first and is committed, record
`results/pf8-blind-probe.json`, sha `6dce4c52a31e43cb`. It changed two things
in the design above, and both changes are declared here before the run rather
than discovered after.

The first change is the observation configuration. The design above speaks of a
branch count that is even with signed count zero, which is the pair-creation
configuration where the worldline both begins and ends on one side of the
observed level. The probe measured that configuration absent on every bound
member. All four end at their own largest observed time and begin at their own
smallest, t_end equal to t_max and t_start equal to t_min, so both candidate
windows have width exactly zero. The bound members are through-going, one branch
in and one branch out, which is the configuration a decay question wants anyway.
The parity invariant on a through-going worldline is that the complete
observer's unsigned branch count is ODD at every level, and a fold changes it by
exactly two, so the sweep reads one branch, then three, then one. A same-species
one-to-two decay would be a change of exactly one and is excluded by the same
arithmetic. Every bar below is stated in this form, and the deviation from the
design's "even count, zero signed count" wording is exactly this reframing.

The second change is the level ladder. The probe measured the fold excursions as
narrow as 0.000253 in observed time on the P = 0.90 member, and 0.005314,
0.007744, 0.04449, and 0.025922 on the others, against a uniform ladder spacing
near 0.2. A uniform ladder therefore steps over the three-branch fibers almost
everywhere. The declared ladder merges a uniform background at fractions
0.01 through 0.99 of the span from t_start to t_end with nine levels at
fractions 0.1 through 0.9 inside each interval spanned by a consecutive pair of
fold times. On this ladder the probe found 46 three-branch levels across the
four members and zero refused levels.

**Bound members and cells.** Arm A takes the four members PREREG-PF6-002 bound
from its own member probe, gap, field, and initial transverse momentum equal to
(0.60, 0.8957885742187499, 3.0), (0.70, 1.0448364257812501, 3.0),
(0.80, 1.2020141601562502, 3.0), and (0.90, 1.3605468750000003, 2.0), step
budget 40000, verified to fold with counts 4, 2, 2, 2. Arm B takes the four
PREREG-PF5-002 cells at the same gaps and fields, ensemble 5000 per cell, seeds
8800000, 8801000, 8802000, and 8803000, keeping the polylines of the first 100
members per cell.

**The declared blind consumer.** The blind consumer fails to record any branch
whose transverse coordinate u at the crossing lies in the closed window
[-0.70, +0.70]. The window is fixed from the probe record and nothing about it
is tuned after the run. The probe pooled 533 crossings with u running from
-2.68598 to 2.714888 and quantiles q30 = -0.9930224 and q70 = 1.0100054, so the
declared window sits inside the bulk and hides 147 of the 533 crossings, 27.6
percent, some but not all. At the three-branch levels the probe measured the
middle branch inside the window and the outer two outside it on the P = 0.60,
0.70, and 0.80 members, while on the P = 0.90 member all three branches lie
inside [-0.33, +0.33] and the window hides the whole zigzag.

**D1, complete-observer parity.** Every audited member's fold count is even. At
every declared generic level the complete observer's unsigned branch count has
the parity fixed by the worldline endpoints, and every change in that count
between adjacent declared levels is even. The bar is zero odd events, where an
odd event is a count change of odd size, which is what a one-to-two decay would
be. Reported are the number of members audited, the number of kept thermal
polylines audited, and the number of odd events, which must be zero. The frozen
census stops a member at its first reversal, so a reversing member's kept
polyline is half a worldline and carries the endpoint form of the parity
statement rather than the even-fold-count form. That is an instrument fact, not
a result, and it is why arm B's parity clause is written against the endpoints.

**D2, signed count.** The frozen `signed_count_rule` reports zero failures on
every audited member at every declared generic level, on both arms, and the
signed count on each arm A member is constant across the whole ladder. This is
the statement that a fold changes the signed count by exactly zero, that folds
make orientation charge only in cancelling pairs. The bar is zero failures and
zero spread.

**D3, the blind consumer, the loophole made mechanical.** Per member and per
level the apparent count is measured twice by independent routes. The blind
consumer's own record scans its samples for sign changes of the observed time
against the level and interpolates u there by index arithmetic, then drops the
branches inside its window. The detector model takes the frozen crossing
instrument's list, reads u at the evolution parameter it returns, and predicts
the complete count minus the number of crossings whose u lies in the window. The
bar has two halves. The two routes agree exactly on every member and every
level, zero mismatches, which is the PF-6 lawful-observer clause applied to
decay. And the fraction of observations whose apparent parity differs from the
complete observer's is strictly greater than zero, which is the loophole. Also
reported and not barred is the count of apparent decay events, adjacent declared
levels across which the blind consumer's count rises by exactly one, the
mechanical imitation of one particle becoming two.

**D4, anti-vacuity.** Every audited arm A member has at least one fold, the
ladder resolves at least one multibranch level, the blind consumer hides at
least one crossing, and arm B's census contains at least one reversing member.
A run failing any of these is recorded vacuous rather than passing.

**Verdict** is computed from D1, D2, D3, and D4 by the runner. PF-8b carries no
bar.

**PF-8b protocol, measurement with an expected negative.** On arm B the survival
curve is measured by re-running the frozen census at a ladder of step caps with
the seed held fixed, so the count of members that have reversed by each cap is
the exact cumulative distribution of the first-reversal step over the same 5000
members. The caps are fractions 0.900 through 1.400 in steps of 0.025 of the
nominal slab-arrival step |T_START| / (P dt), which the probe placed correctly,
measuring the first reversal at cap 20000 and saturation by cap 26000 on the
P = 0.60 cell against a nominal 20000. Reversal times are binned at the ladder
spacing and reported as proper time. Recorded are the mean, the standard
deviation, the coefficient of variation, the coefficient of variation after
shifting to the measured onset, and the sup deviation between the empirical
survival curve and the exponential whose mean matches it, both raw and
onset-shifted. A cross-check sample of exact first-reversal steps comes from the
kept polylines, which end on the step at which the census classified them. The
discriminating statistic is the coefficient of variation, which equals one
exactly for a memoryless exponential. Memorylessness is expected to FAIL,
because the trajectory cannot reverse before it reaches the slab and the onset
is set by the geometry, not by a hazard. Either outcome is a result and the
measured shape is recorded either way.

### PF-4 summit, closed on the pulse-train family (2026-08-06)

Three records close the summit attempt on the thermal-free pulse-train family.
PREREG-PF4-003 sealed itself unevaluable, every cell capped without a reversal out
to 4000 slabs. The direct-observable probe (results/pf4-004-probe.json, sha
c5b7d79c79ac...) then measured N_rev at twelve cells, three field strengths crossed
with four velocities at identical constants, and found zero reversals in all
twelve, so PREREG-PF4-004 cannot bind and its template stays unsealed by its own
verification clause.

#### The mechanism, measured (results/pf4-mechanism.json, sha 99761a6f45d3...)

The declared hypothesis was that the alternating slabs cancel the deposits, with a
compound flag requiring both a cancellation ratio below 0.5 and an extrapolated
slabs-to-reversal above 4000. The flag reads False as recorded, and the two halves
separate cleanly. Cancellation is confirmed and strong, the net drift per slab is
3.3, 0.9, and 5.0 percent of the mean deposit magnitude in the three declared
cells, so 95 to 99 percent of every deposit is undone by the next slabs, with sign
flips on 54, 68, and 27 percent of consecutive deposits. The extrapolation half of
the flag failed because it took the absolute drift, and the third cell's drift is
positive, 0.0096 per slab, carrying the trajectory away from reversal rather than
toward it. The corrected reading is stronger than the declaration, the pulse train
does not merely deposit too slowly, its residual after cancellation has no fixed
sign, and at the largest declared field it accelerates the trajectory away from the
fold. A family whose net transfer can point either way will not spend the gap at
any cap, which is why every probed cell is empty.

## 6. Campaign sequence

```text
PF-0 instrument net
      |
PF-1 structural stability
      |
PF-2 generic local dynamics ---- PF-3 prior-art replication
      |                            |
      +------------+---------------+
                   |
             PF-4 Schwinger scaling
                   |
             PF-5 conservation
                   |
             PF-6 covariance/gauge
                   |
             PF-7 quantum ceiling
```

PF-0 through PF-3 are pilots and replication. PF-4 is the first experiment capable
of supporting a physical pair-production claim. PF-5 and PF-6 are mandatory gates,
not optional follow-up analyses.

## 7. Execution allocation

### MATLAB on Atlas

Best for:

- analytic controls and publication figures;
- adaptive ODE integration with event location;
- energy and conservation diagnostics;
- modest parameter sweeps with `parfor`;
- independent reduction of NRP outputs.

The code uses MATLAB ODE event functions to locate zeros of `dt/dtau` and returns
event time, state, and event index. Parallel sweeps use `parfor` when available.

### Atlas Python

Best for:

- reference implementation and unit tests;
- deterministic cross-language comparison;
- container build validation before NRP;
- exact reruns of selected NRP scenarios.

### NRP Nautilus

Best for:

- thousands to millions of independent trajectories;
- GPU-vectorized fixed-step symplectic integration;
- held-out parameter sweeps;
- replication over seeds, precision, and hardware.

NRP should host finite Kubernetes Jobs, not idle interactive containers. Keep a
large manifest in durable storage and expose only a bounded live working set. The
campaign controller must bound active workers, Kubernetes objects, I/O pressure,
and unreduced evidence.

## 8. Scenario record

Every trial writes one immutable JSON record containing:

- campaign and preregistration identifiers;
- code commit and container digest;
- complete model and numerical parameters;
- initial-condition and random-number seeds;
- projection and observer definition;
- all trajectory outcome counts;
- fold events and orientation indices;
- conservation residuals;
- runtime, hardware, precision, and resource use;
- SHA-256 hashes of inputs and output arrays.

The reducer may summarize records but may not replace or rewrite them.

## 9. Evidence labels

- `[proved]`: fold multiplicity and signed-index statements under stated smoothness.
- `[replicated]`: reproduced SHP or Schwinger benchmark.
- `[demonstrated-in-model]`: candidate passes sealed simulation bars.
- `[exploratory]`: unsealed sizing or instrument work.
- `[refuted]`: a sealed claim fails its bar.

No simulation result is labeled evidence that physical spacetime is a projection.

## 10. First paper boundary

The first paper should report only:

1. the fold theorem and exact instrument net;
2. structural-stability results;
3. the generic Hamiltonian negative control;
4. prior-art replication;
5. the sealed Schwinger scaling challenge, whether positive or negative.

Black-hole and Hawking extensions should remain future work until the constant-field
pair-production gates pass.
