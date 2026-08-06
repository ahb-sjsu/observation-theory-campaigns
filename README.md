# Observation Theory Campaigns

Formerly `projection-fold-pair-creation`; renamed 2026-08-04 when the
work outgrew its first question. GitHub redirects the old name.

One program, seven tracks. The shared question is what an observer with
restricted access to a system can see and what it can lawfully claim.
Each track makes that question concrete in a different setting, and all seven run under one evidence discipline with sealed instruments,
preregistered claims, and append-only evidence records.

If you are new here, read this file top to bottom, then the one track
document that concerns you. Each track section below says what the track
asks in plain language, what it has established, and where its files
live.

## The seven tracks

Each track keeps one color everywhere in this file: 🟦 folds, 🟥
entropy, 🟪 quantum, 🟫 the type-III bridge, 🟧 geometry, 🟨 Wolfram models, ⬜ games and decisions. The letter
codes always accompany the chips, so nothing depends on color alone.

| Track | Short name | Question in one line | Status |
|---|---|---|---|
| 🟦 PF | Projection folds | Can a fold in how hidden motion maps to observed time imitate particle pair creation, quantitatively? | PF-0..4 done (PF4-002 sealed negative), PF4-003 in flight; PF-5 and PF-6 instruments ready, sealed gate runs + PF-7 remain |
| 🟥 PE | Projection entropy | How much information does an observer lose at such a fold, and is that loss thermodynamic or merely observational? | Complete: instruments sealed, PE-0..PE-5 all measured |
| 🟪 QO | Quantum observation | Does the consumer-relative logic survive when the observer is a quantum channel, and does it say anything new? | Complete; two results confirmed under sealed preregistration |
| 🟫 TB | Type-III bridge | Which consumer-relative objects survive the passage from finite type I models to the type III algebras of quantum field theory? | Complete: TB-0..TB-3 all measured |
| 🟧 EG | Entropic geometry | Could spacetime-like structure emerge from how a projection organizes distinguishability? | COMPLETE: EG-0..4 measured, EG-5 forbidden by its own bar; the arc's result is the exact tension between area-law counting and local field structure |
| 🟨 WM | Wolfram models | Which claimed phenomena of hypergraph and cellular-automaton physics are invariant, and which are observer or prescription artifacts? | Complete: WM-0..4 + WM-2h measured; the growth rules bookkeeping is prescription-borne |
| ⬜ GD | Games and decisions | Are the behavioral structures of imperfect-information domains (value of information, prospect-theoretic distortion, reference dependence) consumer-relative phenomena? | GD-0..3 measured (GD-1/GD-2 honest FAILs on their own bars, GD-1b/GD-2b passed corrected); prospect signatures emerge from budgets alone; GD-4..5 designed |

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
| 🟦 **PF4-003** frozen-measure hunt | sealed, run IN FLIGHT 🔄 PREREG-PF4-003 | the summit attempt: thermal-free pulse-train family, observable N_rev(P), claim log N_rev = a+b/P vs power law with held-out ratio bar 4 and a mandatory C5 planted-artifact trap; screen `pf4frozen`, harvest C5 verdict first |
| 🟦 **PF-5** instrument layer | instrument passing ✅ unsealed | complete census (4 declared classes, sums exactly, zero missing, failures counted — 200/200 nonfinite and 100/100 capped controls), continuous energy audit per member (bar 1e-5; harmonic control 4.4e-7, smoke 5.6e-7), declared orientation charge = sign(dt/dτ) with the path-degree rule exact at every generic level via the sealed polyline instrument, nan-safe deletion flagging (a statistic that drops a populated class is mechanically discrepant); claim-bearing PF-5 run awaits the PF4-003 harvest and a seal — PF-5/PF-6 are mandatory gates per CAMPAIGN.md §6 |
| 🟦 **PF-6** instrument layer | instrument passing ✅ unsealed | five audits at machine precision: translation covariance 2.7e-13 with fold worldpoints exactly equivariant; reparametrization bit-exact (path dev 0.0, per-worldline count exactly invariant, rate-per-τ scales exactly as predicted — the physical rate is per worldline, not per parameter tick); boost audit on the PF-3 hyperbolic family (commutation 4.5e-13, invariant 7.1e-11, future cone preserved — never-reverses is boost-invariant); gauge machinery exact on its EM control (Sauter tilt declared non-EM, clause binds when an EM family is declared); observer/detector audit — N(α) measured from the observer's record equals the detector-model prediction exactly at every α, the campaign's lawful-observer-dependence clause made mechanical |
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
| 🟧 **EG-2** matter deformation | `[demonstrated-in-model]` ✅ | matter (rule-150 defects in a rule-90 vacuum) is EXACTLY locally invisible — every window through length 64 at every position identical to vacuum for every source; widths 1/5/7 escape support only at the closed ring (one global parity bit); width 3 is the unique rank-losing sink (exactly 1 bit/step, deficit 60 = T) whose finite D field appears only at window length ≥160 in a period-64 self-similar pattern set by the automaton's algebra, not distance; causality null exact; reverse-engineering audit structural (rule substitution moves support, no reweighting can) |
| 🟧 **EG-3** local first law | `[demonstrated-in-model]` ✅ | δS = T·δQ EXACT on all held-out patterns with the three quantities independent (δQ = event count, T frozen at exactly 1 bit/event on one training injection, δS = rank); the finding: injections in the region's causal past are absorbed exactly (time-slice detectors provably blind — maximal ensemble), so the Clausius relation is an output precisely when the flux counts events crossing into the spacetime region; vacuum patch entropy 120 bits = exact perimeter form |
| 🟧 **EG-4** geometric equations | `[demonstrated-in-model]` ❌ Newtonian rejected | Poisson fails (Laplacian as large far from source as at it), Gauss fails (no monotone flank), superposition fails by DESTRUCTIVE INTERFERENCE — two separated sinks give global deficit 0 (both separations) vs additive 120, three give 1: deficits compose by GF(2) algebra, not addition; interior unevaluable; sink law itself exact (1 bit/step each in isolation) |
| 🟧 **EG-4b** discovery campaign | `[demonstrated-in-model]` — bar intact, obstructions mapped | 3 rounds, exact Walsh instruments (validated to 8e-17): (1) structured vacuum (Bernoulli 0.2) REMOVES the invisibility obstruction — graded field, 0.812-bit plateau with monotone flanks; but the Laplacian lives on the CAUSAL FRONT, not the source, and GF(2) has no continuous weak-field knob (superposition dev 3.6–6.3% doesn't shrink); (2) ring has no static limit (front self-collision flattens the field, 23% drift); (3) escape to infinity yields an EXACT static limit (changes 1e-3→0.0 under time doubling — reversible relaxation by radiating the transient away) but the converged field is FLAT (spread 5.3%) — statics carry no gradient; remaining obstruction precisely located: a passing substrate needs static response with spatial structure (higher dimension / richer alphabet / conserved charge), outside the exact-instrument regime |
| 🟧 **EG-4c** mini-campaign (attack on EG-4) | `[demonstrated-in-model]` — CLOSED, bar intact | round 1: dimensional-dilution hypothesis REFUTED — 2D GF(2) flat again; obstruction sharpened to the finite field itself (parity path-counting cannot decay, any dimension); round 2: wave substrate + Gaussian vacuum (exact covariance instrument, validated 9e-16) — strong-contrast scatterer gives a measured field with isotropy within spread AND superposition decaying with separation (1.13→0.46→0.056): distance = the continuous weak-field knob no finite field could provide; statics still transient-dominated at T≤96 (2D wave tails); round 3 long statics (T=256/512): the near-source field DECAYS with time (3e-5 → ~1e-6 bits) — the wave substrate's static limit is consistent with zero; CAMPAIGN CLOSED, bar intact, the obstruction measured on both passing substrate classes: all distinguishability gradients are radiative, and the three-way tension sharpens to "area law ⇒ zero entropy production ⇒ purely radiative relaxation ⇒ no static field for Poisson structure" |
| 🟧 **EG-4d** constraint-locked structure | `[demonstrated-in-model]` ✅ all 8 items | the escape route measured, with the claim demotion ruled BEFORE the run (constraints source geometry, distinguishability registers them — this does NOT support entropy sourcing geometry): lattice electromagnetism with the Gauss constraint, conditional-Gaussian instrument validated 5e-16; the D field is EXACTLY STATIC under the dynamics (drift 2e-18 over 400 steps — the anti-radiative witness every previous substrate failed), graded and monotone with measured falloff −2.275 vs the 2D-Coulomb −2, field superposition exact (4e-16), D scales exactly quadratically in charge (4.0), Gauss 9e-16 and curl-free 2e-18 on the MEASURED field — the missing EG-4 ingredient located: a local conservation law tying matter to boundary flux |
| 🟧 **EG-6** emergent Gauss law gate | `[demonstrated-in-model]` ✅ designed negative | can the constraint EMERGE rather than be declared? For linear local dynamics, frozen functionals = left null vectors, and Gauss structure = a translation-invariant LOCAL family of them; under a generic local deformation of BOTH blocks of the curl pair (a first one-block deformation falsely showed survival — the div∘curl identity was untouched, caught and recorded) the frozen space collapses 66 → 14 at ε = 10⁻³, the Gauss family's residual jumps 2e-15 → 0.88, and the 14 survivors are NON-LOCAL by the exact window criterion (max radius-1 window eigenvalue 0.2188 vs the 1.0000 a local frozen functional requires — the Maxwell control hits 1.0000 exactly): Gauss structure is an isolated algebraic point, declared or absent, never approached by local deformation — emergence of constraints needs a mechanism outside generic local linear dynamics |
| 🟧 **EG-5** black-hole benchmark | RULED CLOSED after reconsideration 🛑 | the design's own bar: EG-5 may not run unless EG-1..4 passed; EG-4 rejects the Newtonian limit (EG-4b leaves the bar intact), so the benchmark does not run — the arc closes on the measured tension: area-law counting demands zero entropy production, a graded local field forbids it |
| 🟨 **WM-0** dimension instrument net | `[demonstrated-in-model]` ✅ + a bias finding | shell estimator exact on controls (path 1.000, 2D torus 2.000, 3D torus 2.958, tree flagged at 6.47 with growing local slope) — while the naive log-log ball-volume slope, the casual emergent-dimension estimator, reads LOW on every exact control (0.896/1.771/2.657), an O(1/r) bias of 0.10–0.34 at practical radii that any small-graph dimension claim inherits |
| 🟨 **WM-1** reversible-CA entropy cycle | `[demonstrated-in-model]` ✅ | Rule 122R (the featured example of Wolfram's own second-law writings), asymmetric confined random seed: declared block entropy rises 1.646 → 3.288 bits, then retraces bitwise exactly (defect 0.0) with exact microstate recovery — the second law of reversible computation is observational entropy, the PE-2 conclusion verbatim. Three instrument findings preserved: Rule 30R dense-phase locking, symmetric-init time-reflection recurrence, byte-block coarseness |
| 🟨 **WM-2** prescription audit | `[demonstrated-in-model]` ✅ trap discharged | string-substitution instance, three declared update orders: the causal-invariant sorting rule BA→AB agrees exactly under every prescription (final string and event count = inversion number, 406); the planted non-confluent rule {AB→B, BA→A} is flagged with three distinct terminal strings (B, BB, BBBB); the growth rule A→AB splits measured — conserved letter counts prescription-invariant, arrangement prescription-borne |
| 🟨 **WM-3** foliation covariance | `[demonstrated-in-model]` ✅ | genuine causal graphs from token genealogy: the sorting rule's invariants (55 events, 88 edges, depth 13, degree multiset) identical across prescriptions, while the trap's causal graphs differ radically (7 events/6 edges vs 4 events/0 edges — the rightmost order yields a causally disconnected history); across foliations of one graph, earliest and latest both achieve exactly the depth bound 13 while random extensions spread 19–26 slices — invariants frozen, simultaneity bookkeeping varying 2× |
| 🟨 **WM-4** held-out dimension scaling | `[demonstrated-in-model]` ✅ at measured sizes | minimal hypergraph rewriter for {{x,y},{x,z}}→{{x,z},{x,w},{y,w},{z,w}}, 11 generations, 1794 relations/897 vertices under one declared prescription: shell estimator gives d̂ = 2.305 on training radii, and on held-out radii the finite-dimension power law beats the exponential alternative by 40× in SSE (0.028 vs 1.092) — this rule genuinely passes the audit, finite-size crossover beyond the window not excluded |
| ⬜ **GD-0** decision instruments | `[demonstrated-in-model]` ✅ | exact experiment values (uninformative and perfect closed forms to 1e-12); Blackwell garbling certificate (declared garble 5.6e-17 vs infeasible reverse 0.26 — nine orders of separation); garbling never raises any of 20 task values (worst gain 1e-16); BSC(e1) above BSC(e2) iff e1<=e2 across the grid; an incomparable pair whose declared tasks reverse preference (+0.05 / -0.15) — the GD-1 seed |
| ⬜ **GD-1** the flip meets Blackwell | `[refuted]` ✖ its own bar; ensemble stands | verdict FAIL as declared: the exhibit's incomparability bar thresholded a search residual at 0.01 and the measured 0.0045 fell short (the bar's design error, recorded). Controls exact: DPI control over 500 garbles x 205 tasks (worst task gain 3.3e-16); zero wedges among comparable pairs. The measurement: of 2000 random pairs, 767 Blackwell-incomparable, 281 unanimously ordered by all 7 f-divergences, and **281/281** carried a task reversal (max margin 0.078, median 0.021) |
| ⬜ **GD-1b** exhibit certificate | `[demonstrated-in-model]` ✅ | incomparability proved, not thresholded: conic-hull lower bound 0.00426 on the garbling residual (GD-1's search residual 0.00449 sits 5% above — the search was real), TV monotonicity settles the reverse. The rare-decisive-signal exhibit stands: A above B on every declared f-divergence (min margin 0.429) while the screening task prefers B by 0.0395 — scalar fidelity unanimity guarantees nothing about tasks outside Blackwell comparability |
| ⬜ **GD-2** budget flip in a game | `[refuted]` ✖ its own bar; values exact | verdict FAIL on one integer: the declaration claimed 6 tied fidelity-optimal partitions, the instrument counted 3 (the declaration tallied each 2-cell partition from both cells). Every closed-form VALUE matched to 1e-15 and H1/H2/C1-C3 passed, flip 0.6 against bar 0.5 |
| ⬜ **GD-2b** corrected declaration | `[demonstrated-in-model]` ✅ | the stake game exact: task-optimal 2-cell value 1, every MI-optimal 2-cell read worth exactly 0.4 = the no-information value — the fidelity-optimal budget spend buys exactly nothing, flip exactly 3/5. Ensemble: strict flip in **193/200** random games at budget 2 (median 0.070, max 0.328), 188/200 at budget 3 — fidelity-optimal information purchases are generically wrong at scarce budget, now against an adversary |
| ⬜ **GD-3** prospect signatures | `[demonstrated-in-model]` ✅ all audits + all 5 findings | budgeted consumers with NO weighting function, reference point, or loss-aversion input: sample-budget reader = exactly linear regressive weighting (closed form 6.8e-14, curvature 1.5e-14); log-odds reader = full inverse-S (endpoint secants 3.00 vs bar 1.1, middle 0.51, margins 0.099 vs 0.01); crossover tracks environment (0.5 → 0.338 ≈ logistic(−1)); loss-heavy environment → loss side read less compressed, ratio 1.208; diminishing sensitivity unambiguous (second diffs all negative). Zero-noise reads = exact identity; symmetric environments = exactly symmetric reads (1.5e-13); every distortion shrinks along every budget ladder |
| 🟨 **WM-2h** hypergraph prescription audit | \[demonstrated-in-model]\ ⚠ prescription-borne | the WM tracks sharpest audit: the flagship growth rules bulk bookkeeping is NOT prescription-invariant — five declared match orders give relation counts 1710–1882, vertex counts 855–941, and dimension estimates 2.43–2.88 (18% spread), so the WM-4 dimension claim inherits a measured prescription caveat at these sizes (unlike the string sorting rule, which was exact under every order); the fork-contraction trap fires with 3 distinct terminals (a bare path is confluent, verified en route) |

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

The PF-4 Schwinger challenge then ran its full arc. A four-iteration
pilot mapped the Sauter family's critical-field manifold. The first
sealed run returned the defined neither-axis verdict, teaching that
the effective-gap axis organizes the family at the few-percent level
without being a law. The second sealed run, with bars set against
model error as the owner rule demanded, passed both bars with room
and delivered the campaign's disciplined negative, the family's
suppression is a Gaussian measure tail in the effective gap and the
Schwinger axis fails to compete (the fifth paper). Two hunt probes
then located where a non-measure-tail exponent could live, the
post-crossing residual is log-linear in inverse momentum with the
Landau-Zener form explaining its slope quantitatively.

Still open, and in flight. PREREG-PF4-003, the frozen-measure
pulse-train family, is the sealed summit attempt on the open
question of whether any constructible family carries an action-set
exponent; its governed run is executing on Atlas. Behind it stand
the two mandatory gates of the master design, PF-5 (conservation and
complete accounting) and PF-6 (observer, Lorentz, and gauge audit),
whose instrument layers are now built and validated on exact
controls (`experiments/PF5-INSTRUMENT.md`,
`experiments/PF6-INSTRUMENT.md`) and await sealed runs on the family
the harvest selects. PF-7, the quantum-structure ceiling, stays
gated behind both.

Key files. `experiments/CAMPAIGN.md` (the master design),
`experiments/PF3-PROVENANCE.md`, `experiments/PF4-DESIGN.md`, the
five PF preregistrations and instrument documents in `experiments/`,
`matlab/`, `python/shp_land2016.py`, `python/pf4_pilot.py`,
`python/pf4_frozen_run.py`, `python/pf5_accounting.py`,
`python/pf6_covariance.py`.
Papers. The Cayley-pole paper, DOI 10.5281/zenodo.21790096, and A
Sealed Negative for Schwinger Scaling, DOI 10.5281/zenodo.21798545.

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
`python/pe2_reversible_cycle.py` through `python/pe5_hierarchy.py`,
`matlab/run_pe0_entropy_controls.m`.
Papers. Entropy Across Singular Projections,
DOI 10.5281/zenodo.21789011, and Three Sources of Observed Entropy in
Reversible Hidden Dynamics (the track's completion), compiled in
`paper/`, not yet published.

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
lattice weight had tightened toward exclusion. That constancy was then
upgraded to a theorem, relative entropy under a Hermitian-involution
rotation is exactly the squared sine of the angle times the involution
defect, proved in the paper, verified on random states to 1.4e-14, and
kernel-checked at its algebraic core in Lean 4 with Mathlib
(`proofs/PauliRotation.lean`), which retroactively identifies the
quantum track's theta-squared-law residuals as pure kinematics.

TB-1b then ran the declared collar-width sweep at fixed physics. At
every collar including zero the divergence converges in N to ten
digits, the value at the entangling surface is finite with a shallow
boundary layer growing inward, and the consumer-relative layer is
well-behaved exactly where the continuum absolute layer diverges,
locating the ultraviolet pathology in the absolute layer. A first
outside-collar design returned machine zeros and was recorded as the
no-signalling null reconfirmed, an excitation outside the consumer
is invisible at any distance.

Still open. The remaining open questions of the track document; the
true ultraviolet limit is a continuum question the lattice cannot
decide.

Key files. `experiments/TYPE-III-BRIDGE.md`, `python/tb0_modular.py`,
`python/tb1_ladder.py`, `python/tb2_flip_ladder.py`,
`python/tb3_wedge.py`.
Paper. Consumer-Relative Distinguishability in the Thermodynamic
Limit, completed with the wedge-family section and the exactness
theorem, compiled in `paper/`, not yet published.

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
patch entropy by its perimeter for any radius-one rule, saturated
exactly by measurement while one noise bit per cell re-inflates the
construction to an exact volume law.

On that substrate the arc then ran to its end. Matter is exactly
locally invisible, with one global parity bit for generic sources
and a unique width-three sink that destroys one bit per step and
carries the only finite field, an algebraically patterned one
(EG-2). A genuine first law holds exactly, with independently
defined flux, temperature, and entropy, once the flux counts the
events crossing into the spacetime region, because the maximal
ensemble absorbs anything earlier (EG-3). The geometry fails, the
field is non-Poisson and sink deficits interfere destructively, two
sinks canceling to zero against the additive one hundred twenty
(EG-4), so the black-hole benchmark is forbidden by its own bar
(EG-5). The track's result is the measured tension, area-law
counting demands zero entropy production while a graded local field
forbids it. Nothing bears on physical gravity.

Two discovery campaigns then attacked the EG-4 bar. The first
(EG-4b) removed two obstructions and located the third, a structured
vacuum restores a graded field where the maximal vacuum was blind,
escape to infinity yields an exact static limit by radiating the
transient away, but that static field is flat and GF(2) admits no
continuous weak-field knob. The second (EG-4c) refuted the
dimensional-dilution hypothesis, two-dimensional finite-field
substrates are flat again because parity path-counting cannot decay
in any dimension, and then moved to real amplitudes, the discrete
wave equation with a Gaussian vacuum and an exact covariance
instrument, where a strong-contrast scatterer gives a measured
isotropic field and superposition deviations decay cleanly with
separation, distance acting as the continuous weak-field knob no
finite field could provide. The long-time statics batch then
returned the closing answer, the near-source field decays as the
transient escapes, so the static limit is consistent with zero, and
the campaign closed with the bar intact and the tension sharpened,
the area law requires zero entropy production, which makes
relaxation purely radiative, which leaves no static field for the
Poisson structure to live in.

EG-4d then measured the one escape route, with its claim demotion
ruled before the run. A Gauss-type constraint is the standard
mechanism for persistent structure that survives its own relaxation,
and on lattice electromagnetism with a conditioned Gaussian vacuum
all eight declared items pass, the distinguishability field is
exactly static under the deterministic dynamics, graded with the
measured two-dimensional Coulomb falloff, exactly superposing,
exactly quadratic in the charge, and Gauss-exact on the measured
field. The honest reading is fixed by the ruling, constraints source
the geometry and distinguishability registers them exactly, so the
missing ingredient of the EG-4 bar is located, a local conservation
law tying matter to boundary flux, and entropy alone never supplied
it.

Two closing rulings finish the track. EG-5 stays closed after
reconsideration, since on the constrained substrate its items would
pass for constraint-inherited reasons with no horizon, no surface
gravity, and no temperature to test, the ambiguous scorecard the
design philosophy exists to prevent. EG-6, the successor gate, asks
whether the constraint can emerge rather than be declared, and
answers with the designed negative made exact. Under generic local
deformation the frozen-functional space collapses from sixty-six to
fourteen dimensions at strength one part in a thousand, the local
Gauss family is destroyed outright, and every survivor is non-local
by an exact window criterion. Constraint structure is an isolated
algebraic point, so within this class it is declared or absent,
never emergent, and the question the track leaves behind is why
nature has constraints at all.

Key files. `experiments/ENTROPIC-GEOMETRY-TRACK.md`,
`python/eg0_instrument.py`, `python/eg1_area_gate.py`,
`python/eg1b_mechanism.py`, `python/eg_ca_substrate.py`,
`python/eg2_matter.py`, `python/eg3_first_law.py`,
`python/eg4_geometry.py`, `python/eg4b_discovery.py`,
`python/eg4c_mini.py`, `python/eg4c2_wave.py`,
`python/eg4c3_statics.py`.
Paper. An Exact Area Gate for Entropic Accounts of Geometry,
compiled in `paper/`, not yet published.

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
prescription-borne arrangement. WM-3, causal-graph invariants built
from token genealogy are identical across update orders for the
causal-invariant rule while the planted trap's causal graphs differ
radically, and foliations move simultaneity bookkeeping by a factor
of two while the invariants stay frozen, with the extremal
foliations achieving the depth bound exactly. WM-4, a minimal
hypergraph rewriter's measured dimension passes a held-out scaling
test, the power law beating the exponential alternative forty-fold
in held-out error, so that rule's dimension claim genuinely survives
at measured sizes.

WM-2h, the hypergraph prescription audit, then delivered the track's
sharpest finding. Five declared match orders give the flagship
growth rule different relation counts (1710 to 1882), different
vertex counts, and dimension estimates spanning 2.43 to 2.88, an
eighteen percent spread, so the bulk bookkeeping is
prescription-borne and the WM-4 dimension claim inherits a measured
prescription caveat at these sizes, in sharp contrast to the string
sorting rule, which was exact under every order. The fork
contraction trap fires with three distinct terminals while the bare
path is confluent, verified en route, so the audit's teeth are
demonstrated.

Still open. The remaining open questions of the track document, led
by whether the program's topological-obstruction particles admit any
computable signed invariant.

Key files. `experiments/WOLFRAM-MODELS-TRACK.md`,
`python/wm0_dimension.py` through `python/wm4_hypergraph.py`,
`python/wm2h_prescription.py`. Related prior work in
`C:\source\wolfram-observer-bridge`.

### ⬜ GD, games and decisions under projection

The newest track. An information set in a game is the fiber of a
projection, many hidden histories behind one observed set, and
Blackwell's informativeness ordering is the decision-theoretic twin
of the data-processing inequality the campaign has used throughout.
The track asks whether the behavioral structures of
imperfect-information domains, the value of information, the
inverse-S probability weighting and loss asymmetry of prospect
theory, reference dependence, and budget-limited equilibrium play,
are consumer-relative phenomena derivable from declared channel,
task, and budget structure with nothing inserted. The
anti-circularity contract forbids weighting functions, post hoc
reference points, and loss-aversion coefficients as inputs. Nothing
in the track is a claim about human beings.

Established so far. GD-0, the instrument layer, exact experiment
values on closed-form controls, a certified Blackwell garbling
checker whose declared garble resolves nine orders below the
infeasible floor, garbling never raising any task value across the
battery, the binary-channel ordering reproduced across the grid, and
an incomparable experiment pair whose declared tasks reverse
preference, the seed of GD-1, where the campaign's flip meets
Blackwell's theorem.

GD-1 and GD-1b, the flip meets Blackwell. GD-1's verdict is FAIL as
declared, its exhibit bar thresholded a garbling search residual at
a round number 0.01 and the measured residual 0.0045 fell short,
even though the exhibit is provably incomparable, an honest negative
of the bar's own design. Its controls and ensemble stand, the
data-processing control exact across 500 garbles and 205 tasks, and
the substantive measurement, among 2000 random pairs 767 were
certified Blackwell-incomparable, 281 of those showed unanimous
ordering by all seven declared f-divergences, and all 281 carried a
task reversal in the declared battery. GD-1b redeclared the
certificate as proof rather than threshold, a conic-hull lower bound
on the garbling residual (0.00426, and the GD-1 search residual sits
five percent above it, the search was real) plus TV monotonicity for
the reverse direction, and passed all five items. The result, the
rare-decisive-signal exhibit, experiment A above B by every scalar
fidelity measure with minimum margin 0.429 while a declared
screening task strictly prefers B by 0.0395, because A's posteriors
never clear the action threshold and B's rare signal does. Scalar
fidelity unanimity guarantees nothing about tasks outside Blackwell
comparability, measured at 281 out of 281.

GD-2 and GD-2b, the budget flip in a game. A player buys a
coarsening of six hidden states under a cell budget and plays a
zero-sum stake game against an uninformed adversary, values exact by
piecewise-linear minimax. GD-2's verdict is FAIL on one integer, the
declaration double-counted its tied partitions (6 claimed, 3 true),
while every closed-form value matched to 1e-15. GD-2b corrected the
count and passed all six items. The stake-game exhibit is exact and
rational, the task-optimal 2-cell read is worth 1 while every
mutual-information-optimal 2-cell read is worth exactly 0.4, the
no-information value, so the fidelity-optimal budget spend buys
exactly nothing and the flip is exactly 3/5. The ensemble shows the
flip is generic, not constructed, a strict flip in 193 of 200 random
games at budget 2 and 188 of 200 at budget 3.

GD-3, prospect signatures from budgeted consumers. Three declared
consumers containing no weighting function, no reference point, and
no loss-aversion coefficient. All eight audits and all five declared
findings passed. A sample-budget reader produces exactly linear
regressive weighting, overweighting small probabilities and
underweighting large ones with zero inverse-S curvature, matching
its closed form to 6.8e-14. A log-odds reader under a Gaussian
budget produces the full inverse-S, endpoint slopes 3.00, middle
slope 0.51, and its crossover tracks the declared environment, 0.5
for the symmetric prior and 0.338 for the shifted one, matching
logistic(-1). A magnitude reader with a compressive code shows
unambiguous diminishing sensitivity, and a declared loss-heavy
environment makes losses read less compressed by the ratio 1.208
while the symmetric control is odd to 1.5e-13, so the asymmetry is
environment-borne, never machinery-borne. Every distortion shrinks
along every declared budget ladder and vanishes exactly at zero
noise. The signature set of prospect theory emerged from channel,
task, and budget declarations alone.

Designed and open. GD-4 (reference dependence as observer functional
choice under the lawful-observer clause), GD-5 (the Matejka-McKay
logit replication and equilibrium with budgeted consumers).

Key files. `experiments/GAMES-DECISIONS-TRACK.md`,
`python/gd0_instrument.py`, `python/gd1_flip_blackwell.py`,
`python/gd1b_exhibit_certificate.py`,
`python/gd2_budget_flip_game.py`,
`python/gd2b_budget_flip_game.py`,
`python/gd3_prospect_signatures.py`.

## The evidence discipline (applies to every track)

1. Instruments are validated against exact controls and sealed before
   claim-bearing use; the freezes fix every numerical bar in advance.
2. Claim-bearing results require a sealed preregistration naming the
   claim, the grid, the estimator, and the falsification bar before
   the run. Seals are git-blob hashes in `experiments/SEALS.md`
   (seven entries: two freezes, five preregistrations, all verifiable
   with `git show <commit>:<path> | sha256sum`).
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
   (TB track, completed with the TB-3 wedge-family reformulation, the
   fully Lean-verified Pauli-rotation exactness theorem, and the
   collar-width sweep), DOI 10.5281/zenodo.21814848.
5. 🟦 A Sealed Negative for Schwinger Scaling in a Resolved-Field
   Hidden-Dynamics Family (PF track), DOI 10.5281/zenodo.21798545.
6. 🟥 Three Sources of Observed Entropy in Reversible Hidden Dynamics
   (PE track completion), DOI 10.5281/zenodo.21814851.
7. 🟧 An Exact Area Gate for Entropic Accounts of Geometry (EG track,
   EG-0/1/1b), DOI 10.5281/zenodo.21814854.
8. 🟧 Radiative Geometry (EG track, EG-2..6 with the discovery
   campaigns, the constraint-locked closure, the emergence gate, and
   a citation-verified relation-to-prior-work section),
   DOI 10.5281/zenodo.21814858.
9. 🟨 Auditing Emergent Physics Claims in Rewriting Systems (the
   complete WM track), DOI 10.5281/zenodo.21814860.

## Repository layout

- `experiments/` - track designs, seals, preregistrations, provenance.
- `matlab/` - Atlas MATLAB instruments and pilots (`+pf` package).
- `python/` - reference implementations, quantum instruments, governed
  runners, replications, pilots, and the test suite.
- `paper/` - seven RevTeX papers, compiled PDFs, and the figure-data
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
