#!/usr/bin/env python3
"""PE-3 mixing versus folding (exploratory, PE track).

A matched two-by-two. Two dynamics of the full toy Hamiltonian
(omega_t = 1, omega_u = 1.2, g = 0.25, E = 2), integrable at
lambda = 0 and nonintegrable at lambda = 0.35, share everything else.
Two observers read the same trajectories, the folding time functional
T = t and the monotone functional T = t + 3 tau, which never folds
because |p_t| stays well under 3. Because the observers differ only by
the linear tau term, the instantaneous ensemble marginal of t is
common to both, so the design separates the two mechanisms exactly.
Ensemble-marginal entropy growth can come only from the dynamics
(mixing), and slice multiplicity can come only from the observer's
singularities (folds). The witnesses are the centered binned entropy
curve of the t marginal per dynamics, its late-time slope, and the
mean unsigned crossing multiplicity per observed level for each
observer on a reference trajectory.

Expected and asserted: the chaotic dynamics grows entropy faster than
the integrable one under EITHER observer; the folding observer sees
mean multiplicity above one under EITHER dynamics while the monotone
observer sees exactly one everywhere. Mixing pumps entropy, folds
create multiplicity, and the axes are independent.

Exploratory label.
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

OMEGA_T = 1.0
OMEGA_U = 1.2
G_COUP = 0.25
E_FIELD = 2.0
T_BATH = 1.0
DT = 1e-3
TAU_MAX = 40.0
N_ENS = 20_000
SEED = 20260805
EPS = 0.05
ALPHA_MONOTONE = 3.0


def evolve(lam: float):
    rng = np.random.RandomState(SEED)
    t = np.zeros(N_ENS)
    pt = np.ones(N_ENS)
    u = rng.standard_normal(N_ENS) * math.sqrt(T_BATH) / OMEGA_U
    pu = rng.standard_normal(N_ENS) * math.sqrt(T_BATH)
    curve = []
    ref = []  # reference trajectory (member 0): (tau, t, pt)
    steps = int(round(TAU_MAX / DT))
    for k in range(steps + 1):
        if k % 40 == 0:
            centered = t - t.mean()
            counts = np.bincount(
                np.clip(((centered + 8.0) / EPS).astype(int), 0,
                        int(16.0 / EPS)))
            p = counts[counts > 0] / N_ENS
            curve.append(float(-(p * np.log2(p)).sum()))
        ref.append((k * DT, float(t[0]), float(pt[0])))
        ft = -OMEGA_T**2 * t - G_COUP * E_FIELD * u
        fu = -OMEGA_U**2 * u - lam * u**3 - G_COUP * E_FIELD * t
        pth = pt + 0.5 * DT * ft
        puh = pu + 0.5 * DT * fu
        t = t + DT * pth
        u = u + DT * puh
        ft = -OMEGA_T**2 * t - G_COUP * E_FIELD * u
        fu = -OMEGA_U**2 * u - lam * u**3 - G_COUP * E_FIELD * t
        pt = pth + 0.5 * DT * ft
        pu = puh + 0.5 * DT * fu
    return curve, ref


def late_slope(curve):
    n = len(curve)
    xs = np.arange(n) * (TAU_MAX / (n - 1))
    lo = n // 2
    return float(np.polyfit(xs[lo:], np.array(curve)[lo:], 1)[0])


def multiplicity(ref, alpha: float) -> dict:
    taus = np.array([r[0] for r in ref])
    ts = np.array([r[1] for r in ref])
    big_t = ts + alpha * taus
    levels = np.linspace(big_t.min() + 0.3, big_t.max() - 0.3, 200)
    counts = []
    for level in levels:
        s = big_t - level
        crossings = int(np.sum(s[:-1] * s[1:] < 0))
        if crossings:
            counts.append(crossings)
    return {"mean_multiplicity": float(np.mean(counts)),
            "max_multiplicity": int(np.max(counts)),
            "levels_sampled": len(counts)}


def main() -> int:
    results = {}
    for name, lam in (("integrable", 0.0), ("chaotic", 0.35)):
        curve, ref = evolve(lam)
        entry = {"lambda": lam,
                 "entropy_curve_every_40": curve,
                 "entropy_rise": curve[-1] - curve[0],
                 "late_slope_bits_per_tau": late_slope(curve),
                 "observers": {
                     "folding": multiplicity(ref, 0.0),
                     "monotone": multiplicity(ref, ALPHA_MONOTONE)}}
        results[name] = entry
        print(f"{name}: rise {entry['entropy_rise']:.3f} bits, late slope "
              f"{entry['late_slope_bits_per_tau']:.5f}; multiplicity "
              f"folding {entry['observers']['folding']['mean_multiplicity']:.2f} "
              f"vs monotone "
              f"{entry['observers']['monotone']['mean_multiplicity']:.2f}")

    slope_i = results["integrable"]["late_slope_bits_per_tau"]
    slope_c = results["chaotic"]["late_slope_bits_per_tau"]
    assert slope_c > slope_i, "chaotic dynamics should out-grow integrable"
    for name in ("integrable", "chaotic"):
        obs = results[name]["observers"]
        assert obs["folding"]["mean_multiplicity"] > 1.5, \
            f"folding observer should see multiplicity ({name})"
        assert obs["monotone"]["mean_multiplicity"] == 1.0, \
            f"monotone observer must see exactly one crossing ({name})"

    record = {
        "schema": "pe3-mixing-v1",
        "label": "exploratory",
        "declared": {"omega_t": OMEGA_T, "omega_u": OMEGA_U, "g": G_COUP,
                     "E": E_FIELD, "T": T_BATH, "dt": DT,
                     "tau_max": TAU_MAX, "n": N_ENS, "seed": SEED,
                     "eps": EPS, "alpha_monotone": ALPHA_MONOTONE,
                     "lambdas": {"integrable": 0.0, "chaotic": 0.35}},
        "results": results,
        "statement": "the two-by-two separates the mechanisms: ensemble "
            "entropy growth follows the dynamics (mixing) under either "
            "observer, slice multiplicity follows the observer's "
            "singularities under either dynamics, and the axes are "
            "independent",
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
    output = Path(__file__).resolve().parents[1] / "results" \
        / "pe3-mixing.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
