# QO Track: Consumer-Relative Quantum Distinguishability on Observer Algebras

**Status:** design draft, unsealed, non-claim-bearing. No physics claims are
made anywhere in this document. Every quantitative statement below is either
a citation, a definition, or a target for a future sealed run.

The intellectual content of sections 2 through 5 follows a reviewer analysis
(2026-08-04) of how this repository's projection and entropy work connects to
the modern gravity-from-information literature. The cautions in that analysis
are load-bearing and are reproduced here at full strength, not weakened.

Terminology follows the Observation Theory program (geometric-observation
repository): observer triple O = (C, G, B) with consumer C, output metric G,
and budget B; read metric P_C; consumer quotient X/~_C with kernel ker P_C;
the flip as the conjunction of a downstream win and a reconstruction loss at
matched budget, with an anti-arm control. This track replaces the classical
read operator with a quantum channel or an observer algebra and asks whether
the same consumer-relative structure survives, reduces correctly, and says
anything about the informational formulations of gravity.

## 1. Question

Modern derivations of gravitational field equations from information run
through one object: the distinguishability of quantum states as seen from a
restricted vantage point (a horizon exterior, a local Rindler wedge, an
algebra of accessible observables). Observation Theory's central move is that
distinguishability is not one thing: it is relative to a consumer, and the
distinctions a consumer needs for its task can be preserved while global
state fidelity is sacrificed, and vice versa.

The question of this track: does the consumer-relative structure of
Observation Theory (consumer equivalence, task-relative distortion, the
flip) exist and behave lawfully when the read operator is replaced by a
quantum channel or observer algebra, and when the task functionals are the
gravitationally relevant ones (energy flux, area response), all inside
finite-dimensional models where every quantity is computable?

The candidate unifying statement under test, stated as a target and not a
claim: geometry governs which distinctions are accessible to which
observers; gravity enforces consistency between changes in accessible
distinguishability, energy flux, and causal-boundary area. In Jacobson's
derivation the quantifier "for all local Rindler horizons" reads, in this
vocabulary, as a family of consumers: each consumer computes a different
restricted relative entropy, yet all must be compatible with one
observer-independent metric. Einstein's equation would then be the
consistency condition across the consumer family. Observation is
consumer-relative; truth is not (the metric is shared). Whether anything in
that reading is more than a relabeling is exactly what section 4 disciplines
and what QO-3 is designed to probe, model-internally only.

Position in the campaign: projection-fiber multiplicity (PF, instrument net
sealed) -> conditional entropy across singular projections (PE, instruments
passing) -> quantum channel distinguishability (QO, this track) -> area and
geometry (EG). QO is the third rung. It supplies the quantum objects that EG
section 3 currently lacks and inherits the PF/PE evidence discipline whole.

## 2. Context: what is informational in the lineage

The three citations below were verified during the drafting of
ENTROPIC-GEOMETRY-TRACK.md section 2 and are reused here consistently; they
are not re-verified in this document, and any bibliographic correction made
there propagates here.

**T. Jacobson, "Thermodynamics of Spacetime: The Einstein Equation of
State", arXiv:gr-qc/9504004, Phys. Rev. Lett. 75, 1260-1263 (1995).** The
lineage root. Demands that the Clausius relation delta Q = T delta S hold
for ALL local Rindler causal horizons and derives the Einstein equation as
an equation of state. What is informational in it: the derivation never uses
a specific matter model, only an entropy assigned to a causal boundary and
an energy flux across it; the universal quantifier over horizons, that is,
over uniformly accelerated observers and their accessible wedges, is what
turns a thermodynamic identity into a constraint on geometry. In this
track's vocabulary that quantifier is a consumer family, and the entropy-area
input is an assumed property of every consumer's boundary. Jacobson does not
say what the entropy counts; the quantifier structure is the part this track
borrows.

**G. Bianconi, "Gravity from entropy", arXiv:2408.14391, Phys. Rev. D 111,
066001 (2025).** Postulates an action that IS a quantum relative entropy:
the entropic action compares the spacetime metric, treated as an operator
playing the role of an effective density matrix, with a metric induced by
matter fields. What is informational in it: the dynamical variable of
gravity is placed directly inside a distinguishability functional, so the
field equations are extremization of a distinguishability between geometry
and matter. The action is postulated, not derived, and there is no observer
anywhere in the construction; the relative entropy compares two global
objects. This track's question to that construction is whose
distinguishability the action measures, which is precisely the question the
consumer layer exists to make well-posed.

**P. Dorau and A. Much, "From Quantum Relative Entropy to the Semiclassical
Einstein Equations", arXiv:2510.24491, listed journal reference Phys. Rev.
Lett. 136, 091602 (2026).** Uses Tomita-Takesaki modular theory to show that
the quantum relative entropy between the vacuum and coherent excitations of
a scalar field, restricted to a bifurcate Killing horizon, equals an
energy-flux expression; combined with the entropy-area input this yields the
semiclassical Einstein equations. What is informational in it: the theorem
is exactly of the form "restricted distinguishability equals a physical
flux". The restriction to the horizon algebra is the informational move; the
relative entropy is computed for the observer who can only measure outside,
and it is that observer-restricted quantity, not any global one, that equals
the flux. This is the closest existing result to the bridge object of
section 3, with two standing gaps this track must not paper over: the
entropy-area formula remains an input, and the state class (coherent
excitations on a Killing horizon) is special.

All three results are theoretical derivations, not experiments. Each takes
distinguishability or entropy as computable from an assumed structure; none
contains a consumer or task layer. The reviewer analysis locates the novelty
candidate exactly there and nowhere else; section 4 makes that binding.

## 3. The bridge objects

The objects below are definitions, stated so that QO-0 can compute all of
them in closed form or numerically in small dimension.

**The consumer channel.** A consumer C receives states through a quantum
channel N_C: rho -> rho_C. The channel is the quantum replacement for the
read operator. Canonical instances: partial trace over a causal region
(rho_ext = Tr_inside rho), a detector restriction (measure-and-record POVM),
an algebra restriction (conditional expectation onto a subalgebra A_C when
one exists). The classical read metric P_C = J^T G J is the commuting shadow
of this object.

**Consumer-relative distinguishability.** For states rho, sigma and a
divergence D (default: Umegaki quantum relative entropy
D(rho||sigma) = Tr rho (log rho - log sigma)),

D_C(rho||sigma) = D(N_C(rho)||N_C(sigma)).

**The data-processing inequality as the access law.** For every channel N_C,

D_C(rho||sigma) <= D(rho||sigma),

with equality only when the channel loses nothing the divergence can see.
This is exactly Observation Theory's law that claimable distinctions cannot
exceed underlying distinctions. Projection, coarse-graining, and
inaccessible regions only erase distinguishability, never create it. In the
PF/PE tracks this appeared as fiber multiplicity and conditional entropy;
here it is a theorem about channels, and QO-0's first job is to instrument
it, not to test whether mathematics is true, but to verify that the
implementation computes the objects the theorem is about.

**Horizon as observation boundary.** Operationally, a horizon is a
statement about which factor of a Hilbert space a consumer can touch:
H = H_accessible tensor H_inaccessible, with the consumer channel
N_C = Tr_inaccessible. Nothing in this definition invokes gravity; a
bipartite lattice cut is already an observation boundary in this sense. The
gravitational literature's horizons are the special case where the split is
causal and the restricted state is thermal with respect to a modular flow.
The finite toys of this track use the general case and must not claim the
special one.

**Consumer equivalence.** rho ~_C sigma iff Tr(rho O) = Tr(sigma O) for all
O in the consumer's algebra A_C. This is the quantum consumer quotient: the
world the consumer can act on, with unreadable distinctions collapsed. It is
the direct analogue of x ~_C x' iff x - x' in ker P_C.

**Task-relative distortion.** A task is a declared functional f on states
(or a declared family of observables). The task distortion of an encoding E
at budget B is the error in f, not the error in the state:

d_task(rho, E) = |f(rho) - f(decode(E(rho)))|,

against the global-fidelity distortion 1 - F(rho, decode(E(rho))). For this
track the declared gravitational task functionals are: local energy flux
T_ab k^a k^b (in the toy, a declared local energy-current observable),
null-congruence expansion, horizon-area variation (in the toy, a declared
area-analogue, see QO-3 and open question 3), detector response, curvature
invariants, and bulk-operator recoverability.

**Questions the task layer makes well-posed.** The known layer answers "how
distinguishable are two states through this channel". The task layer asks
"which distinction does THIS consumer need", and thereby makes the following
askable: how many qubits are needed to witness a given curvature
perturbation; which compressed boundary observations preserve the
Einstein-equation functional and which destroy it; whether one can estimate
gravitationally relevant stress-energy well while reconstructing the field
configuration poorly; when a horizon-entropy certificate is vacuous for a
curvature claim (the GO-3 certificate-vacuity question transplanted); and
whether observer algebras admit successive refinement with lawful
distinguishability ordering (the GO two-observer refinement question
transplanted).

**The gravitational flip hypothesis.** At a fixed boundary-information
budget, an encoding optimized to preserve the null energy flux functional
predicts the area response delta A better than a global-state-fidelity-
optimized encoding at matched budget, while having lower global state
fidelity. This is the quantum-gravity analogue of the classical flip, and it
is a hypothesis, not a result. QO-2 is its test.

## 4. Claim separation and anti-circularity

The track separates three claims that must not be conflated:

1. **Instrument claim:** consumer-relative divergences, DPI margins,
hierarchy orderings, and task distortions can be computed correctly in
finite dimension, verified against closed forms. This is QO-0/QO-1 and is
testable now.
2. **Structural claim:** in a declared model class, the gravitational flip
exists (QO-2), and consumer-family consistency conditions constrain the
model's coupling structure (QO-3), neither being inserted. This is the
campaign.
3. **Physical claim:** real gravity is the consistency condition across a
physical consumer family. Nothing in this track can support this claim and
no run will be labeled as doing so.

**The causal caution, as a contract clause.** The consumer does not create
gravity by choosing what to observe. The only admissible causal direction in
every model, every witness definition, and every sentence of every report
is:

physical state and geometry -> accessible channel -> consumer-relative
distinguishability.

Never consumer preference -> curvature. Observation relativity concerns
evidential access, not reality. Any model in which a consumer's choice of
algebra, task, or budget feeds back into the state, the couplings, or the
declared geometry is void under this contract, in the same way a
potential-equivalent source voids EG-2. Any write-up sentence that can be
read as "observers make gravity" fails review by construction.

**The relabeling clause.** Renaming known quantities in Observation Theory
vocabulary is NOT a contribution. Specifically not contributions: calling
relative entropy "distinguishability"; calling the DPI "the access law";
calling a partial trace "a consumer channel"; calling Dorau-Much's
horizon-restricted relative entropy "consumer-relative". All of that is
known mathematics under new names, and this document uses the names only for
continuity with the classical tracks. Novelty, if any exists, lives only in
the task layer: consumer equivalence classes for declared gravitational
functionals, task-relative distortion against those functionals, the flip
for a flux consumer, certificate vacuity, and refinement structure. If the
task layer produces nothing beyond what the divergence layer already gives,
that is a clean negative and will be reported as one.

**Forbidden inputs (contract list).** A QO model or encoder may not
contain, directly or through an equivalent fitted term:

- a task functional adjusted after inspecting which functional makes the
flip appear;
- an area-analogue selected after inspecting which choice makes QO-3's
proportionality hold (see open question 3);
- an encoder family for the fidelity arm chosen to be weak on the task by
construction (the arms must draw from the same family, differing only in
objective);
- postselection on states, cuts, or budgets that exhibit the flip;
- any use of the consumer's identity to modify the state or dynamics (the
causal caution above);
- budget accounting that differs between arms.

The model may contain: a declared finite-dimensional Hilbert space and
Hamiltonian or Gaussian structure, a declared cut, declared channels,
declared task functionals, and declared encoder families, all fixed before
any claim-bearing sweep.

## 5. Experiments

### QO-0: Finite-dimensional instrument — IMPLEMENTED, PASSING (exploratory)

Implemented 2026-08-04 as `python/qo0_instrument.py` with tests in
`python/tests/test_qo0.py`; evidence `results/qo0-instrument.json`. Declared
defaults recorded in the instrument (partially resolving open questions 4,
5, and 10 for this instrument; final closure at seal time): Umegaki
divergence in nats; the channel is the primitive object; commuting
embedding = branches by increasing tau as computational basis states,
coarea weights as eigenvalues, uniform fiber as reference, branch-label
algebra as the diagonal algebra.

Measured (corrected record, beta = 0.5): the classical anchors reproduce
through the divergence pathway exactly (P0 1.000000000000 bits, M0
1.500000000000 bits via S = log2 d - D(rho||I/d)/ln 2), and merging the
M0 orientation pair returns exactly the fold bit with nonnegative DPI
margin. Closed-form residuals <= 1.8e-15. On the 8-qubit gapped Ising
thermal model with a Z-axis excitation on a visible site: 32 DPI checks,
minimum margin +9.6e-8 (strictly positive and all finite), dephasing and
composition monotonicity clean, spectral-floor spread 0.0 across
1e-14..1e-10. Exploratory correlation-assistance observation:
distinguishability of the local excitation grows from 0.632 nats
(site-only consumer) to 0.675 nats (full outside region); correlated
neighbors carry witness information about a strictly local event.

Three instrument defects were discovered by failed first designs and are
now standing controls or bars:

- **Silent infinite divergence at the support floor.** At beta = 1 the
  thermal spectrum's smallest weight (~2e-12) sat at the 1e-12 support
  floor, so a full-rank reference read as rank-deficient, the full-state
  divergence went silently infinite, and global-versus-traced margins
  were inf minus finite: vacuously positive and invisible in the
  minimum. Models must now clear the floor by three decades (asserted)
  and every global divergence carries a finiteness assert. The first
  QO-0 evidence record had this flaw and was regenerated; the corrected
  record supersedes it.

- **No-signalling null.** A unitary (or any CPTP map) on the traced-out
  interior leaves the consumer's reduced state exactly unchanged; the
  first sweep design put the matter inside and every consumer divergence
  was exactly zero, so DPI passed trivially. Interior excitation is now an
  asserted null (measured |D| <= 5.6e-16). Consequence recorded for EG-2:
  matter must deform what the consumer's channel actually reads.
- **Symmetry null.** The Ising thermal single-site reduced state is
  exactly (I + m X)/2 by global spin-flip symmetry, so an X-axis rotation
  commutes with it and is invisible to the site-only consumer even on its
  own qubit. Whether a consumer can see an excitation depends on the
  interplay of excitation direction and state symmetry, not only on
  locality; this is a concrete finite-dimensional instance of the
  certificate-vacuity question.

**Question.** Do the consumer-channel instruments compute divergences,
restricted divergences, and DPI margins correctly in an explicit small
model?

**Method.** A small explicit model, total dimension at most 2^10: a
bipartite spin lattice or tensor-network toy with a declared inside/outside
cut. Vacuum reference: the ground state of a declared gapped local
Hamiltonian, or a Gaussian (quasi-free) reference state where covariance-
matrix formulas give closed forms. Matter: a local excitation (local
operator applied to the vacuum, or a coherent shift in the Gaussian case).
Channels: partial trace over the inside, local dephasing at declared
strength, restriction to a declared subalgebra. Compute D(rho||sigma) and
D_C(rho||sigma) across the channel family; verify DPI numerically at every
point of a parameter sweep; verify monotonicity of D_C under channel
composition (composing two channels never increases the divergence); verify
closed-form values on 2-qubit cases where relative entropy is analytic
(orthogonal states, identical states, known qubit pairs under partial trace
and dephasing). Substrate: numpy/scipy; cross-language replication is not
required for this track, breaking with PF-0 practice, because the objects
are standard linear algebra and the risk profile is numerical (degenerate
spectra, log of near-singular matrices), not implementation divergence. That
risk is handled by the closed-form net and by spectral-floor sweeps.

**Primary witnesses.** Divergence error against closed forms; minimum DPI
margin over the sweep (must be >= 0 within numerical floor); composition-
monotonicity margin; behavior of all witnesses under declared spectral
regularization as the floor is refined.

**Falsification bar.** Any closed-form disagreement beyond the sealed
tolerance, any negative DPI or composition margin beyond the numerical
floor, or any witness that fails to converge as the spectral floor is
refined invalidates the instrument. No later QO experiment may run until
QO-0 is sealed and passing.

---

### QO-1: Consumer hierarchy — IMPLEMENTED, PASSING (exploratory)

Implemented 2026-08-04 as `python/qo1_hierarchy.py` with tests in
`python/tests/test_qo1.py`; evidence `results/qo1-hierarchy.json`. The
four levels are realized as a degradation chain (each weaker consumer is
a channel composed onto the stronger one's output), so the ordering is a
theorem and any inversion is a bug; none was measured. The declared flux
stand-in is the transverse-field energy density on the excited site
(open question 8: declared, not derived).

Measured, both at theta = 0.8 (stable across 0.4 and 1.2):

- Z-excitation chain: 0.000000 <= 0.667985 <= 0.675183 <= 0.723532
  nats. The position-only consumer sees exactly nothing (commutation
  theorem, asserted); the largest gap sits at the flux rung. A position
  certificate is vacuous for this excitation.
- X-excitation chain: 0.047621 <= 0.116320 <= 0.148405 <= 0.300990
  nats. The position consumer sees it through correlations; the largest
  gap sits at the interior rung.
- Where the distinguishing information lives moves with the excitation
  sector: the same four consumers, ranked the same way by DPI, divide
  the same total distinguishability entirely differently. This is the
  task layer measured, not relabeled.
- Classical anchors in closed form: merging the M0 orientation pair
  against the uniform fiber is an exact DPI equality (sufficiency; gap
  1.1e-16), and against the asymmetric reference the gap matches
  ln2/4 - ln(4/3)/2 to twelve decimals. Spectral-floor spread 0.0.

**Question.** Do nested observer algebras produce the lawful
distinguishability ordering, and with measurable, interpretable gaps?

**Method.** Declare a nested family A_1 subset A_2 subset ... subset A_n:
position-type observables only; position plus the declared flux observable;
the full boundary algebra; the full state (identity channel). For the
vacuum-versus-excitation pair of QO-0, measure D_{A_1} <= D_{A_2} <= ...
<= D and record every gap. The gaps are the value of each additional
observable class to the distinction at hand. PE-5's consumer hierarchy
(H(Z|X_pos) >= H(Z|X_pos,orient) >= H(Z|X_branch) >= 0) is the classical
shadow of this experiment, and QO-1's design deliberately mirrors it so that
section 6's reduction check has matched objects on both sides.

**Primary witnesses.** The full ordered chain of restricted divergences;
each gap with its numerical uncertainty; stability of the ordering and gaps
under the QO-0 regularization sweep; the location of the largest gap (which
observable class carries the distinction).

**Falsification bar.** Any measured inversion of the ordering beyond
numerical floor invalidates the instrument (the ordering is a theorem; an
inversion is a bug, and finding it before it contaminates QO-2 is this
experiment's purpose). A hierarchy in which all gaps are degenerate (every
algebra sees the full distinction, or none does) fails the design, not the
theory: it means the model or the excitation was chosen without enough
structure for the task layer to be non-trivial, and QO-2 may not run on that
model.

---

### QO-2: The gravitational flip — IMPLEMENTED, FLIP CONFIRMED IN-MODEL
(exploratory)

Implemented 2026-08-04 as `python/qo2_flip.py` with tests in
`python/tests/test_qo2.py` (including a 2-qubit analytic flip control that
no optimizer can fake, answering open question 2 for this model class);
evidence `results/qo2-flip.json`. The encoder family is discrete and
exhaustively searched, so there is no optimization artifact to classify.
The declared task is the flux functional only; the area-response variant
remains deferred on open question 3. The anti-arm (T-arm encoder with the
flux qubit Z-pinched at identical budget, per open question 7) was worst
on task at every budget (1.289 against 0.118 and 0.000), so the runs are
interpretable.

Measured on held-out states, budgets in stored qubit slots:

- k = 1: T-arm keeps the flux site: task distortion exactly 0, infidelity
  0.326. F-arm keeps the strong site: task distortion 0.118, infidelity
  0.069. FLIP: the task-optimized encoder wins the task outright and is
  4.7x worse on global fidelity.
- k = 2: same split (F-arm keeps the correlated strong pair rather than
  adding the weakly-excited flux qubit: fidelity prefers preserving
  correlation structure). FLIP again.
- k = 3: the fidelity-optimal subset now contains the flux qubit, both
  arms reach task distortion 0, and the flip vanishes.

The flip region is contiguous (budgets 1 and 2) and the flip dies exactly
when the budget suffices to keep everything task-relevant: the flip is a
scarcity phenomenon, which is the budget-relativity structure the
classical Observation Theory flip predicts. This completes paper step 5
(quantum flip for an energy-flux consumer, positive sign) at exploratory
label; a sealed prereg would be required before the paper can claim it.

**Question.** At matched budget, does an encoding optimized for the flux
functional beat a fidelity-optimized encoding on area-response prediction
while losing on global fidelity?

**Method.** Fix the QO-0 model, cut, and a declared flux functional (the
toy's stand-in for T_ab k^a k^b, declared at Level 0; see open question 8)
and a declared area-response functional. Two encoders from the same declared
family at matched budget, where budget is qubit count or measurement count,
declared once and audited identically for both arms: an F-arm trained or
constructed to maximize global state fidelity, and a T-arm trained or
constructed to minimize task distortion on the flux functional. An anti-arm
that deliberately destroys the flux-relevant observables at the same budget
is mandatory, mirroring the classical flip protocol: if the anti-arm is not
clearly worst on the task, the declared functional is not what governs the
task and the run is uninterpretable rather than positive. Sweep the budget
over a declared range and record both distortions for all arms at every
budget.

**Primary witnesses.** Task distortion on the flux/area-response functional
per arm per budget; global fidelity per arm per budget; the flip indicator
(T-arm strictly better on task AND strictly worse on fidelity) with effect
sizes at each budget; anti-arm separation; stability of the flip region
under the declared encoder-family variations.

**Falsification bar.** The flip is confirmed only if the T-arm wins on task
and loses on fidelity, both beyond sealed margins, on held-out states not
used in encoder construction, across a contiguous budget region, with the
anti-arm worst on task. If the F-arm matches the T-arm on task at all
budgets, the gravitational functionals are fidelity-aligned in this model
class and the flip hypothesis is refuted there; that is a clean negative and
a publishable structural fact. If the flip appears only at isolated budgets
or only on training states, it is classified as an optimization artifact.

---

### QO-3: Consistency across a consumer family

**Question.** Model-internally only: if a declared area-analogue is fixed,
does requiring D_C proportional to that area-analogue for ALL consumers in a
declared family constrain the model's coupling structure, in the way
Jacobson's all-horizons quantifier constrains geometry?

**Method (design-level).** Declare a family of consumers (a set of cuts
and/or algebra restrictions playing the role of the Rindler-wedge family)
and a declared area-analogue for each (see open question 3 for why this
declaration is the hard part). For a parameterized family of model
Hamiltonians (couplings as free parameters), measure for each consumer the
proportionality residual between D_C(vacuum, excitation family) and the
declared area-analogue response. Ask whether the joint requirement (small
residual for every consumer simultaneously) selects a lower-dimensional
subset of coupling space, and whether that subset is characterizable.

**Primary witnesses.** Per-consumer proportionality residual; the measure
of coupling space surviving the joint requirement at declared residual
thresholds; sensitivity of the surviving set to the family's size (does
adding consumers genuinely tighten the constraint or is the quantifier
inert).

**Falsification bar.** If the joint requirement over the full declared
family constrains couplings no more than any single consumer does, the
Jacobson-quantifier reading fails in this model class: the "consistency
across observers" story adds nothing, and that negative is the result. If no
point of coupling space satisfies the requirement, the declared
area-analogue is wrong for this model class, which is a statement about the
declaration, not about gravity.

**Standing label.** QO-3 is explicitly the hardest and most speculative
experiment in this track. It may terminate as design-only: a precise
statement of what would have to be declared and measured, published without
a run, is an acceptable and honest endpoint for it.

## 6. Relation to the classical tracks

The quantum objects must reduce to the classical ones in the commuting
limit, and the reduction is a mandatory instrument check, not an aspiration.

When all states and channels are simultaneously diagonalizable (classical
probability embedded in quantum), D becomes Kullback-Leibler divergence, the
consumer channel becomes a stochastic map, consumer equivalence becomes the
classical quotient, and the QO-1 hierarchy becomes exactly the PE-5
conditional-entropy ordering. Two anchors from the sealed and passing
classical work pin this limit numerically:

- the P0 fold's branch distinction carries exactly 1 bit at every two-branch
slice (PE-0, both languages);
- the M0 double fold at the symmetric slice carries exactly 1.5 bits with
branch weights (1/4, 1/2, 1/4) (PE-0, both languages).

QO-0 must include a commuting embedding of these two controls (diagonal
density matrices whose eigenvalue distributions are the PE-0 branch-weight
distributions, with the branch-label observable as the consumer algebra) and
must reproduce 1 bit and 1.5 bits to the PE-0 tolerances. A quantum
instrument that cannot reproduce the classical anchors in the classical
limit is invalid regardless of what else it computes. Note open question 10:
the embedding must be declared, because more than one exists.

In the other direction, nothing classical constrains the genuinely quantum
content (non-commuting algebras, entangled references). The classical tracks
anchor the limit; they cannot certify the interior.

Progression map:

```text
PF   projection-fiber multiplicity      instrument net sealed
      |
PE   conditional entropy                instruments passing, unsealed
      |
QO   quantum channel distinguishability this track
      |
EG   area and geometry                  design draft, gated on PE
```

QO feeds EG in one specific place: EG section 3's relative entropy between
matter-deformed and vacuum fiber measures is the classical shadow of
D_C(rho_matter || rho_vac), and if EG ever reaches its area gate with
quantum models, the QO instruments are the ones it will use. No EG
dependency runs the other way.

## 7. Paper boundary

Working title: "Consumer-Relative Quantum Distinguishability on Causal
Boundaries".

The paper's scope is exactly six steps, following the reviewer analysis:

1. replace the classical read operator with a quantum channel or observer
algebra;
2. define consumer equivalence and task-relative distortion in that setting;
3. relate both to quantum relative entropy and the data-processing
inequality, with the relabeling clause of section 4 stated in the paper
itself;
4. analyze a finite-dimensional horizon/tensor-network toy where everything
is computable (QO-0/QO-1 material);
5. show the quantum flip for an energy-flux consumer, or report its clean
absence (QO-2 material, either sign);
6. state precisely what would be required, and what is currently missing,
to connect any of this to Jacobson's derivation or to Dorau-Much's theorem:
at minimum, type III algebras in place of finite factors, a genuine causal
structure in place of a lattice cut, the entropy-area input justified rather
than declared, and the special state class relaxed.

What the paper deliberately does NOT claim: no emergent gravity claim, no
claim that Einstein's equations are a consistency condition (that is QO-3's
question and QO-3 is not in the paper's scope unless it produces a sealed
result), no claim that the toy's cut is a horizon in the causal sense, no
claim about quantum gravity. If QO-2 is negative, the paper reports the
negative with the same prominence a positive would have received.

## 8. Non-claims

Nothing in this track bears on physical gravity, quantum or classical. No
run in this track will be labeled evidence that gravity is informational,
that spacetime is emergent, that observers participate in creating physical
law, or that the cited literature is confirmed or refuted. The causal
caution of section 4 is repeated here as a standing sentence for any
write-up: observation relativity concerns evidential access, not reality.
Evidence labels follow CAMPAIGN.md section 9; everything in this document is
[exploratory] until a sealed preregistration exists, and the highest label
any QO result can earn is [demonstrated-in-model].

## 9. Open design questions (must close before QO-0 seals)

Recorded at drafting time, 2026-08-04. Each needs a decision or a
closed-form control before the corresponding experiment can seal.

1. **Choice of vacuum reference in a finite toy.** Ground state of a gapped
local Hamiltonian gives locality but no closed forms; a Gaussian reference
gives covariance-matrix closed forms but a weaker claim to "vacuum". The
choice affects every downstream witness. Likely resolution: Gaussian for the
closed-form net, Hamiltonian ground state for the claim-bearing sweeps, with
an agreement check where both exist; but that doubles QO-0 and must be
decided, not drifted into.
2. **Does the flip need optimization over encoders, or does it admit an
analytic witness?** The classical flip has analytic instances (read metric
misaligned with source covariance). If a 2-qubit or Gaussian analytic flip
exists for a flux-type functional, QO-2 gains a control that no optimizer
artifact can fake, and the falsification bar sharpens. If none exists, that
absence needs to be understood before trusting optimized encoders at all.
3. **How can an area-analogue be declared without smuggling the answer into
QO-3?** Candidate declarations (cut size, boundary-algebra log-dimension,
mutual information across the cut) are already entropic quantities, so
"D_C proportional to area-analogue" risks being true by construction. The
declaration must be made in geometric/combinatorial terms fixed by the model
graph, not in information terms, and then audited for equivalence to the
measured side, in the spirit of EG-2's reverse-engineering audit. Unresolved.
4. **Algebra restriction and channel restriction are inequivalent, and the
track currently blurs them.** A conditional expectation onto a subalgebra
exists only for special subalgebra/state pairs; a general channel does not
fix a subalgebra; two consumers with the same accessible algebra can have
different channels (different noise). Sections 3 and 5 must decide, per
experiment, which object is primitive. Proposed default: the channel is
primitive, and A_C is derived as the algebra the channel preserves; QO-1's
nesting must then be checked to survive that derivation.
5. **Which divergence is the default.** Umegaki relative entropy, measured
relative entropy, and sandwiched Renyi divergences all satisfy DPI but
differ operationally; the measured relative entropy is arguably the honest
one for a consumer who can only apply POVMs from A_C, and it differs from
the restricted Umegaki quantity in general. The QO-1 gaps can depend on this
choice. Needs a declared default plus one sensitivity sweep.
6. **What are G and B in the quantum triple.** Observation Theory's observer
is (C, G, B), not C alone. The channel gives C; the output metric G (how
task errors are scored) and the budget B (qubits, measurement shots,
classical bits of record; these are not interconvertible) must be declared
per experiment. QO-2's "matched budget" is only as meaningful as this
declaration, and shot-budget versus qubit-budget can plausibly reverse a
flip verdict.
7. **The anti-arm construction in the quantum setting.** Classically the
anti-arm destroys the read direction. The quantum analogue (dephase or
scramble the flux-relevant observables at matched budget) must be defined so
that it spends the same budget as the other arms, or the control is
confounded. No construction is written down yet.
8. **The finite-dimensional stand-in for T_ab k^a k^b.** A lattice toy has
no null direction. Candidate stand-ins (a boundary energy-current operator,
a modular-Hamiltonian-weighted energy) differ, and the modular choice risks
selecting the answer for QO-2 because modular flow is exactly what ties
energy to relative entropy in Dorau-Much. Declaring the flux functional
independently of the modular structure, then measuring their relation, is
probably the honest design; needs a written construction.
9. **Is a bipartition cut an honest stand-in for a causal boundary.** The
toy's cut has no causal structure, no Killing flow, and its "exterior" is
one tensor factor. Every conclusion must be stated for cuts, with the
causal-boundary language reserved for the section 7 step-6 gap list. The
discipline is easy to state and easy to erode; a reviewer check for leaked
causal vocabulary should be part of sealing.
10. **The commuting embedding of the classical anchors is not unique.**
Section 6 requires reproducing PE-0's 1 bit and 1.5 bits, but the embedding
of a classical branch distribution into a diagonal quantum model can be done
in more than one way (which observable is the branch label, how fiber
weights become eigenvalues). The embedding must be declared once, before
QO-0 runs, and the reduction check is only as strong as that declaration.
11. **QO-3's consumer family may be too small to mean anything.** Jacobson
quantifies over a continuum of wedges; any finite toy family may leave the
joint constraint equal to the single-consumer constraint (the QO-3
falsification bar's "inert quantifier" branch) for the trivial reason that
the family is tiny, not because the reading fails. Distinguishing "family
too small" from "quantifier genuinely inert" needs a design idea that does
not exist yet; this is the main reason QO-3 may end design-only.
12. **Type III honesty.** The algebras of real horizon exteriors are type
III von Neumann factors: no density matrices, no partial trace, relative
entropy only via relative modular operators. Everything in this track is
type I by construction. The track must maintain a standing list of which
statements are finite-dimensional artifacts (existence of rho_ext itself)
and which have type III counterparts (relative entropy, DPI), so that
section 7 step 6 stays accurate as results accumulate.
