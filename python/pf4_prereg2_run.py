#!/usr/bin/env python3
"""Governed run of PREREG-PF4-002. Reuses the sealed PF4-001 machinery;
only the grids and the bar arithmetic of the sealed document change."""
from __future__ import annotations

import json
import math
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from projection_fold import canonical_sha256  # noqa: E402
from pf4_pilot import DT, run_cell  # noqa: E402
import pf4_prereg_run as m1  # noqa: E402
from pf4_prereg_run import (  # noqa: E402
    axis_g,
    axis_s,
    run_block,
    usable,
    wls_fit,
    wmse,
)

TRAIN_P = [0.55, 0.75, 0.95]
HELD_P = [0.65, 0.85]
TARGETS = [0.22, 0.30, 0.38, 0.46]
GEN_RATIO_BAR = 2.0
S_RATIO_BAR = 2.0
MIN_HELD_USABLE = 3

m1.TARGETS = TARGETS  # declared-grid substitution, per the estimator


def main() -> int:
    null_cell = run_cell(0.75, 0.0, n=5000)
    assert null_cell["count"] == 0, "zero-field null failed"

    train = run_block(TRAIN_P, "train")
    held = run_block(HELD_P, "held")
    train_usable = [c for c in train if usable(c)]
    held_usable = [c for c in held if usable(c)]
    print(f"usable: train {len(train_usable)}/{len(train)}, "
          f"held {len(held_usable)}/{len(held)}")

    controls = {}
    for tag, target_f in (("near_1pct", 0.01), ("near_10pct", 0.1)):
        ctrl = min(train_usable, key=lambda c: abs(c["fraction"] - target_f))
        rk4 = run_cell(ctrl["P"], ctrl["placed_E"], n=50_000,
                       integrator="rk4")
        half = run_cell(ctrl["P"], ctrl["placed_E"], n=50_000, dt=DT / 2)
        entry = {"cell": {"P": ctrl["P"], "E": ctrl["placed_E"],
                          "fraction": ctrl["fraction"]}}
        for name, other in (("rk4", rk4), ("dt_half", half)):
            pooled = math.sqrt(ctrl["binomial_stderr"]**2
                               + other["binomial_stderr"]**2)
            z = abs(other["fraction"] - ctrl["fraction"]) / max(pooled, 1e-12)
            entry[name] = {"fraction": other["fraction"], "z": z}
            assert z < 4.0, f"C3/C4 control failed ({tag}, {name})"
        controls[tag] = entry
        print(f"control {tag}: base {entry['cell']['fraction']:.5f}, "
              f"rk4 z={entry['rk4']['z']:.2f}, "
              f"dt/2 z={entry['dt_half']['z']:.2f}")

    if len(held_usable) < MIN_HELD_USABLE:
        label, outcome, fits = "unevaluable", \
            "manifest-design failure: fewer than three held-out usable", None
    else:
        coef_g = wls_fit(train_usable, axis_g)
        coef_s = wls_fit(train_usable, axis_s)
        train_mse_g = wmse(train_usable, axis_g, coef_g)
        train_mse_s = wmse(train_usable, axis_s, coef_s)
        held_mse_g = wmse(held_usable, axis_g, coef_g)
        held_mse_s = wmse(held_usable, axis_s, coef_s)
        fits = {
            "model_G": {"alpha": float(coef_g[0]), "beta": float(coef_g[1]),
                        "train_wmse": train_mse_g,
                        "held_wmse": held_mse_g,
                        "generalization_ratio": held_mse_g
                        / max(train_mse_g, 1e-300)},
            "model_S": {"alpha": float(coef_s[0]), "beta": float(coef_s[1]),
                        "train_wmse": train_mse_s,
                        "held_wmse": held_mse_s},
            "ratio_S_over_G_held": held_mse_s / max(held_mse_g, 1e-300),
        }
        bar_a = fits["model_G"]["generalization_ratio"] <= GEN_RATIO_BAR
        bar_b = fits["ratio_S_over_G_held"] >= S_RATIO_BAR
        if bar_a and bar_b:
            label = "demonstrated-in-model"
            outcome = ("claim PASSES: the effective-gap axis generalizes "
                       "within its accuracy class and the Schwinger-shaped "
                       "axis fails to compete")
        elif held_mse_s <= held_mse_g:
            label, outcome = "refuted", \
                "claim REFUTED: the Schwinger-shaped axis fits held-out "\
                "cells as well or better"
        else:
            label, outcome = "neither-axis", \
                "neither bar met: reported with both residual sets"

    record = {
        "schema": "prereg-pf4-002-run-v1",
        "registration_id": "PREREG-PF4-002",
        "label": label,
        "outcome": outcome,
        "fits": fits,
        "declared": {"train_P": TRAIN_P, "held_P": HELD_P,
                     "targets": TARGETS,
                     "generalization_ratio_bar": GEN_RATIO_BAR,
                     "s_ratio_bar": S_RATIO_BAR},
        "train_cells": train, "held_cells": held,
        "controls": controls, "zero_field_null": null_cell,
        "runtime": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version,
            "numpy": np.__version__,
            "platform": platform.platform(),
            "hostname": platform.node(),
            "code_commit": os.environ.get("CODE_COMMIT", "unknown"),
        },
    }
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"}
    )
    output = Path(__file__).resolve().parents[1] / "results" \
        / "prereg-pf4-002.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")
    if fits:
        g = fits["model_G"]
        print(f"G: train {g['train_wmse']:.2f}, held {g['held_wmse']:.2f}, "
              f"gen ratio {g['generalization_ratio']:.2f} (bar "
              f"{GEN_RATIO_BAR}); S held {fits['model_S']['held_wmse']:.2f}; "
              f"S/G {fits['ratio_S_over_G_held']:.2f} (bar {S_RATIO_BAR})")
    print(outcome)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
