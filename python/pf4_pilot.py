#!/usr/bin/env python3
"""PF-4 candidate-family pilot (exploratory, PF4-DESIGN.md section 9.1).

Family P1, static-potential SHP. With static a^0 = a^5 = U(x) the
Euler-Lagrange equation for t integrates exactly, M tdot + eps U(x(tau))
= const, so tdot is enslaved to the local potential and reversal is the
deterministic condition eps [U(x) - U_in] > M tdot_in somewhere on the
trajectory. Rates over any declared ensemble are the measure of a fixed
initial-condition set. No dynamical exponential exists to measure; the
family is an analytic null for the Schwinger question, stated and
unit-tested, not swept.

Family P2S, resolved Sauter-slab energy transfer.

  H = p_t^2/2 + p_u^2/2 + omega_u^2 u^2/2 + lambda u^4/4
      + g E L tanh(t/L) u,

with omega_t = 0, initial momentum gap p_t(0) = P > 0, the event
starting outside the slab at t(0) = -4L, and the hidden oscillator
thermal at temperature T. The force on the time momentum is
-g E u sech^2(t/L), a field localized in a slab of width L that the
event crosses, so the field does bounded work.

Version note (v1 finding, preserved). The first sweep used the
unbounded coupling g E t u. Because t grows secularly with omega_t = 0,
that coupling does unbounded work, the oscillator equilibrium runs away,
and the fixed step under-resolved the strong-field cells (measured
energy drift up to 0.23 at E = 2). Those cells were dynamically and
numerically meaningless. The slab profile bounds the tilt at g E L,
which removes the runaway at its physical source; the step is also
tightened and a per-cell drift bar now excludes any cell above it from
every fit.

The event reverses when the oscillator transfers momentum P across the
gap during the slab crossing. Gaussian-tail reasoning predicts
exponential suppression with exponent proportional to P^2/(g E)^2,
which differs from the Schwinger-shaped axis P^2/(g E) by one power of
the field. The pilot measures reversal fractions over a (P, E) grid,
fits the powers, and compares the two axes. Continuous velocity-Verlet
integration throughout (closure clause C1), with a step-halving and an
independent-integrator control on one cell (C3/C4 style, pilot grade).

Exploratory label. No physics claim; the measured exponent is expected
to be measure-set, which is the point.
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

OMEGA_U = 1.2
LAM = 0.1
G = 1.0
T_BATH = 1.0
SAUTER_L = 3.0
T_START = -4.0 * SAUTER_L
DT = 1e-3
TAU_MAX = 40.0
N_PER_CELL = 50_000
SEED = 20260805
P_GRID = [1.0, 1.5, 2.0]
E_GRID = [0.5, 0.75, 1.0, 1.5, 2.0]
CONTROL_CELL = (1.5, 1.0)
MIN_COUNT_FOR_FIT = 5
DRIFT_BAR = 1e-4


def static_family_reverses(
    u_max: float, u_in: float, tdot_in: float, eps: float, mass: float = 1.0
) -> bool:
    """Family P1 exact reversal condition, from M tdot + eps U = const."""
    return eps * (u_max - u_in) > mass * tdot_in


def run_cell(p_gap, e_field, *, dt=DT, n=N_PER_CELL, seed=SEED,
             integrator="verlet"):
    rng = np.random.RandomState(seed + int(1000 * p_gap) + int(100 * e_field))
    t = np.full(n, T_START)
    pt = np.full(n, p_gap)
    u = rng.standard_normal(n) * math.sqrt(T_BATH) / OMEGA_U
    pu = rng.standard_normal(n) * math.sqrt(T_BATH)

    def slab(t):
        return SAUTER_L * np.tanh(t / SAUTER_L)

    def slab_force_profile(t):
        return 1.0 / np.cosh(t / SAUTER_L) ** 2

    def energy(t, pt, u, pu):
        return (0.5 * (pt**2 + pu**2) + 0.5 * OMEGA_U**2 * u**2
                + 0.25 * LAM * u**4 + G * e_field * slab(t) * u)

    e0 = energy(t, pt, u, pu)
    reversed_mask = np.zeros(n, dtype=bool)
    n_steps = int(round(TAU_MAX / dt))

    if integrator == "verlet":
        for _ in range(n_steps):
            ft = -G * e_field * u * slab_force_profile(t)
            fu = -OMEGA_U**2 * u - LAM * u**3 - G * e_field * slab(t)
            pt_h = pt + 0.5 * dt * ft
            pu_h = pu + 0.5 * dt * fu
            t = t + dt * pt_h
            u = u + dt * pu_h
            ft = -G * e_field * u * slab_force_profile(t)
            fu = -OMEGA_U**2 * u - LAM * u**3 - G * e_field * slab(t)
            pt = pt_h + 0.5 * dt * ft
            pu = pu_h + 0.5 * dt * fu
            reversed_mask |= pt <= 0.0
    elif integrator == "rk4":
        def rhs(state):
            t, pt, u, pu = state
            return np.array([
                pt, -G * e_field * u * slab_force_profile(t),
                pu,
                -OMEGA_U**2 * u - LAM * u**3 - G * e_field * slab(t),
            ])
        state = np.array([t, pt, u, pu])
        for _ in range(n_steps):
            k1 = rhs(state)
            k2 = rhs(state + 0.5 * dt * k1)
            k3 = rhs(state + 0.5 * dt * k2)
            k4 = rhs(state + dt * k3)
            state = state + dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
            reversed_mask |= state[1] <= 0.0
        t, pt, u, pu = state
    else:
        raise ValueError(integrator)

    drift = float(np.max(np.abs(energy(t, pt, u, pu) - e0)
                         / np.maximum(np.abs(e0), 1.0)))
    count = int(reversed_mask.sum())
    fraction = count / n
    stderr = math.sqrt(max(fraction * (1 - fraction), 1e-12) / n)
    return {"P": p_gap, "E": e_field, "n": n, "dt": dt,
            "integrator": integrator, "count": count,
            "fraction": fraction, "binomial_stderr": stderr,
            "max_relative_energy_drift": drift}


def usable_cells(cells):
    """Fit-eligible cells: enough counts, unsaturated, under the drift bar."""
    return [c for c in cells if c["count"] >= MIN_COUNT_FOR_FIT
            and c["fraction"] < 0.9
            and c["max_relative_energy_drift"] < DRIFT_BAR]


def fit_powers(cells):
    """Fit -log f = alpha * P^a * E^b on cells with enough counts."""
    usable = usable_cells(cells)
    if len(usable) < 4:
        return None
    y = np.log([-math.log(c["fraction"]) for c in usable])
    a_matrix = np.column_stack([
        np.ones(len(usable)),
        np.log([c["P"] for c in usable]),
        np.log([c["E"] for c in usable]),
    ])
    coef, residuals, _, _ = np.linalg.lstsq(a_matrix, y, rcond=None)
    predicted = a_matrix @ coef
    ss_res = float(np.sum((y - predicted) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    return {
        "n_cells_used": len(usable),
        "log_alpha": float(coef[0]),
        "P_power": float(coef[1]),
        "E_power": float(coef[2]),
        "r_squared": 1.0 - ss_res / max(ss_tot, 1e-300),
        "gaussian_tail_expectation": {"P_power": 2.0, "E_power": -2.0},
        "schwinger_shape_expectation": {"P_power": 2.0, "E_power": -1.0},
    }


def axis_comparison(cells):
    """R^2 of -log f against P^2/E^2 and against P^2/E, with intercept."""
    usable = usable_cells(cells)
    if len(usable) < 4:
        return None
    y = np.array([-math.log(c["fraction"]) for c in usable])

    def r2(x):
        a_matrix = np.column_stack([np.ones(len(usable)), x])
        coef, _, _, _ = np.linalg.lstsq(a_matrix, y, rcond=None)
        predicted = a_matrix @ coef
        ss_res = float(np.sum((y - predicted) ** 2))
        ss_tot = float(np.sum((y - y.mean()) ** 2))
        return 1.0 - ss_res / max(ss_tot, 1e-300), [float(v) for v in coef]

    gauss = r2(np.array([c["P"]**2 / c["E"]**2 for c in usable]))
    schwinger = r2(np.array([c["P"]**2 / c["E"] for c in usable]))
    return {
        "gaussian_axis_P2_over_E2": {"r_squared": gauss[0], "coef": gauss[1]},
        "schwinger_axis_P2_over_E": {"r_squared": schwinger[0],
                                     "coef": schwinger[1]},
    }


def main() -> int:
    cells = []
    for p_gap in P_GRID:
        for e_field in E_GRID:
            cell = run_cell(p_gap, e_field)
            cells.append(cell)
            print(f"P={p_gap} E={e_field}: fraction {cell['fraction']:.5f} "
                  f"({cell['count']}/{cell['n']}), drift "
                  f"{cell['max_relative_energy_drift']:.1e}")

    p_c, e_c = CONTROL_CELL
    base = next(c for c in cells if c["P"] == p_c and c["E"] == e_c)
    halved = run_cell(p_c, e_c, dt=DT / 2)
    rk4 = run_cell(p_c, e_c, integrator="rk4")
    for name, ctrl in (("dt-halving", halved), ("rk4", rk4)):
        pooled = math.sqrt(base["binomial_stderr"]**2
                           + ctrl["binomial_stderr"]**2)
        z = abs(ctrl["fraction"] - base["fraction"]) / max(pooled, 1e-12)
        print(f"control {name}: fraction {ctrl['fraction']:.5f} vs "
              f"{base['fraction']:.5f} (z = {z:.2f})")
        assert z < 4.0, f"prescription control failed ({name})"

    null_cell = run_cell(1.0, 0.0, n=5000)
    assert null_cell["count"] == 0, "zero-field null produced reversals"

    powers = fit_powers(cells)
    axes = axis_comparison(cells)

    excluded = [
        {"P": c["P"], "E": c["E"],
         "drift": c["max_relative_energy_drift"], "count": c["count"]}
        for c in cells if c not in usable_cells(cells)
    ]
    record = {
        "schema": "pf4-pilot-v2",
        "label": "exploratory",
        "v1_note": "the first sweep used the unbounded coupling g E t u; "
                   "secular growth of t made the field do unbounded work "
                   "and drift reached 0.23 at E = 2; superseded by the "
                   "Sauter-slab family before any record was written",
        "drift_bar": DRIFT_BAR,
        "cells_excluded_from_fits": excluded,
        "family_p1_static": {
            "statement": "M tdot + eps U(x) is exactly conserved for "
                "static a0 = a5 = U, so reversal is the deterministic "
                "condition eps (U_max - U_in) > M tdot_in and any rate "
                "is pure initial-condition measure; no dynamical "
                "exponential exists in this family",
        },
        "family_p2s": {
            "hamiltonian": "pt^2/2 + pu^2/2 + omega_u^2 u^2/2 + "
                           "lambda u^4/4 + g E L tanh(t/L) u, omega_t = 0, "
                           "t(0) = -4L",
            "parameters": {"omega_u": OMEGA_U, "lambda": LAM, "g": G,
                           "T": T_BATH, "L": SAUTER_L, "t_start": T_START,
                           "dt": DT, "tau_max": TAU_MAX,
                           "n_per_cell": N_PER_CELL, "seed": SEED},
            "P_grid": P_GRID, "E_grid": E_GRID,
            "cells": cells,
            "controls": {"dt_halving": halved, "rk4": rk4,
                         "zero_field_null": null_cell},
            "power_fit": powers,
            "axis_comparison": axes,
        },
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
    output = Path(__file__).resolve().parents[1] / "results" / "pf4-pilot.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    if powers:
        print(f"power fit over {powers['n_cells_used']} cells: "
              f"-log f ~ P^{powers['P_power']:.2f} E^{powers['E_power']:.2f} "
              f"(R^2 {powers['r_squared']:.4f}); Gaussian tail predicts "
              f"(2, -2), Schwinger shape predicts (2, -1)")
    if axes:
        print(f"axis comparison: P^2/E^2 R^2 = "
              f"{axes['gaussian_axis_P2_over_E2']['r_squared']:.4f}, "
              f"P^2/E R^2 = "
              f"{axes['schwinger_axis_P2_over_E']['r_squared']:.4f}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
