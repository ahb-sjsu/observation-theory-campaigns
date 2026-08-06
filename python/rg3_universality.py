#!/usr/bin/env python3
"""RG-3 the universality gate (exploratory).

Protocol declared in RENORMALIZATION-TRACK.md before this run.
Three microscopic models under declared channels, the family
residual is total-variation distance from the best nearest-neighbor
Ising fit. Decimation flows M1 exactly in-family and M2 toward it,
symmetry classes do not mix, and the same substrate flows out of
the family under majority blocking. Verdict computed from the
measured items.

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


def configs(n):
    idx = np.arange(2 ** n, dtype=np.int64)
    bits = (idx[:, None] >> np.arange(n)) & 1
    return (1 - 2 * bits).astype(np.int8)


def model_probs(n, j1, j2, h):
    c = configs(n).astype(np.float64)
    e = (j1 * (c * np.roll(c, -1, axis=1)).sum(axis=1)
         + j2 * (c * np.roll(c, -2, axis=1)).sum(axis=1)
         + h * c.sum(axis=1))
    w = np.exp(e)
    return w / w.sum()


def nn_probs(n, k):
    return model_probs(n, k, 0.0, 0.0)


def nn_corr(n, k):
    t = np.tanh(k)
    return (t + t ** (n - 1)) / (1 + t ** n)


def measured_nn_corr(n, p):
    c = configs(n).astype(np.float64)
    return float(np.sum(p * (c[:, 0] * c[:, 1])))


def fit_k(n, p):
    target = measured_nn_corr(n, p)
    lo, hi = -5.0, 5.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if nn_corr(n, mid) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def family_residual(n, p):
    k = fit_k(n, p)
    return float(0.5 * np.sum(np.abs(p - nn_probs(n, k)))), k


def decimate(n, p):
    c = configs(n)
    m = n // 2
    out = np.zeros(2 ** m)
    keys = ((1 - c[:, 0::2]) // 2)
    idx = (keys * (2 ** np.arange(m))[None, :]).sum(axis=1)
    np.add.at(out, idx, p)
    return out


def majority3(n, p):
    c = configs(n)
    m = n // 3
    blocks = c.reshape(-1, m, 3).sum(axis=2)
    keys = ((1 - np.sign(blocks).astype(np.int64)) // 2)
    idx = (keys * (2 ** np.arange(m))[None, :]).sum(axis=1)
    out = np.zeros(2 ** m)
    np.add.at(out, idx, p)
    return out


def magnetization(n, p):
    c = configs(n).astype(np.float64)
    return float(np.sum(p * c.mean(axis=1)))


def main() -> int:
    record: dict = {"schema": "rg3-universality-v1",
                    "label": "exploratory"}
    items = {}

    # U1 M1 in-family flow
    p16 = model_probs(16, 0.7, 0.0, 0.0)
    p8 = decimate(16, p16)
    p4 = decimate(8, p8)
    r8, _ = family_residual(8, p8)
    r4, _ = family_residual(4, p4)
    items["U1_m1_in_family"] = max(r8, r4) <= 1e-12

    # U2 M2 residual shrinks under decimation
    q16 = model_probs(16, 0.5, 0.15, 0.0)
    q8 = decimate(16, q16)
    q4 = decimate(8, q8)
    d0, _ = family_residual(16, q16)
    d1, _ = family_residual(8, q8)
    d2, _ = family_residual(4, q4)
    items["U2_m2_flows_in"] = d2 < d1 < d0

    # U3 symmetry classes do not mix
    f16 = model_probs(16, 0.7, 0.0, 0.3)
    f4 = decimate(8, decimate(16, f16))
    m_f = abs(magnetization(4, f4))
    m_1 = abs(magnetization(4, p4))
    m_2 = abs(magnetization(4, q4))
    items["U3_symmetry_classes"] = (m_f >= 0.01
                                    and max(m_1, m_2) <= 1e-14)

    # U4 channel-relative convergence on the 12-ring
    q12 = model_probs(12, 0.5, 0.15, 0.0)
    dm, _ = family_residual(12, q12)
    dd, _ = family_residual(6, decimate(12, q12))
    dj, _ = family_residual(4, majority3(12, q12))
    items["U4_channel_relative"] = (dd < dm and dj > dm)

    record["measured"] = {
        "u1_residuals": [r8, r4],
        "u2_residual_flow": [d0, d1, d2],
        "u2_shrink_ratio": float(d2 / d0),
        "u3_field_coarse_m": m_f,
        "u3_symmetric_coarse_m": [m_1, m_2],
        "u4_micro_dec_maj": [dm, dd, dj]}
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
        / "rg3-universality.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("flow", [d0, d1, d2], "u4", [dm, dd, dj])
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
