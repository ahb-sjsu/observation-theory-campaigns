#!/usr/bin/env python3
"""QD-0 exact fragment-information instrument layer (exploratory).

Protocol declared in QUANTUM-DARWINISM-TRACK.md before this run.
One system qubit, six environment qubits, pure states, exact
reduced density matrices and von Neumann entropies, I(S:F) per
fragment size. Product, GHZ, partial-record closed form, and
Haar-random no-plateau controls. Verdict computed from the
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

NENV = 6
NQ = NENV + 1  # system is qubit 0


def entropy_bits(rho):
    ev = np.linalg.eigvalsh(rho)
    ev = ev[ev > 1e-14]
    return float(-np.sum(ev * np.log2(ev)))


def reduced(psi, keep):
    """Reduced density matrix on the qubit list `keep`."""
    t = psi.reshape([2] * NQ)
    drop = [q for q in range(NQ) if q not in keep]
    perm = list(keep) + drop
    t = np.transpose(t, perm)
    a = t.reshape(2 ** len(keep), 2 ** len(drop))
    return a @ a.conj().T


def mi_sf(psi, frag):
    rs = reduced(psi, [0])
    rf = reduced(psi, list(frag))
    rsf = reduced(psi, [0] + list(frag))
    return entropy_bits(rs) + entropy_bits(rf) - entropy_bits(rsf)


def h2(p):
    q = 1.0 - p
    out = 0.0
    if p > 0:
        out -= p * np.log2(p)
    if q > 0:
        out -= q * np.log2(q)
    return float(out)


def branching_state(c):
    """(|0>|phi0..> + |1>|phi1..>)/sqrt(2), <phi0|phi1> = c."""
    alpha = np.arccos(c)
    phi0 = np.array([1.0, 0.0])
    phi1 = np.array([np.cos(alpha), np.sin(alpha)])
    b0 = np.array([1.0, 0.0])
    b1 = np.array([0.0, 1.0])
    t0 = b0
    t1 = b1
    for _ in range(NENV):
        t0 = np.kron(t0, phi0)
        t1 = np.kron(t1, phi1)
    return (t0 + t1) / np.sqrt(2.0)


def main() -> int:
    record: dict = {"schema": "qd0-instrument-v1",
                    "label": "exploratory"}
    items = {}
    frags = {f: list(range(1, 1 + f)) for f in range(1, NENV + 1)}

    # C1 product control
    psi = np.zeros(2 ** NQ)
    plus = np.array([1.0, 1.0]) / np.sqrt(2.0)
    t = plus
    for _ in range(NENV):
        t = np.kron(t, np.array([1.0, 0.0]))
    psi = t
    dev1 = max(abs(mi_sf(psi, frags[f])) for f in frags)
    items["C1_product_zero"] = dev1 <= 1e-12

    # C2 GHZ classical plateau
    ghz = np.zeros(2 ** NQ)
    ghz[0] = 1.0 / np.sqrt(2.0)
    ghz[-1] = 1.0 / np.sqrt(2.0)
    dev2 = max(abs(mi_sf(ghz, frags[f]) - 1.0)
               for f in range(1, NENV))
    dev2 = max(dev2, abs(mi_sf(ghz, frags[NENV]) - 2.0))
    items["C2_ghz_plateau"] = dev2 <= 1e-10

    # C3 partial-record closed form, c = 1/2
    c = 0.5
    psi3 = branching_state(c)
    dev3 = 0.0
    mi_curve = []
    for f in range(1, NENV + 1):
        meas = mi_sf(psi3, frags[f])
        pred = (h2((1 + c ** NENV) / 2) + h2((1 + c ** f) / 2)
                - h2((1 + c ** (NENV - f)) / 2))
        dev3 = max(dev3, abs(meas - pred))
        mi_curve.append(float(meas))
    items["C3_partial_record_closed_form"] = dev3 <= 1e-10

    # C4 Haar-random no plateau
    rng = np.random.RandomState(20260810)
    v = rng.normal(size=2 ** NQ) + 1j * rng.normal(size=2 ** NQ)
    v /= np.linalg.norm(v)
    ss = entropy_bits(reduced(v, [0]))
    singles = [mi_sf(v, [q]) for q in range(1, NQ)]
    full = mi_sf(v, list(range(1, NQ)))
    items["C4_no_plateau"] = (float(np.mean(singles)) <= 0.15
                              and abs(full - 2 * ss) <= 1e-10)

    record["measured"] = {
        "c1_max_mi": float(dev1), "c2_max_dev": float(dev2),
        "c3_max_dev": float(dev3),
        "c3_mi_curve_bits": mi_curve,
        "c4_mean_single_fragment_mi": float(np.mean(singles)),
        "c4_full_env_mi_minus_2S": float(full - 2 * ss),
        "c4_system_entropy_bits": float(ss)}
    record["items"] = {k: bool(x) for k, x in items.items()}
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
        {k: x for k, x in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "qd0-instrument.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("mi curve", np.round(mi_curve, 4))
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
