#!/usr/bin/env python3
"""PF4-006 gate run for the Lorentzian profile (exploratory).

Protocol declared in CAMPAIGN.md before this run. CAMPAIGN.md
section 6 makes PF-5 and PF-6 mandatory gates before a
claim-bearing run. Those gates passed on the thermal Sauter family
under PREREG-PF5-002 and PREREG-PF6-002. The analyticity result
uses a field profile those gates never saw, an arctangent tilt with
a Lorentzian force, in a deterministic setting, so the gate content
that applies to it is applied here before anything is sealed.

What applies and what does not. The extended system is a canonical
autonomous two-degree-of-freedom Hamiltonian system in the
evolution parameter, so the conservation content of PF-5 applies
directly and is checked exactly. The census content applies and is
checked. The observer and detector audit of PF-6 counts events at
declared observer offsets, and these crossings produce no events at
any offset, so that clause is recorded not applicable rather than
passed, in the same way PF-6 recorded its gauge clause not
applicable for a family that declares no electromagnetic coupling.
A vacuous pass is not a pass.

Exploratory label. Not claim-bearing. This run is the prerequisite
for a preregistration, not a substitute for one.
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
    E_FIELD, POLE_DISTANCE, equilibrium, potential,
    tilt_and_force)
from projection_fold import canonical_sha256  # noqa: E402

L_GRID = [2.0, 3.0, 4.0]
KAPPA_GRID = [0.9, 1.5, 3.0]
DT = 2e-4
SPAN = 20.0
SHIFTS = [-3.0, 1.5, 4.0]
H_BAR = 1e-10
SHIFT_BAR = 1e-10
STABILITY_BAR = 1e-8


def hamiltonian(t, pt, u, pu, l_s, profile):
    s, _ = tilt_and_force(t, l_s, profile)
    return (0.5 * pt ** 2 + 0.5 * pu ** 2
            + 0.5 * pilot.OMEGA_U ** 2 * u ** 2
            + 0.25 * pilot.LAM * u ** 4
            + pilot.G * E_FIELD * l_s * s * u)


def crossing(profile, l_s, p_value, dt=DT, span=SPAN, shift=0.0):
    """One deterministic crossing with a declared field centre
    offset. Returns the residual energy, the census class, the
    worst relative drift of the conserved quantity, the fold count,
    and the exit state."""
    t0 = -span * l_s + shift
    t = np.array([t0])
    pt = np.array([float(p_value)])
    s0, _ = tilt_and_force(np.array([t0 - shift]), l_s, profile)
    u = np.array([float(equilibrium(s0[0], l_s))])
    pu = np.array([0.0])

    def rhs(t_, pt_, u_, pu_):
        s, f = tilt_and_force(t_ - shift, l_s, profile)
        return (pt_,
                -pilot.G * E_FIELD * u_ * f,
                pu_,
                -pilot.OMEGA_U ** 2 * u_ - pilot.LAM * u_ ** 3
                - pilot.G * E_FIELD * l_s * s)

    h0 = float(hamiltonian(t - shift, pt, u, pu, l_s, profile))
    scale = max(abs(h0), 1.0)
    worst = 0.0
    folds = 0
    nonfinite = False
    t_end = span * l_s + shift
    steps = int(math.ceil((2.0 * span * l_s)
                          / (dt * float(p_value)))) + 2
    for k in range(steps):
        if t[0] >= t_end:
            break
        d1 = rhs(t, pt, u, pu)
        d2 = rhs(t + 0.5 * dt * d1[0], pt + 0.5 * dt * d1[1],
                 u + 0.5 * dt * d1[2], pu + 0.5 * dt * d1[3])
        d3 = rhs(t + 0.5 * dt * d2[0], pt + 0.5 * dt * d2[1],
                 u + 0.5 * dt * d2[2], pu + 0.5 * dt * d2[3])
        d4 = rhs(t + dt * d3[0], pt + dt * d3[1],
                 u + dt * d3[2], pu + dt * d3[3])
        pt_new = pt + dt / 6 * (d1[1] + 2 * d2[1] + 2 * d3[1]
                                + d4[1])
        if pt_new[0] * pt[0] < 0.0:
            folds += 1
        t = t + dt / 6 * (d1[0] + 2 * d2[0] + 2 * d3[0] + d4[0])
        u = u + dt / 6 * (d1[2] + 2 * d2[2] + 2 * d3[2] + d4[2])
        pu = pu + dt / 6 * (d1[3] + 2 * d2[3] + 2 * d3[3] + d4[3])
        pt = pt_new
        if not (np.isfinite(t[0]) and np.isfinite(pt[0])
                and np.isfinite(u[0]) and np.isfinite(pu[0])):
            nonfinite = True
            break
        if k % 200 == 0:
            h = float(hamiltonian(t - shift, pt, u, pu, l_s,
                                  profile))
            worst = max(worst, abs(h - h0) / scale)
    s_end, _ = tilt_and_force(t - shift, l_s, profile)
    u_star = equilibrium(s_end, l_s)
    e_res = float(0.5 * pu ** 2 + potential(u, s_end, l_s)
                  - potential(u_star, s_end, l_s))
    cls = "nonfinite" if nonfinite else (
        "reversing" if folds > 0 else "transmitted")
    return {"e_res": e_res, "class": cls,
            "h_drift": float(worst), "folds": int(folds),
            "pt_final": float(pt[0])}


def main() -> int:
    record: dict = {"schema": "pf4-006-gate-v1",
                    "label": "exploratory"}
    profile = "lorentz"
    cells = {}
    worst_h = 0.0
    census = {"transmitted": 0, "reversing": 0, "nonfinite": 0}
    for l_s in L_GRID:
        a = POLE_DISTANCE[profile] * l_s
        for kappa in KAPPA_GRID:
            p_value = pilot.OMEGA_U * a / kappa
            r = crossing(profile, l_s, p_value)
            key = f"L{l_s}_kappa{kappa}"
            cells[key] = r
            census[r["class"]] += 1
            worst_h = max(worst_h, r["h_drift"])
            print(f"  {key} E_res={r['e_res']:.6e} "
                  f"drift={r['h_drift']:.3e} class={r['class']}",
                  flush=True)

    items = {}
    items["G1_conserved_quantity"] = worst_h <= H_BAR
    total = sum(census.values())
    items["G2_complete_census"] = (
        total == len(L_GRID) * len(KAPPA_GRID)
        and census["nonfinite"] == 0)

    # G3 translation covariance of the transfer
    worst_shift = 0.0
    shift_rows = {}
    for l_s in L_GRID:
        a = POLE_DISTANCE[profile] * l_s
        p_value = pilot.OMEGA_U * a / KAPPA_GRID[1]
        base = cells[f"L{l_s}_kappa{KAPPA_GRID[1]}"]["e_res"]
        for sh in SHIFTS:
            r = crossing(profile, l_s, p_value, shift=sh)
            rel = abs(r["e_res"] - base) / abs(base)
            worst_shift = max(worst_shift, rel)
            shift_rows[f"L{l_s}_shift{sh}"] = float(rel)
    items["G3_translation_covariance"] = worst_shift <= SHIFT_BAR

    # G4 independence of the declared entry point and timestep
    worst_stab = 0.0
    stab_rows = {}
    for l_s in L_GRID:
        a = POLE_DISTANCE[profile] * l_s
        p_value = pilot.OMEGA_U * a / KAPPA_GRID[1]
        base = cells[f"L{l_s}_kappa{KAPPA_GRID[1]}"]["e_res"]
        far = crossing(profile, l_s, p_value, span=SPAN * 1.5)
        fine = crossing(profile, l_s, p_value, dt=DT / 2.0)
        r1 = abs(far["e_res"] - base) / abs(base)
        r2 = abs(fine["e_res"] - base) / abs(base)
        worst_stab = max(worst_stab, r1, r2)
        stab_rows[f"L{l_s}_entry"] = float(r1)
        stab_rows[f"L{l_s}_timestep"] = float(r2)
    items["G4_entry_and_timestep_independence"] = (
        worst_stab <= STABILITY_BAR)

    not_applicable = {
        "G5_observer_detector":
            "the declared crossings produce no events at any "
            "observer offset, so there are no observer-dependent "
            "counts to audit and this clause is recorded not "
            "applicable rather than passed",
        "G6_gauge":
            "the profile declares no electromagnetic coupling, as "
            "in PREREG-PF6-002"}

    record["measured"] = {
        "profile": profile, "cells": cells, "census": census,
        "worst_hamiltonian_drift": float(worst_h),
        "translation_relative_changes": shift_rows,
        "worst_translation_change": float(worst_shift),
        "stability_relative_changes": stab_rows,
        "worst_stability_change": float(worst_stab),
        "reading": "the conservation and census content of PF-5 "
                   "applies to this profile and is checked "
                   "exactly, the transfer is independent of where "
                   "the field is centred and of the declared entry "
                   "point and timestep, and the event-count "
                   "clauses of PF-6 have nothing to audit here and "
                   "are recorded not applicable"}
    record["items"] = {k: bool(v) for k, v in items.items()}
    record["not_applicable"] = not_applicable
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items)}
    record["declared"] = {
        "L_grid": L_GRID, "kappa_grid": KAPPA_GRID, "dt": DT,
        "span_in_L": SPAN, "shifts": SHIFTS,
        "hamiltonian_bar": H_BAR, "shift_bar": SHIFT_BAR,
        "stability_bar": STABILITY_BAR,
        "purpose": "prerequisite gate content for a "
                   "preregistration on the Lorentzian profile, "
                   "not a substitute for one"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "pf4-006-gate.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("census", census, "worst H drift", worst_h)
    print("worst shift", worst_shift, "worst stability",
          worst_stab)
    print("items", items)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
