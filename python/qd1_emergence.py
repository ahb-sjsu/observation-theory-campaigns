#!/usr/bin/env python3
"""QD-1 emergence gate for redundancy (exploratory).

Protocol declared in QUANTUM-DARWINISM-TRACK.md before this run.
Basis-carrying dynamics, controlled rotations of declared angle,
evolved by explicit gate application and checked against the QD-0
branching closed form with nothing fitted. Basis-free dynamics,
seeded Haar-random two-qubit unitaries with matched entangling
power. Redundancy is declared-or-absent. Verdict computed from the
measured items.

Exploratory label. No claim about laboratory classicality.
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
from qd0_instrument import (  # noqa: E402
    NENV, NQ, entropy_bits, h2, mi_sf, reduced)


def apply_two_qubit(psi, u, qa, qb):
    """Apply 4x4 unitary u to qubits (qa, qb) of the state."""
    t = psi.reshape([2] * NQ)
    perm = [qa, qb] + [q for q in range(NQ) if q not in (qa, qb)]
    t = np.transpose(t, perm)
    t = (u @ t.reshape(4, -1)).reshape([2, 2] + [2] * (NQ - 2))
    inv = np.argsort(perm)
    return np.transpose(t, inv).reshape(-1)


def controlled_ry(theta):
    c, s = np.cos(theta / 2.0), np.sin(theta / 2.0)
    u = np.eye(4, dtype=complex)
    u[2:, 2:] = np.array([[c, -s], [s, c]])
    return u


def haar_unitary(rng, dim=4):
    z = rng.normal(size=(dim, dim)) + 1j * rng.normal(
        size=(dim, dim))
    q, r = np.linalg.qr(z)
    return q * (np.diag(r) / np.abs(np.diag(r)))


def redundancy(psi):
    ss = entropy_bits(reduced(psi, [0]))
    if ss <= 1e-12:
        return 0, ss
    r = sum(1 for q in range(1, NQ)
            if mi_sf(psi, [q]) >= 0.9 * ss)
    return r, ss


def initial_state():
    plus = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2.0)
    psi = plus
    for _ in range(NENV):
        psi = np.kron(psi, np.array([1.0, 0.0], dtype=complex))
    return psi


def main() -> int:
    record: dict = {"schema": "qd1-emergence-v1",
                    "label": "exploratory"}
    items = {}
    thetas = [np.pi / 16, np.pi / 8, np.pi / 4, np.pi / 2, np.pi]

    dev_q1 = 0.0
    frag1 = []
    ladder = {}
    for theta in thetas:
        psi = initial_state()
        u = controlled_ry(theta)
        for j in range(1, NQ):
            psi = apply_two_qubit(psi, u, 0, j)
        c = float(np.cos(theta / 2.0))
        for f in range(1, NENV + 1):
            meas = mi_sf(psi, list(range(1, 1 + f)))
            pred = (h2((1 + c ** NENV) / 2) + h2((1 + c ** f) / 2)
                    - h2((1 + c ** (NENV - f)) / 2))
            dev_q1 = max(dev_q1, abs(meas - pred))
        r, ss = redundancy(psi)
        f1 = mi_sf(psi, [1])
        frag1.append(f1)
        ladder[f"{theta:.6f}"] = {
            "record_overlap_c": c, "system_entropy_bits": ss,
            "fragment1_mi_bits": float(f1), "redundancy": int(r)}
    items["Q1_closed_form"] = dev_q1 <= 1e-10
    items["Q2_monotone_records"] = all(
        frag1[i + 1] > frag1[i] for i in range(len(thetas) - 1))
    items["Q3_full_plateau"] = (
        ladder[f"{np.pi:.6f}"]["redundancy"] == 6)
    items["Q4_weak_records_no_redundancy"] = (
        ladder[f"{np.pi / 16:.6f}"]["redundancy"] == 0)

    rng = np.random.RandomState(20260813)
    psi = initial_state()
    for j in range(1, NQ):
        psi = apply_two_qubit(psi, haar_unitary(rng), 0, j)
    r_rand, ss_rand = redundancy(psi)
    items["Q5_basis_free_no_redundancy"] = (ss_rand >= 0.3
                                            and r_rand == 0)

    record["measured"] = {
        "q1_max_closed_form_dev": float(dev_q1),
        "theta_ladder": ladder,
        "basis_free": {"system_entropy_bits": float(ss_rand),
                       "redundancy": int(r_rand)},
        "matched_exhibit": "at theta = pi, S(S) = "
                           f"{ladder[f'{np.pi:.6f}']['system_entropy_bits']:.6f}"
                           f" with R = 6; basis-free S(S) = "
                           f"{ss_rand:.6f} with R = 0"}
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
        / "qd1-emergence.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("ladder", {k: v["redundancy"] for k, v in ladder.items()},
          "rand", r_rand, ss_rand)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
