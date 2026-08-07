# PREREG-UN1-001: the removability discriminator

**Status:** FROZEN CANDIDATE, awaiting seal. Once sealed no field
may change. Chip ⚖️ UN.

**Written before the run.** No number below was produced by the
runner. The runner does not exist as this is written.

---

## 1. The claim

On one substrate, under one budget ladder, and against one declared
consumer family, two kinds of uncertainty separate. One is removed
by budget. The other is not moved by budget at all.

**Claim.** For the declared substrate and family, the expectation
estimation error falls as the reciprocal of the budget for both a
compatible and an incompatible observable pair, while the
single-shot prediction error is zero at every rung for the
compatible pair and is constant across every rung for the
incompatible pair.

If that holds, the classification into removable and irreducible is
sharp on this substrate, the floor is a property of the pair rather
than of the budget, and the two task types are not interchangeable
descriptions of one quantity.

---

## 2. What is not claimed

Nothing here is evidence about physical measurement outside the
declared finite model.

**The reciprocal falling of the estimation error is
replication-grade and is declared as such now.** That estimator
variance falls as one over the number of copies is standard, and
recovering it earns no novelty credit. It is included because the
discriminator needs both halves measured on one substrate under one
ladder, and a design that measured only the interesting half would
have nothing to discriminate against.

No claim is made that the incompatible floor equals any published
bound. Bar 4 requires only that the bound is respected. Whether the
achievable floor sits above it, and by how much, is UN-2's
question and is reported here without a bar.

No claim of irreducibility extends beyond the declared family of
section 4. Section 4 is the whole content of the word irreducible
in this document.

---

## 3. Substrate and observables

**Substrate.** A two-qubit system in the declared pure product
state

|psi> = (cos a |0> + sin a |1>) tensor (cos b |0> + sin b |1>)

with a = pi/5 and b = pi/7. The consumer receives N independent
copies.

These angles are declared so that all four observables below have
strictly positive variance on the state. A state making any of them
deterministic would satisfy several bars vacuously, which is the
defect bar 5 exists to catch.

**Compatible pair.** A = Z tensor I and B = I tensor Z. They
commute.

**Incompatible pair.** A = Z tensor I and B = X tensor I. They do
not commute, and their maximum overlap is one half, so the
Maassen-Uffink value is one bit.

Both pairs live on the same substrate and the same state, so the
comparison between them changes only the pair.

---

## 4. The declared consumer family

Irreducibility below means irreducibility across exactly this
family and nothing wider.

**Type I family, expectation estimation.** At budget N the consumer
allocates copies between the two observables on the declared grid
of split fractions k/N for k from 0 to N, measures each observable
projectively on its allocated copies, and forms the unbiased sample
mean. For a commuting pair the family also contains the joint
member, which measures both observables on every copy in their
common eigenbasis. The error of a member is the sum of the two mean
squared errors, computed in closed form as the observable's variance
divided by the number of copies allocated to it, and infinite when
that number is zero.

**Type II family, single-shot prediction.** At budget N the consumer
applies a projective measurement to every copy, in a basis taken
from the declared grid of angles theta on the great circle through
Z and X, at the grid points j pi / 24 for j from 0 to 24. It may
use one angle on copy one and a second angle on every other copy,
and both range over the grid. The record is the full list of
outcomes. A referee then measures A or B, chosen after the record
exists, on copy one's post-measurement state under the Lueders
rule. The error of a member is the sum of the two conditional
entropies of the referee's outcome given the record, in bits. The
family also contains the trivial member, which measures nothing.

The type II family is enumerated in full and its errors are
computed by exact summation over the whole record space of 4 to
the power N outcomes. No sampling and no optimizer are used
anywhere in this experiment.

**Frontier.** The frontier at a cell is the minimum error over the
members of the family at that cell, together with the identity of a
member attaining it.

---

## 5. Budget ladder

N in {1, 2, 3, 4, 5, 6}, the same ladder for both task types. It
stops at six because the type II record space is exhaustively
enumerated and grows as four to the power N, and an exhaustive
computation at every rung is worth more here than a longer ladder
computed by approximation.

---

## 6. Cells

Two pairs by two task types by six rungs, so twenty-four cells.
Every cell is computed and reported.

---

## 7. Bars

The verdict is PASS only if all six hold. Each is computed from the
record by the runner and none is pre-written.

**Bar 1, type I falls, replication-grade.** For both pairs, the
frontier error times N is constant across the six rungs to within
1e-12, which is the reciprocal law stated so that it can fail.

**Bar 2, type I incompatibility costs a factor and not a floor.**
The ratio of the incompatible frontier to the compatible frontier
is finite and is constant across the six rungs to within 1e-12.

**Bar 3, type II compatible reaches zero.** The compatible
frontier is at most 1e-12 bits at every rung, including N = 1.

**Bar 4, type II incompatible does not move.** The incompatible
frontier varies across the six rungs by at most 1e-12 bits, and at
every rung it is at least the Maassen-Uffink value of one bit less
1e-9.

**Bar 5, anti-vacuity, checked at every one of the twenty-four
cells.** At each cell the runner confirms that the declared family
has at least three members with pairwise distinct finite errors,
that the frontier is attained by a named member which is recorded,
and, for the type II cells, that the record is non-degenerate in
the sense that at least two records carry probability above 1e-12.
A cell failing any part fails bar 5, and a bar met only because a
quantity was degenerate is not met.

**Bar 6, census.** All twenty-four cells appear in the record with
a finite frontier and a named attaining member. A cell that is
absent, skipped, or has no attaining member fails this bar.

---

## 8. The declared expectation and what would refute it

The expectation is that all six bars pass, which would make the
classification sharp.

Each of these outcomes refutes the claim of section 1 and is a
result to be reported as it stands.

- Bar 1 fails and the estimation error does not fall reciprocally,
  which would mean the instrument or the closed form is wrong,
  since the reciprocal law is not in doubt.
- Bar 2 fails and the incompatible-to-compatible ratio grows with
  budget, which would make type I incompatibility a floor and not a
  factor, and would collapse the distinction this document is built
  on.
- Bar 3 fails and the compatible pair cannot be predicted exactly,
  which would mean commuting observables do not admit a common
  record on this substrate and would refute the reading directly.
- Bar 4 fails and the incompatible type II frontier moves with
  budget. If it falls, the floor is removable within this family
  and the word irreducible does not apply to it. If it rises, the
  family or the enumeration is defective.
- Bar 5 fails at any cell, in which case the bars that cell
  supports are recorded as vacuous and the run is void, following
  the standing rule this campaign adopted after three vacuous runs.

---

## 9. Anti-circularity

No uncertainty relation is supplied to the model. The
Maassen-Uffink value enters only as a comparison in bar 4 and is
computed from the declared observables rather than assumed. The
consumer family, the grids, the ladder, the state, the observables
and all six bars are fixed by this document before the runner
exists. No family member is added or removed after any error is
seen. The type II family is enumerated exhaustively so that no
member can be selected after the fact.

The floors reported here are floors across the family of section 4.
A floor produced by restricting that family is a tautology, and the
family is declared here in full so a reader can judge that for
themselves.

---

## 10. Outputs

`results/un1-discriminator.json`, hashed and committed with the
runner's code commit, containing every one of the twenty-four
cells, the members attaining each frontier, all six bar values, and
the verdict computed from them.
