# OFC 2027 paper — XPROTO-QOT (consumer-relative QoT false-clear)

**Status:** 3-page draft in the Optica meeting template. Target: OFC 2027,
networks/systems track. Deadline **2026-10-20**; student/early-career prize eligible.
Evidence cell: `../../analysis/qot/` (GNPy). Sole author: A. H. Bond.

**Structure (revised):** *leads with the ML-QoT result* (the genuine novelty).
§3.1 ML-QoT objective misalignment → **Fig. 1 = `ml_cliff.pdf`** (measured);
§3.2 consumer-relative margin + honest capacity (**~8%** over a uniform margin, not the
strawman 50%) → **Fig. 2 = `fc_footprint.pdf`**; §3.3 refresh floor (measured).

**§3.2 capacity is grounded on real traffic + deterministic (FINAL, not GRADED-SWAP):**
`sndlib_fill.py` derives the deployed per-link channel-fill distribution from the real
**SNDlib janos-us-ca** demand matrix (median 10, 90th-pct 35 of 76 ch → heavy-tailed →
`SNDlib-fill.json`); `qot_capacity.py` interpolates each lightpath's deployed GSNR to
its real fill and gives BOTH policies a 0.5 dB estimator RMSE (aware is not assumed
perfect). Result: **+8.0% SE (0.33 b/sym, ~21 Gb/s/ch)** at matched safety (FC≤0.01),
uniform M=2.75 dB vs aware M=1.25 dB. The raw SNDlib `.txt` is git-ignored (`data/`);
fetch via the SNDlib native bundle (`sndlib-networks-native.zip`).

## Submission hard limits (OFC site + style guide)
- **≤ 3 pages**, **PDF ≤ 2 MB**, abstract **≤ 35 words**, ≤ 3 figures.
- The uploaded PDF **must** carry title, abstract, and **all author names +
  affiliations**, and these must **match** what is entered in the submission form.
- **No author-supplied copyright statement** (Optica adds it). Follow the Style
  Guide exactly or the paper is auto-rejected.

## Build
1. Copy `opticameet3.sty` and `opticajnl.bst` from the Overleaf "Template for
   manuscript for submission to an Optica meeting or conference" into this directory
   (they are not redistributed here).
2. `pdflatex ofc-qot && bibtex ofc-qot && pdflatex ofc-qot && pdflatex ofc-qot`
   (MiKTeX; same toolchain as the IEEE drafts).
3. Confirm **≤ 3 pages**, abstract **≤ 35 words**, PDF **≤ 2 MB**.

## Finalization checklist (before submit)
- [x] **§3.2 capacity grounded on real SNDlib janos-us-ca fill** (`sndlib_fill.py` +
      `qot_capacity.py`, deterministic): +8.0% SE at matched safety, both policies
      carry 0.5 dB estimator RMSE. FINAL number, wired into §3.2. (No longer synthetic.)
- [x] **SEALED + GRADED PASS 2026-08-25** (sealing commit `8bb6e5b`, seeds
      20260825-27). **XPROTO-QOT**: naive_fc 0.37-0.55, aware_fc 0.0, all bars+MCs
      (`XPROTO-QOT-graded.json`). **XPROTO-QOT-ML**: MAE mse 0.65 < aware 0.95, FC mse
      ~0.041 vs aware ~0.008 (**~5×**, graded — the shakedown's ~8× did not replicate),
      bps comparable (`XPROTO-QOT-ML-graded.json`). Both figures regenerated from graded
      seed 20260825; §3.1 abstract+text reconciled to ~5× / FC 0.041 vs 0.008. **No
      `% GRADED-SWAP` items remain** — every number in the paper is now sealed-graded or
      deterministic.
- [ ] **Generate Fig. 1** (`fc_footprint.pdf`): (a) naive vs footprint-aware
      false-clear; (b) per-footprint false-clear vs (spectral position, reach).
      *Requires a small enhancement to `fam_qot.py` to emit per-lightpath records
      (position, reach, naive/aware fail) — currently it emits only aggregates.*
      Use line style + marker shape, not colour alone (Optica accessibility rule).
- [ ] Fill the real references (GNPy paper; a representative ML-QoT / margin-reduction
      citation, e.g. Pointon/Seve/Ayassi; the OT program).
- [ ] Author block / email confirmed; no author-supplied copyright statement.
- [x] **Result 2 BUILT + measured** (`analysis/qot/fam_qotml.py`, F-QOTML shakedown
      PASS): average-error ML-QoT wins reconstruction (MAE 0.64 vs 0.94) yet
      false-clears ~5x at the FEC cliff (0.05 vs 0.01) at equal capacity. Seal
      alongside XPROTO-QOT (PREREG-XPROTO-QOT-ML.md; run in the qot venv, numpy<2).
- [x] **Fig. 1 pipeline ready** (`analysis/qot/fam_qot.py --paths-out` +
      `plot_fig1.py` → `fc_footprint.pdf`, marker-shape classes). Draft committed
      (shakedown); regenerate from the graded per-lightpath emit post-seal:
      `fam_qot.py --seeds 20260825 20260826 20260827 --paths-out QOT-paths.json`
      then `plot_fig1.py QOT-paths.json ../../paper/ofc-qot/fc_footprint.pdf`.
      Run in the qot venv (numpy<2).
- [x] **Fig. 2 pipeline ready** (`fam_qotml.py --preds-out` + `plot_fig2.py` →
      `ml_cliff.pdf`: (a) MAE-vs-false-clear dissociation, (b) false-clear vs GSNR
      headroom = the FEC cliff; marker-shape classes). Draft committed (shakedown);
      regenerate from graded seeds post-seal, in the qot venv.
- [x] **Sec. 3.2 fill-sweep DONE** (`qot_sweep.py` → `QOT-sweep.json`): FC rises
      linearly with added channels (FC ≈ 0.008·ΔN, R²=0.95); refresh floor ≈ 8 added
      channels at FC≤0.05. Deterministic (no seed) → numbers final, wired into §3.2.
      Optional Fig. 3 via `plot_fig3.py` (`refresh_floor.pdf`) — add only if the
      3-page budget allows a 3rd figure. (Per-reach floor came out degenerate — not
      claimed.)
- [ ] **Use case framing** (done in the .tex): brownfield incremental fill --
      keep it concrete on final pass (name a representative link length / service rate).

## Positioning (honest)
The contribution is a **measurement + framing** (false-clear rate as a first-class,
consumer-relative KPI; QoT margin as a footprint property), not a new optimizer;
margin reduction / ML-QoT is an active area and is credited. GNPy's GN model is the
evidence rung; a fibre-testbed pre-FEC-BER witness is the external-validity
graduation and is stated as future work.
