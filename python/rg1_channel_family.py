#!/usr/bin/env python3
"""RG-1 channel-family invariance of long-distance structure.

Protocol declared in RENORMALIZATION-TRACK.md before this run.
Width-4 Ising cylinder at K = 0.3, exact symmetric column transfer
matrix. Four declared channels, two odd (decimation, majority), two
even (pair product, parity). The measured decay rate of each
channel's connected correlator must equal its symmetry sector's
eigenvalue ratio, the channel selects which sector's invariant the
observer sees. Verdict computed from the measured items.

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

W = 4
K = 0.3


def main() -> int:
    record: dict = {"schema": "rg1-channel-family-v1",
                    "label": "exploratory"}
    items = {}
    states = list(itertools.product([-1, 1], repeat=W))
    n = len(states)

    def ring_e(s):
        return sum(s[i] * s[(i + 1) % W] for i in range(W))

    t_mat = np.empty((n, n))
    for a, sa in enumerate(states):
        for b, sb in enumerate(states):
            inter = sum(sa[i] * sb[i] for i in range(W))
            t_mat[a, b] = np.exp(K * inter
                                 + 0.5 * K * (ring_e(sa)
                                              + ring_e(sb)))
    # block-diagonalize by global-flip parity so degenerate momentum
    # pairs cannot mix sectors in the numerical eigenvectors
    flip = np.array([states.index(tuple(-x for x in s))
                     for s in states])
    reps = [i for i in range(n) if i < flip[i]]
    basis_even = np.zeros((n, len(reps)))
    basis_odd = np.zeros((n, len(reps)))
    for col, i in enumerate(reps):
        basis_even[i, col] = basis_even[flip[i], col] = \
            1.0 / np.sqrt(2.0)
        basis_odd[i, col] = 1.0 / np.sqrt(2.0)
        basis_odd[flip[i], col] = -1.0 / np.sqrt(2.0)
    te = basis_even.T @ t_mat @ basis_even
    to = basis_odd.T @ t_mat @ basis_odd
    ee, ve = np.linalg.eigh(te)
    eo, vo = np.linalg.eigh(to)
    evals = np.concatenate([ee, eo])
    evecs = np.concatenate([basis_even @ ve, basis_odd @ vo],
                           axis=1)
    parity = np.array([1] * len(reps) + [-1] * len(reps))
    order = np.argsort(evals)[::-1]
    evals, evecs, parity = (evals[order], evecs[:, order],
                            parity[order])
    lam1 = evals[0]
    v1 = evecs[:, 0]
    assert parity[0] == 1, "ground state must be even"
    lam_odd = max(evals[i] for i in range(1, n) if parity[i] == -1)
    lam_even2 = max(evals[i] for i in range(1, n)
                    if parity[i] == 1)

    def maj(s):
        t = sum(s)
        return float(np.sign(t)) if t != 0 else float(s[0])

    channels = {
        "decimation": np.array([s[0] for s in states], float),
        "majority": np.array([maj(s) for s in states]),
        "pair": np.array([s[0] * s[1] for s in states], float),
        "parity": np.array([s[0] * s[1] * s[2] * s[3]
                            for s in states], float)}
    def corr_eigen(f, d):
        amps = np.array([np.sum(v1 * f * evecs[:, i])
                         for i in range(1, n)])
        return float(np.sum((evals[1:] / lam1) ** d * amps ** 2))

    def corr_direct(f, d):
        vec = v1 * f
        for _ in range(d):
            vec = t_mat @ vec / lam1
        mean = float(np.sum(v1 * f * v1))
        return float(np.sum(vec * f * v1)) - mean ** 2

    chan_parity = {"decimation": -1, "majority": -1,
                   "pair": 1, "parity": 1}
    dev_route = 0.0
    leakage = {}
    lead_amp = {}
    amps1 = {}
    for name, f in channels.items():
        for d in range(8, 17):
            ce = corr_eigen(f, d)
            cd = corr_direct(f, d)
            dev_route = max(dev_route,
                            abs(ce - cd) / max(abs(ce), 1e-300))
        amps = np.array([np.sum(v1 * f * evecs[:, i])
                         for i in range(n)])
        wrong = [abs(amps[i]) for i in range(1, n)
                 if parity[i] != chan_parity[name]]
        leakage[name] = max(wrong)
        sector = [(evals[i], abs(amps[i])) for i in range(1, n)
                  if parity[i] == chan_parity[name]]
        lead = max(sector)[0]
        lead_amp[name] = max(a for e, a in sector
                             if abs(e - lead) < 1e-12)
        amps1[name] = corr_eigen(f, 8)
    items["B0_route_agreement"] = dev_route <= 1e-10
    items["B1_odd_sector"] = all(
        leakage[c] <= 1e-12 and lead_amp[c] >= 1e-6
        for c in ("decimation", "majority"))
    items["B2_even_sector"] = all(
        leakage[c] <= 1e-12 and lead_amp[c] >= 1e-6
        for c in ("pair", "parity"))
    xi_odd = -1.0 / np.log(lam_odd / lam1)
    xi_even = -1.0 / np.log(lam_even2 / lam1)
    items["B3_sectors_differ"] = (abs(lam_odd - lam_even2)
                                  / lam1 >= 1e-3)

    record["measured"] = {
        "lam1": float(lam1), "lam_odd": float(lam_odd),
        "lam_even2": float(lam_even2),
        "xi_odd": float(xi_odd), "xi_even": float(xi_even),
        "xi_ratio": float(xi_odd / xi_even),
        "cross_sector_leakage": {k: float(v)
                                 for k, v in leakage.items()},
        "leading_amplitude": {k: float(v)
                              for k, v in lead_amp.items()},
        "route_rel_dev": float(dev_route),
        "amplitude_at_d8": {k: float(v) for k, v in amps1.items()},
        "note_b4": "amplitudes within a sector differ across "
                   "channels, spread recorded, no bar"}
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
        / "rg1-channel-family.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("xi_odd", xi_odd, "xi_even", xi_even)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
