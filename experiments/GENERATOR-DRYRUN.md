# G1 dry run: harness rehearsal on an excluded domain

**Status:** declared 2026-08-07, before the rehearsal. Not
claim-bearing. No result here counts for or against the generator
claim.

## Purpose

The G1 experiment can fail on plumbing rather than on science. The
packet schema, the operator's operational text, the normalizer that
strips arm identity, the scorer instruction, and the adjudication
path are all untested. This rehearsal exercises them end to end so
that the twelve real packets are not the first time anything runs.

## Domain

Originally quant-ph, changed to cond-mat.stat-mech before any
generation ran, for the reason in finding 3 below. Both are on the
exclusion list and can never be drawn, so nothing learned here can
contaminate the experiment and no test domain is consumed. The
description supplied is the frozen one from the taxonomy, "Phase
transitions, thermodynamics, field theory, non-equilibrium
phenomena, renormalization group and scaling, integrable models,
turbulence".

Using a domain the campaign knows well is acceptable here because
the rehearsal measures whether the harness runs and not whether the
generator is any good.

## The rule that governs the rehearsal

G1 is sealed. This rehearsal may find and fix defects in the
harness freely, meaning the schema, the scripts, the instruction
rendering, and the scoring plumbing. It may not change the
operator. If the rehearsal exposes a flaw in G1 itself, the flaw is
recorded here and a successor G2 is created naming it. G1 is never
edited. Without that rule the rehearsal is a back door to tuning
the operator after sealing.

## What is measured

Nothing about the generator's merit. The rehearsal reports only
whether each harness component ran, what broke, and what the fixes
were. Any scores produced are discarded and are marked as
rehearsal in their record.

## Findings register

Defects are recorded here as they are found, each classified as a
harness defect, fixable now, or an operator defect, which becomes
a G2 item.

### Finding 1, operator defect, G2 item

G1 specifies the operator's content in sections 3 through 6 but
does not fix its operational text. Two people implementing G1
faithfully could write materially different instructions and
obtain different packets, so the operator as sealed is
underdetermined and the experiment is not reproducible from the
sealed document alone.

The rehearsal proceeds with a rendering committed as
`experiments/GENERATOR-INSTRUCTIONS.md`, which quotes the sealed
sections and adds no content. That rendering is a faithful
implementation but it is not the only possible one, and the gap is
real. G2 must include the verbatim operator text and the verbatim
comparator text as sealed fields.

### Finding 2, harness limitation, recorded not fixed

Full blinding of scorers is not achievable. The arms produce
recognizably different vocabulary, since the kernel arm speaks of
substrates, consumers, channels, tasks and budgets while the
comparator does not, so a scorer may infer which arm produced a
packet from style alone.

The mitigation, declared here, is that scorers are never told that
one arm is the hypothesis and another the control, are never told
how many arms exist, and receive only a domain description, an
item list, and the rubric. Style may leak but direction does not,
and a scorer with no stake in which arm wins has no lever to
apply. The residual risk is recorded as a limitation of the
experiment and must appear in the paper.

### Finding 3, the same defect from another angle

quant-ph was chosen as the rehearsal domain precisely because it is
excluded, and it turned out to be one of the three categories whose
published description is the placeholder. It could not supply the
rehearsal with an input, which is the same defect that
GENERATOR-DOMAIN-POOL-V3.md removed from the pool, met a second
time from a different direction. The rehearsal domain was changed
to cond-mat.stat-mech before any generation ran. Recorded because
the coincidence is a useful reminder that the defect was not
hypothetical.

### Finding 4, harness result, positive

The primary endpoint is measurable with three scorers. Across
thirty items the adjudication rate was zero. Twenty-one items drew
identical levels from all three scorers and nine differed by one
level, and no item differed by more than one, so the adjudication
path never fired. Inter-scorer agreement is not the bottleneck the
rehearsal was designed to look for.

### Finding 5, operator defect, G2 item

The level taxonomy does not discriminate. Consensus levels were one
item at two, twelve at three, fourteen at four, and three at five.
Levels zero and one were never used by any scorer on any item. A
six-level ladder on which four levels never appear is not measuring
what it was built to measure, and either the ladder is
miscalibrated for packets that were written to a rubric or scorers
are lenient in a way the rubric does not restrain.

This matters less than it might because the primary endpoint counts
the five validity conditions rather than levels, and those did
discriminate, failing three times on counterfactual leverage and
once on being settled by the setup. The secondary endpoints that
use levels are weakened. G2 must either recalibrate the ladder or
demote level-based endpoints.

### Finding 6, operator defect, G2 item, and the most serious

Replication-grade may be tracking vocabulary rather than novelty.
All three scorers independently marked every one of the fifteen
comparator items replication-grade and none of the fifteen kernel
items. A split that clean across three independent scorers is
unlikely to be about the content alone.

The plausible mechanism is that a packet phrased in the standard
vocabulary of a domain reads as a restatement of that domain's
textbook results, while the same substance phrased in unfamiliar
vocabulary reads as new. If that is what happened, then
replication-grade is measuring which arm wrote the packet, which is
precisely the confound the blinding was meant to remove, and the
same mechanism could inflate the domain-native condition in the
opposite direction.

The repair belongs to G2 because the rubric is a sealed field. A
scorer marking an item replication-grade must name the established
result it restates, and an unnamed mark does not count. That
converts a judgment into a checkable claim. G2 should apply the
same requirement to any condition that a scorer can satisfy on
impression.

### Finding 7, recorded for calibration, not a defect

On a domain this campaign knows intimately, and where the kernel
should therefore look best, the primary endpoint separated the arms
by two items, fourteen against twelve. Effect sizes in the real
experiment may be small. This is a reason to be glad the primary
endpoint is a sign test across domains, which asks only which arm
is ahead in each domain and not by how much, and a reason not to
expect a decisive margin from any single domain.

All rehearsal scores are discarded and count for nothing.

---

## Closure of the operator defects

Findings 1, 5 and 6 were operator defects and could not be fixed in
G1, which is sealed and is never edited. They are closed by
`GENERATOR-G2.md`, sealed 2026-08-07, which supersedes G1 as the
governing specification and names each repair against the finding
it closes.

Finding 1 is closed by making the verbatim arm and scorer texts
sealed fields of G2. Finding 5 is closed without recalibrating the
ladder, by requiring a scorer who assigns level two or above to
name what stops the item being level one, and by a calibration
probe on the excluded domain that a scorer must pass before
scoring anything real. Finding 6 is closed by requiring a scorer
marking an item replication-grade to name the established result it
restates, with the same naming requirement placed on the
domain-native validity condition, which is the other condition a
scorer can satisfy on impression.

The naming requirement on the domain-native condition makes the
primary endpoint harder for the arm writing in unfamiliar
vocabulary, which is the arm under test. That the repair runs
against the hypothesis is stated in G2 section 4.2 rather than
noticed afterwards.

Findings 2, 3, 4 and 7 needed no operator change. Finding 2 is a
limitation carried into G2 section 4.3 and into the paper.
