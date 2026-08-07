# G1: a frozen research generator, specification for freezing

**Status:** FROZEN CANDIDATE, awaiting seal. Once sealed, no field
below may change. An edit voids the seal and creates G2.

**Version:** G1

**Purpose.** This document specifies a domain-independent operator
that maps a domain description to a registered research packet. It
is frozen before any test domain is known so that its output on
new domains is prospective rather than fitted.

---

## 1. The claim under test

The campaign has applied one observational discipline to thirteen
domains and produced technically distinct research in each. Two
explanations compete.

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

**Two claims must not be conflated.** The declaration-before-run
discipline is already prospectively evidenced, because every
preregistration in this campaign was declared before its run and
its failures are in the record. The generator claim is a different
and untested claim about whether the kernel's structure produces
research in domains it has never seen.

---

## 2. Inputs

### 2.1 Permitted

The generator receives exactly one domain description, taken
verbatim from an external source that no member of this campaign
authored, and nothing else. The description may characterize the
domain's state space, dynamics, canonical observables and
operations, accepted symmetries and constraints, standard
definitions, and tractability limits.

### 2.2 Forbidden

The generator may not receive, and its operator may not supply,
any of the following. A packet that contains one is void.

- Any target phenomenon, effect, or result the packet is meant to
  find.
- Any statement of what the campaign expects to be true in the
  domain.
- Any prior campaign result, except where a domain description
  itself is a replication anchor declared as such in advance.
- Any hint about which arm of the experiment is running.
- Any material added after the domain is drawn.

### 2.3 One description, all arms

Every arm of the experiment receives the identical domain
description, verbatim. No arm receives more context than another.

---

## 3. The observation tuple

The kernel's single canonical object is

Omega = (X, C, T, B, E)

with X the substrate or hidden state, C the consumer with its
channel, T the task or functional the consumer must serve, B the
budget or resource limit, and E the environment and intervention
structure.

Every generated object below must be expressed as a property of
Omega or of a declared family of Omegas.

---

## 4. Required packet contents

For its domain, the generator must output all of the following.
A packet missing any item is malformed and scores zero.

1. A proposed substrate, with what is hidden from whom.
2. A declared consumer family, at least three members, including a
   null consumer that reads nothing and a maximal consumer that
   reads everything the substrate permits.
3. Channel definitions, exactly, as maps from substrate to record.
4. At least two declared tasks that are not monotone functions of
   one another.
5. A budget or scarcity parameter with a declared ladder, and the
   value at which scarcity vanishes.
6. Candidate consumer-relative observables.
7. Candidate substrate invariants.
8. Induced equivalence classes and any information or decision
   orderings.
9. Positive controls, where the effect must appear.
10. Negative controls, where it must not.
11. Anti-circularity checks naming what may not enter the model.
12. At least one prediction the generator expects to fail.
13. Quantitative tests with numerical bars fixed in the packet.
14. Falsification conditions for every claim.
15. Stopping rules and the declared compute limit.

---

## 5. The question operators

The generator applies exactly these eight and no others. Each must
yield at least one packet item or be recorded as not applicable
with a reason.

- **Q1 channel variation.** Hold substrate and task fixed and vary
  the channel. What moves and what does not?
- **Q2 task variation.** Hold substrate and channel fixed and vary
  the task. Which rankings reverse?
- **Q3 budget variation.** Does the consumer-relative structure
  vanish as scarcity vanishes?
- **Q4 consumer-family consistency.** Does requiring agreement
  across overlapping consumers constrain the model?
- **Q5 invariance.** Which quantities survive every admissible
  consumer?
- **Q6 garbling and data processing.** Is an apparent scalar
  ordering backed by an ordering of experiments, or only by a
  number?
- **Q7 mechanism removal.** Does deleting the proposed structural
  source destroy the effect?
- **Q8 prescription sensitivity.** Does the phenomenon survive an
  alternative exact or continuous representation of the same
  content?

---

## 6. Validity conditions

A generated item earns credit only if it satisfies all five. These
generalize the campaign's standing rule that renaming a standard
object is not a contribution.

1. **Prospective specificity.** The item commits to a question and
   its bars before any answer is known.
2. **Falsifiability.** The item names an outcome that would count
   against its own proposed decomposition.
3. **Domain-native content.** At least one quantity in the item is
   meaningful to a practitioner of the domain and is not stated
   only in consumer vocabulary.
4. **Counterfactual leverage.** Changing a declared component of
   Omega yields a different quantitative prediction.
5. **Non-tautology.** The result does not follow from how the
   consumer was defined. A bar whose outcome is settled before the
   run tests nothing.

---

## 7. Scoring

### 7.1 Item taxonomy

- 0 invalid, malformed or domain-inappropriate.
- 1 tautological, true by construction.
- 2 valid null, well posed and correctly predicting absence.
- 3 nontrivial measured result, a prospective quantitative effect
  that survives its bars.
- 4 structural result, a general mechanism or invariant.
- 5 exact result, a theorem or closed-form identity.

Separately and not on this ladder, an item is marked
**replication-grade** when it correctly rediscovers an established
domain result from the supplied description alone. Replication-
grade is evidence of generativity and is not novelty, and the two
are reported separately and never summed.

### 7.2 Blind scoring

Packets are stripped of arm labels, normalized to one format, and
presented in randomized order. Three independent scorers who have
not seen this document score each item against the taxonomy and
the five validity conditions. The consensus is the median. Any
item whose scores span more than one level goes to a fourth
adjudicator whose decision is final and recorded.

Scoring by language models is itself a limitation and is reported
as such, with the scorer identity, version, and prompt recorded in
the evidence.

### 7.3 Novelty

Novelty is assessed against the field and not against the supplied
description, by a literature check recorded per item. An item
already known to the field is not scored as novel even if it is
absent from the description. Novelty is scored conservatively and
reported separately from the taxonomy.

---

## 8. Arms

- **A1 full kernel.** This document applied in full.
- **A2 structured control.** A generic instruction to design a
  preregistered falsification study for the domain, with declared
  controls, bars, and failure conditions, containing no substrate,
  consumer, channel, task, or budget content and none of the eight
  question operators. This is the primary comparator, because it
  isolates this structure from structure in general.
- **A3 free-form.** An instruction to generate interesting
  research questions for the domain, with no further constraint.
  A floor, not a comparator.
- **Ablations,** each identical to A1 with one part removed.
  A4 removes the channel operator Q1. A5 removes the task layer,
  which deletes Q2 and Q6 and the requirement of two tasks. A6
  removes the budget layer and Q3. A7 removes the controls,
  anti-circularity checks, and the five validity conditions.

---

## 9. Endpoints

### 9.1 Primary, fixed now

For each drawn domain, count the packet items that satisfy all
five validity conditions by consensus blind scoring. Compare A1
against A2 pairwise within domain.

**The primary endpoint is the number of domains in which A1's
count exceeds A2's.** With twelve domains drawn, the declared
success threshold is ten or more, which is a one-sided sign test
at p equal to 0.019 under the null of no difference. Ties count
against A1.

The primary endpoint is scored on packets alone and requires no
result-bearing computation, so it cannot be affected by how much
compute any arm received.

### 9.2 Secondary, declared now and subordinate

- Mean per-domain count of items scoring three or higher after
  execution, on the execution subset.
- Ablation contrasts, A1 against each of A4 through A7, on the
  ablation subset.
- Replication-grade rate.
- Novelty rate.
- Rate of packets containing at least one correct prospective null.
- A3 as a floor.

No secondary endpoint may be reported as the paper's result.

---

## 10. Execution subset

Full execution of twelve domains is beyond the declared compute.
After packets are generated and sealed, four domains are drawn
from the twelve by the same beacon protocol for full execution,
and six are drawn for the ablation arms. The draws happen after
packet sealing so that no packet can be written toward an
anticipated execution.

---

## 11. Stopping rules

- Twelve domains, drawn once, no redraws for any reason.
- At most fifteen items per packet. Items beyond fifteen are
  discarded from the end before scoring.
- One generation pass per arm per domain. A failed or malformed
  generation is recorded as scored, not retried.
- Declared compute ceiling per executed experiment, recorded in
  the packet, with overruns recorded as unresolved rather than
  extended.
- No arm may be rerun after any scoring has been seen.

---

## 12. Failure taxonomy

Every failure is classified and kept in the record.

1. Generator failure, no meaningful domain mapping exists.
2. Tautology failure, the outcome was inserted by construction.
3. Instrument failure, the measurement path was invalid.
4. Declaration failure, the bar or the bookkeeping was wrong while
   the model was not.
5. Model failure, the proposed structure is absent from the domain.
6. Surprise success, the proposed model fails and the run exposes
   structure the declaration did not anticipate.
7. Scope failure, the claim exceeded what a finite model licenses.

A failed substantive hypothesis is not a generator failure. The
generator's task is to produce productive falsifiable inquiries,
not true ones.

---

## 13. What would falsify the generator claim

The claim fails if any of the following holds.

- A1 does not exceed A2 in at least ten of twelve domains.
- Most new-domain mappings are judged arbitrary by blind scorers.
- Most generated items are scored tautological.
- Ablating the kernel produces no measurable loss of yield.
- Substantive predictions require importing target-domain results
  that section 2.2 forbids.
- Apparent successes cannot be scored without the scorer knowing
  which arm produced the packet.
- Failed applications are rescued by redefining the consumer, the
  task, or the channel after seeing an outcome.

---

## 14. Interpretation ladder

The experiment is designed to reach level two and possibly level
three. Levels four and five are named here only so that the paper
cannot later be read as having claimed them.

0. The discipline supplies a useful vocabulary.
1. It supplies a reusable audit methodology.
2. It systematically generates falsifiable scientific questions.
3. Its question structure transfers to unrelated domains.
4. Repeated cross-domain results expose common mathematics.
5. A general calculus of representation exists.

---

## 15. Known limitations, declared before the run

The operator is executed by a language model with broad scientific
priors, so a positive result is confounded with the capability of
that model, and the ablation contrasts rather than the A1 against
A2 contrast are what speak to the kernel's internal structure. The
same model runs every arm and cannot unlearn the discipline.
Scoring is model-assisted. Tractability of finite models shapes
which questions can be executed. Novelty judgments are imperfect.
The mapping of domain vocabulary onto the tuple retains
flexibility that this document constrains but does not eliminate.

---

## 16. Outputs

Each packet is written to `results/g1-packet-<domain>-<arm>.json`,
hashed, and committed before any result-bearing computation on
that domain. Scores are written to `results/g1-scores.json` after
all packets are sealed.
