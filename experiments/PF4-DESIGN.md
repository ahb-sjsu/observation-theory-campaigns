# PF-4 design: the sealed Schwinger scaling challenge

**Status:** design draft, unsealed, non-claim-bearing. This document
extends CAMPAIGN.md section PF-4 into a runnable design. No candidate
model is declared here; declaring one and sealing it is a separate,
later act. Nothing below is a physics claim.

## 1. Question

Does a candidate hidden-manifold dynamics predict the nonperturbative
field, mass, and charge dependence of pair production? For a constant
field the semiclassical target is

log Gamma = const - pi m^2 / |qE|

up to known prefactors. PF-4 is the first experiment in the campaign
capable of supporting a physical pair-production claim, and it is
gated behind everything the campaign has sealed so far.

## 2. What PF-4 inherits

The instrument net is sealed (PF0-FREEZE-001) and the entropy and
quantum instruments are sealed (PEQO-FREEZE-002). Three results shape
this design directly.

1. **PF-2 (negative-control shape).** Fold counts in a generic bounded
   Hamiltonian are set rigidly by the dynamics and the
   initial-condition measure (every member of a 10^4 ensemble produced
   exactly 12 folds). Exponentially suppressed rates therefore require
   large-deviation structure, and the anti-circularity contract forbids
   inserting it. The expected outcome of PF-4 remains a disciplined
   negative.
2. **PF-3 (replication).** A published classical pair event was
   replicated exactly, and its reversal threshold was proved to sit on
   the pole of the Cayley transform that its impulsive midpoint closure
   applies to the kick generator, while continuous accumulation of the
   same generator conserves a hyperbolic form and never reverses.
3. **PF-3 corollary (the frozen-kick null family).** Any interaction
   treated as a frozen-point kick, accumulated continuously, provably
   produces zero reversals at every coupling. A candidate whose
   reversals survive only because its interactions are closed
   impulsively is reproducing the Cayley pole, not a dynamical rate.

## 3. The closure-prescription clause

This clause is a contract. A violation voids the run, not the bar.

- **C1, continuous integration.** Candidate dynamics must be integrated
  continuously through every interaction with a smooth, resolved
  integrator. Impulsive, algebraic, midpoint, or Cayley-style closures
  of interactions are forbidden as dynamics. No interaction may be
  replaced by a solved scattering map.
- **C2, preregistered prescription.** The integrator family, step
  policy, event-location method, and any interaction smoothing are
  declared in the sealed preregistration, with their tolerances.
- **C3, prescription-pair control.** Every claim-bearing rate is
  measured under two independent prescriptions declared in advance
  (an adaptive event-locating integrator and a fixed-step symplectic
  integrator at minimum). The two rates must agree within the sealed
  tolerance at every grid point used for fitting; disagreement
  classifies the rate as prescription-borne and voids the point.
- **C4, refinement stability.** Rates must be stable under step
  halving and under smoothing-width halving within sealed tolerance,
  with the stability measured on the same trajectories that enter the
  fit, not on a side sample.
- **C5, the Cayley trap (positive control for the artifact detector).**
  Alongside the candidate, the campaign runs a deliberately impulsive
  variant of a null model known to have no continuous reversal, and
  the analysis pipeline must flag its manufactured threshold as
  prescription-borne under C3/C4. If the pipeline fails to catch the
  planted artifact, the pipeline is invalid and no candidate result
  may be read.

C5 turns the PF-3 finding into an instrument check. The artifact we
discovered becomes the artifact we plant.

## 4. Candidate model family (constraints, not a declaration)

The candidate is declared at seal time, not here. It must satisfy the
CAMPAIGN.md section 3 anti-circularity contract in full, plus:

- reversals must arise from resolved, trajectory-varying field
  structure, since frozen-point kicks provably cannot produce them
  (the PF-3 null family);
- the initial-condition measure is declared before the sweep and is
  not a function of E, m, or q beyond declared physical scaling;
- the Schwinger exponent, any exp(-a/x) ansatz in the model's inputs,
  and any stopping rule correlated with reversal are forbidden inputs;
- mass, charge, and field enter as declared parameters of the
  dynamics, not of the sampling.

Plausible families to evaluate before sealing include SHP-type
dynamics with resolved (non-impulsive) field configurations and
thermal or wave-packet hidden ensembles whose escape structure is not
inserted by hand. Whether any such family produces exponentially
suppressed reversal at all is precisely what the pilot phase measures.

## 5. Statistical design

- **Grid.** Held-out contiguous ranges in E, m, and q, plus
  combinations absent from training, per CAMPAIGN.md. Training may
  calibrate one overall time/volume scale and at most one prefactor.
- **Estimator.** The reversal rate per trajectory per unit tau,
  converted to a rate per four-volume with the declared normalization.
  Every trajectory is counted in the denominator, including no-fold,
  escape, recrossing, and numerical-failure outcomes (PF-5
  accounting). Numerical failures above a sealed fraction void the
  grid point.
- **Alternatives.** The candidate law log Gamma = c - pi m^2/|qE| is
  fit against the preregistered alternatives of CAMPAIGN.md
  (polynomial threshold, Arrhenius in a different variable, power
  law, penalized spline) by held-out log-likelihood with declared
  complexity penalties.
- **Rare events.** No importance sampling, biasing, or adaptive
  seeding unless declared at seal time with its own null-model
  validation; the default design is brute-force ensembles sized by
  the pilot.
- **Stopping.** Trajectory counts per grid point are fixed at seal
  time from pilot variance estimates. No sequential peeking.

## 6. Witnesses and falsification bars

Primary witnesses: held-out log-likelihood ranking; slope of
log Gamma against m^2/|qE| with its confidence interval; residual
structure against every declared covariate; C3 prescription agreement
and C4 refinement stability at every fitted point.

The candidate fails if any of the following holds:

- the held-out slope confidence interval excludes -pi;
- a preregistered alternative predicts held-out data better under the
  declared penalty;
- the apparent exponential is produced by an initial-condition weight
  or stopping rule equivalent to the target law (audit per EG-2
  style equivalence check);
- any fitted point is prescription-borne under C3 or unstable under
  C4;
- the C5 planted artifact is not caught by the pipeline (this voids
  the run rather than failing the candidate).

A candidate that produces no reversals at all, or rates without
exponential structure, is a clean negative for that family and is the
expected outcome.

## 7. Substrate and resource envelope

Pilot and reduction on Atlas (MATLAB event-located integration for
the adaptive arm, Python fixed-step symplectic for the other,
cross-checked under the sealed instrument bars). Production ensembles
on NRP as CPU swarm Jobs (one CPU, two gigabytes, self-contained via
ConfigMap, bounded live working set, every Job finite), with the
politeness bounds of the campaign's standing cluster policy. Rate
sweeps never run on the laptop. The four campaign bounds (active
workers, Kubernetes objects, I/O pressure, unreduced evidence) apply,
and a policy violation is a failed experiment.

## 8. Evidence and labels

Every trial writes the standard append-only record with hashes,
commit, dependency versions, prescription identity, and outcome
counts. The run is claim-bearing only under a sealed preregistration
(PREREG-PF4-001, future) whose blob hash joins the ledger. Possible
labels: [refuted], [demonstrated-in-model] for the candidate family
only, or the clean negative. No outcome supports a claim about
physical spacetime; CAMPAIGN.md section 9's ceiling stands.

## 9a. Pilot outcome (2026-08-04, exploratory, results/pf4-pilot.json)

The candidate-family pilot ran four iterations, each failure preserved
in the code's version notes: the unbounded coupling did secular work
(drift 0.23), the slab fix exposed an initialization transient that
reversed everything, the shifted-well fix exposed a deterministic
crossing kick, and the final design splits regimes with a per-cell
thermal-free probe. Findings from the completed sweep of the Sauter
family (18 cells, 5 x 10^4 trajectories each, drift uniformly at
6 x 10^-7, eleven decades under the v1 worst):

1. **The family has a critical field.** Above a P-dependent threshold
   the deterministic crossing kick alone reverses the event (with
   runaway feedback, since a slowing event absorbs more kick); below
   it reversal is fluctuation-driven. The deterministic minimum of the
   time momentum, measured by the probe at every cell, maps this
   manifold.
2. **The sub-critical transition is razor sharp.** At gap 0.5 the
   fraction moves from 2.8 x 10^-4 to 0.91 between fields 0.65 and
   0.80, three decades in a fifteen-percent field step. Only two of
   eighteen cells landed in the measurable band, so the preregistered
   grids must be adaptive in the field (or parameterized along the
   measured critical manifold), and fixed rectangular grids will
   mostly buy bounds.
3. **Two-point diagnostic, post hoc and exploratory.** The two
   measurable cells satisfy -log f proportional to (d/E)^2, with d
   the probe's deterministic minimum (the effective gap), to two
   percent (ratio 2.03 measured against 1.99 predicted), while the
   Schwinger-shaped axis d^2/E misses by fifty-seven percent and the
   bare-gap Gaussian axis (P/E)^2 by forty percent. Two points prove
   nothing, but they point where the family is going: suppression
   organized by a Gaussian measure tail in the effective gap, which is
   the measure-set exponent PF-2 anticipated, not the Schwinger form.
4. **A control lesson.** The prescription-pair and step-halving
   controls agreed exactly but vacuously, because the declared control
   cell produced zero counts under all three prescriptions. Sealed
   controls must sit on cells verified measurable, or they certify
   nothing.

Implication for sealing: the first preregisterable claim is now
concrete and negative-shaped. In the Sauter family, held-out
suppression follows the effective-gap Gaussian axis and excludes the
Schwinger axis. Demonstrating that with an adaptive grid, measurable
controls, and the C1-C5 clauses would be the campaign's disciplined
negative for this family, and the effective-gap parameterization is
the design vehicle.

## 9b. Governed outcome of PREREG-PF4-001 (2026-08-04, sealed verdict)

The first sealed run returned **neither-axis**, exactly the third
branch the preregistration defined. All twenty probe-placed cells
landed in the measurable band (the adaptive manifest worked), drift
was uniform at 6e-7, and both C3/C4 controls agreed per-member exactly
(z = 0.00 under RK4 and under step halving). The fitted effective-gap
slope beta = 41.2 confirmed the pilot's two-point prediction of 41.6,
and the G model beat the Schwinger-shaped model by 3.28x on held-out
weighted error. But the sealed bars were not met: MSE_G = 81.2 against
the bar of 4, because at 5 x 10^4-trajectory precision the residual
gap-dependence of the suppression at fixed d/E is many binomial sigma;
and the S model, though worse, was not 4x worse. The claim neither
passed nor was refuted, and the record carries both residual sets.

Reading. The effective-gap Gaussian axis is a few-percent-accurate
organizer of the family and not a law; the family's true exponent has
structure beyond any single (P, E) combination, with suppression
deepening in the gap at fixed d/E. The pilot-level conclusion that the
Schwinger form does not organize this family stands descriptively but
did not earn a sealed label. Any second attempt must either model the
gap-dependence explicitly (a two-variable exponent) or set bars
against model error rather than binomial error, and must say which
before running. Evidence: results/prereg-pf4-001.json.

## 9. Open design questions (must close before sealing)

0. **Standing requirement for any second attempt (owner-imposed,
   2026-08-04).** A second sealed attempt on this family must either
   model the two-variable structure explicitly (an exponent depending
   on more than one combination of P and E, for example the
   effective-gap axis plus a declared gap term) or set its bars
   against model error rather than binomial error, and the
   preregistration must declare which of the two it does before any
   governed run executes. PREREG-PF4-002 does not exist until this
   choice is made in writing.
1. Which candidate family is worth the first seal. ANSWERED by the
   pilot (section 9a): the Sauter-slab energy-transfer family is
   viable, rare-event generating, and clean; its measured structure
   (critical manifold, effective gap, sharp transition) now shapes the
   prereg. The remaining construction question is whether any family
   exists whose exponent is NOT a measure tail, which is the actual
   Schwinger question.
2. The four-volume normalization of the rate in a hidden-parameter
   theory (per tau, per t, per worldline, per detector window) must
   be declared once and defended, since the target law's prefactor
   convention depends on it.
3. The C3 tolerance. Too tight and honest prescriptions disagree on
   rare-event tails; too loose and the clause has no teeth. The pilot
   must measure inter-prescription scatter on a null family first.
4. Whether m and q can be varied independently in a classical
   candidate without a quantization convention linking them, or
   whether the held-out grid must treat m^2/|qE| as the only
   physical axis, weakening the covariance tests.
5. How large the ensembles must be to bound a slope near -pi with a
   confidence interval tight enough to exclude the alternatives, at
   rates that may span several decades. This is a pilot-variance
   question and may be the binding cost constraint.
