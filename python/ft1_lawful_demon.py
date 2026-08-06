#!/usr/bin/env python3
"""FT-1 the lawful-demon audit (exploratory).

Protocol declared in FLUCTUATION-TRACK.md before this run. Four
declared observers of the FT-0 system, complete, lumped, held, and
blind. The complete and blind observers satisfy Jarzynski exactly,
the lumped observer breaks it by a definite measured amount, and
every restricted observer's defect is predicted exactly by the
observed-record process, route agreement between full path
enumeration and the exact hidden-Markov marginal. Verdict computed
from the measured items.

Exploratory label. No claim about laboratory thermodynamics.
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

from ft0_instrument import (  # noqa: E402
    T_STEPS, energies, equilibrium, free_energy, metropolis_kernel,
    path_data)
from projection_fold import canonical_sha256  # noqa: E402


def main() -> int:
    record: dict = {"schema": "ft1-lawful-demon-v1",
                    "label": "exploratory"}
    items = {}
    protocol = [energies(k) for k in range(T_STEPS + 1)]
    df = free_energy(protocol[-1]) - free_energy(protocol[0])
    kernels = [metropolis_kernel(protocol[k])
               for k in range(1, T_STEPS + 1)]
    pi0 = equilibrium(protocol[0])
    paths, probs, works = path_data(protocol)

    # complete observer
    d_full = abs(float(np.sum(probs * np.exp(-works)))
                 - np.exp(-df))
    items["L1_complete_zero"] = d_full <= 1e-14

    # blind observer, apparent work telescopes to df
    w_blind = sum(free_energy(protocol[k])
                  - free_energy(protocol[k - 1])
                  for k in range(1, T_STEPS + 1))
    d_blind = abs(np.exp(-w_blind) - np.exp(-df))
    items["L2_blind_zero"] = d_blind <= 1e-14

    # lumped observer, merge states 0 and 1
    lump = {0: 0, 1: 0, 2: 1}

    def lump_e(e):
        return np.array([-np.log(np.exp(-e[0]) + np.exp(-e[1])),
                         e[2]])

    lprot = [lump_e(e) for e in protocol]

    def w_lump(sym_path):
        w = 0.0
        for k in range(1, T_STEPS + 1):
            w += lprot[k][sym_path[k - 1]] \
                - lprot[k - 1][sym_path[k - 1]]
        return w

    exp_lump_paths = float(np.sum(
        probs * np.exp(-np.array([w_lump([lump[s] for s in p])
                                  for p in paths]))))
    # route two, exact marginal over observed records by filtering
    exp_lump_hmm = 0.0
    for rec in itertools.product((0, 1), repeat=T_STEPS + 1):
        alpha = pi0 * np.array([lump[s] == rec[0]
                                for s in range(3)])
        for k in range(1, T_STEPS + 1):
            sel = np.array([lump[s] == rec[k] for s in range(3)])
            alpha = (alpha @ kernels[k - 1]) * sel
        p_rec = float(alpha.sum())
        if p_rec > 0:
            exp_lump_hmm += p_rec * np.exp(-w_lump(rec))
    d_lump = abs(exp_lump_paths - np.exp(-df))
    route_lump = abs(exp_lump_paths - exp_lump_hmm)
    items["L3_lumped_broken"] = d_lump >= 1e-5

    # held observer, reads only even stages, holds the last reading
    def held_states(p):
        return [p[2 * (k // 2)] for k in range(T_STEPS + 1)]

    def w_held(held):
        w = 0.0
        for k in range(1, T_STEPS + 1):
            w += protocol[k][held[k - 1]] \
                - protocol[k - 1][held[k - 1]]
        return w

    exp_held_paths = float(np.sum(
        probs * np.exp(-np.array([w_held(held_states(p))
                                  for p in paths]))))
    exp_held_hmm = 0.0
    for rec in itertools.product(range(3),
                                 repeat=T_STEPS // 2 + 1):
        alpha = pi0 * (np.arange(3) == rec[0])
        for k in range(1, T_STEPS + 1):
            alpha = alpha @ kernels[k - 1]
            if k % 2 == 0:
                alpha = alpha * (np.arange(3) == rec[k // 2])
        p_rec = float(alpha.sum())
        if p_rec > 0:
            held = [rec[k // 2] for k in range(T_STEPS + 1)]
            exp_held_hmm += p_rec * np.exp(-w_held(held))
    d_held = abs(exp_held_paths - np.exp(-df))
    route_held = abs(exp_held_paths - exp_held_hmm)
    items["L4_route_agreement"] = (route_lump <= 1e-12
                                   and route_held <= 1e-12)

    record["measured"] = {
        "df": float(df),
        "defect_complete": float(d_full),
        "defect_blind": float(d_blind),
        "defect_lumped": float(d_lump),
        "defect_held": float(d_held),
        "route_dev_lumped": float(route_lump),
        "route_dev_held": float(route_held),
        "mean_apparent_work": {
            "complete": float(np.sum(probs * works)),
            "lumped": float(np.sum(probs * np.array(
                [w_lump([lump[s] for s in p]) for p in paths]))),
            "held": float(np.sum(probs * np.array(
                [w_held(held_states(p)) for p in paths]))),
            "blind": float(w_blind)},
        "reading": "the defect lives strictly between full sight "
                   "and total blindness"}
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
        / "ft1-lawful-demon.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("defects", d_full, d_lump, d_held, d_blind)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
