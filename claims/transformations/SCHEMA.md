# Transformation registries

One file per track or campaign, `claims/transformations/<TRACK>.toml`. A registry is the
machine-readable form of the admissible transformations a track declares, so that every
invariance claim names the family it was tested against, the encyclopedia can print each
entry's invariance envelope, and a failed test carries its reduced witness and the revision
it forced. Registries are records: a transformation is entered when it is declared, before a
seal, and a test is entered when its verdict is committed, citing the record it comes from.
Nothing in a registry is evidence by itself; every line points at the file that is.

## The tuple a registry fixes

| Field | Meaning |
|---|---|
| `x` | the representation space the transformations act on |
| `y` | the output space, what a judgment or prediction returns |
| `equivalence` | the output equivalence and its tolerance, what "unchanged" means for `y` |
| `complexity_ordering` | the declared ordering over transformations that a witness must be minimal under |

## `[[transformation]]`

| Field | Meaning |
|---|---|
| `id` | `TRACK:slug`, unique across the program |
| `family` | the transformations in one sentence |
| `parameters` | the parameter set or ladder, or `none` |
| `closure` | what the family is closed under (composition, inversion, or `none`) |
| `rank` | position in the complexity ordering, 1 the simplest |
| `declared` | the date the family was declared, which must precede the seal that tested it |
| `declared_in` | where the declaration is, when it is not this file: the sealed registration's path, blob hash and seal commit. Required on a backfilled row |
| `entered` | the date this row was written, when that is later than `declared`. Its presence marks the row as a backfill |

A row carrying `entered` is a **backfill**. It says that the family was declared
on `declared`, in the file `declared_in` names, and that this registry was late to
carry it. The distinction matters because the declaration date is what D1 of
PE-DSC-1.0 tests and the entry date is what a reader would otherwise assume it was.
A backfill is honest only when the declaration it points at is intact and precedes
the run, which means the seal commit is a git ancestor of the commit adding that
gate's results and the sealed blob still hashes to the recorded value. A row whose
declaration cannot be shown to precede its result is not a backfill, it is a family
chosen to fit a result, and it must not be entered.

## `[[test]]`

| Field | Meaning |
|---|---|
| `transformation` | the `id` tested |
| `claim` | the invariance claim in one sentence, the thing that survives or fails |
| `entries` | encyclopedia entry ids the test bears on, may be empty |
| `outcome` | one of `survived`, `failed`, `boundary`, `predicted`, `proved` |
| `record` | `repo/path:first-last` of the verdict, at the commit the registry names |
| `boundary` | for `boundary`: the parameter value at which the claim stops holding, and the tolerance |
| `witness` | for `failed` and `boundary`: the reduced counterexample, the smallest transformation or the named cause that breaks the claim |
| `absorbed_by` | for `failed` and `boundary`: which component absorbed the change, one of `representation`, `metric`, `constraint`, `budget`, `dynamics`, `equivalence`, `declaration`, `measurement` |
| `revision` | the record of the revised commitment that followed, or `none` |

`survived` means the claim held across the whole family within the equivalence tolerance.
`failed` means it did not, with the witness saying where. `boundary` means the family has a
parameter and the claim holds up to a measured value. `predicted` means the test is sealed
and unrun. `proved` means the invariance is a theorem for the declared family and the record
is the proof.

## What the encyclopedia does with a registry

`encyclopedia/generate.py` reads every registry and gives each entry an **invariance
envelope** section listing, for the tests whose `entries` name it, the transformations
survived, the boundaries measured, the transformations failed with their witnesses and what
absorbed them, and the transformations only predicted. An entry with no test names it prints
`none declared`. The section is built from the registry, never written by hand.

## Ledger classes that registries cite

Two classes, defined in `encyclopedia/SCHEMA.md` beside the six evidence classes:
`[witness]` for a row whose content is a reduced counterexample and the component it names,
and `[revised]` for a row recording a commitment revised in response to a named witness.
A registry's `witness` and `revision` fields cite such rows where they exist, and the
verdict rows they were reduced from otherwise.
