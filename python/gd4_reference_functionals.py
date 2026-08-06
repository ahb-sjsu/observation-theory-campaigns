#!/usr/bin/env python3
"""GD-4 reference dependence as observer functional choice.

Protocol declared in GAMES-DECISIONS-TRACK.md before this run. An
encoder adapted to a fixed declared environment reads deviations
from a declared reference functional through a compressive code and
a Gaussian budget, and values novel gambles by mean reference plus
expected read. Four declared functionals, six declared gambles.
Verdict computed from the audits, findings recorded individually
with declared directional bars.

Exploratory label. No claim about human beings.
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

ENV_SCALE = 30.0
GRID = np.round(np.arange(-150.0, 150.0 + 1e-9, 0.5), 10)
MGRID = np.round(np.arange(-13.0, 13.0 + 1e-9, 0.01), 10)
SIGMAS = [2.5, 1.0, 0.0]

BATTERY = {
    "B1": {-40.0: 0.5, 50.0: 0.5},
    "B2": {-5.0: 0.5, 15.0: 0.5},
    "B3": {10.0: 1.0},
    "B4": {-60.0: 0.3, 0.0: 0.4, 60.0: 0.3},
    "B5": {-20.0: 0.8, 80.0: 0.2},
    "B6": {-10.0: 0.8, 90.0: 0.2},
}


def gamble_mean(g):
    return float(sum(x * p for x, p in g.items()))


def lower_median(g):
    xs = sorted(g)
    c = 0.0
    for x in xs:
        c += g[x]
        if c >= 0.5 - 1e-12:
            return float(x)
    return float(xs[-1])


def readmaps(sigma):
    """E[read | true deviation] for every grid deviation, under the
    declared environmental prior. sigma == 0 is the exact identity
    control, the code is injective on the grid."""
    if sigma == 0.0:
        return {float(d): float(d) for d in GRID}
    code = np.sign(GRID) * np.log1p(np.abs(GRID))
    env = np.exp(-np.abs(GRID) / ENV_SCALE)
    env /= env.sum()
    like = np.exp(-0.5 * ((MGRID[None, :] - code[:, None])
                          / sigma) ** 2)
    like /= like.sum(axis=1, keepdims=True)
    joint = env[:, None] * like
    pm = joint.sum(axis=0)
    dec = (joint * GRID[:, None]).sum(axis=0) \
        / np.where(pm > 0, pm, 1.0)
    rm = like @ dec
    return {float(d): float(r) for d, r in zip(GRID, rm)}


def deviation_atoms(g, observer):
    """(atoms, probs, mean reference) for a declared functional."""
    if observer == "O1":
        r = 0.0
        return {x - r: p for x, p in g.items()}, r
    if observer == "O2":
        r = gamble_mean(g)
        return {x - r: p for x, p in g.items()}, r
    if observer == "O3":
        r = lower_median(g)
        return {x - r: p for x, p in g.items()}, r
    if observer == "O4":
        atoms: dict = {}
        for x2, p2 in g.items():
            for x1, p1 in g.items():
                d = x2 - x1
                atoms[d] = atoms.get(d, 0.0) + p1 * p2
        return atoms, gamble_mean(g)
    raise ValueError(observer)


def valuation(g, observer, rm):
    atoms, rbar = deviation_atoms(g, observer)
    total = 0.0
    for d, p in atoms.items():
        dk = round(d * 2.0) / 2.0
        assert abs(dk - d) < 1e-9, f"off-grid deviation {d}"
        total += p * rm[float(dk)]
    return rbar + total


def main() -> int:
    record: dict = {"schema": "gd4-reference-functionals-v1",
                    "label": "exploratory"}
    observers = ["O1", "O2", "O3", "O4"]
    vals = {}
    for sigma in SIGMAS:
        rm = readmaps(sigma)
        vals[sigma] = {name: {o: valuation(g, o, rm)
                              for o in observers}
                       for name, g in BATTERY.items()}
        print(f"sigma {sigma}",
              {n: {o: round(v, 4) for o, v in d.items()}
               for n, d in vals[sigma].items()}, flush=True)

    mus = {n: gamble_mean(g) for n, g in BATTERY.items()}
    audits = {}
    a1 = max(abs(vals[0.0][n][o] - mus[n])
             for n in BATTERY for o in observers)
    audits["A1_zero_noise_identity"] = a1 <= 1e-12
    a2 = 0.0
    for sigma in SIGMAS:
        a2 = max(a2, abs(vals[sigma]["B1"]["O2"] - 5.0),
                 abs(vals[sigma]["B4"]["O1"]),
                 abs(vals[sigma]["B4"]["O2"]),
                 max(abs(vals[sigma][n]["O4"] - mus[n])
                     for n in BATTERY))
    audits["A2_symmetry_anchors"] = a2 <= 1e-10
    a3 = abs(vals[2.5]["B6"]["O2"] - vals[2.5]["B5"]["O2"] - 10.0)
    audits["A3_translation_covariance_O2"] = a3 <= 1e-10
    devs = [max(abs(vals[s][n][o] - mus[n])
                for n in BATTERY for o in observers)
            for s in SIGMAS]
    audits["A4_budget_monotone"] = devs[0] > devs[1] > devs[2]

    v25 = vals[2.5]
    spread = max(max(v25[n][o] for o in observers)
                 - min(v25[n][o] for o in observers)
                 for n in BATTERY)
    findings = {"F1_observer_spread": bool(spread >= 0.5)}
    best_rev = None
    names = list(BATTERY)
    for i, o1 in enumerate(observers):
        for o2 in observers[i + 1:]:
            for x, n1 in enumerate(names):
                for n2 in names[x + 1:]:
                    d1 = v25[n1][o1] - v25[n2][o1]
                    d2 = v25[n1][o2] - v25[n2][o2]
                    if d1 > 0.02 and d2 < -0.02:
                        m = min(d1, -d2)
                    elif d1 < -0.02 and d2 > 0.02:
                        m = min(-d1, d2)
                    else:
                        continue
                    if best_rev is None or m > best_rev[0]:
                        best_rev = (m, o1, o2, n1, n2,
                                    float(d1), float(d2))
    findings["F2_ranking_reversal"] = best_rev is not None
    breach = abs(v25["B6"]["O1"] - v25["B5"]["O1"] - 10.0)
    findings["F3_status_quo_breach"] = bool(
        breach >= 0.05 and a3 <= 1e-10)

    record["valuations"] = {
        str(s): {n: {o: float(v) for o, v in d.items()}
                 for n, d in vals[s].items()} for s in SIGMAS}
    record["gamble_means"] = {n: float(m) for n, m in mus.items()}
    record["measured"] = {
        "a1_max_dev": float(a1), "a2_max_anchor_dev": float(a2),
        "a3_O2_covariance_dev": float(a3),
        "ladder_max_devs": [float(d) for d in devs],
        "max_observer_spread": float(spread),
        "best_reversal": (list(best_rev) if best_rev else None),
        "O1_covariance_breach": float(breach)}
    record["audits"] = {k: bool(v) for k, v in audits.items()}
    record["findings"] = {k: bool(v) for k, v in findings.items()}
    verdict = "PASS" if all(audits.values()) else "FAIL"
    record["verdict"] = {
        "value": verdict, "computed_from": sorted(audits),
        "note": "findings recorded individually per the declared "
                "protocol"}
    record["declared"] = {
        "env_scale": ENV_SCALE, "sigmas": SIGMAS,
        "bars": {"F1_spread": 0.5, "F2_margin": 0.02,
                 "F3_breach": 0.05}}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "gd4-reference-functionals.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("audits", audits)
    print("findings", findings, "spread", spread,
          "reversal", best_rev, "breach", breach)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
