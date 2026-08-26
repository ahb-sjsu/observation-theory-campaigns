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
| `wcnc-csi.docx` | Word rendering (pandoc; both figures embedded) |
| `OUTLINE.md` | Structure + the §III-C refutation record |
| `build/plot_urllc.py` → `urllc_relativity.{pdf,png}` | Fig. 1, from sealed `XPROTO-URLLC-graded.json` |
| `build/plot_refresh.py` → `refresh_floor.{pdf,png}` | Fig. 2, from sealed `CSI-refreshfloor.json` |

## Numbers (all sealed-graded, real Sionna)
- **§III (URLLC), 3 seeds:** eMBB achieved BLER 0.112 (at $10^{-1}$ target); URLLC-naive
  0.112 = **112× over** the $10^{-3}$ target; URLLC-aware 1.2e-5 (meets it) at ~2 dB margin.
  (`analysis/urllc/`, sealed 2026-08-24, commit 6375ebd.)
- **§IV (refresh), 3 seeds + sweep:** at $f_D$=200 Hz / 20-TTI period, naive BLER 0.36 vs
  OLLA 0.10; refresh floor **≈ 0.177·$T_{coh}$, $R^2$=0.915** (saturates at 1 TTI at high
  Doppler). (`analysis/csi/`, sealed 2026-08-23, commit ng:fda9148.)

## Build
    python build/plot_urllc.py    # -> build/urllc_relativity.{pdf,png}
    python build/plot_refresh.py  # -> build/refresh_floor.{pdf,png}   (qot venv)
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
KPI; the two relativities; the refresh law), not a new estimator/scheduler. OLLA and
coherence-driven reporting are the credited deployed corrections. Sionna link-level is
the evidence rung; an OTA/srsRAN HARQ trace is the external-validity graduation. The
learned-CSI-feedback axis was tested (AICSI-v2, CsiNet-on-CDL) and **did not survive** —
dropped, not hidden (see `OUTLINE.md`).
