#!/usr/bin/env python3
"""PF5-001 governed gate run. Sealed under PREREG-PF5-001.

Applies the frozen PF-5 accounting instrument to the PF4-002
Sauter-slab family on the sealed grid. Every constant is from the
sealed document. The verdict is computed from the bars.
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

P_GRID = [0.60, 0.70, 0.80, 0.90]
E_GRID = [0.45, 0.70]
N_CELL = 20_000
K_POLY = 12
LEVEL_MULTS = [-0.61, -0.26, 0.14, 0.41, 0.69]
F_MAX = 0.20
MIN_EVALUABLE = 6


def main() -> int:
    record: dict = {"schema": "prereg-pf5-001-v1",
                    "registration_id": "PREREG-PF5-001",
                    "label": "sealed-gate-run"}
    t_exit = -pilot.T_START
    levels = [m * t_exit for m in LEVEL_MULTS]
    cells = {}
    evaluable = 0
    bars_ok = True
    for ip, p in enumerate(P_GRID):
        for ie, e in enumerate(E_GRID):
            seed = 8_100_000 + 1000 * ip + ie
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
                f, sk = signed_count_rule(pl["t"], pl["pt"],
                                          levels, pilot.DT)
                fails += len(f)
                refused += sk
            b3 = fails == 0
            frac_bad = (counts["nonfinite"] + counts["capped"]) \
                / N_CELL
            cell_eval = frac_bad < F_MAX
            if cell_eval:
                evaluable += 1
                bars_ok = bars_ok and b1 and b2 and b3
            cells[f"P{p}_E{e}"] = {
                "counts": counts,
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
            print(f"P={p} E={e} {counts} resid="
                  f"{res['max_energy_residual']:.2e} fails={fails}"
                  f" refused={refused} eval={cell_eval}",
                  flush=True)
    if evaluable < MIN_EVALUABLE:
        verdict = "manifest-design failure"
    elif bars_ok:
        verdict = "PASS"
    else:
        verdict = "FAIL"
    record["cells"] = cells
    record["evaluable_cells"] = int(evaluable)
    record["verdict"] = {"value": verdict,
                         "computed_from":
                             ["b1", "b2", "b3", "bar5-rule"]}
    record["declared"] = {"P_grid": P_GRID, "E_grid": E_GRID,
                          "n": N_CELL, "k_poly": K_POLY,
                          "level_mults": LEVEL_MULTS,
                          "f_max": F_MAX,
                          "min_evaluable": MIN_EVALUABLE}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "prereg-pf5-001.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
