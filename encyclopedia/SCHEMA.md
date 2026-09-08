# Encyclopedia entry schema

An entry is one Markdown file in `encyclopedia/entries/`, named by its stable id, and it is
built from the records rather than written beside them. The claims ledger in
geometric-observation stays the authority for what a result is worth. A campaign track file
stays the authority for what was measured. An entry gathers what those records say about one
thing, keyed by their identifiers, so that a correction in a record propagates to the entry
on the next rebuild and never has to be chased by hand. The three entries in this directory
were filled by hand on 2026-09-03 to fix the schema. The generator that fills them from the
records comes second, and the hand-filled entries are its acceptance test.

## Fields

Every entry carries these headings in this order. A heading with nothing to say is kept with
the word "none", so that a missing field and an empty field cannot be confused.

| Field | What it holds | Source of truth |
|---|---|---|
| `id` | the file name without extension, lowercase, hyphenated, never reused | this directory |
| `kind` | one of `concept`, `instrument`, `result`, `correction` | this directory |
| `definition` | one or two sentences a reader can act on, with the symbols the equation uses | the volume or paper that first stated it |
| `equation` | the displayed form, with the book equation number where the book states it | the volume, the book |
| `ledger` | every claims-ledger row that bears on the entry, with its class in brackets, `[proved]` `[demonstrated]` `[replicated]` `[predicted]` `[exploratory]` `[refuted]` | `geometric-observation/claims/LEDGER.md` |
| `first stated` | where the idea first appears in the record, with a DOI or commit | papers, volumes |
| `measurements` | a table of the numbers, each with the file and line range and the commit it was read at | campaign tracks, experiment results |
| `failures and corrections` | every retraction, refuted bar, vacuous pass, and erratum that touches the entry, dated, at the same prominence as the measurements | ledger, `ERRATA.md` files |
| `invariance envelope` | every registered transformation test that names the entry, grouped as proved invariant, survived, boundary measured, failed with its witness and what absorbed it, and predicted; `none declared` otherwise | `claims/transformations/*.toml` in the campaigns repository, schema in `claims/transformations/SCHEMA.md` |
| `conditions` | the assumptions under which the theorem or law holds, stated so a reader can tell when it does not apply | the volume, the book's revision notes |
| `machine checked` | the Lean file and theorem names, or none | `observation-data-mining/lean/`, `ot-lean` |
| `used in` | papers by DOI, book chapters by number, instruments by repository | the book's sources tables and index |
| `related` | other entry ids | this directory |
| `status` | the date the entry was last rebuilt or checked, and the commits of the records it was read from | this directory |

## Rules

1. Every number in an entry names its file, line range, and commit, exactly as the book's
   sources tables do. A number without a row is removed.
2. Failures sit in the entry at the size of the results they bound. An entry that lists a
   result and omits its refuted bar is wrong.
3. An entry states a theorem with its conditions. A law stated without the conditions under
   which it fails is an error of the same kind as a wrong number.
4. Prose in an entry follows the program's standing writing rule. No em dashes, colons, or
   semicolons in sentences, and no sentence that argues for the work's merit.
5. The entry does not restate a proof. It points to where the proof lives and, where one
   exists, to the Lean file that checks it.
6. When a record and an entry disagree, the record wins and the entry is rebuilt. An entry
   is never edited to contradict its records.

## What the generator will do

Walk `geometric-observation/claims/LEDGER.md` for rows, the campaign track files under
`experiments/` for cells and numbers, `ERRATA.md` files for corrections, and the book's
`chapters/*.md` sources tables and `tools/index_terms.py` for uses. Emit one entry per id
listed in `encyclopedia/entries.yaml`, which maps an id to the ledger rows, track cells, and
book sections it draws on. Fail the build if a cited path does not exist at the named commit,
as the book's checker does. Until the generator exists, entries are maintained by hand under
the same rules, and their `status` line says so.

## Relationships

A record joins an entry by a typed edge, and only the first four kinds appear in the body of the
entry. The rest are collapsed into the entry's "see also" heading.

| Edge | What it means | How the generator decides |
|---|---|---|
| defines | a book equation that states the entry | the paragraph around the display names the entry's terms |
| proves | a ledger row of class proved that names the entry | the row's claim text matches `book_terms` or the title |
| measures | a ledger row of class demonstrated, replicated, predicted, or exploratory that names the entry, or a sources-table row whose claim names it | the same match |
| refutes or corrects | a ledger row of class refuted, missed, or void that names the entry, or an erratum | the same match |
| uses | a book equation stated beside the entry's terms that does not define it | cited but not matched |
| mentions | a ledger row or sources-table row that cites the entry's records without naming it | cited but not matched |

An entry of kind `result` or `correction`, or one that sets `strict = false`, trusts every
record it cites, because its records were chosen for it. A ledger row appears once in full, in
the ledger; the entry carries the row's first sentence, its class, and a link to the line. The
ledger classes are `[proved]`, `[demonstrated]`, `[replicated]`, `[predicted]`, `[exploratory]`,
`[refuted]`, `[missed]`, and `[void]`, and, since 2026-09-08, two record classes that carry no
evidence grade of their own: `[witness]`, a row whose content is a reduced counterexample, the
smallest admissible transformation or the named cause that breaks a claim, and the component
that absorbed it; and `[revised]`, a row recording a commitment changed in response to a
named witness, with what changed and where the new commitment is sealed. Both render under
failures and corrections. `standards/DPE-RECORDS.md` in the campaigns repository states the
protocol steps they enforce.

Two optional fields sit beside `definition`: `definition` in `entries.toml` overrides the
glossary when an entry has no glossary headword, and `known_as` names the prior art the entry
sits beside or extends. Source citations are written with one separator, `repo/path:lines`,
and link to the file at the commit it was read at.

## Examples and the TSK map

`examples.toml` holds one worked example per entry, a line a student can check by hand, in
the manner of the book's chapter 0. The generator prints it under the definition and fails
the build when an entry has no example or an example names no entry. `tsk_map.toml` is the
curated table from a term of Tan, Steinbach, Karpatne, and Kumar, *Introduction to Data
Mining*, second edition, to the entries to read and the chapter of *Data Mining as
Observation* that takes the term up. The README, the PDF, and the site print it.
