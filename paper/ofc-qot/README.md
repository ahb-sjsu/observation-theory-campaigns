# OFC 2027 paper — XPROTO-QOT (consumer-relative QoT false-clear)

**Status:** 2-page skeleton in the Optica meeting template. Target: OFC 2027,
networks/systems track. Deadline **2026-10-20**; student/early-career prize eligible.
Evidence cell: `../../analysis/qot/` (GNPy).

## Build
1. Copy `opticameet3.sty` and `opticajnl.bst` from the Overleaf "Template for
   manuscript for submission to an Optica meeting or conference" into this directory
   (they are not redistributed here).
2. `pdflatex ofc-qot && bibtex ofc-qot && pdflatex ofc-qot && pdflatex ofc-qot`
   (MiKTeX; same toolchain as the IEEE drafts).
3. Confirm it fits **2 pages** and the abstract is **≤ 35 words**.

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
- [ ] Optional Result 2: build a small ML-QoT estimator on GNPy data and show the
      average-error-optimal estimator false-clears at the FEC cliff vs a
      consumer/threshold-aware objective (the AICSI corollary). Only if it fits 2 pp.

## Positioning (honest)
The contribution is a **measurement + framing** (false-clear rate as a first-class,
consumer-relative KPI; QoT margin as a footprint property), not a new optimizer;
margin reduction / ML-QoT is an active area and is credited. GNPy's GN model is the
evidence rung; a fibre-testbed pre-FEC-BER witness is the external-validity
graduation and is stated as future work.
