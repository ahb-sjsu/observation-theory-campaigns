#!/usr/bin/env python3
"""RG-4 relevance as a channel property (exploratory).

Protocol declared in RENORMALIZATION-TRACK.md before this run.
Field and next-nearest perturbations of strength 1e-4 to the
nearest-neighbor Ising 12-ring at K = 0.6, flowed through
decimation and majority-of-three, coarse parameters solved exactly
by Newton on the small ring, response multipliers compared across
channels. Verdict computed from the measured items.

Exploratory label. No claim about material systems.
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
from rg3_universality import (  # noqa: E402
    configs, decimate, majority3, model_probs)

K0 = 0.6
DELTA = 1e-4


def observables(n, p):
    c = configs(n).astype(np.float64)
    c1 = float(np.sum(p * (c[:, 0] * c[:, 1])))
    c2 = float(np.sum(p * (c[:, 0] * c[:, 2 % n])))
    m = float(np.sum(p * c.mean(axis=1)))
    return np.array([c1, c2, m])


def fit_params(n, target):
    theta = np.array([0.3, 0.0, 0.0])
    for _ in range(80):
        f = observables(n, model_probs(n, *theta)) - target
        if np.max(np.abs(f)) < 1e-13:
            break
        jac = np.zeros((3, 3))
        for j in range(3):
            tp = theta.copy()
            tp[j] += 1e-7
            jac[:, j] = (observables(n, model_probs(n, *tp))
                         - f - target) / 1e-7
        theta = theta - np.linalg.solve(jac, f)
    return theta


def coarse_params(channel, j1, j2, h):
    p = model_probs(12, j1, j2, h)
    if channel == "dec":
        q = decimate(12, p)
        return fit_params(6, observables(6, q))
    q = majority3(12, p)
    return fit_params(4, observables(4, q))


def main() -> int:
    record: dict = {"schema": "rg4-relevance-v1",
                    "label": "exploratory"}
    items = {}
    mult = {}
    lin_dev = 0.0
    for channel in ("dec", "maj"):
        base = coarse_params(channel, K0, 0.0, 0.0)
        for name, pj2, ph in (("h", 0.0, DELTA),
                              ("j2", DELTA, 0.0)):
            pert = coarse_params(channel, K0, pj2, ph)
            half = coarse_params(channel, K0, pj2 / 2, ph / 2)
            idx = 2 if name == "h" else 1
            lam = (pert[idx] - base[idx]) / DELTA
            lam_half = (half[idx] - base[idx]) / (DELTA / 2)
            mult[f"{name}_{channel}"] = float(lam)
            if abs(lam) > 1e-9:
                lin_dev = max(lin_dev, abs(lam_half / lam - 1.0))
    items["V1_linearity"] = lin_dev <= 1e-3
    diff_h = abs(mult["h_dec"] - mult["h_maj"]) / max(
        abs(mult["h_dec"]), abs(mult["h_maj"]))
    diff_j2 = abs(mult["j2_dec"] - mult["j2_maj"]) / max(
        abs(mult["j2_dec"]), abs(mult["j2_maj"]), 1e-300)
    items["V3_channel_borne"] = max(diff_h, diff_j2) >= 0.10
    signs_agree = {
        "h": (mult["h_dec"] > 1.0) == (mult["h_maj"] > 1.0),
        "j2": (abs(mult["j2_dec"]) < 1.0)
        == (abs(mult["j2_maj"]) < 1.0)}

    record["measured"] = {
        "multipliers": mult,
        "linearity_dev": float(lin_dev),
        "rel_diff_h": float(diff_h),
        "rel_diff_j2": float(diff_j2),
        "v4_growth_agreement": {k: bool(v)
                                for k, v in signs_agree.items()},
        "note": "V2 is the multiplier table itself, V4 is a "
                "measurement with no bar"}
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
        / "rg4-relevance.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("multipliers", mult)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
