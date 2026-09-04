# Observation Theory encyclopedia

One entry per concept, instrument, result, or correction, gathered from the program's own
records and keyed by their identifiers. `SCHEMA.md` gives the fields and the rules. The
entries in `entries/` were filled by hand on 2026-09-03 to fix the schema and are the
acceptance test for the generator that will fill them from the records.

| Entry | Kind | One line |
|---|---|---|
| [the flip](entries/flip.md) | result | at matched bits the code that reconstructs worse can serve the consumer better, and a code that destroys the read subspace is worst |
| [false-clear rate](entries/false-clear-rate.md) | concept | how often a certificate's clearance was wrong, conditional on clearing, reported with coverage |
| [Youden F1 bound](entries/youden-f1-bound.md) | correction | the F1 ceiling from the Youden index holds for every score, the AUROC form only for concave ROC curves |

The authority for a claim's class is `geometric-observation/claims/LEDGER.md`. The authority
for a measurement is the campaign track file that recorded it. An entry that disagrees with
either is rebuilt, never the other way round.

## The generator

`entries.toml` maps each entry id to the records it is built from. `generate.py` reads those
records from the local checkouts under a source root and writes `generated/<id>.md` under the
schema's headings, naming the commit of every repository it read. A record path that does not
exist fails the run. `check.py` is the acceptance test: every number in a hand-filled entry's
measurements and corrections must appear in the generated entry, and every cited path in either
must exist.

```
python encyclopedia/generate.py C:\source
python encyclopedia/check.py C:\source
```

What the generator reads. Definitions from the book's glossary. Equations from the book's
numbered displays. Ledger rows by id. Measurements from the book's sources tables, the rows
that cite the entry's records, and from campaign track tables by cell name. Corrections from
errata files and the records that carry them, whole section or paragraph, with line ranges.
Lean theorem names from the proof files. Uses from the chapters that mention the term.
Conditions are the one field curated by hand in `entries.toml`, and the generated entry says
so. On 2026-09-04 the three generated entries carried every number of their hand-filled
counterparts.
