#!/usr/bin/env python3
"""FT-0 exact path-space instrument layer (exploratory).

Protocol declared in FLUCTUATION-TRACK.md before this run. Three
states, declared linear energy protocol over eight steps at unit
inverse temperature, quench-then-relax Metropolis updates in
detailed balance with the current energies, equilibrium start, the
full path space enumerated exactly. Jarzynski on the ensemble,
Crooks path by path, the second law with its quasistatic control,
and the lumped-observer preview. Verdict computed from the measured
items.

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

from projection_fold import canonical_sha256  # noqa: E402

T_STEPS = 8
E0 = np.array([0.0, 0.5, 1.0])
E1 = np.array([1.0, 0.2, 0.0])


def energies(k):
    return E0 + (E1 - E0) * (k / T_STEPS)


def metropolis_kernel(e):
    """All-to-all proposal, propose each other state with 1/2."""
    n = len(e)
    m = np.zeros((n, n))
    for s in range(n):
        for sp in range(n):
            if sp != s:
                m[s, sp] = 0.5 * min(1.0, np.exp(-(e[sp] - e[s])))
        m[s, s] = 1.0 - m[s].sum()
    return m


def equilibrium(e):
    w = np.exp(-e)
    return w / w.sum()


def free_energy(e):
    return -float(np.log(np.exp(-e).sum()))


def path_data(protocol):
    """Enumerate all paths, return probabilities and work values.
    protocol is the list of energy vectors, stages 0..T."""
    kernels = [metropolis_kernel(protocol[k])
               for k in range(1, T_STEPS + 1)]
    pi0 = equilibrium(protocol[0])
    paths = list(itertools.product(range(3), repeat=T_STEPS + 1))
    probs = np.empty(len(paths))
    works = np.empty(len(paths))
    for i, path in enumerate(paths):
        p = pi0[path[0]]
        w = 0.0
        for k in range(1, T_STEPS + 1):
            w += protocol[k][path[k - 1]] \
                - protocol[k - 1][path[k - 1]]
            p *= kernels[k - 1][path[k - 1], path[k]]
        probs[i] = p
        works[i] = w
    return paths, probs, works


def main() -> int:
    record: dict = {"schema": "ft0-instrument-v1",
                    "label": "exploratory"}
    items = {}
    fwd_protocol = [energies(k) for k in range(T_STEPS + 1)]
    df = free_energy(fwd_protocol[-1]) - free_energy(fwd_protocol[0])

    paths, probs, works = path_data(fwd_protocol)
    items_dev = abs(float(np.sum(probs * np.exp(-works)))
                    - np.exp(-df))
    items["C1_jarzynski"] = items_dev <= 1e-12

    # C2 Crooks path by path. The reverse of quench-then-relax is
    # relax-then-quench, so the reverse process runs the SAME
    # detailed-balance kernels in reversed order with transposed
    # indices, starting from the final equilibrium.
    kernels = [metropolis_kernel(fwd_protocol[k])
               for k in range(1, T_STEPS + 1)]
    pi_t = equilibrium(fwd_protocol[-1])
    dev2 = 0.0
    for i, path in enumerate(paths):
        pr = pi_t[path[-1]]
        for k in range(T_STEPS, 0, -1):
            pr *= kernels[k - 1][path[k], path[k - 1]]
        dev2 = max(dev2, abs(probs[i] * np.exp(-works[i])
                             - pr * np.exp(-df)))
    items["C2_crooks_per_path"] = dev2 <= 1e-12

    # C3 second law and quasistatic control
    mean_w = float(np.sum(probs * works))
    frozen = [E0.copy() for _ in range(T_STEPS + 1)]
    _, fprobs, fworks = path_data(frozen)
    frozen_dev = max(abs(float(np.sum(fprobs * fworks))),
                     float(np.max(np.abs(fworks))))
    items["C3_second_law"] = (mean_w >= df and frozen_dev <= 1e-14)

    # C4 lumped-observer preview, merge states 0 and 1
    def lump_e(e):
        return np.array([-np.log(np.exp(-e[0]) + np.exp(-e[1])),
                         e[2]])

    lump = {0: 0, 1: 0, 2: 1}
    lprot = [lump_e(e) for e in fwd_protocol]
    app_w = np.empty(len(paths))
    for i, path in enumerate(paths):
        w = 0.0
        for k in range(1, T_STEPS + 1):
            o = lump[path[k - 1]]
            w += lprot[k][o] - lprot[k - 1][o]
        app_w[i] = w
    ldf = (-np.log(np.exp(-lprot[-1]).sum())) \
        - (-np.log(np.exp(-lprot[0]).sum()))
    defect = abs(float(np.sum(probs * np.exp(-app_w)))
                 - np.exp(-ldf))
    record["C4_preview"] = {
        "lumped_df": float(ldf), "true_df": float(df),
        "jarzynski_defect": float(defect),
        "note": "measurement, no bar, the FT-1 seed"}

    record["measured"] = {
        "df": float(df), "c1_dev": float(items_dev),
        "c2_max_path_dev": float(dev2),
        "mean_work": mean_w,
        "dissipation": float(mean_w - df),
        "frozen_dev": float(frozen_dev),
        "n_paths": len(paths)}
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
        / "ft0-instrument.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("df", df, "mean W", mean_w, "defect", defect)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
