# PF-7h declaration: the Bell ceiling, corrected instrument

Written and committed before the PF-7h run. Bars are numerical and fixed here.
The verdict is computed from the data by `python/pf7b_bell_ceiling.py`.

Supersedes the bar structure of `PF7-BELL-DECLARATION.md` (PF-7g). It does not
supersede PF-7g's record, which stands as a VOID with its two declaration
errors named, per the programme's practice of keeping honest negatives.

## 1. What PF-7g got wrong, and how it was found

PF-7g returned VOID_INSTRUMENT_NOT_LIVE. Both failures were declaration errors,
not results about folds.

**B0 barred every cell on a quantity the substrate varies.** PF-7g required each
of P1, P2, P3 to exceed 2.0 at every one of sixteen configurations. Measured,
they fire 14/16, 15/16 and 10/16. This is the same rule the programme has now
learned four times, most explicitly at C-3c and C-6, and PF-7g quoted the rule
in its own section 2 before breaking it in section 4.

**B3b compared against the unscaled sawtooth.** The parent harness compares
`rms_vs_scaled_sawtooth` against `rms_vs_quantum`, the scale being fitted to the
mean detection product. PF-7g barred the unscaled mean absolute deviation at
0.05, which the skewed measures cannot meet. Under the parent's own comparison
the scaled sawtooth is closer than quantum in 15 of 16 cells, not 16.

## 2. The instrument study, unsealed and non-claim-bearing

`python/pf7_control_tuning.py` measured why the controls die. Two findings, both
used below.

The inner product `L . q` falls as 1/sqrt(d), measured mean 0.4997, 0.2906,
0.1421, 0.0702 at d = 3, 8, 32, 128. Every control in the parent harness applies
a FIXED coefficient to that product, so each perturbation weakens with
dimension. Rescaling the measurement dependence tilt by d strengthens it
materially, from the 2.0 to 2.3 band up to 2.3 to 3.8.

Rescaling does NOT make the premise controls universal. With scaling, the
post-selection control fires 8/16 (worse than unscaled at 10/16), the tilt 15/16
and the locality leak 12/16. Failures concentrate on the skewed measures, where
a few orientations dominate the sample and the correlation structure degenerates
whatever the coefficient. **Premise-break violation magnitude is a quantity the
substrate varies by design.**

A PR box, outputs satisfying a XOR b = x.y, gives S = 4.000 in 16 of 16 cells.
It is nonlocal by construction and carries no geometry, so it is the only
control here that a per-cell bar can be declared against honestly.

## 3. Bars

**B0, anti-vacuity, per cell, against the geometry-independent control only.**
The PR box arm must give S > 2.0 in EVERY configuration. This bar gates the run.
It is safe as a per-cell bar precisely because the substrate cannot vary it.

**B0b, premise controls, aggregate.** Each of the post-selection, measurement
dependence and locality arms must have MEDIAN S > 2.0 across the sixteen
configurations, and each must fire in at least 10 of 16. Aggregate because the
instrument study measured that the substrate varies these. The per-cell counts
are reported, not barred.

**B1, the ceiling, a CODE CHECK not a discovery.** P0, all trials counted, must
give S <= 2 + 3 sigma at every configuration. The P0 null is a theorem for any
source measure, so this carries no evidence about folds and is retained only
because failure would mean a premise is silently broken.

**B2, the conservation signature.** With complete detection, matched settings
must give |E(theta = 0)| >= 0.99.

**B3, the discriminator, using the parent harness's own comparison.** For at
least 14 of 16 configurations, `rms_vs_scaled_sawtooth < rms_vs_quantum`, that
is the fold's angular law is closer to a scaled classical sign law than to the
quantum cosine. The threshold is 14 rather than 16 because the instrument study
measured 15 of 16 under PF-7g's data and the skewed cells are the marginal ones.
The distance `max_gap_vs_quantum` is REPORTED as a distribution, not barred,
because PF-7g passed that bar by 0.0011 and a margin that thin is not evidence.

**B4, no signalling residual <= 0.01 in P0.** A code check.

**B5, the blind consumer, PF-8's clause for correlations.** The 1->3 zigzag arm
must give S_postselected > 2.0 while S_all_counted <= 2 + 3 sigma. PF-7g
measured 2.259 against 1.003, so this bar is known reachable; it is retained to
confirm it under the corrected instrument.

## 4. Fixed configuration

```
SEED            20260808
DIMS            3, 8, 32, 128
KAPPA           0.0, 2.0
ZIPF            0.0, 1.5
N_ORIENT        60000
N_DRAW          200000
N_ANG           37
DETECTOR_SHARP  3.0
TILT            1.2 * d          rescaled per the instrument study
LEAK            0.45
ZIGZAG          0.35
B0_BAR          2.0   per cell, PR box only
B0B_MEDIAN      2.0   per premise arm
B0B_MIN_FIRE    10    of 16, per premise arm
B2_BAR          0.99
B3_MIN_CELLS    14    of 16, scaled sawtooth closer than quantum
B4_BAR          0.01
```

## 5. Interpretation, fixed in advance

If B0 and B0b pass and B1 holds and B3 shows the scaled sawtooth, the recorded
result is that the fold reproduces the conservation signature of a pair and not
the contextual one, and PF-7's interpretation clause applies as written, the
model is capped as a classical representation. That is the expected outcome and
it is a negative for folding as an account of entanglement.

The residue kept either way is the measured distribution of
`max_gap_vs_quantum`, the size of the gap a fold would have to close, reported
without a bar.
