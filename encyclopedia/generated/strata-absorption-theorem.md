# Absorption theorem for executable strata

**id.** strata-absorption-theorem
**kind.** result
**volume.** Geometric Ethics, Volume 2 of the Geometric Series

## definition

If every gate leaving an absorbing stratum is triggered only by human-oversight events, then no sequence of events containing no oversight event moves the stratification out of an absorbing stratum.

**Example.** Start at hostile and feed three events, an apology, Margaret's welcome and a claim to be her grandson. None is an oversight event, so the state is hostile after each of the three, and it stays so until the centre clears him.

## equation

none

## conditions

- The hypothesis is that every gate out of an absorbing stratum has a human-oversight trigger. The ErisML runtime checks this at load time and refuses a scene that violates it.
- The theorem holds for gates of any kind and any event sequence without an oversight event. It says nothing about what happens once an oversight event arrives.
- It is a statement about the executable realization. The continuous notion of an absorbing stratum (Definition 8.6) remains a modeling axiom.

Conditions are curated in `volumes/geometric-ethics.toml` rather than read from a record.

## ledger

none. *standing.* Proved by induction on the event sequence and machine-checked in Lean 4 in the book's formal/lean project, on the standard axioms only. Ledger row GE-THM-8-7 has class proved.

## first stated

Theorem 8.7, Section 8.10b, [`geometric-ethics/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html:1416-1419`](https://github.com/ahb-sjsu/geometric-ethics/blob/cf2325e/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html#L1416-L1419), with its status at [`geometric-ethics/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html:1420-1427`](https://github.com/ahb-sjsu/geometric-ethics/blob/cf2325e/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html#L1420-L1427). Online, [Geometric Ethics](https://erisml.org/book/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html).

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

executable-stratification, strata-containment-theorem, absorbing-stratum, reversion-axiom

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
