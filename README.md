# Observation Theory Campaigns

Formerly `projection-fold-pair-creation`; renamed 2026-08-04 when the
work outgrew its first question. GitHub redirects the old name.

One program, six tracks. The shared question is what an observer with
restricted access to a system can see and what it can lawfully claim.
Each track makes that question concrete in a different setting, and all six run under one evidence discipline with sealed instruments,
preregistered claims, and append-only evidence records.

If you are new here, read this file top to bottom, then the one track
document that concerns you. Each track section below says what the track
asks in plain language, what it has established, and where its files
live.

## The six tracks

Each track keeps one color everywhere in this file: 🟦 folds, 🟥
entropy, 🟪 quantum, 🟫 the type-III bridge, 🟧 geometry, 🟨 Wolfram models. The letter
codes always accompany the chips, so nothing depends on color alone.

| Track | Short name | Question in one line | Status |
|---|---|---|---|
| 🟦 PF | Projection folds | Can a fold in how hidden motion maps to observed time imitate particle pair creation, quantitatively? | PF-0..PF-3 done, PF-4 first sealed run resolved neither-axis |
| 🟥 PE | Projection entropy | How much information does an observer lose at such a fold, and is that loss thermodynamic or merely observational? | Complete: instruments sealed, PE-0..PE-5 all measured |
| 🟪 QO | Quantum observation | Does the consumer-relative logic survive when the observer is a quantum channel, and does it say anything new? | Complete; two results confirmed under sealed preregistration |
| 🟫 TB | Type-III bridge | Which consumer-relative objects survive the passage from finite type I models to the type III algebras of quantum field theory? | Complete: TB-0..TB-3 all measured |
| 🟧 EG | Entropic geometry | Could spacetime-like structure emerge from how a projection organizes distinguishability? | EG-0/1/1b done: gate negative for spatial constraint mechanisms, but causal determinism passes on spacetime regions |
| 🟨 WM | Wolfram models | Which claimed phenomena of hypergraph and cellular-automaton physics are invariant, and which are observer or prescription artifacts? | Designed; WM-0 and WM-1 measured |

## Status ledger, one row per experiment

Class labels follow the evidence scheme at the end of this file; a seal
or registration ID means the row is governed by a hash-ledgered
document in `experiments/SEALS.md`.

| Experiment | Class | Evidence |
|---|---|---|
| 🟦 **PF-0** instrument net | `[proved]` + sealed ✅ PF0-FREEZE-001 | full N0/P0/P1/D0/M0/S0/E0 net in MATLAB and Python; branch counts 0→1→2 exact with signed count 0; separation exponent 0.500000000000; cross-language branch agreement 4.4e-16; same scenario on two substrates bit-identical outcome hashes |
| 🟦 **PF-1** structural stability | `[exploratory]` ✅ bar not tripped | fold persistence 1.000 to perturbation norm 0.12 (0.956 at 0.32, all window-loss, zero degeneracies); fitted exponent 0.500 at every norm; location and curvature deviations from first-order perturbation theory scale as norm² over seven decades |
| 🟦 **PF-2** generic Hamiltonian control | `[exploratory]` ✅ expected negative shape | 10^4-member symplectic ensemble: every member exactly 12 folds — fold counts are set by dynamics and measure, no universality; drift ≤ 4.3e-9 |
| 🟦 **PF-3** Land 2016 replication | `[replicated]` ✅ + 2 findings | printed Eq. 66 system vs printed Eq. 67 closed form agree to 5.7e-14 over 90 cells; threshold g_e > 2 exact everywhere; asymptote E_f = −(E_in+2M) to 1.4e-3. F1: trajectory-varying smoothing fakes below-threshold folds (1/λ kernel artifact). F2: the published threshold is the Cayley/Padé(1,1) pole of the kick generator — continuous accumulation conserves (ṫ+1)²−w² and never reverses (paper 3) |
| 🟦 **PF-4** Schwinger challenge, second sealed run | `[demonstrated-in-model]` ✅ PREREG-PF4-002 | bars set against model error per the §9.0 declaration, both met with room: the effective-gap model generalizes to unseen gaps at held/train ratio **0.38** (bar ≤ 2) — predicting fresh gaps better than it fits trained ones — while the Schwinger-shaped model is **3.14× worse** held-out (bar ≥ 2); controls exact per-member (z = 0.00); 10/12 + 7/8 cells usable, drift 6e-7. The Sauter family's suppression is a Gaussian measure tail in the effective gap and the Schwinger axis fails to compete: **the campaign's disciplined negative, sealed and earned**. Open summit: does any constructible family have a non-measure-tail exponent |
| 🟦 **PF-4** first sealed run | sealed verdict: **neither-axis** ⚖ PREREG-PF4-001 | governed run complete: all 20 probe-placed cells in band (12/12 train, 7/8 held usable), drift 6e-7, both C3/C4 controls exact per-member prescription agreement (z = 0.00). Fitted G slope β = 41.2 confirms the pilot two-point prediction 41.6, and G beats the Schwinger axis 3.28× on held-out weighted MSE — but the sealed bars (MSE_G ≤ 4, ratio ≥ 4) were not met: G organizes the family at the few-percent level yet residual gap-dependence at fixed d/E is many binomial σ, and S is worse but not 4× worse. Neither pass nor refutation; the residual structure is the next question. Sauter family exhibits a critical-field manifold E_crit(P) (deterministic vs fluctuation regimes) found in the 4-iteration pilot |
| 🟥 **PE-0** entropy controls | `[proved]` + sealed ✅ PEQO-FREEZE-002 | coarea branch weights closed-form: fold slice exactly 1 bit, M0 symmetric slice exactly 1.5 bits (weights ¼,½,¼), band edge → 1 bit, monotone/degenerate exactly 0 — multiplicity, not criticality, stores the information; both languages |
| 🟥 **PE-1** resolution scaling | `[demonstrated-in-model]` ✅ | binned fold-caustic entropy: H + log₂ε → 1 − 1/ln2 with deviations 4.5e-3 → 4.5e-4 shrinking as √ε; the inverse-square-root caustic is integrable, no entropy pathology |
| 🟥 **PE-2** reversible fold cycle | `[demonstrated-in-model]` ✅ | observed binned entropy swings 2.0708 bits along the trajectory while momentum reversal recovers the initial 10^4-member ensemble to 1.1e-14 and the reversed entropy curve retraces with defect exactly 0 — the entire change is observational; multiplicity staircase 4-8-12-13 with the signed path-degree rule at every level |
| 🟥 **PE-5** classical consumer hierarchy | `[demonstrated-in-model]` ✅ | exact finite sums on the double fold (3 branches, 2 orientations, so the rungs are genuinely distinct): H(Z|pos) 9.556 ≥ H(Z|pos,orient) 8.831 ≥ H(Z|pos,branch) 8.545 ≥ 0 bits — orientation worth 0.725 bits, branch label 0.285 more, residual = within-branch positional uncertainty; the classical shadow of the QO-1 chain, closing the loop the QO paper cites |
| 🟥 **PE-3** mixing versus folding | `[demonstrated-in-model]` ✅ | matched 2×2 (integrable vs chaotic dynamics × folding vs monotone observer, same trajectories): early entropy rise is common linear dispersion (5.71 vs 5.83 bits) but the late-time slope separates (−0.024 vs +0.030 bits/τ, integrable recurs while chaotic keeps growing) and slice multiplicity is set purely by the observer (mean ~10 per level folding, exactly 1 monotone, under either dynamics) — mixing pumps entropy, folds create multiplicity, independent axes |
| 🟥 **PE-4** noise and inaccessible hidden state | `[demonstrated-in-model]` ✅ | PE-2 cycle coupled to a 32-mode thermal bath: system-only flip fails monotonically in κ (recovery defect 0.33→1.89, retrace failure up to 5.87 bits) while the full flip including the bath recovers to 4e-15 at every κ — entropy production is consumer-relative reach, not dynamics; and the leak is invisible to coarse bath observables (I(Z;E_bath) pinned at the 0.009–0.016-bit estimator floor, mean bath energy even falls) while lost retraceability grows to ~6 bits — recovery needs microstate access |
| 🟪 **QO-0** quantum instrument | `[demonstrated-in-model]` + sealed ✅ PEQO-FREEZE-002 | classical anchors exact through the Umegaki divergence pathway (1.000000000000 and 1.500000000000 bits; orientation merge returns exactly the fold bit); 32 DPI margins all strictly positive (min 9.6e-8); 3 discovered defects now standing controls: no-signalling null (7e-16), symmetry null ((I+mX)/2 invisibility), support-floor silent infinity |
| 🟪 **QO-1** consumer hierarchy | `[demonstrated-in-model]` ✅ | degradation chain, ordering is a theorem: Z-excitation 0 → 0.668 → 0.675 → 0.724 nats (position-blind, largest gap at flux rung); X-excitation 0.048 → 0.116 → 0.148 → 0.301 (position-visible, largest gap interior) — where distinguishability lives moves with the sector; exact sufficiency anchor (DPI equality 1.1e-16) |
| 🟪 **QO-2** the flip | `[demonstrated-in-model]` ✅ PREREG-QO2-001 | governed run on fully disjoint grids: flip at k\*=1 at all 3 coupling points (primary: T-arm task 0.0000/infid 0.3637 vs F-arm 0.1076/0.0678, margins 0.01 cleared ×10/×30); anti-arm worst everywhere (≥1.25); flip vanishes when budget suffices — scarcity phenomenon, the classical budget-relativity flip reproduced quantum |
| 🟪 **QO-3** consumer-family quantifier | `[demonstrated-in-model]` ✅ PREREG-QO3-001 | two-sided, δ = 0.05 preregistered: disjoint probes INERT (joint = min single = 1.00, λ's agree ≤1.6e-3 grid-wide); shared-event nested windows ACTIVE (joint 0.25 < 1.00, tightening 1.0→0.75→0.25, surviving set exactly the weak-coupling row) — an all-observers requirement does work iff observers share events |
| 🟫 **TB-0** modular instrument | `[demonstrated-in-model]` ✅ | the Araki relative-modular route and the states-as-expectation-functionals route (no partial-trace primitive anywhere) both reproduce the sealed Umegaki instrument to 9.4e-16, six decades under the 1e-10 bar, across closed forms, the 8-qubit consumer sweep, a dephased pair, and a near-degenerate case; the asymmetric commuting control pins the modular index-order convention |
| 🟫 **TB-1** scaling ladder | `[demonstrated-in-model]` ✅ thesis pattern | chains N = 4..12: every consumer-relative restricted relative entropy converges exponentially (~50× per rung, 9-digit stable by N = 10; limits D_site 0.631800, D_pair 0.674747, D_half 0.675183) — including the half-chain consumer whose algebra grows with N — while the thermal half-chain entropy diverges exactly extensively (0.1756 nats/site-pair), the deliberate control. The sealed QO numbers at N = 8 were already converged to quoted precision: the campaign's quantum results are effectively infinite-volume statements |
| 🟫 **TB-2** flip persistence | `[demonstrated-in-model]` ✅ fixed-k limit | OQ4 decided before the run (budget = fixed absolute qubits; fractions have no type III meaning). At k = 1 the flip holds at every N = 6..12 with task gap 0.10762 constant to 5.3e-10 and infidelity gap converging 0.2994 → 0.2946: the flip is a thermodynamic-limit phenomenon at fixed budget. Honest finding: the flip region's upper edge in k is a subset-combinatorics artifact at small m ([1],[1,2],[1],[1,3]) and the fractional diagnostic is non-monotone at these sizes |
| 🟫 **TB-3** wedge family | `[demonstrated-in-model]` ✅ | the Kubo-Mori quadratic form (exact second-order Araki coefficient, assembled from reference modular data with no entropy in its code path) passes the circularity audit and replaces the lattice θ² flux weight: QO-3's shared-event family, which tightened 1.0→0.75→0.25 under the lattice weight, survives at 1.0 at every family size under the modular weight, with λ = 0.98854532044 constant to 13 digits across all 80 window×coupling combinations (lattice spread 0.079 mean) — universality becomes automatic under modular normalization; saturation reappears in Q itself, dichotomy derived from localization, TB-0 route agreement 1.9e-15. UPGRADED TO THEOREM `[proved]`: S(e^{iθP}ρe^{−iθP}‖ρ) = sin²θ·S(PρP‖ρ) exactly for any full-rank ρ and Hermitian involution P (proof in TYPE-III-BRIDGE.md; algebraic core kernel-checked in Lean 4/Mathlib, `proofs/PauliRotation.lean`; 120 random verifications worst 1.4e-14) — λ is the pure kinematic constant Σθ²sin²θ/Σθ⁴ of the grid |
| 🟧 **EG-0** entropy instrumentation | `[demonstrated-in-model]` ✅ | all four parts exact on closed forms: PE-0 reproduction (fold bit 1.4e-14, slice exactly 1.5 bits), conditional-entropy surface (aligned linear control = log₂100 to 1e-12, both resolution sweeps converge), fiber relative entropy (nested uniforms exact, Gaussian KL to 1.75e-10 with truncation floor identified, deformed-fold D field = binary closed form to 3.3e-16 over 90 bins), reparametrization invariance at the rounding floor both by relabeling and Jacobian re-gridding; unsealed pending MATLAB replication |
| 🟧 **EG-1** area-versus-volume gate | `[demonstrated-in-model]` ✅ negative | the designed stopping point, reached: over two decades of R with exact counts, Gauss-law/gauge-quotient ensembles give exactly (R−1)² interior distinctions given the boundary (volume law — mechanisms fail the primary count), and boundary-limited access leaves the hidden residual volume while only its image is area by construction; FINDING: the same Gauss-law ensemble carries an exact area-law cut mutual information 4R−5 — constraint structure puts area scaling into observer-relative correlations while interior independence stays extensive, exactly the count-split the OQ2 decision anticipated |
| 🟧 **EG-1b** mechanism discovery | `[demonstrated-in-model]` ✅ | CAUSAL DETERMINISM PASSES: entropy-density lemma (proved) forces any passing mechanism to zero bulk entropy density; causal-cone bound (proved) gives H(patch) ≤ 3R−2 for ANY deterministic radius-1 rule on spacetime regions; measured exactly — rules 90/150 saturate the bound (H = 3R−2 exactly, every R over two decades), rule 110 enumerated inside it, H(interior\|boundary) = 0 exactly; structural-origin audit: one noise bit per cell re-inflates to R² exactly (slope 2.0000) — the area law tracks determinism, nothing tuned |
| 🟧 **EG-2..5** matter deformation onward | design 📐 | conditionally unblocked on the causal-determinism substrate (deterministic hidden dynamics, spacetime regions, mandatory noise-audit control); spatial-region negative of EG-1 stands |
| 🟨 **WM-0** dimension instrument net | `[demonstrated-in-model]` ✅ + a bias finding | shell estimator exact on controls (path 1.000, 2D torus 2.000, 3D torus 2.958, tree flagged at 6.47 with growing local slope) — while the naive log-log ball-volume slope, the casual emergent-dimension estimator, reads LOW on every exact control (0.896/1.771/2.657), an O(1/r) bias of 0.10–0.34 at practical radii that any small-graph dimension claim inherits |
| 🟨 **WM-1** reversible-CA entropy cycle | `[demonstrated-in-model]` ✅ | Rule 122R (the featured example of Wolfram's own second-law writings), asymmetric confined random seed: declared block entropy rises 1.646 → 3.288 bits, then retraces bitwise exactly (defect 0.0) with exact microstate recovery — the second law of reversible computation is observational entropy, the PE-2 conclusion verbatim. Three instrument findings preserved: Rule 30R dense-phase locking, symmetric-init time-reflection recurrence, byte-block coarseness |
| 🟨 **WM-2** prescription audit | `[demonstrated-in-model]` ✅ trap discharged | string-substitution instance, three declared update orders: the causal-invariant sorting rule BA→AB agrees exactly under every prescription (final string and event count = inversion number, 406); the planted non-confluent rule {AB→B, BA→A} is flagged with three distinct terminal strings (B, BB, BBBB); the growth rule A→AB splits measured — conserved letter counts prescription-invariant, arrangement prescription-borne |
| 🟨 **WM-3** foliation covariance | `[demonstrated-in-model]` ✅ | genuine causal graphs from token genealogy: the sorting rule's invariants (55 events, 88 edges, depth 13, degree multiset) identical across prescriptions, while the trap's causal graphs differ radically (7 events/6 edges vs 4 events/0 edges — the rightmost order yields a causally disconnected history); across foliations of one graph, earliest and latest both achieve exactly the depth bound 13 while random extensions spread 19–26 slices — invariants frozen, simultaneity bookkeeping varying 2× |
| 🟨 **WM-4** held-out dimension scaling | `[demonstrated-in-model]` ✅ at measured sizes | minimal hypergraph rewriter for {{x,y},{x,z}}→{{x,z},{x,w},{y,w},{z,w}}, 11 generations, 1794 relations/897 vertices under one declared prescription: shell estimator gives d̂ = 2.305 on training radii, and on held-out radii the finite-dimension power law beats the exponential alternative by 40× in SSE (0.028 vs 1.092) — this rule genuinely passes the audit, finite-size crossover beyond the window not excluded |

Six sealed documents in the ledger (two instrument freezes, four
preregistrations), every one verifiable by blob hash. Three papers
published and a fourth drafted (the TB thermodynamic-limit paper,
compiled in `paper/`). The governed PREREG-PF4-002 run (bars set
against model error per the section 9.0 declaration) is in flight in
Atlas screen `pf4prereg2`.

### 🟦 PF, projection folds (the founding track)

A hidden system evolves smoothly in its own parameter. An observer
parameterizes what it sees by its own clock. If observed time, as a
function of the hidden parameter, has a turning point (a fold), then one
observed instant suddenly corresponds to two hidden states, which looks
like a pair of particles appearing. The kinematics of this is a theorem.
The scientific question is whether any honest dynamics produces folds
with the quantitative statistics of real pair production, above all the
Schwinger exponential, without the answer being inserted by hand.

Established so far. The instrument net is sealed (PF0-FREEZE-001), fold
detection and classification are validated against exact controls in
MATLAB and Python with cross-language agreement at machine precision.
Structural stability of folds matches first-order perturbation theory
over seven decades (PF-1). A generic bounded Hamiltonian produces folds
at a rate set rigidly by the dynamics and the sampling measure, with no
universality (PF-2, the negative control). A published classical
pair-creation calculation in Stueckelberg-Horwitz-Piron electrodynamics
was replicated exactly (PF-3), and the replication proved that the
published reversal threshold is a pole of the Cayley transform its
impulsive closure applies, while continuous integration of the same
force never reverses. That finding is now a binding design clause for
the remaining experiment.

Still open. PF-4, the sealed Schwinger challenge, is designed
(`experiments/PF4-DESIGN.md`) with the closure-prescription clause and
a planted-artifact control, and a candidate-family pilot is running.
The expected outcome remains a disciplined negative.

Key files. `experiments/CAMPAIGN.md` (the master design),
`experiments/PF3-PROVENANCE.md`, `experiments/PF4-DESIGN.md`,
`matlab/`, `python/shp_land2016.py`, `python/pf4_pilot.py`.
Paper. The Cayley-pole paper, DOI 10.5281/zenodo.21790096.

### 🟥 PE, projection entropy

When a fold doubles the number of hidden states behind one observation,
the observer's ignorance grows. This track measures that growth
exactly and keeps three different things called entropy strictly apart:
the observer's conditional ignorance, the coarse-grained entropy of
binned observations, and thermodynamic entropy production, which
requires physically destroying information and never follows from a
projection alone.

Established so far. Closed-form branch entropies (a fold carries
exactly one bit, the double-fold symmetric slice exactly one and one
half bits, degenerate monotone maps exactly zero, so multiplicity, not
criticality, stores the information). The fold caustic's binned entropy
converges to its differential limit with square-root-of-resolution
deviations. A reversible ensemble's observed entropy swings 2.07 bits
along a trajectory while momentum reversal recovers the initial hidden
state to machine precision, so the entire change is observational
(PE-2). Mixing and folding are independent axes, a matched two-by-two
shows sustained entropy growth follows the dynamics while slice
multiplicity follows the observer's singularities, and neither implies
the other (PE-3). The classical consumer hierarchy is measured exactly,
with lawful ordering and strictly positive gaps at every rung (PE-5).
Coupling to an inaccessible environment is what turns the ambiguity
into real entropy production, and the production is consumer-relative,
a full flip including the bath restores exact recovery at every
coupling while the leak leaves no trace in any coarse bath observable
(PE-4). Instruments sealed under PEQO-FREEZE-002.

The track is complete. All six experiments are measured.

Key files. `experiments/ENTROPY-TRACK.md`, `python/projection_fold.py`,
`python/pe2_reversible_cycle.py`, `matlab/run_pe0_entropy_controls.m`.
Paper. Entropy Across Singular Projections,
DOI 10.5281/zenodo.21789011.

### 🟪 QO, quantum observation

Observation Theory's classical observer reads the world through a fixed
operator and budget. This track replaces that read operator with a
quantum channel (a partial trace over an inaccessible region, a noisy
detector, a restricted algebra of observables) and asks whether the
consumer-relative structure survives and produces anything a plain
information theorist would not already know. The connection to gravity
literature is that several modern derivations of Einstein's equations
run through exactly this object, distinguishability of quantum states
from a restricted vantage point.

Established so far, all in small exactly computable spin models.
Instruments reproduce the classical fold entropies through the quantum
divergence pathway exactly and are sealed. A hierarchy of nested
consumers divides one fixed distinguishability total differently
depending on the excitation, so a certificate built from the wrong
observable class can be exactly vacuous. At scarce storage budgets an
encoder optimized for a declared energy functional beats a
fidelity-optimized encoder on that functional while losing badly on
fidelity, and the trade vanishes when storage suffices (the flip). A
consistency requirement imposed across many observers constrains the
model's couplings exactly when the observers witness one shared event
and is provably idle when they are probed separately. The flip and the
family result passed sealed preregistrations (PREREG-QO2-001,
PREREG-QO3-001) on grids fully disjoint from their exploratory runs
and carry the demonstrated-in-model label.

Still open. Nothing scheduled; the track is complete at its declared
scope. Its standing caution is printed in the paper: the consumer does
not create anything physical by choosing what to observe.

Key files. `experiments/QUANTUM-OBSERVATION-BRIDGE.md`,
`python/qo0_instrument.py` through `python/qo3_family.py`, the two
governed runners, `experiments/PREREG-QO2-001.md`,
`experiments/PREREG-QO3-001.md`.
Paper. Consumer-Relative Quantum Distinguishability on Causal
Boundaries, concept DOI 10.5281/zenodo.21789046 (v2 at
10.5281/zenodo.21789929).

### 🟫 TB, the type-III bridge

The campaign's quantum results were measured in finite matrix models,
where every state has a density matrix and every region a partial
trace. The local algebras of quantum field theory are type III von
Neumann factors, where none of those objects exist. This track asks
which of the campaign's consumer-relative objects survive that
passage, makes the answer a table rather than a slogan, and then
measures the approach to the limit on ladders of growing chains. The
thesis, now confirmed in its first regime, is that relative quantities
survive (relative entropies, their orderings, task distortions, the
flip) while absolute quantities were never load-bearing.

Established so far. TB-0, the type-III-native routes (the Araki
relative modular formula and states as expectation functionals with no
partial-trace primitive) reproduce the sealed finite instrument at
machine precision. TB-1, every consumer-relative restricted relative
entropy converges exponentially on chains N = 4..12 while the thermal
half-chain entropy diverges exactly extensively as the deliberate
control, with the corollary that the sealed QO numbers were already
infinite-volume values at their quoted precision. TB-2, the flip at
fixed absolute budget has a sharp thermodynamic limit (the budget
decision is recorded in the track document, since a fractional budget
has no type III meaning), and the flip region's upper edge was found
to be small-size combinatorics, reported as such. TB-3, the
consumer-family quantifier survives reformulation in modular language,
and improves. With the Kubo-Mori quadratic form as the flux weight the
shared-event family becomes universal with a single lambda constant to
thirteen digits across every window and coupling point, where the
lattice weight had tightened toward exclusion.

Still open. The IR-versus-UV scaling question and the remaining open
questions of the track document.

Key files. `experiments/TYPE-III-BRIDGE.md`, `python/tb0_modular.py`,
`python/tb1_ladder.py`, `python/tb2_flip_ladder.py`,
`python/tb3_wedge.py`.
Paper. Consumer-Relative Distinguishability in the Thermodynamic
Limit, drafted and compiled in `paper/`, not yet published.

### 🟧 EG, entropic geometry

The speculative track, deliberately gated. If fibers of a projection
carry entropy, could matter-induced changes in that entropy play the
role of gravity? The design confronts the idea with the hard gates in
order: entropy of a region must scale with its boundary area rather
than its volume (the expected point of failure), a local source must
produce inverse-square attraction without any inserted potential, a
first law must hold with independently defined quantities, and the
Poisson structure must survive held-out tests. A clean negative at the
area gate is a publishable and expected outcome.

Established so far. EG-0, the instrument layer, passes on every exact
closed-form control, including reparametrization invariance of every
witness, the track's defense against coordinate-artifact forces.
EG-1, the area gate, reached its designed negative with exact
arithmetic over two decades of region size, the measured constraint
mechanisms count volume-many interior distinctions given the
boundary, and an access limit is not a distinguishability limit. The
gate also produced a genuine finding, the Gauss-law ensemble carries
an exact area-law mutual information across the cut while its
interior count stays extensive, so area scaling lives in
observer-relative correlations, not in interior independence, for
this mechanism class. EG-1b, the discovery effort, then found the
passing mechanism by theory first. An entropy-density lemma forces
any passing mechanism to zero bulk entropy density, whose natural
non-inserted origin is deterministic local dynamics with the region
read as a spacetime region, and there the causal cone bounds the
patch entropy by its perimeter for any radius-one rule. Measured
exactly, rules 90 and 150 saturate the bound at every size over two
decades while one noise bit per cell re-inflates the same
construction to an exact volume law, so the area law tracks
determinism and nothing tuned. EG-2 through EG-5 are conditionally
unblocked on that substrate.

Key files. `experiments/ENTROPIC-GEOMETRY-TRACK.md`,
`python/eg0_instrument.py`, `python/eg1_area_gate.py`,
`python/eg1b_mechanism.py`.

### 🟨 WM, Wolfram models

The Wolfram Physics Project claims that simple rewriting systems
exhibit emergent dimension, special relativity from causal invariance,
particles as stable structures, and a second law from computational
irreducibility. Each of those claims rests on an inference pattern the
campaign has already made measurable, so this track runs the audits:
estimator validation before any dimension claim, update-order
independence as a prescription test with a planted non-confluent rule
as the trap, foliation covariance for particle claims with the
signed-versus-unsigned trichotomy, and the reversible-entropy protocol
for the second law. The framing is deliberately fair. The track tests
claims rather than people, and a claim that survives the audits comes
out stronger.

Established so far. WM-0, the shell dimension estimator is exact on
controls of known dimension with a regular tree flagged as
non-finite-dimensional, and the naive ball-volume slope that casual
measurements use was caught reading low on every exact control, a
finite-radius bias of 0.10 to 0.34 that small-graph dimension claims
inherit. WM-1, a second-order reversible automaton on Rule 122, the
featured example of the program's own second-law writings, raises its
declared coarse entropy and then retraces bitwise exactly with exact
microstate recovery, so the second law of reversible computation is
observational entropy, the campaign's PE-2 conclusion transplanted.
WM-2, the prescription audit on string substitution systems: the
causal-invariant sorting rule agrees exactly under every update order
(the event count is the inversion number), the planted non-confluent
rule is flagged with three distinct terminal strings, and the growth
rule splits cleanly into prescription-invariant conserved counts and
prescription-borne arrangement.

Still open. WM-3, foliation covariance on causal graphs; WM-4,
held-out dimension scaling on published hypergraph rules; the
hypergraph version of WM-2; the seven open questions of the track
document, led by whether the program's topological-obstruction
particles admit any computable signed invariant.

Key files. `experiments/WOLFRAM-MODELS-TRACK.md`,
`python/wm0_dimension.py`, `python/wm1_reversible_ca.py`,
`python/wm2_prescription.py`. Related prior work in
`C:\source\wolfram-observer-bridge`.

## The evidence discipline (applies to every track)

1. Instruments are validated against exact controls and sealed before
   claim-bearing use; the freezes fix every numerical bar in advance.
2. Claim-bearing results require a sealed preregistration naming the
   claim, the grid, the estimator, and the falsification bar before
   the run. Seals are git-blob hashes in `experiments/SEALS.md` (five
   entries: two freezes, three preregistrations, all verifiable with
   `git show <commit>:<path> | sha256sum`).
3. Every trajectory is counted; no conditioning on success.
4. Evidence records in `results/` are append-only hashed JSON
   sufficient for independent recomputation; every paper figure
   regenerates from them via `paper/make_figdata.py`.
5. Instrument defects found during shakedowns become permanent
   controls (seven so far). A clean negative is a result.

Evidence labels. `[proved]` mathematics, `[replicated]` published
benchmarks, `[demonstrated-in-model]` sealed bars passed,
`[exploratory]` unsealed work, `[refuted]` a sealed claim failed. No
result in this repository is evidence that physical spacetime is a
projection.

## Published papers

1. 🟥 Entropy Across Singular Projections (PE track),
   DOI 10.5281/zenodo.21789011.
2. 🟪 Consumer-Relative Quantum Distinguishability on Causal Boundaries
   (QO track), concept DOI 10.5281/zenodo.21789046.
3. 🟦 The Pair-Creation Threshold of Impulsive
   Stueckelberg-Horwitz-Piron Scattering Is a Cayley-Transform Pole
   (PF track), DOI 10.5281/zenodo.21790096.
4. 🟫 Consumer-Relative Distinguishability in the Thermodynamic Limit
   (TB track), drafted and compiled in `paper/`, not yet published.
5. 🟦 A Sealed Negative for Schwinger Scaling in a Resolved-Field
   Hidden-Dynamics Family (PF track), DOI 10.5281/zenodo.21798545.
6. 🟥 Three Sources of Observed Entropy in Reversible Hidden Dynamics
   (PE track completion), drafted and compiled in `paper/`, not yet
   published.

## Repository layout

- `experiments/` - track designs, seals, preregistrations, provenance.
- `matlab/` - Atlas MATLAB instruments and pilots (`+pf` package).
- `python/` - reference implementations, quantum instruments, governed
  runners, replications, pilots, and the test suite.
- `paper/` - six RevTeX papers, compiled PDFs, and the figure-data
  generator.
- `proofs/` - Lean 4 / Mathlib formalizations (machine-checked
  algebraic cores; build with `lake build` after `lake exe cache get`).
- `results/` - append-only hashed evidence records.
- `nrp/` - Kubernetes Job templates for large ensembles.

## Reproducing

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r python/requirements.txt
pytest -q python/tests            # full test suite
python python/qo0_instrument.py   # QO instruments + classical anchors
python python/pe2_reversible_cycle.py
python python/shp_land2016.py     # PF-3 replication + findings
python paper/make_figdata.py      # regenerate all figure data
```

MATLAB (Atlas): `addpath(genpath('matlab'))` then
`run_p0_instrument_net`, `run_pe0_entropy_controls`,
`run_p1_structural_stability`, `run_p2_toy_hamiltonian`.
