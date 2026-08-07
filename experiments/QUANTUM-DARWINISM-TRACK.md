# QD Track: Quantum Darwinism as Multi-Consumer Structure

**Status:** design draft, unsealed, non-claim-bearing. Chip 🧬 QD.
Everything is measured in declared exact finite models.

## 1. Question

Why do observers agree on classical facts. The quantum Darwinism
answer is redundancy, many environment fragments carry the same
record of the system. That is intrinsically a statement about a
family of consumers, each reading its own fragment through its own
channel. The track question is whether objectivity is
consumer-relative structure, whether redundancy emerges from
declared interactions or must be declared the way the EG track
found constraints must be, and where the budget knob (fragment
size, interaction strength, monitoring rate) places the transition
between quantum and effectively classical reads.

## 2. Anchors (verified citations to be completed before any seal)

Zurek's quantum Darwinism and einselection program, the classical
plateau of mutual information at the system entropy, and Page-type
behavior of random pure states. Each enters as a replication target
or a comparison, never as an inserted answer.

## 3. Anti-circularity contract

No pointer basis is inserted where its emergence is the measured
question. States, interactions, and fragment families are declared
before claim-bearing runs.

## 4. Experiments

### QD-0: Exact fragment-information instrument layer

One system qubit and six environment qubits, pure states, exact
density matrices and von Neumann entropies, mutual information
I(S:F) for every fragment size (fragments of equal size are
equivalent by declared symmetry). Protocol declared 2026-08-05,
before the run.

C1 product control, a product state gives I(S:F) = 0 for every
fragment within 1e-12. C2 perfect-record control, the GHZ branching
state gives I(S:F) = 1 bit for every fragment of size one through
five and 2 bits for the full environment, all within 1e-10, the
classical plateau exact. C3 partial-record closed form, the
branching state with per-qubit record overlap c = 1/2 has I(S:F) at
fragment size f equal to H((1+c^6)/2) + H((1+c^f)/2) -
H((1+c^(6-f))/2) bits with H the binary entropy, measured against
the closed form within 1e-10 at every f. C4 no-plateau control, a
declared seeded Haar-random pure state of seven qubits has average
single-qubit-fragment I(S:F) at most 0.15 bits while the full
environment gives I = 2 S(S) within 1e-10, records are structure,
not a generic feature of purity. All four or QD-0 fails.
Exploratory label, results/qd0-instrument.json.

#### QD-0 results (run 2026-08-05, record sha edcf2ebd004d...)

Verdict PASS, all four items. The product state carries no
information at 3.2e-16, the GHZ plateau is exact at 1 bit for every
proper fragment and 2 bits for the whole environment, and the
partial-record state matches its overlap closed form to 2.2e-16 at
every fragment size, the measured curve rising from 0.81 bits at
one qubit through the plateau shoulder to 2.00 bits at six. The
Haar-random control has mean single-fragment information 0.051
bits against system entropy 0.999, records are structure, not a
generic feature of purity. The redundancy instrument is validated
end to end.

### QD-1: Emergence gate for redundancy

Declared interaction dynamics (controlled rotations of declared
strength, no record structure inserted). Measured, does the
classical plateau form under evolution, and is its formation
declared-or-absent in the EG-6 sense. Either outcome is a result.

#### QD-1 protocol (declared 2026-08-05, before the run)

The system qubit starts in the plus state, six environment qubits
in zero. Two declared dynamics with matched entangling power. The
basis-carrying dynamics applies a controlled rotation of declared
angle theta from the system to each environment qubit, ladder
theta in pi/16, pi/8, pi/4, pi/2, pi. The evolved state is then a
branching state whose per-qubit record overlap is cos(theta/2), so
every fragment information value has the QD-0 closed form, an
exact prediction with nothing fitted. The basis-free dynamics
applies six seeded Haar-random two-qubit unitaries, system with
each environment qubit in turn, no preferred basis anywhere in the
declaration. Redundancy R is the number of disjoint single-qubit
fragments whose information reaches ninety percent of the system
entropy.

Bars. Q1, at every theta the measured fragment informations match
the branching closed form within 1e-10, the plateau's formation is
predicted entirely by the declared gate angle. Q2, fragment-one
information is monotone increasing along the theta ladder. Q3, at
theta = pi the plateau is exact and R = 6. Q4, at theta = pi/16,
R = 0, weak declared records give no redundancy. Q5, the
basis-free dynamics ends with system entropy at least 0.3 bits and
R = 0, entangling power without a declared basis produces
entanglement and no redundancy, and at theta = pi the two dynamics
have comparable system entropy with opposite redundancy, recorded.
All five or QD-1 fails. The reading, redundancy is
declared-or-absent, the plateau appears exactly when and exactly as
the declared interaction's basis dictates, and generic interaction
of the same strength produces none. Exploratory label,
results/qd1-emergence.json.

#### QD-1 results (run 2026-08-05, record sha 5f4089923187...)

Verdict FAIL on Q5, and the failure is a measured finding. The
basis-carrying items are exact, the evolved states match the
branching closed form to 2.7e-15 at every angle with nothing
fitted, records grow monotonically, the full plateau appears at
theta = pi with R = 6, and weak declared records give R = 0. The
declared basis-free control, six sequential pairwise Haar unitaries,
ended with system entropy 0.665 bits and R = 1, not 0, the
last-touched environment qubit carries a redundancy-grade record.
Sequential pairwise scrambling is not basis-free in the operational
sense, the causal order of the interactions itself imprints a
recency record on the most recently scrambled qubit. The Q5 bar
failed as declared and the mechanism is recorded as a finding, an
observer can be handed a record by the schedule of interactions
alone.

#### QD-1b protocol (declared 2026-08-05, before the run)

Identical to QD-1 except the basis-free control, which becomes a
seeded Haar-random pure state of all seven qubits, globally
scrambled with no interaction schedule at all, the QD-0 C4
construction. Bars unchanged, system entropy at least 0.3 bits and
R = 0. The named error, QD-1's control declared a sequence, and a
sequence is structure. Exploratory label,
results/qd1b-emergence.json.

#### QD-1b results (run 2026-08-05, record sha d4b29d1738be...)

Verdict PASS, all five items. The branching closed form holds to
2.7e-15 at every angle, records grow monotonically, the full
plateau appears at theta = pi with R = 6, weak records give R = 0,
and the global Haar state carries system entropy 0.9945 bits with
R = 0. The gate's reading, redundancy is declared-or-absent, the
plateau appears exactly when and exactly as the declared
interaction's basis dictates, maximal entanglement without a
declared basis carries no redundancy at all, and QD-1's recorded
finding stands alongside, even an interaction schedule with no
declared basis can hand one observer a record through its causal
order alone.

### QD-2: The budget knob

Fragment size and interaction strength ladders. Measured, the
redundancy transition as a function of consumer budget, and whether
the transition point is an invariant or a consumer artifact.

#### QD-2 protocol (declared 2026-08-06, before the run)

Two declared consumers of branching states built by explicit gate
application as in QD-1. The symmetric consumer, controlled
rotations of equal angle theta on all six environment qubits,
theta on the declared grid k pi/32 for k = 1 through 16. Its
budget curve f*(theta) is the smallest fragment size whose
information reaches ninety percent of the system entropy, absent
when no fragment of six or fewer suffices. The portfolio consumer,
declared unequal angles (pi/16, pi/16, pi/8, pi/4, pi/2, 3 pi/4),
where a fragment's record overlap is the product of cos(theta_j/2)
over the qubits it holds, so fragments of equal size are no longer
equivalent and the closed form extends to every subset.

Bars. K1, at every grid angle the measured fragment informations
match the branching closed form within 1e-10 and the measured
f*(theta) equals the closed-form prediction. K2, f*(theta) is
nonincreasing in theta, more interaction strength never demands a
larger fragment. K3, for the portfolio consumer the measured
information of every one of the 62 proper environment subsets
matches the subset closed form within 1e-10. Measurements, the
onset angle, the smallest theta at which any fragment of six or
fewer suffices, and the portfolio spread, the information ratio
between the best and worst fragments of size two, the statement
that a consumer's budget is a portfolio, not a number. Exploratory
label, results/qd2-budget-knob.json.

#### QD-2 results (run 2026-08-06, record sha 0c441dc6fc92...)

Verdict PASS, all three items, closed forms to machine precision
throughout. The symmetric budget curve is flat, f* = 3 at every
grid angle, and the closed form says why, a fragment holding half
the environment has record overlap equal to its complement's, so
its information equals the system entropy exactly at any nonzero
angle, three qubits always suffice and on this grid two never do.
The portfolio consumer is the sharp result, with declared unequal
angles the best and worst two-qubit fragments differ by the factor
36.0 in information, all 62 subset closed forms matching to
1e-10. Two consumers with identical fragment counts and identical
access sizes read the same state with a thirty-six-fold
information disparity, the budget is a portfolio, not a number.

### QD-3: Multi-consumer agreement audit

Two declared consumers reading disjoint fragments. Measured, when
their records agree, and whether every disagreement is predicted
exactly by the declared channel models, the lawful-observer clause.

#### QD-3 protocol (declared 2026-08-06, before the run)

Branching states at the QD-1 angle ladder, built by gate
application. Consumer A holds environment qubits one and two,
consumer B holds three and four, disjoint. Each performs its
declared optimal two-outcome measurement, the Helstrom
discrimination of its fragment's two branch states, whose success
probability has the closed form half of one plus the square root
of one minus the squared fragment overlap. The joint outcome
distribution is computed exactly from the Born rule.

Bars. J1, each consumer's marginal success probability matches the
Helstrom closed form within 1e-10 at every angle. J2, route
agreement, the joint distribution computed on the full state and
on the reduced four-qubit state agree within 1e-12. J3, agreement
is manufactured by record strength, the probability that the two
consumers' outcomes agree is strictly increasing along the angle
ladder, reaching at least 1 - 1e-10 at theta = pi and staying at
most 0.6 at theta = pi/16. All three or QD-3 fails. The reading,
objectivity between observers is record strength made mechanical,
and every disagreement rate is the declared channels' exact Born
arithmetic, never noise. Exploratory label,
results/qd3-agreement.json.

#### QD-3 results (run 2026-08-06, record sha c6463efc00c1...)

Verdict PASS, all three items. Helstrom marginals match their
closed form to 8.9e-16 at every angle, the two Born routes agree to
1e-15, and the agreement curve is the budget knob made social,
0.510, 0.537, 0.636, 0.875, 1.000 along the angle ladder, exactly
1 at the perfect-record point and barely above coin-flip at the
weakest. Two optimal observers of disjoint fragments agree exactly
to the extent the declared interaction wrote records for them,
objectivity between observers is record strength made mechanical,
and every disagreement is Born arithmetic, not noise.

## 5. Evidence discipline and non-claims

Seals, labels, append-only records, and falsification bars as in
CAMPAIGN.md. Substrate, exact finite models in Python on Atlas.
Nothing in this track is a claim about macroscopic classicality in
the laboratory.
