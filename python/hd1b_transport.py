#!/usr/bin/env python3
"""HD-1b transport, the spurious invariants made exact bars.

Protocol declared in HYDRODYNAMICS-TRACK.md before this run. HD-1
measured a shear mode that did not decay at all, decay ratio
exactly 1.0, because HPP conserves the transverse momentum of every
column and the longitudinal momentum of every row separately.
HD-1b measures those two spurious invariants as exact integer
conservation laws at every step, keeps HD-1's sound bars, and
withdraws the diffusive-scaling bar as unmeasurable on this
substrate, viscosity moves to the FHP design of HD-2.

Exploratory label. No claim about physical fluids.
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

from hd1_transport import (  # noqa: E402
    AMP, F0, L, M, T, crossings_omega, sine, step)
from projection_fold import canonical_sha256  # noqa: E402


def main() -> int:
    record: dict = {"schema": "hd1b-transport-v1",
                    "label": "exploratory"}
    items = {}

    # S1 the two spurious invariants, shear ensemble, k = 1
    rng = np.random.RandomState(20260815)
    s = sine(1)[None, None, :]
    p = np.full((4, M, L, L), F0)
    p[1] = F0 + AMP * s
    p[3] = F0 - AMP * s
    n = rng.random((4, M, L, L)) < p
    col_py0 = (n[1].astype(np.int64)
               - n[3].astype(np.int64)).sum(axis=1)
    row_px0 = (n[0].astype(np.int64)
               - n[2].astype(np.int64)).sum(axis=2)
    ok_col = ok_row = True
    for _ in range(T):
        n = step(n)
        col_py = (n[1].astype(np.int64)
                  - n[3].astype(np.int64)).sum(axis=1)
        row_px = (n[0].astype(np.int64)
                  - n[2].astype(np.int64)).sum(axis=2)
        ok_col = ok_col and np.array_equal(col_py, col_py0)
        ok_row = ok_row and np.array_equal(row_px, row_px0)
    items["S1_spurious_invariants_exact"] = bool(ok_col and ok_row)

    # S2 sound bars, unchanged from HD-1
    sound = {}
    cons_all = True
    for k in (1, 2):
        rng = np.random.RandomState(20260816 + k)
        p = np.full((4, M, L, L), F0) + AMP * sine(k)[None, None, :]
        n = rng.random((4, M, L, L)) < p
        inv0 = (int(n.sum()), int(n[0].sum() - n[2].sum()),
                int(n[1].sum() - n[3].sum()))
        proj = sine(k)[None, :]
        amps = []
        for _ in range(T + 1):
            field = n.astype(np.int32).sum(axis=0).sum(axis=1)
            amps.append(float((field * proj).sum(axis=1).mean()
                              * 2.0 / L))
            n = step(n)
            cons_all = cons_all and (
                int(n.sum()), int(n[0].sum() - n[2].sum()),
                int(n[1].sum() - n[3].sum())) == inv0
        omega = crossings_omega(np.array(amps))
        kp = 2 * np.pi * k / L
        sound[k] = {"omega": float(omega),
                    "c_over_pred": float(omega
                                         / (kp / np.sqrt(2.0)))}
    wratio = sound[2]["omega"] / sound[1]["omega"]
    items["S2_sound_dispersion"] = (
        0.85 <= sound[1]["c_over_pred"] <= 1.15
        and 1.85 <= wratio <= 2.15)
    items["S3_conservation"] = bool(cons_all)

    record["measured"] = {
        "column_py_exactly_conserved": bool(ok_col),
        "row_px_exactly_conserved": bool(ok_row),
        "sound": {str(k): v for k, v in sound.items()},
        "sound_freq_ratio": float(wratio),
        "withdrawn": "diffusive-scaling bar unmeasurable on HPP, "
                     "the spurious invariants freeze shear, "
                     "viscosity moves to the FHP design of HD-2"}
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
        / "hd1b-transport.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("sound", sound)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
