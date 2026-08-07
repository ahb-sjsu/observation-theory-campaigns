# UN Track: Removable and Irreducible Uncertainty

**Status:** design draft, unsealed, non-claim-bearing. Chip ⚖️ UN.
Everything is measured in declared exact finite models.

**This track is not a G1 test domain and cannot become one.**
quant-ph is on the exclusion list of GENERATOR-DOMAIN-POOL-V3.md
because it contributed to the kernel's construction through the QO
and QD tracks. Work here is a campaign track in its own right, in
the way GD and CR are, and it supplies no prospective evidence for
the generator claim.

---

## 1. Question

The campaign's recurring move is to hold a substrate fixed, vary
the admissible consumer, and see what moves. Applied to quantum
measurement it suggests a classification that the usual telling of
uncertainty does not make.

Some uncertainty is a consumer's limitation. Give the consumer more
budget, more access, or a better encoding and it goes away. Some
uncertainty survives every admissible consumer. The track question
is where that boundary lies, whether the two kinds separate
cleanly, and what fixes the floor when a floor exists.

The proposed reading, stated so it can be refuted, is that
**fundamental means invariant after quantifying over all
physically admissible observations**. That is a definition of a
word, not a discovery, and its content is entirely in whether the
classification it induces is sharp and whether the floor it leaves
behind has structure.

---

## 2. Three guards, declared before any design

These exist because the obvious version of this track would be
worthless, and each guard names a specific way it could be
worthless.

### 2.1 The tautology guard

The admissible consumer class is an input. If the class is every
quantum channel, then the statement that incompatible observables
resist every member of it is a theorem about the input, restated.
CAMPAIGN.md's anti-circularity contract and G1's fifth validity
condition both forbid a bar whose outcome is settled before the
run.

Therefore **no claim of this track is that quantum incompatibility
survives quantum consumers.** That is assumed, not tested. What is
tested is where the boundary between removable and irreducible
falls across a declared family, how the achievable frontier
approaches its floor, and whether that floor is fixed by the
quantities usually said to fix it. Any result that reduces to
restating a known relation is recorded as replication-grade and
carries no novelty credit.

### 2.2 The admissible-class relativity

Invariance here is invariance with respect to a declared class.
Allowing collective measurements on many copies gives one frontier,
allowing post-selection gives another, restricting to projective
measurements on the system alone gives a third. So the word
invariant in this track always means invariant across the declared
class and never means absolute.

This is consumer-relativity applied one level up, to the campaign's
own notion of fundamental, and it is stated rather than hidden. Any
claim of irreducibility carries its admissible class in the same
sentence.

### 2.3 The distinctness guard

Four literatures are adjacent here and conflating them produces
confident error. This track keeps them separate by name and never
transfers a bound from one to another.

Product-form relations of Robertson type, whose right side is
state-dependent and can vanish where uncertainty does not.
Entropic relations of Maassen-Uffink type, which do not have that
defect. Error-disturbance relations, where a public dispute turned
on competing definitions of error and disturbance rather than on
physics, so this track declares its definitions explicitly and
claims nothing about any other definition. And uncertainty with
quantum side information, which is the setting where a consumer
holds correlated memory.

---

## 3. The distinction that decides the answer

Declared in advance because getting it wrong would produce a
correct-looking wrong result.

**Type I task, expectation estimation.** The consumer receives N
copies of the declared state and must estimate the expectation
values of two observables. Error is mean squared estimation error.

**Type II task, single-shot outcome prediction.** The consumer
receives one copy, produces a record, and must then predict the
outcome of a projective measurement of one of two observables,
chosen after the record exists. Error is conditional entropy of the
outcome given the record.

These behave oppositely under the same budget ladder, and a design
that does not declare which it means will report whichever it
happened to implement. Measuring both on one substrate is the point
rather than a complication.

---

## 4. Claim types, never conflated

Instrument claims, that frontiers, entropies, and achievable
regions are computed exactly in finite models. Structural claims
measured in model, that a declared uncertainty separates into a
consumer-removable part and a part irreducible across a declared
class. Replication claims, that a measured floor coincides with a
known relation. Claims about physical reality, which nothing here
supports.

---

## 5. Anti-circularity contract

No uncertainty relation is supplied to a model as an input where it
is the measured question. No consumer family is chosen after seeing
which family produces a wanted frontier. No budget ladder is
truncated at the rung that gives a wanted limit. The admissible
class, the tasks, the ladder, and the bars are declared before any
run. A floor that was inserted by restricting the class is a
tautology and is recorded as one.

---

## 6. Experiments

### UN-0: exact frontier instrument layer

Qubit and qutrit substrates, states and POVMs as exact matrices,
conditional entropies and estimation errors computed in closed form
where closed forms exist. Controls, a compatible observable pair
where both task types must reach zero error, a maximally mixed
state where the record carries nothing, a trivial consumer whose
frontier is the no-information point, and a reproduction of the
Maassen-Uffink bound for two declared bases. No later experiment
runs until UN-0 passes.

### UN-1: the removability discriminator

The headline experiment. One substrate, two declared task types,
one declared consumer family, and a budget ladder in the number of
copies available to a collective measurement.

Measured, the achievable frontier's closest approach to zero error
at each rung, for a compatible pair and for an incompatible pair,
under both task types. The declared expectation, which the run may
refute, is that the type I frontier approaches zero for both pairs
while the type II frontier approaches zero only for the compatible
pair. If that holds, the classification is sharp and the floor is a
property of the pair rather than of the consumer.

### UN-2: is the floor the bound

Design only. The achievable type II floor is generally above the
Maassen-Uffink bound, which is tight only at special
configurations. Measured across a declared family of basis angles,
how far the achievable floor sits above the standard bound, and
whether that gap is itself a function of the overlap alone or
carries structure the overlap does not predict. This is the
track's best candidate for a non-tautological result, because
neither answer is settled by the setup.

### UN-3: side information, expected to be replication-grade

Design only. Consumers holding correlated quantum memory face a
lower floor than consumers without it, and with maximal
entanglement the floor reaches zero. This is a known theorem and
the track expects to recover it. Declaring that expectation in
advance is the point, because a framework that reproduces a known
result from its own machinery has demonstrated something modest
and real, and calling it novel afterwards would not.

---

## 7. Non-claims

Nothing here is evidence about physical measurement outside the
declared finite models. No claim is made that Heisenberg
uncertainty is observer-relative, and no claim is made that it is
not. No claim is made about any error-disturbance relation other
than the one this track defines. No claim of irreducibility
extends beyond its declared admissible class. Seals, labels,
append-only records, and falsification bars as in CAMPAIGN.md.
Substrate, exact finite models in Python on Atlas.
