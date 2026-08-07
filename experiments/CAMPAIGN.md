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

### PF4-005: The analyticity exponent (declared 2026-08-07, before the run)

**The summit question.** PREREG-PF4-002 sealed the negative that the Sauter
family's suppression is a Gaussian measure tail in the effective gap, and left one
question open, whether any constructible family has a non-measure-tail exponent.
PREREG-PF4-003 and the PF4-004 probe closed the pulse-train route by measuring that
family empty at every probed cell, and the mechanism study explained why, its
deposits cancel between 95 and 99 percent with no fixed sign.

**The route the first hunt probe left open.** A single deterministic crossing has
one declared initial condition, so there is no distribution whose tail could produce
a suppression. The first hunt probe already measured the per-crossing transfer to be
exponential in the inverse velocity with a coefficient of determination of 0.992,
and it recorded a slope of -7.8186 against a naive estimate of -11.3097, a ratio of
0.6913. What that probe could not say is whether the exponent is dynamical rather
than an accident of the fitted range.

**The decisive test.** An exponent set by the field's nearest complex singularity is
a dynamical quantity, and no measure tail knows where a function's poles are. The
declared comparison changes the singularity distance while holding the width fixed.
The tilt tanh with force sech squared has its nearest pole at pi over two times the
width, and the tilt arctangent with Lorentzian force has its nearest pole at the
width itself, so at equal width their exponents should stand in the ratio pi over
two. Both predictions used here are ratios, so neither depends on the absolute
coefficient the probe found to be 0.69 of the naive estimate.

**Declared run.** Field 0.4, velocities 1.2, 1.5, 2.0, 2.5, 3.0, and 4.0, widths
2.0, 3.0, and 4.0, both profiles, timestep 2e-4, fourth-order Runge-Kutta, entry and
exit at twenty widths. The observable is the residual oscillator energy about the
instantaneous well at exit, which is well defined for both profiles including the
one whose tails are algebraic.

**Bars.** A0, the timestep control, halving the timestep changes the most suppressed
measured value by at most two percent. A1, the exponential form holds, the fit of
the log residual against the inverse velocity has a coefficient of determination of
at least 0.99 in every one of the six cells. A2, the pole-distance test, at each
width the ratio of the two profiles' exponents is within ten percent of pi over two.
A3, the width-scaling test, at each profile the exponent is linear in the width
within ten percent.

**Measurements with no bar.** A4, the run is deterministic with one declared initial
condition per cell, so no measure exists whose tail could be responsible. A5, the
ratio of each measured exponent to the naive estimate, recorded for the question of
what the correct dynamical formula is.

**Readings, declared in advance.** If A2 and A3 hold, a constructible family has an
exponent fixed by the field's analytic structure, which is dynamical and cannot be a
measure tail, and the summit question is answered for the per-crossing transfer. The
open step from that transfer to an observable event rate remains, and it is blocked
by the cancellation the mechanism study measured, so no claim about a pair rate
follows. If A2 or A3 fails, the exponential is not analyticity-controlled and the
summit stays open, recorded as such.

**Substrate.** Atlas Python, exploratory and unsealed,
`results/pf4-005-analyticity.json`.

#### PF4-005 results (run 2026-08-07, record sha 91358f459661...)

Verdict FAIL on three of four bars, and the failure separates the two profiles
cleanly rather than condemning the idea. The timestep control passed with a relative
change of 6.9e-11, so nothing here is numerical. The sech-squared cell at width
three reproduced the first hunt probe's slope, -7.8154 against its -7.8186, an
independent replication of that record by a separate runner.

The Lorentzian profile behaved exactly as an analyticity-controlled exponent should.
Its three fits have coefficients of determination 0.99997, 0.99991, and 0.99933, its
measured exponents are 1.0095, 1.0344, and 1.0658 times the naive estimate of twice
the frequency times the pole distance, and its width scaling is 1.537 and 2.111
against predictions of 1.5 and 2.0. The sech-squared profile did not. Its ratios to
the same naive estimate are 0.5430, 0.6910, and 0.8098, drifting with width, and its
width scalings are 1.909 and 2.982 against the same 1.5 and 2.0.

The named error is the grid. Velocities were declared in absolute terms and applied
to every width, so the three widths were compared in different dynamical regimes and
the narrowest cells sat partly outside the adiabatic regime where the exponential
form is asymptotic, which is also why the only coefficient of determination below
the bar is the narrowest sech-squared cell at 0.9886. The cross-profile ratio test
inherited that contamination and cannot be read.

What the committed numbers already show once they are placed in the natural
variable. Writing the adiabaticity as the frequency times the pole distance divided
by the velocity, the Lorentzian exponents are -2.019, -2.069, and -2.132, a spread
of 5.4 percent about a parameter-free prediction of exactly minus two, while the
sech-squared exponents are -1.086, -1.382, and -1.619, a spread of 39 percent.

#### PF4-005b protocol (declared 2026-08-07, before the run)

Each cell is placed at a declared adiabaticity rather than a declared velocity, so
every width is compared in one dynamical regime. The declared adiabaticity grid is
0.9, 1.2, 1.5, 2.0, 2.5, and 3.0, and the velocity of each cell follows from it and
from that profile's own pole distance. In that variable the analyticity estimate is
a parameter-free prediction of exactly minus two.

Bars. B0, the timestep control, unchanged. B1, the exponential form holds in every
one of the six cells. B2, the Lorentzian exponent is width-universal, its three
fitted values agreeing within ten percent of their mean. B3, the Lorentzian exponent
matches the parameter-free prediction within fifteen percent at every width.

Findings, with expectations declared in advance from PF4-005's committed record so
this run can refute them. F1, the sech-squared exponent is not width-universal. F2,
the sech-squared exponent is smaller in magnitude than the prediction.

The named hypothesis for the difference, recorded and not tested here. The tilt that
generates the sech-squared force is a hyperbolic tangent, whose nearest singularity
is a simple pole at which the driving term diverges, while the tilt that generates
the Lorentzian force is an arctangent, whose nearest singularity is a logarithmic
branch point at which it diverges far more slowly. A constant-frequency estimate
should survive the milder singularity and fail at the stronger one. Testing that
would need a family that varies the strength of the divergence at fixed distance,
which is a later experiment.

**Readings, declared in advance.** If B2 and B3 hold, a constructible family has a
deterministic exponent fixed by the distance to the field's nearest complex
singularity, with no distribution present whose tail could be responsible, and the
summit question of PREREG-PF4-002 is answered for the per-crossing transfer. The
step from that transfer to an observable event rate is not taken here and remains
blocked by the cancellation the mechanism study measured, so no claim about a pair
rate follows. If B2 or B3 fails, no family has yet shown an analyticity-controlled
exponent and the summit stays open.

**Substrate.** Atlas Python, exploratory and unsealed,
`results/pf4-005b-analyticity.json`.

#### PF4-005b results (run 2026-08-07, record sha 8da5c1e9dca4...)

Verdict FAIL on one bar of four, with the two bars the summit turns on both passing
and one declared expectation refuted.

The Lorentzian family answered the question it was asked. Its exponent in the
declared adiabaticity variable is -2.0661, -2.0639, and -2.0607 across the three
widths, a spread of 0.26 percent, and each value sits 3.3 percent above the
parameter-free prediction of exactly minus two. Its exponential form is close to
exact, coefficients of determination 0.99984, 0.99983, and 0.99982. The timestep
control passed at 1.8e-13.

The declared expectation F1 is refuted, and that is the run's most useful result.
The sech-squared family is also width-universal once the widths are compared at
matched adiabaticity, its exponents being -1.0490, -1.0478, and -1.0462, a spread of
0.27 percent. PF4-005's 39 percent spread was entirely an artifact of the grid it
declared, not a property of the profile. Both profiles therefore carry an exponent
fixed by the adiabaticity built from their own singularity distance, and the
singularity distance is what makes the exponent width-independent.

What the two profiles do not share is the constant. The Lorentzian sits at the naive
value and the sech-squared sits at 0.524 of it. The sech-squared mean of -1.0477 is
close to minus pi over three, which is a resemblance and not a claim, because a
constant recognised after measurement is not a prediction. Testing it would require
deriving the constant from the singularity type before running, which is the open
question named in the PF4-005b declaration and is not answered here.

The bar that failed is B1, the exponential form, applied across both profiles at a
coefficient of determination of 0.99. The Lorentzian cells clear it by three orders
of margin and the sech-squared cells sit at 0.9886, 0.9887, and 0.9889, just under.
That shortfall is stable across widths and is itself informative, the suppression of
the sech-squared profile is close to but not exactly a pure exponential in the
adiabaticity, which is consistent with its nearest singularity being a simple pole
where the driving term diverges rather than a logarithmic branch point. The bar was
declared over both profiles when only one of them was predicted to be exactly
exponential.

#### The summit question, as it now stands

PREREG-PF4-002 asked whether any constructible family has a non-measure-tail
exponent. The answer is yes, and it is measured. The crossing is deterministic with
one declared initial condition, so no distribution exists whose tail could produce a
suppression. The exponent depends only on the adiabaticity built from the distance
to the field's nearest complex singularity, which makes it width-universal to a
quarter of a percent across a factor of two in width, for both declared profiles.
For the Lorentzian profile it matches a parameter-free prediction to 3.3 percent.
This is a dynamical exponent and it is not a measure tail.

Three limits are recorded with it. The observable is the per-crossing transfer and
not an event rate, and the step between them remains blocked by the cancellation the
mechanism study measured. The constant that multiplies the adiabaticity is not
predicted for the sech-squared profile and is left as a named open question. And
nothing here is sealed, so the result is exploratory and would need a
preregistration before it could carry a claim.

The campaign does not pursue the constant further in this arc. Two runs have already
corrected two declaration errors of mine, the grid in absolute velocity and a bar
applied to a profile it was not predicted to fit, and a third refinement aimed at a
constant that was recognised rather than predicted would be fitting the analysis to
a wanted answer.

#### PF4-006 gate protocol (declared 2026-08-07, before the run)

Section 6 of this document makes PF-5 and PF-6 mandatory gates before a
claim-bearing run. Those gates passed on the thermal Sauter family under
PREREG-PF5-002 and PREREG-PF6-002. The analyticity result uses a field profile
those gates never saw, an arctangent tilt with a Lorentzian force, in a
deterministic setting, so the gate content that applies is applied to it here
before anything about it is sealed.

What applies. The extended system is a canonical autonomous two-degree-of-freedom
Hamiltonian system in the evolution parameter, so the conservation content of PF-5
applies directly. The census content applies. The transfer must not depend on where
the field is centred, which is the translation content of PF-6, nor on the declared
entry point or timestep, which is what makes it a property of the crossing rather
than of the integration.

What does not apply, declared rather than quietly passed. The observer and detector
audit of PF-6 counts events at declared observer offsets, and these crossings
produce no events at any offset, so that clause is recorded not applicable. The
gauge clause is recorded not applicable as in PREREG-PF6-002, the profile declaring
no electromagnetic coupling. A clause with nothing to audit is not a clause that
passed, and the standing rule earned four times over in this campaign is that a
vacuous pass is not a pass.

Bars. G1, the conserved quantity of the extended system drifts by at most 1e-10
relative in every declared crossing. G2, the census is complete with no nonfinite
member. G3, shifting the field centre by the declared amounts changes the transfer
by at most 1e-10 relative. G4, moving the entry point half again further out and
halving the timestep each change the transfer by at most 1e-8 relative.

This run is the prerequisite for a preregistration and not a substitute for one.
Exploratory and unsealed, `results/pf4-006-gate.json`.

#### PF4-006 gate results (run 2026-08-07, record sha 42e2eb1923c7...)

Verdict FAIL on the entry-point clause, and the gate did the job it exists to do.
It found a defect in the observable's definition before anything about that profile
was sealed.

What passed. The conserved quantity of the extended system drifts by at most 8.6e-14
across every declared crossing, four orders inside its bar. The census is complete
with no nonfinite member and every crossing transmitted. Translation covariance is
exact to 8.8e-14, so the transfer does not care where the field is centred.

What failed. Moving the entry point from twenty widths to thirty changes the
transfer by 1.289, 1.295, and 1.291 percent at the three widths, against a bar of
1e-10. The changes are nearly identical across widths. The declared diagnosis is
that the arctangent tilt approaches its asymptote algebraically rather than
exponentially, so the field never fully turns off and a transfer measured from any
finite entry carries a tail contribution.

A second clause missed by a smaller margin and for a different reason. Halving the
timestep changes the transfer by about 3e-7 against the same 1e-8 bar. That is a
bar set tighter than the declared timestep can deliver and is a fault in the
declaration rather than in the profile.

The consequence for the summit result. PF4-005b measured its exponents at a span of
twenty widths, so those numbers carry this tail contribution. Because the
contribution is nearly common across widths it should move the fitted intercept far
more than the fitted exponent, but that is a hypothesis and not a measurement, and
no seal may rest on it until it is measured.

#### PF4-007 protocol (declared 2026-08-07, before the run)

Measure the convergence rather than assume a fix. A declared span ladder of 20, 30,
45, 65, and 90 widths is applied to one probe cell of each profile, and the
exponent itself is refitted at the nearest and furthest spans for every width of
both profiles.

Bars. S1, the Lorentzian transfer converges, its successive relative changes
decreasing along the ladder. S2, the sech-squared transfer is already converged, its
successive changes at most 1e-9, which is the control that the effect belongs to
algebraic tails. S3, the exponent is robust to the span, changing by at most one
percent between the nearest and furthest spans in every cell of both profiles. S4,
the width universality survives at the furthest span, the Lorentzian exponents
agreeing within two percent of their mean.

The reading and what it decides. If S3 and S4 hold, the summit result stands as
measured, the tail contribution lands in the prefactor rather than the exponent, and
a preregistration may declare the furthest span with a timestep bar set from the
measured convergence. If S3 or S4 fails, the exponent measured at twenty widths was
contaminated, PF4-005b's numbers must be reported as span-dependent, and the summit
answer weakens to a statement about one declared span rather than about the
crossing.

Exploratory and unsealed, `results/pf4-007-span.json`.

#### PF4-008 protocol (declared 2026-08-07, before the run)

The rehabilitation. The property that made the Lorentzian profile interesting was a
first-order singularity, and the property that broke its gate was an algebraic tail.
Those are separable, and the Gudermannian tilt separates them. Written as the
arcsine of a hyperbolic tangent it runs from minus one to plus one, its force is a
hyperbolic secant whose nearest singularity is a simple pole at pi over two times
the width, the same distance as the sech-squared family's double pole, and its tails
decay exponentially so the entry-point defect cannot arise.

That makes the comparison controlled. Two profiles, one distance, two orders. What
the distance fixes and what the order fixes are separated by construction rather
than by argument.

Two hypotheses, mutually exclusive and declared here before the run so the run
discriminates rather than confirms. H1, the distance is what matters, and the
Gudermannian exponent equals the sech-squared exponent of minus 1.04767 within five
percent. H2, the order matters, and the Gudermannian exponent equals the Lorentzian
exponent of minus 2.06356 within ten percent. Both references are from the committed
PF4-005b record. If neither holds that is recorded as a third outcome and the
question stays open.

Grid, disjoint from every prior run. Widths 1.5, 2.5, and 3.5, adiabaticities 1.0,
1.4, 1.8, 2.2, 2.6, and 3.2, timestep 2e-4, span twenty widths, with the
sech-squared profile rerun on the identical grid so the comparison is side by side
rather than across records.

Bars, with the gate content folded in because this profile has never been gated.
P1a, the conserved quantity of the extended system drifts by at most 1e-10. P1b,
moving the entry point half again further out changes the transfer by at most 1e-6
relative, which is the clause the Lorentzian failed at 1.3e-2 and which exponential
tails should now satisfy. P1c, halving the timestep changes it by at most 1e-5, a
bar set from the 3e-7 measured in PF4-006 rather than from optimism. P1d,
translation covariance at 1e-6. P1e, the census is complete. P2, the exponential
form holds at a coefficient of determination of at least 0.98, a bar low enough to
admit either profile's behaviour since the answer is not known in advance. P3, both
profiles are width-universal within two percent. P4, every transfer lies between
1e-12 and 1, so no fit rests on numerical noise.

**Readings.** If the bars hold and H2 holds, the exponent is fixed by the order of
the singularity as well as its distance, the Lorentzian's agreement with the
parameter-free value is reproduced by a profile that passes its gate, and the summit
result rests on a well-conditioned family. If the bars hold and H1 holds, the
distance alone fixes the exponent, the Lorentzian's differing value was the tail
contamination the gate found, and the summit statement narrows accordingly. Either
way the entry-point defect is gone and the seal binds to this profile rather than to
the one that failed.

Exploratory and unsealed, `results/pf4-008-pole-order.json`.

#### PF4-008 results (run 2026-08-07, record sha b0727e164dd5...)

The first execution of this runner was invalid and is recorded as such. It imported
a fitting helper that regresses against the reciprocal of the adiabaticity rather
than the adiabaticity itself, which is the named error, and it produced positive
exponents with poor fits for both profiles including one whose exponent is already
committed as negative. The dynamics were untouched by the error, so the quantities
that do not pass through the fit are identical in both executions. The runner was
corrected and the declared protocol rerun with no bar or design changed.

The rehabilitation worked. The clause the Lorentzian profile failed at 1.3e-2 is
passed by the Gudermannian profile at 5.7e-11, four orders inside its bar, and the
timestep and translation clauses pass at 4.9e-13 and 6.5e-15. Exponential tails
remove the entry-point defect exactly as the declaration predicted, and the census
is complete.

The discriminator answered, and it answered H2. The Gudermannian exponents are
-1.9333, -1.9286, and -1.9217 across the three widths, a spread of 0.61 percent, at
coefficients of determination of 0.9987. The sech-squared exponents on the identical
grid are -1.1028, -1.1015, -1.0997, a spread of 0.29 percent. The Gudermannian value
is 84 percent away from the sech-squared reference and 6.6 percent from the
Lorentzian reference, so H1 is refuted and H2 holds within its declared tolerance.

The reading. Two profiles whose nearest singularities sit at the same distance and
differ only in order carry different exponents, in the ratio 1.75. The distance
alone does not fix the exponent. The order fixes it too, and a first-order
singularity gives close to the parameter-free value of minus two whether it is a
pole, as here, or a branch point, as in the Lorentzian, while a second-order pole
gives about 1.1.

Two caveats belong beside that. The Gudermannian's clean value of -1.9279 sits 6.6
percent below the Lorentzian's -2.0636, and the Lorentzian's number carries the tail
contamination its gate found, so the well-conditioned value is the smaller one. And
the sech-squared exponent measured -1.1013 on this grid against -1.0477 on
PF4-005b's, a 5 percent difference across two disjoint grids, which is larger than
either run's internal spread and says the exponent is not quite grid-independent at
this precision.

The verdict is FAIL, on the conservation bar alone. The Gudermannian cells drift by
1.9e-10 against a bar of 1e-10, while the sech-squared cells on the same grid drift
by 9e-13. The bar was set from the Sauter family's 8.6e-14 and is too tight for a
broader force at this timestep. This is a numerical bar missed by a factor of two,
not a physical failure, and the principled repair is a smaller timestep rather than
a larger bar, since fourth-order integration should bring the drift to about 1e-11
when the step is halved.

#### PF4-008b, the remaining step

Identical in every declared object and bar, with the timestep halved to 1e-4 so the
conservation bar is met by integration rather than by relaxation. Nothing else
changes. If it passes, the seal binds to the Gudermannian profile, which has now
cleared the entry-point clause the Lorentzian could not, and the preregistration's
primary bar is the width universality that both well-conditioned profiles have shown
at better than one percent.

#### PF4-007 results (run 2026-08-07, record sha e12453effa2f...)

Verdict PASS on all four items, after the same reciprocal-fit import that
invalidated PF4-008's first execution was found in this runner and corrected. The
diagnosis of the gate failure is confirmed. The Lorentzian transfer's successive
relative changes along the span ladder are 1.278, 0.586, 0.130, and 0.015 percent,
falling steadily, while the sech-squared transfer changes by at most 1e-13 across
the same ladder, so the effect belongs to algebraic tails and not to the method. The
exponent is far more robust than the transfer, changing by at most 0.28 percent
between the nearest and furthest spans, and the Lorentzian width universality
survives at the furthest span with a spread of 0.36 percent. The tail contribution
lands in the prefactor and leaves the exponent, which is what the seal turned on.

#### PF4-007, a bookkeeping defect and its correction

The record committed as `results/pf4-007-span.json`, sha
e12453effa2f, was produced by the runner before the reciprocal-fit
import was found, so its exponent items are invalid. Its Lorentzian
slopes are positive, which is the signature of that defect. It
stays in the record unedited.

The corrected rerun was left in the working tree and never
committed, so it was invisible to anything reading the repository.
It is now committed separately as `results/pf4-007b-span.json`,
which supersedes the invalid record and names it. The runner writes
to the new path so that a rerun can no longer overwrite a committed
record's file.

What changes and what does not. The span ladder itself does not
pass through the fit, so the convergence numbers are identical in
both records and the diagnosis of algebraic tails stands. The
exponent items move slightly, the worst relative exponent change
from 0.00278 to 0.00234 and the Lorentzian spread at the furthest
span from 0.00356 to 0.00359, and both remain far inside their
bars, so no verdict changes.

The defect is mine and it is the second of its family today. A
committed record was produced by a runner that was later found
defective, and the correction was then left uncommitted where the
paper could not see it. The rule the campaign already applies to
declarations now applies to records as well, a rerun writes to a new
path and never over a committed one.

#### PF4-008b and PF4-008c results (2026-08-07)

PF4-008b refuted its own declared repair. Halving the timestep left the conservation
drift unchanged at 1.1e-10 and 2.0e-10, so the drift was not integration error and
the repair was wrong.

PF4-008c diagnosed it exactly. A hyperbolic tangent of twenty rounds to exactly one
in double precision, so the arcsine form of the Gudermannian tilt saturates while
its own derivative is still 2.6e-9 at that point. The two become mutually
inconsistent in the tails, and because the Hamiltonian carries the tilt the
inconsistency appears as an apparent conservation violation. The predicted size was
1.115e-10 against a measured 1.12e-10. The sech-squared profile is immune because
its force at the same point is 1.7e-17.

Evaluating the tilt so that it saturates together with its derivative dropped the
drift from 1.12e-10 to 7.6e-14, a factor of fifteen hundred, and moved the exponent
only in its seventh digit, which is what the diagnosis predicted since the defect
enters the transfer at a relative 1e-8. PF4-008c passes all eight of its items, and
the discriminator's answer is unchanged, H2 holds and the singularity's order fixes
the exponent alongside its distance.

#### PREREG-PF4-009, the sealed result (record sha 6a4d6a28d309...)

Verdict PASS on all eight of its items, which the sealed document groups into six bars. The four fitted exponents on a grid disjoint from
every prior run are -1.929735, -1.924383, -1.916823, and -1.909268 across widths
spanning a factor of 2.56, a spread of 1.07 percent against a declared bar of two
percent. Coefficients of determination are 0.9989 or better in every cell. The
extended Hamiltonian drifts by at most 3.7e-13 against a bar of 1e-11, entry-point
independence measures 9.2e-9 against 1e-7, every transfer lies inside the declared
signal window, and no cell is nonfinite or folds.

**The summit question of PREREG-PF4-002 now has a sealed answer.** A constructible
family has a suppression whose exponent depends only on the adiabaticity built from
the distance to the field's nearest complex singularity, and is therefore
width-independent. Each crossing is deterministic with one declared initial
condition, so no distribution exists whose tail could produce the suppression. The
exponent is dynamical and it is not a measure tail.

The non-claims of the registration bind the reading. The observable is the
per-crossing transfer and not an event rate, and the step between them remains
blocked by the cancellation the mechanism study measured. The constant multiplying
the adiabaticity is not claimed. Nothing here is a claim about quantum field theory
or about any physical process.

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

#### PF-8 results (run 2026-08-06, record sha b375000e2a70...)

Verdict PASS on all four bars, exploratory and unsealed, runner at code commit
84af03a, record `results/pf8-decay-gate.json`.

**D1, complete-observer parity, zero odd events.** Four deterministic members
audited on 441 generic levels and 400 kept thermal polylines audited on five
levels each. The complete observer's unsigned branch count took only the values
1 and 3, and every change between adjacent levels was -2, 0, or +2. Zero odd
events, zero parity failures on either arm. Fold counts 4, 2, 2, 2, all even.
The three-branch fibers are narrow, the excursions measuring 0.005314, 0.007744,
0.04449, 0.025922, and 0.000253 in observed time, which is why the ladder places
levels inside them.

**D2, signed count, zero failures.** The frozen path-degree rule reported zero
failures on all 441 deterministic levels and all 2000 thermal polyline checks.
The signed count on every arm A member was exactly +1 at every level, spread
zero, so no fold moved it. Folds make orientation charge only in cancelling
pairs, measured here rather than assumed.

**D3, the blind consumer.** Across 441 observations the consumer blind to
branches with u in [-0.70, +0.70] failed to record 147 crossings and read a
parity different from the complete observer on 129 observations, a flip fraction
of 0.2925. Sixty-three of those were apparent decay events, adjacent levels
across which the blind count rose by exactly one, one particle becoming two with
missing energy. Every single apparent count matched the detector-model
prediction exactly, zero mismatches on 441 observations, computed by an
independent route from the observer's own record. The P = 0.90 member is the
extreme case, all three branches of its zigzag lie inside the window, so that
consumer sees nothing at all where the complete observer sees three.

**D4, anti-vacuity.** Every member folded, the ladder resolved 46 multibranch
levels, the consumer hid 147 crossings, and the thermal census contained 1963
reversing members. The thermal census summed exactly to 20000 with zero missing
trajectories and a maximum relative energy residual of 6.3e-7 against the PF-5
bar of 1e-5.

**PF-8b, lifetimes, memorylessness fails.** The expected negative is what the
run measured. Pooling the four cells, 1963 first-reversal times have mean proper
time 18.92 and standard deviation 3.01, a coefficient of variation of 0.159
against the value 1 that a memoryless exponential requires, so the deviation is
-0.841. Per cell the coefficient of variation is 0.0526, 0.0530, 0.0694, and
0.0764, and the pooled figure is larger only because the four cells have
different means. The sup deviation between the empirical survival curve and the
exponential whose mean matches it is 0.506 pooled and near 0.57 in every cell,
which is most of the available range. Shifting to the measured onset does not
rescue it, the shifted coefficient of variation is 0.494 pooled and the shifted
sup deviation 0.232. An exact cross-check on 32 first-reversal steps read from
the kept polylines gives mean 18.94 and coefficient of variation 0.188, matching
the binned ladder. First-reversal time in this family has a hard onset set by
when the trajectory reaches the slab and a narrow spread after it, which is not
a hazard at all. This is the PF-2 lesson again, fold statistics are borne by the
declared measure.

**Can folding account for particle decay.** No for the decay everyone means, yes
for a decay nobody can distinguish from it without seeing every branch.

What is excluded. A same-species one-to-two decay is a change of exactly one in
the observed branch count. Every fold changes that count by exactly two. Across
441 generic levels on four folding worldlines the measured change was never
anything but -2, 0, or +2, and the signed count never moved. So a complete
observer of a continuous worldline under a generic projection cannot see one
particle become two. This is not a limit of the search, it is parity.

What is imitable. The one-to-three zigzag, parent plus created pair, which the
run found at 46 levels where the neighbouring levels showed one branch. Folding
imitates pair creation because pairs are what folds make, and it imitates decay
only by adding a pair to a branch that was already there.

What the blind consumer showed. Declaring one branch class invisible turns the
one-to-three event into a one-to-two reading, and the run produced 63 of them.
Their apparent counts were predicted exactly by the consumer's detector model,
zero mismatches, which is the PF-6 lawful-observer clause holding for decay as
it did for particle number. Apparent decay in this model is therefore a
measurement of what the consumer cannot see, never a property of the worldline.
That is the same structure as the PE track's invisible leak, and it is the
phenomenology of decays with unobserved neutrinos without any of the physics.

Caveats. Arm A is four members and one declared blind window, so the counts of
apparent decays are counts on this ladder and not a rate. The frozen census
stops a member at its first reversal, so the kept thermal polylines are half
worldlines and carry the endpoint form of the parity statement rather than the
even-fold-count form, which is why arm B's parity clause was written against the
endpoints before the run. Nothing here is sealed.

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
