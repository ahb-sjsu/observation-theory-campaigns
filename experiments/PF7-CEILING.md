# PF-7: Quantum-Structure Ceiling Test

Declared 2026-08-06, unsealed, exploratory. This document holds the
concrete PF-7 protocol. The design question is in CAMPAIGN.md
section 5, can the model reproduce more than a classical worldline
picture, with the standing interpretation that failure caps the
model as a classical representation and does not invalidate the
kinematic fold theorem.

PF-7 is ungated because both mandatory gates passed, PREREG-PF5-002
on conservation and complete accounting and PREREG-PF6-002 on
covariance and observers.

## PF-7 protocol (declared 2026-08-06, before the run)

The discriminator, declared with its reasoning so the run can
refute it. A quantum mode swept twice through an avoided crossing
accumulates a relative phase between the two passages, so its
excitation probability oscillates with the delay between them. A
classical ensemble of independent trajectories carries no phase, so
its event fraction cannot oscillate with the same delay. PF-7
measures both curves with one declared statistic.

Quantum arm. A two-level mode with declared gap 0.30 and sweep rate
1.0 in natural units, integrated by fourth-order Runge-Kutta at
timestep 2e-4. The single-passage control sweeps the detuning
linearly through zero. The double-passage run sets the detuning to
the sweep rate times the absolute time minus a declared half-delay,
so the mode crosses at plus and minus that half-delay, the
Landau-Zener-Stueckelberg construction. Declared half-delay grid,
twenty-four points from 2.0 to 7.75 in steps of 0.25.

Classical arm. The pilot fold dynamics with two Sauter pulses of
the declared field 1.2020141601562502 at the PF5-002 gap 0.80,
separated by twice the same half-delay, thermal ensemble of 2000
declared seeded members per delay, timestep 2e-3, observable the
reversing fraction. The dynamics are the pilot's, with the single
slab replaced by the declared two-pulse profile, so this runner is
not the frozen single-slab instrument and says so.

The statistic. For each curve, the mean is removed and the discrete
Fourier power spectrum taken, and the oscillation statistic is the
largest nonzero-frequency power divided by the total power.

Bars. Q1, the single-passage probability matches the Landau-Zener
closed form within 2e-3. Q2, the quantum curve's oscillation
statistic is at least 0.30. Q4, the exclusion statement, the
two-level norm is conserved within 1e-10 at every step, so the mode
holds at most one excitation exactly. The verdict is computed from
Q1, Q2, and Q4, which establish that the instrument can see
interference where interference exists.

Q3, the ceiling measurement, recorded individually with a declared
directional bar and either outcome a result. The classical curve's
oscillation statistic is at most 0.15 and the quantum statistic
exceeds it by at least a factor of three. If Q3 holds, the reading
is the one the design anticipated, the fold model is capped as a
classical representation, it does not carry the phase structure
that produces interference, and this does not touch the kinematic
fold theorem or any measured PF result. If Q3 fails, a classical
ensemble reproduced an interference signature and that is the more
interesting outcome.

Exploratory label, results/pf7-quantum-ceiling.json.

## PF-7 results (run 2026-08-06, record sha 70dd6558f636...)

Verdict FAIL, on two instrument bars, and the ceiling measurement
that appeared to hold is vacuous. All three failures are the
declaration's, and the physics arm behaved.

Q1 measured 0.8631 against the Landau-Zener closed form 0.868167, a
deviation of 5.06e-3 against the declared 2e-3. The declared sweep
range of forty natural units does not reach the asymptotic regime
at the declared gap, so the comparison was made before the state
settled.

Q2 measured an oscillation statistic of 0.2238 against the declared
0.30, while the recorded curve plainly oscillates, 0.0313, 0.0247,
0.2306, 0.4172, 0.2722, 0.0104, 0.1641, 0.4027 and onward across
the grid. The declaration mis-specified the grid rather than the
physics. The Stueckelberg phase between two crossings at plus and
minus a half-delay is the integral of the detuning between them,
which is proportional to the square of the half-delay, so the
oscillation is a chirp whose local frequency grows linearly with
delay. A grid uniform in delay therefore undersamples the far end
and spectral power spreads across bins instead of concentrating.

Q4 passed, the two-level norm is conserved to 5.5e-14, so the mode
holds at most one excitation exactly.

Q3, the ceiling measurement, read as holding and must not be
reported as a result. The classical arm returned a reversing
fraction of exactly 1.0 at every one of the twenty-four delays, all
2000 members of every cell reversing, so its oscillation statistic
was computed on a constant curve and is zero for a reason that has
nothing to do with interference. The declared field was strong
enough that two pulses reverse everything. This is the fourth
instance of one error class in this campaign, after PF4-003's empty
cells, PREREG-PF5-001's event-free grid, and PREREG-PF6-001's
fold-free members, and the standing rule that already covers it was
not applied here because the arm was a new construction rather than
a bound manifest. The rule is now unconditional, any arm of any
experiment must have a committed probe showing it contains the
variation the claim is about.

## PF-7b protocol (declared 2026-08-06, before the run)

Three corrections, each to a named error, with everything else
unchanged.

The sweep range of the single-passage control becomes 120 natural
units so the comparison is made in the asymptotic regime, bar
unchanged at 2e-3.

The delay grid becomes uniform in the square of the half-delay
rather than in the half-delay, thirty-two points with the squared
half-delay running from 4.0 to 60.0, so the chirp becomes a single
frequency and the declared statistic measures what it was meant to
measure. Bar unchanged at 0.30 for the quantum arm.

The classical field is bound from a committed probe,
`python/pf7_classical_probe.py` writing
`results/pf7-classical-probe.json`, which bisects the field at the
declared gap under the two-pulse profile to bring the reversing
fraction to the declared target 0.5, and reports the fraction at
the extreme delays. PF-7b binds the field only if the probe's
fraction lies inside the declared window 0.15 to 0.85 at the middle
delay and at both extremes. The anti-vacuity bar for the classical
arm, every delay cell's reversing fraction lies strictly inside
0.02 to 0.98 in the governed run, else the ceiling measurement is
recorded vacuous rather than holding.

Bars otherwise unchanged, Q1 and Q2 and Q4 compute the verdict, Q3
is the ceiling measurement recorded individually with either
outcome a result. Exploratory label,
results/pf7b-quantum-ceiling.json.
