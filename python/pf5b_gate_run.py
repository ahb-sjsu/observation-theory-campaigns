#!/usr/bin/env python3
"""PF5-002 governed gate run. Sealed under PREREG-PF5-002.

Applies the frozen PF-5 accounting instrument to the PF4-002
Sauter-slab family on the probe-placed cells bound in the sealed
document, with the anti-vacuity bar that PREREG-PF5-001 lacked.
Every constant is from the sealed document. The verdict is computed
from the bars.
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

import pf4_pilot as pilot  # noqa: E402
from pf5_accounting import census_run, signed_count_rule  # noqa: E402
from projection_fold import canonical_sha256  # noqa: E402

# (gap, field) bound from results/pf5-placement-probe.json
CELLS = [(0.60, 0.8957885742187499),
         (0.70, 1.0448364257812501),
         (0.80, 1.2020141601562502),
         (0.90, 1.3605468750000003)]
PROBE_FRACTIONS = [0.1000, 0.0970, 0.0995, 0.1030]
N_CELL = 20_000
K_POLY = 12
LEVEL_MULTS = [-0.61, -0.26, 0.14, 0.41, 0.69]
F_MAX = 0.20
MIN_EVALUABLE = 3
MIN_TOTAL_REVERSALS = 2000


def main() -> int:
    record: dict = {"schema": "prereg-pf5-002-v1",
                    "registration_id": "PREREG-PF5-002",
                    "label": "sealed-gate-run"}
    t_exit = -pilot.T_START
    levels = [m * t_exit for m in LEVEL_MULTS]
    cells = {}
    evaluable = 0
    bars_ok = True
    total_rev = 0
    all_cells_have_events = True
    for i, (p, e) in enumerate(CELLS):
        seed = 8_300_000 + 1000 * i
        res = census_run(p, e, N_CELL, seed,
                         keep_polyline=tuple(range(K_POLY)))
        counts = res["counts"]
        b1 = (sum(counts.values()) == N_CELL
              and res["missing"] == 0)
        b2 = res["max_energy_residual"] < 1e-5
        fails = 0
        refused = 0
        for k in range(K_POLY):
            pl = res["polylines"][str(k)]
            f, sk = signed_count_rule(pl["t"], pl["pt"], levels,
                                      pilot.DT)
            fails += len(f)
            refused += sk
        b3 = fails == 0
        frac_bad = (counts["nonfinite"] + counts["capped"]) / N_CELL
        cell_eval = frac_bad < F_MAX
        if cell_eval:
            evaluable += 1
            bars_ok = bars_ok and b1 and b2 and b3
            total_rev += counts["reversing"]
            if counts["reversing"] <= 0:
                all_cells_have_events = False
        cells[f"P{p}_E{e:.6f}"] = {
            "counts": counts,
            "probe_fraction": PROBE_FRACTIONS[i],
            "max_energy_residual":
                float(res["max_energy_residual"]),
            "path_degree_failures": int(fails),
            "refused_levels": int(refused),
            "reversing_fraction_full_denominator":
                counts["reversing"] / N_CELL,
            "bad_fraction": float(frac_bad),
            "evaluable": bool(cell_eval),
            "bars": {"b1": bool(b1), "b2": bool(b2),
                     "b3": bool(b3)}}
        print(f"P={p} E={e:.6f} {counts} resid="
              f"{res['max_energy_residual']:.2e} fails={fails}"
              f" refused={refused} eval={cell_eval}", flush=True)
    b6 = all_cells_have_events and total_rev >= MIN_TOTAL_REVERSALS
    if evaluable < MIN_EVALUABLE:
        verdict = "manifest-design failure"
    elif not b6:
        verdict = "vacuous"
    elif bars_ok:
        verdict = "PASS"
    else:
        verdict = "FAIL"
    record["cells"] = cells
    record["evaluable_cells"] = int(evaluable)
    record["total_reversing_evaluable"] = int(total_rev)
    record["bars"] = {"b1_b3_all_evaluable": bool(bars_ok),
                      "b6_anti_vacuity": bool(b6)}
    record["verdict"] = {
        "value": verdict,
        "computed_from": ["b1", "b2", "b3", "bar5-rule", "b6"]}
    record["declared"] = {"cells": CELLS,
                          "probe_fractions": PROBE_FRACTIONS,
                          "n": N_CELL, "k_poly": K_POLY,
                          "level_mults": LEVEL_MULTS,
                          "f_max": F_MAX,
                          "min_evaluable": MIN_EVALUABLE,
                          "min_total_reversals":
                              MIN_TOTAL_REVERSALS}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "prereg-pf5-002.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("total reversing", total_rev)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
