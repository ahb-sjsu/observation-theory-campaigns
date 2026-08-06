#!/usr/bin/env python3
"""PF5-002 placement probe (exploratory, unsealed).

PREREG-PF5-001 passed every declared bar on a product grid that
produced zero reversal events, so its accounting claim about pair
events was untested. The named error, a product grid was declared
where PF4-002 placed cells by bisection. This probe bisects the
field at each declared gap to land the reversing fraction in the
declared window, so PF5-002 can bind cells that actually contain
the events the gate is meant to audit.

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

from pf5_accounting import census_run  # noqa: E402
from projection_fold import canonical_sha256  # noqa: E402

P_GRID = [0.60, 0.70, 0.80, 0.90]
TARGET = 0.10
WINDOW = (0.02, 0.30)
N_PROBE = 2000
E_LO, E_HI = 0.45, 6.0
ITERS = 12


def frac_rev(p, e, seed):
    res = census_run(p, e, N_PROBE, seed)
    c = res["counts"]
    return c["reversing"] / N_PROBE, c


def main() -> int:
    record: dict = {"schema": "pf5-placement-probe-v1",
                    "label": "exploratory"}
    rows = []
    for ip, p in enumerate(P_GRID):
        lo, hi = E_LO, E_HI
        f_hi, c_hi = frac_rev(p, hi, 8_200_000 + ip)
        best = None
        for it in range(ITERS):
            mid = 0.5 * (lo + hi)
            f, c = frac_rev(p, mid, 8_200_000 + 100 * ip + it)
            if best is None or abs(f - TARGET) < abs(best[1]
                                                    - TARGET):
                best = (mid, f, c)
            if f < TARGET:
                lo = mid
            else:
                hi = mid
        rows.append({"P": p, "E_probe_top": E_HI,
                     "frac_at_top": f_hi,
                     "E_selected": float(best[0]),
                     "frac_selected": float(best[1]),
                     "counts_selected": best[2],
                     "in_window": bool(WINDOW[0] <= best[1]
                                       <= WINDOW[1])})
        print(rows[-1], flush=True)
    record["rows"] = rows
    record["usable_cells"] = int(sum(r["in_window"] for r in rows))
    record["declared"] = {"P_grid": P_GRID, "target": TARGET,
                          "window": list(WINDOW),
                          "n_probe": N_PROBE,
                          "E_bracket": [E_LO, E_HI],
                          "iters": ITERS,
                          "rule": "PF5-002 binds only cells whose "
                                  "probe fraction lies in the "
                                  "window"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "pf5-placement-probe.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("usable", record["usable_cells"])
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
