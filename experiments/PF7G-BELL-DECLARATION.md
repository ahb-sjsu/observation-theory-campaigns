# PF-7g declaration: the Bell ceiling

Written and committed before the run. Bars are numerical and fixed here. The
verdict is computed from the data by `python/pf7_bell_ceiling.py` and is not
written in this file.

Status: declaration, unsealed, non-claim-bearing until the run records.

## 1. Question

PF-7 asks whether the model reproduces more than a classical worldline picture.
Its declared targets are scalar versus spinor rates, multipair statistics, Pauli
blocking, interference, and backreaction. This declaration adds one target,
entangled pair correlations, and it is added because it is the only one of the
set with a theorem behind it rather than a modelling comparison. Bell's theorem
is exactly the statement that separates classical worldline pictures from
quantum ones, so it converts PF-7's interpretation clause, that failure caps the
model as a classical representation, into a measured quantity.

The fold makes pairs. PF-8 states the reason, a fold changes the observed
unsigned branch count by exactly two and the signed count by exactly zero, by
Whitney genericity. A pair whose members carry opposite charge and a shared
hidden orientation is the natural fold analogue of an emitted pair, so the
question is whether such a pair can carry the correlations of a singlet.

## 2. What is already known, and why one obvious bar is nearly vacuous

`geometric-observation/experiments/bell_geometry_audit.py` (GO-P-2026-057) states
in its own header that the P0 null is a theorem. With a setting independent
source, strictly local responses, and every trial counted, the pointwise bound
needs only that outcomes lie in [-1, 1], so S <= 2 for ANY source law rho.

That has a consequence this declaration records in advance. **The fold's
particular hidden distribution cannot change the P0 result.** Declaring "the
fold obeys S <= 2" and then passing is not evidence about folds, it is a
restatement of the theorem and a check on the code. The programme has been
burned four times by bars that could not fail, C-7b by saturation, C-8 by a
pinned quantity, C-3c N3 and N5 by barring quantities the substrate varies by
design. The standing rule from those is that before believing a bar of the form
"X predicts Y", require a prior bar that Y varies.

So B1 below is retained as a code check and is labelled as one. **The
informative content of this run is B2, B3, and B5**, which measure the SHAPE of
the fold's angular law and the size of the blind consumer loophole. Those can
fail.

## 3. Construction

The hidden variable is the worldline orientation at the fold, a unit vector on
S^(d-1). The pair's two branches carry opposite charge, charge being
sign(dt/dtau) under the PF-5 rule, which is the signed count zero statement. The
responses are the local sign rules already in the audit harness,
A = sign(lambda . a) and B = -sign(lambda . b), so the fold's parity structure
supplies the anti correlation and nothing else is inserted by hand.

Arms are the harness's own, unmodified in meaning:

- P0 every premise intact, setting independent source, local responses, every
  emitted trial counted, non detection an explicit third outcome 0
- P1 outcome accounting broken, post select on coincidence
- P2 measurement dependence, source law depends on the settings
- P3 locality broken, Alice's response reads Bob's setting

## 4. Bars

**B0, anti-vacuity, the instrument must be able to see a violation.** Each of
P1, P2, P3 must give S > 2.0. If any control fails to exceed the bound the
instrument is not demonstrated live and every other number here is void. This
bar gates the run.

**B1, the ceiling, labelled a CODE CHECK not a discovery.** P0, all trials
counted, must give S <= 2 + 3 sigma_finite at every configuration, with
sigma_finite the binomial standard error at the declared trial count. Predicted
to pass by theorem. Recorded because a failure would mean the fold source or the
response rule silently breaks a premise, which is the only way this bar carries
information.

**B2, the conservation signature, what the fold does buy.** With complete
detection, matched settings must give |E(theta = 0)| >= 0.99. The fold's signed
count zero should produce near exact anti correlation, which is the half of the
singlet that looks quantum.

**B3, the discriminator, what the fold does not buy.** Over theta in [0, pi],
sweeping the full angular law rather than scoring one CHSH value:

- max over theta of |E_fold(theta) - (-cos theta)| >= 0.20, the fold departs
  from the quantum curve
- mean over theta of |E_fold(theta) - sawtooth(theta)| <= 0.05, where
  sawtooth(theta) = -(1 - 2 theta / pi), the fold follows the classical local
  sign law

B3 is the bar that can fail in an interesting direction. If the fold's angular
law were closer to -cos theta than to the sawtooth, the fold would be carrying
structure a generic local model does not, and that would be a real finding about
folds rather than about Bell.

**B4, no signalling residual <= 0.01.** A code check on locality in P0.

**B5, the blind consumer, tying PF-7 to PF-8.** A declared detector model whose
efficiency depends on lambda and the LOCAL setting only is run, and its post
selected S is reported. PF-8's lawful observer clause applies unchanged, an
apparent violation under blindness must be predicted by the detector model. The
bar is that S_postselected > 2.0 while S_all_counted <= 2, demonstrating that
the loophole is reachable in this model. Apparent quantum correlation, like
apparent decay, is then a measurement of consumer blindness and never a property
of the worldline.

## 5. Fixed configuration

Declared before the run.

```
DIMS            3, 8, 32, 128
N_TRIALS        200000 per context
N_CONFIGS       72          setting geometries, as in GO-P-2026-057
THETA_GRID      37 points, 0 to pi inclusive
SEED            20260808
CHSH_ANGLES     the registered near pi/4 geometry
DETECTOR_SHARP  3.0         B5 blind consumer only
B0_BAR          2.0         each of P1, P2, P3
B1_BAR          2.0 + 3 sigma
B2_BAR          0.99
B3_QUANTUM_BAR  0.20
B3_SAWTOOTH_BAR 0.05
B4_BAR          0.01
```

## 6. Interpretation, fixed in advance

If B0 passes and B1 holds and B3 shows the sawtooth, the recorded result is that
**the fold reproduces the conservation signature of a pair and not the
contextual one**, and PF-7's interpretation clause applies as written, the model
is capped as a classical representation. That is a negative for folding as an
account of entanglement and it is the expected outcome.

The residue worth keeping either way is quantitative, the measured distance
between the fold's angular law and the quantum curve, which is the size of the
gap a fold would have to close.

If B3 fails in the direction of -cos theta, the run is not evidence of a Bell
violation, because B1 forbids one. It would instead mean the fold's hidden
measure is shaped in a way a generic local model is not, and the next question
would be which feature of the fold does that.
