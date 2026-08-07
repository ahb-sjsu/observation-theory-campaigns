# G2: the generator operator, second and governing version

**Status:** FROZEN CANDIDATE, awaiting seal. Once sealed, no field
below may change.

**Version:** G2. Supersedes G1 as the governing specification.
`GENERATOR-G1.md` stays in the repository unedited, as sealed, and
is the record of what was declared first.

**Written before the seed exists.** The draw is seeded by the NIST
randomness beacon pulse of 2026-08-14T00:00:00Z, whose value does
not exist as this is written. No domain is known. No packet has
been generated in any pooled domain.

---

## 1. Why there is a second version

The G1 dry run on an excluded domain found three defects in the
operator itself, registered as findings 1, 5 and 6 of
`GENERATOR-DRYRUN.md`. The rehearsal rule forbids editing G1 and
requires a successor naming what it repairs. This is that
successor.

All rehearsal scores were discarded and count for nothing. The
three repairs below were chosen to close the named defects without
touching anything that could move the primary endpoint's outcome
in a wanted direction. What follows section 5 is unchanged from G1
and is restated so that this document stands alone.

**The primary endpoint is not changed.** In the rehearsal A1 led
A2 by fourteen items to twelve on a domain the campaign knows
intimately. Adjusting the endpoint after seeing that would be
tuning, whether it moved the bar up or down. The threshold, the
tie rule, the sign test and the twelve domains are all carried
over exactly.

---

## 2. Repair one, the operator's text is now a sealed field

Finding 1 held that G1 fixed the operator's content without fixing
its operational text, so two faithful implementations could differ
and the experiment was not reproducible from the sealed document
alone.

Section 16 below contains the verbatim text given to each arm and
to the scorers. Those texts are sealed fields of this document.
The generating agent receives the text of section 16 for its arm
and the domain description, and nothing else. An implementation
that paraphrases a sealed text has not run this experiment.

The texts are the renderings committed in
`GENERATOR-INSTRUCTIONS.md` on 2026-08-07, plus the additions that
repairs two and three require and nothing else. Every addition is
marked in section 16 so the difference from the rehearsal text can
be read directly.

---

## 3. Repair two, levels must be anchored before they are used

Finding 5 held that the six-level taxonomy did not discriminate.
Levels zero and one were never used by any scorer on any item, and
consensus piled at three and four.

The ladder is **not recalibrated**. Rewriting the level
definitions after seeing which levels got used would be tuning of
exactly the kind this experiment exists to detect. The definitions
in section 8.1 are carried over word for word from G1.

Two things change instead, and both convert an impression into a
checkable claim.

**3.1 The justification requirement.** A scorer assigning any
level at or above two must state, in the same breath, what stops
the item being level one. That means naming the specific way the
item could come out other than as proposed. A level at or above
two with no such statement is recorded as level one.

**3.2 The calibration probe.** Before scoring any real packet,
each scorer scores the four calibration items of section 17
against the excluded domain cond-mat.stat-mech. Those four are
constructed to sit at levels zero, one, two and five, and their
intended levels are declared in section 17 before any scorer sees
them. A scorer who does not place the level-zero item at zero and
the level-one item at one is recorded as uncalibrated and is
replaced before any real scoring, with the replacement recorded.

If three successive scorer sets fail calibration, the level-based
endpoints are reported as unusable and said to be unusable in the
paper. **The primary endpoint does not use levels and stands
either way.** That is why it was built out of the five validity
conditions and not out of the ladder.

The calibration domain is on the permanent exclusion list and can
never be drawn, so calibration consumes no test domain.

---

## 4. Repair three, a scorer must name what an item restates

Finding 6 was the most serious. All three scorers independently
marked every one of the fifteen comparator items replication-grade
and none of the fifteen kernel items. A split that clean across
independent scorers is unlikely to be about content alone, and the
plausible mechanism is that familiar vocabulary reads as
restatement while unfamiliar vocabulary reads as new. If that is
what happened, replication-grade was measuring which arm wrote the
packet.

**4.1 Named restatement.** A scorer marking an item
replication-grade must name the established result it restates,
by its accepted name in the field or by a statement of the result
itself. An unnamed mark does not count and the item is recorded as
not replication-grade. This converts a judgment into a claim
another reader can check.

**4.2 The same requirement where impression can satisfy a
condition.** Validity condition three, domain-native content, is
satisfiable on impression in the same way and in the opposite
direction, so a scorer answering yes to it must name the quantity
and say what a practitioner of the domain uses it for. An unnamed
yes is recorded as no.

Condition three is part of the primary endpoint and this
requirement makes it harder to satisfy. The vocabulary mechanism
of finding 6 predicts that the harm falls on the arm writing in
unfamiliar vocabulary, which is A1. **The repair is therefore
conservative against the hypothesis under test**, and that is
recorded here rather than discovered afterwards.

**4.3 What is not repaired.** Full blinding remains unachievable,
for the reason in finding 2. The arms produce recognizably
different vocabulary and a scorer may infer the arm from style.
The mitigation is unchanged, that scorers are never told one arm
is the hypothesis and another the control, are never told how many
arms exist, and receive only a domain description, an item list
and the rubric. Style may leak but direction does not. The
residual risk is a limitation of the experiment and must appear in
the paper.

---

## 5. What is carried over unchanged

The claim under test, the input rules, the observation tuple, the
fifteen required packet contents, the eight question operators,
the five validity conditions, the level ladder's definitions, the
arms, the primary and secondary endpoints, the execution subset,
the stopping rules, the failure taxonomy, the falsification
conditions, the interpretation ladder, the known limitations and
the output paths. They are restated in sections 6 through 15 so
that this document governs on its own.

The domain pool is unchanged and stays sealed in
`GENERATOR-DOMAIN-POOL-V3.md`. The draw algorithm is unchanged and
stays in `python/g1_draw.py`. The standing restriction is
unchanged, that no new track may be opened in any pooled arXiv
category until the twelve packets are scored.

---

## 6. The claim under test

**H0, flexible reinterpretation.** The vocabulary of substrates,
consumers, channels, tasks, and budgets is expressive enough that
almost any scientific content can be rewritten in it after the
fact, so the apparent productivity is redescription.

**H1, generative structure.** The discipline imposes constraints
strong enough that, supplied with a domain it did not help
construct, it produces non-obvious falsifiable questions with
domain-native content.

What is tested is the operator, not any result it produces, and
not the truth of any ontological reading of the discipline.

Two claims must not be conflated. The declaration-before-run
discipline is already prospectively evidenced, because every
preregistration in this campaign was declared before its run and
its failures are in the record. The generator claim is a different
and untested claim about whether the kernel's structure produces
research in domains it has never seen.

---

## 7. Inputs, the tuple, the packet, the operators, the conditions

**Permitted input.** Exactly one domain description, taken
verbatim from an external source that no member of this campaign
authored, and nothing else.

**Forbidden.** Any target phenomenon the packet is meant to find,
any statement of what the campaign expects to be true in the
domain, any prior campaign result, any hint about which arm is
running, and any material added after the domain is drawn. A
packet containing one is void. Every arm receives the identical
description, verbatim.

**The tuple.** Omega equals (X, C, T, B, E), with X the substrate
or hidden state, C the consumer with its channel, T the task the
consumer must serve, B the budget or resource limit, and E the
environment and intervention structure. Every generated object
must be a property of Omega or of a declared family of Omegas.

**The fifteen required packet contents.** A proposed substrate
with what is hidden from whom. A declared consumer family of at
least three members including a null consumer that reads nothing
and a maximal consumer that reads everything the substrate
permits. Channel definitions given exactly as maps from substrate
to record. At least two declared tasks that are not monotone
functions of one another. A budget or scarcity parameter with a
declared ladder and the value at which scarcity vanishes.
Candidate consumer-relative observables. Candidate substrate
invariants. Induced equivalence classes and any information or
decision orderings. Positive controls. Negative controls.
Anti-circularity checks naming what may not enter the model. At
least one prediction the generator expects to fail. Quantitative
tests with numerical bars fixed in the packet. Falsification
conditions for every claim. Stopping rules and the declared
compute limit. A packet missing any item is malformed and scores
zero.

**The eight question operators**, applied exactly and with no
others, each yielding at least one item or recorded as not
applicable with a reason. Q1 channel variation. Q2 task
variation. Q3 budget variation. Q4 consumer-family consistency.
Q5 invariance. Q6 garbling and data processing. Q7 mechanism
removal. Q8 prescription sensitivity. Their statements are in the
sealed arm text of section 16.

**The five validity conditions.** Prospective specificity.
Falsifiability. Domain-native content. Counterfactual leverage.
Non-tautology. An item earns credit only if it satisfies all five.

---

## 8. Scoring

### 8.1 Item taxonomy, definitions carried over word for word

- 0 invalid, malformed or domain-inappropriate.
- 1 tautological, true by construction.
- 2 valid null, well posed and correctly predicting absence.
- 3 nontrivial measured result, a prospective quantitative effect
  that survives its bars.
- 4 structural result, a general mechanism or invariant.
- 5 exact result, a theorem or closed-form identity.

Separately and not on this ladder, an item is marked
replication-grade when it correctly rediscovers an established
domain result from the supplied description alone, **and the
scorer names that result** as section 4.1 requires.
Replication-grade is evidence of generativity and is not novelty,
and the two are reported separately and never summed.

Any level at or above two carries the justification of section
3.1 or is recorded as level one.

### 8.2 Blind scoring

Packets are stripped of arm labels, normalized to one format, and
presented in randomized order. Three independent scorers who have
not seen this document score each item against the taxonomy and
the five validity conditions, after passing the calibration probe
of section 3.2. The consensus is the median. Any item whose scores
span more than one level goes to a fourth adjudicator whose
decision is final and recorded.

Scoring by language models is itself a limitation and is reported
as such, with the scorer identity, version, and prompt recorded in
the evidence.

### 8.3 Novelty

Novelty is assessed against the field and not against the supplied
description, by a literature check recorded per item. An item
already known to the field is not scored as novel even if it is
absent from the description. Novelty is scored conservatively and
reported separately from the taxonomy.

---

## 9. Arms

- **A1 full kernel.** The sealed text of section 16.1.
- **A2 structured control.** The sealed text of section 16.2. A
  generic instruction to design a preregistered falsification
  study, containing no substrate, consumer, channel, task or
  budget content and none of the eight question operators. This is
  the primary comparator, because it isolates this structure from
  structure in general.
- **A3 free-form.** The sealed text of section 16.3. A floor, not
  a comparator.
- **Ablations,** each identical to A1 with one part removed. A4
  removes Q1. A5 removes the task layer, deleting Q2, Q6 and the
  requirement of two tasks. A6 removes the budget layer and Q3. A7
  removes the controls, the anti-circularity checks and the five
  validity conditions. Each ablation text is A1's text with the
  named passages struck and nothing else altered.

---

## 10. Endpoints

### 10.1 Primary, unchanged from G1

For each drawn domain, count the packet items that satisfy all
five validity conditions by consensus blind scoring. Compare A1
against A2 pairwise within domain.

**The primary endpoint is the number of domains in which A1's
count exceeds A2's.** With twelve domains drawn, the declared
success threshold is ten or more, a one-sided sign test at p equal
to 0.019 under the null of no difference. Ties count against A1.

The primary endpoint is scored on packets alone and requires no
result-bearing computation, so it cannot be affected by how much
compute any arm received. It does not use the level ladder.

### 10.2 Secondary, subordinate, and now conditional

- Mean per-domain count of items scoring three or higher after
  execution, on the execution subset. **Reported only if
  calibration passed.**
- Ablation contrasts, A1 against each of A4 through A7.
- Replication-grade rate, counting only named marks.
- Novelty rate.
- Rate of packets containing at least one correct prospective
  null.
- A3 as a floor.

No secondary endpoint may be reported as the paper's result.

---

## 11. Execution subset

After packets are generated and sealed, four domains are drawn
from the twelve by the same beacon protocol for full execution and
six for the ablation arms. The draws happen after packet sealing
so that no packet can be written toward an anticipated execution.

---

## 12. Stopping rules

Twelve domains, drawn once, no redraws for any reason. At most
fifteen items per packet, with items beyond fifteen discarded from
the end before scoring. One generation pass per arm per domain,
with a failed or malformed generation recorded as scored and not
retried. A declared compute ceiling per executed experiment, with
overruns recorded as unresolved rather than extended. No arm may
be rerun after any scoring has been seen. Scorer replacement is
permitted only for calibration failure, only before any real
scoring, and is recorded.

---

## 13. Failure taxonomy

Generator failure, no meaningful domain mapping exists. Tautology
failure, the outcome was inserted by construction. Instrument
failure, the measurement path was invalid. Declaration failure,
the bar or the bookkeeping was wrong while the model was not.
Model failure, the proposed structure is absent from the domain.
Surprise success, the proposed model fails and the run exposes
structure the declaration did not anticipate. Scope failure, the
claim exceeded what a finite model licenses.

A failed substantive hypothesis is not a generator failure. The
generator's task is to produce productive falsifiable inquiries,
not true ones.

---

## 14. What would falsify the generator claim

- A1 does not exceed A2 in at least ten of twelve domains.
- Most new-domain mappings are judged arbitrary by blind scorers.
- Most generated items are scored tautological.
- Ablating the kernel produces no measurable loss of yield.
- Substantive predictions require importing target-domain results
  that section 7 forbids.
- Apparent successes cannot be scored without the scorer knowing
  which arm produced the packet.
- Failed applications are rescued by redefining the consumer, the
  task, or the channel after seeing an outcome.

---

## 15. Interpretation ladder and known limitations

The experiment is designed to reach level two and possibly level
three. Levels four and five are named only so the paper cannot
later be read as having claimed them. 0, the discipline supplies a
useful vocabulary. 1, it supplies a reusable audit methodology. 2,
it systematically generates falsifiable scientific questions. 3,
its question structure transfers to unrelated domains. 4, repeated
cross-domain results expose common mathematics. 5, a general
calculus of representation exists.

The operator is executed by a language model with broad scientific
priors, so a positive result is confounded with the capability of
that model, and the ablation contrasts rather than the A1 against
A2 contrast are what speak to the kernel's internal structure. The
same model runs every arm and cannot unlearn the discipline.
Scoring is model-assisted. Tractability of finite models shapes
which questions can be executed. Novelty judgments are imperfect.
The mapping of domain vocabulary onto the tuple retains
flexibility that this document constrains but does not eliminate.
Blinding is partial for the reason in section 4.3.

---

## 16. Sealed operator texts

An implementation gives the text of the relevant subsection, in
full and unparaphrased, together with the domain description and
nothing else. Passages marked **[G2 addition]** are the only text
here that is not the rehearsal rendering of 2026-08-07; each is
required by repair two or repair three.

### 16.1 Arm A1, the full kernel

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
> **[G2 addition]** For each item, name the quantity in it that a
> practitioner of this domain would recognize, and say in one
> clause what that practitioner uses it for. An item with no such
> quantity is one you should not write.
>
> Produce at most fifteen items. Do not use any knowledge of what
> results this domain is expected to yield. Do not import results
> from outside the description you were given.

### 16.2 Arm A2, the structured comparator

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
> **[G2 addition]** For each item, name the quantity in it that a
> practitioner of this domain would recognize, and say in one
> clause what that practitioner uses it for. An item with no such
> quantity is one you should not write.
>
> Produce at most fifteen items. Do not use any knowledge of what
> results this domain is expected to yield. Do not import results
> from outside the description you were given.

### 16.3 Arm A3, the free-form floor

> You are given a description of a scientific domain. Generate
> interesting research questions for it. Produce at most fifteen.

### 16.4 Scorer instruction

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
> **[G2 addition]** If you assign a level of two or higher, state
> in the same answer what stops this item being level one, by
> naming the specific way it could come out other than as the item
> proposes. If you cannot name one, assign level one.
>
> Then answer five yes or no questions about the item. Does it
> commit to a question and its bars before the answer is known? Does
> it name an outcome that would count against it? Does at least one
> quantity in it mean something to a practitioner of this domain?
> Would changing a declared component of the setup yield a
> different quantitative prediction? Is it free of the defect that
> its outcome is settled by how the setup was defined?
>
> **[G2 addition]** If you answer yes to the third question, name
> the quantity and say what a practitioner of this domain uses it
> for. A yes with no named quantity will be read as a no.
>
> Separately mark an item replication-grade if it correctly
> restates or rediscovers an established result of this domain.
> Replication-grade is not a level and is never added to one.
>
> **[G2 addition]** If you mark an item replication-grade, name the
> established result it restates, either by the name the field uses
> for it or by stating the result itself. A mark with no named
> result will be read as not replication-grade.
>
> Give a one-sentence reason for each level. Do not speculate about
> where the items came from.

---

## 17. Calibration items, with their intended levels declared here

Scored against the excluded domain cond-mat.stat-mech, whose
frozen description is "Phase transitions, thermodynamics, field
theory, non-equilibrium phenomena, renormalization group and
scaling, integrable models, turbulence". That domain is on the
permanent exclusion list and can never be drawn.

The four items are presented to a scorer mixed into a list, in the
order given, without their intended levels and without any
indication that they are calibration items.

**K1, intended level 0.** "Measure the ratio of the model's
critical temperature to the number of papers the field published
last year, and report whether that ratio exceeds four."

Inappropriate to the domain. A quantity of the field's sociology
is not a quantity of the model.

**K2, intended level 1.** "Define a coarse-graining that maps
every microstate to a single symbol. Test whether an observer
holding only that symbol can distinguish any two microstates, with
the bar that it distinguishes none."

True by construction. A constant map distinguishes nothing because
it is a constant map.

**K3, intended level 2.** "Predict that the measured critical
exponent is unchanged when the lattice's local coordination number
is changed while the dimension and the order-parameter symmetry
are held fixed, with a bar of two percent across a declared family
of three lattices."

A well posed null predicting an absence. It could come out
otherwise, so it is not level one, and it is not a quantitative
effect, so it is not level three.

**K4, intended level 5.** "Prove that for any two coarse-grainings
where the second factors through the first, the mutual information
between the microstate and the record is no larger for the second
than for the first."

An exact result with a closed-form proof.

**The calibration bar.** A scorer must place K1 at zero and K2 at
one. K3 and K4 are recorded but do not gate, because the middle
and the top of the ladder were not where the rehearsal found the
defect and adding bars there would be tuning past the fault.

---

## 18. Outputs

Each packet is written to `results/g2-packet-<domain>-<arm>.json`,
hashed, and committed before any result-bearing computation on
that domain. Calibration responses are written to
`results/g2-calibration.json` before any real scoring. Scores are
written to `results/g2-scores.json` after all packets are sealed.
