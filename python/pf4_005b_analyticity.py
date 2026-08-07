#!/usr/bin/env python3
"""PF4-005b the analyticity exponent, matched regimes.

Protocol declared in CAMPAIGN.md before this run. PF4-002 sealed the
negative that the Sauter family's suppression is a Gaussian measure
tail in the effective gap, and left the summit question, whether any
constructible family has a non-measure-tail exponent. PF4-003 and
the PF4-004 probe closed the pulse-train route by measuring that
family empty, and the mechanism study explained why, the deposits
cancel with no fixed sign.

This run takes the route the first hunt probe left open. A single
deterministic crossing has one declared initial condition, so there
is no distribution whose tail could produce a suppression, and the
probe already measured the transfer to be exponential in the inverse
velocity with a coefficient of determination of 0.992. What that
probe could not say is whether the exponent is dynamical. This run
decides that by changing the field's complex singularity structure
while holding its width fixed, because an exponent set by a
singularity distance is a dynamical quantity and no measure tail
knows where a function's poles are.

The two declared predictions are parameter free and are ratios, so
they do not depend on the absolute coefficient the probe found to be
0.69 of the naive estimate.

Exploratory label. Not claim-bearing.
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

import pf4_pilot as pilot  # noqa: E402
from projection_fold import canonical_sha256  # noqa: E402

E_FIELD = 0.4
KAPPA_GRID = [0.9, 1.2, 1.5, 2.0, 2.5, 3.0]
L_GRID = [2.0, 3.0, 4.0]
DT = 2e-4
SPAN = 20.0          # integration half-range in units of L
R2_BAR = 0.99
UNIV_TOL = 0.10
ABS_TOL = 0.15
ABS_PREDICTION = -2.0
CONV_TOL = 0.02


def tilt_and_force(t, l_s, profile):
    """Declared tilt s(t) running from minus one to plus one and the
    force f(t) that multiplies the oscillator coordinate. The pole
    of s' nearest the real axis sits at the recorded distance."""
    if profile == "sech2":
        return np.tanh(t / l_s), 1.0 / np.cosh(
            np.clip(t / l_s, -300, 300)) ** 2
    if profile == "lorentz":
        return ((2.0 / math.pi) * np.arctan(t / l_s),
                (2.0 / math.pi) / (1.0 + (t / l_s) ** 2))
    raise ValueError(profile)


POLE_DISTANCE = {"sech2": math.pi / 2.0, "lorentz": 1.0}


def equilibrium(tilt_value, l_s):
    """Instantaneous minimum of the oscillator potential."""
    u = -pilot.G * E_FIELD * l_s * tilt_value / pilot.OMEGA_U ** 2
    for _ in range(60):
        f = (pilot.OMEGA_U ** 2 * u + pilot.LAM * u ** 3
             + pilot.G * E_FIELD * l_s * tilt_value)
        fp = pilot.OMEGA_U ** 2 + 3.0 * pilot.LAM * u ** 2
        step = f / fp
        u = u - step
        if np.all(np.abs(step) < 1e-15):
            break
    return u


def potential(u, tilt_value, l_s):
    return (0.5 * pilot.OMEGA_U ** 2 * u ** 2
            + 0.25 * pilot.LAM * u ** 4
            + pilot.G * E_FIELD * l_s * tilt_value * u)


def run_cell(profile, l_s, p_values, dt):
    """Deterministic crossings at the declared velocities, started
    in the instantaneous well at the entry time with zero velocity.
    Returns the residual oscillator energy about the instantaneous
    well at the exit time."""
    p = np.array(p_values, dtype=float)
    n = p.size
    t0 = -SPAN * l_s
    t = np.full(n, t0)
    pt = p.copy()
    s0, _ = tilt_and_force(np.array([t0]), l_s, profile)
    u = np.full(n, float(equilibrium(s0[0], l_s)))
    pu = np.zeros(n)

    def rhs(t_, pt_, u_, pu_):
        s, f = tilt_and_force(t_, l_s, profile)
        return (pt_,
                -pilot.G * E_FIELD * u_ * f,
                pu_,
                -pilot.OMEGA_U ** 2 * u_ - pilot.LAM * u_ ** 3
                - pilot.G * E_FIELD * l_s * s)

    t_end = SPAN * l_s
    steps = int(math.ceil((2.0 * SPAN * l_s) / (dt * p.min()))) + 2
    for _ in range(steps):
        if np.all(t >= t_end):
            break
        live = t < t_end
        d1 = rhs(t, pt, u, pu)
        d2 = rhs(t + 0.5 * dt * d1[0], pt + 0.5 * dt * d1[1],
                 u + 0.5 * dt * d1[2], pu + 0.5 * dt * d1[3])
        d3 = rhs(t + 0.5 * dt * d2[0], pt + 0.5 * dt * d2[1],
                 u + 0.5 * dt * d2[2], pu + 0.5 * dt * d2[3])
        d4 = rhs(t + dt * d3[0], pt + dt * d3[1],
                 u + dt * d3[2], pu + dt * d3[3])
        t = np.where(live, t + dt / 6 * (d1[0] + 2 * d2[0]
                                         + 2 * d3[0] + d4[0]), t)
        pt = np.where(live, pt + dt / 6 * (d1[1] + 2 * d2[1]
                                           + 2 * d3[1] + d4[1]), pt)
        u = np.where(live, u + dt / 6 * (d1[2] + 2 * d2[2]
                                         + 2 * d3[2] + d4[2]), u)
        pu = np.where(live, pu + dt / 6 * (d1[3] + 2 * d2[3]
                                           + 2 * d3[3] + d4[3]), pu)
    s_end, _ = tilt_and_force(t, l_s, profile)
    u_star = equilibrium(s_end, l_s)
    e_res = (0.5 * pu ** 2 + potential(u, s_end, l_s)
             - potential(u_star, s_end, l_s))
    return e_res, pt


def fit_slope(kappa_values, e_res):
    x = np.array(kappa_values, dtype=float)
    y = np.log(np.asarray(e_res, dtype=float))
    a = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(a, y, rcond=None)
    pred = a @ coef
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return float(coef[0]), float(coef[1]), r2


def main() -> int:
    record: dict = {"schema": "pf4-005b-analyticity-v1",
                    "label": "exploratory"}
    cells = {}
    for profile in ("sech2", "lorentz"):
        for l_s in L_GRID:
            a = POLE_DISTANCE[profile] * l_s
            p_values = [pilot.OMEGA_U * a / k for k in KAPPA_GRID]
            e_res, pt_end = run_cell(profile, l_s, p_values, DT)
            slope, icept, r2 = fit_slope(KAPPA_GRID, e_res)
            cells[f"{profile}_L{l_s}"] = {
                "profile": profile, "L": l_s,
                "pole_distance": float(a),
                "p_values": [float(v) for v in p_values],
                "kappa_grid": KAPPA_GRID,
                "e_res": [float(v) for v in e_res],
                "pt_final": [float(v) for v in pt_end],
                "slope_vs_kappa": slope, "intercept": icept,
                "r_squared": r2,
                "slope_over_prediction":
                    float(slope / ABS_PREDICTION)}
            print(f"  {profile} L={l_s} slope_kappa={slope:.6f} "
                  f"r2={r2:.6f} vs -2 -> "
                  f"{slope / ABS_PREDICTION:.4f}", flush=True)

    items = {}
    items["B1_exponential_form"] = all(
        c["r_squared"] >= R2_BAR for c in cells.values())

    def slopes(profile):
        return [cells[f"{profile}_L{l}"]["slope_vs_kappa"]
                for l in L_GRID]

    lor = slopes("lorentz")
    sec = slopes("sech2")
    lor_mean = float(np.mean(lor))
    sec_mean = float(np.mean(sec))
    lor_spread = float((max(lor) - min(lor)) / abs(lor_mean))
    sec_spread = float((max(sec) - min(sec)) / abs(sec_mean))
    items["B2_lorentz_width_universal"] = lor_spread <= UNIV_TOL
    items["B3_lorentz_matches_prediction"] = all(
        abs(v - ABS_PREDICTION) <= ABS_TOL * abs(ABS_PREDICTION)
        for v in lor)

    e_fine, _ = run_cell(
        "sech2", 4.0,
        [pilot.OMEGA_U * POLE_DISTANCE["sech2"] * 4.0
         / KAPPA_GRID[-1]], DT / 2.0)
    e_coarse = cells["sech2_L4.0"]["e_res"][-1]
    conv = abs(float(e_fine[0]) - e_coarse) / abs(e_coarse)
    items["B0_timestep_convergence"] = conv <= CONV_TOL

    findings = {
        "F1_sech2_not_width_universal": bool(
            sec_spread > UNIV_TOL),
        "F2_sech2_below_prediction": bool(
            all(abs(v) < abs(ABS_PREDICTION) for v in sec))}

    record["measured"] = {
        "cells": cells,
        "lorentz_slopes": [float(v) for v in lor],
        "sech2_slopes": [float(v) for v in sec],
        "lorentz_mean_slope": lor_mean,
        "sech2_mean_slope": sec_mean,
        "lorentz_relative_spread": lor_spread,
        "sech2_relative_spread": sec_spread,
        "absolute_prediction": ABS_PREDICTION,
        "convergence_relative_change": float(conv),
        "prior_run": "results/pf4-005-analyticity.json",
        "reading": "each cell is placed at a declared adiabaticity "
                   "so the widths are compared in one dynamical "
                   "regime, and the exponent in that variable is "
                   "predicted to be minus two with no free "
                   "parameter if the field's nearest singularity "
                   "fixes it"}
    record["items"] = {k: bool(v) for k, v in items.items()}
    record["findings"] = findings
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items)}
    record["declared"] = {
        "E": E_FIELD, "kappa_grid": KAPPA_GRID, "L_grid": L_GRID,
        "dt": DT, "span_in_L": SPAN, "r2_bar": R2_BAR,
        "universality_tolerance": UNIV_TOL,
        "absolute_tolerance": ABS_TOL,
        "absolute_prediction": ABS_PREDICTION,
        "convergence_tolerance": CONV_TOL,
        "profiles": {"sech2": "tilt tanh, nearest singularity a "
                              "simple pole at pi over two times L",
                     "lorentz": "tilt arctangent, nearest "
                                "singularity a logarithmic branch "
                                "point at L"},
        "named_error_of_the_prior_run":
            "the velocity grid was declared in absolute velocity, "
            "so different widths were compared in different "
            "dynamical regimes and partly outside the adiabatic "
            "regime where the exponential form is asymptotic"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "pf4-005b-analyticity.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("lorentz slopes", lor, "spread", lor_spread)
    print("sech2 slopes", sec, "spread", sec_spread)
    print("convergence", conv)
    print("items", items, "findings", findings)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
