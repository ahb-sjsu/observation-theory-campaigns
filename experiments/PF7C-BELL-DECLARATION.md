# PF-7c declaration: the Bell ceiling on the sealed PF4-009 dynamics

Written and committed before the run. Bars are numerical and fixed here. The
verdict is computed by `python/pf7c_bell_dynamics.py`.

PF-7a stands as VOID, PF-7b as PASS. This run replaces PF-7b's synthetic
orientation source with the hidden measure the sealed family actually produces,
which is the only part of the question PF-7b left open.

Binding inheritance. PREREG-PF4-009's non-claims apply here unchanged. Nothing
in this run is a claim about quantum field theory or about any physical process.

## 1. What PF-7b actually established, corrected

PF-7b returned PASS 7/7. On preparing this declaration, two of its bars were
found to be structurally forced rather than measured, and that is recorded here
rather than left standing.

**B2 was near-vacuous.** With `A = sign(lambda . qa)` and `B = -sign(lambda . qb)`,
matched settings give `A . B = -1` identically for ANY measure. The measured
`E(0) = -1.000000` in all sixteen cells therefore tested the response rule, not
the fold's parity. The statement that signed count zero buys exact
anti correlation is a property of the model as constructed and PF-7b did not
test it. **B1 and B4 were already declared code checks.** So of PF-7b's seven
bars, three carried no information, and the informative ones were B0 and B0b,
the instrument, B3, the angular law, and B5, the blind consumer.

This is the fifth instance of the programme's standing rule biting, and the
first where the vacuity was found by writing the next declaration rather than by
a failed bar.

## 2. The source, harvested not posited

`pf4_009_run.run_cell` integrates `(t, pt, u, pu)` with `dt/dtau = pt` under the
Gudermannian tilt, and returns only the residual oscillator energy. PF-7c uses a
harvesting twin that returns the exit oscillator state as well. The hidden
variable is the exit phase

```
phi = atan2(pu / OMEGA_U, u - u_star)
```

taken at the declared exit, so its distribution is whatever the sealed dynamics
produces. This is the fold's own measure rather than a chosen one.

**Structural limitation, stated in advance.** The manifest starts every
trajectory at `u = u_star, pu = 0`, so the only freedom is kappa and `phi` is a
deterministic function of it. The hidden variable is therefore one dimensional,
a circle, not the sphere PF-7b swept. The P0 ceiling is a theorem for any
measure in any dimension, so this cannot change the ceiling. What it can change
is the angular law, which is what this run is for.

## 3. Bars

**D0, instrument live, per cell.** The PR box arm must give S > 2.0 in every
cell. Safe as a per-cell bar because it carries no geometry. Gates the run.

**D1, the measure must vary, the gate that matters here.** PF4-009's result is
that per-crossing transfer is exponentially suppressed, so the oscillator may
barely move and the exit phase may be near a point mass. A degenerate hidden
variable makes every correlation deterministic and the Bell question empty.
Bar: circular variance `1 - |mean(exp(i phi))| >= 0.05`, pooled AND for each of
the four widths. **If D1 fails the run is VOID for vacuity and no other number
here is reported as evidence.** This bar exists because the programme has passed
four vacuous gates and this is the shape they take.

**D2, the ceiling, a CODE CHECK.** P0 all trials counted `S <= 2 + 3 sigma` in
every cell. A theorem for any measure. Carries no evidence about folds.

**D3, matched-setting correlation, a CODE CHECK.** `|E(0)| >= 0.99`. Recorded as
forced by the response rule, per section 1, and retained only to detect a coding
error.

**D4, the conservation signature, made falsifiable.** A declared mispairing
fraction `m` is applied, in which a fraction of events carry same-sign rather
than opposite-sign charge, as a 1->3 zigzag miscount would produce. Prediction
fixed now: `E(0) = -(1 - 2m)` within 0.01, at `m = 0.0, 0.1, 0.25, 0.4`. This is
the bar D3 should have been, because it can fail.

**D5, the discriminator, the informative bar.** Using the parent harness's own
comparison, `rms_vs_scaled_sawtooth < rms_vs_quantum` in at least 4 of the 5
cells (four widths plus pooled). `max_gap_vs_quantum` is REPORTED as a
distribution and not barred, because PF-7a passed such a bar by 0.0011.

**D6, no signalling residual <= 0.01** in P0. A code check.

**D7, the blind consumer.** The 1->3 zigzag arm must give `S_postselected > 2.0`
while `S_all_counted <= 2 + 3 sigma`.

**D8, the dynamics twin.** The harvesting integrator must reproduce
`pf4_009_run.run_cell`'s `e_res` to `<= 1e-12` on the declared six-kappa
manifest at all four widths. Measured 0.000e+00 in the unsealed probe; repeated
inside the record so the harvest is auditable.

## 4. Fixed configuration

```
SEED            20260808
PROFILE         gudermann              PF4-009 sealed family
L_GRID          1.8, 2.8, 3.8, 4.6     as sealed
KAPPA_RANGE     1.05 to 3.05           the sealed endpoints, sampled uniformly
N_SAMP          1024 per width         4096 harvested phases total
DT              1e-4                   as sealed
SPAN            20.0                   as sealed
N_DRAW          200000 per context
N_ANG           37
MISPAIR_GRID    0.0, 0.1, 0.25, 0.4
ZIGZAG          0.35
DETECTOR_SHARP  3.0
D1_CIRCVAR_BAR  0.05
D4_TOL          0.01
D5_MIN_CELLS    4 of 5
D6_BAR          0.01
D8_BAR          1e-12
```

`N_SAMP` was set from the unsealed timing probe, ~110 s fixed plus ~0.24 s per
sample per width, so 1024 per width is about 24 minutes for the harvest. No bar
was informed by that probe.

## 5. Interpretation, fixed in advance

If D1 passes and D5 shows the scaled sawtooth, the recorded result is that the
fold's OWN measure, not a chosen one, still yields a classical angular law, and
PF-7's interpretation clause applies. The model is capped as a classical
representation.

If D1 fails, the recorded result is that the sealed family's exit phase is too
concentrated to pose the question, which is itself informative about the family
and is reported as a vacuity, never as a ceiling.

If D5 fails toward the quantum curve, that is not a Bell violation, because D2
forbids one. It would mean the sealed measure is shaped unlike a generic local
model and the next question is which feature of the dynamics does that.
