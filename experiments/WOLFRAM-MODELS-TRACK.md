# WM Track: Wolfram Models and Cellular Automata Under the Campaign Audits

**Status:** design draft, unsealed, non-claim-bearing. No physics claims
are made anywhere in this document. Every quantitative statement below
is either a citation, a definition, a closed-form control target, or a
target for a future run.

One sentence of intent before anything else. This track tests claims,
not people. The Wolfram Physics Project and the cellular-automaton
literature contain a family of inference patterns that this campaign
has, for its own reasons, already made exactly measurable, and the
audits below are stated so that a defender of the program would accept
every pass condition as fair and would recognize every failure
condition as a finding about a model class rather than an insult. A
claim that survives these audits comes out stronger than it went in.

## 1. Question

The Wolfram program claims that simple rewriting systems exhibit
emergent space, with dimension read from ball-volume growth (Wolfram
2020, Gorard 2020a), special relativity from causal invariance of the
rewriting (Gorard 2020a), quantum mechanics from multiway branching
(Gorard 2020b), particles as stable localized structures in the
evolving hypergraph or automaton (Wolfram 2002, Wolfram 2020), and a
second law of thermodynamics from computational irreducibility acting
on computationally bounded observers (Wolfram 2023).

The campaign has exact instruments for four of the underlying
inference patterns.

1. **Observer and foliation covariance.** The PF-6 audit asks whether
   a claimed event survives a passive change of the observer's
   slicing, and the PF fold theorem says exactly which changes of
   multiplicity are legitimate under such a change (unsigned counts
   may jump, the signed count is conserved).
2. **Prescription independence.** The PF-4 closure-prescription clause
   and the PF-3 Cayley-pole finding, in which a published threshold
   was proved to belong to the discretization rather than to the
   dynamics. Any quantity that exists only under one update
   prescription is prescription-borne, and the campaign now plants a
   known artifact in every pipeline to prove the pipeline can catch
   one.
3. **Estimator validation before claim-bearing use.** The PF-0 rule.
   No estimator measures anything until it has passed exact controls,
   including a control it must refuse, and a null result is
   interpretable only after the instrument net passes.
4. **The separation of observational from thermodynamic entropy.** The
   PE track's three-entropies discipline and the PE-2 reversible-cycle
   demonstration, in which observed binned entropy swings more than
   two bits while the hidden ensemble is recovered exactly, so the
   entire change is observational.

The track question. Which Wolfram-model claims survive these audits,
stated so that every audit has a pass condition a defender would
accept and a failure condition that is a finding, not an insult. A
clean negative here is a result about a model class under a declared
audit, and nothing more.

## 2. Verified references

Entries below were verified against arXiv abstract pages, publisher
records, or the published PDF on 2026-08-04 unless marked otherwise.
Bibliographic corrections made here propagate to any WM write-up.

**S. Wolfram, "A Class of Models with the Potential to Represent
Fundamental Physics", arXiv:2004.08210, Complex Systems 29(2),
107-536 (2020).** The program statement. Hypergraph rewriting rules,
causal graphs, multiway systems, dimension from ball-volume growth,
and the claimed correspondences to relativity and quantum mechanics.
Verified against the arXiv abstract page.

**J. Gorard, "Some Relativistic and Gravitational Properties of the
Wolfram Model", arXiv:2004.14810, Complex Systems 29(2), 599-654
(2020).** Cited here as Gorard 2020a. Argues that causal invariance
corresponds to a discrete general covariance and derives discrete
analogues of the Einstein equations. The causal-invariance claim this
track's WM-2 audits is stated here in its strongest form. Verified
against the arXiv abstract page.

**J. Gorard, "Some Quantum Mechanical Properties of the Wolfram
Model", Complex Systems 29(2), 537-598 (2020), DOI
10.25088/ComplexSystems.29.2.537.** Cited here as Gorard 2020b.
Studies rule classes where causal invariance fails and reads the
resulting multiway evolution as an analogue of quantum superposition,
with observers imposing effective causal invariance by completion.
Verified against the published journal PDF. Bibliographic hazard,
recorded because it bit during drafting. The arXiv identifier
2004.14811, which circulates for this paper, belongs to an unrelated
mathematics paper on Riemann surfaces, so this entry cites the journal
version only.

**S. Wolfram, A New Kind of Science, Wolfram Media (2002).** Cellular
automata as a systematically explored model class, Rule 110 and its
localized structures, second-order reversible rules, and the book's
discussion of irreversibility and the second law. Book, cited without
fetch by declared exception.

**T. Toffoli and N. Margolus, "Invertible cellular automata: a
review", Physica D 45, 229-253 (1990).** The standard review of
invertible CA constructions, including the second-order technique this
track uses in WM-1, in which invertibility holds by construction
rather than by search. Verified against the publisher listing and the
ADS record 1990PhyD...45..229T via search on 2026-08-04. Direct
abstract-page fetches were blocked at drafting time and the
verification route is recorded here honestly.

**S. Wolfram, "Computational Foundations for the Second Law of
Thermodynamics", writings.stephenwolfram.com, February 2023, and in
book form in The Second Law: Resolving the Mystery of the Second Law
of Thermodynamics, Wolfram Media (2023).** The claim that the second
law arises from computational irreducibility of the microdynamics
together with the computational boundedness of observers. This is the
claim WM-1 sharpens rather than attacks, because it is already an
observer-relative statement. The essay page could not be fetched
directly at drafting time (certificate failure) and was verified via
search listings and the book form, by declared exception.

## 3. The mapping table

The core deliverable of this track. One row per Wolfram-program claim,
the campaign instrument that audits it, what a pass means, and what a
failure means. Rows are audits of inference patterns, not of the
research program's worth.

| Wolfram-program claim | Campaign audit | A pass means | A failure means |
|---|---|---|---|
| Emergent dimension from ball-volume growth | WM-0 estimator net with exact controls, then WM-4 held-out scaling with preregistered alternatives (the PF-4 axis-discrimination pattern) | The rule's d-hat is finite, stable on radius ranges never used for fitting, and beats the preregistered alternative growth laws under bars fixed in advance | The dimension estimate belongs to the fitted radius window, a statement about estimator scope on that rule, not about the program |
| Causal invariance, hence Lorentz-type claims | WM-2 prescription-pair protocol, with update order as the prescription (the Cayley lesson verbatim) | For a rule with proved confluence, declared causal-graph invariants agree exactly across independent update orders | For a rule without proved confluence, the order-dependence is measured rather than assumed away, and any quantity that varies is classified prescription-borne for that rule |
| Particles as stable localized structures, their creation and annihilation | WM-3 foliation-covariance protocol on the causal graph | Counts and collision events are invariant across all valid foliations, or multiplicity varies while a declared signed invariant is conserved, which the campaign's fold theorem says is the legitimate form of observer-dependent counting | The counted structures are foliation-borne projection kinematics, with no conserved invariant identified behind them |
| A second law from computational irreducibility | WM-1, the PE-2 protocol transplanted to a manifestly reversible second-order CA | Coarse-grained entropy rises from an ordered seed and the trajectory retraces exactly under time reversal, so the growth is observational in the campaign's three-entropies sense, which is the sharpened form of the program's own observer-relative statement | A nonzero retrace defect, which would indicate hidden information loss in the implementation and voids the reading rather than scoring against anyone |
| Quantum mechanics from multiway branching | Design-only in this track. The QO track's consumer-channel vocabulary (restricted algebras, consumer-relative distinguishability, the flip) is the natural audit language, but no experiment is designed here | Not applicable, no audit designed | Not applicable, no audit designed |

Two reading rules for the table. First, the second-law row is not
adversarial at all. Wolfram's own account already locates the second
law in the observer, and WM-1 supplies the exact-arithmetic witness
that makes that account a measured statement instead of an argued one.
Second, the particle row explicitly allows observer-dependent counts.
The PF track's central theorem is that unsigned multiplicity may
legitimately change under a change of slicing while a signed invariant
is conserved, so the audit's job is to find the invariant or to
certify that none was identified, never to demand naive invariance of
raw counts.

## 4. Experiments

Sequence discipline. WM-0 is the instrument net and runs first, before
any Wolfram-rule measurement, per the campaign rule that a null result
is interpretable only after the instrument net passes. WM-1 is the
measured transplant of PE-2 and can run as soon as its coarse-graining
is declared. WM-2, WM-3, and WM-4 are designs and run only under
future preregistrations.

### WM-0: Dimension-estimator instrument net

**Question.** Does the ball-volume dimension estimator recover known
dimensions exactly where they are known, and refuse to report a
dimension where none exists.

**Method.** For a graph or hypergraph, define B(v, r) as the number of
vertices within graph distance r of v. The estimator d-hat is the
slope of log B against log r over a radius window declared before any
rule is measured, averaged over declared base points. Exact controls,
all with known answers.

- Path graph, required d-hat = 1 within sealed tolerance.
- 2D torus grid, required d-hat = 2 within sealed tolerance.
- 3D torus grid, required d-hat = 3 within sealed tolerance.
- Regular tree, the diverging control. Ball volume grows
  exponentially, the local log-log slope must grow without bound
  across the window, and the estimator must flag the graph
  non-finite-dimensional rather than print a number.

**Primary witnesses.** Per-control d-hat with its window, deviation
from the exact value, the tree control's slope-growth profile, and the
estimator's refusal behavior on the tree.

**Falsification bar.** Any control failure invalidates the estimator.
A finite d-hat reported for the regular tree is a failure of the same
severity as a wrong d-hat on a torus, because the entire point of the
net is that the instrument must know what it cannot measure. No
Wolfram-rule dimension may be quoted, even at exploratory label,
before this net passes.

### WM-1: Reversible-CA entropy cycle (the transplanted PE-2)

**Question.** In a cellular automaton that is reversible by
construction, is the observed growth of coarse-grained entropy from an
ordered seed observational in exactly the PE-2 sense, with zero hidden
information loss.

**Method.** A second-order reversible elementary CA,

a(t+1) = F(a(t)) XOR a(t-1),

where F is any elementary rule applied to the current configuration.
The update is invertible by construction, since a(t-1) = F(a(t)) XOR
a(t+1) recovers the past exactly, in the family reviewed by Toffoli
and Margolus (1990) and explored in A New Kind of Science. The
specific rule F, the lattice size, the boundary condition, and the run
length are declared before any run. Start from an ordered seed (a
single nonzero cell or a declared low-entropy block). Evolve T steps
and record the coarse-grained block entropy H_b(t) at every step,
with block width b and histogram binning declared in advance per the
section 5 contract. Reverse by swapping the last two configurations
and evolving the same rule T further steps.

Arithmetic note. The update is exact over GF(2), so the reversed
trajectory is not approximately the forward trajectory, it is the
forward trajectory, bitwise, or the implementation is wrong. This is
a stronger retrace guarantee than PE-2's floating-point version had,
and the bar below uses it.

**Primary witnesses.** The entropy curve H_b(t) over the full cycle.
The exact-retrace defect, the number of cells at which the reversed
trajectory differs from the forward one at mirrored times, which must
be exactly zero. Microstate recovery, the Hamming distance between
the recovered initial pair of configurations and the true initial
pair, which must be exactly zero.

**Falsification bar.** Any nonzero retrace defect or recovery
distance invalidates the run as an implementation error. Conditional
on exact retrace, a coarse-grained entropy that rises from the
ordered seed and retraces its curve establishes the reading, which
mirrors PE-2 verbatim. Entropy growth in reversible computational
systems is observational, produced by the observer's coarse-graining,
with zero hidden information loss. The three-entropies distinction of
ENTROPY-TRACK.md section 2 applies unchanged, and Wolfram's
irreversibility statements are then claims about observer
coarse-graining, which is exactly what the campaign's PE track
formalizes. This experiment is the measured piece that makes the
second-law audit concrete rather than rhetorical.

### WM-2: Prescription-pair and causal-invariance audit (design)

**Question.** For a declared hypergraph rewriting rule, which
causal-graph quantities are independent of the update order, and which
exist only under one prescription.

**Method, design-level.** Update order is a prescription in exactly
the PF-4 sense. For each declared rule, evolve the system under two
independent update orders declared in advance (for example a fixed
scan order and a declared-seed random order), from the same initial
hypergraph, for the same number of events. Measure declared
causal-graph invariants under both prescriptions. Candidate invariant
list, to be fixed at preregistration. Total event count, the multiset
of causal-edge counts per event, declared graph invariants of the
causal graph, and the WM-0 dimension estimate of the causal graph.
Rules with a proof of confluence (causal invariance) must agree
exactly. Rules without such a proof get their order-dependence
measured rather than assumed away, which is the Cayley lesson
verbatim. The published threshold in PF-3 belonged to the
discretization, and a causal structure that exists only under one
update order belongs to the update order.

**The planted artifact.** Alongside the declared rules, the run
includes a deliberately non-confluent rule whose order-dependence is
known in advance. The analysis pipeline must flag it
prescription-borne. If the pipeline fails to catch the planted
artifact, the pipeline is invalid and no rule verdict may be read.
This is the C5 clause of PF4-DESIGN.md transplanted whole.

**Primary witnesses.** Per-rule, per-invariant agreement or measured
disagreement across the prescription pair, and the planted artifact's
detection record.

**Falsification bar.** For the pipeline, missing the planted artifact
voids the run. For a rule, exact agreement of every declared invariant
is the pass. Measured disagreement is not a refutation of the program,
it is a classification. The disagreeing quantity is prescription-borne
for that rule, and any physical claim resting on it inherits that
label.

### WM-3: Foliation-covariance audit (design)

**Question.** Which claimed structures of an evolution (particle
counts, collision events, dimension estimates) are invariant across
valid foliations of its causal graph, and where counts vary, is there
a conserved signed invariant behind them.

**Method, design-level.** A valid foliation of a causal graph is a
sequence of antichains respecting the partial order, each antichain a
maximal set of pairwise causally unrelated events, the sequence
exhausting the graph in order. The audit draws foliations from a
declared family (see open question 2) and measures each claimed
structure on each foliation. For particle claims the structures are
localized-pattern counts per slice and collision or
creation-annihilation events between slices. For dimension the
structure is the WM-0 estimate on the slices and on the causal graph.

**The signed-versus-unsigned lesson, stated in advance.** The
campaign's fold theorem established that a change of slicing can
legitimately change unsigned multiplicity while a signed invariant is
conserved, and PE-2 measured an entropy staircase doing exactly that.
The audit therefore has two honest outcomes per structure, not one.
Either the structure is foliation-invariant outright, or its
multiplicity varies while a declared signed invariant (an orientation
index, a conserved charge-like count, a topological index) is
conserved across all foliations. Both are physics-in-the-model. The
failure case is the third outcome, multiplicity that varies with no
conserved invariant identified, which classifies the structure as
projection kinematics of the foliation choice.

**Primary witnesses.** Per-structure invariance record across the
foliation family, the identified invariant where one exists, and the
explicit certification where none was found.

**Falsification bar.** Set at preregistration per structure. The
design commitment made now is only the trichotomy above and the rule
that "no invariant found" is a recorded result, not a silence.

### WM-4: Held-out dimension scaling on published rules (design)

**Question.** Do the dimension claims published for specific rules
survive the PF-4 held-out pattern.

**Method, design-level.** For each declared published rule, the WM-0
estimator (already validated, or this experiment does not run) is
calibrated on a training radius window and tested on held-out radius
windows and system sizes never used in calibration. Preregistered
alternatives, fit against the same held-out data with declared
complexity penalties. Finite dimension d, exponential growth
(non-finite-dimensional), and a crossover law (finite d at small
radius crossing over at a fitted scale). Bars fixed in advance at
preregistration.

**Primary witnesses.** Held-out ranking of the three growth laws per
rule, the stability of d-hat across held-out windows, and residual
structure against radius.

**Falsification bar.** A rule's dimension claim passes if the finite-d
law wins on held-out data and d-hat is stable across held-out windows
within the sealed tolerance. A crossover or exponential verdict is a
finding about that rule at the measured sizes, with the honest caveat
that finite-size verdicts do not settle asymptotic claims (open
question 6).

## 5. Anti-circularity contract for the track

A WM run may not contain, directly or through an equivalent choice
made after seeing data,

- a foliation or update order chosen after inspecting which choice
  yields the claimed phenomenon;
- a coarse-graining (block width, bin count, pattern alphabet) tuned
  after seeing the entropy curve, so the WM-1 coarse-graining is
  declared before any run;
- a radius window chosen post hoc, so the WM-0 estimator window is
  declared before any rule measurement;
- a dimension claimed from the fitted region without held-out
  confirmation;
- postselection on rules, seeds, or trajectories that exhibit the
  claimed structure, with every evolved instance counted in the
  denominator.

## 6. Relation to prior local work

The user's wolfram-observer-bridge experiments (local repository
C:\source\wolfram-observer-bridge) established that an observer's
coarse-graining basis, the compressibility or angle-only low-mode
Laplacian embedding, preserves geodesic structure on emergent
hypergraph manifolds at rank correlations near 0.9 while the magnitude
component carries only degree noise, an observer-first reading of the
Wolfram program in which the measurable content lives in what a
bounded observer's basis preserves. The WM track is the
campaigns-repo formalization of that same observer-first reading. It
replaces that project's exploratory scoring with this repository's
sealed-instrument discipline, and it audits the program's claims with
the same instruments every other track's claims must survive.

## 7. Non-claims

Nothing in this track bears on whether the Wolfram program is true or
false as fundamental physics, and no WM result may be quoted as
evidence in either direction. The track measures which of the
program's inference patterns are invariant under the audits any
physical claim must survive, inside finite computable models. A clean
negative, a claim shown foliation-borne or prescription-borne for a
declared rule, is a result about the model class under a declared
audit, not a refutation of the research program, exactly as the
campaign's own PF-4 neither-axis verdict was a result about a family
and not a verdict on the campaign's founding question. Evidence labels
follow CAMPAIGN.md section 9. Everything in this document is design,
everything an unsealed run produces is [exploratory], and the highest
label any WM result can earn is [demonstrated-in-model].

## 8. Open design questions

Recorded at drafting time, 2026-08-04. Each needs a decision or a
closed-form control before the corresponding experiment can seal.

1. **Subhypergraph matching cost and canonical hashing for WM-2.**
   Hypergraph rewriting requires subhypergraph isomorphism per event
   and causal-graph comparison requires a canonical form. Both are
   expensive in general. Whether declared-rule structure keeps
   matching tractable at the sizes WM-2 needs, and which
   canonical-form hash makes causal-edge multisets comparable across
   prescriptions without ambiguity, are open engineering questions
   with correctness consequences, since a hash collision would
   manufacture false agreement.
2. **What counts as a valid foliation family for WM-3.** Random
   maximal antichains, geodesic slicings from a declared root, and
   greedy layerings sample the foliation space very differently, and
   the audit's strength depends on the family's coverage. A family too
   narrow proves little, a family defined post hoc violates section 5.
   The declaration must also say whether the family is meant to sample
   or to exhaust.
3. **Rule 110 versus synthetic particle CAs for WM-3.** Rule 110's
   gliders are the canonical particle claim, but identifying them
   requires filtering the periodic ether background, a nontrivial
   instrument with its own failure modes. A synthetic CA with declared
   particles would make the audit cheap and exact at the cost of
   auditing a strawman nobody defends. Whether the ether-filter
   instrument is worth building, or whether both should run with the
   synthetic case as the control, is undecided.
4. **Declaring the WM-1 coarse-graining so the entropy is not tuned.**
   Block width and bin structure fix the height and shape of the
   entropy curve, and the section 5 contract requires declaring them
   before runs. The open part is whether one declared coarse-graining
   suffices or whether a declared sweep (several block widths, all
   preregistered) is needed to show the observational reading is not
   an artifact of one lucky block size.
5. **Whether WPP particles have a computable signed invariant at
   all.** The program describes particles as locally stable
   topological obstructions in the hypergraph. The WM-3 trichotomy
   needs a candidate signed invariant to check for conservation, and
   no computable one is currently declared for hypergraph
   obstructions. If none can be constructed, the audit can still
   certify invariance or foliation-borneness of counts, but the
   middle outcome of the trichotomy is unreachable for those objects,
   and the design must say so rather than quietly narrowing.
6. **Finite-size verdicts against asymptotic claims.** WM-4 measures
   at finite radius and size, and the program's dimension claims are
   asymptotic. A crossover verdict at measured sizes is compatible
   with either asymptotic story. What size ladder, if any, would let
   WM-4 speak to the asymptotic claim, and whether that ladder is
   affordable, is open, and until it closes WM-4 verdicts carry an
   explicit at-measured-sizes qualifier.
7. **How many prescriptions bound a prescription class.** WM-2's pair
   protocol detects order-dependence but two orders cannot certify
   independence across the full class of valid orders for a rule
   without a confluence proof. Whether measured agreement across a
   declared larger family earns a weaker independence label, and what
   that label is called so it cannot be misread as proved confluence,
   needs a decision before any WM-2 pass is quotable.
