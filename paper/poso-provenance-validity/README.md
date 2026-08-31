# Provenance Is Not Validity — critique paper

An Observation-Theory critique of SkyMapper L1 / Proof of Space Observation (POSO):
cryptographic anchoring certifies **provenance**, not scientific **validity**, and the
"provably reliable / reproducible" framing conflates the two.

- **Status:** skeleton stood up 2026-08-31. Argument filled; empirical numbers filled from the
  cadence run; citations and one figure are TODO.
- **Companion artifact:** "Provenance Is Not Validity" —
  https://claude.ai/code/artifact/fa668661-c868-4020-844a-3137a3aea026
- **Grounding:** IEEE P3787 (validity attestation), the replication-vacuity result, and the
  measured cadence false-clear (0.9995) on real Breakthrough Listen L-band data.

## Build

```
pdflatex poso
bibtex poso
pdflatex poso
pdflatex poso
```

MiKTeX on this box:
`C:\Users\abptl\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe`.
Word copy for reviewers who want it:
`pandoc poso.tex -o poso.docx` (embed a 300-dpi PNG figure for pandoc).

Check the log for `undefined` references and `Citation ... undefined` before circulating.

## Files

- `poso.tex` — main skeleton (IEEEtran conference; swap the class for the chosen venue).
- `refs.bib` — bibliography. Every entry is either `% VERIFY` (confirm before submit) or an
  explicit `TODO` stub with `author={TODO}`. **Do not ship a fabricated reference.**

## Finalization checklist

- [ ] **Venue + class.** IEEEtran is a placeholder. Pick the target (systems / metascience /
      astro-methods) and swap the class; re-check the page limit.
- [ ] **POSO specifics.** The CoinDesk page is behind a JS bot-wall; fetch failed. Paste the
      primary description and quote the "reliable / reproducible" claims verbatim in
      Sec. II, and confirm the pure-provenance reading (Sec. III/VIII hedge covers the
      alternative).
- [ ] **Citations.** Fill and verify every `refs.bib` entry against a real record
      (authors, venue, year, pages). Confirm RFC 3161, Merkle, Lebofsky 2019, turboSETI.
      Find real blockchain-for-science + provenance-vs-quality references.
- [ ] **P3787 clause.** Cite the exact validity-attestation-class clause.
- [ ] **Figure.** Build Fig. `cadence` (ON/OFF waterfall + the surviving candidate) from
      `cadence_result.json` on the compute host (`/archive/seti`); add a parameters table
      (target designation, MJD 57574, project AGBT16A_999_233, coarse channels 119–144).
- [ ] **Numbers.** Re-verify 6651 / 3 / 0.9995 against `cadence_result.json` (primary record),
      not this README.
- [ ] **Author block.** Add affiliation detail + contact email.
- [ ] **Prose pass.** No em-dashes: `grep -- "---" poso.tex` should hit nothing outside bib
      titles. Kill label-speak; short declarative sentences.
- [ ] **Owner submits.** Build submit-ready PDF + DOCX; do not submit or post automatically.
