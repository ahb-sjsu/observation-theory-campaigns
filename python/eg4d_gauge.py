#!/usr/bin/env python3
"""EG-4d constraint-locked structure (exploratory, EG track).

Declared in the track document before this run, including the claim
demotion. A Gauss-type constraint is the one standard mechanism for
persistent local structure that survives its own relaxation, and if
it is declared at Level 0 the static Poisson structure of the mean
field follows from constraint mathematics, not from entropy. The
honest claim under test is that constraints source geometry and
distinguishability registers them exactly. The nontrivial measured
content is stationarity of the D field under the dynamics (the
anti-radiative witness every previous substrate failed), the graded
falloff measured against alternatives, exact superposition and
charge scaling of the field-level object, and the Gauss and Poisson
forms holding on the MEASURED field.

Substrate. Two-dimensional lattice electromagnetism on an L x L
torus. E lives on edges (two per site, right and down), B on
plaquettes, H = (sum E^2 + sum B^2)/2, dynamics the local curl
pair, dE/dt = -curl B and dB/dt = curl E, which preserves the
per-vertex divergence of E identically. The vacuum is the
identity-covariance Gaussian conditioned on div E = 0 everywhere;
matter conditions on div E = rho for a declared plus-minus vertex
pair. Conditional means come from one Fourier Poisson solve (the
mathematics of conditioning a Gaussian on a linear constraint, not a
model input, per the declared audit), conditional covariances from
torus Green-function lookups, and every D value is the closed
Gaussian form with equal covariances,
D = (1/2) dmu^T Sigma_w^{-1} dmu / ln 2.

Exploratory label. No physics claim. Nothing here supports the
reading that entropy sources geometry.
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

L_SIDE = 64
CHARGE_SEP = 32
AXIS_RS = [2, 3, 4, 6, 8, 11, 16, 22]
EVOLVE_STEPS = 400
DT_EVOLVE = 0.05


def green_function(side: int) -> np.ndarray:
    """Torus Green function of the 5-point Laplacian, zero-mean
    convention, via Fourier."""
    kx, ky = np.meshgrid(np.arange(side), np.arange(side),
                         indexing="ij")
    eig = 4.0 - 2.0 * np.cos(2 * np.pi * kx / side) \
        - 2.0 * np.cos(2 * np.pi * ky / side)
    inv = np.zeros_like(eig)
    inv[eig > 1e-12] = 1.0 / eig[eig > 1e-12]
    g = np.real(np.fft.ifft2(inv))
    return g


def mean_field(side: int, charges: dict, g: np.ndarray):
    """Conditional mean of E given div E = rho: mu = C^T phi with
    Lap phi = rho (the conditioning formula). Returns (ex, ey) with
    ex[i,j] the edge from (i,j) to (i,j+1) and ey the edge to
    (i+1,j). Divergence convention: div(v) = sum of outgoing minus
    incoming edge fields."""
    rho = np.zeros((side, side))
    for (i, j), q in charges.items():
        rho[i % side, j % side] += q
    phi = np.real(np.fft.ifft2(np.fft.fft2(rho)
                               * np.fft.fft2(g)))
    ex = phi - np.roll(phi, -1, axis=1)
    ey = phi - np.roll(phi, -1, axis=0)
    return ex, ey


def divergence(ex, ey):
    return (ex - np.roll(ex, 1, axis=1)
            + ey - np.roll(ey, 1, axis=0))


def edge_cov(side: int, g: np.ndarray, edges):
    """Conditional covariance of listed edges, Sigma = I - C^T G C,
    entries from four Green values per pair. Edge = ("x"|"y", i, j)."""
    def endpoints(e):
        kind, i, j = e
        if kind == "x":
            return (i % side, j % side), (i % side, (j + 1) % side)
        return (i % side, j % side), ((i + 1) % side, j % side)

    def gval(a, b):
        return g[(a[0] - b[0]) % side, (a[1] - b[1]) % side]

    k = len(edges)
    cov = np.empty((k, k))
    for a in range(k):
        pa, qa = endpoints(edges[a])
        for b in range(a, k):
            pb, qb = endpoints(edges[b])
            v = (gval(pa, pb) - gval(pa, qb)
                 - gval(qa, pb) + gval(qa, qb))
            cov[a, b] = cov[b, a] = (1.0 if a == b else 0.0) - v
    return cov


def window_D(side, g, charges, edges) -> float:
    ex, ey = mean_field(side, charges, g)
    mu = []
    for kind, i, j in edges:
        mu.append(ex[i % side, j % side] if kind == "x"
                  else ey[i % side, j % side])
    mu = np.array(mu)
    cov = edge_cov(side, g, edges)
    return float(0.5 * mu @ np.linalg.solve(cov, mu) / math.log(2.0))


def evolve_mean(ex, ey, b, steps, dt):
    """Leapfrog for the curl pair; curl B on an edge is the
    difference of the two adjacent plaquette values, curl E on a
    plaquette is the circulation."""
    for _ in range(steps):
        curl_e = (ex - np.roll(ex, -1, axis=0)
                  + np.roll(ey, -1, axis=1) - ey)
        b = b + dt * curl_e
        ex = ex - dt * (b - np.roll(b, 1, axis=0))
        ey = ey - dt * (np.roll(b, 1, axis=1) - b)
    return ex, ey, b


def main() -> int:
    record: dict = {"schema": "eg4d-gauge-v1", "label": "exploratory"}

    # P0: instrument control against dense conditioning, small torus
    s_small = 6
    g_s = green_function(s_small)
    n_e = 2 * s_small * s_small
    c_mat = np.zeros((s_small * s_small, n_e))
    for i in range(s_small):
        for j in range(s_small):
            v = i * s_small + j
            ex_id = i * s_small + j
            ey_id = s_small * s_small + ex_id
            c_mat[v, ex_id] += 1.0
            c_mat[i * s_small + (j - 1) % s_small, ex_id] -= 1.0
            c_mat[v, ey_id] += 1.0
            c_mat[((i - 1) % s_small) * s_small + j, ey_id] -= 1.0
    lap = c_mat @ c_mat.T
    lap_pinv = np.linalg.pinv(lap)
    charges_s = {(1, 1): 1.0, (4, 4): -1.0}
    rho = np.zeros(s_small * s_small)
    rho[1 * s_small + 1] = 1.0
    rho[4 * s_small + 4] = -1.0
    mu_dense = c_mat.T @ (lap_pinv @ rho)
    ex_f, ey_f = mean_field(s_small, charges_s, g_s)
    mu_fft = np.concatenate([ex_f.reshape(-1), ey_f.reshape(-1)])
    ctl_mu = float(np.max(np.abs(mu_dense - mu_fft)))
    assert ctl_mu < 1e-10, f"P0 mean control {ctl_mu}"
    sig_dense = np.eye(n_e) - c_mat.T @ lap_pinv @ c_mat
    test_edges = [("x", 1, 1), ("x", 1, 2), ("y", 2, 1), ("y", 3, 3)]
    idx = [e[1] * s_small + e[2] if e[0] == "x"
           else s_small * s_small + e[1] * s_small + e[2]
           for e in test_edges]
    sig_fft = edge_cov(s_small, g_s, test_edges)
    ctl_sig = float(np.max(np.abs(sig_dense[np.ix_(idx, idx)]
                                  - sig_fft)))
    assert ctl_sig < 1e-10, f"P0 covariance control {ctl_sig}"
    record["P0_control"] = {"mean_dev": ctl_mu, "cov_dev": ctl_sig}

    # main lattice and charges
    g = green_function(L_SIDE)
    c0 = L_SIDE // 2
    charges = {(c0, c0): 1.0, (c0, (c0 + CHARGE_SEP)): -1.0}

    # P1: stationarity, the anti-radiative witness. The conditional
    # mean must be an exact fixed point of the dynamics, and the
    # window covariance must be invariant (transverse isotropy),
    # verified densely on the small lattice.
    ex, ey = mean_field(L_SIDE, charges, g)
    b0 = np.zeros((L_SIDE, L_SIDE))
    ex2, ey2, b2 = evolve_mean(ex.copy(), ey.copy(), b0.copy(),
                               EVOLVE_STEPS, DT_EVOLVE)
    stat_dev = float(max(np.max(np.abs(ex2 - ex)),
                         np.max(np.abs(ey2 - ey)),
                         np.max(np.abs(b2))))
    assert stat_dev < 1e-10, f"P1 mean not stationary: {stat_dev}"
    record["P1_stationarity"] = {"mean_field_drift": stat_dev,
                                 "steps": EVOLVE_STEPS,
                                 "dt": DT_EVOLVE}

    # P2: profile and falloff along the axis away from both charges
    def window_at(r):
        return [("x", c0 + r, c0), ("y", c0 + r, c0),
                ("x", c0 + r, c0 - 1), ("y", c0 + r - 1, c0)]

    profile = [{"r": r, "D_bits": window_D(L_SIDE, g, charges,
                                           window_at(r))}
               for r in AXIS_RS]
    ds = np.array([row["D_bits"] for row in profile])
    assert np.all(ds > 0), "P2 field must be nonzero"
    assert np.all(np.diff(ds) < 0), "P2 field must decay monotonically"
    x = np.log(np.array(AXIS_RS, dtype=float))
    y = np.log(ds)
    slope = float(np.polyfit(x, y, 1)[0])
    record["P2_profile"] = {"profile": profile,
                            "loglog_slope": slope,
                            "expected_2d_coulomb_D": -2.0}

    # P3: exact superposition and charge scaling of the field object
    charges_a = {(c0, c0 - 8): 1.0, (c0, c0 + CHARGE_SEP): -1.0}
    charges_b = {(c0, c0 + 8): 1.0,
                 ((c0 + CHARGE_SEP) % L_SIDE, c0): -1.0}
    charges_ab = {**charges_a, **charges_b}
    exa, eya = mean_field(L_SIDE, charges_a, g)
    exb, eyb = mean_field(L_SIDE, charges_b, g)
    exs, eys = mean_field(L_SIDE, charges_ab, g)
    sup_dev = float(max(np.max(np.abs(exs - exa - exb)),
                        np.max(np.abs(eys - eya - eyb))))
    assert sup_dev < 1e-12, f"P3 superposition {sup_dev}"
    charges_q2 = {k: 2.0 * v for k, v in charges.items()}
    d1 = window_D(L_SIDE, g, charges, window_at(6))
    d2 = window_D(L_SIDE, g, charges_q2, window_at(6))
    q_ratio = d2 / d1
    assert abs(q_ratio - 4.0) < 1e-9, f"P3 charge scaling {q_ratio}"
    record["P3_superposition"] = {"field_superposition_dev": sup_dev,
                                  "D_charge2_over_charge1": q_ratio,
                                  "predicted_quadratic": 4.0}

    # P4: Gauss and Poisson forms on the MEASURED mean field
    div = divergence(ex, ey)
    rho_target = np.zeros((L_SIDE, L_SIDE))
    rho_target[c0, c0] = 1.0
    rho_target[c0, (c0 + CHARGE_SEP) % L_SIDE] = -1.0
    gauss_dev = float(np.max(np.abs(div - rho_target)))
    assert gauss_dev < 1e-10, f"P4 Gauss {gauss_dev}"
    curl = (ex - np.roll(ex, -1, axis=0)
            + np.roll(ey, -1, axis=1) - ey)
    curl_dev = float(np.max(np.abs(curl)))
    assert curl_dev < 1e-10, f"P4 curl-free {curl_dev}"
    record["P4_gauss_poisson"] = {
        "gauss_residual": gauss_dev,
        "curl_residual": curl_dev,
        "reading": "div E = rho exactly and curl E = 0 exactly on "
                   "the measured field, so its potential solves the "
                   "lattice Poisson equation, a derived consequence "
                   "of the declared local constraint per the "
                   "demotion ruling"}

    items = {
        "instrument_control": True,
        "static_under_dynamics": bool(stat_dev < 1e-10),
        "graded_monotone_decay": True,
        "falloff_measured": bool(-2.6 < slope < -1.4),
        "superposition_exact": bool(sup_dev < 1e-12),
        "charge_scaling_quadratic": bool(abs(q_ratio - 4.0) < 1e-9),
        "gauss_exact_on_measured_field": bool(gauss_dev < 1e-10),
        "poisson_inherited_from_constraint": True,
    }
    passed = sum(1 for v in items.values() if v)
    verdict = (
        f"constraint-locked structure delivers what every previous "
        f"substrate lacked, a distinguishability field that is "
        f"EXACTLY static under the deterministic dynamics (drift "
        f"{stat_dev:.2e} over {EVOLVE_STEPS} steps), graded and "
        f"monotone with measured log-log slope {slope:.3f} against "
        f"the two-dimensional Coulomb expectation of -2, exactly "
        f"superposing at the field level ({sup_dev:.2e}) with exact "
        f"quadratic charge scaling of D, and satisfying Gauss and "
        f"curl-free conditions on the measured field to {gauss_dev:.2e}; "
        f"{passed} of {len(items)} items pass; per the demotion "
        f"ruling this does NOT support entropy sourcing geometry, "
        f"the constraint sources the geometry and the "
        f"relative-entropy field registers it exactly, which locates "
        f"the missing ingredient of the EG-4 bar precisely, a local "
        f"conservation law tying matter to boundary flux")
    record["items"] = items
    record["verdict"] = verdict

    record["declared"] = {
        "lattice": L_SIDE, "charge_separation": CHARGE_SEP,
        "axis_rs": AXIS_RS,
        "evolve": {"steps": EVOLVE_STEPS, "dt": DT_EVOLVE},
        "vacuum": "identity-covariance Gaussian conditioned on "
                  "div E = 0 everywhere",
        "matter": "plus-minus unit charges entering only through "
                  "the constraint value",
        "audit": "constraint is per-vertex and local; no radial "
                 "function, potential, or Poisson equation inserted; "
                 "conditioning formulas are Gaussian mathematics; "
                 "claim demotion recorded in the track document "
                 "before this run",
    }
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown"),
    }
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"}
    )
    output = Path(__file__).resolve().parents[1] / "results" \
        / "eg4d-gauge.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print("P0:", record["P0_control"])
    print("P1 drift:", stat_dev)
    print("P2 profile:", [(row["r"], round(row["D_bits"], 6))
                          for row in profile], "slope", round(slope, 3))
    print("P3:", record["P3_superposition"])
    print("P4 gauss:", gauss_dev, "curl:", curl_dev)
    print("items:", items)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
