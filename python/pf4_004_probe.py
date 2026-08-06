#!/usr/bin/env python3
"""PF4-004 manifest probe (exploratory, unsealed, PF track).

PF4-003 sealed itself unevaluable, every cell capped without a
reversal, because its manifest was placed from a probe of a proxy
observable at different declared constants. This probe measures the
sealed observable N_rev directly, with the sealed runner's dynamics
mirrored verbatim, across a declared ladder of field strengths and
velocities, so that a PF4-004 manifest can bind only to cells this
probe verifies reverse below half its cap. The PF4-004 rule, no
cell enters a sealed manifest without a committed direct-observable
probe at the exact sealed constants.

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

from pf4_frozen_run import (  # noqa: E402
    D_SPACING, L_SLAB, tilt_and_force)
from pf4_pilot import shifted_equilibrium  # noqa: E402
from projection_fold import canonical_sha256  # noqa: E402

DT = 2e-3
N_CAP_PROBE = 300
E_LADDER = [0.6, 1.0, 1.5]
P_GRID = [1.2, 1.5, 1.8, 2.1]


def run_cells(e_field, p_values, dt=DT, cap=N_CAP_PROBE):
    """The sealed runner's dynamics verbatim, parameterized only by
    the field strength, the timestep, and the slab cap."""
    from pf4_pilot import G, LAM, OMEGA_U
    p = np.array(p_values, dtype=float)
    n = p.size
    u0 = shifted_equilibrium(e_field, -4.0 * L_SLAB)
    t = np.full(n, -4.0 * L_SLAB)
    pt = p.copy()
    u = np.full(n, u0)
    pu = np.zeros(n)
    alive = np.ones(n, dtype=bool)
    n_rev = np.full(n, -1.0)

    def rhs(t_, pt_, u_, pu_):
        s, f = tilt_and_force(t_, True)
        return (pt_,
                -G * e_field * u_ * f,
                pu_,
                -OMEGA_U ** 2 * u_ - LAM * u_ ** 3
                - G * e_field * L_SLAB * s)

    tau_max = (cap * D_SPACING) / max(min(p_values), 0.1)
    steps = int(round(tau_max / dt))
    for _ in range(steps):
        if not alive.any():
            break
        d1 = rhs(t, pt, u, pu)
        d2 = rhs(t + 0.5 * dt * d1[0], pt + 0.5 * dt * d1[1],
                 u + 0.5 * dt * d1[2], pu + 0.5 * dt * d1[3])
        d3 = rhs(t + 0.5 * dt * d2[0], pt + 0.5 * dt * d2[1],
                 u + 0.5 * dt * d2[2], pu + 0.5 * dt * d2[3])
        d4 = rhs(t + dt * d3[0], pt + dt * d3[1],
                 u + dt * d3[2], pu + dt * d3[3])
        m = alive
        t = np.where(m, t + dt / 6 * (d1[0] + 2 * d2[0] + 2 * d3[0]
                                      + d4[0]), t)
        pt_new = np.where(m, pt + dt / 6 * (d1[1] + 2 * d2[1]
                                            + 2 * d3[1] + d4[1]), pt)
        u = np.where(m, u + dt / 6 * (d1[2] + 2 * d2[2] + 2 * d3[2]
                                      + d4[2]), u)
        pu = np.where(m, pu + dt / 6 * (d1[3] + 2 * d2[3] + 2 * d3[3]
                                        + d4[3]), pu)
        reversed_now = m & (pt_new <= 0.0)
        if reversed_now.any():
            n_rev[reversed_now] = np.maximum(
                t[reversed_now] / D_SPACING, 0.5)
            alive &= ~reversed_now
        pt = pt_new
        if (t[alive] > cap * D_SPACING).any():
            capped = alive & (t > cap * D_SPACING)
            alive &= ~capped
    return [{"P": float(pv), "N_rev": float(nr),
             "reversed": bool(nr > 0)}
            for pv, nr in zip(p, n_rev, strict=True)]


def main() -> int:
    record: dict = {"schema": "pf4-004-probe-v1",
                    "label": "exploratory"}
    grid = {}
    for e in E_LADDER:
        rows = run_cells(e, P_GRID)
        grid[str(e)] = rows
        print("E", e, [(r["P"], round(r["N_rev"], 1)) for r in rows],
              flush=True)
    # dt-halving check on the most promising populated cell
    check = None
    for e in E_LADDER:
        pop = [r for r in grid[str(e)] if r["reversed"]]
        if pop:
            p0 = pop[0]["P"]
            fine = run_cells(e, [p0], dt=1e-3)
            check = {"E": e, "P": p0,
                     "n_rev_dt2e3": pop[0]["N_rev"],
                     "n_rev_dt1e3": fine[0]["N_rev"]}
            break
    record["grid"] = grid
    record["dt_check"] = check
    record["declared"] = {"dt": DT, "cap": N_CAP_PROBE,
                          "E_ladder": E_LADDER, "P_grid": P_GRID,
                          "rule": "PF4-004 manifest cells must "
                                  "reverse below cap/2 in this "
                                  "probe at identical constants"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "pf4-004-probe.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
