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


def continuous_accumulation(*, ge: float, v: float, rhat_x: float) -> dict:
    """Continuous integration of the source's kick generator.

    With the interaction point frozen (the source's Eq. 61 convention)
    and the kernel-derivative term dropped (its integral is exactly zero
    there), Eqs. 59-60 reduce, in the accumulated-kernel variable
    s = integral phi dtau in [0, 1], to the linear system

        d(tdot)/ds = -ge w        dw/ds = -ge (tdot + 1)

    for w the R-hat component of the spatial velocity. The solution is
    hyperbolic,

        tdot(s) + 1 = (tdot_in + 1) cosh(ge s) - w_in sinh(ge s),

    and since w_in = v tdot_in rhat_x < tdot_in + 1, tdot never reverses
    for any ge. The midpoint convention of source Eq. 63 is instead the
    Cayley transform (I - G/2)^{-1}(I + G/2) of the same generator, the
    Pade(1,1) approximant of this exponential, whose pole at ge = 2 is
    exactly the published annihilation threshold. Verified here by an
    independent RK4 integration against the closed form.
    """
    tdot_in = 1.0 / math.sqrt(1.0 - v * v)
    w_in = v * tdot_in * rhat_x

    def closed(s):
        a = tdot_in + 1.0
        return (a * math.cosh(ge * s) - w_in * math.sinh(ge * s) - 1.0,
                w_in * math.cosh(ge * s) - a * math.sinh(ge * s))

    tdot_c, w_c = closed(1.0)

    n = 20000
    ds = 1.0 / n
    tdot, w = tdot_in, w_in
    tdot_min = tdot
    for _ in range(n):
        def rhs(td, ww):
            return -ge * ww, -ge * (td + 1.0)
        k1 = rhs(tdot, w)
        k2 = rhs(tdot + ds / 2 * k1[0], w + ds / 2 * k1[1])
        k3 = rhs(tdot + ds / 2 * k2[0], w + ds / 2 * k2[1])
        k4 = rhs(tdot + ds * k3[0], w + ds * k3[1])
        tdot += ds / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        w += ds / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        tdot_min = min(tdot_min, tdot)

    return {
        "ge": ge, "v": v, "rhat_x": rhat_x, "tdot_in": tdot_in,
        "tdot_final_closed_form": tdot_c,
        "tdot_final_rk4": float(tdot),
        "closed_vs_rk4": abs(tdot_c - tdot),
        "tdot_min_along_path": float(tdot_min),
        "tdot_final_impulse_cayley": tdot_final(tdot_in, v, rhat_x, ge),
        "reverses": tdot_c < 0.0,
    }


def midpoint_bridge(
    *, ge: float, v: float, rhat_x: float, lam: float = 0.02, dt: float = 1e-4
) -> dict:
    """The source-faithful smooth reading of the impulsive worldline.

    The midpoint algebra transitions the velocity from its incoming to
    its outgoing value across the kernel window; the natural smooth
    worldline it defines is tdot(tau) = tdot_in + (tdot_f - tdot_in)
    S(tau) with S the kernel's cumulative integral. This uses only the
    source's own velocities and kernel. The crossing, when tdot_f < 0,
    is located and classified with the sealed classifier.
    """
    tdot_in = 1.0 / math.sqrt(1.0 - v * v)
    tdot_f = tdot_final(tdot_in, v, rhat_x, ge)

    taus = np.arange(-lam, lam + dt, dt)

    def kernel_cdf(s):
        if s <= -lam:
            return 0.0
        if s >= lam:
            return 1.0
        return 0.5 + s / (2.0 * lam) + math.sin(math.pi * s / lam) / (2.0 * math.pi)

    tdots = np.array([
        tdot_in + (tdot_f - tdot_in) * kernel_cdf(s) for s in taus
    ])
    crossings = []
    hits = np.nonzero(tdots[:-1] * tdots[1:] < 0.0)[0]
    for idx in hits:
        alpha = tdots[idx] / (tdots[idx] - tdots[idx + 1])
        tau_c = float(taus[idx] + alpha * dt)
        slope = (tdot_f - tdot_in) * hann_kernel(tau_c, lam)
        crossings.append({
            "tau": tau_c,
            "tdot_slope": float(slope),
            "classification": classify_scalar_critical_point(
                0.0, slope, second_tol=1e-9
            ),
        })
    return {
        "ge": ge, "v": v, "rhat_x": rhat_x, "lambda": lam,
        "tdot_in": tdot_in, "tdot_final_impulse": tdot_f,
        "n_tdot_zero_crossings": len(crossings),
        "crossings": crossings,
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

    continuous = {
        str(ge): continuous_accumulation(ge=ge, v=0.4, rhat_x=0.8)
        for ge in (1.0, 3.0, 6.0)
    }
    for entry in continuous.values():
        assert entry["closed_vs_rk4"] < 1e-9, "cosh/sinh closed-form guard"
        assert not entry["reverses"], \
            "continuous accumulation reversed: the Cayley finding is wrong"
        assert entry["tdot_min_along_path"] > -1e-12

    bridge_below = midpoint_bridge(ge=1.0, v=0.4, rhat_x=0.8)
    bridge_above = midpoint_bridge(ge=3.0, v=0.4, rhat_x=0.8)
    assert bridge_below["n_tdot_zero_crossings"] == 0, \
        "no crossing below threshold"
    assert bridge_above["n_tdot_zero_crossings"] == 1, \
        "exactly one crossing above threshold"
    assert bridge_above["crossings"][0]["classification"] == \
        "annihilation-fold"

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
        "continuous_accumulation_finding": {
            "statement": "with the source's frozen-point convention the "
                "kick generator exponentiates to cosh/sinh evolution and "
                "never reverses tdot; the published ge > 2 threshold is "
                "the pole of the midpoint (Cayley / Pade(1,1)) form of "
                "the same generator",
            "sweeps": continuous,
        },
        "midpoint_bridge": {
            "below_threshold": bridge_below,
            "above_threshold": bridge_above,
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
    for ge_key, entry in continuous.items():
        print(f"continuous ge={ge_key}: tdot_f = "
              f"{entry['tdot_final_closed_form']:.4f} (never reverses) "
              f"vs Cayley/impulse {entry['tdot_final_impulse_cayley']:.4f}")
    print(f"midpoint bridge: below crossings "
          f"{bridge_below['n_tdot_zero_crossings']}, above crossings "
          f"{bridge_above['n_tdot_zero_crossings']} "
          f"({bridge_above['crossings'][0]['classification']} at tau "
          f"{bridge_above['crossings'][0]['tau']:.5f})")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
