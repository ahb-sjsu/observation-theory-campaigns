# Exploration (kept negative): sensor calibration drift — the clean template does NOT hold

**Status: EXPLORATION, NOT a sealed cell.** 2026-08-24. Chip 🕒🌫️. Recorded as an
honest negative (the program keeps FAILs), with the redesign that would make it a
clean cell. `fam_sensor.py`, real UCI Air Quality co-location data (De Vito et al.;
`data/` gitignored, auto-fetched).

## What was tested

The physical-sensing twin of XPROTO-QUANTUM: a low-cost metal-oxide gas sensor is
calibrated once against a co-located reference analyser (the certificate: "reading
accurate to ±tol"); over ~1 year it drifts; the frozen calibration should
false-clear (drifted reading trusted); periodic recalibration (the witness = the
reference) should hold it. Consumers = pollutants (CO, C6H6, NOx, NO2).

## What actually happened (real data, honest)

The **drift is real and large**: a frozen linear calibration's error **doubles**
over the year (`drift_ratio ≈ 2.05`), and it is out of tolerance 25–47% of the
time; false-clears are strongly consumer-relative (per-pollutant spread ~0.27 —
different sensors drift very differently). **But periodic *linear* recalibration
only recovers ~1.6×**, never reaching the clean bar (at no tolerance does
`naive_fc ≥ 0.25` hold while `refreshed_fc ≤ 0.10` with 2× dominance):

| TOL (×train σ) | naive_fc | refreshed_fc |
|---|---|---|
| 0.75 | 0.357 | 0.235 |
| 1.0 | 0.255 | 0.162 |
| 1.5 | 0.159 | 0.087 |
| 2.0 | 0.114 | 0.050 |

The residual is **model-limited** (metal-oxide nonlinearity + humidity
cross-sensitivity), not purely staleness — so "the witness fully holds the
certificate" is **not supported** on this substrate with a linear calibration.
This is a genuine finding, kept on the record rather than tuned into a pass.

## The redesign that would make it a clean cell (not yet built)

Two options, either of which restores the clean grammar:
1. **Witness-triggered recalibration (the ZK `read_fresh` framing).** Don't
   recalibrate on a fixed schedule — recalibrate *when the witness shows the error
   crossing tolerance*. Then false-clear → ~0 **by construction**, and the cell's
   result is the **refresh cost** (how often the reference is needed) vs the naive
   false-clear rate — an interpolation curve, exactly like ZK-FIX. This is the
   correct OT witnessed policy and is expected to dominate cleanly.
2. **A calibration model whose fresh residual is below tolerance** (nonlinear /
   humidity-aware), so the tolerance separates drift from model error.

Recommended: option 1 (it is the honest witnessed policy and reuses the freshread
lesson). Until then this stays an exploration, not a claim.
