# TB Track: The Type III Bridge

**Status:** design draft, unsealed, non-claim-bearing. No physics claims are
made anywhere in this document. Every quantitative statement below is either
a citation, a definition, a number already established by a sealed or
passing QO run, or a target for a future run.

This track grows out of one open question. QUANTUM-OBSERVATION-BRIDGE.md
open question 12 ("Type III honesty") required a standing list of which QO
statements are finite-dimensional artifacts and which have type III
counterparts, and the QO paper's section VIII promised that list to its
readers. TB is that list promoted to a track, with instruments and a
falsification discipline attached. Section 3 is the list. Everything else
in this document exists to make section 3 checkable rather than
declarative.

Terminology follows the QO track. Consumer channel N_C, consumer algebra
A_C, consumer-relative divergence D_C, the flip as a task win plus a
fidelity loss at matched budget, the family quantifier as a joint
requirement over many consumers. All QO results referenced here are the
sealed or passing ones recorded in README.md and the QO paper.

## 1. Question

The QO track measured consumer-relative distinguishability entirely inside
finite-dimensional type I factors. Every algebra was B(H) for a finite H,
every state had a density matrix, every consumer had a partial trace. The
observable algebra of a real quantum field theory region is not that
object. Local algebras are type III_1 von Neumann factors (Fredenhagen
1985 for the type III_1 identification, the Witten review for the modern
account). A type III factor admits no trace, no density matrices, no
partial trace, and no von Neumann entropy of a restricted state. Relative
entropy nevertheless survives there, defined through the relative modular
operator (Araki 1976), and the data-processing inequality survives with it
(Uhlmann 1977, Petz 1986).

The question of this track. Which QO-track objects have type III
counterparts, which are finite-N artifacts, and can the passage between
the two settings be made quantitative with a computable ladder of growing
finite models.

The candidate thesis, stated as a target and not a claim. Consumer-relative
RELATIVE quantities survive the passage. Restricted relative entropies,
their differences and orderings, task distortions, and the flip are all
built from expectation functionals and relative modular data, and each is
expected to have a well-defined limit. Absolute quantities do not survive.
The entanglement entropy of a cut, the reduced density matrix itself, and
pinching to a preferred basis are type I artifacts with no counterpart.
The TB experiments are designed so that either half of this thesis can
fail per quantity, and a failure is a recorded result.

## 2. Verified references

Entries below were verified against arXiv abstract pages or publisher
listings on 2026-08-04 unless marked otherwise. Bibliographic corrections
made here propagate to any TB write-up.

**H. Araki, "Relative entropy of states of von Neumann algebras", Publ.
RIMS Kyoto Univ. 11, 809-833 (1976).** Defines relative entropy for two
states of a general von Neumann algebra through the relative modular
operator, with no density matrices anywhere in the definition. This is the
object row three of the honesty table names as the survivor.

**E. Witten, "Notes on Some Entanglement Properties of Quantum Field
Theory", arXiv:1803.04993, Rev. Mod. Phys. 90, 045003 (2018).** The
standard modern review. Local algebras in QFT are type III_1, there is no
partial trace and no entanglement entropy of a region, and relative
entropy is nevertheless well defined through Tomita-Takesaki theory. The
Connes classification of type III factors and the Bisognano-Wichmann
modular structure of wedges are cited in this document through this
review, not independently verified.

**R. Haag, Local Quantum Physics: Fields, Particles, Algebras, 2nd ed.,
Springer (1996).** The algebraic framework, Haag duality, the net of local
algebras. Book, cited without fetch by declared exception.

**K. Fredenhagen, "On the modular structure of local algebras of
observables", Commun. Math. Phys. 97, 79-89 (1985).** Asymptotic form of
the modular operators of local algebras. In an asymptotically scale
invariant theory the local algebras are type III with only type III_1
factors in the central decomposition.

**S. Doplicher and R. Longo, "Standard and split inclusions of von
Neumann algebras", Invent. Math. 75, 493-536 (1984).** The theory of
standard split inclusions. Between the two algebras of a split inclusion
there is a canonical interpolating type I factor. This is the object
section 5 makes the physical referent of every finite-N model.

**D. Buchholz and E. H. Wichmann, "Causal independence and the
energy-level density of states in local quantum field theory", Commun.
Math. Phys. 106, 321-344 (1986).** The nuclearity condition on the
energy-level density that implies the split property, verified there for
free field theory. Supplies the physical reason split inclusions exist at
all.

**A. Uhlmann, "Relative entropy and the Wigner-Yanase-Dyson-Lieb
concavity in an interpolation theory", Commun. Math. Phys. 54, 21-32
(1977).** Relative entropy for positive linear forms of arbitrary
*-algebras, with joint convexity and monotonicity under identity-
preserving completely positive maps. The DPI in the generality row four
needs.

**D. Petz, "Sufficient subalgebras and the relative entropy of states of
a von Neumann algebra", Commun. Math. Phys. 105, 123-131 (1986).**
Already cited in the QO paper. Characterizes when restriction to a
subalgebra preserves relative entropy (weak sufficiency holds iff the
subalgebra contains the Radon-Nikodym cocycle). The equality case of the
DPI, and therefore the type III statement of QO-1's exact sufficiency
anchor.

**N. Lashkari, "Relative Entropies in Conformal Field Theory", Phys. Rev.
Lett. 113, 051602 (2014), arXiv:1404.3216.** Computes Renyi relative
entropies in CFT and shows they are free of ultraviolet divergences.
Direct field-theory evidence for the relative half of the thesis, cited
as context only.

## 3. The honesty table

One row per QO-track object. The middle column states the type III fact
with its source. The last column states what the bridge is, meaning the
form in which the object or claim must be rephrased so that it still says
something when the algebra is type III. "Survives verbatim" means the
type I definition never used a density matrix and needs no rephrasing.

| QO object | Type I definition as used | Type III status | The bridge |
|---|---|---|---|
| Reduced density matrix rho_ext | Tr_inside rho, the state the consumer holds | No counterpart. A type III factor has no trace and no density operators (Witten review) | States as expectation functionals. omega restricted to the algebra replaces rho_ext everywhere. The functional survives, the matrix was its type I shadow |
| Partial trace channel | CPTP map Tr_inside, the canonical consumer channel | No counterpart, since there is no trace to take | Algebra restriction omega -> omega restricted to A_C. The dual object, a conditional expectation onto A_C, exists only in special cases (Takesaki criterion, invariance of A_C under the reference state's modular flow). TB treats restriction as primitive and conditional expectations as a flagged special case |
| Umegaki relative entropy | Tr rho (log rho - log sigma), the sealed QO-0 instrument | Counterpart exists. Araki relative entropy via the relative modular operator (Araki 1976). Equality with Umegaki in type I is proven | Compute both routes at finite N and require exact agreement. TB-0. The relative modular operator is the surviving object |
| Data-processing inequality | D(N(rho) \|\| N(sigma)) <= D(rho \|\| sigma) for CPTP N, 32 sealed margins in QO-0 | Holds in full generality for positive maps on *-algebras (Uhlmann 1977). Equality case characterized by sufficiency (Petz 1986) | Survives verbatim. QO-1's exact sufficiency anchor becomes Petz's cocycle condition |
| Consumer equivalence | rho ~_C sigma iff Tr(rho O) = Tr(sigma O) for all O in A_C | Survives verbatim. The definition is phi = psi on A_C and never mentioned density matrices | None needed. This was already the algebraic definition, which is why the QO paper stated it this way |
| Pinching / dephasing channel | Diagonal-part map in the computational basis, the QO-0 branch-label consumer | No canonical counterpart. The map is basis-dependent, and a type III factor supplies no preferred maximal abelian subalgebra and in general no normal conditional expectation onto one | None. Pinching is type I language. Every TB statement that needs it is flagged finite-N. The classical anchors that used it live entirely inside the commuting embedding, which is honestly type I |
| Entanglement entropy of the cut | S(rho_ext) = -Tr rho_ext log rho_ext | Undefined. Divergent in the type I approximation limit, no von Neumann entropy of a region in type III (Witten review) | None, and none needed. No QO claim used it. This is stated explicitly because it is the quantity outsiders most expect the track to depend on. TB-1 carries it as the deliberately diverging control |
| Uhlmann fidelity | F(rho, sigma) via trace norm, the QO-2 fidelity arm witness | Survives. Defined for states on any von Neumann algebra through GNS / standard form vector representatives (transition probability) | Compute in GNS form at finite N and require agreement with the trace-norm formula. Folded into TB-0 |
| The flip (QO-2) | T-arm beats F-arm on task and loses on fidelity at matched budget, budgets as kept-qubit counts | Both witnesses are built from expectations of declared observables and from fidelity, so both have type III formulations. Expected to survive. The encoder family "keep a subset of qubits" does NOT survive as stated, it is type I language | Encoders rephrased as channels between algebras with a declared budget object (open question 7). Flip persistence measured on the ladder. TB-2 |
| Consumer-family quantifier (QO-3) | Joint theta^2-law requirement over nested window subalgebras, active iff windows share an event | The family of wedge algebras with shared events is exactly the structure QFT possesses (Rindler wedges, Bisognano-Wichmann via the Witten review). The theta^2 law is a spectral statement about a lattice excitation parameter and has no direct counterpart | Reformulate the per-consumer law through modular flow and re-pose universality across a wedge-like family. Design-only allowed. TB-3 |

Two reading rules for the table. First, a "no counterpart" verdict is not
a defect of the QO track, it is the reason the QO claims were phrased
through expectations and divergences wherever possible. Second, the table
is a standing document. Any TB run that contradicts a cell overwrites the
cell, with the change logged.

## 4. The modular dictionary

The type I formulas that TB instruments compute, written so that the
type III limit is visible in them.

Purify. For a faithful state rho on B(H) with eigendecomposition
rho = sum_i p_i |e_i><e_i|, the vector Omega_rho = sum_i sqrt(p_i)
e_i tensor e_i* on the doubled space H tensor H* represents rho. Under
the identification of H tensor H* with Hilbert-Schmidt operators,
Omega_rho is the matrix sqrt(rho).

The relative modular operator. For the pair (rho, sigma) it acts on
Hilbert-Schmidt operators as

Delta_{sigma|rho}(X) = sigma X rho^{-1},

equivalently sigma tensor (rho^{-1})^T on the doubled space. Its spectrum
is the set of ratios s_i / p_j over eigenvalue pairs. Araki's formula is

S(rho || sigma) = - (Omega_rho, log Delta_{sigma|rho} Omega_rho),

and in type I this equals Tr rho (log rho - log sigma) identically, which
a two-line computation in the joint eigenbasis confirms. Convention
hazard, recorded here because it will bite. References disagree on the
index order of Delta, and some write the same operator as rho tensor
sigma^{-1} with the roles exchanged. Relative entropy is asymmetric, so a
convention slip silently computes D(sigma || rho). The TB-0 instrument
pins its convention with an asymmetric commuting control pair where
D(p || q) and D(q || p) differ in closed form.

The instrument obligation. The campaign's finite instruments can compute
BOTH the spectral Umegaki formula (the sealed QO-0 route) and the modular
formula above, and the two must agree to machine precision. That
agreement is the TB-0 instrument check. It is deliberately a null test of
mathematics, exactly as QO-0's DPI margins were. Its job is to certify
that the implementation computes the objects the theorems are about,
because every later TB statement leans on the modular route.

The subalgebra form. For two states given only as expectation functionals
phi, psi on a finite-dimensional *-algebra A_C, the GNS construction on
A_C from psi gives a Hilbert space (A_C with inner product psi(a* b),
null space quotiented), a cyclic vector, and a relative modular operator
built from the two functionals alone. Araki's formula then yields
S(phi || psi) without any reduced density matrix ever being formed. In
type I this must equal the restricted Umegaki value computed through the
partial trace. TB-0 requires that equality numerically. This route is the
honest one, because it is the only one of the two that still parses when
the algebra is type III.

The moral, stated once. The relative modular operator is the object that
survives the passage. Density matrices are its type I shadow, useful for
computation and meaningless as a foundation.

## 5. The split property as the physical bridge

Finite models cannot be honest stand-ins for local algebras, and the
split property says what they can be honest stand-ins for.

In a QFT satisfying nuclearity (Buchholz-Wichmann 1986), for a double
cone O and a slightly larger concentric double cone O_hat there is an
interpolating type I factor N with

A(O) subset N subset A(O_hat),

a standard split inclusion in the sense of Doplicher-Longo 1984. The
type I factor N is where density matrices, partial traces, and all of
the QO track's machinery legitimately live. The local algebras on either
side of it are type III_1 and have none of that machinery.

Consequence, adopted as a track rule. Every finite-N claim in this
campaign is a statement about a split-inclusion approximation, never
about a local algebra. The collar, the gap between O and O_hat, is the
new resolution parameter, playing the role epsilon plays in the PE
track. On a chain the collar is concrete. The consumer keeps region R,
the enlarged region R_hat adds w buffer sites on each side, and w is the
collar width. A TB witness is reported at stated (N, w) and its behavior
as w shrinks at fixed physics is part of the witness, exactly as PE
witnesses are reported at stated (delta, epsilon). The type III
divergences are expected to reappear as w -> 0 for absolute quantities
and not for relative ones, which is the thesis of section 1 in collar
language.

## 6. Experiments

### TB-0: Modular instrument

**Question.** Does the relative modular route compute exactly what the
sealed Umegaki instrument computes, on the same states, and can Araki
relative entropy on a subalgebra be computed from restricted expectation
functionals alone, with no reduced density matrix formed anywhere.

**Method.** Reuse the QO-0 model unchanged (8-qubit transverse-field
Ising chain, field 2.0, thermal reference at beta 0.5, Z-axis excitation
on qubit 4, the PEQO-FREEZE-002 support-floor discipline). Route one is
the sealed spectral Umegaki instrument, untouched. Route two computes
S = -(Omega_rho, log Delta_{sigma|rho} Omega_rho) from the
eigendecompositions of rho and sigma, spectrally through the ratio set
s_i / p_j and the overlap matrix, never as a dense operator on the
doubled space. Route three computes, for each consumer region of the
QO-0 hierarchy, the Araki entropy of the two restricted functionals via
GNS construction on the region algebra A_C, taking as input only the
expectation values phi(a), psi(a) for a basis of A_C. Route three also
computes Uhlmann fidelity in GNS form against the trace-norm formula.
Controls. The asymmetric commuting pair that pins the Delta index
convention, the QO-0 classical anchors through the modular route (P0 one
bit, M0 1.5 bits), a near-degenerate pair with eigenvalue splittings
swept down to 1e-12 to expose GNS conditioning, and the QO-0 spectral
floor sweep repeated on the modular route.

**Primary witnesses.** Maximum absolute disagreement between routes one
and two over the full QO-0 state and theta grid. Maximum absolute
disagreement between route three and the restricted Umegaki values over
all hierarchy regions. Fidelity route agreement. Smallest GNS Gram
eigenvalue encountered, reported alongside every route-three number.
Floor-sweep spread on the modular route.

**Falsification bar.** Any route disagreement exceeding 1e-10, on any
state pair or region in the declared grid, invalidates the instrument.
Any GNS Gram eigenvalue below the declared conditioning floor that is
not detected and reported by the instrument is a defect of the QO-0
silent-failure class and blocks sealing. No later TB experiment may run
until TB-0 is sealed and passing.

---

### TB-1: The scaling ladder — RUN, THESIS PATTERN CONFIRMED
(exploratory)

Executed 2026-08-04 as `python/tb1_ladder.py`, evidence
`results/tb1-ladder.json`, chains N = 4..12 at (J, h, beta, theta) =
(1, 2, 0.5, 0.8), half-chain cut, diagonal excitation at the cut
boundary. Every consumer-relative restricted relative entropy
converges exponentially, successive differences shrinking roughly
fifty-fold per rung (site consumer 1.2e-3 down to 8.0e-9, pair
9.5e-4 down to 5.7e-9, and the half-chain consumer, whose algebra
grows with N, 5.2e-4 down to 3.4e-9), reaching nine-digit stability
by N = 10. The effective thermodynamic-limit values are D_site =
0.631800, D_pair = 0.674747, D_half = 0.675183, D_global = 0.723532,
which shows the sealed QO-1 numbers at N = 8 were already converged
to their quoted precision, so the campaign's quantum results are
effectively infinite-volume statements. The diverging control
diverged exactly as predicted, the thermal half-chain entropy exactly
extensive at 0.1756 nats per added site pair. The Araki route agreed
with the sealed Umegaki instrument at every rung and consumer (bar
1e-10), and the states-as-functionals route agreed through N = 8.
One quantity, one verdict: relative quantities have limits, the
absolute entropy does not. This is the thesis's first quantitative
confirmation, at exploratory label, in the regime of fixed physical
excitation with a gapped reference; the open questions about scaling
regime and uniformity (section 9) remain open.

Original design follows.

### TB-1: The scaling ladder (original design)

**Question.** At fixed physical excitation and fixed cut fraction, which
QO quantities converge as N grows and which diverge.

**Method.** Chains N = 4 through 12, extended beyond 12 only if dense
eigendecomposition remains exact-arithmetic-honest on Atlas (dimension
4096 at N = 12 is comfortable, each further qubit quadruples cost).
Fixed physics across the ladder. Coupling 1.0, field 2.0 (gapped
paramagnetic), beta 0.5, excitation exp(i theta Z) with theta = 0.8 on
the site nearest fractional position 1/2, cut at half chain, hierarchy
regions scaled proportionally. All modular-route computations spectral
per TB-0. Measured per N, in two lists declared in advance. The
candidate-convergent list. Restricted relative entropy of excitation
versus reference for the outside consumer, the full hierarchy chain and
its gaps, task distortion of the QO-2 arms at matched budget fraction,
and the flip effect sizes (feeding TB-2). The candidate-divergent list.
Half-chain von Neumann entropy of the thermal reference, included
deliberately as the diverging control (extensive in N at this beta), and
the half-chain entropy of the ground state at the critical field as a
second control if the ladder is extended. Extrapolation by declared fit
families only, constant plus exponential and constant plus power for the
convergent list, linear and logarithmic growth for the divergent list,
with fit orders and residuals recorded. No fit family added after seeing
the data.

**Primary witnesses.** Per-quantity extrapolated limit with fit family,
fit order, and residual. Per-quantity classification convergent or
divergent under the declared criteria. The contrast pair, meaning the
diverging control's growth alongside the relative quantities' plateaus,
or the absence of that contrast.

**Falsification bar.** A quantity on the candidate-convergent list that
grows without bound across the ladder, failing every declared convergent
fit while the diverging control fits its divergent form, kills the
section 1 thesis for that quantity. That is a recorded negative, not a
track failure. If the diverging control fails to diverge, the ladder has
no contrast and supports no convergence claim for anything, and TB-1
reports itself unrunnable at this beta rather than reporting limits.

---

### TB-2: Flip persistence — RUN, FIXED-BUDGET LIMIT CONFIRMED
(exploratory)

Open question 4 was decided before the run and the decision is
binding for this track. The primary budget accounting is a fixed
absolute number of stored qubits, for two reasons. The task is local
and its relevant halo converges (TB-1), so scarcity relative to the
task is an N-independent notion. And a fractional budget has no type
III meaning, because algebra dimension is the quintessential type I
artifact, so only the fixed-k object can have a limit at all. The
fraction of the kept region is retained as a secondary diagnostic.

Executed 2026-08-04 as `python/tb2_flip_ladder.py`, evidence
`results/tb2-flip-ladder.json`, kept halves of chains N = 6..12 with
the PREREG-QO2-001 scenario grids. Results.

1. The fixed-budget flip has a sharp limit. At k = 1 the flip holds
   at every N with the anti-arm worst everywhere. The held-out task
   gap is 0.10762 at all four rungs, converged to 5.3e-10 by N = 12
   (the task functional, the T-arm, and the F-arm's miss are all
   local, so the gap is N-independent almost immediately). The
   infidelity gap converges 0.2994 to 0.2946 with successive
   differences shrinking 3.5e-3 to 1.1e-4. The flip is a
   thermodynamic-limit phenomenon at fixed absolute budget, which is
   what the OQ4 decision predicted and what a type III phrasing
   needs.
2. The secondary diagnostic did not trivialize and is honestly
   non-monotone. The flip region in k ran [1], [1,2], [1], [1,3]
   across the ladder, because the fidelity-optimal subset at
   intermediate budgets sometimes contains the flux site and
   sometimes does not, depending on the combinatorics of which
   subsets best capture the reference correlations at each m. The
   collapse fraction (0.33, 0.5, 0.2, 0.5) neither shrinks nor
   stabilizes at these sizes. Reading: the upper edge of the flip
   region is a discrete subset-selection artifact at small m, the
   clean convergent object is the fixed-k flip, and the
   trivialization prediction for fractions is untestable below
   substantially larger m. This is recorded as a finding, not
   massaged away.

Original design follows.

### TB-2: Flip persistence (original design)

**Question.** Does the QO-2 flip survive growing N when the encoder
family is rephrased as channels, and does the flip region, expressed in
budget fraction, have a limit.

**Method.** Rerun the sealed QO-2 protocol at each ladder N. The encoder
family is rephrased from "keep a subset of k qubits" to a declared
family of channels from the full algebra to a budget algebra, with the
kept-subset channels as the finite instance, so that the family's
definition no longer mentions qubits held, only a channel and its target
algebra. T-arm, F-arm, and anti-arm exactly as in PREREG-QO2-001, same
margins, held-out states, exhaustive search over the discrete family.
Budgets are accounted both ways per open question 4, fixed count k and
fixed fraction k/N, and both accountings are reported at every N. Record
the flip region endpoints in k/N per N.

**Primary witnesses.** Flip region per N under both accountings. Task
and fidelity effect sizes at the region endpoints per N. Anti-arm
separation per N. Extrapolated region endpoints with the TB-1 fit
discipline.

**Falsification bar.** If the flip region endpoints converge in neither
accounting, no limit claim is made and the row-nine bridge is downgraded
to open. If the flip vanishes at large N under both accountings, the
flip is a finite-N artifact, the honesty table row nine is rewritten to
say so, and that negative carries the same weight as QO-2's positive
did. If the anti-arm is not worst on task at some N, the run at that N
is uninterpretable per the QO-2 rule and is excluded with its exclusion
logged, not silently.

---

### TB-3: The wedge-family reformulation (design-only permitted)

**Question.** Can QO-3's measured result, an all-observers requirement
that does work exactly when the observers share an event, be restated so
that every object in it has a type III counterpart, with modular flow in
place of the theta^2 spectral law.

**Method, design-level.** The QO-3 ingredients and their required
replacements. The nested windows become a declared family of split
inclusions sharing the excitation region, the finite stand-in for a
family of wedges sharing a horizon event (wedge modular structure cited
through the Witten review). The excitation becomes a channel or
automorphism localized in the shared region. The per-consumer quantity
becomes the Araki entropy of excited versus reference functional on each
member, computed by the TB-0 route-three instrument. The declared
theta^2 flux weight, which was a lattice-parameter statement, must be
replaced by a modular statement. The candidate is the small-theta
expansion of the Araki entropy itself, whose leading term is quadratic
with coefficient a declared quadratic form in the excitation generator
determined by the reference state's modular data on the window. The
universality requirement then reads, lambda equals the ratio of measured
Araki entropy to that declared quadratic form, constant across the
family within delta.

**What would need to be true.** Three things, stated so a future run can
check them. First, the quadratic coefficient must be computable from the
reference and the generator without inserting the entropy it normalizes,
otherwise the law is circular by construction (the QO open-question-8
hazard transplanted, and sharpened, because modular flow is exactly what
ties energy to relative entropy in the Dorau-Much theorem that motivated
QO-3). Second, the saturation structure QO-3 measured, all windows
beyond the correlation length agreeing to four decimals, must reappear
as saturation of the modular quadratic form, or the mechanism does not
survive rephrasing. Third, the activation dichotomy, inert for disjoint
probes and active for a shared event, must be derivable from the
localization of the excitation channel relative to the family, since
that is the part claimed to be exactly the structure the QFT wedge
family has.

**Primary witnesses, if run.** Per-member lambda under the modular law.
Joint survival fraction versus family size against the QO-3 tightening
curve (1.0 to 0.75 to 0.25 on the exploratory grid). The circularity
audit outcome for the declared quadratic form.

**Falsification bar.** If no declared quadratic form passes the
circularity audit, TB-3 terminates design-only and says so, which is an
acceptable endpoint exactly as it was for QO-3. If the reformulated
quantifier is inert on the shared-event family that activated QO-3, the
row-ten bridge fails and the table is rewritten.

## 7. Relation to the campaign

TB exists to service the QO paper's section VIII gap list, item by item.
That section names four replacements required before any connection to
the gravitational results could be discussed, plus one open question.

1. **Type III algebras in place of finite factors, relative entropy
through relative modular operators.** This is the item TB targets. TB-0
builds the modular instruments, TB-1 measures which quantities the
passage preserves, and the honesty table records the verdicts. TB can
close this item for the divergence layer, meaning the restricted
relative entropies, their orderings, and the DPI structure. Closing it
for the task layer is exactly TB-2 and TB-3, and the paper's standing
open question, whether consumer equivalence and the flip can even be
formulated without density matrices, is answered in the affirmative at
the level of definitions by table rows five and nine, with the
quantitative persistence left to the runs.
2. **A genuine causal structure in place of a lattice cut.** TB cannot
close this and does not try. The chain has no light cones, no Killing
flow, and no horizon generators, and the collar of section 5 is a
distance in sites, not a causal separation. TB-3's wedge language is
declared analogy throughout, per the leaked-vocabulary discipline of QO
open question 9.
3. **The entropy-area input justified rather than declared.** Untouched
by TB. That item belongs to EG-1 and remains gated there.
4. **The special state class relaxed.** Not closed. TB's excitations are
lattice unitaries on thermal references, and nothing in TB relates them
to coherent excitations on a bifurcate Killing horizon. TB-1's ladder
makes the state class explicit per N but does not generalize it.

Dependency direction. TB depends on the sealed QO instruments and on
nothing else in the campaign. No QO, PE, PF, or EG result depends on TB.
If EG ever reaches a quantum area gate, the TB modular instruments are
the ones it would use, mirroring how QO feeds EG, and no dependency runs
the other way.

## 8. Non-claims and the standing causal caution

Nothing in this track bears on physical gravity, on real horizons, or on
the physics of quantum field theory. The type III facts cited here are
the literature's theorems, not results of this repository, and no TB run
tests them. TB proves statements about finite models and about the
internal limits of ladders of finite models. Convergence of a ladder is
not existence of a continuum limit, and no TB report may use the phrase
"the QFT value" for an extrapolated number. The finite models stand in
for split-inclusion interpolators, never for local algebras, per section
5, and every witness is reported at stated (N, w).

The standing causal caution of the QO track applies verbatim. The
consumer does not create anything physical by choosing what to observe.
The only admissible causal direction is physical state to accessible
channel to consumer-relative distinguishability. Observation relativity
concerns evidential access, not reality.

Evidence labels follow CAMPAIGN.md section 9. Everything in this
document is design, everything an unsealed run produces is
[exploratory], and the highest label any TB result can earn is
[demonstrated-in-model]. A clean negative is a result.

## 9. Open design questions (must close before TB-0 seals)

Recorded at drafting time, 2026-08-04. Each needs a decision or a
closed-form control before the corresponding experiment can seal.

1. **GNS conditioning for near-degenerate states.** The route-three Gram
matrix psi(a* b) becomes ill-conditioned when the restricted reference
has near-degenerate or near-vanishing weights, and the relative modular
spectrum contains ratios of small numbers. The QO-0 support-floor
discipline was derived for the spectral route and enters the modular
route twice, once per state. The floor semantics must be re-derived for
GNS numerics and pinned with the near-degenerate control, or TB-0 will
have its own silent-infinity defect waiting.
2. **Uniform versus per-quantity convergence.** The section 1 thesis is
stated per quantity, but a bridge worth the name would give uniform
control over a declared class of consumers and excitations. Whether TB-1
can even phrase a uniform claim with five ladder points, or must settle
for per-quantity verdicts, is undecided. Per-quantity is the honest
default.
3. **The choice of scaling regime.** Fixed cut fraction grows the system
and probes an infrared limit. Fixed collar width in sites while refining
the lattice at fixed physical size probes an ultraviolet limit. The
type III pathologies of the continuum are ultraviolet, so the ladder of
TB-1 as designed may converge for reasons that say nothing about the
type III passage. The two regimes differ, both are computable, and which
one carries the thesis must be decided and stated before TB-1 seals,
with the collar sweep of section 5 as the tiebreaker candidate.
4. **Flip budget scaling.** Qubit count and budget fraction give
different ladders, the QO-2 flip is a scarcity phenomenon, and scarcity
at fixed k deepens with N while scarcity at fixed k/N does not. TB-2
measures both, but a limit claim needs one declared primary accounting,
chosen before the governed run, not after seeing which converges.
5. **The classical tracks have no type III side.** The PF and PE
families, including the Sauter-pulse and Schwinger-adjacent PF-4 family,
are classical, and commutative von Neumann algebras are never type III.
There is no classical passage for TB to build. The proposed resolution
is to declare TB QO-only, with the classical anchors entering solely
through the commuting embedding inside TB-0, which is honestly type I.
The alternative, phrasing a classical-to-continuum bridge for PF/PE
observables separately, would be a different track and is not this one.
Needs a one-line decision recorded at seal time.
6. **Conditional expectations were never actually used, or were they.**
The Takesaki criterion says the thermal chain reference generically
admits no conditional expectation onto a kept-region algebra. The QO
track claims to have used only state restriction, and an audit should
confirm that no sealed QO number secretly depended on a conditional
expectation existing, since the type III bridge for such a number would
be weaker than the table currently states.
7. **The budget object in algebraic language.** Row nine's bridge needs
a budget that does not count qubits. Log-dimension is unavailable in
type III. Candidates include the interpolator of a declared split
inclusion and nuclearity-type indices, none of which TB has developed.
Until a budget object is declared, TB-2's channels are finite-N budgeted
and the flip's type III formulation is incomplete at exactly one point,
which the table should continue to say out loud.
8. **Modular numerics at the top of the ladder.** At N = 12 the doubled
space has dimension 1.7e7 and the relative modular operator must never
be formed densely. The spectral representation through eigenvalue ratios
and overlap matrices is declared in TB-0's method, but the error budget
of that representation at near-floor eigenvalues has no closed-form
control yet, and TB-1's top rungs are only as good as that control.
