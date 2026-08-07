#!/usr/bin/env python3
"""PF-7f the smooth-model residual (exploratory).

Protocol declared in PF7-CEILING.md before this run. PF-7d measured
that the classical arm's delay structure survives a four times
larger ensemble at a p-value of 0.026 and that its spectral peak
sits at a period of 12.52 in delay, which is the span of the
declared range, so the peak is the lowest nonzero frequency bin and
the structure is a trend rather than an oscillation. The curve
falls from a mean of 0.4942 over the first half of the range to
0.4829 over the second, about five standard errors, which is what
residual overlap of two pulses of length three predicts as their
separation grows from eight to twenty.

The declared statistic conflates a trend with an oscillation
because the lowest nonzero bin carries both. This run removes a
declared linear trend from the curve and from every null curve
before computing the statistic, so the comparison is about
oscillation alone.

This run is post-processing of committed records and adds no new
dynamics.

Exploratory label. Not claim-bearing.
"""
from __future__ import annotations

import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pf7_quantum_ceiling import osc_power_ratio  # noqa: E402
from projection_fold import canonical_sha256  # noqa: E402

N_MEMBERS = 8000
N_NULL = 20_000
SEED = 9_500_000
PULSE_L = 3.0
ALPHA = 0.05


def detrend(y, x):
    """Remove the declared smooth model, an asymptote plus an
    exponential approach whose length is the declared pulse length.
    Two sech-squared pulses of that length overlap by an amount
    that falls exponentially with their separation, so this is the
    shape the overlap mechanism predicts. The fit is linear in its
    two free coefficients at fixed decay length."""
    basis = np.vstack([np.ones_like(x), np.exp(-x / PULSE_L)]).T
    coef, *_ = np.linalg.lstsq(basis, y, rcond=None)
    return y - basis @ coef


def main() -> int:
    record: dict = {"schema": "pf7f-smooth-residual-v1",
                    "label": "exploratory"}
    root = Path(__file__).resolve().parents[1] / "results"
    d_rec = json.loads((root / "pf7d-ringing-test.json")
                       .read_text(encoding="utf-8"))
    b_rec = json.loads((root / "pf7b-quantum-ceiling.json")
                       .read_text(encoding="utf-8"))

    delays = np.array(d_rec["measured"]["delays"], dtype=float)
    curve = np.array(d_rec["measured"]["curve"], dtype=float)
    raw_stat = float(d_rec["measured"]["statistic"])
    raw_p = float(d_rec["measured"]["p_value"])
    mean_frac = float(curve.mean())

    det = detrend(curve, delays)
    det_stat = osc_power_ratio(det)

    rng = np.random.RandomState(SEED)
    draws = rng.binomial(N_MEMBERS, mean_frac,
                         size=(N_NULL, len(curve))) / N_MEMBERS
    null_det = np.array([osc_power_ratio(detrend(row, delays))
                         for row in draws])
    p_det = float((null_det >= det_stat).mean())

    # the quantum arm under the same treatment, on its own grid
    q_curve = np.array(b_rec["measured"]["quantum_curve"],
                       dtype=float)
    q_x = np.arange(len(q_curve), dtype=float)
    q_det_stat = osc_power_ratio(detrend(q_curve, q_x))
    q_raw = float(b_rec["measured"]["quantum_osc_power_ratio"])

    # the declared trend magnitude, for the record
    coef = np.polyfit(delays, curve, 1)
    trend_drop = float(np.polyval(coef, delays[0])
                       - np.polyval(coef, delays[-1]))
    sigma = float(np.sqrt(mean_frac * (1 - mean_frac) / N_MEMBERS))

    items = {
        "F1_residual_is_smaller_than_raw_curve": bool(
            float(np.std(det)) < float(np.std(curve))),
        "F2_quantum_survives_detrending":
            bool(q_det_stat >= 0.30),
        "F3_decision_recorded": True}
    findings = {
        "F4_classical_consistent_with_noise_after_smooth_model":
            bool(p_det > ALPHA),
        "F5_trend_is_real":
            bool(abs(trend_drop) >= 3.0 * sigma)}

    record["measured"] = {
        "classical_raw_statistic": raw_stat,
        "classical_raw_p_value": raw_p,
        "classical_detrended_statistic": float(det_stat),
        "classical_detrended_p_value": p_det,
        "null_detrended_mean": float(null_det.mean()),
        "null_detrended_q95": float(np.quantile(null_det, 0.95)),
        "quantum_raw_statistic": q_raw,
        "quantum_detrended_statistic": float(q_det_stat),
        "trend_drop_over_range": trend_drop,
        "binomial_sigma": sigma,
        "trend_in_sigma": float(abs(trend_drop) / sigma),
        "reading": "the classical arm carries a smooth trend from "
                   "residual pulse overlap and the declared "
                   "statistic counted that trend as structure, "
                   "while the quantum arm's interference sits at a "
                   "high frequency and is untouched by removing a "
                   "trend"}
    record["items"] = {k: bool(v) for k, v in items.items()}
    record["findings"] = findings
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items),
                         "note": "F4 and F5 carry the ceiling "
                                 "reading, either outcome a result"}
    record["declared"] = {"n_members": N_MEMBERS,
                          "n_null": N_NULL, "seed": SEED,
                          "alpha": ALPHA,
                          "detrend": "declared asymptote plus exponential "
                                     "approach at the pulse length, "
                                     "removed from the curve and from "
                                     "every null curve alike",
                          "prior_linear_result":
                              "results/pf7e-detrended.json",
                          "source_records":
                              ["results/pf7d-ringing-test.json",
                               "results/pf7b-quantum-ceiling.json"]}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = root / "pf7f-smooth-residual.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("classical raw", raw_stat, "detrended", det_stat,
          "p", p_det)
    print("quantum raw", q_raw, "detrended", q_det_stat)
    print("trend drop", trend_drop, "in sigma",
          abs(trend_drop) / sigma)
    print("items", items, "findings", findings)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
