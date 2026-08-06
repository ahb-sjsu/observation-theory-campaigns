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
