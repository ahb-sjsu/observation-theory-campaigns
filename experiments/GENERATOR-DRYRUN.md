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

quant-ph, which is on the exclusion list of
GENERATOR-DOMAIN-POOL-V2.md and can therefore never be drawn.
Nothing learned here can contaminate the experiment, and no test
domain is consumed.

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
