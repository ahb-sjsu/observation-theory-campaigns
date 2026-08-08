#!/usr/bin/env python3
"""PF-7c: the Bell ceiling on the sealed PF4-009 dynamics.

Bars in experiments/PF7C-BELL-DECLARATION.md. Inherits PREREG-PF4-009's
non-claims unchanged: nothing here is a claim about quantum field theory or
about any physical process.

The hidden variable is HARVESTED, not posited. It is the exit phase of the
oscillator, phi = atan2(pu/OMEGA_U, u - u_star), taken from the sealed
Gudermannian trajectories, so its measure is whatever the family produces.

D1 gates the run on that measure actually varying. PF4-009's result is that
per-crossing transfer is exponentially suppressed, so a near point-mass phase is
a live possibility, and a degenerate hidden variable would make the Bell
question empty rather than answered.
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

import pf4_009_run as R  # noqa: E402
import pf4_pilot as pilot  # noqa: E402
from pf4_005_analyticity import E_FIELD, equilibrium, potential  # noqa: E402
from projection_fold import canonical_sha256  # noqa: E402

SEED = 20260808
KAPPA_LO, KAPPA_HI = R.KAPPA_GRID[0], R.KAPPA_GRID[-1]
N_SAMP = 1024
N_DRAW = 200000
N_ANG = 37
MISPAIR_GRID = (0.0, 0.1, 0.25, 0.4)
ZIGZAG = 0.35
DETECTOR_SHARP = 3.0
D1_CIRCVAR_BAR = 0.05
D4_TOL = 0.01
D5_MIN_CELLS = 4
D6_BAR = 0.01
D8_BAR = 1e-12


def harvest_cell(l_s, p_values, dt=R.DT, span=R.SPAN, shift=0.0, profile="gudermann"):
    """Twin of pf4_009_run.run_cell that also returns the exit oscillator state.

    Verified against the official run_cell by D8 on the sealed six-kappa
    manifest; the integrator body is identical.
    """
    p = np.array(p_values, dtype=float)
    n = p.size
    t0 = -span * l_s + shift
    t = np.full(n, t0)
    pt = p.copy()
    s0, _ = R.tilt_and_force(np.array([t0 - shift]), l_s, profile)
    u = np.full(n, float(equilibrium(s0[0], l_s)))
    pu = np.zeros(n)

    def rhs(t_, pt_, u_, pu_):
        s, f = R.tilt_and_force(t_ - shift, l_s, profile)
        return (pt_,
                -pilot.G * E_FIELD * u_ * f,
                pu_,
                -pilot.OMEGA_U ** 2 * u_ - pilot.LAM * u_ ** 3
                - pilot.G * E_FIELD * l_s * s)

    t_end = span * l_s + shift
    steps = int(math.ceil((2.0 * span * l_s) / (dt * p.min()))) + 2
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
        t = np.where(live, t + dt / 6 * (d1[0] + 2 * d2[0] + 2 * d3[0] + d4[0]), t)
        pt = np.where(live, pt + dt / 6 * (d1[1] + 2 * d2[1] + 2 * d3[1] + d4[1]), pt)
        u = np.where(live, u + dt / 6 * (d1[2] + 2 * d2[2] + 2 * d3[2] + d4[2]), u)
        pu = np.where(live, pu + dt / 6 * (d1[3] + 2 * d2[3] + 2 * d3[3] + d4[3]), pu)
    s_end, _ = R.tilt_and_force(t - shift, l_s, profile)
    u_star = equilibrium(s_end, l_s)
    e_res = (0.5 * pu ** 2 + potential(u, s_end, l_s) - potential(u_star, s_end, l_s))
    phi = np.arctan2(pu / pilot.OMEGA_U, u - u_star)
    return e_res, phi


def circvar(phi):
    return float(1.0 - abs(np.mean(np.exp(1j * np.asarray(phi)))))


def chsh(E):
    return abs(E[(0, 0)] + E[(0, 1)] + E[(1, 0)] - E[(1, 1)])


def arm(phi, rng, kind, angA, angB, sharp=None, mispair=0.0, zigzag=0.0):
    """Circle-valued source. A = sign(cos(phi-a)); B = -sign(cos(phi-b))."""
    E_all, E_ps, marg, eff = {}, {}, {}, {}
    base = rng.integers(0, len(phi), N_DRAW)
    flip = rng.random(N_DRAW) < mispair if mispair > 0 else None
    blind = rng.random(N_DRAW) < zigzag if zigzag > 0 else None
    for x in (0, 1):
        for y in (0, 1):
            if kind == "C2":                       # measurement dependence
                wt = np.exp(2.0 * np.cos(phi - angA[x]) * np.cos(phi - angB[y]))
                wt /= wt.sum()
                idx = rng.choice(len(phi), N_DRAW, p=wt)
            else:
                idx = base
            L = np.asarray(phi)[idx]
            if kind == "C0":                       # PR box
                a = rng.integers(0, 2, N_DRAW)
                b = (a ^ (x * y)).astype(int)
                A, B = 1.0 - 2.0 * a, 1.0 - 2.0 * b
            else:
                sa = np.cos(L - angA[x])
                if kind == "C3":                   # locality broken
                    sa = sa + 0.45 * np.cos(L - angB[y])
                A = np.where(sa >= 0, 1.0, -1.0)
                B = np.where(np.cos(L - angB[y]) >= 0, -1.0, 1.0)
                if flip is not None:               # same-sign charge miscount
                    B = np.where(flip, -B, B)
                if sharp is not None:
                    eA = 1.0 / (1.0 + np.exp(-sharp * np.cos(L - angA[x])))
                    eB = 1.0 / (1.0 + np.exp(-sharp * np.cos(L - angB[y])))
                    A = np.where(rng.random(N_DRAW) < eA, A, 0.0)
                    B = np.where(rng.random(N_DRAW) < eB, B, 0.0)
                if blind is not None:
                    B = np.where(blind, 0.0, B)
            E_all[(x, y)] = float((A * B).mean())
            both = (A != 0) & (B != 0)
            eff[(x, y)] = float(both.mean())
            E_ps[(x, y)] = float((A[both] * B[both]).mean()) if both.sum() > 50 else 0.0
            marg[(x, y)] = (float(A.mean()), float(B.mean()))
    ns = max(max(abs(marg[(x, 0)][0] - marg[(x, 1)][0]) for x in (0, 1)),
             max(abs(marg[(0, y)][1] - marg[(1, y)][1]) for y in (0, 1)))
    return dict(kind=kind, S_all_counted=chsh(E_all), S_postselected=chsh(E_ps),
                no_signalling_residual=float(ns),
                eff_mean=float(np.mean(list(eff.values()))))


def angular(phi, rng, n_draw):
    L = np.asarray(phi)[rng.integers(0, len(phi), n_draw)]
    ths = np.linspace(0.0, np.pi, N_ANG)
    E = np.array([float((np.where(np.cos(L) >= 0, 1.0, -1.0)
                         * np.where(np.cos(L - t) >= 0, -1.0, 1.0)).mean())
                  for t in ths])
    saw = -(1.0 - 2.0 * ths / np.pi)
    qm = -np.cos(ths)
    scale = float(np.dot(E, saw) / max(np.dot(saw, saw), 1e-12))
    return dict(thetas=ths.tolist(), E=E.tolist(), E_at_zero=float(E[0]),
                fitted_scale=scale,
                rms_vs_scaled_sawtooth=float(np.sqrt(np.mean((E - scale * saw) ** 2))),
                rms_vs_quantum=float(np.sqrt(np.mean((E - qm) ** 2))),
                max_gap_vs_quantum=float(np.abs(E - qm).max()))


def main() -> int:
    rng = np.random.default_rng(SEED)
    tol = 4.0 / np.sqrt(N_DRAW)
    print("PF-7c Bell ceiling on the sealed PF4-009 dynamics")
    print("hidden variable is HARVESTED; D1 gates on it actually varying\n", flush=True)

    # ---- D8 dynamics twin, on the sealed six-kappa manifest
    twin_dev = 0.0
    for l_s in R.L_GRID:
        a = R.POLE_DISTANCE * l_s
        pv = [pilot.OMEGA_U * a / k for k in R.KAPPA_GRID]
        off, _, _ = R.run_cell("gudermann", l_s, pv)
        tw, _ = harvest_cell(l_s, pv)
        twin_dev = max(twin_dev, float(np.max(np.abs(off - tw))))
    print(f"D8 dynamics twin worst deviation {twin_dev:.3e}", flush=True)

    # ---- harvest the fold's own measure
    per_width, phis = {}, []
    for l_s in R.L_GRID:
        a = R.POLE_DISTANCE * l_s
        ks = rng.uniform(KAPPA_LO, KAPPA_HI, N_SAMP)
        pv = [pilot.OMEGA_U * a / k for k in ks]
        e_res, phi = harvest_cell(l_s, pv)
        per_width[l_s] = dict(circvar=circvar(phi),
                              e_res_median=float(np.median(e_res)),
                              e_res_max=float(np.max(e_res)))
        phis.append(phi)
        print(f"  L={l_s}  circvar={per_width[l_s]['circvar']:.4f}  "
              f"median e_res={per_width[l_s]['e_res_median']:.3e}", flush=True)
    pooled = np.concatenate(phis)
    cv_pooled = circvar(pooled)
    print(f"pooled circular variance {cv_pooled:.4f}  (D1 bar {D1_CIRCVAR_BAR})\n",
          flush=True)

    d1 = bool(cv_pooled >= D1_CIRCVAR_BAR
              and min(v["circvar"] for v in per_width.values()) >= D1_CIRCVAR_BAR)

    cells = {f"L{l_s}": p for l_s, p in zip(R.L_GRID, phis)}
    cells["pooled"] = pooled
    angA = {0: 0.0, 1: np.pi / 2}
    angB = {0: np.pi / 4, 1: -np.pi / 4}

    p0, pr, prem, blind, ang, mis = [], [], [], [], [], []
    for name, ph in cells.items():
        p0.append(dict(cell=name, **arm(ph, rng, "P0", angA, angB)))
        pr.append(dict(cell=name, **arm(ph, rng, "C0", angA, angB)))
        for k, sh in (("C1", DETECTOR_SHARP), ("C2", None), ("C3", None)):
            prem.append(dict(cell=name, **arm(ph, rng, k, angA, angB, sharp=sh)))
        blind.append(dict(cell=name, **arm(ph, rng, "P0", angA, angB,
                                           sharp=DETECTOR_SHARP, zigzag=ZIGZAG)))
        ang.append(dict(cell=name, **angular(ph, rng, N_DRAW // 4)))
        print(f"  {name:8s} P0={p0[-1]['S_all_counted']:.4f} "
              f"PR={pr[-1]['S_all_counted']:.3f} "
              f"saw<qm={ang[-1]['rms_vs_scaled_sawtooth'] < ang[-1]['rms_vs_quantum']} "
              f"gap_qm={ang[-1]['max_gap_vs_quantum']:.3f}", flush=True)

    # ---- D4 mispairing, the falsifiable conservation bar.
    # A fraction m of events carry same-sign rather than opposite-sign charge,
    # as a 1->3 zigzag miscount would produce, and E(0) must fall as -(1-2m).
    for m in MISPAIR_GRID:
        idx = rng.integers(0, len(pooled), N_DRAW)
        L = pooled[idx]
        A = np.where(np.cos(L) >= 0, 1.0, -1.0)
        B = np.where(np.cos(L) >= 0, -1.0, 1.0)
        flip = rng.random(N_DRAW) < m
        B = np.where(flip, -B, B)
        meas = float((A * B).mean())
        mis.append(dict(mispair=m, predicted_E0=-(1.0 - 2.0 * m), measured_E0=meas,
                        deviation=abs(meas + (1.0 - 2.0 * m))))
        print(f"  mispair m={m:.2f} predicted {-(1.0-2.0*m):+.3f} "
              f"measured {meas:+.4f}", flush=True)

    s0 = np.array([r["S_all_counted"] for r in p0])
    ns0 = np.array([r["no_signalling_residual"] for r in p0])
    s_pr = np.array([r["S_all_counted"] for r in pr])
    e0 = np.array([a["E_at_zero"] for a in ang])
    saw_wins = int(sum(a["rms_vs_scaled_sawtooth"] < a["rms_vs_quantum"] for a in ang))
    gap = np.array([a["max_gap_vs_quantum"] for a in ang])
    b_all = np.array([r["S_all_counted"] for r in blind])
    b_ps = np.array([r["S_postselected"] for r in blind])

    bars = {
        "D0_prbox_every_cell": bool(s_pr.min() > 2.0),
        "D1_measure_varies_GATE": d1,
        "D2_ceiling_code_check": bool(s0.max() <= 2.0 + 3.0 * tol),
        "D3_matched_setting_code_check": bool(np.abs(e0).min() >= 0.99),
        "D4_mispairing_prediction": bool(all(x["deviation"] <= D4_TOL for x in mis)),
        "D5_scaled_sawtooth_beats_quantum": bool(saw_wins >= D5_MIN_CELLS),
        "D6_no_signalling": bool(ns0.max() <= D6_BAR),
        "D7_blind_consumer": bool(b_ps.max() > 2.0 and b_all.max() <= 2.0 + 3.0 * tol),
        "D8_dynamics_twin": bool(twin_dev <= D8_BAR),
    }
    verdict = "PASS" if all(bars.values()) else "FAIL"
    if not bars["D1_measure_varies_GATE"]:
        verdict = "VOID_MEASURE_DEGENERATE"
    elif not bars["D0_prbox_every_cell"]:
        verdict = "VOID_INSTRUMENT_NOT_LIVE"

    record = {
        "schema": "pf7c-bell-dynamics-v1",
        "declaration": "experiments/PF7C-BELL-DECLARATION.md",
        "inherits_nonclaims_from": "PREREG-PF4-009",
        "source": "harvested exit phase of the sealed gudermann trajectories",
        "note_on_code_checks": "D2, D3 and D6 are code checks; D1, D4, D5, D7 carry the run",
        "per_width": {str(k): v for k, v in per_width.items()},
        "pooled_circvar": cv_pooled,
        "p0": p0, "prbox": pr, "premise_controls": prem,
        "blind_consumer": blind, "angular": ang, "mispairing": mis,
        "summary": {
            "P0_S_max": float(s0.max()), "PR_S_min": float(s_pr.min()),
            "scaled_sawtooth_wins": saw_wins, "cells": len(ang),
            "max_gap_vs_quantum": {"min": float(gap.min()),
                                   "median": float(np.median(gap)),
                                   "max": float(gap.max())},
            "blind_S_all_max": float(b_all.max()),
            "blind_S_postselected_max": float(b_ps.max()),
            "no_signalling_max": float(ns0.max()),
            "twin_deviation": twin_dev, "finite_tolerance": float(tol)},
        "bars": bars,
        "verdict": {"value": verdict, "computed_from": sorted(bars)},
        "declared": {"seed": SEED, "profile": "gudermann", "L_grid": R.L_GRID,
                     "kappa_range": [KAPPA_LO, KAPPA_HI], "n_samp": N_SAMP,
                     "dt": R.DT, "span": R.SPAN, "n_draw": N_DRAW, "n_ang": N_ANG,
                     "mispair_grid": list(MISPAIR_GRID), "zigzag": ZIGZAG,
                     "detector_sharp": DETECTOR_SHARP,
                     "D1_circvar_bar": D1_CIRCVAR_BAR, "D4_tol": D4_TOL,
                     "D5_min_cells": D5_MIN_CELLS, "D6_bar": D6_BAR, "D8_bar": D8_BAR},
        "runtime": {"generated_utc": datetime.now(timezone.utc).isoformat(),
                    "python": sys.version, "numpy": np.__version__,
                    "platform": platform.platform(), "hostname": platform.node(),
                    "code_commit": os.environ.get("CODE_COMMIT", "unknown")},
    }
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" / "pf7c-bell-dynamics.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")

    print("\n" + "=" * 68)
    for k, v in bars.items():
        print(f"  {k:36s} {'PASS' if v else 'FAIL'}")
    print("=" * 68)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
