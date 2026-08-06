#!/usr/bin/env python3
"""RG-0 exact coarse-graining instrument layer (exploratory).

Protocol declared in RENORMALIZATION-TRACK.md before this run.
One-dimensional Ising ring, exact by transfer matrix and by full
enumeration. Decimation is exactly in-family with the closed-form
coupling flow, majority-rule blocking measurably leaves the
nearest-neighbor family, the same substrate is representable or not
depending only on the declared channel. Verdict computed from the
measured items.

Exploratory label. No claim about material systems.
"""
from __future__ import annotations

import itertools
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from projection_fold import canonical_sha256  # noqa: E402


def ring_configs(n):
    return list(itertools.product([-1, 1], repeat=n))


def ring_probs(n, k):
    """Exact Boltzmann distribution of the n-ring at coupling k."""
    cfgs = ring_configs(n)
    w = np.array([np.exp(k * sum(c[i] * c[(i + 1) % n]
                                 for i in range(n)))
                  for c in cfgs])
    return cfgs, w / w.sum()


def free_energy_tm(n, k):
    lam1 = 2.0 * np.cosh(k)
    lam2 = 2.0 * np.sinh(k)
    return float(np.log(lam1 ** n + lam2 ** n))


def xi(k):
    return -1.0 / np.log(np.tanh(k))


def ring4_correlators(k):
    """Exact nearest and next-nearest correlators on the 4-ring."""
    t = np.tanh(k)
    c1 = (t + t ** 3) / (1.0 + t ** 4)
    c2 = 2.0 * t ** 2 / (1.0 + t ** 4)
    return float(c1), float(c2)


def main() -> int:
    record: dict = {"schema": "rg0-instrument-v1",
                    "label": "exploratory"}
    items = {}

    # C1 route agreement
    dev1 = 0.0
    for k in (0.3, 0.7):
        cfgs, p = ring_probs(12, k)
        w = np.array([np.exp(k * sum(c[i] * c[(i + 1) % 12]
                                     for i in range(12)))
                      for c in cfgs])
        dev1 = max(dev1, abs(np.log(w.sum())
                             - free_energy_tm(12, k)))
    items["C1_route_agreement"] = dev1 <= 1e-12

    # C2 decimation exactness at K = 0.5
    k = 0.5
    kp = float(np.arctanh(np.tanh(k) ** 2))
    cfgs12, p12 = ring_probs(12, k)
    coarse: dict = {}
    for c, pr in zip(cfgs12, p12):
        key = tuple(c[0::2])
        coarse[key] = coarse.get(key, 0.0) + pr
    cfgs6, p6 = ring_probs(6, kp)
    dev2 = max(abs(coarse[tuple(c)] - pr)
               for c, pr in zip(cfgs6, p6))
    items["C2_decimation_exact"] = dev2 <= 1e-12

    # C3 correlation-length flow
    dev3 = abs(xi(kp) - xi(k) / 2.0)
    items["C3_xi_flow"] = dev3 <= 1e-12

    # C4 channel dependence of representability at K = 0.6
    k4 = 0.6
    cfgs12b, p12b = ring_probs(12, k4)
    cmaj: dict = {}
    for c, pr in zip(cfgs12b, p12b):
        key = tuple(int(np.sign(c[3 * b] + c[3 * b + 1]
                                + c[3 * b + 2]))
                    for b in range(4))
        cmaj[key] = cmaj.get(key, 0.0) + pr
    keys = list(itertools.product([-1, 1], repeat=4))
    pm = np.array([cmaj.get(tuple(c), 0.0) for c in keys])
    c1_meas = float(sum(pr * c[0] * c[1]
                        for c, pr in zip(keys, pm)))
    c2_meas = float(sum(pr * c[0] * c[2]
                        for c, pr in zip(keys, pm)))
    lo, hi = 1e-6, 5.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if ring4_correlators(mid)[0] < c1_meas:
            lo = mid
        else:
            hi = mid
    keff = 0.5 * (lo + hi)
    resid_maj = abs(ring4_correlators(keff)[1] - c2_meas)
    # decimation residual for the same substrate, full distribution
    kp4 = float(np.arctanh(np.tanh(k4) ** 2))
    cdec: dict = {}
    for c, pr in zip(cfgs12b, p12b):
        key = tuple(c[0::2])
        cdec[key] = cdec.get(key, 0.0) + pr
    cfgs6b, p6b = ring_probs(6, kp4)
    resid_dec = max(abs(cdec[tuple(c)] - pr)
                    for c, pr in zip(cfgs6b, p6b))
    items["C4_channel_representability"] = (resid_maj >= 1e-4
                                            and resid_dec <= 1e-12)

    # C5 flow composition
    kpp_direct = float(np.arctanh(np.tanh(k) ** 4))
    kpp_two = float(np.arctanh(np.tanh(kp) ** 2))
    dev5 = abs(kpp_direct - kpp_two)
    items["C5_flow_composition"] = dev5 <= 1e-12

    record["measured"] = {
        "c1_dev": float(dev1), "c2_dev": float(dev2),
        "c3_dev": float(dev3),
        "c4_majority_nnn_residual": float(resid_maj),
        "c4_decimation_residual": float(resid_dec),
        "c4_fitted_keff": float(keff),
        "c5_dev": float(dev5),
        "k_prime_of_0.5": kp}
    record["items"] = {kk: bool(v) for kk, v in items.items()}
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
        {kk: v for kk, v in record.items() if kk != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "rg0-instrument.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("majority nnn residual", resid_maj,
          "decimation residual", resid_dec)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
