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
