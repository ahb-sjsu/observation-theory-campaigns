#!/usr/bin/env python3
"""HD-2 FHP viscosity, the prescription gate (exploratory).

Protocol declared in HYDRODYNAMICS-TRACK.md before this run. FHP-I
on a 64x64 triangular lattice in even-r offset coordinates, six
channels, head-on pairs rotated with deterministic alternating
chirality plus the symmetric three-body collision. Shear modes at
k = 1, 2 decay viscously, and nine declared coarse-graining
prescriptions (cell size x sampling cadence) are applied to the
same stored per-column momentum series to ask whether the
extracted rate is prescription-invariant or prescription-borne.
The verdict is computed from H2a, H2b, H2c only, H2d is a finding
with a declared directional bar, recorded individually.

Exploratory label. No claim about physical fluids.
"""
from __future__ import annotations

import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from projection_fold import canonical_sha256  # noqa: E402

L = 64
M = 50
T = 300
F0 = 0.35
AMP = 0.10
S3 = np.sqrt(3.0) / 2.0
# channels 0:E, 1:NE, 2:NW, 3:W, 4:SW, 5:SE ; arrays [6, M, L(r), L(c)]
# x_phys = c + 0.5*(r % 2), y_phys = -r*S3 (row r-1 is up, +y)
CX2 = (2, 1, -1, -2, -1, 1)     # 2 * e_i x-component
CYU = (0, 1, 1, 0, -1, -1)      # e_i y-component / S3
# neighbor tables (dr, dc), index = channel, per row parity
TABLE = (
    ((0, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0)),   # even r
    ((0, 1), (-1, 1), (-1, 0), (0, -1), (1, 0), (1, 1)),     # odd r
)
WINDOWS = {1: (30, 250), 2: (15, 120)}
CELLS = (1, 4, 8)
CADENCES = (1, 2, 4)


def collide(n, t):
    out = n.copy()
    for i in range(3):
        j = i + 3
        m = n[i] & n[j]
        for k in range(6):
            if k not in (i, j):
                m = m & ~n[k]
        if t % 2 == 0:
            a, b = (i + 1) % 6, (i + 4) % 6
        else:
            a, b = (i - 1) % 6, (i + 2) % 6
        out[i] &= ~m
        out[j] &= ~m
        out[a] |= m
        out[b] |= m
    m3a = n[0] & n[2] & n[4] & ~n[1] & ~n[3] & ~n[5]
    m3b = n[1] & n[3] & n[5] & ~n[0] & ~n[2] & ~n[4]
    for k in (0, 2, 4):
        out[k] = (out[k] & ~m3a) | m3b
    for k in (1, 3, 5):
        out[k] = (out[k] & ~m3b) | m3a
    return out


def stream(n):
    out = np.zeros_like(n)
    rows = np.arange(L)
    for i in range(6):
        for p in (0, 1):
            dr, dc = TABLE[p][i]
            src = rows[rows % 2 == p]
            dst = (src + dr) % L
            out[i][..., dst, :] = np.roll(n[i][..., src, :], dc,
                                          axis=-1)
    return out


def step(n, t):
    return stream(collide(n, t))


def invariants(n):
    """(mass, 2*px, py/S3) per realization, integer-exact."""
    per = n.astype(np.int64).sum(axis=(2, 3))  # [6, M]
    mass = per.sum(axis=0)
    px2 = sum(CX2[i] * per[i] for i in range(6))
    pyu = sum(CYU[i] * per[i] for i in range(6))
    return mass, px2, pyu


def selftest_t1():
    for i in range(6):
        n = np.zeros((6, 1, L, L), dtype=bool)
        r0, c0 = 32, 32
        n[i, 0, r0, c0] = True
        for t in range(6):
            n = step(n, t)
        ch, _, r1, c1 = [int(v[0]) for v in np.argwhere(n)[0:1].T]
        if ch != i:
            return False
        d2x = (2 * c1 + (r1 % 2)) - (2 * c0 + (r0 % 2))
        dyu = -(r1 - r0)
        if d2x != 6 * CX2[i] or dyu != 6 * CYU[i]:
            return False
    return True


def selftest_t2():
    for r0 in (32, 33):
        r, c = r0, 32
        for i in range(6):
            dr, dc = TABLE[r % 2][i]
            r, c = (r + dr) % L, (c + dc) % L
        if (r, c) != (r0, 32):
            return False
    return True


def x_phys():
    r = np.arange(L)[:, None]
    c = np.arange(L)[None, :]
    return c + 0.5 * (r % 2)


def run_shear(k, seed):
    rng = np.random.RandomState(seed)
    s = np.sin(2 * np.pi * k * x_phys() / L)[None, :, :]
    p = np.empty((6, M, L, L))
    for i in range(6):
        p[i] = np.clip(F0 + AMP * CYU[i] * s, 0.0, 1.0)
    n = rng.random((6, M, L, L)) < p
    inv0 = invariants(n)
    cons = True
    cols = []
    for t in range(T + 1):
        field = sum(CYU[i] * n[i].astype(np.int64) for i in range(6)
                    if CYU[i] != 0).sum(axis=1)  # [M, L(c)]
        cols.append(field.mean(axis=0))  # ensemble-mean per column
        n = step(n, t)
        inv = invariants(n)
        cons = cons and all(np.array_equal(a, b)
                            for a, b in zip(inv, inv0))
    return np.array(cols), cons  # [T+1, L]


def project(colfield, k):
    proj = np.sin(2 * np.pi * k * np.arange(L) / L)
    return colfield @ proj * 2.0 / L


def fit_rate(amps, xs):
    a = np.vstack([xs, np.ones_like(xs, dtype=float)]).T
    slope = np.linalg.lstsq(a, np.log(np.abs(amps)), rcond=None)[0][0]
    return -float(slope)


def gate_rate(colfield, cell, cadence, lo, hi):
    if cell > 1:
        blk = colfield.reshape(colfield.shape[0], L // cell, cell)
        cf = np.repeat(blk.mean(axis=2), cell, axis=1)
    else:
        cf = colfield
    times = np.array([t for t in range(0, T + 1, cadence)
                      if lo <= t <= hi])
    amps = project(cf[times], 1)
    per_frame = fit_rate(amps, np.arange(len(times)))
    return per_frame / cadence


def main() -> int:
    record: dict = {"schema": "hd2-fhp-viscosity-v1",
                    "label": "exploratory"}
    record["declared"] = {
        "model": "FHP-I, 64x64 even-r offset triangular torus, "
                 "6 channels, head-on pairs rotated +1 on even and "
                 "-1 on odd steps, three-body 024<->135, "
                 "collide then stream",
        "L": L, "M": M, "T": T, "f0": F0, "amp": AMP,
        "seeds": {str(k): 20260820 + k for k in (1, 2)},
        "windows": {str(k): list(WINDOWS[k]) for k in (1, 2)},
        "gate": "9 prescriptions = cells {1,4,8} x cadence {1,2,4} "
                "on the stored k=1 per-column series, window "
                "[30,250], per-frame slope / cadence",
        "verdict_split": "verdict from H2a, H2b, H2c only; H2d is "
                         "a finding with a declared directional "
                         "bar (spread <= 10 percent of mean), "
                         "recorded individually"}
    items = {}

    t1, t2 = selftest_t1(), selftest_t2()

    shear = {}
    stored = {}
    cons_all = True
    for k in (1, 2):
        colfield, cons = run_shear(k, 20260820 + k)
        cons_all = cons_all and cons
        stored[k] = colfield
        amps = project(colfield, k)
        lo, hi = WINDOWS[k]
        mid = (lo + hi) // 2
        rate = fit_rate(amps[lo:hi], np.arange(lo, hi))
        r1 = fit_rate(amps[lo:mid], np.arange(lo, mid))
        r2 = fit_rate(amps[mid:hi], np.arange(mid, hi))
        kp = 2 * np.pi * k / L
        shear[k] = {"rate": rate, "half1": r1, "half2": r2,
                    "nu": rate / kp ** 2,
                    "decay_ratio": float(abs(amps[hi])
                                         / abs(amps[lo]))}
    ratio = shear[2]["rate"] / shear[1]["rate"]

    items["H2a_shear_decays"] = bool(
        shear[1]["decay_ratio"] < 0.9
        and abs(shear[1]["half1"] - shear[1]["half2"])
        <= 0.25 * shear[1]["rate"]
        and abs(shear[2]["half1"] - shear[2]["half2"])
        <= 0.25 * shear[2]["rate"])
    items["H2b_diffusive_scaling"] = bool(3.0 <= ratio <= 5.0)
    items["H2c_geometry_exact"] = bool(t1 and t2 and cons_all)

    lo, hi = WINDOWS[1]
    gate = {}
    for cell in CELLS:
        for cad in CADENCES:
            gate[f"cell{cell}_cad{cad}"] = gate_rate(
                stored[1], cell, cad, lo, hi)
    rates = np.array(list(gate.values()))
    spread = float(rates.max() - rates.min())
    spread_over_mean = float(spread / rates.mean())
    h2d = bool(spread_over_mean <= 0.10)
    finding = {
        "hypothesis": "rate is prescription-invariant, spread "
                      "across the nine at most 10 percent of mean",
        "prescription_rates": {kk: float(v)
                               for kk, v in gate.items()},
        "spread": spread,
        "spread_over_mean": spread_over_mean,
        "outcome": ("prescription-invariant" if h2d
                    else "prescription-borne"),
        "bar_passed": h2d}
    record["findings"] = {"H2d_prescription_gate": finding}

    fboltz = (1.0 / 12.0) / (F0 * (1.0 - F0) ** 3) - 1.0 / 8.0
    record["measured"] = {
        "selftests": {"T1_displacement": bool(t1),
                      "T2_hexagon_closes": bool(t2),
                      "T3_conservation": bool(cons_all)},
        "shear": {str(k): {kk: float(v) for kk, v in d.items()}
                  for k, d in shear.items()},
        "shear_rate_ratio_k2_over_k1": float(ratio),
        "measured_viscosity_k1": float(shear[1]["nu"]),
        "measured_viscosity_k2": float(shear[2]["nu"]),
        "boltzmann_comparison_nu": float(fboltz),
        "note": "nu recorded as a value; the FHP-I Boltzmann "
                "estimate (1/12)/(f(1-f)^3) - 1/8 is comparison "
                "only, never a bar"}
    record["items"] = {k: bool(v) for k, v in items.items()}
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items)}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "hd2-fhp-viscosity.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("shear", shear)
    print("ratio", ratio)
    print("gate", gate)
    print("spread_over_mean", spread_over_mean, finding["outcome"])
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
