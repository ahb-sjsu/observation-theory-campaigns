#!/usr/bin/env python3
"""FT-2 consumer-relative restoration (exploratory).

Protocol declared in FLUCTUATION-TRACK.md before this run. A
budgeted consumer replaces its naive apparent work with the Bayes
work estimate through its declared detector model, minus the log
conditional expectation of exp(-W) given its record. The tower
property makes the restored identity exact with the true model,
and a misdeclared model must fail to restore it. Verdict computed
from the measured items.

Exploratory label. No claim about laboratory thermodynamics.
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

from ft0_instrument import (  # noqa: E402
    T_STEPS, energies, equilibrium, free_energy, path_data)
from projection_fold import canonical_sha256  # noqa: E402


def wrong_kernel(e, beta=0.9):
    n = len(e)
    m = np.zeros((n, n))
    for s in range(n):
        for sp in range(n):
            if sp != s:
                m[s, sp] = 0.5 * min(1.0,
                                     np.exp(-beta * (e[sp] - e[s])))
        m[s, s] = 1.0 - m[s].sum()
    return m


def path_probs_with(kernels, pi0, paths):
    probs = np.empty(len(paths))
    for i, p in enumerate(paths):
        pr = pi0[p[0]]
        for k in range(1, T_STEPS + 1):
            pr *= kernels[k - 1][p[k - 1], p[k]]
        probs[i] = pr
    return probs


def restored_defect(paths, probs, works, rec_of_path, model_probs):
    """<exp(-Wtilde)> - exp(-dF) with Wtilde from the model's
    conditional expectation of exp(-W) given the record."""
    num: dict = {}
    den: dict = {}
    for i, p in enumerate(paths):
        rec = rec_of_path(p)
        num[rec] = num.get(rec, 0.0) + model_probs[i] \
            * np.exp(-works[i])
        den[rec] = den.get(rec, 0.0) + model_probs[i]
    est = {rec: num[rec] / den[rec] for rec in num if den[rec] > 0}
    return float(sum(probs[i] * est[rec_of_path(p)]
                     for i, p in enumerate(paths)))


def main() -> int:
    record: dict = {"schema": "ft2-restoration-v1",
                    "label": "exploratory"}
    items = {}
    protocol = [energies(k) for k in range(T_STEPS + 1)]
    df = free_energy(protocol[-1]) - free_energy(protocol[0])
    target = np.exp(-df)
    paths, probs, works = path_data(protocol)
    lump = {0: 0, 1: 0, 2: 1}

    def rec_lump(p):
        return tuple(lump[s] for s in p)

    def rec_held(p):
        return tuple(p[2 * (k // 2)] for k in range(0, T_STEPS + 1,
                                                    2))

    # E1 naive defects replicate FT-1
    def lump_e(e):
        return np.array([-np.log(np.exp(-e[0]) + np.exp(-e[1])),
                         e[2]])

    lprot = [lump_e(e) for e in protocol]
    w_naive_lump = np.array([
        sum(lprot[k][lump[p[k - 1]]] - lprot[k - 1][lump[p[k - 1]]]
            for k in range(1, T_STEPS + 1)) for p in paths])
    d_naive_lump = abs(float(np.sum(probs * np.exp(-w_naive_lump)))
                       - target)
    w_naive_held = np.array([
        sum(protocol[k][p[2 * ((k - 1) // 2)]]
            - protocol[k - 1][p[2 * ((k - 1) // 2)]]
            for k in range(1, T_STEPS + 1)) for p in paths])
    d_naive_held = abs(float(np.sum(probs * np.exp(-w_naive_held)))
                       - target)
    items["E1_naive_defects"] = (d_naive_lump >= 1e-5
                                 and d_naive_held >= 1e-3)

    # E2 restoration with the true model
    d_rest_lump = abs(restored_defect(paths, probs, works,
                                      rec_lump, probs) - target)
    d_rest_held = abs(restored_defect(paths, probs, works,
                                      rec_held, probs) - target)
    items["E2_restored_exact"] = (d_rest_lump <= 1e-12
                                  and d_rest_held <= 1e-12)

    # E3 no restoration by a wrong model
    wkernels = [wrong_kernel(protocol[k])
                for k in range(1, T_STEPS + 1)]
    wpi0 = equilibrium(protocol[0])
    wprobs = path_probs_with(wkernels, wpi0, paths)
    d_wrong = abs(restored_defect(paths, probs, works,
                                  rec_lump, wprobs) - target)
    items["E3_wrong_model_fails"] = d_wrong >= 1e-6

    record["measured"] = {
        "df": float(df),
        "naive_defect_lumped": float(d_naive_lump),
        "naive_defect_held": float(d_naive_held),
        "restored_defect_lumped": float(d_rest_lump),
        "restored_defect_held": float(d_rest_held),
        "wrong_model_restored_defect": float(d_wrong),
        "reading": "the fluctuation identity for a budgeted "
                   "consumer is an inference theorem, restored "
                   "exactly by lawful inference through the true "
                   "declared channel and by nothing less"}
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
        / "ft2-restoration.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("naive", d_naive_lump, d_naive_held,
          "restored", d_rest_lump, d_rest_held, "wrong", d_wrong)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
