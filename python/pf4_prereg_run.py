#!/usr/bin/env python3
"""Governed run of PREREG-PF4-001. Every constant is from the sealed
document; the family machinery is the sealed-commit code in pf4_pilot."""
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
from pf4_pilot import (  # noqa: E402
    DRIFT_BAR,
    DT,
    deterministic_probe,
    run_cell,
)

TRAIN_P = [0.5, 0.7, 0.9]
HELD_P = [0.6, 0.8]
TARGETS = [0.20, 0.28, 0.36, 0.44]
N_PER_CELL = 50_000
BISECT_LO, BISECT_HI, BISECT_TOL = 0.05, 1.6, 1e-3
MSE_G_BAR = 4.0
RATIO_BAR = 4.0
MIN_HELD_USABLE = 3


def probe_ratio(p_gap: float, e_field: float) -> float:
    d = deterministic_probe(p_gap, e_field)["pt_min"]
    return d / e_field if d > 0 else -1.0


def place_cell(p_gap: float, target: float) -> float:
    """Bisect E so that d(P, E)/E = target. d/E decreases in E."""
    lo, hi = BISECT_LO, BISECT_HI
    if probe_ratio(p_gap, hi) > target:
        raise RuntimeError(f"target {target} unreachable below E={hi}")
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        r = probe_ratio(p_gap, mid)
        if abs(r - target) < BISECT_TOL:
            return mid
        if r > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def usable(cell) -> bool:
    return (cell["count"] >= 5 and cell["fraction"] < 0.9
            and cell["max_relative_energy_drift"] < DRIFT_BAR
            and not cell["deterministically_reversing"])


def wls_fit(cells, axis):
    x = np.array([axis(c) for c in cells])
    y = np.array([-math.log(c["fraction"]) for c in cells])
    w = np.array([c["fraction"] * c["n"] / (1.0 - c["fraction"])
                  for c in cells])
    a_matrix = np.column_stack([np.ones_like(x), x])
    wa = a_matrix * w[:, None]
    coef = np.linalg.solve(a_matrix.T @ wa, a_matrix.T @ (w * y))
    return coef


def wmse(cells, axis, coef):
    x = np.array([axis(c) for c in cells])
    y = np.array([-math.log(c["fraction"]) for c in cells])
    w = np.array([c["fraction"] * c["n"] / (1.0 - c["fraction"])
                  for c in cells])
    predicted = coef[0] + coef[1] * x
    return float(np.mean(w * (y - predicted) ** 2))


def axis_g(cell):
    return (cell["deterministic_pt_min"] / cell["E"]) ** 2


def axis_s(cell):
    return cell["deterministic_pt_min"] ** 2 / cell["E"]


def run_block(p_values, label):
    cells = []
    for p_gap in p_values:
        for target in TARGETS:
            e_field = place_cell(p_gap, target)
            d_verlet = deterministic_probe(p_gap, e_field)["pt_min"]
            cell = run_cell(p_gap, e_field, n=N_PER_CELL)
            probe_rk4 = probe_rk4_min(p_gap, e_field)
            assert abs(d_verlet - probe_rk4) < 1e-3, \
                "probe prescription disagreement"
            cell["target_ratio"] = target
            cell["placed_E"] = e_field
            cell["probe_rk4_min"] = probe_rk4
            cells.append(cell)
            print(f"[{label}] P={p_gap} target={target} -> E={e_field:.4f}: "
                  f"fraction {cell['fraction']:.5f} "
                  f"({cell['count']}/{cell['n']}), "
                  f"d={cell['deterministic_pt_min']:.3f}, drift "
                  f"{cell['max_relative_energy_drift']:.1e}")
    return cells


def probe_rk4_min(p_gap, e_field):
    """The deterministic probe under RK4, for the prescription check."""
    import pf4_pilot as fam
    u0 = fam.shifted_equilibrium(e_field, fam.T_START)
    state = np.array([fam.T_START, p_gap, u0, 0.0])
    dt = DT
    pt_min = p_gap

    def rhs(s):
        t, pt, u, pu = s
        return np.array([
            pt,
            -fam.G * e_field * u / math.cosh(t / fam.SAUTER_L) ** 2,
            pu,
            -fam.OMEGA_U**2 * u - fam.LAM * u**3
            - fam.G * e_field * fam.SAUTER_L * math.tanh(t / fam.SAUTER_L),
        ])

    for _ in range(int(round(fam.TAU_MAX / dt))):
        k1 = rhs(state)
        k2 = rhs(state + 0.5 * dt * k1)
        k3 = rhs(state + 0.5 * dt * k2)
        k4 = rhs(state + dt * k3)
        state = state + dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
        pt_min = min(pt_min, float(state[1]))
    return pt_min


def main() -> int:
    null_cell = run_cell(0.7, 0.0, n=5000)
    assert null_cell["count"] == 0, "zero-field null failed"

    train = run_block(TRAIN_P, "train")
    held = run_block(HELD_P, "held")

    train_usable = [c for c in train if usable(c)]
    held_usable = [c for c in held if usable(c)]
    print(f"usable: train {len(train_usable)}/{len(train)}, "
          f"held {len(held_usable)}/{len(held)}")

    controls = {}
    if train_usable:
        for tag, target_f in (("near_1pct", 0.01), ("near_10pct", 0.1)):
            ctrl = min(train_usable,
                       key=lambda c: abs(c["fraction"] - target_f))
            rk4 = run_cell(ctrl["P"], ctrl["placed_E"], n=N_PER_CELL,
                           integrator="rk4")
            half = run_cell(ctrl["P"], ctrl["placed_E"], n=N_PER_CELL,
                            dt=DT / 2)
            entry = {"cell": {"P": ctrl["P"], "E": ctrl["placed_E"],
                              "fraction": ctrl["fraction"]}}
            for name, other in (("rk4", rk4), ("dt_half", half)):
                pooled = math.sqrt(ctrl["binomial_stderr"]**2
                                   + other["binomial_stderr"]**2)
                z = abs(other["fraction"] - ctrl["fraction"]) \
                    / max(pooled, 1e-12)
                entry[name] = {"fraction": other["fraction"], "z": z}
                assert z < 4.0, f"C3/C4 control failed ({tag}, {name})"
            controls[tag] = entry
            print(f"control {tag}: base {entry['cell']['fraction']:.5f}, "
                  f"rk4 z={entry['rk4']['z']:.2f}, "
                  f"dt/2 z={entry['dt_half']['z']:.2f}")

    if len(held_usable) < MIN_HELD_USABLE:
        label = "unevaluable"
        outcome = ("manifest-design failure: fewer than three held-out "
                   "cells usable")
        fits = None
    else:
        coef_g = wls_fit(train_usable, axis_g)
        coef_s = wls_fit(train_usable, axis_s)
        mse_g = wmse(held_usable, axis_g, coef_g)
        mse_s = wmse(held_usable, axis_s, coef_s)
        fits = {
            "model_G": {"alpha": float(coef_g[0]), "beta": float(coef_g[1]),
                        "held_out_wmse": mse_g},
            "model_S": {"alpha": float(coef_s[0]), "beta": float(coef_s[1]),
                        "held_out_wmse": mse_s},
            "ratio_S_over_G": mse_s / mse_g if mse_g > 0 else float("inf"),
        }
        bar_a = mse_g <= MSE_G_BAR
        bar_b = mse_s >= RATIO_BAR * mse_g
        if bar_a and bar_b:
            label = "demonstrated-in-model"
            outcome = ("claim PASSES: the effective-gap Gaussian axis "
                       "predicts held-out cells and the Schwinger-shaped "
                       "axis is decisively worse")
        elif mse_s <= mse_g:
            label = "refuted"
            outcome = "claim REFUTED: the Schwinger-shaped axis fits as "\
                      "well or better"
        else:
            label = "neither-axis"
            outcome = "neither bar met: reported with both residual sets"

    record = {
        "schema": "prereg-pf4-001-run-v1",
        "registration_id": "PREREG-PF4-001",
        "label": label,
        "outcome": outcome,
        "fits": fits,
        "declared": {
            "train_P": TRAIN_P, "held_P": HELD_P, "targets": TARGETS,
            "n_per_cell": N_PER_CELL, "mse_g_bar": MSE_G_BAR,
            "ratio_bar": RATIO_BAR,
        },
        "train_cells": train, "held_cells": held,
        "controls": controls,
        "zero_field_null": null_cell,
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
        / "prereg-pf4-001.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")
    if fits:
        print(f"G: wmse {fits['model_G']['held_out_wmse']:.3f} "
              f"(beta {fits['model_G']['beta']:.1f}); "
              f"S: wmse {fits['model_S']['held_out_wmse']:.3f}; "
              f"ratio {fits['ratio_S_over_G']:.2f}")
    print(outcome)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
