#!/usr/bin/env python3
"""PF-3 replication of Land 2016 (arXiv:1604.01625), Section 3.

Transcribes the impulsive Coulomb scattering solution of classical
Stueckelberg-Horwitz-Piron electrodynamics and integrates the smoothed
pre-impulse dynamics to exhibit the pair event as a fold. Equation
numbers refer to the arXiv v1; the transcription map and guards are in
experiments/PF3-PROVENANCE.md. Exploratory label. No physics claim.
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

from projection_fold import canonical_sha256, classify_scalar_critical_point


def coupling_ge(lam: float, mass: float, strength: float, radius: float) -> float:
    """Source Eq. 64: g_e = (lambda/M) (Ze^2/4piR^2), strength = Ze^2/4pi."""
    return (lam / mass) * strength / radius**2


def impulse_system(tdot_in: float, v: float, rhat, ge: float):
    """Source Eq. 66 as printed: A vf = B vin - 2 c. Returns (A, rhs)."""
    rx, ry = rhat
    ax = 0.5 * ge * rx
    ay = 0.5 * ge * ry
    a = np.array([[1.0, ax, ay], [ax, 1.0, 0.0], [ay, 0.0, 1.0]])
    b = np.array([[1.0, -ax, 0.0], [-ax, 1.0, 0.0], [-ay, 0.0, 0.0]])
    vin = np.array([tdot_in, v * tdot_in, 0.0])
    rhs = b @ vin - 2.0 * np.array([0.0, ax, ay])
    return a, rhs


def final_velocity(tdot_in: float, v: float, rhat, ge: float) -> np.ndarray:
    """Source Eq. 67 closed form for (tdot_f, xdot_f, ydot_f)."""
    rx, ry = rhat
    d = 1.0 - 0.25 * ge**2
    term0 = np.array([tdot_in, v * tdot_in, 0.0])
    term1 = np.array([
        tdot_in * v * rx,
        (tdot_in + 1.0) * rx,
        (tdot_in + 1.0) * ry,
    ])
    term2 = np.array([
        tdot_in + 2.0,
        (rx**2 - ry**2) * v * tdot_in,
        2.0 * rx * ry * v * tdot_in,
    ])
    return (term0 - ge * term1 + 0.25 * ge**2 * term2) / d


def tdot_final(tdot_in: float, v: float, rhat_x: float, ge: float) -> float:
    """Source Eq. 76."""
    return (tdot_in * (1.0 - ge * v * rhat_x)
            + 0.25 * ge**2 * (tdot_in + 2.0)) / (1.0 - 0.25 * ge**2)


def rutherford_cot_half_angle(rhat) -> float:
    """Source Eq. 74 under the Eq. 72 constraint: cot(theta/2) = Ry/Rx."""
    return rhat[1] / rhat[0]


def hann_kernel(s: float, lam: float) -> float:
    if abs(s) >= lam:
        return 0.0
    return (1.0 + math.cos(math.pi * s / lam)) / (2.0 * lam)


def hann_kernel_prime(s: float, lam: float) -> float:
    if abs(s) >= lam:
        return 0.0
    return -math.pi * math.sin(math.pi * s / lam) / (2.0 * lam**2)


def integrate_smoothed(
    *,
    ge: float,
    v: float,
    rhat,
    radius: float = 1.0,
    lam: float = 0.02,
    mass: float = 1.0,
    tau_pad: float = 0.5,
    dt: float = 2e-5,
) -> dict:
    """Source Eqs. 59-62 with the delta kernel smoothed (raised cosine).

    Convention, following the source exactly: the delta collapse in
    source Eq. 61 evaluates the potential and its gradient at the fixed
    interaction point radius * rhat, which is why the source's
    kernel-derivative term integrates to exactly zero there. The first
    version of this bridge evaluated U along the moving trajectory
    instead; the kernel-derivative term then produces transient tdot
    excursions that scale like the inverse kernel width and cross zero
    even below threshold. That is a smoothing artifact, not a fold, and
    it is preserved as a finding in the provenance note. Here U and
    grad U are frozen at the interaction point, as the source's own
    derivation does; the kernel-derivative term still acts pointwise
    (its integral is exactly zero for the symmetric kernel) and its
    transient is reported as tdot_max.

    U = k/radius with k = ge * mass * radius^2 / lam so the coupling at
    the interaction distance equals the requested ge. RK4 fixed step;
    records the tdot path and locates smooth zero crossings with their
    classifier labels.
    """
    tdot_in = 1.0 / math.sqrt(1.0 - v * v)
    strength = ge * mass * radius**2 / lam
    rx, ry = rhat
    position1 = np.array([radius * rx, radius * ry])
    velocity_in = np.array([v * tdot_in, 0.0])
    u_pot = strength / radius
    grad_u = -strength * position1 / radius**3

    def acceleration(tau, state):
        t, tdot, x, xdot, y, ydot = state
        phi = hann_kernel(tau, lam)
        phi_p = hann_kernel_prime(tau, lam)
        sdot = np.array([xdot, ydot])
        ttdot = (lam / mass) * (
            float(sdot @ grad_u) * phi + (1.0 + 1.0 / tdot_in) * u_pot * phi_p
        )
        sddot = (lam / mass) * (tdot + 1.0) * grad_u * phi
        return np.array([tdot, ttdot, xdot, sddot[0], ydot, sddot[1]])

    tau0 = -(lam + tau_pad)
    start_pos = position1 + velocity_in * tau0
    state = np.array([
        tdot_in * tau0, tdot_in,
        start_pos[0], velocity_in[0],
        start_pos[1], velocity_in[1],
    ])
    n_steps = int(round(2.0 * (lam + tau_pad) / dt))
    taus = np.empty(n_steps + 1)
    tdots = np.empty(n_steps + 1)
    taus[0], tdots[0] = tau0, state[1]
    tau = tau0
    for k in range(1, n_steps + 1):
        k1 = acceleration(tau, state)
        k2 = acceleration(tau + dt / 2, state + dt / 2 * k1)
        k3 = acceleration(tau + dt / 2, state + dt / 2 * k2)
        k4 = acceleration(tau + dt, state + dt * k3)
        state = state + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        tau += dt
        taus[k], tdots[k] = tau, state[1]

    crossings = []
    hits = np.nonzero(tdots[:-1] * tdots[1:] < 0.0)[0]
    for idx in hits:
        alpha = tdots[idx] / (tdots[idx] - tdots[idx + 1])
        tau_c = taus[idx] + alpha * dt
        second = (tdots[idx + 1] - tdots[idx]) / dt
        crossings.append({
            "tau": float(tau_c),
            "tdot_second_derivative": float(second),
            "classification": classify_scalar_critical_point(
                0.0, second, second_tol=1e-6
            ),
        })

    return {
        "ge": ge, "v": v, "rhat": list(rhat), "lambda": lam, "dt": dt,
        "tdot_in": tdot_in,
        "tdot_final_ode": float(state[1]),
        "xdot_final_ode": [float(state[3]), float(state[5])],
        "tdot_final_impulse": tdot_final(tdot_in, v, rx, ge),
        "n_tdot_zero_crossings": len(crossings),
        "crossings": crossings,
        "tdot_min": float(tdots.min()),
        "tdot_max": float(tdots.max()),
    }


def main() -> int:
    grid = {
        "tdot_in_values": [1.0206207261596576, 1.0910894511799618,
                           1.2909944487358056],
        "v_values": [0.2, 0.4, 0.6],
        "rhat_values": [[0.8, 0.6], [0.6, 0.8], [0.96, 0.28]],
        "ge_values": [0.25, 0.5, 1.0, 1.5, 1.9, 2.1, 3.0, 5.0, 10.0, 50.0],
    }

    max_system_residual = 0.0
    max_component_mismatch = 0.0
    timelike_margins = []
    spacelike_cells = []
    threshold_ok = True
    for v in grid["v_values"]:
        tdot_in = 1.0 / math.sqrt(1.0 - v * v)
        for rhat in grid["rhat_values"]:
            for ge in grid["ge_values"]:
                a, rhs = impulse_system(tdot_in, v, rhat, ge)
                solved = np.linalg.solve(a, rhs)
                closed = final_velocity(tdot_in, v, rhat, ge)
                max_system_residual = max(
                    max_system_residual, float(np.max(np.abs(solved - closed)))
                )
                max_component_mismatch = max(
                    max_component_mismatch,
                    abs(closed[0] - tdot_final(tdot_in, v, rhat[0], ge)),
                )
                margin = closed[0]**2 - closed[1]**2 - closed[2]**2
                timelike_margins.append(margin)
                if margin <= 0.0:
                    spacelike_cells.append(
                        {"v": v, "rhat": rhat, "ge": ge,
                         "margin": float(margin)}
                    )
                if ge < 2.0 and closed[0] <= 0.0:
                    threshold_ok = False
                if ge > 2.0 and closed[0] >= 0.0:
                    threshold_ok = False

    assert max_system_residual < 1e-12, "Eq.66 vs Eq.67 transcription guard"
    assert max_component_mismatch < 1e-12, "Eq.67 vs Eq.76 consistency guard"
    assert threshold_ok, "threshold guard (source Eqs. 79-80)"

    # Timelike guard, corrected scope. The source's timelike sentence
    # attaches to the g_e -> infinity limiting value (Eq. 81), where
    # tdot_f -> -(tdot_in + 2) while the spatial speed tends to
    # v tdot_in, so the limit is timelike for every v < 1. At
    # intermediate g_e the outgoing velocity can be spacelike, which is
    # the Stueckelberg requirement that a time-reversing worldline cross
    # the spacelike region; the first version of this guard asserted
    # timelike everywhere, failed, and the failure is preserved as a
    # measured finding rather than suppressed.
    limit_margin = (tdot_in + 2.0) ** 2 - (0.6 * tdot_in) ** 2
    assert limit_margin > 0.0, "asymptotic timelike guard (source Eq. 81)"

    asymptote = {}
    tdot_in = 1.0 / math.sqrt(1.0 - 0.4**2)
    for ge in (10.0, 100.0, 1000.0):
        asymptote[str(ge)] = tdot_final(tdot_in, 0.4, 0.8, ge)
    limit = -(tdot_in + 2.0)
    assert abs(asymptote["1000.0"] - limit) < 0.01, "asymptote guard"

    below = integrate_smoothed(ge=1.0, v=0.4, rhat=(0.8, 0.6))
    above = integrate_smoothed(ge=3.0, v=0.4, rhat=(0.8, 0.6))
    assert below["n_tdot_zero_crossings"] == 0, "no fold below threshold"
    assert below["tdot_min"] > 0.0
    assert below["tdot_final_ode"] > 0.0
    assert above["tdot_final_ode"] < 0.0, "no net reversal above threshold"
    assert above["n_tdot_zero_crossings"] % 2 == 1, \
        "net reversal needs an odd crossing count"
    assert above["crossings"][-1]["classification"] == "annihilation-fold"
    deviation = abs(
        above["tdot_final_ode"] - above["tdot_final_impulse"]
    ) / abs(above["tdot_final_impulse"])

    record = {
        "schema": "pf3-shp-land2016-v1",
        "label": "exploratory",
        "source": {
            "arxiv": "1604.01625v1",
            "related_doi": "10.1088/1742-6596/845/1/012025",
            "provenance_note": "experiments/PF3-PROVENANCE.md",
        },
        "grid": grid,
        "guards": {
            "eq66_vs_eq67_max_residual": max_system_residual,
            "eq67_vs_eq76_max_mismatch": max_component_mismatch,
            "min_timelike_margin": float(min(timelike_margins)),
            "n_spacelike_cells": len(spacelike_cells),
            "spacelike_cells": spacelike_cells,
            "spacelike_reading": "intermediate-ge spacelike outgoing "
                "velocities are the Stueckelberg crossing of the spacelike "
                "region, not a transcription error; the source's timelike "
                "claim is about the ge->infinity limit",
            "threshold_ge2_exact": threshold_ok,
            "asymptote_series": asymptote,
            "asymptote_limit": limit,
            "rutherford_cot_half_angle_08_06":
                rutherford_cot_half_angle((0.8, 0.6)),
        },
        "smoothed_bridge": {
            "below_threshold": below,
            "above_threshold": above,
            "ode_vs_impulse_relative_deviation": deviation,
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
    output = Path(__file__).resolve().parents[1] / "results" / "pf3-land2016.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")

    print(f"guards: system residual {max_system_residual:.2e}, "
          f"component mismatch {max_component_mismatch:.2e}, "
          f"threshold exact: {threshold_ok}")
    print(f"spacelike cells: {len(spacelike_cells)} of "
          f"{len(timelike_margins)} (min margin "
          f"{min(timelike_margins):.4f}); asymptotic limit timelike")
    print(f"asymptote at ge=1000: {asymptote['1000.0']:.6f} "
          f"(limit {limit:.6f})")
    print(f"smoothed: below threshold crossings "
          f"{below['n_tdot_zero_crossings']}, tdot_min "
          f"{below['tdot_min']:.4f}; above threshold crossings "
          f"{above['n_tdot_zero_crossings']} "
          f"({above['crossings'][0]['classification']}), tdot_f ODE "
          f"{above['tdot_final_ode']:.4f} vs impulse "
          f"{above['tdot_final_impulse']:.4f} "
          f"(deviation {deviation:.1%})")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
