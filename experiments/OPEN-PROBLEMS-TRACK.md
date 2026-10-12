# OP Track: open problems of other fields where the read operator might help

**Status:** opened 2026-10-11 by the owner, from the survey `notes/ot-open-problems-survey.md`. OP1
(Koopman dictionaries): probe done in two rounds; on the probe READ is level with the controls
under TEND and behind under RFF; pilot running on Atlas as designed (owner). OP2 (memory in
Mori–Zwanzig models): RECORDED AT THE PILOT (owner, 2026-10-12), pilot grade FAIL; the modes READ
makes explicit leave less memory than ENERGY's (0.538 against 0.574) and slightly more than BALL's
(0.531), at both resolutions. OP3 a record draft; OP4 a design draft. Nothing here is claim-bearing until
registered. Chip 🧭 OP.

## 1. Question

The OD track asked what Observation Theory can find about observation itself. This track asks a
narrower and more outward question. Other fields have open problems whose sharp part is a choice of
what to observe. Does the read operator make that choice better than the field's own classical
choices, under the evidence discipline of this repository?

A problem enters the track only when three things hold. Its open question, or a named part of it,
is a choice of which quantities an observer reads or keeps. The choice can be tested on a finite,
seeded world in this repository. And the field has a classical choice to beat, which is computed
beside the read operator's and graded against it.

The survey records why the track holds no Millennium problem. Every property the read operator
supplies is preserved by a known obstruction (Tao's averaged Navier–Stokes equation for regularity,
relativization and the locality barrier for P versus NP), so the operator cannot carry a proof
there. The track's results are about choosing what to read, which is where OT's sealed positive
results sit (D6v3, D7v3).

## 2. Anchors

`notes/ot-open-problems-survey.md` (the list and its ranking); `notes/dynamical-read-operator.md`
(Proposition 4, read distortion as the optimal ranking under random phases; Section 6, the
dynamical read); the OD gates D6v3 (PASS, the read operator's spectrum places sensors), D7v3 (PASS,
the read-distortion closure ahead of the energy closure inside its rank scope) and D8 (nudging mode
selection, pilot pointing to FAIL); `standards/DPE-RECORDS.md` for the records every gate produces.
Each gate names its field's literature in its own registration.

## 3. Anti-circularity contract

OD's contract applies unchanged: observer families declared in `claims/transformations/OP.toml`
before a seal, every classical control computed beside the observational quantity, and a result the
classical quantity reproduces is not an Observation Theory result.

Two clauses are added because the problems belong to other fields. First, the strongest selector
that field's literature would use on the same data runs beside the graded controls as a recorded
reference, so the record shows where the read operator sits against it even when the bars do not
grade against it. Second, the world, the controls and the error are fixed from that field's
practice, not from what favours the read operator, and any departure is stated in the registration
with its reason.

## 4. Gates

### OP1. On which coordinates should a Koopman dictionary be built

Open problem. EDMD approximates the Koopman operator on a dictionary of observables, and choosing
the dictionary is open (Colbrook, arXiv:2312.00137). OP1 takes the slice an observer defines. A
consumer reads the large scales of a forced two-dimensional flow and forecasts them with EDMD on a
dictionary holding its own coordinates and r further coordinates of the flow.

Prediction. Ranking the further coordinates by their read distortion for the consumer gives a
lower multi-step forecast error than ranking them by energy or by scale, at matched r, under both
a linear and a nonlinear lift, converging in resolution.

World. D8's forced turbulence and its validated worlds; the rankings READ, ENERGY, BALL, SENS and
RANDOM; references POD, GREEDY and the persistence forecast. Registration draft
`experiments/OP/OP1/PREREG-OP1-DRAFT.md`, code `experiments/OP/OP1/op1_edmd.py`.

What falsifies. READ not ahead of the better of ENERGY and BALL, pooled, in either lift.

### OP2. How much memory a reduced model needs, and which modes to keep explicit

Open problem. The Mori–Zwanzig formalism gives an exact closure for resolved variables with a
memory integral that is costly to evaluate. Why the simple t-model works is recorded as an
outstanding question (Parish and Duraisamy, arXiv:1611.03311).

Design draft. On D7's filtered flow, the read-distortion choice of which subfilter modes to carry
explicitly, with the rest represented through a finite memory, against the energy choice, scored by
the memory length needed for a fixed resolved-tendency error. The theory note's Section 2 (the
failure of closure for a spectral observer) and Proposition 3 (the feedback bound) are the starting
algebra.

Literature status (searched 2026-10-11, abstracts and summaries only). Data-driven Mori–Zwanzig is
active after 2020. Lin and coauthors extract the Markov term, memory kernel and orthogonal dynamics
from data with Mori's projection (arXiv:2101.05873, 2021) and then with regression as the
projection (arXiv:2205.05135, 2022), and call Zwanzig's projection optimal but infeasible. Tian,
Lin, Anghel and Livescu learn the operators for isotropic turbulence (arXiv:2108.13288, 2021; the
journal version is Phys. Fluids 33, 125118) and compare four hand-chosen sets of observables; read
in full on 2026-10-11 and summarized in the OP2 registration draft. (Corrected 2026-10-11: an earlier
version of this paragraph named the authors as Hader and coauthors, from a search summary. Christoph
Hader is a coauthor of the boundary-layer paper arXiv:2309.15864, not of this one.) Later
work applies the method to sparse sensors in boundary-layer transition (arXiv:2309.15864) and to
Lagrangian particles (de Wit et al., PNAS 123, 2026, arXiv:2507.16058). The memory length is
treated as a problem-dependent choice, fitted or set dynamically (arXiv:1906.01411). The search found no
work that chooses which modes stay explicit so as to shorten the memory, which is OP2's question.
Why the t-model works is still described through renormalization (Stinis; Price and Stinis,
arXiv:1707.01955), and no newer explanation turned up.

Registration draft: `experiments/OP/OP2/PREREG-OP2-DRAFT.md` (written 2026-10-11 as a design draft). Probe and pilot
done. Recorded at the pilot on the owner's decision (2026-10-12): pilot grade FAIL, with READ
leaving less memory than ENERGY and slightly more than BALL, and its forecast with memory 1.06
percent worse pooled. Not sealed. It uses Mori's linear
projection and the correlation recursion of Lin and coauthors on OP1's world, trajectories,
rankings and TEND observable, and asks whether the modes READ makes explicit leave a shorter memory
than ENERGY's or BALL's.

### OP3. Sensor selection as observer choice, the joint record

Not a new experiment. A write-up of D6v3 (PASS: the read operator's spectrum places sensors on a
linear system with fewer sensors than the energy ranking and never more) and D8 (which modes a
nudged copy must read, graded when its run completes), set against the sensor-selection literature
(Kazma et al. 2023 and 2024, Mons and Marquet 2021, Inubushi and Caulfield arXiv:2508.16920). The
two results may point in opposite directions, and the record says so if they do.

### OP4. D6v3's spectral selector on D8's flow

The test OP3's record suggests. D6v3's window-Gramian selector, restricted to the flow's leading
tangent subspace, chooses the Fourier pairs a nudged copy of D8's turbulence must read, and its
synchronization budget is compared cell by cell with D8's pilot budgets for BALL and READ on the same
seeds. The outcome says whether D8's loss to BALL belongs to the per-mode instrument or to the
system. Design draft: `experiments/OP/OP4/OP4-DESIGN-DRAFT.md` (2026-10-12). It waits for D8's
eighth pilot cell.

### Deferred

Probes in mechanistic interpretability (survey entry 3.5) waits for `readscope` evidence beyond
one model. Observable choice in quantum state learning (entry 3.6) is not pursued, since classical
shadows remove the selection question.

## 5. Records

Each gate writes its families to `claims/transformations/OP.toml` before sealing, its sealed
registration under `experiments/OP/`, its verdict rows to the status ledger, its witnesses and
revisions as `[witness]` and `[revised]` rows.

## 6. Order and what stops the track

OP1 first, since it reuses D8's solver and D7's instrument and needs nothing new. OP2 after OP1 and
after its literature check. OP3 when D8's run is graded. If OP1 fails in both lifts and D8 fails,
read distortion will have lost twice as a selector for dynamical forecasting, against one win for
closure (D7v3) and one for sensor placement (D6v3). OP2 is then reconsidered before it is
registered, and the record states the pattern.
