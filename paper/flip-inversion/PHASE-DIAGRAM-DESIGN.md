# PHASE-DIAGRAM-DESIGN — continuous sign maps for the policy-reversal paper

**STATUS: DESIGN NOTE, 2026-08-27. No grid has been run.** The only executions behind
this note are two single-cell timing probes (one per substrate, reported below).
Family construction, shakedown, prereg, cooled seal, and graded sweeps all remain to
be done, in that order, per house discipline. Companion to OUTLINE.md (the
anti-construction plan) and formal-core.tex (the gate that defines the per-cell
field).

## Purpose

The flip cells declare two consumer classes and show opposite verdicts. The
anti-construction answer is to erase the labels: map the SIGN of the policy delta as
a continuous field over the footprint plane, so the two classes appear as measured
regions of one field, not as constructed fleets. The gate turns the map into a
three-valued field: licensed-negative, licensed-positive, abstain.

## QOT grid (reach x spectral position)

- **Axes.** Reach: all 30 unique CORONET-CONUS span counts, ns in {2..31} (the
  substrate's own set; no interpolation to fake reaches). Spectral position:
  p in {0, 0.05, ..., 1.0}, 21 points. Grid = 30 x 21 = 630 cells.
- **Per-cell population.** K_cell = 40 replicate services at the cell footprint,
  distinct monitoring-noise draws (0.3 dB), N_rep = 20 noise redraws averaged, per
  seed.
- **Policies at a cell.** m_A(cell) = rn(ns)·c_A, m_B(cell) = (ct(p)+0.05)·c_B with
  rn, ct exactly as in fam_qotflip. The normalizers c_A, c_B are FROZEN fleet
  constants (declared at family construction, computed once from the sealed fleet
  construction averaged over the disclosed calibration seeds), because per-cell
  renormalization would silently equalize the policies inside every cell and erase
  the field.
- **Per-cell quantity.** Primary map: sign(ΔR(cell)) with ΔR = FC_A − FC_B at the
  cell. Secondary map (the gate field): the stencil {0, 1/4, 1/2, 3/4, 1} per cell,
  gate per formal-core Eq. 10 with the F-QOT-GRAD floor estimator, three-valued
  outcome licensed−/licensed+/abstain. The secondary map costs 5x the primary.
- **Runtime estimate from the probe.** Probe (2026-08-27, qot venv, local CPU):
  one comb pair (CH_REF + CH_FULL) at one reach = 0.016 s; one cell A/B evaluation
  (K = 40) < 1 ms. Extrapolation: combs 30 reaches x 0.016 s ≈ 0.5 s once per
  process; primary map 630 cells x 3 seeds x 20 redraws x 2 policies x ~0.25 ms
  ≈ 20 s; gate field ~5x ≈ 100 s. **The full QOT phase diagram is under two
  minutes end to end.** Resolution is not runtime-limited; it is limited by the
  1/40 per-cell risk quantization, which sets the practical floor on visible
  boundary sharpness.

## CSI grid (Doppler x mean SNR)

- **Axes.** Doppler: fd in {10, 20, 40, 70, 100, 140, 200, 280, 400} Hz (9 points,
  log-spaced, spanning the sealed S and M fleets and the sweep2 range). Mean SNR:
  {4, 6, 8, 10, 12, 14, 16} dB (7 points, bracketing the sealed 7 and 12 dB
  operating points). Grid = 63 cells.
- **Per-cell population.** N_u = 4 independent TDL-A traces (distinct sub-seeds)
  at the cell's (fd, snr), 6000 TTI each, NACK averaged, per seed.
- **Policies at a cell.** m_A(cell) = fd·c_A, m_B(cell) = (max(0, 12−snr)+0.05)·c_B
  with the deficit form exactly as in fam_csiflip; c_A, c_B frozen at the sealed
  fleet's normalizers (same freezing argument as QOT).
- **Per-cell quantity.** Primary: sign(ΔR(cell)), ΔR = NACK_A − NACK_B. Secondary:
  the same three-valued gate field from the stencil (5x cost).
- **Runtime estimate from the probe.** Probe (2026-08-27, Atlas CPU, sionna-venv,
  TF intra-op 16 threads, cached LDPC curves): one trace at (100 Hz, 9 dB) =
  0.14 s; two _nack evaluations on it = 0.10 s; one trace-cell ≈ 0.24 s.
  Extrapolation: primary map 63 cells x 3 seeds x 4 traces x 0.24 s ≈ 3 min;
  gate field ~5x on the _nack part ≈ 12-15 min. **The full CSI phase diagram is
  ~15 minutes on Atlas CPU.**

## Proposed bar structure (to be fixed in the future prereg, not binding here)

- **B1 — both signs present, in declared fractions.** Per seed, among LICENSED
  cells: at least a declared fraction (proposal: 20%) licensed-negative and at
  least the same fraction licensed-positive. The reversal is then a property of
  the plane, not of two chosen points.
- **B2 — the sealed fleets sit on opposite sides.** Per seed: the cells containing
  the sealed class footprints (QOT: long-reach band-edge vs short-reach
  band-centre; CSI: (200 Hz, 12 dB) vs (10 Hz, 7 dB)) are licensed with opposite
  signs, matching the sealed flip directions.
- **B3 — boundary position predicted before grading.** On declared 1-D slices
  (QOT: the p = 0.5 column and the ns = 16 row; CSI: the snr = 9-10 dB column and
  the fd = 100 Hz row), the sign-change location is estimated on calibration seeds
  and registered with a band (same spread-based construction as the GRAD cells);
  the graded boundary must fall in the band on every seed. This is the
  phase-diagram analog of the lambda* registration.
- **MCs.** Frozen normalizers equal the sealed fleet's (declared constants);
  interior nondegeneracy (risks strictly inside (0,1) on a declared interior
  subgrid; edge cells may saturate and are reported, not graded); the abstain
  fraction reported per seed (an all-abstain map is a VOID, not a FAIL).

## What stays exploration vs what seals

- **Exploration (never graded, disclosed as pilots):** grid ranges and resolution,
  colormap rendering, the choice of declared slices for B3, the licensed-fraction
  threshold, per-cell population sizes. All of these get fixed by one disclosed
  pilot sweep on calibration seeds ONLY.
- **Seals:** the B1/B2/B3 bars on graded seeds {>= 2026-08-31, disjoint from all
  calibration and shakedown seeds}, with the frozen normalizers, the gate
  constants inherited verbatim from the sealed GRAD cells, and the registered
  boundary bands. Cooling-off applies from the day the phase-diagram family
  scripts are constructed; nothing in this note starts that clock, because no
  family code exists yet.

## Open design risks (stated, not fudged)

- The QOT per-cell risk is quantized at 1/(K_cell·N_rep); boundary cells will
  dither. If the graded boundary band has to exceed one grid step to absorb the
  dither, that widening must be set on calibration data and disclosed.
- The frozen-normalizer choice makes the per-cell margins extrapolations of the
  sealed policies outside the sealed fleet's footprint support (for example,
  16 dB SNR cells receive near-zero policy-B margin). That is the honest reading
  of "the same policy rule elsewhere in the plane"; the prereg must say the map
  characterizes THESE policy rules, not all pairs.
- CSI traces at 400 Hz Doppler and 4 dB SNR sit at the edge of the sweep2
  calibration experience; if the fresh-policy sanity check fails there, those
  cells are reported as out-of-scope, not silently dropped.
