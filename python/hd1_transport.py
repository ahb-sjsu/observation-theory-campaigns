#!/usr/bin/env python3
"""HD-1 exact transport instrument (exploratory).

Protocol declared in HYDRODYNAMICS-TRACK.md before this run. HPP on
a 64 torus, ensembles of 100 seeded realizations. Shear modes decay
diffusively, sound modes oscillate at the lattice sound speed, and
the bars are scaling-based, no Boltzmann coefficient assumed.
Verdict computed from the measured items.

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
M = 100
T = 400
F0 = 0.3
AMP = 0.06
# channels 0:E, 1:N, 2:W, 3:S ; arrays [4, M, L(y), L(x)]


def collide(n):
    ew = n[0] & n[2] & ~n[1] & ~n[3]
    ns = n[1] & n[3] & ~n[0] & ~n[2]
    out = n.copy()
    out[0] = (n[0] & ~ew) | ns
    out[2] = (n[2] & ~ew) | ns
    out[1] = (n[1] & ~ns) | ew
    out[3] = (n[3] & ~ns) | ew
    return out


def stream(n):
    out = np.empty_like(n)
    out[0] = np.roll(n[0], 1, axis=2)
    out[2] = np.roll(n[2], -1, axis=2)
    out[1] = np.roll(n[1], -1, axis=1)
    out[3] = np.roll(n[3], 1, axis=1)
    return out


def step(n):
    return stream(collide(n))


def sine(k):
    x = np.arange(L)
    return np.sin(2 * np.pi * k * x / L)


def run_mode(kind, k, seed):
    rng = np.random.RandomState(seed)
    s = sine(k)[None, None, :]
    p = np.full((4, M, L, L), F0)
    if kind == "shear":
        p[1] = F0 + AMP * s
        p[3] = F0 - AMP * s
    else:
        p = p + AMP * s
    n = rng.random((4, M, L, L)) < p
    inv0 = (int(n.sum()), int(n[0].sum() - n[2].sum()),
            int(n[1].sum() - n[3].sum()))
    proj = sine(k)[None, :]
    amps = []
    cons = True
    for _ in range(T + 1):
        if kind == "shear":
            field = (n[1].astype(np.int32)
                     - n[3].astype(np.int32)).sum(axis=1)
        else:
            field = n.astype(np.int32).sum(axis=0).sum(axis=1)
        amps.append(float((field * proj).sum(axis=1).mean()
                          * 2.0 / L))
        n = step(n)
        cons = cons and (int(n.sum()), int(n[0].sum()
                         - n[2].sum()),
                         int(n[1].sum() - n[3].sum())) == inv0
    return np.array(amps), cons


def fit_rate(amps, lo, hi):
    t = np.arange(lo, hi)
    y = np.log(np.abs(amps[lo:hi]))
    a = np.vstack([t, np.ones_like(t)]).T
    slope = np.linalg.lstsq(a, y, rcond=None)[0][0]
    return -float(slope)


def crossings_omega(amps):
    sgn = np.sign(amps)
    idx = np.where(np.diff(sgn) != 0)[0]
    if len(idx) < 2:
        return 0.0
    gaps = np.diff(idx)
    return float(np.pi / gaps.mean())


def main() -> int:
    record: dict = {"schema": "hd1-transport-v1",
                    "label": "exploratory"}
    items = {}
    windows = {1: (50, 350), 2: (20, 140)}
    cons_all = True
    shear = {}
    for k in (1, 2):
        amps, cons = run_mode("shear", k, 20260814 + k)
        cons_all = cons_all and cons
        lo, hi = windows[k]
        mid = (lo + hi) // 2
        rate = fit_rate(amps, lo, hi)
        r1, r2 = fit_rate(amps, lo, mid), fit_rate(amps, mid, hi)
        kp = 2 * np.pi * k / L
        shear[k] = {"rate": rate, "half1": r1, "half2": r2,
                    "nu": rate / kp ** 2,
                    "decay_ratio": float(abs(amps[350])
                                         / abs(amps[50]))}
    items["H1_shear_decays"] = (
        shear[1]["decay_ratio"] < 0.9
        and abs(shear[1]["half1"] - shear[1]["half2"])
        <= 0.2 * shear[1]["rate"]
        and abs(shear[2]["half1"] - shear[2]["half2"])
        <= 0.2 * shear[2]["rate"])
    ratio = shear[2]["rate"] / shear[1]["rate"]
    items["H2_diffusive_scaling"] = 3.4 <= ratio <= 4.6

    sound = {}
    for k in (1, 2):
        amps, cons = run_mode("sound", k, 20260816 + k)
        cons_all = cons_all and cons
        omega = crossings_omega(amps)
        kp = 2 * np.pi * k / L
        sound[k] = {"omega": omega,
                    "c_over_pred": omega / (kp / np.sqrt(2.0))}
    wratio = sound[2]["omega"] / sound[1]["omega"]
    items["H3_sound_dispersion"] = (
        0.85 <= sound[1]["c_over_pred"] <= 1.15
        and 1.85 <= wratio <= 2.15)
    items["H4_conservation"] = bool(cons_all)

    record["measured"] = {
        "shear": {str(k): {kk: float(v) for kk, v in d.items()}
                  for k, d in shear.items()},
        "shear_rate_ratio_k2_over_k1": float(ratio),
        "sound": {str(k): {kk: float(v) for kk, v in d.items()}
                  for k, d in sound.items()},
        "sound_freq_ratio": float(wratio),
        "measured_viscosity_k1": float(shear[1]["nu"]),
        "note": "viscosity and sound speed recorded as values, "
                "Boltzmann-level comparison only"}
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
        / "hd1-transport.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("shear", shear)
    print("sound", sound)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
