# Operational renderings of the G1 arms

Committed 2026-08-07. These render the sealed specification into
the text actually given to a generating or scoring agent. They add
no content beyond GENERATOR-G1.md and exist because that document
fixes the operator's content without fixing its operational text,
which is recorded as an operator defect in GENERATOR-DRYRUN.md and
must be closed in G2.

Every arm receives the identical domain description and nothing
else. No arm is told that other arms exist.

---

## Arm A1, the full kernel

> You are given a description of a scientific domain. Produce a
> registered research packet for it.
>
> Use one canonical object throughout. Write Omega equals the tuple
> of X the substrate or hidden state, C the consumer together with
> its channel, T the task or functional the consumer must serve, B
> the budget or resource limit, and E the environment and
> intervention structure. Every object you propose must be a
> property of Omega or of a declared family of Omegas.
>
> Your packet must contain all fifteen of the following. A packet
> missing any one is void. A proposed substrate with what is hidden
> from whom. A declared consumer family of at least three members
> including a null consumer that reads nothing and a maximal
> consumer that reads everything the substrate permits. Channel
> definitions given exactly as maps from substrate to record. At
> least two declared tasks that are not monotone functions of one
> another. A budget or scarcity parameter with a declared ladder
> and the value at which scarcity vanishes. Candidate
> consumer-relative observables. Candidate substrate invariants.
> Induced equivalence classes and any information or decision
> orderings. Positive controls where the effect must appear.
> Negative controls where it must not. Anti-circularity checks
> naming what may not enter the model. At least one prediction you
> expect to fail. Quantitative tests with numerical bars fixed in
> the packet. Falsification conditions for every claim. Stopping
> rules and a declared compute limit.
>
> Apply exactly these eight question operators and no others. Each
> must yield at least one packet item or be recorded as not
> applicable with a reason. Q1, hold substrate and task fixed and
> vary the channel, and ask what moves and what does not. Q2, hold
> substrate and channel fixed and vary the task, and ask which
> rankings reverse. Q3, ask whether the consumer-relative structure
> vanishes as scarcity vanishes. Q4, ask whether requiring
> agreement across overlapping consumers constrains the model. Q5,
> ask which quantities survive every admissible consumer. Q6, ask
> whether an apparent scalar ordering is backed by an ordering of
> experiments or only by a number. Q7, ask whether deleting the
> proposed structural source destroys the effect. Q8, ask whether
> the phenomenon survives an alternative exact or continuous
> representation of the same content.
>
> Every item you produce must satisfy five conditions. It commits
> to a question and its bars before any answer is known. It names
> an outcome that would count against its own proposed
> decomposition. At least one quantity in it is meaningful to a
> practitioner of the domain and is not stated only in the
> vocabulary of consumers and channels. Changing a declared
> component yields a different quantitative prediction. And it does
> not follow from how the consumer was defined, because a bar whose
> outcome is settled before the run tests nothing.
>
> Produce at most fifteen items. Do not use any knowledge of what
> results this domain is expected to yield. Do not import results
> from outside the description you were given.

---

## Arm A2, the structured comparator

> You are given a description of a scientific domain. Design a
> preregistered falsification study for it.
>
> Your design must state what is being tested, the quantities to be
> measured, the controls that must behave in a declared way, the
> numerical bars fixed before any run, the conditions under which
> the design would be judged to have failed, what may not enter the
> model, and the stopping rules and compute limit.
>
> Every item you produce must satisfy five conditions. It commits
> to a question and its bars before any answer is known. It names
> an outcome that would count against it. At least one quantity in
> it is meaningful to a practitioner of the domain. Changing a
> declared component yields a different quantitative prediction.
> And it does not follow from how the study was set up, because a
> bar whose outcome is settled before the run tests nothing.
>
> Produce at most fifteen items. Do not use any knowledge of what
> results this domain is expected to yield. Do not import results
> from outside the description you were given.

---

## Arm A3, the free-form floor

> You are given a description of a scientific domain. Generate
> interesting research questions for it. Produce at most fifteen.

---

## Scorer instruction

Scorers receive the domain description, one normalized item list,
and this rubric. They are not told how many arms exist, which arm
produced anything, or that any hypothesis is under test.

> You are given a description of a scientific domain and a list of
> proposed research items. Score each item independently.
>
> Assign one level. Zero, invalid, malformed or inappropriate to
> the domain. One, tautological, true by construction. Two, a valid
> null, well posed and correctly predicting an absence. Three, a
> nontrivial prospective quantitative claim with bars it could
> fail. Four, a structural claim identifying a general mechanism or
> invariant. Five, an exact claim, a theorem or closed-form
> identity.
>
> Then answer five yes or no questions about the item. Does it
> commit to a question and its bars before the answer is known? Does
> it name an outcome that would count against it? Does at least one
> quantity in it mean something to a practitioner of this domain?
> Would changing a declared component of the setup yield a
> different quantitative prediction? Is it free of the defect that
> its outcome is settled by how the setup was defined?
>
> Separately mark an item replication-grade if it correctly
> restates or rediscovers an established result of this domain.
> Replication-grade is not a level and is never added to one.
>
> Give a one-sentence reason for each level. Do not speculate about
> where the items came from.
