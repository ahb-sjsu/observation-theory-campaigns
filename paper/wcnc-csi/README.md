# IEEE WCNC 2027 paper — the consumer-relative CSI certificate

**Deadline: 15 September 2026** (accept 15 Jan 2027; camera-ready 8 Feb 2027).
Venue: IEEE WCNC 2027, Panama City. Sole author: A. H. Bond. EDAS: `N34673`.

**Submit to → Track 1: Physical Layer and Communication Theory** (all four tracks close
Sep 15). Best fit: the paper is core link-level PHY/comm-theory (LDPC BLER, MCS/SNR
selection, CSI feedback, Clarke coherence). Matching Track-1 topics — pick as EDAS
keywords: *Feedback and Two-Way Communication* (the CSI certificate), *Low-Latency and
Short Packet Communications* (URLLC axis, §III), *Channel Modeling and Estimation* (CSI
aging / refresh floor, §IV). Fallback: Track 3 (Resource Allocation & ML) is defensible
via the margin-allocation angle, but the ML half no longer applies (AICSI-v2 refuted, §III-C
dropped) and the paper is a measurement/PHY contribution, not an allocation optimizer.
Not Track 2 (MAC/networking) or Track 4 (emerging tech: RIS/ISAC/NTN).

**Thesis:** a CSI report is a certificate whose *false-clear rate* is consumer-relative
along two measured axes — the reliability target (URLLC vs eMBB) and the refresh horizon
(OT-14). Both results are **sealed + graded on real 5G NR link-level (Sionna LDPC)**.

## Files
| File | What |
|---|---|
| `wcnc-csi.tex` | IEEEtran conference manuscript (canonical source) |
| `wcnc-csi.pdf` | Built PDF (pdflatex/MiKTeX, 3 pp) |
| `wcnc-csi.docx` | Word rendering (pandoc; all three figures embedded) |
| `OUTLINE.md` | Structure + the §III-C refutation record |
| `build/plot_urllc.py` → `urllc_relativity.{pdf,png}` | Fig. 1, from sealed `XPROTO-URLLC-graded.json` |
| `build/plot_snr.py` → `snr_robustness.{pdf,png}` | Fig. 2, from sealed `analysis/urllc/URLLCSNRREP-graded-raw.json` |
| `../../analysis/csi/plot_age.py` → `build/age_horizon.{pdf,png}` | Fig. 3, from the sealed XPROTO-CSI-SWEEP2 record (`analysis/csi/CSISWEEP2REP-*.json`) |
| `build/plot_refresh.py` → `refresh_floor.{pdf,png}` | **RETIRED, not included by the manuscript.** Built from the unsealed 0.15-threshold exploration `CSI-refreshfloor.json`; superseded by XPROTO-CSI-SWEEP2. Files kept as record. |

## Numbers (all sealed-graded, real Sionna)
- **§III (URLLC), 3 seeds:** eMBB achieved BLER 0.112 (at $10^{-1}$ target); URLLC-naive
  0.112 = **112× over** the $10^{-3}$ target; URLLC-aware 1.2e-5 (meets it) at ~2 dB margin.
  (`analysis/urllc/`, sealed 2026-08-24, commit 6375ebd.)
- **§IV (age horizon), 3 seeds:** at $f_D$=200 Hz / 20-TTI period, naive BLER 0.36 vs
  OLLA 0.10. (`analysis/csi/`, XPROTO-CSI sealed 2026-08-23, commit ng:fda9148.)
- **§IV (age horizon), 3 graded seeds at the calibrated 0.10 budget:** the horizon
  collapses. Largest compliant report period $P^\star$ = 4/6/4 TTI at 10 Hz, 2/2/3 TTI at
  25 Hz, and 1 TTI (the frame minimum) at 50/100/200/400 Hz on every seed, with no
  censoring. Origin-fit slopes 0.1008 / 0.1398 / 0.1086 at $R^2$ 0.7376 / 0.9218 / 0.6174.
  There is no room for a proportionality law. Periodic reporting alone cannot protect a
  tight budget at practical mobility, so the HARQ-witnessed correction (OLLA) is mandatory
  rather than optional. (XPROTO-CSI-SWEEP2, sealed 2026-08-27, graded PASS on seeds
  20260827/28/29.)

**Superseded, never sealed.** An earlier exploration claimed a refresh floor
≈ 0.177·$T_{coh}$ at $R^2$=0.915. It measured its floors at a relaxed 0.15 threshold while
the paper claimed the 0.10 target, and its fresh baseline (BLER ≈ 0.113) never met the
budget at all. It carried no SEALS row and no prereg. Refuted and replaced by
XPROTO-CSI-SWEEP2; `csi_sweep.py` and `CSI-refreshfloor.json` are kept as record.

## Build
    python build/plot_urllc.py    # -> build/urllc_relativity.{pdf,png}
    python build/plot_snr.py      # -> build/snr_robustness.{pdf,png}
    # Fig. 3 is built from analysis/csi (see the usage line in plot_age.py):
    #   python plot_age.py <CSISWEEP2REP record> ../../paper/wcnc-csi/build/age_horizon
    # build/plot_refresh.py is RETIRED. It plots the unsealed 0.15-threshold
    # exploration and its output is no longer included by the manuscript.
    pdflatex wcnc-csi && pdflatex wcnc-csi                 # PDF (MiKTeX; IEEEtran)
    pandoc wcnc-csi.tex -o wcnc-csi.docx --resource-path=".;build"   # DOCX

## Finalization checklist (before submit)
- [ ] **Submit to EDAS Track 1** (Phys. Layer & Comm. Theory); primary keywords
      *Feedback and Two-Way Communication* + *Low-Latency and Short Packet Communications*.
- [ ] Confirm WCNC 2027 IEEEtran/PDF-eXpress formatting + exact page limit (usually 6);
      current build is 3 dense IEEE pages (§II system model + link-param table + per-seed
      results table all added — can expand further if a fuller paper is wanted).
- [x] **§II expanded** — formal system model (eqs. 1–3), link-param Table I, per-seed
      results Table II. (commits bf83f42, d194058.)
- [x] **References verified** — Durisi/Wen/Sionna correct as written; OLLA fixed to
      P. Sarath Kumar, VTC'97 vol. 2. (commit 7d9f457.)
- [ ] Author block / affiliation / email confirmed; IEEE copyright line as required.
- [ ] Optional: OTA / srsRAN external-validity note; §III-C stays dropped (AICSI-v2 refuted).

## Positioning (honest)
The contribution is a **measurement + framing** (false-clear rate as a consumer-relative
KPI; the two relativities; the age horizon at the true budget), not a new
estimator/scheduler. OLLA and
coherence-driven reporting are the credited deployed corrections. Sionna link-level is
the evidence rung; an OTA/srsRAN HARQ trace is the external-validity graduation. The
learned-CSI-feedback axis was tested (AICSI-v2, CsiNet-on-CDL) and **did not survive** —
dropped, not hidden (see `OUTLINE.md`).
