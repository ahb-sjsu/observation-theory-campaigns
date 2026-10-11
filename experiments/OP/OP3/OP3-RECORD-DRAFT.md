# OP3 (RECORD DRAFT): sensor selection as the choice of an observer, what two gates say together

Status: DRAFT, 2026-10-11. A record, not an experiment and not claim-bearing. Gate OP3 of the OP
track (`experiments/OPEN-PROBLEMS-TRACK.md`). It sets two finished or running gates of the OD track
beside each other and beside the sensor-selection literature. D6v3 is sealed and graded. D8's pilot
has 7 of its 8 cells and its run is not registered, so every D8 statement below is a probe or pilot
reading and none is a verdict. The record is completed when D8 is graded.

## 1. The question in the field

Choosing which quantities to measure is a standing problem wherever a state is estimated from part
of it. In control and estimation it is posed as maximizing an observability measure under a sensor
budget, usually by greedy selection with submodular guarantees, which is often suboptimal
(Kazma et al. 2023 and 2024; the empirical-Gramian determinant of Serpas et al. 2013 is a
mixed-integer nonlinear program). In fluid data assimilation it is posed as where to place probes
for a reconstruction (Mons and Marquet, J. Fluid Mech. 2021) or which Fourier modes a nudged copy of
a turbulent flow must receive. For the last, the classical theory gives counts, not choices. The
determining-modes bound of Jones and Titi grows with the Grashof number. In practice nudging only
the modes below a threshold near the forcing wavenumber synchronizes two-dimensional Kolmogorov
flow, and the threshold is identified by the leading Lyapunov exponent (Inubushi and Caulfield,
arXiv:2508.16920, 2025; the same picture from conditional Lyapunov vectors, Li et al., J. Fluid Mech.
2024 and 2025). Which modes to observe for a given count is not settled by either literature.

## 2. Two gates, two settings, two instruments

| | D6v3 (sealed, PASS) | D8 (pilot, 7 of 8 cells) |
|---|---|---|
| System | Linear systems and Lorenz-96: a diffusion chain, Lorenz-96 at $n = 20$, shallow water, and two unseen families (Lorenz-96 at $F = 10$, an advection-diffusion chain) | Forced two-dimensional turbulence (Kolmogorov forcing at $k_f = 4$, drag), $\nu = 0.03$ and 0.02 at $n = 96$ and 128 |
| Task | Place the fewest sensors that identify $m$ directions at a budget over a window | Find the fewest Fourier pairs whose nudging synchronizes a copy, sustained over a final window |
| OT's selector | The spectrum of the read operator, which for a linear system observed over a window is the exact window Gramian: the count of directions above the budget, searched exactly where checkable | READ, the read distortion of each pair (its sensitivity to the nonlinear tendency times its training energy), a ranking mode by mode |
| Controls | The energy ranking of the readings, random orderings, D6's greedy | BALL ($|k|$ ascending, the Inubushi and Caulfield observer), ENSTROPHY (READ's own amplitude factor), KE |
| Result | The selector equals the exhaustive minimum in all 50 checkable cells, needs strictly fewer sensors than the energy ranking in 10 of 28 cells where placement matters and never more, never more than D6's greedy and fewer in six, and gives a forecast horizon 12.3 percent longer than the energy placement's pooled | READ behind BALL in every cell measured. Probe round 3 (one trajectory per world): 3 ladder steps behind on both valid worlds. Pilot so far: 1 step behind in both $\nu = 0.02$, $n = 96$ cells, 3 behind at $\nu = 0.02$, $n = 128$, and 3 and 5 behind in each $\nu = 0.03$ pair. READ level with or ahead of ENSTROPHY in every pilot cell |

The pilot's eighth cell ($\nu = 0.02$, $n = 128$, trajectory 0) is running as five split Jobs after
its first attempt timed out. The timed-out attempt logged READ's budget as 48 pairs before it was
stopped. Its controls were not reached.

## 3. Reading the two together

The two gates point in opposite directions, and they differ in three ways at once. The system
(linear and low-dimensional chaotic, against two-dimensional turbulence), the instrument (the exact
spectrum of a Gramian searched over sets, against a diagonal ranking of single modes) and the
strongest control (the energy of the readings, against the scale of the modes). These two gates do
not identify which difference explains the split, and this record does not claim one.

What can be said is narrower, and it holds across the campaign so far.

| Gate | OT quantity | Against an energy-type control | Against a scale control |
|---|---|---|---|
| D6v3 | Window-Gramian spectrum | ahead (fewer sensors in 10 of 28, never more) | not run |
| D7v3 | Read distortion per mode, closure | ahead (2.8 and 10.0 percent at ranks 64 and 128) | not run |
| D8 | Read distortion per mode, nudging | ahead of or level with ENSTROPHY in every pilot cell | behind BALL in every cell |
| OP1 | Read distortion per mode, Koopman forecast | ahead of ENERGY in 13 of 20 TEND cells | level with BALL under TEND, behind under RFF (probe) |
| OP2 | Read distortion per mode, memory | less memory than ENERGY (0.533 against 0.574) | slightly more than BALL (0.524) (probe) |

Wherever energy is the control, the read operator's quantity wins or ties. Wherever scale is the
control, per-mode read distortion loses or ties. In forced turbulence the scale ordering is the
physics. The large scales near the forcing carry the instability (Inubushi and Caulfield), and BALL
takes them first by construction. A diagonal ranking of modes by their one-step read can promote a
small-scale mode with a large instantaneous read over a large-scale mode that the flow's instability
needs. D8's rankings show it. At $\nu = 0.03$, $n = 96$, six of READ's first twelve pairs lie at
$|k| \ge 4$, the forcing shell and beyond, while BALL's first twelve stop at $|k| = 2.83$.

## 4. Placement against the literature

D8's BALL arm reproduces Inubushi and Caulfield's observer on their flow family, and its budgets
($|k| \le 2$ and 3 on the two probe worlds) agree with their threshold near the forcing scale. That
part is a replication, not a contribution. D6v3's comparison with greedy selection is the closest
contact with the submodular sensor-selection literature (Kazma et al.). On its worlds the exact
spectral search never needs more sensors than greedy and needs fewer in six cells, which is the
suboptimality of greedy that literature reports, measured on a criterion OT supplies.

## 5. A test that would separate the explanations (suggestion, not decided)

The instrument that won on linear systems has not been tried where per-mode read distortion lost.
D6v3's selector needs a Gramian. For a nudged copy of the flow the natural one is the finite-time
Gramian of the linearized synchronization error. Its generator is the finite-gain observer
operator $DF(u) - \mu P_S$ of the theory note (`notes/dynamical-read-operator.md`, Section 6). Choosing the pairs by the spectrum of
that Gramian, searched over sets as D6v3 searched, and comparing it with BALL on D8's worlds would
ask whether the split in Section 3 belongs to the instrument or to the system. If the spectral
selector matched or beat BALL, the per-mode ranking would be the weak link. If it also lost, scale
would be what turbulence asks an observer to read, and OT would have learned where its selection
results stop. The cost is of the order of D8's pilot. This is a suggestion for the owner and is not
registered.

## 6. What waits

D8's eighth pilot cell, its pilot grade and tolerances, and the owner's decision on its run. The
row for D8 in Section 2 and the D8 lines in Section 3 are rewritten from D8's graded record when
it exists, and this draft becomes `OP3-RECORD.md`.

## Sources

D6v3: `experiments/DISCOVERY-TRACK.md` (record of 2026-09-10) and `experiments/OD/D6v3/`. D7v3:
`experiments/OD/D7v3/grade.json`. D8: `experiments/OD/D8/PREREG-D8-DRAFT.md` Section 7 and the saved
pilot pieces `experiments/OD/D8/pilot_pieces/` on Atlas (read 2026-10-11). OP1 and OP2: their drafts'
probe records. Literature as cited in D8's draft background and the survey
`notes/ot-open-problems-survey.md`, entry 3.3.
