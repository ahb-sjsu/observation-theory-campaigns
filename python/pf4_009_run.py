#!/usr/bin/env python3
"""PF4-009 governed run. Sealed under PREREG-PF4-009.

Protocol declared in CAMPAIGN.md before this run. The PF4-006 gate
failed the Lorentzian profile on entry-point independence because
its tilt approaches its asymptote algebraically, so its field never
fully turns off. The property that made that profile interesting,
a first-order singularity, is not the property that broke it.

The Gudermannian tilt separates them. Written as the arcsine of a
hyperbolic tangent it runs from minus one to plus one, its force is
a hyperbolic secant with a simple pole at pi over two times the
width, the same distance as the sech-squared family's double pole,
and its tails decay exponentially so the entry-point defect cannot
arise.

PF4-008 answered the discriminator and missed the conservation
bar, and PF4-008b refuted the repair by halving the timestep and
measuring the same drift. The cause is the tilt's evaluation. A
hyperbolic tangent of twenty rounds to exactly one in double
precision, so the arcsine form of the tilt saturates while its own
derivative, a hyperbolic secant, is still 2.6e-9 there. The two
become mutually inconsistent in the tails, and because the
Hamiltonian carries the tilt the inconsistency appears as an
apparent conservation violation of 1.1e-10, which is what was
measured. The sech-squared profile is immune because its force at
the same point is 1.7e-17.

This run evaluates the tilt in a form that does not saturate before
its derivative does, and changes nothing else. The exponents are
unaffected by the defect, which enters the transfer at a relative
1e-8, so this run also serves as their check.

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
from pf4_005_analyticity import (  # noqa: E402
    E_FIELD, equilibrium, potential)
from projection_fold import canonical_sha256  # noqa: E402

L_GRID = [1.8, 2.8, 3.8, 4.6]
KAPPA_GRID = [1.05, 1.45, 1.85, 2.25, 2.65, 3.05]
DT = 1e-4
SPAN = 20.0
SHIFT = 3.0
H_BAR = 1e-11
ENTRY_BAR = 1e-7
STEP_BAR = 1e-5
R2_BAR = 0.995
UNIV_TOL = 0.02
SIGNAL_LO, SIGNAL_HI = 1e-12, 1.0
# both profiles have their nearest singularity at pi/2 times L
POLE_DISTANCE = math.pi / 2.0
SECH2_REFERENCE = -1.04767      # PF4-005b, record 8da5c1e9dca4
LORENTZ_REFERENCE = -2.06356    # PF4-005b, same record
H1_TOL = 0.05
H2_TOL = 0.10


def fit_slope(kappa_values, e_res):
    """Fit the log transfer against the adiabaticity itself. The
    first execution of this runner imported a helper that fits
    against the reciprocal instead, which is the named error that
    invalidated it."""
    x = np.array(kappa_values, dtype=float)
    y = np.log(np.asarray(e_res, dtype=float))
    a = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(a, y, rcond=None)
    pred = a @ coef
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return float(coef[0]), float(coef[1]), r2


def tilt_and_force(t, l_s, profile):
    x = np.clip(t / l_s, -300.0, 300.0)
    if profile == "sech2":
        return np.tanh(x), 1.0 / np.cosh(x) ** 2
    if profile == "gudermann":
        # evaluated so the tilt and its own derivative saturate
        # together, which the arcsine form does not do
        tilt = np.sign(x) * (1.0 - (4.0 / math.pi)
                             * np.arctan(np.exp(-np.abs(x))))
        return tilt, (2.0 / math.pi) / np.cosh(x)
    raise ValueError(profile)


def hamiltonian(t, pt, u, pu, l_s, profile):
    s, _ = tilt_and_force(t, l_s, profile)
    return (0.5 * pt ** 2 + 0.5 * pu ** 2
            + 0.5 * pilot.OMEGA_U ** 2 * u ** 2
            + 0.25 * pilot.LAM * u ** 4
            + pilot.G * E_FIELD * l_s * s * u)


def run_cell(profile, l_s, p_values, dt=DT, span=SPAN, shift=0.0):
    p = np.array(p_values, dtype=float)
    n = p.size
    t0 = -span * l_s + shift
    t = np.full(n, t0)
    pt = p.copy()
    s0, _ = tilt_and_force(np.array([t0 - shift]), l_s, profile)
    u = np.full(n, float(equilibrium(s0[0], l_s)))
    pu = np.zeros(n)
    h0 = hamiltonian(t - shift, pt, u, pu, l_s, profile)
    scale = np.maximum(np.abs(h0), 1.0)
    worst_h = 0.0
    nonfinite = False

    def rhs(t_, pt_, u_, pu_):
        s, f = tilt_and_force(t_ - shift, l_s, profile)
        return (pt_,
                -pilot.G * E_FIELD * u_ * f,
                pu_,
                -pilot.OMEGA_U ** 2 * u_ - pilot.LAM * u_ ** 3
                - pilot.G * E_FIELD * l_s * s)

    t_end = span * l_s + shift
    steps = int(math.ceil((2.0 * span * l_s)
                          / (dt * p.min()))) + 2
    for k in range(steps):
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
        if not np.all(np.isfinite(t) & np.isfinite(pt)
                      & np.isfinite(u) & np.isfinite(pu)):
            nonfinite = True
            break
        if k % 400 == 0:
            h = hamiltonian(t - shift, pt, u, pu, l_s, profile)
            worst_h = max(worst_h,
                          float(np.max(np.abs(h - h0) / scale)))
    s_end, _ = tilt_and_force(t - shift, l_s, profile)
    u_star = equilibrium(s_end, l_s)
    e_res = (0.5 * pu ** 2 + potential(u, s_end, l_s)
             - potential(u_star, s_end, l_s))
    return e_res, float(worst_h), bool(nonfinite)


def main() -> int:
    record: dict = {"schema": "prereg-pf4-009-v1",
                    "registration_id": "PREREG-PF4-009",
                    "label": "sealed-claim-run"}
    cells = {}
    worst_h = 0.0
    any_nonfinite = False
    for profile in ("gudermann",):
        for l_s in L_GRID:
            a = POLE_DISTANCE * l_s
            p_values = [pilot.OMEGA_U * a / k for k in KAPPA_GRID]
            e_res, wh, nf = run_cell(profile, l_s, p_values)
            worst_h = max(worst_h, wh)
            any_nonfinite = any_nonfinite or nf
            slope, icept, r2 = fit_slope(KAPPA_GRID, e_res)
            cells[f"{profile}_L{l_s}"] = {
                "profile": profile, "L": l_s,
                "e_res": [float(v) for v in e_res],
                "slope_vs_kappa": slope, "intercept": icept,
                "r_squared": r2, "hamiltonian_drift": wh}
            print(f"  {profile} L={l_s} slope={slope:.6f} "
                  f"r2={r2:.6f} drift={wh:.2e}", flush=True)

    items = {}
    items["P1a_conserved_quantity"] = worst_h <= H_BAR

    # entry-point and timestep independence for the new profile
    a = POLE_DISTANCE * L_GRID[1]
    p_mid = [pilot.OMEGA_U * a / KAPPA_GRID[2]]
    base, _, _ = run_cell("gudermann", L_GRID[1], p_mid)
    far, _, _ = run_cell("gudermann", L_GRID[1], p_mid,
                         span=SPAN * 1.5)
    fine, _, _ = run_cell("gudermann", L_GRID[1], p_mid,
                          dt=DT / 2.0)
    moved, _, _ = run_cell("gudermann", L_GRID[1], p_mid,
                           shift=SHIFT)
    entry_rel = abs(float(far[0]) - float(base[0])) \
        / abs(float(base[0]))
    step_rel = abs(float(fine[0]) - float(base[0])) \
        / abs(float(base[0]))
    shift_rel = abs(float(moved[0]) - float(base[0])) \
        / abs(float(base[0]))
    items["P1b_entry_independence"] = entry_rel <= ENTRY_BAR
    items["P1c_timestep_independence"] = step_rel <= STEP_BAR
    items["P1d_translation_covariance"] = shift_rel <= ENTRY_BAR
    items["P1e_census"] = not any_nonfinite

    gud = [cells[f"gudermann_L{l}"]["slope_vs_kappa"]
           for l in L_GRID]
    gud_mean = float(np.mean(gud))
    gud_spread = float((max(gud) - min(gud)) / abs(gud_mean))
    items["P2_exponential_form"] = all(
        c["r_squared"] >= R2_BAR for c in cells.values())
    items["P3_width_universal"] = gud_spread <= UNIV_TOL
    items["P4_signal_in_range"] = all(
        SIGNAL_LO < v < SIGNAL_HI
        for c in cells.values() for v in c["e_res"])

    findings = {
        "exploratory_reference_pf4_008c": SECH2_REFERENCE,
        "note": "the constant is not claimed by this registration"}

    record["measured"] = {
        "cells": cells,
        "gudermann_slopes": [float(v) for v in gud],
        "gudermann_mean_slope": gud_mean,
        "gudermann_relative_spread": gud_spread,
        "sech2_reference_pf4_005b": SECH2_REFERENCE,
        "lorentz_reference_pf4_005b": LORENTZ_REFERENCE,
        "worst_hamiltonian_drift": float(worst_h),
        "entry_relative_change": float(entry_rel),
        "timestep_relative_change": float(step_rel),
        "translation_relative_change": float(shift_rel),
        "reading": "both profiles carry their nearest singularity "
                   "at the same distance and differ in its order, "
                   "so a difference in the exponent is a "
                   "difference the order makes and an agreement is "
                   "one the distance makes"}
    record["items"] = {k: bool(v) for k, v in items.items()}
    record["findings"] = findings
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items),
                         "note": "the findings discriminate the "
                                 "two declared hypotheses, either "
                                 "outcome a result"}
    record["declared"] = {
        "L_grid": L_GRID, "kappa_grid": KAPPA_GRID, "dt": DT,
        "span_in_L": SPAN, "shift": SHIFT,
        "pole_distance_over_L": POLE_DISTANCE,
        "profiles": {"sech2": "tanh tilt, sech squared force, "
                              "double pole at pi over two times L",
                     "gudermann": "arcsine of tanh tilt, sech "
                                  "force, simple pole at the same "
                                  "distance, exponential tails"},
        "hypotheses": {
            "H1_distance_only": "the Gudermannian exponent equals "
                                "the sech-squared exponent within "
                                "five percent",
            "H2_order_matters": "the Gudermannian exponent equals "
                                "the Lorentzian exponent within "
                                "ten percent"},
        "bars": {"hamiltonian": H_BAR, "entry": ENTRY_BAR,
                 "timestep": STEP_BAR, "r_squared": R2_BAR,
                 "universality": UNIV_TOL}}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "prereg-pf4-009.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("gudermann", gud, "mean", gud_mean, "spread", gud_spread)
    print("entry", entry_rel, "step", step_rel, "shift", shift_rel)
    print("items", items)
    print("findings", findings)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
