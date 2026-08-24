# OFC 2027 paper — XPROTO-QOT (consumer-relative QoT false-clear)

**Status:** 3-page draft in the Optica meeting template. Target: OFC 2027,
networks/systems track. Deadline **2026-10-20**; student/early-career prize eligible.
Evidence cell: `../../analysis/qot/` (GNPy). Sole author: A. H. Bond.

**Structure (revised):** *leads with the ML-QoT result* (the genuine novelty).
§3.1 ML-QoT objective misalignment → **Fig. 1 = `ml_cliff.pdf`** (measured);
§3.2 consumer-relative margin + honest capacity (~5–6% over a uniform margin, not the
strawman 50%) → **Fig. 2 = `fc_footprint.pdf`**; §3.3 refresh floor (measured).

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
- [ ] **Seal + grade XPROTO-QOT** (fresh day ≥ 2026-08-25) → `XPROTO-QOT-graded.json`;
      then **swap every `% GRADED-SWAP` number** in `ofc-qot.tex` (naive_fc, aware_fc,
      loading penalty, per-footprint spread) from shakedown to the graded values.
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
