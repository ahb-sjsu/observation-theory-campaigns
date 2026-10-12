# OP3 (RECORD): sensor selection as the choice of an observer, what the gates say together

Status: RECORD, 2026-10-12. A record, not an experiment and not claim-bearing. Gate OP3 of the OP
track (`experiments/OPEN-PROBLEMS-TRACK.md`). It sets D6v3 and D8 beside each other, beside the
other OP gates and beside the sensor-selection literature. D6v3 is sealed and graded PASS. D8, OP1
and OP2 were recorded at their pilots on the owner's decisions of 2026-10-12, each with a pilot grade
of FAIL by its committed grader. Pilot grades are not registered verdicts, and every D8, OP1 and OP2
number below is a pilot number. Written 2026-10-11 as `OP3-RECORD-DRAFT.md` and rewritten from D8's
graded pilot.

## 1. The question in the field

Choosing which quantities to measure is a standing problem wherever a state is estimated from part
of it. In control and estimation it is posed as maximizing an observability measure under a sensor
budget, usually by greedy selection with submodular guarantees, which is often suboptimal (Kazma
et al. 2023 and 2024; the empirical-Gramian determinant of Serpas et al. 2013 is a mixed-integer
nonlinear program). In fluid data assimilation it is posed as where to place probes for a
reconstruction (Mons and Marquet, J. Fluid Mech. 2021) or which Fourier modes a nudged copy of a
turbulent flow must receive. For the last, the classical theory gives counts, not choices. The
determining-modes bound of Jones and Titi grows with the Grashof number. In practice nudging only
the modes below a threshold near the forcing wavenumber synchronizes two-dimensional Kolmogorov
flow, and the threshold is identified by the leading Lyapunov exponent (Inubushi and Caulfield,
arXiv:2508.16920, 2025; the same picture from conditional Lyapunov vectors, Li et al., J. Fluid Mech.
2024 and 2025). Which modes to observe for a given count is not settled by either literature.

## 2. Two gates, two settings, two instruments

| | D6v3 (sealed, PASS) | D8 (recorded at the pilot, pilot grade FAIL) |
|---|---|---|
| System | Linear systems and Lorenz-96: a diffusion chain, Lorenz-96 at $n = 20$, shallow water, and two unseen families (Lorenz-96 at $F = 10$, an advection-diffusion chain) | Forced two-dimensional turbulence (Kolmogorov forcing at $k_f = 4$, drag), $\nu = 0.03$ and 0.02 at $n = 96$ and 128, two test trajectories each |
| Task | Place the fewest sensors that identify $m$ directions at a budget over a window | Find the fewest Fourier pairs whose nudging synchronizes a copy, sustained over a final window |
| OT's selector | The spectrum of the read operator, which for a linear system observed over a window is the exact window Gramian: the count of directions above the budget, searched exactly where checkable | READ, the read distortion of each pair (its sensitivity to the nonlinear tendency times its training energy), a ranking mode by mode |
| Controls | The energy ranking of the readings, random orderings, D6's greedy | BALL ($|k|$ ascending, the Inubushi and Caulfield observer), ENSTROPHY (READ's own amplitude factor), KE |
| Result | The selector equals the exhaustive minimum in all 50 checkable cells, needs strictly fewer sensors than the energy ranking in 10 of 28 cells where placement matters and never more, never more than D6's greedy and fewer in six, and gives a forecast horizon 12.3 percent longer than the energy placement's pooled | READ behind BALL in all 8 cells, by 3.1 ladder steps pooled. BALL synchronizes at 8 pairs ($\nu = 0.03$) and 12 ($\nu = 0.02$) in every cell, READ at 16 to 48. Against ENSTROPHY READ is ahead in 5 cells and level in 3. Against KE it is ahead in 2, level in 3 and behind in 3. The theory note's Propositions 2 and 3 hold on all 24 checks |

## 3. Reading the gates together

D6v3 and D8 point in opposite directions, and they differ in three ways at once. The system
(linear and low-dimensional chaotic, against two-dimensional turbulence), the instrument (the exact
spectrum of a Gramian searched over sets, against a diagonal ranking of single modes) and the
strongest control (the energy of the readings, against the scale of the modes). These two gates do
not identify which difference explains the split, and this record does not claim one. OP4 is the
test that separates them (Section 5).

What the campaign's pilots and seals do show, cell by cell, with READ (or D6v3's spectrum) against
each kind of control:

| Gate | OT quantity | Against its own amplitude ranking | Against kinetic energy | Against scale (BALL) |
|---|---|---|---|---|
| D6v3 (sealed) | Window-Gramian spectrum | ahead of the energy ranking, fewer sensors in 10 of 28 cells and never more | not run | not run |
| D7v3 (sealed) | Read distortion per mode, closure | ahead of energy, 2.8 and 10.0 percent at ranks 64 and 128 | not run | not run |
| D8 (pilot) | Read distortion per mode, nudging | ENSTROPHY: 5 ahead, 3 level, 0 behind | KE: 2 ahead, 3 level, 3 behind | 0 ahead, 8 behind |
| OP1 (pilot) | Read distortion per mode, Koopman forecast | ENERGY: 48 ahead, 3 level, 29 behind of 80 | not run | 42 ahead, 38 behind of 80 |
| OP2 (pilot) | Read distortion per mode, memory | ENERGY: 34 ahead, 5 behind of 40 | not run | 18 ahead, 21 behind of 40 |

Three statements follow, and each is as wide as the table and no wider.
- Read distortion improves on the energy ranking it is built from. READ is the energy of a mode
  weighted by the consumer's sensitivity to it, and the weighting helps in every gate where that
  energy ranking competes (D7v3 sealed; D8, OP1 and OP2 at their pilots, by 5 to 0, 48 to 29 and 34
  to 5 cells).
- Read distortion does not reliably beat other classical rankings. Against kinetic energy in D8 it
  splits 2 ahead, 3 behind. Against scale it loses outright where scale is the physics (D8, 0 of 8),
  and it is level with scale where the task is a forecast or a memory (OP1 42 to 38, OP2 18 to 21).
- Every pilot that graded READ against the better of two controls in each cell failed (D8, OP1,
  OP2). A per-mode weighting that beats each control on average still loses to whichever control is
  best in a given cell.

Why scale wins for nudging, as far as these gates show it. In forced turbulence the large scales
near the forcing carry the instability (Inubushi and Caulfield), and BALL takes them first by
construction. A diagonal ranking of modes by their one-step read can promote a small-scale mode with
a large instantaneous read over a large-scale mode that the flow's instability needs. D8's rankings
show it. At $\nu = 0.03$, $n = 96$, six of READ's first twelve pairs lie at $|k| \ge 4$, the forcing shell and
beyond, while BALL's first twelve stop at $|k| = 2.83$, and READ's budget there is 24 to 48 pairs
against BALL's 8.

## 4. Placement against the literature

D8's BALL arm reproduces Inubushi and Caulfield's observer on their flow family, and its budgets
agree with their threshold near the forcing scale. Its 8 pairs reach out to $|k| = \sqrt 5 \approx 2.24$ and
its 12 pairs to $|k| = \sqrt 8 \approx 2.83$, inside $k_f = 4$, in every pilot cell at both resolutions. That part is
a replication, not a contribution. D6v3's comparison with greedy selection is the closest contact
with the submodular sensor-selection literature (Kazma et al.). On its worlds the exact spectral
search never needs more sensors than greedy and needs fewer in six cells, which is the suboptimality
of greedy that literature reports, measured on a criterion OT supplies.

## 5. The test that separates the explanations: OP4

The instrument that won on linear systems had not been tried where per-mode read distortion lost.
OP4 (`experiments/OP/OP4/OP4-DESIGN-DRAFT.md`, code `op4_gram.py`, committed 2026-10-12) takes
D6v3's window-Gramian selector to D8's flow. The selector is restricted to the flow's leading
tangent subspace. Its generator is the tangent dynamics, the $\mu \to 0$ form of the finite-gain observer
operator $DF(u) - \mu P_S$ of the theory note (`notes/dynamical-read-operator.md`, Section 6). It is put
through D8's nudging protocol on D8's pilot seeds, paired cell by cell with D8's budgets. Its
parameters are fixed by a rule blind to every nudging result. Its readings were fixed before any
run. Matching or beating BALL means the per-mode instrument was the weak link ("instrument"). Beating
READ but not BALL means "both". Beating neither means that in this flow scale is what an observer
must read, even with the instrument that won on linear systems ("system"). Its probe, on one world
($\nu = 0.03$, $n = 96$, both trajectories), is running on Atlas.

## 6. What waits

OP4's probe. If it reads "system", this record's Section 3 stands as the campaign's finding on
selection, and the OT selection results are bounded by D6v3's linear and low-dimensional worlds and
by D7v3's closure. If it reads "instrument" or "both", the per-mode ranking of D8, OP1 and OP2 is the
part to replace, and the campaign's next registrations should use the Gramian spectrum.

## Sources

D6v3: `experiments/DISCOVERY-TRACK.md` (record of 2026-09-10) and `experiments/OD/D6v3/`. D7v3:
`experiments/OD/D7v3/grade.json`. D8: `experiments/OD/D8/PREREG-D8-DRAFT.md` Section 7,
`experiments/OD/D8/pilot_grade.json`, and the merged pilot results on Atlas (sha256 569b38f1...). OP1
and OP2: their drafts' pilot records and `pilot_grade.json` files. The cell counts in Section 3 were
computed from the merged pilot results on 2026-10-12. Literature as cited in D8's draft background
and the survey `notes/ot-open-problems-survey.md`, entry 3.3.
