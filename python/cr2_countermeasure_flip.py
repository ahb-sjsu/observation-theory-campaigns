#!/usr/bin/env python3
"""CR-2 the countermeasure flip (exploratory).

Protocol declared in CRYPTO-TRACK.md before this run. A single
declared secret bit read through leakage channels, so the scalar
fidelity battery is exactly the GD-1 battery of seven f-divergences
between the two conditional leakage distributions. The measured
question is whether a channel that every scalar measure ranks as
leakier can be worth less to a declared commitment task, the GD-1b
wedge in leakage form. Verdict computed from the measured items.

Exploratory label. The reading is about evaluation methodology in
declared finite models. Nothing here is a claim that any
countermeasure, implementation, or system is insecure, and none is
modeled.
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

from gd0_instrument import FEAS_TOL, experiment_value  # noqa: E402
from gd1_flip_blackwell import (  # noqa: E402
    DIV_KEYS, divergences, garbling_residual)
from gd1b_exhibit_certificate import conic_lower_bound  # noqa: E402
from projection_fold import canonical_sha256  # noqa: E402

PRIOR = np.array([0.5, 0.5])
INCOMP_TOL = 1e-2
WEDGE_TOL = 1e-6
DPI_TOL = 1e-10


def battery(rng):
    tasks = [rng.uniform(-1, 1, size=(3, 2)) for _ in range(200)]
    for c in (2.0, 5.0, 10.0, 20.0, 50.0):
        tasks.append(np.array([[0.0, 0.0], [-c, 1.0],
                               [1.0, -c]]))
    return tasks


def draw_channel(rng, k=4, floor=0.005):
    while True:
        c = rng.dirichlet(np.ones(k), size=2)
        if c.min() >= floor:
            return c


def main() -> int:
    record: dict = {"schema": "cr2-countermeasure-flip-v1",
                    "label": "exploratory"}
    rng = np.random.RandomState(20260902)
    tasks = battery(rng)
    items = {}

    # F1 the declared exhibit
    a = np.array([[0.55, 0.25, 0.15, 0.05],
                  [0.45, 0.25, 0.15, 0.15]])
    b = np.array([[0.49, 0.49, 0.01, 0.01],
                  [0.49, 0.49, 0.005, 0.015]])
    da, db = divergences(a[0], a[1]), divergences(b[0], b[1])
    margins = {k: da[k] - db[k] for k in DIV_KEYS}
    best_task = -np.inf
    for t in tasks:
        best_task = max(best_task,
                        experiment_value(PRIOR, t, b)
                        - experiment_value(PRIOR, t, a))
    bound = conic_lower_bound(a, b, PRIOR)
    tv_gap = da["tv"] - db["tv"]
    f1 = (all(m > 0.005 for m in margins.values())
          and best_task > 0.002
          and bound > 1e-3 and tv_gap > 0.005)
    items["F1_exhibit"] = f1

    # F2 data-processing control
    worst_div = np.inf
    worst_task = -np.inf
    for _ in range(500):
        x = draw_channel(rng)
        m = rng.dirichlet(np.ones(4), size=4)
        y = x @ m
        dx, dy = divergences(x[0], x[1]), divergences(y[0], y[1])
        worst_div = min(worst_div,
                        min(dx[k] - dy[k] for k in DIV_KEYS))
        for t in tasks:
            worst_task = max(worst_task,
                             experiment_value(PRIOR, t, y)
                             - experiment_value(PRIOR, t, x))
    items["F2_dpi"] = (worst_div > -DPI_TOL
                       and worst_task < DPI_TOL)

    # F3 and F4 the ensemble
    counts = {"comparable": 0, "incomparable": 0, "ambiguous": 0,
              "unanimous_incomparable": 0, "wedge_incomparable": 0,
              "wedge_comparable": 0, "wedge_ambiguous": 0}
    margins_list = []
    for i in range(2000):
        x = draw_channel(rng)
        y = draw_channel(rng)
        dx, dy = divergences(x[0], x[1]), divergences(y[0], y[1])
        signs = [np.sign(dx[k] - dy[k]) for k in DIV_KEYS]
        unanimous = all(s > 0 for s in signs) or all(s < 0
                                                     for s in signs)
        top, bot = (x, y) if signs[0] > 0 else (y, x)
        best_rev = -np.inf
        if unanimous:
            for t in tasks:
                best_rev = max(best_rev,
                               experiment_value(PRIOR, t, bot)
                               - experiment_value(PRIOR, t, top))
        wedge = unanimous and best_rev > WEDGE_TOL
        r1 = garbling_residual(x, y)
        r2 = garbling_residual(y, x)
        if r1 < FEAS_TOL or r2 < FEAS_TOL:
            cls = "comparable"
        elif r1 > INCOMP_TOL and r2 > INCOMP_TOL:
            cls = "incomparable"
        else:
            cls = "ambiguous"
        counts[cls] += 1
        if unanimous and cls == "incomparable":
            counts["unanimous_incomparable"] += 1
        if wedge:
            counts[f"wedge_{cls}"] += 1
            if cls == "incomparable":
                margins_list.append(float(best_rev))
        if (i + 1) % 500 == 0:
            print(f"  ensemble {i + 1}/2000 {counts}", flush=True)
    items["F3_localization"] = counts["wedge_comparable"] == 0
    wm = (np.array(margins_list) if margins_list
          else np.array([0.0]))

    record["measured"] = {
        "exhibit": {
            "divergence_margins": {k: float(v)
                                   for k, v in margins.items()},
            "min_divergence_margin": float(min(margins.values())),
            "best_task_margin_for_B": float(best_task),
            "conic_lower_bound": float(bound),
            "tv_gap": float(tv_gap)},
        "f2": {"worst_divergence_drop": float(worst_div),
               "worst_task_gain": float(worst_task)},
        "f3_counts": {k: int(v) for k, v in counts.items()},
        "f4_prevalence": {
            "unanimous_among_incomparable":
                int(counts["unanimous_incomparable"]),
            "wedge_among_incomparable":
                int(counts["wedge_incomparable"]),
            "wedge_margin_max": float(wm.max()),
            "wedge_margin_median": float(np.median(wm)),
            "gd1_comparison": "GD-1 measured 281 of 281 in "
                              "decision form"},
        "reading": "a reduction in a scalar leakage measure is not "
                   "a security guarantee outside certified "
                   "Blackwell comparability, a statement about "
                   "evaluation methodology in declared finite "
                   "models and about nothing else"}
    record["items"] = {k: bool(v) for k, v in items.items()}
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items)}
    record["declared"] = {"battery_size": len(tasks),
                          "incomp_tol": INCOMP_TOL,
                          "wedge_tol": WEDGE_TOL,
                          "dpi_tol": DPI_TOL,
                          "ensemble": 2000, "seed": 20260902}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "cr2-countermeasure-flip.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("exhibit", items["F1_exhibit"], "task", best_task,
          "bound", bound, "min div margin", min(margins.values()))
    print("counts", counts)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
