#!/usr/bin/env python3
"""PF6-002 member placement probe (exploratory, unsealed).

PREREG-PF6-001 returned vacuous, its anti-vacuity bar catching that
the deterministic member at each bound cell produces no folds. The
thermal ensemble reverses about ten percent of the time at these
cells, so the reversing members are the ones with transverse
momentum in the tail, and the deterministic member at pu0 = 0.1 is
not one of them. This probe scans the initial transverse momentum
at each bound cell and records, per cell, the smallest declared pu0
whose deterministic member folds within the declared step budget.
PF6-002 binds only members this probe verifies fold.

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

from pf6_covariance import fold_count, integrate  # noqa: E402
from projection_fold import canonical_sha256  # noqa: E402

CELLS = [(0.60, 0.8957885742187499),
         (0.70, 1.0448364257812501),
         (0.80, 1.2020141601562502),
         (0.90, 1.3605468750000003)]
PU0_LADDER = [0.1, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0]
N_STEPS = 40_000


def main() -> int:
    record: dict = {"schema": "pf6-member-probe-v1",
                    "label": "exploratory"}
    rows = []
    for p, e in CELLS:
        found = None
        scan = {}
        for pu0 in PU0_LADDER:
            r = integrate(p, e, n_steps=N_STEPS, pu0=pu0)
            n = fold_count(r[1])
            scan[f"{pu0:g}"] = int(n)
            if n > 0 and found is None:
                found = (pu0, n)
        rows.append({"P": p, "E": e, "scan": scan,
                     "pu0_selected": (found[0] if found else None),
                     "folds_selected": (found[1] if found else 0),
                     "folds": bool(found)})
        print(rows[-1], flush=True)
    record["rows"] = rows
    record["usable_cells"] = int(sum(r["folds"] for r in rows))
    record["declared"] = {"cells": CELLS, "pu0_ladder": PU0_LADDER,
                          "n_steps": N_STEPS,
                          "rule": "PF6-002 binds only members this "
                                  "probe verifies fold"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "pf6-member-probe.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("usable", record["usable_cells"])
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
