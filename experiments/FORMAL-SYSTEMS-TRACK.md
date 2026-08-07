# FS Track: Removable and Irreducible Limits of a Formal Consumer

**Status:** SEALED UNRUN. Chip 📜 FS. The design is sealed and
timestamped, and no experiment in it may be executed until the
condition in section 8 is met. Sealing a design before it can run
is unusual in this campaign and the reason is given there.

---

## 1. Question

A formal theory is a consumer. Its channel is its axioms and
inference rules, its budget is the proof effort it may spend, and
its task is to decide declared sentences. Some of what such a
consumer cannot decide is a budget limitation that more search
removes. Some of it is not.

The track measures where that boundary sits in finite models, and
whether the frontier between decided and undecided has a shape
that belongs to the theory rather than to the proof calculus used
to search it.

---

## 2. Three guards, declared before any design

### 2.1 The vacuity guard

The statement that no admissible interface exhausts a rich
structure is nearly empty. It follows for cheap reasons from
counting and diagonalization, and it predicts incompleteness about
as well as gravity predicts general relativity. The content of
incompleteness lies in its mechanism, arithmetization together with
self-reference, and in the strength conditions under which it
applies.

**This track therefore claims nothing at that level of
generality.** It does not assert that observation theory explains,
implies, or illuminates the incompleteness theorems. It measures a
specific computable frontier and reports its shape.

### 2.2 The self-application prohibition

There is a tempting reading in which the second incompleteness
theorem, that a sufficiently strong consistent effective theory
cannot prove its own consistency, is the same principle as this
campaign's use of frozen declarations, external hashes, and
preregistration to certify its own runs.

**That reading is forbidden as a claim of this track.**
Preregistration works because it removes degrees of freedom from a
fallible agent. Incompleteness is a theorem about arithmetization
and self-reference. Treating them as instances of one principle is
the flexible reinterpretation that the generator experiment's null
hypothesis predicts, performed by us, on ourselves, inside the
program built to detect it. The resemblance may be recorded as a
resemblance and never as a result.

### 2.3 The methodological guard

Everywhere else the campaign varies a consumer and measures. Here
the surrounding facts are theorems, and the campaign's apparatus of
declared bars has no purchase on them. This track therefore
measures only what is genuinely computable, which is bounded proof
search over declared finite sentence sets, and it never asserts a
metamathematical fact it has not either proved or cited to the
literature. Independence results enter as citations and are
labelled as inputs.

---

## 3. Claim types

Instrument claims, that bounded proof search over declared finite
sentence sets is exact and reproducible. Structural claims measured
in model, about the shape of the decided fraction as a function of
budget and about its sensitivity to the proof calculus.
Replication claims, where the track recovers an established fact.
Claims about metamathematics, which nothing here supports beyond
what it cites.

---

## 4. Anti-circularity contract

No sentence known to be independent may be counted as evidence that
budget fails to decide it, because that outcome is settled by the
citation that put it there. No proof calculus may be selected after
seeing which one produces a wanted frontier. The sentence set, the
calculus, the budget ladder, and the bars are declared before any
run.

---

## 5. The declared objects

**Consumer.** A declared axiom set with a declared inference
calculus.

**Budget.** Maximum proof length, with proof-search node count
recorded alongside, on a declared ladder.

**Task.** Decide each sentence of a declared finite set, meaning
derive it or derive its negation.

**Distortion.** The fraction of the declared set left undecided at
a given budget.

---

## 6. Experiments

### FS-0: bounded proof search instrument

Exact bounded search over a declared calculus. Controls, a
propositional fragment where every declared sentence is decided at
finite budget, a sentence and its negation which must never both be
derived, a derivation replayed from its recorded certificate, and
agreement of the decided set across two independent search
strategies at equal budget.

### FS-1: the budget frontier and its prescription sensitivity

The track's real experiment, and the only one with a chance of
producing something not settled in advance.

For a declared decidable theory, measure the decided fraction as a
function of budget across the declared ladder. The limitation is
removable by construction, so the fraction reaching one is not the
result. **The result is the shape of the approach**, and whether
that shape survives a change of proof calculus at matched budget,
which is the campaign's prescription-sensitivity question applied
to logic.

Declared bars. The decided fraction is monotone in budget. It
reaches one at finite budget. The shape measured under two declared
calculi agrees within a declared tolerance, or it does not, and
either outcome is a result. If it does not agree, the frontier is a
property of the search and not of the theory, which would be the
more interesting finding and would narrow every claim of this
track.

### FS-2: the incomplete case, expected to be partly tautological

Design only. A declared theory together with a cited independent
sentence. The plateau of the decided fraction is partly settled by
the citation that placed the sentence in the set, so **the plateau
itself earns no credit**. What is measured is whether the approach
to the plateau has the same shape as the decidable case, which is
not settled by the citation.

### FS-3: the effectiveness and completeness trade

Design only. True arithmetic is complete and not effectively
axiomatizable, and effective theories of sufficient strength are
incomplete. Both halves are cited, not measured. The measurable
question in finite models is what the trade costs at bounded
budget, meaning how the decided fraction of a declared set varies
as axioms are added along a declared chain, and whether the gain
per added axiom has a stable form.

---

## 7. Expected replication-grade, declared in advance

The track expects to recover established facts, that a decidable
theory decides everything at sufficient budget and that an
incomplete one does not. Recovering a known result through this
machinery is modest and real. Declaring the expectation now is what
makes it modest rather than a discovery announced after the fact.

---

## 8. Why this is sealed unrun, and when it may run

`math.LO` and `cs.LO` are both in stratum F of the G1 domain pool
frozen in GENERATOR-DOMAIN-POOL-V3.md. The standing restriction
sealed with that pool forbids opening a track in any pooled
category until the twelve generator packets are scored, because
every domain touched informally is a prospective test domain spent.

**No experiment in this track may run until that restriction
lifts.** The design is sealed now so that it is timestamped and
cannot later be presented as having been conceived after seeing a
draw or a result.

**Contingency.** If the beacon draw of 2026-08-14 selects math.LO
or cs.LO, this track is withdrawn from the campaign entirely and
this document is recorded as a conflict rather than as a design.
The generator packet for that domain then stands alone and is
scored without reference to anything written here, and this
document is disclosed to the scorers' adjudicator as a prior
exposure so the conflict is on the record rather than in it.
