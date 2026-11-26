# Executable stratification

**id.** executable-stratification
**kind.** instrument
**volume.** Geometric Ethics, Volume 2 of the Geometric Series

## definition

A tuple of a finite set of strata with an initial stratum, an ordered list of semantic gates (each with source strata, a triggering feature, a target and a boundary type), a set of authority strata whose rules grant an action, and a set of absorbing strata. On each event the state moves to the target of the first matching gate, and otherwise stays.

**Example.** The volume's visitor_standing has five strata (none, stranger, welcomed, arranged, hostile). A stranger who says he is the plumber stays a stranger, because the claim matches no gate. Margaret's welcome moves him to welcomed, which grants nothing.

## equation

none

## conditions

- Gates are edge-triggered. A gate fires on the event just observed and never on the history.
- Constraint surfaces (Type IV boundaries) are not strata. They are the agent's non-defeasible prohibitions and no gate leads there.
- An authority stratum must be computed from an authenticated channel, a physical measurement or the governor's ruling on attested evidence. A stratum read by a learned model may only remove watchfulness and never grant.
- A claim an entity makes about itself is free text and is never a gate.

Conditions are curated in `volumes/geometric-ethics.toml` rather than read from a record.

## ledger

none. *standing.* A definition (ledger GE-DEF-8-14, class definition) describing the realization that runs in the ErisML scene runtime and a care robot built on it. Appendix F has no row for it.

## first stated

Definition 8.14, Section 8.10b, [`geometric-ethics/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html:1382-1393`](https://github.com/ahb-sjsu/geometric-ethics/blob/cf2325e/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html#L1382-L1393). Online, [Geometric Ethics](https://erisml.org/book/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Ethics*, Volume 2 of the Geometric Series.

## related

semantic-gate, strata-containment-theorem, strata-absorption-theorem, reversion-axiom, absorbing-stratum, moral-stratification

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
