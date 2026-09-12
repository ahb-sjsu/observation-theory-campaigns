# footprint

**id.** footprint
**kind.** concept

![The set of entries a reader reads.](../figures/footprint.svg)

## definition

The set of entries a reader reads. What the reader reads decides how warm and how stale the reader is. Chapter 13 section 13.3.

**Example.** A reader that touches 3 of a cache's 10 entries has a footprint of 3, and only those 3 decide its hit rate.

## equation

none

## conditions

- The set of entries a reader reads. The hit rate is one when the cache holds the footprint and does not move when entries outside it are added, so what the reader reads decides how warm, and how stale, the reader is.
- A replica is stale because of what the reader asks for. The hot reader read a false-clear rate of 0.99 and the cold reader 0.01 on the same store, and the aggregate described neither.

Conditions are curated in `entries.toml` rather than read from a record.

## ledger

none

## first stated

Chapter 13 section 13.3 of *Data Mining as Observation*, with the reader's footprint in `geometric-observation/chapters/ch19_the_certificate_that_ages.md:1-95`.

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

[`lean/DataMiningAsObservation/Cache.lean`](https://github.com/ahb-sjsu/observation-data-mining/blob/f3914f0/lean/DataMiningAsObservation/Cache.lean), theorems `hitRate_mem_unit`, `hitRate_cold`, `hitRate_warm`, `hitRate_mono`, `hitRate_footprint`, at observation-data-mining f3914f0; what the check covers is stated in the book's [appendix C](https://github.com/ahb-sjsu/observation-data-mining/blob/f3914f0/chapters/machine_checked.md).

## used in

*Data Mining as Observation* chapters 0, 2, 11, 12, 13, 14.

## related

cache, cold-warm, replica, false-clear-rate, read-subspace

## see also

Book equations stated beside the entry's terms, not defining it: 0.26, 13.2, 13.1.

Ledger rows that cite the entry's records without naming it: OT-11, GO-12.

Sources-table rows that share a record with the entry without naming it: chapter 13 section 13.2, chapter 13 section 13.3.

## status

Generated 2026-09-12 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
