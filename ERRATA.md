# Errata

Errors found after publication, recorded here whether or not the
published record is corrected. Each entry names what is wrong, where
it appears, when it was found, and what was done.

---

## E1. Wrong Land reference in two published papers

**Found** 2026-08-07, during the proofread of the PF arc paper, by
checking the campaign's own citations against Crossref.

**What is wrong.** The campaign cited Land's Stueckelberg-Horwitz-
Piron pair-production work as J. Phys. Conf. Ser. **845**, 012025
(2017), DOI 10.1088/1742-6596/845/1/012025. Crossref resolves that
DOI to *Mass stability in classical Stueckelberg-Horwitz-Piron
electrodynamics*, which is a different paper by the same author.

The pair-production paper is J. Phys. Conf. Ser. **615**, 012007
(2015), DOI 10.1088/1742-6596/615/1/012007, title *Pair production
in classical Stueckelberg-Horwitz-Piron electrodynamics*.

The artifact PF-3 actually transcribed is the preprint
arXiv:1604.01625, whose title the arXiv metadata confirms is the
pair-production paper. **The replication itself is unaffected.**
What PF-3 reproduced, and what papers 3 and 5 report about it, was
transcribed from the correct source. Only the journal reference
printed beside it was wrong.

**Where it appears.**

- Published, DOI 10.5281/zenodo.21790096, the Cayley-pole paper.
- Published, DOI 10.5281/zenodo.21798545, the sealed Schwinger
  negative.
- `paper/references.bib`, `experiments/PF3-PROVENANCE.md`, and the
  two paper sources named above.

**What was done.** The bibliography, the provenance document, and
the paper sources are corrected, so any future build is right. The
PF arc paper, drafted after the error was found, cites the
preprint with the published version named correctly.

**What was done on Zenodo, 2026-08-09.** The Cayley-pole paper was
reissued as version 2, DOI 10.5281/zenodo.21837523 under the
unchanged concept DOI 10.5281/zenodo.21790095. The corrected Land
reference appears in the version 2 record, both in the deposited PDF
and in the record description, and the description's change list
names the superseded reference explicitly so a reader of version 1
can see what moved. Version 1 remains published and unaltered, as
Zenodo versions are immutable.

**What is still not done.** The sealed Schwinger negative, DOI
10.5281/zenodo.21798545, still carries the wrong journal reference
in its published record. Its source is corrected in this repository,
so any future build is right, but no corrected version has been
issued. For that paper this entry remains the correction of record.

---

## E2. Wrong Stueckelberg title in one published paper

**Found** 2026-08-07, same pass.

**What is wrong.** The bibliography entry printed the title of
Stueckelberg's proper-time note, Helv. Phys. Acta 14, 322 (1941),
at the page of the pair-creation note, Helv. Phys. Acta 14, 588
(1941). Both citation contexts in the campaign want the
pair-creation note, so the page is right and the title was wrong.

**Where it appears.** `paper/cayley-pole-pair-threshold.tex`,
published as DOI 10.5281/zenodo.21790096, which is version 1.

**Status.** The corrected entry ships in version 2, DOI
10.5281/zenodo.21837523, issued 2026-08-09. Version 1 is immutable
and still carries the wrong title.

**Confidence.** Lower than E1. Helvetica Physica Acta is not
indexed in the services used to verify E1, so this rests on the
proofreading pass rather than on a resolver. The correction makes
the entry consistent with the page cited and with the use made of
it, and if the volume itself is ever checked directly this entry
should be revisited.

**What was done.** Corrected in the PF arc paper. The Cayley-pole
source is corrected. The published record is unchanged, as above.

---

## E3. Two wrong bar values in the campaign notes

**Found** 2026-08-07, same pass. Not a published error.

`experiments/CAMPAIGN.md` twice described the PF4-006 entry-point
and timestep clause as having a bar of 1e-10. The sealed
declaration and the committed record both set that bar at 1e-8. The
1e-10 figure is the separate translation-covariance bar. The
narrative was wrong and the verdict was not, since the clause
failed at 1.3e-2 against either number.

The same document described PREREG-PF4-009 as passing all six
bars. The sealed document groups its requirements into six bars and
the governed runner reports eight items, and the mapping between
them was never declared. Both statements are now made explicitly.

Corrected in place, since these are working notes rather than
sealed documents or published records.

---

## Standing note on records and runners

Two failures this session shared one shape. A record was committed
from a runner later found defective, and the correction was left
uncommitted where nothing reading the repository could see it. The
rule adopted in response is that a rerun writes to a new path and
never over a committed record, and that the superseded record stays
in the repository naming what replaced it. See the PF4-007
subsection of `experiments/CAMPAIGN.md`.
