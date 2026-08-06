#!/usr/bin/env python3
"""QD-3 multi-consumer agreement audit (exploratory).

Protocol declared in QUANTUM-DARWINISM-TRACK.md before this run.
Two consumers holding disjoint two-qubit fragments of branching
states perform their Helstrom-optimal branch discriminations, the
joint outcome distribution is exact Born arithmetic on two routes,
and agreement is manufactured by record strength. Verdict computed
from the measured items.

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
from qd0_instrument import NQ, reduced  # noqa: E402
from qd1_emergence import (  # noqa: E402
    apply_two_qubit, controlled_ry, initial_state)


def branch_pair(theta):
    a = np.arccos(np.cos(theta / 2.0))
    phi0 = np.array([1.0, 0.0])
    phi1 = np.array([np.cos(a), np.sin(a)])
    b0 = np.kron(phi0, phi0)
    b1 = np.kron(phi1, phi1)
    return b0, b1


def helstrom_projectors(b0, b1):
    delta = 0.5 * (np.outer(b0, b0) - np.outer(b1, b1))
    ev, vec = np.linalg.eigh(delta)
    pi0 = np.zeros((4, 4))
    for i in range(4):
        if ev[i] >= 0:
            pi0 += np.outer(vec[:, i], vec[:, i])
    return pi0, np.eye(4) - pi0


def embed(op, qubits):
    """Operator on the listed adjacent qubits, identity elsewhere."""
    full = np.array([[1.0]])
    q = 0
    while q < NQ:
        if q == qubits[0]:
            full = np.kron(full, op)
            q += len(qubits)
        else:
            full = np.kron(full, np.eye(2))
            q += 1
    return full


def main() -> int:
    record: dict = {"schema": "qd3-agreement-v1",
                    "label": "exploratory"}
    items = {}
    thetas = [np.pi / 16, np.pi / 8, np.pi / 4, np.pi / 2, np.pi]
    dev_j1 = 0.0
    dev_j2 = 0.0
    agree = []
    table = {}
    for theta in thetas:
        psi = initial_state()
        u = controlled_ry(theta)
        for j in range(1, NQ):
            psi = apply_two_qubit(psi, u, 0, j)
        b0, b1 = branch_pair(theta)
        pa0, pa1 = helstrom_projectors(b0, b1)
        c_f = float(np.cos(theta / 2.0)) ** 2
        p_pred = 0.5 * (1.0 + np.sqrt(1.0 - c_f ** 2))
        proj_s = [embed(np.diag([1.0, 0.0]), [0]),
                  embed(np.diag([0.0, 1.0]), [0])]
        proj_a = [embed(pa0, [1, 2]), embed(pa1, [1, 2])]
        proj_b = [embed(pa0, [3, 4]), embed(pa1, [3, 4])]
        for projs in (proj_a, proj_b):
            succ = sum(float(np.real(
                psi.conj() @ (proj_s[s] @ (projs[s] @ psi))))
                for s in range(2))
            dev_j1 = max(dev_j1, abs(succ - p_pred))
        p_joint = np.zeros((2, 2))
        for a in range(2):
            for b in range(2):
                p_joint[a, b] = float(np.real(
                    psi.conj() @ (proj_a[a] @ (proj_b[b] @ psi))))
        rho = reduced(psi, [1, 2, 3, 4])
        dev = 0.0
        for a in range(2):
            for b in range(2):
                op = np.kron([pa0, pa1][a], [pa0, pa1][b])
                dev = max(dev, abs(float(np.real(
                    np.trace(rho @ op))) - p_joint[a, b]))
        dev_j2 = max(dev_j2, dev)
        p_agree = float(p_joint[0, 0] + p_joint[1, 1])
        agree.append(p_agree)
        table[f"{theta:.6f}"] = {
            "helstrom_pred": float(p_pred),
            "p_agree": p_agree}
    items["J1_helstrom_closed_form"] = dev_j1 <= 1e-10
    items["J2_route_agreement"] = dev_j2 <= 1e-12
    items["J3_agreement_manufactured"] = (
        all(agree[i + 1] > agree[i] for i in range(len(agree) - 1))
        and agree[-1] >= 1.0 - 1e-10 and agree[0] <= 0.6)

    record["measured"] = {
        "j1_max_dev": float(dev_j1),
        "j2_max_dev": float(dev_j2),
        "table": table,
        "agreement_curve": [float(a) for a in agree],
        "reading": "objectivity between observers is record "
                   "strength made mechanical, every disagreement "
                   "rate is the declared channels' exact Born "
                   "arithmetic"}
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
        / "qd3-agreement.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("agreement", [round(a, 4) for a in agree])
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
