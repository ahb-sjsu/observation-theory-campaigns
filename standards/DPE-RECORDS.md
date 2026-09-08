# Discovery records: the four record types and the protocol steps they enforce

The program's evidence discipline (sealed instruments, preregistered claims, verdicts
committed as executed, negatives kept) runs the loop that *Discovery Philosophy Engineering*
(Bond, draft September 2026) names: formalize, derive, search, probe, witness, revise. Four of
the loop's objects were until 2026-09-08 present in the records only as prose. This document
makes them record types, so that the accounting sees them.

## 1. Transformation registry

`claims/transformations/<TRACK>.toml`, schema in `claims/transformations/SCHEMA.md`. A track
declares its admissible transformations there before the seal that tests them: the
representation space, the output space, the output equivalence with its tolerance, the
families with their parameters and closure, and the complexity ordering under which a witness
must be minimal. The registry answers the objection that the transformation class is chosen by
the theorist: it is, and the choice is a versioned, sealed file.

Protocol step. No registration that claims an invariance is sealed without the family it
claims it for entered in the registry.

## 2. Invariance envelope

For each encyclopedia entry, the transformations the claim survived, the boundaries measured,
the transformations it failed with their witnesses, and the transformations only predicted,
rendered by `encyclopedia/generate.py` from the registries. The envelope is the comparative
object: an entry whose envelope strictly contains another's, at comparable adequacy and
without compensating structure, is the more invariantly fundamental of the two, and the
generator prints what each envelope contains so that comparison is a reading of two lists.

Protocol step. A registry test names the entries it bears on; an invariance claim in a paper
cites the envelope, not a sentence.

## 3. Witness

A failed or bounded test is reduced before it is recorded: the smallest transformation under
the declared ordering, or the named cause, that breaks the claim, and the component that
absorbs it, one of representation, metric, constraint, budget, dynamics, equivalence,
declaration, measurement. The ledger class `[witness]` carries a row whose content is such a
reduction. A registry test of outcome `failed` or `boundary` carries the witness in its own
fields and cites the row.

Protocol step. A verdict of FAIL or INDETERMINATE is not complete until its witness is
recorded or the record says that reduction was attempted and what stopped it.

## 4. Revised commitment

The ledger class `[revised]` carries a row recording a commitment changed in response to a
named witness: what changed, the witness it answers, and where the new commitment is sealed.
The registry test's `revision` field cites it. Without this class the loop's last arrow is
invisible to the accounting, and a program can revise its commitments without the record
showing that it did.

Protocol step. A registration that supersedes another because of a witness records a
`[revised]` row before it is sealed.

## What already exists and what these add

The tracks already ask invariance questions (WM, RG, GG, HD, QD), already keep every failure
with its cause named (the status ledger's `[refuted]` rows), already run a sealed generator
that searches domains for research packets (GENERATOR-G1, G2), and already print every
entry's failures and corrections from the ledger and the errata. The four record types add
the machine-readable declaration, the per-entry envelope, the reduced witness as a row, and
the revision as a row. The first registries are `GG.toml`, filled from the gauge track's own
record, and `GET.toml`, filled from the Geometric Evaluation Theory campaign, whose second
shared-code registration is the first `[revised]` row and whose all-keys truncation result the
first `[witness]` row, in that repository's ledger.

## Correspondence with the paper

| Paper | Record |
|---|---|
| Definition 1, invariance claim | a registry `[[test]]` with its `claim` and `equivalence` |
| Definition 2, invariance envelope | the entry's envelope section |
| Definition 3, comparative fundamentality | two envelopes read side by side, with the complexity qualification stated in the registry's ordering |
| Definition 4, boundary witness | a `[witness]` row and the registry's `witness` field |
| Stage 6, reduce failures | the protocol step under Section 3 |
| Section 13.3, the class is chosen by the theorist | the registry file, versioned and sealed |
| Workstream A, calculus of invariants | the registry schema |
| Workstream B, representation attacks | registry families of rank 1 across tracks |
| Workstream D, automated theory search | GENERATOR-G1 and G2 |
| Workstream E, boundary atlases | the envelope sections across the encyclopedia |
