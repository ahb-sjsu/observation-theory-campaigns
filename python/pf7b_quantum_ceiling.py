#!/usr/bin/env python3
"""PF-7b quantum-structure ceiling test, corrected.

Protocol declared in PF7-CEILING.md before this run, correcting
three named errors of PF-7. The sweep range now reaches the
asymptotic regime, the delay grid is uniform in the square of the
half-delay because the Stueckelberg phase is quadratic in delay so
the oscillation is a chirp, and the classical field and delay range
are bound from committed probes (results/pf7-classical-probe.json
and results/pf7-classical-probe2.json) so the classical arm carries
the variation its finding is about.

Quantum arm, an exactly integrable two-level model swept through an
avoided crossing twice, the Landau-Zener-Stueckelberg construction.
Classical arm, the pilot fold dynamics under a matched two-pulse
field with the same declared delay grid. Both curves are read by
the same declared oscillation statistic, the fraction of spectral
power at nonzero frequency.

Exploratory label. Failure of the classical arm caps the model as a
classical representation and does not touch the kinematic fold
theorem.
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

# quantum arm
DELTA = 0.30
SWEEP_V = 1.0
DT_Q = 2e-4
# uniform in the square of the half-delay, the phase variable
T_HALF_GRID = [round((16.0 + (100.0 - 16.0) * k / 31.0)
                     ** 0.5, 6) for k in range(32)]
# classical arm
E_FIELD = 0.675507688522339
P_GAP = 0.80
N_ENS = 2000
DT_C = 2e-3
SEED0 = 8_700_000
QUANTUM_OSC_BAR = 0.30
CLASSICAL_OSC_BAR = 0.15
RATIO_BAR = 3.0


def lz_single(v, delta, t_max):
    """One linear passage, returns final diabatic survival."""
    n = int(2 * t_max / DT_Q)
    c = np.array([1.0 + 0j, 0.0 + 0j])
    t = -t_max

    def ham(t_):
        return np.array([[0.5 * v * t_, 0.5 * delta],
                         [0.5 * delta, -0.5 * v * t_]],
                        dtype=complex)

    for _ in range(n):
        for h, dt_ in ((ham(t), DT_Q), ):
            k1 = -1j * (h @ c)
            k2 = -1j * (ham(t + 0.5 * dt_) @ (c + 0.5 * dt_ * k1))
            k3 = -1j * (ham(t + 0.5 * dt_) @ (c + 0.5 * dt_ * k2))
            k4 = -1j * (ham(t + dt_) @ (c + dt_ * k3))
            c = c + dt_ / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        t += DT_Q
    return c


def lz_double(v, delta, t_half, t_pad=6.0):
    """Two passages, epsilon(t) = v (|t| - t_half), crossings at
    |t| = t_half. Returns final state and worst norm deviation."""
    t_max = t_half + t_pad
    n = int(2 * t_max / DT_Q)
    c = np.array([1.0 + 0j, 0.0 + 0j])
    t = -t_max
    worst_norm = 0.0

    def ham(t_):
        eps = v * (abs(t_) - t_half)
        return np.array([[0.5 * eps, 0.5 * delta],
                         [0.5 * delta, -0.5 * eps]], dtype=complex)

    for _ in range(n):
        k1 = -1j * (ham(t) @ c)
        k2 = -1j * (ham(t + 0.5 * DT_Q) @ (c + 0.5 * DT_Q * k1))
        k3 = -1j * (ham(t + 0.5 * DT_Q) @ (c + 0.5 * DT_Q * k2))
        k4 = -1j * (ham(t + DT_Q) @ (c + DT_Q * k3))
        c = c + DT_Q / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        t += DT_Q
        worst_norm = max(worst_norm,
                         abs(float(np.vdot(c, c).real) - 1.0))
    return c, worst_norm


def classical_reversing_fraction(delay, seed):
    """Pilot fold dynamics under two Sauter pulses separated by the
    declared delay. Returns the reversing fraction and the maximum
    number of reversing members inside a declared narrow cell."""
    rng = np.random.RandomState(seed)
    n = N_ENS
    l_s = pilot.SAUTER_L
    t0 = -4.0 * l_s - 0.5 * delay
    t = np.full(n, t0)
    u_star = pilot.shifted_equilibrium(E_FIELD, t0)
    u = u_star + rng.standard_normal(n) * math.sqrt(pilot.T_BATH) \
        / pilot.OMEGA_U
    pu = rng.standard_normal(n) * math.sqrt(pilot.T_BATH)
    pt = np.full(n, P_GAP)
    alive = np.ones(n, dtype=bool)
    reversed_flag = np.zeros(n, dtype=bool)
    t_exit = 4.0 * l_s + 0.5 * delay
    c1, c2 = -0.5 * delay, 0.5 * delay
    steps = int((t_exit - t0) / (DT_C * 0.5 * P_GAP)) + 1

    def forces(t_, u_):
        s1 = np.cosh(np.clip((t_ - c1) / l_s, -30, 30)) ** -2
        s2 = np.cosh(np.clip((t_ - c2) / l_s, -30, 30)) ** -2
        ft = -pilot.G * E_FIELD * (s1 + s2) * u_
        tilt = (np.tanh((t_ - c1) / l_s) + np.tanh((t_ - c2) / l_s))
        fu = (-pilot.OMEGA_U ** 2 * u_ - pilot.LAM * u_ ** 3
              - pilot.G * E_FIELD * l_s * tilt)
        return ft, fu

    for _ in range(steps):
        if not alive.any():
            break
        ft, fu = forces(t, u)
        pt_h = np.where(alive, pt + 0.5 * DT_C * ft, pt)
        pu_h = np.where(alive, pu + 0.5 * DT_C * fu, pu)
        t = np.where(alive, t + DT_C * pt_h, t)
        u = np.where(alive, u + DT_C * pu_h, u)
        ft, fu = forces(t, u)
        pt = np.where(alive, pt_h + 0.5 * DT_C * ft, pt)
        pu = np.where(alive, pu_h + 0.5 * DT_C * fu, pu)
        bad = alive & ~(np.isfinite(t) & np.isfinite(pt))
        alive &= ~bad
        rev = alive & (pt <= 0.0)
        reversed_flag |= rev
        alive &= ~rev
        out = alive & (t >= t_exit)
        alive &= ~out
    return float(reversed_flag.mean()), int(reversed_flag.sum())


def osc_power_ratio(curve):
    """Fraction of spectral power at nonzero frequency."""
    y = np.asarray(curve, dtype=float)
    y = y - y.mean()
    if np.allclose(y, 0.0):
        return 0.0
    p = np.abs(np.fft.rfft(y)) ** 2
    tot = float(p.sum())
    return float(p[1:].max() / tot) if tot > 0 else 0.0


def main() -> int:
    record: dict = {"schema": "pf7b-quantum-ceiling-v1",
                    "label": "exploratory"}
    items = {}

    # Q1 instrument, single passage against the closed form
    c = lz_single(SWEEP_V, DELTA, 120.0)
    p_dia = float(abs(c[0]) ** 2)
    gamma = DELTA ** 2 / (4.0 * SWEEP_V)
    p_closed = math.exp(-2.0 * math.pi * gamma)
    dev_q1 = abs(p_dia - p_closed)
    items["Q1_landau_zener_closed_form"] = dev_q1 <= 2e-3

    # Q2 quantum double passage, interference against delay
    q_curve = []
    worst_norm = 0.0
    for th in T_HALF_GRID:
        cf, wn = lz_double(SWEEP_V, DELTA, th)
        q_curve.append(float(abs(cf[1]) ** 2))
        worst_norm = max(worst_norm, wn)
        print(f"  quantum t_half={th} P_exc={q_curve[-1]:.6f}",
              flush=True)
    q_ratio = osc_power_ratio(q_curve)
    items["Q2_quantum_interferes"] = q_ratio >= QUANTUM_OSC_BAR

    # Q4 exclusion, the mode holds at most one excitation exactly
    items["Q4_norm_conservation"] = worst_norm <= 1e-10

    # Q3 the ceiling, classical arm on the matched delay grid
    c_curve = []
    c_counts = []
    for i, th in enumerate(T_HALF_GRID):
        frac, cnt = classical_reversing_fraction(2.0 * th,
                                                 SEED0 + i)
        c_curve.append(frac)
        c_counts.append(cnt)
        print(f"  classical delay={2 * th} frac={frac:.5f}",
              flush=True)
    c_ratio = osc_power_ratio(c_curve)
    c_arr = np.array(c_curve)
    dynamic = bool(c_arr.min() > 0.02 and c_arr.max() < 0.98)
    findings = {
        "Q3_classical_shows_no_interference":
            bool(dynamic and c_ratio <= CLASSICAL_OSC_BAR
                 and q_ratio / max(c_ratio, 1e-12) >= RATIO_BAR),
        "Q3_anti_vacuity_classical_arm_varies": dynamic}

    record["measured"] = {
        "q1_probability_measured": p_dia,
        "q1_probability_closed_form": p_closed,
        "q1_deviation": dev_q1,
        "quantum_curve": q_curve,
        "quantum_osc_power_ratio": q_ratio,
        "quantum_worst_norm_dev": worst_norm,
        "classical_curve": c_curve,
        "classical_reversing_counts": c_counts,
        "classical_osc_power_ratio": c_ratio,
        "classical_fraction_min": float(min(c_curve)),
        "classical_fraction_max": float(max(c_curve)),
        "quantum_over_classical_ratio":
            float(q_ratio / max(c_ratio, 1e-12)),
        "delay_grid": [2.0 * t for t in T_HALF_GRID],
        "reading": "the quantum mode accumulates a relative phase "
                   "between passages and the classical ensemble "
                   "has no phase to accumulate, so the declared "
                   "interference statistic separates them"}
    record["items"] = {k: bool(v) for k, v in items.items()}
    record["findings"] = findings
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {
        "value": verdict, "computed_from": sorted(items),
        "note": "Q3 is the ceiling measurement, recorded "
                "individually, either outcome a result"}
    record["declared"] = {
        "delta": DELTA, "sweep_v": SWEEP_V, "dt_quantum": DT_Q,
        "t_half_grid": T_HALF_GRID, "e_field": E_FIELD,
        "p_gap": P_GAP, "n_ensemble": N_ENS, "dt_classical": DT_C,
        "probe_records": ["results/pf7-classical-probe.json",
                          "results/pf7-classical-probe2.json"],
        "quantum_osc_bar": QUANTUM_OSC_BAR,
        "classical_osc_bar": CLASSICAL_OSC_BAR,
        "ratio_bar": RATIO_BAR}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "pf7b-quantum-ceiling.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("findings", findings)
    print("q_ratio", q_ratio, "c_ratio", c_ratio)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
