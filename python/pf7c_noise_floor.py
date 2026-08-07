#!/usr/bin/env python3
"""PF-7c the oscillation statistic's noise floor (exploratory).

Protocol declared in PF7-CEILING.md before this run. PF-7b's
classical arm measured an oscillation statistic of 0.3626 against a
declared bar of 0.15, and the bar was set without accounting for
the statistic's noise floor. A spectral concentration statistic on
a thirty-two point curve has a nonzero floor even for pure noise,
because the largest of sixteen nonzero-frequency powers is a
sizable fraction of their sum. This run decides whether the
measured statistic is a signal or that floor, by a declared null
test on the committed PF-7b curve.

The null. Each delay cell measured a reversing fraction from a
declared ensemble of 2000 independent members, so under the
hypothesis of no delay dependence the counts are binomial at the
curve's mean fraction. Twenty thousand declared null curves are
drawn, the statistic computed for each, and the measured statistic
placed in that distribution.

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

N_MEMBERS = 2000
N_NULL = 20_000
SEED = 9_100_000
ALPHA = 0.05


def main() -> int:
    record: dict = {"schema": "pf7c-noise-floor-v1",
                    "label": "exploratory"}
    src = Path(__file__).resolve().parents[1] / "results" \
        / "pf7b-quantum-ceiling.json"
    prior = json.loads(src.read_text(encoding="utf-8"))
    curve = np.array(prior["measured"]["classical_curve"],
                     dtype=float)
    q_ratio = float(prior["measured"]["quantum_osc_power_ratio"])
    measured = float(prior["measured"]
                     ["classical_osc_power_ratio"])
    n_points = len(curve)
    mean_frac = float(curve.mean())

    rng = np.random.RandomState(SEED)
    draws = rng.binomial(N_MEMBERS, mean_frac,
                         size=(N_NULL, n_points)) / N_MEMBERS
    null = np.array([osc_power_ratio(row) for row in draws])
    p_value = float((null >= measured).mean())
    q_p_value = float((null >= q_ratio).mean())

    items = {
        "N1_measured_recomputed":
            abs(osc_power_ratio(curve) - measured) <= 1e-12,
        "N2_null_floor_is_high": float(null.mean()) >= 0.15,
        "N3_decision_made": True}
    consistent_with_noise = p_value > ALPHA

    record["measured"] = {
        "n_points": int(n_points),
        "mean_fraction": mean_frac,
        "classical_statistic": measured,
        "quantum_statistic": q_ratio,
        "null_mean": float(null.mean()),
        "null_median": float(np.median(null)),
        "null_q95": float(np.quantile(null, 0.95)),
        "null_q99": float(np.quantile(null, 0.99)),
        "classical_p_value": p_value,
        "quantum_p_value": q_p_value,
        "classical_consistent_with_noise":
            bool(consistent_with_noise),
        "curve_range": [float(curve.min()), float(curve.max())],
        "binomial_sigma": float(np.sqrt(mean_frac
                                        * (1 - mean_frac)
                                        / N_MEMBERS))}
    record["findings"] = {
        "Q3c_classical_no_interference_beyond_noise":
            bool(consistent_with_noise),
        "Q3c_quantum_exceeds_null": bool(q_p_value < ALPHA)}
    record["items"] = {k: bool(v) for k, v in items.items()}
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items),
                         "note": "the findings carry the ceiling "
                                 "reading, either outcome a result"}
    record["declared"] = {"n_members": N_MEMBERS,
                          "n_null": N_NULL, "seed": SEED,
                          "alpha": ALPHA,
                          "source_record": "results/"
                                           "pf7b-quantum-ceiling"
                                           ".json"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "pf7c-noise-floor.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("measured", measured, "null mean", null.mean(),
          "q95", np.quantile(null, 0.95), "p", p_value)
    print("quantum", q_ratio, "p", q_p_value)
    print("findings", record["findings"])
    print("VERDICT", verdict)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
