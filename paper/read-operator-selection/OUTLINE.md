# Where the Read Helps: Choosing What to Observe by Read Distortion, from Linear Sensors to Turbulence

**Status: OUTLINE v1, 2026-10-12.** Not a draft. The write-up of the OP track and the selection gates
of the OD track (D6v3, D7v3, D8). One section has two versions, and the OP4 probe, now running,
decides which one is written. Nothing below goes into prose until the open items at the end are
settled.

## The claim, as wide as the evidence and no wider

A consumer that reads part of a dynamical system has a read operator, and the read distortion of a
mode is its energy weighted by the consumer's sensitivity to it. Ranking candidate observables by
read distortion
1. improves on the energy ranking it is built from, in every setting where the two compete:
   linear sensor placement (D6v3, sealed), closure of a filtered flow (D7v3, sealed), and, at their
   pilots, synchronization of a nudged copy (D8), Koopman forecasting (OP1) and Mori–Zwanzig memory
   (OP2);
2. does not reliably beat other classical rankings: it is mixed against kinetic energy (D8) and level
   with scale in forecasting and memory (OP1, OP2);
3. loses outright to scale where the flow's instability lives in the large scales. A nudged copy of
   forced two-dimensional turbulence needs 1.3 to 6 times as many modes chosen by read distortion as
   chosen by scale, in all 8 pilot cells (D8).

The paper's contribution is the map, not a new selector. It also gives the mechanism behind
statement 3: the per-mode ranking spends its picks at the forcing shell, while synchronization
needs the large scales first. And it carries the OP4 result, which says whether a better OT
instrument closes that gap.

## Evidence base and its status (state it in the paper exactly like this)

| Gate | Setting | Status | Grade | What it contributes |
|---|---|---|---|---|
| D6v3 | Sensor placement, linear and Lorenz-96 | sealed, run | PASS | the Gramian spectrum beats energy (fewer sensors in 10 of 28 cells, never more) |
| D7v3 | Closure of filtered 2-D turbulence | sealed, run | PASS | read distortion beats energy by 2.8 and 10.0 percent at ranks 64 and 128 |
| D8 | Nudging forced 2-D turbulence | recorded at the pilot | pilot FAIL | read distortion behind scale in 8 of 8 cells, by 3.1 ladder steps |
| OP1 | Koopman (EDMD) dictionaries | recorded at the pilot | pilot FAIL | ahead of energy in 48 of 80 cells, level with scale; one world in a slow regime |
| OP2 | Mori–Zwanzig memory | recorded at the pilot | pilot FAIL | less memory than energy (34 of 40 cells), level with scale |
| OP4 | D6v3's Gramian on D8's flow | probe running | none yet | instrument or system |
| Theory note | Galerkin Navier–Stokes | proved, finite-dimensional | n/a | Propositions 1 to 4; Propositions 2 and 3 checked numerically in every D8 pilot cell (T1, T2) |

The weak point a referee will find first. Three of the five comparisons are pilots with committed
graders, recorded on the owner's decisions and not sealed runs. The paper has two honest options,
and the choice is the owner's (open item 2). (a) Present them as preregistered pilots: graders and
tolerances fixed before the pilot, every outcome reported. (b) Seal and run one decisive gate
before submission.

## Structure (headings state findings, per the standing prose standard)

1. **Choosing what to observe is an open problem in several fields** (introduction, no
   mathematics). EDMD dictionaries, Mori–Zwanzig closures, sensor placement and nudging all ask
   which quantities to read. This paper asks one question across all of them: does the consumer's
   sensitivity help choose? It answers in one paragraph, with the three statements above.
2. **The read operator and the read distortion of a mode.** The observer, the read operator, read
   distortion, and Proposition 4 (read distortion is the optimal ranking under random phases), from
   the theory note. The first-order argument shows why the ranking should help each task, and where
   that argument ends (one step, linear in the mode, diagonal).
3. **Where the read helps: linear sensors and closure.** D6v3 and D7v3, both sealed.
4. **Where it ties: forecasts and memory.** OP1 (the lift rule, TEND, the regime caveat) and OP2
   (the memory share chosen by split-half reliability). Ahead of energy, level with scale.
5. **Where it loses: synchronizing forced turbulence.** D8: the budgets, the mechanism, the
   replication of Inubushi and Caulfield's observer. The theory note's propositions hold in every
   cell, so the loss is not a failure of the operator's computation.
6. **Instrument or system** (two versions, chosen by OP4).
   - If OP4 reads "instrument": the Gramian spectrum chooses as well as scale, so the per-mode
     ranking was the weak link. This becomes the positive result, and OP4 needs a full pilot and a
     sealed run first.
   - If OP4 reads "system" or "both": scale is what this flow asks an observer to read, even of the
     instrument that won on linear systems. OT's selection results are bounded by D6v3's and D7v3's
     settings. Include the recorded hypothesis about near-neutral directions, labelled as untested.
7. **What the theory does not reach.** Short: the propositions are preserved by Tao's averaged
   equation, so they cannot carry a regularity proof, and the paper makes no claim about
   regularity.
8. **What a practitioner can take from this.** Weight energy by sensitivity rather than using
   energy alone. In forced turbulence, start from scale or from a Lyapunov-informed choice. Check
   the world's regime before comparing selectors (OP1's lesson).

Appendices. The preregistration discipline and the graders. Every probe round and design change,
each with its reason and the READ-blind rule behind it (OP1's lift rule, OP2's statistic rule, OP4's
parameter rule). The failures and their repairs (D8's timeout and split rerun, lost logs, OP1's slow
regime). The theory-note checks.

## Figures (TikZ and pgfplots, to the standing illustration standard)

1. The consumer, its read operator and read distortion: a schematic.
2. The campaign map: gates by controls, cells won, level and lost (the table of OP3 Section 3, drawn).
3. D8 budgets per cell: BALL, KE, READ, ENSTROPHY and, after OP4, GRAM.
4. The first twelve picks of READ, BALL and GRAM in the wavevector plane, with the forcing shell.
5. OP1 forecast error against $r$ for READ, ENERGY and BALL, under TEND.
6. OP2 memory share against $r$.
7. OP4's Lyapunov spectrum, with the positive and near-neutral exponents marked.

## Claims the paper must not make (already corrected in the records)

- Not "read distortion beats every energy-type control". It is mixed against kinetic energy (D8).
- Not "BALL is new". It replicates Inubushi and Caulfield.
- Not anything about Navier–Stokes regularity.
- Not "the pilots are verdicts". They are pilot grades, recorded.
- Not OP1's $\nu = 0.03$, $n = 128$ world as evidence about selection. That world is in a slow regime
  where every EDMD forecast is worse than persistence.
- Not novelty for the Gramian instrument itself. Empirical Gramians are standard in sensor placement
  (Krener and Ide 2009, Singh and Hahn 2004).

## Open items before any prose

1. OP4's probe result, which chooses Section 6. If it reads "instrument", OP4 gets a full pilot and
   a sealed run before the paper.
2. The owner's choice between options (a) and (b) above.
3. A database search (Scholar, Web of Science) on sensitivity-weighted observable selection and on
   Gramian-based nudging, before any novelty sentence.
4. Venue, chosen by the owner after reading each candidate's generative-AI policy. Candidates by fit,
   not ranked: Physica D, Chaos, SIAM Journal on Applied Dynamical Systems, Journal of Fluid
   Mechanics (Rapids).
5. The prose standard (no em-dashes, colons or semicolons in prose; no mathematics in abstract or
   introduction; headings state findings), checked by scan, not by checklist.
