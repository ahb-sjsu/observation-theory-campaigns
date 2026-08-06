#!/usr/bin/env python3
"""QD-1b emergence gate, corrected basis-free control.

Identical to QD-1 except the basis-free control, now a seeded
Haar-random pure state of all seven qubits, globally scrambled with
no interaction schedule. QD-1's sequential control was itself
structure, its causal order imprinted a recency record on the
last-touched qubit, recorded there as a finding.

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
from qd0_instrument import NENV, NQ, h2, mi_sf  # noqa: E402
from qd1_emergence import (  # noqa: E402
    apply_two_qubit, controlled_ry, initial_state, redundancy)


def main() -> int:
    record: dict = {"schema": "qd1b-emergence-v1",
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

    # corrected basis-free control, a global Haar state
    rng = np.random.RandomState(20260813)
    v = rng.normal(size=2 ** NQ) + 1j * rng.normal(size=2 ** NQ)
    v /= np.linalg.norm(v)
    r_rand, ss_rand = redundancy(v)
    items["Q5_basis_free_no_redundancy"] = (ss_rand >= 0.3
                                            and r_rand == 0)

    record["measured"] = {
        "q1_max_closed_form_dev": float(dev_q1),
        "theta_ladder": ladder,
        "basis_free_global_haar": {
            "system_entropy_bits": float(ss_rand),
            "redundancy": int(r_rand)},
        "correction": "the basis-free control is a global Haar "
                      "state, QD-1's sequential control was "
                      "structure, its causal order imprinted a "
                      "recency record (R = 1) on the last-touched "
                      "qubit, recorded as a finding"}
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
        {k: vv for k, vv in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "qd1b-emergence.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("haar", ss_rand, r_rand)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
