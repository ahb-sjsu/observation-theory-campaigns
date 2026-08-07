#!/usr/bin/env python3
"""PF-7b classical probe, stage two (exploratory, unsealed).

Stage one selected the field 0.675507688522339 and reported that
the reversing fraction is 0.4975 at the middle delay and 0.475 at
delay 15.5 but exactly 1.0 at delay 4.0, so the declared delay
range was rejected by its own window rule. At delay 4.0 the two
pulse centres sit at plus and minus 2.0 while the pulse length is
3.0, so the pulses overlap and act as one stronger pulse. This
stage probes a declared candidate range whose shortest delay
separates the pulses, and PF-7b binds the range only if every
probed delay lies inside the window.

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
from pf7_quantum_ceiling import classical_reversing_fraction  # noqa: E402,E501
from projection_fold import canonical_sha256  # noqa: E402

E_SELECTED = 0.675507688522339
WINDOW = (0.15, 0.85)
CANDIDATE_DELAYS = [8.0, 11.0, 14.0, 17.0, 20.0]


def main() -> int:
    record: dict = {"schema": "pf7-classical-probe2-v1",
                    "label": "exploratory"}
    pf7.E_FIELD = E_SELECTED
    rows = {}
    for i, d in enumerate(CANDIDATE_DELAYS):
        f, _ = classical_reversing_fraction(d, 9_000_000 + i)
        rows[str(d)] = float(f)
        print(f"  delay={d} frac={f:.4f}", flush=True)
    in_window = all(WINDOW[0] <= v <= WINDOW[1]
                    for v in rows.values())
    record["measured"] = {
        "E_bound": E_SELECTED,
        "fraction_by_delay": rows,
        "in_window": bool(in_window),
        "half_delay_range": [0.5 * CANDIDATE_DELAYS[0],
                             0.5 * CANDIDATE_DELAYS[-1]],
        "half_delay_squared_range":
            [(0.5 * CANDIDATE_DELAYS[0]) ** 2,
             (0.5 * CANDIDATE_DELAYS[-1]) ** 2]}
    record["declared"] = {"window": list(WINDOW),
                          "candidate_delays": CANDIDATE_DELAYS,
                          "stage_one_field": E_SELECTED,
                          "rule": "PF-7b binds this delay range "
                                  "only if every probed delay lies "
                                  "inside the window"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "pf7-classical-probe2.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("in_window", in_window)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
