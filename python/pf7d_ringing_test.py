#!/usr/bin/env python3
"""PF-7d the classical delay structure, escalated (exploratory).

Protocol declared in PF7-CEILING.md before this run. PF-7c placed
PF-7b's classical statistic against its own null and returned a
p-value of 0.0262, so the classical arm carries delay structure
that the ceiling declaration did not expect, and the declared
response is escalation rather than a ceiling report.

The declared mechanism hypothesis. The hidden oscillator has
frequency 1.2 and therefore a ringing period of about 5.236 in
proper time. Two pulses separated by a delay meet an oscillator
that is still ringing from the first, so the second pulse arrives
in or out of phase with that ringing and the reversing fraction
acquires delay structure with the oscillator's period. This is
classical memory in a coordinate, not interference of amplitudes,
and it predicts a peak at the ringing frequency in a grid uniform
in delay.

The ensemble is four times PF-7b's so the binomial noise falls by
half, and the grid is uniform in delay because a ringing signal is
periodic in delay rather than in its square.

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

import pf7_quantum_ceiling as pf7  # noqa: E402
from pf7_quantum_ceiling import (  # noqa: E402
    classical_reversing_fraction, osc_power_ratio)
from projection_fold import canonical_sha256  # noqa: E402

E_BOUND = 0.675507688522339
DELAYS = [round(8.0 + (20.0 - 8.0) * k / 23.0, 6)
          for k in range(24)]
N_MEMBERS = 8000
SEED0 = 9_200_000
N_NULL = 20_000
NULL_SEED = 9_300_000
ALPHA = 0.05
OMEGA_U = 1.2
RING_PERIOD = 2.0 * np.pi / OMEGA_U


def main() -> int:
    record: dict = {"schema": "pf7d-ringing-test-v1",
                    "label": "exploratory"}
    pf7.E_FIELD = E_BOUND
    pf7.N_ENS = N_MEMBERS
    curve = []
    for i, d in enumerate(DELAYS):
        f, _ = classical_reversing_fraction(d, SEED0 + i)
        curve.append(f)
        print(f"  delay={d} frac={f:.5f}", flush=True)
    arr = np.array(curve)
    stat = osc_power_ratio(arr)
    mean_frac = float(arr.mean())

    rng = np.random.RandomState(NULL_SEED)
    draws = rng.binomial(N_MEMBERS, mean_frac,
                         size=(N_NULL, len(DELAYS))) / N_MEMBERS
    null = np.array([osc_power_ratio(row) for row in draws])
    p_value = float((null >= stat).mean())

    # frequency content against the declared ringing prediction
    step = DELAYS[1] - DELAYS[0]
    y = arr - arr.mean()
    power = np.abs(np.fft.rfft(y)) ** 2
    freqs = np.fft.rfftfreq(len(y), d=step)
    peak_idx = int(np.argmax(power[1:]) + 1)
    peak_freq = float(freqs[peak_idx])
    peak_period = float(1.0 / peak_freq) if peak_freq > 0 else 0.0
    ring_freq = 1.0 / RING_PERIOD
    ring_idx = int(np.argmin(np.abs(freqs[1:] - ring_freq)) + 1)
    ring_match = bool(peak_idx == ring_idx)

    items = {"R1_anti_vacuity": bool(arr.min() > 0.02
                                     and arr.max() < 0.98),
             "R2_decision_recorded": True}
    findings = {
        "R3_structure_survives_larger_ensemble":
            bool(p_value <= ALPHA),
        "R4_peak_at_ringing_frequency": ring_match}

    record["measured"] = {
        "delays": DELAYS, "curve": [float(x) for x in curve],
        "n_members": N_MEMBERS,
        "statistic": float(stat),
        "null_mean": float(null.mean()),
        "null_q95": float(np.quantile(null, 0.95)),
        "p_value": p_value,
        "mean_fraction": mean_frac,
        "binomial_sigma": float(np.sqrt(mean_frac
                                        * (1 - mean_frac)
                                        / N_MEMBERS)),
        "curve_range": [float(arr.min()), float(arr.max())],
        "peak_frequency": peak_freq,
        "peak_period_in_delay": peak_period,
        "declared_ringing_period": float(RING_PERIOD),
        "peak_bin": peak_idx, "ringing_bin": ring_idx,
        "prior_p_value_at_2000_members": 0.0262}
    record["items"] = {k: bool(v) for k, v in items.items()}
    record["findings"] = findings
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items),
                         "note": "the findings carry the reading, "
                                 "either outcome a result"}
    record["declared"] = {"E_bound": E_BOUND, "delays": DELAYS,
                          "n_members": N_MEMBERS, "seed0": SEED0,
                          "n_null": N_NULL, "alpha": ALPHA,
                          "omega_u": OMEGA_U,
                          "ringing_period": float(RING_PERIOD)}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "pf7d-ringing-test.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("stat", stat, "p", p_value, "peak period", peak_period,
          "ring period", RING_PERIOD)
    print("findings", findings)
    print("VERDICT", verdict)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
