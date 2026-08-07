# PREREG-UN1-002: the removability discriminator, corrected

**Status:** FROZEN CANDIDATE, awaiting seal. Once sealed no field
may change. Chip ⚖️ UN.

**Supersedes** PREREG-UN1-001, which was sealed at commit b549a29,
run as declared, and failed four of its six bars. That document
stays in the repository unedited and its evidence record,
`results/un1-discriminator.json` with record sha e5c85c97444cf61f,
stays committed. This document names each error and repairs it.

**Written before its runner exists.** No number below came from a
UN-1b run. Numbers quoted from UN-1 are quoted as the failures they
are.

---

## 1. What UN-1 got wrong

Three errors, all in the declaration and none in the model. The
model behaved correctly at every point. What failed was that the
sealed document asked the model for things the declared family
cannot supply.

**Error one, an empty family at the bottom of the ladder.** The
type I family allocates N copies between two observables and its
error is infinite when either allocation is empty. At N equal to
one there is no non-empty split, so for a non-commuting pair, which
has no joint member, the family had no member with finite error at
all. The frontier was infinite, and that infinity propagated into
three bars. The design put a rung on the ladder that the family
cannot stand on.

**Error two, a constancy bar on a quantity that oscillates.** Bar 1
required the frontier error times N to be constant to within 1e-12.
For the commuting pair it was, to 2.2e-16, because the joint member
gives exactly the sum of the variances at every rung. For the
non-commuting pair it is not, and cannot be, because the optimal
allocation is an integer and the best integer jitters around the
continuum optimum. UN-1 measured 2.000, 1.643, 1.588, 1.608, 1.643
at N from two to six, which is neither constant nor even monotone.
The reciprocal law is real and the declaration named the wrong
signature for it.

**Error three, a richness requirement the family cannot meet.** Bar
5 required at least three members with distinct finite errors at
every cell. At N equal to two the non-commuting family has exactly
one such member. The anti-vacuity check, which exists to catch bars
that are met degenerately, was itself unsatisfiable by
construction at the bottom of the ladder. Five of the twenty-four
cells failed it for that reason alone.

**What UN-1 established anyway.** Bars 3 and 4 passed on their own
terms and are not re-litigated here, though they are re-run. The
type II compatible frontier was exactly zero at all six rungs. The
type II incompatible frontier was one bit at all six rungs, with a
spread of 1.5e-13 across the ladder and sitting on the
Maassen-Uffink value to within 1.5e-13. The half of the
discriminator that was in doubt behaved as the track expected. The
half that failed is the half that is textbook.

---

## 2. The claim

Unchanged in substance from UN-1 section 1. On one substrate and
against one declared family, expectation estimation error falls
toward zero as budget grows for both a compatible and an
incompatible observable pair, while single-shot prediction error is
zero at every budget for the compatible pair and does not move with
budget for the incompatible pair.

---

## 3. What is not claimed

The reciprocal falling of estimation error is replication-grade and
is declared as such, as in UN-1 section 2. No claim is made that
the incompatible type II floor equals any published bound; bar 4
requires only that the bound is respected, and the size of any gap
is UN-2's question. No claim of irreducibility extends beyond the
family of section 5. Nothing here is evidence about physical
measurement outside the declared finite model.

---

## 4. Substrate and observables, unchanged

Two-qubit system in the pure product state

|psi> = (cos a |0> + sin a |1>) tensor (cos b |0> + sin b |1>)

with a = pi/5 and b = pi/7. Compatible pair A = Z tensor I and
B = I tensor Z. Incompatible pair A = Z tensor I and B = X tensor I,
whose maximum overlap is one half, so the Maassen-Uffink value is
one bit. All four observables have strictly positive variance on
this state.

The consumer receives N independent copies.

---

## 5. The declared consumer family, unchanged

**Type I.** At budget N the consumer allocates copies between the
two observables on the grid of integer splits k from 0 to N,
measures each observable projectively on its allocated copies, and
forms the unbiased sample mean. For a commuting pair the family
also contains the joint member, which measures both in the common
eigenbasis on every copy. A member's error is the sum of the two
mean squared errors, each the observable's variance divided by its
allocation, and infinite when an allocation is empty.

**Type II.** At budget N the consumer measures every copy
projectively, using one declared angle on copy one and a second on
every other copy, each angle from the grid j pi / 24 for j from 0
to 24 and applied to both qubits of the copy. The record is the
full list of outcomes. A referee then measures A or B, chosen after
the record exists, on copy one's post-measurement state under the
Lueders rule. A member's error is the sum of the two conditional
entropies of the referee's outcome given the record, in bits. The
family also contains the trivial member, which measures nothing.
The family is enumerated in full and the entropies are computed by
exact summation over the whole record space of 4 to the power N
outcomes.

**Frontier.** The minimum error over members at a cell, with the
identity of an attaining member recorded.

---

## 6. Two ladders, and why

UN-1 used one ladder for both task types and that was the root of
errors one and three. The two task types have different natural
budget ranges. Type I is a closed form and costs nothing at large
N. Type II is enumerated exhaustively and costs four to the power
N, so it cannot go far.

**Type I ladder.** N in {4, 8, 16, 32, 64, 128}. It starts at four
because that is the smallest budget at which the non-commuting
family has three members with distinct finite errors, which is what
the anti-vacuity bar requires. Starting a ladder where its family
is rich enough to be checked is the repair for errors one and
three.

**Type II ladder.** N in {1, 2, 3, 4, 5, 6}, as in UN-1.

**The anchor.** N equal to four appears on both ladders and is the
cell where the two task types are compared at identical budget on
identical substrate. The discriminator does not need a common
ladder, only a common substrate and a common meaning of budget, and
the anchor makes the comparison concrete at one shared rung.

**The boundary case.** N equal to one is computed for type I and
reported, and it is barred in section 7 rather than left to be
stumbled over.

---

## 7. Bars

The verdict is PASS only if all seven hold. Each is computed from
the record by the runner and none is pre-written.

Let C_compatible be the sum of the two variances and C_incompatible
be the square of the sum of the two standard deviations, both
computed by the runner from the declared state. These are the
continuum optima of the two families.

**Bar 1, type I falls at the reciprocal rate, replication-grade.**
For both pairs and every rung of the type I ladder, the frontier
error times N lies in the interval from C_pair to C_pair times
(1 + 2/N). This is the reciprocal law stated in a form an integer
allocation can satisfy, and it fails if the error falls at any
other rate.

**Bar 2, type I incompatibility costs a factor and not a floor.**
The ratio of the incompatible frontier to the compatible frontier
is finite at every type I rung, is at most 1.5 at every rung with N
at least eight, and at the top rung differs from
C_incompatible / C_compatible by at most two percent.

**Bar 3, type II compatible reaches zero.** The compatible frontier
is at most 1e-12 bits at every type II rung, including N equal to
one.

**Bar 4, type II incompatible does not move.** The incompatible
frontier varies across the type II ladder by at most 1e-11 bits,
and at every rung is at least the Maassen-Uffink value of one bit
less 1e-9.

The tolerance is 1e-11 and not 1e-12 because the exhaustive
summation over four to the power N records accumulates rounding,
and UN-1 measured that drift at 1.5e-13 at the top rung. A bar must
sit above the instrument's own noise floor, which is the lesson
PF-7 cost this campaign four attempts. The measured drift is
reported alongside the bar.

**Bar 5, anti-vacuity at every cell.** At each cell of both
ladders the runner confirms at least three members with pairwise
distinct finite errors, a named attaining member, and, for type II
cells, at least two records carrying probability above 1e-12 under
the attaining member. A cell failing any part fails this bar, and a
bar met only because a quantity was degenerate is not met.

**Bar 6, census.** Every cell of both ladders appears with a finite
frontier and a named attaining member. Two pairs by six rungs by
two task types is twenty-four cells, plus the two boundary cells of
bar 7.

**Bar 7, the boundary case is what UN-1 tripped over.** At N equal
to one under type I, the compatible frontier is finite and the
incompatible frontier is not. This states as a testable claim what
UN-1 met as an accident. At a single copy the declared family
cannot serve two non-commuting estimation tasks at all, because
every copy spent on one is a copy not spent on the other and there
is only one. If the incompatible frontier at N equal to one turns
out finite, the family is not what this document says it is.

---

## 8. What would refute the claim

Bar 1 failing at a rate other than reciprocal, which would mean the
closed form is wrong. Bar 2 failing upward, which would make type I
incompatibility a floor rather than a factor and collapse the
distinction. Bar 3 failing, which would mean commuting observables
admit no common record here. Bar 4 failing downward, which would
mean the type II floor is removable inside this family and the word
irreducible does not apply to it, or upward, which would mean the
enumeration is defective. Bar 5 failing anywhere, in which case the
bars that cell supports are vacuous and the run is void. Bar 7
failing, which would mean the family is not as described.

---

## 9. Anti-circularity

No uncertainty relation is supplied to the model. The
Maassen-Uffink value enters only as a comparison and is computed
from the declared observables. The continuum optima of bar 1 are
computed from the declared state and are not fitted. The family,
the grids, the two ladders, the state, the observables and all
seven bars are fixed here before the runner exists. No member is
added or removed after any error is seen, and the type II family is
enumerated exhaustively so no member can be selected after the
fact.

The floors reported are floors across the family of section 5. A
floor produced by restricting that family is a tautology, and the
family is declared in full so a reader can judge that.

---

## 10. Outputs

`results/un1b-discriminator.json`, a new path, because the UN-1
record at `results/un1-discriminator.json` is committed and this
campaign does not write a rerun over a committed record.
