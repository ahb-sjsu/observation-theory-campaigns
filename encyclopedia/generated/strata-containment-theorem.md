# Containment theorem for executable strata

**id.** strata-containment-theorem
**kind.** result
**volume.** Geometric Ethics, Volume 2 of the Geometric Series

## definition

If every gate whose target is an authority stratum is triggered only by system events, then no sequence of events containing no system event, whatever a learned model classified, moves the stratification into an authority stratum it did not start in.

**Example.** Start at stranger and feed the events he says he is the plumber, then Margaret welcomes him. Neither is a system event, so the state ends at welcomed and is never arranged, the authority stratum, which only the monitoring centre's authenticated announcement can enter.

## equation

none

## conditions

- The hypothesis is about the gate list. Every gate into an authority stratum must have a system-event trigger. The ErisML runtime checks this when a scene loads and refuses to run one that violates it.
- The theorem is about the stratum state machine. It does not say that system events are authentic, which rests on the channels and measurements that produce them.
- It does not prevent entry into non-authority strata. A welcomed visitor reaches the welcomed stratum, which grants nothing.

Conditions are curated in `volumes/geometric-ethics.toml` rather than read from a record.

## ledger

none. *standing.* Proved by induction on the event sequence and machine-checked in Lean 4 in the book's formal/lean project, on the standard axioms only. Ledger row GE-THM-8-6 has class proved, and Appendix F lists the theorem as Proved (Lean) as of v1.29. The care robot's own proof is a weaker form.

## first stated

Theorem 8.6, Section 8.10b, [`geometric-ethics/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html:1418-1422`](https://github.com/ahb-sjsu/geometric-ethics/blob/401b9a5/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html#L1418-L1422), with its status at [`geometric-ethics/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html:1427-1434`](https://github.com/ahb-sjsu/geometric-ethics/blob/401b9a5/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html#L1427-L1434). Online, [Geometric Ethics](https://erisml.org/book/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html).

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

executable-stratification, strata-absorption-theorem, reversion-axiom, no-escape-theorem, semantic-gate

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
