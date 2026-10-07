# IEEE WCNC 2027 paper — consumer-relative budgets across five NR certificates

**UPDATE 2026-10-06: final extension. WCNC email to the author: "Submit your paper
by 26 October 2026." Re-check the EDAS table for the exact time zone.**

**Deadlines (from the EDAS registration table, read 2026-09-22).** Register the
paper by **5 October 2026**, review manuscript due **6 October 2026**. Accept
15 Jan 2027, camera-ready 8 Feb 2027. The conference flyer's 15 September date
is superseded, and the site now marks the paper deadline **Deadline Extended**.
Venue: IEEE WCNC 2027, Panama City. Sole author: A. H. Bond. EDAS: `N34673`.

**Submit to → Track 1: Physical Layer and Communication Theory.** Core
link-level PHY and communication theory (LDPC BLER, MCS selection, CSI feedback,
beam and precoder aging, uplink timing). Matching Track-1 topics as EDAS
keywords: *Feedback and Two-Way Communication*, *Low-Latency and Short Packet
Communications*, *Channel Modeling and Estimation*. Note EDAS renames Track 3 to
**Resource Allocation and Machine Learning**, and the ML half of this paper was
dropped (AICSI-v2 refuted), so Track 3 is no longer the fallback it was.

## The 2-page cap was not the real page limit

**RESOLVED ON PAPER, STILL TO CONFIRM IN EDAS.** The 4-page upload was refused
in September with *"The review manuscript cannot be longer than 2 pages
(type)."* The published WCNC 2027 rule is different and explicit:

> The page length limit for all initial submissions for review is SIX (6)
> printed pages (10-point font). Initial submissions longer than SIX (6) pages
> will be rejected without review.

Camera-ready may reach 8 pages, the 7th and 8th at US$100 each.

**Likely cause, not yet verified.** In the EDAS registration list the tracks are
separate conference records, `WCNC 2027 Track 1` through `Track 4`, while the
workshops and tutorials sit under the parent `WCNC 2027`. A submission
registered against the parent record rather than against `WCNC 2027 Track 1`
would inherit a paper type with its own small cap. **Before submitting, open
`WCNC 2027 Track 1` in the EDAS list and read the page limit it offers.** If it
still says 2 pages, mail the Track 1 co-chairs or the TPC co-chairs (Jalel Ben
Othman, Ana García Armada).

`wcnc-csi-2pp.tex` is therefore **superseded** and kept only as a record of the
cut. Do not submit it unless EDAS proves the 2-page type is the only one open.

**Site caveat.** The WCNC 2027 `call-papers` and `submission-guidelines` pages
carry leaked **NetSoft 2027** boilerplate (NetSoft topic list, "Full or Short
papers, up to 9 and 6 pages", EDAS link `N35644`, and "IEEE NetSoft 2027
Conference Proceedings" in the registration paragraph). Ignore those page
limits. The 6+2 rule quoted above is genuine WCNC text.

## Files
| File | What |
|---|---|
| `wcnc-csi.tex` | IEEEtran conference manuscript (canonical source) |
| `wcnc-csi.pdf` | Built PDF, **5 pp**, no overfull boxes, no undefined refs |
| `wcnc-csi.docx` | Word rendering (pandoc, all four figures embedded) |
| `wcnc-csi-2pp.tex` / `.pdf` | **SUPERSEDED** two-page variant, 2026-09-10 |
| `OUTLINE.md` | Structure + the §III-C refutation record |
| `build/plot_urllc.py` → `urllc_relativity.{pdf,png}` | Fig. 1, from sealed `XPROTO-URLLC-graded.json` |
| `build/plot_snr.py` → `snr_robustness.{pdf,png}` | Fig. 2, from sealed `analysis/urllc/URLLCSNRREP-graded-raw.json` |
| `../../analysis/csi/plot_age.py` → `build/age_horizon.{pdf,png}` | Fig. 3, from sealed XPROTO-CSI-SWEEP2 |
| `build/plot_families.py` → `family_sweep.{pdf,png}` | **Fig. 4 (NEW 2026-09-22)**, from sealed `XPROTO-BEAM-graded.json` + `XPROTO-PHY-graded.json` |
| `build/plot_refresh.py` | **RETIRED.** Plots the unsealed 0.15-threshold exploration. Not included by the manuscript. |

## What changed on 2026-09-22 (4 pp → 5 pp)

**New §V, "Four More Certificates Fail the Same Way"** (Fig. 4, Table III), built
from two sealed PASS records that no earlier draft used.

| Certificate | Record | naive | witnessed | fresh |
|---|---|---|---|---|
| beam index, FR2 | XPROTO-BEAM, sealed 2026-08-23 | 0.310–0.329 | 0.098–0.104 (BFR) | 0.021–0.027 |
| precoder (PMI) | XPROTO-PHY, sealed 2026-08-24 | 0.299–0.311 | **0.124–0.130** | 0 |
| rank (RI) | XPROTO-PHY | 0.268–0.299 | 0.079–0.085 | 0 |
| timing advance (TA, uplink) | XPROTO-PHY | 0.419–0.425 | 0.055–0.056 | 0 |

Min–max over three graded seeds each, target 0.10. Three findings worth keeping:

1. **Precoder re-selection does not reach the target** (0.124–0.130, a quarter to
   a third above it) while the other three loops do. Two consecutive failures is
   a slow trigger against continuous angular drift. 549–558 re-reports in 6000
   slots. This is the paper's only case of a deployed correction, run as
   specified, failing to reach target. **Do not soften this.**
2. **TA is an uplink certificate**, so the paper now spans both links.
3. **Fresh is zero, not proven zero.** PMI, RI and TA record zero events in 6000
   slots, which bounds F below 5e-4 at 95% (rule of three). Stated that way in
   the text, the table footnote, and the figure.

**Substrate discrepancy found and resolved in the paper's favour of the code.**
`PREREG-XPROTO-PHY.md` §Scope says the sealed rung swaps "the abstract aging
processes for TR38.901 CDL (PMI/RI) and a real timing model (TA)". The code does
not. `fam_phy._decode_nrsionna` states *"Aging processes unchanged; only the
SINR->BLER decode moves to the measured curve"*, and the aging constants
(`OMEGA_PMI=1200` deg/s, `RANK_FLIP_HZ=270`, `TA_DRIFT_US_PER_S=20`, `CP_US=4.7`)
are module-level and shared by both modes. **The paper follows the code** and
says these four cells age parametrically and measure only the decode, in the
Method and again at the end of §V. The prereg's Scope paragraph overstates and
should be corrected in the campaign repo.

**Title changed** to remove the colon, per the standing prose rule. Was *"One
CSI-Derived Rate Cannot Serve Every Budget: Budget Overrun and the Age Horizon in
5G Link Adaptation"*. Now *"One Report Cannot Serve Every Budget / Overrun and
Age Horizons in Five 5G NR Adaptation Certificates"*. Revert if unwanted.

**Abstract and introduction rewritten** to carry the third finding, to drop all
inline math (abstract now has zero `$`), and to state the budgets in words ("one
block in ten", "one in a thousand") rather than as symbols.

**Prose pass over the whole manuscript.** The 4-pp draft carried 14 colons and
22 semicolons in prose plus two banned words ("reliability regime", "budget gap
lives"). All removed. The three remaining colons are set-builder notation inside
math (`\{m:\rho_m...\}`), which the rule exempts. Scanner kept at
`scratchpad/prose_scan.py`, and it also runs the two eaten-backslash guards.

**New references.** `beamtut` (Giordani et al., IEEE Commun. Surveys Tuts. 21(1)
173–196, 2019, verified) and `ts38213` (TS 38.213, beam failure recovery and
uplink timing, **clause numbers carry a `% verify` mark**).

**Tables narrowed.** All three tables were overflowing the column. Now
`\scriptsize` with `\tabcolsep=3pt`, and the hand-wrapped footnote rows replaced
by a single wrapping `p{0.97\linewidth}` cell. Build reports zero overfull boxes.

## Machine checks (2026-10-06, both run on Atlas)

**Provenance checker** (`checks/check_claims.py`). It ties 49 quantitative claims
(snippet must appear verbatim) to the sealed URLLC, SNR, CSI, CSI-SWEEP2, BEAM and PHY
records, the disclosed exploration record, the runner constants, and the Sionna curve
file on Atlas (`/home/claude/csi/nr_bler_curves_sionna.npz`). Last run: **PASS 49,
FAIL 0**.

Run:
`python check_claims.py --tex ../wcnc-csi.tex --analysis <campaigns>/analysis --curves <npz>`.

**Lean 4 / Mathlib v4.32.2** (`lean/WcncCsi/Certificate.lean`). It has 14 theorems, no
`sorry`, and only the standard axioms (`Axioms.lean`). It proves:
- the hundredfold overrun is automatic;
- with delta_dn = delta_up (1 - beta)/beta, OLLA's mean drift vanishes exactly at
  NACK rate beta and points toward it;
- zero events with n p = 3 exclude p at 95% (the 6000-slot and 400-block bounds);
- independent branches at 3% or less multiply to more than 30x below 1e-3;
- a larger backoff never picks a higher MCS, so the expected BLER cannot rise;
- the Doppler-to-speed conversions.

Build as in `ofc-qot`: symlink `.lake/packages` to `~/dmo-lean`, then `lake build`.

**Errors the checks found and fixed (2026-10-06):**
- Deep-fade fraction: the text said about 4%. The measured fraction on the TDL-A
  traces is 5.4-6.4%, and the Rayleigh analytic value is 6.1%, both at the lowest
  MCS's 1e-3 point. The 4% came from an unverified code comment in `fam_urllc.py`.
  The text now says about 6%, and defines the fade.
- Diversity margin: the text said "two orders". It is actually 53-59x, so the text
  now says "a factor of about fifty".
- Precoder overshoot: the text said "a quarter to a third". It is actually 24-30%.
- eMBB budget loss: the text said "below about 6 dB". It now says "at 6 dB and
  below", matching the figure shading (0.20 at 6 dB).
- Uncalibrated fresh BLER: 0.113 is now 0.11. The values are 0.105-0.116 across
  Dopplers.
- Abstract: removed "Every number comes from" (a banned phrase) and the
  revision-history clause.
- Section IV: split a sentence that had two consecutive "because" clauses.

## Numbers in §III and §IV (unchanged, all sealed-graded)
- **§III (URLLC), 3 seeds:** eMBB achieved BLER 0.112 (at 1e-1 target);
  URLLC-naive 0.112 = **112× over** the 1e-3 target; URLLC-aware 1.2e-5 at a
  4 dB backoff plus K=3 diversity. (`analysis/urllc/`, sealed 2026-08-24.)
- **§IV (age horizon), 3 graded seeds at the calibrated 0.10 budget:** largest
  compliant report period P* = 4/6/4 TTI at 10 Hz, 2/2/3 at 25 Hz, 1 TTI at
  50 Hz and above, no censoring. (XPROTO-CSI-SWEEP2, sealed 2026-08-27.)
- **Superseded, never sealed:** the 0.177·T_coh refresh-floor claim. Measured at
  a relaxed 0.15 threshold with a fresh baseline that never met the budget. Kept
  as record, disclosed in §II and §IV.

## Build
    python build/plot_urllc.py      # -> build/urllc_relativity.{pdf,png}
    python build/plot_snr.py        # -> build/snr_robustness.{pdf,png}
    python build/plot_families.py   # -> build/family_sweep.{pdf,png}
    # Fig. 3 from analysis/csi:
    #   python plot_age.py <CSISWEEP2REP record> ../../paper/wcnc-csi/build/age_horizon
    pdflatex wcnc-csi && pdflatex wcnc-csi
    pandoc wcnc-csi.tex -o wcnc-csi.docx --resource-path=".;build" --default-image-extension=png
    python <scratchpad>/prose_scan.py wcnc-csi.tex    # punctuation + corruption guards

## Finalization checklist (before submit)
- [ ] **Open `WCNC 2027 Track 1` in EDAS and confirm the page limit is 6.** This
      is the one blocker. See the section above.
- [ ] Manuscript by **26 Oct 2026** (final extension). EDAS author list and title
      must match the PDF exactly.
- [ ] Author block, affiliation, email, IEEE copyright line.
- [x] TS 38.213 clause titles checked 2026-10-06 against the v16.2.0 contents
      (4.2 Transmission timing adjustments, 6 Link recovery procedures); bib now cites v16.2.0.
- [ ] Read the abstract and §V aloud (articles and missing "the" are the most
      flagged grammar error).
- [x] Links now `hidelinks` (black) for the review PDF (2026-10-06).
- [x] **AI-use disclosure is REQUIRED by IEEE, not optional.** Acknowledgment
      confirmed by the author 2026-10-07, with the Lean proofs and the claim-checking
      script added.
- [x] EDAS-style PDF check (2026-10-07): 5 pp, US Letter, no page numbers, all fonts
      embedded. Figures now use TrueType (`pdf.fonttype: 42`); the matplotlib default
      Type 3 fonts would be flagged by IEEE PDF eXpress at camera-ready.
- [ ] Confirm in EDAS that the Track 1 upload offers the 6-page limit.
- [x] §V added from sealed BEAM + PHY records; Fig. 4 and Table III built.
- [x] Prose scan clean (0 semicolons, 0 em-dashes, 0 banned words, 0 colored
      text, corruption guards clean).
- [x] Build clean at **5 pp** (0 undefined refs, 0 overfull boxes).
- [x] §II expanded — system model (eqs. 1–3), link parameters, per-seed results.
- [x] References verified (Durisi/Wen/Sionna/Giordani; OLLA = Sampath, Sarath
      Kumar, Holtzman, VTC'97 vol. 2).

## Positioning (honest)
The contribution is a **measurement plus framing**, not a new estimator or
scheduler. OLLA, beam failure recovery, precoder re-selection, rank reduction
and the TA command loop are the credited deployed corrections, and the paper
reports how far each one gets. Sionna link level is the evidence, and an
over-the-air HARQ trace is the next step. Of the four new cells, only the decode
is measured. The learned-CSI-feedback axis was tested (AICSI-v2, CsiNet on
CDL-C) and **did not survive**, so it is dropped rather than hidden (see
`OUTLINE.md`).

## Not in this paper, reserved for the WCNC workshop track
`XPROTO-HO` (RSRP to serving cell, 0.31–0.44 naive against 0.09–0.12 witnessed)
and the O-RAN rApp and xApp mapping in `../../analysis/ran/DESIGN.md` are held
for a workshop submission, where registration closes **16 Oct 2026** and the
manuscript is not due until **30 Nov 2026**. Candidate workshops: WS12 Open RAN
(RIC control-loop stability, xApp and rApp conflict management, reproducible
testbeds) and WS09 AgenticRAN (safety guardrails, benchmarking, case studies in
scheduling and handover). Keeping HO out of this paper avoids any double
submission question.
