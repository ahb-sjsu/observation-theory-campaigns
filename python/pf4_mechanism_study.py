#!/usr/bin/env python3
"""PF-4 mechanism mini-study (exploratory, unsealed).

Why is the thermal-free pulse-train family empty. Declared
hypothesis, the slabs alternate in sign, so the oscillator-mediated
momentum transfer alternates with them and consecutive deposits
cancel, leaving a residual drift orders of magnitude too small to
spend the gap within any feasible cap. This study integrates the
sealed dynamics verbatim for single trajectories and records the
velocity at every slab boundary, measuring the per-slab deposits,
their cancellation ratio, their sign-alternation fraction, and the
extrapolated slabs-to-reversal.

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

from pf4_004_probe import run_cells  # noqa: F401  (dynamics twin)
from pf4_frozen_run import D_SPACING, L_SLAB, tilt_and_force  # noqa: E402
from pf4_pilot import G, LAM, OMEGA_U, shifted_equilibrium  # noqa: E402
from projection_fold import canonical_sha256  # noqa: E402

DT = 2e-3
N_SLABS = 60
CELLS = [(0.6, 1.2), (1.0, 1.5), (1.5, 2.1)]


def trace_cell(e_field, p0):
    t = np.array([-4.0 * L_SLAB])
    pt = np.array([float(p0)])
    u = np.array([shifted_equilibrium(e_field, -4.0 * L_SLAB)])
    pu = np.array([0.0])

    def rhs(t_, pt_, u_, pu_):
        s, f = tilt_and_force(t_, True)
        return (pt_,
                -G * e_field * u_ * f,
                pu_,
                -OMEGA_U ** 2 * u_ - LAM * u_ ** 3
                - G * e_field * L_SLAB * s)

    boundary_pt = []
    next_k = 0
    while next_k <= N_SLABS:
        d1 = rhs(t, pt, u, pu)
        d2 = rhs(t + 0.5 * DT * d1[0], pt + 0.5 * DT * d1[1],
                 u + 0.5 * DT * d1[2], pu + 0.5 * DT * d1[3])
        d3 = rhs(t + 0.5 * DT * d2[0], pt + 0.5 * DT * d2[1],
                 u + 0.5 * DT * d2[2], pu + 0.5 * DT * d2[3])
        d4 = rhs(t + DT * d3[0], pt + DT * d3[1],
                 u + DT * d3[2], pu + DT * d3[3])
        t = t + DT / 6 * (d1[0] + 2 * d2[0] + 2 * d3[0] + d4[0])
        pt = pt + DT / 6 * (d1[1] + 2 * d2[1] + 2 * d3[1] + d4[1])
        u = u + DT / 6 * (d1[2] + 2 * d2[2] + 2 * d3[2] + d4[2])
        pu = pu + DT / 6 * (d1[3] + 2 * d2[3] + 2 * d3[3] + d4[3])
        if float(t[0]) >= next_k * D_SPACING:
            boundary_pt.append(float(pt[0]))
            next_k += 1
    deposits = np.diff(np.array(boundary_pt))
    denom = float(np.sum(np.abs(deposits)))
    cancel = abs(float(np.sum(deposits))) / max(denom, 1e-300)
    signs = np.sign(deposits)
    flips = float(np.mean(signs[1:] * signs[:-1] < 0))
    drift = float(np.mean(deposits))
    slabs_to_rev = (p0 / abs(drift)) if drift != 0 else float("inf")
    return {"P": p0, "E": e_field,
            "pt_first_last": [boundary_pt[0], boundary_pt[-1]],
            "mean_abs_deposit": denom / len(deposits),
            "cancellation_ratio": cancel,
            "sign_flip_fraction": flips,
            "mean_drift_per_slab": drift,
            "extrapolated_slabs_to_reversal": slabs_to_rev}


def main() -> int:
    record: dict = {"schema": "pf4-mechanism-v1",
                    "label": "exploratory"}
    cells = []
    for e, p in CELLS:
        row = trace_cell(e, p)
        cells.append(row)
        print(row, flush=True)
    record["cells"] = cells
    worst_slabs = min(c["extrapolated_slabs_to_reversal"]
                      for c in cells)
    record["finding"] = {
        "hypothesis": "alternating slabs cancel deposits",
        "min_extrapolated_slabs_to_reversal": float(worst_slabs),
        "supported": bool(
            all(c["cancellation_ratio"] < 0.5 for c in cells)
            and worst_slabs > 4000)}
    record["declared"] = {"dt": DT, "n_slabs": N_SLABS,
                          "cells": CELLS}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "pf4-mechanism.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("finding", record["finding"])
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
