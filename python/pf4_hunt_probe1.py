#!/usr/bin/env python3
"""Non-measure-tail hunt, probe one (exploratory, PF track).

Probe zero measured the in-slab dip and found it power-law, because
the dip is the reversible adiabatic depression. The action-carrying
observable is the post-crossing residual, the oscillator excitation
about its asymptotic well after the passage completes, equivalently
the net momentum the crossing keeps. For a smooth passage at speed P
through the sech^2 slab profile, adiabatic-invariance analysis
predicts residual energy exponentially small in 1/P,

    E_res proportional to exp(-pi omega_u L / P),

an action-type, dynamics-set exponent measured here in an exactly
thermal-free system, so no initial measure contributes anything. If
the fitted slope of log E_res against 1/P is near -pi omega_u L, the
family possesses the hunt's candidate mechanism, an exponential whose
argument carries one power of the velocity scale, structurally
Schwinger-shaped and categorically not a measure tail.

RK4 at dt = 5e-4 (local accuracy preferred over symplecticity for
exponentially small residuals), integration until the event has fully
exited the slab. Exploratory label.
"""
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
from pf4_pilot import G, LAM, OMEGA_U, shifted_equilibrium  # noqa: E402
import pf4_pilot as fam  # noqa: E402

L_SLAB = 3.0
E_FIELD = 0.4
P_GRID = [1.2, 1.5, 2.0, 2.5, 3.0, 4.0]
DT = 5e-4
EXIT_MARGIN = 2.0


def crossing_residual(p_gap: float) -> dict:
    fam.SAUTER_L = L_SLAB
    fam.T_START = -4.0 * L_SLAB
    u0 = shifted_equilibrium(E_FIELD, fam.T_START)
    state = np.array([fam.T_START, p_gap, u0, 0.0])

    def rhs(s):
        t, pt, u, pu = s
        sech2 = 1.0 / math.cosh(t / L_SLAB) ** 2
        tanh = math.tanh(t / L_SLAB)
        return np.array([
            pt,
            -G * E_FIELD * u * sech2,
            pu,
            -OMEGA_U**2 * u - LAM * u**3 - G * E_FIELD * L_SLAB * tanh,
        ])

    max_tau = (8.0 * L_SLAB + 20.0) / max(p_gap, 0.1) + 30.0
    steps = int(round(max_tau / DT))
    for _ in range(steps):
        k1 = rhs(state)
        k2 = rhs(state + 0.5 * DT * k1)
        k3 = rhs(state + 0.5 * DT * k2)
        k4 = rhs(state + DT * k3)
        state = state + DT / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
        if state[0] > 4.0 * L_SLAB + EXIT_MARGIN * p_gap:
            break
    t_f, pt_f, u_f, pu_f = state
    assert t_f > 4.0 * L_SLAB, "crossing did not complete"

    u_star = shifted_equilibrium(E_FIELD, t_f)

    def potential(u):
        return (0.5 * OMEGA_U**2 * u**2 + 0.25 * LAM * u**4
                + G * E_FIELD * L_SLAB * math.tanh(t_f / L_SLAB) * u)

    e_res = 0.5 * pu_f**2 + potential(u_f) - potential(u_star)
    dp = p_gap - pt_f
    return {"P": p_gap, "pt_final": float(pt_f),
            "delta_pt": float(dp),
            "E_res": float(max(e_res, 1e-300)),
            "log_E_res": math.log(max(e_res, 1e-300))}


def main() -> int:
    rows = [crossing_residual(p) for p in P_GRID]
    for r in rows:
        print(f"P={r['P']}: E_res {r['E_res']:.4e}, "
              f"delta_pt {r['delta_pt']:.3e}")

    inv_p = np.array([1.0 / r["P"] for r in rows])
    log_e = np.array([r["log_E_res"] for r in rows])
    slope, intercept = np.polyfit(inv_p, log_e, 1)
    predicted = -math.pi * OMEGA_U * L_SLAB
    residuals = log_e - (slope * inv_p + intercept)
    r2 = 1.0 - float(np.sum(residuals**2)) \
        / max(float(np.sum((log_e - log_e.mean())**2)), 1e-300)

    record = {
        "schema": "pf4-hunt-probe1-v1",
        "label": "exploratory",
        "declared": {"L": L_SLAB, "E": E_FIELD, "P_grid": P_GRID,
                     "dt": DT, "omega_u": OMEGA_U,
                     "integrator": "rk4",
                     "observable": "post-crossing residual oscillator "
                                   "energy about the asymptotic well"},
        "rows": rows,
        "fit": {"slope_vs_invP": float(slope),
                "intercept": float(intercept), "r_squared": r2,
                "analyticity_prediction": predicted,
                "slope_ratio": float(slope / predicted)},
        "statement": "a slope near -pi omega_u L in a thermal-free "
            "system is a dynamics-set action-type exponential, the "
            "candidate non-measure-tail mechanism",
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
        / "pf4-hunt-probe1.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print(f"log E_res vs 1/P: slope {slope:.3f} (prediction {predicted:.3f}, "
          f"ratio {slope / predicted:.3f}), R^2 {r2:.4f}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
