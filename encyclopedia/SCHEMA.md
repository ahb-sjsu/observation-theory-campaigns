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
