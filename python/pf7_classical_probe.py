#!/usr/bin/env python3
"""PF-7b classical dynamic-range probe (exploratory, unsealed).

PF-7's classical arm saturated, every member of every delay cell
reversed, so its oscillation statistic was measured on a constant
curve and its finding was vacuous. The standing rule of this
campaign requires a committed probe verifying that a bound cell
contains the variation its claim is about. This probe bisects the
field at the declared gap under the two-pulse profile so that the
reversing fraction lands inside the declared window, and reports
the fraction at the extreme delays so the dynamic range is on
record before PF-7b binds anything.

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

from pf7_quantum_ceiling import classical_reversing_fraction  # noqa: E402,E501
import pf7_quantum_ceiling as pf7  # noqa: E402
from projection_fold import canonical_sha256  # noqa: E402

TARGET = 0.5
WINDOW = (0.15, 0.85)
E_LO, E_HI = 0.05, 1.2020141601562502
ITERS = 12
MID_DELAY = 10.0
EDGE_DELAYS = [4.0, 15.5]


def frac_at(e_field, delay, seed):
    pf7.E_FIELD = e_field
    return classical_reversing_fraction(delay, seed)[0]


def main() -> int:
    record: dict = {"schema": "pf7-classical-probe-v1",
                    "label": "exploratory"}
    lo, hi = E_LO, E_HI
    best = None
    trace = []
    for it in range(ITERS):
        mid = 0.5 * (lo + hi)
        f = frac_at(mid, MID_DELAY, 8_800_000 + it)
        trace.append({"E": float(mid), "frac": float(f)})
        print(f"  E={mid:.6f} frac={f:.4f}", flush=True)
        if best is None or abs(f - TARGET) < abs(best[1] - TARGET):
            best = (mid, f)
        if f < TARGET:
            lo = mid
        else:
            hi = mid
    e_sel = float(best[0])
    edges = {}
    for d in EDGE_DELAYS:
        edges[str(d)] = float(frac_at(e_sel, d, 8_900_000
                                      + int(d * 10)))
        print(f"  edge delay={d} frac={edges[str(d)]:.4f}",
              flush=True)
    in_window = (WINDOW[0] <= best[1] <= WINDOW[1]
                 and all(WINDOW[0] <= v <= WINDOW[1]
                         for v in edges.values()))
    record["measured"] = {
        "bisection_trace": trace,
        "E_selected": e_sel,
        "frac_at_mid_delay": float(best[1]),
        "frac_at_edge_delays": edges,
        "in_window": bool(in_window)}
    record["declared"] = {"target": TARGET, "window": list(WINDOW),
                          "mid_delay": MID_DELAY,
                          "edge_delays": EDGE_DELAYS,
                          "E_bracket": [E_LO, E_HI],
                          "iters": ITERS,
                          "rule": "PF-7b binds the classical field "
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
        / "pf7-classical-probe.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("selected", e_sel, "in_window", in_window)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
