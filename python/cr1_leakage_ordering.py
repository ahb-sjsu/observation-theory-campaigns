#!/usr/bin/env python3
"""CR-1 Blackwell ordering of declared leakage channels.

Protocol declared in CRYPTO-TRACK.md before this run. A four-bit
key read through declared leakage channels. The certificate is a
proof rather than a search, a channel B is a garbling of A exactly
when B is conditionally independent of the key given A, so a
strictly positive conditional mutual information proves B is not a
garbling of A. The GD-0 projected-gradient residual is retained as
a cross-check only. Verdict computed from the measured items.

Exploratory label. Nothing here is a claim about any real cipher,
implementation, or system, and no attack is developed.
"""
from __future__ import annotations

import json
import math
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gd0_instrument import FEAS_TOL, experiment_value  # noqa: E402
from gd1_flip_blackwell import garbling_residual  # noqa: E402
from projection_fold import canonical_sha256  # noqa: E402

NK = 16
SBOX = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
NOISE = 0.2


def det_channel(fn, n_out):
    m = np.zeros((NK, n_out))
    for k in range(NK):
        m[k, fn(SBOX[k])] = 1.0
    return m


def channels():
    ident = det_channel(lambda v: v, 16)
    hw = det_channel(lambda v: bin(v).count("1"), 5)
    lsb = det_channel(lambda v: v & 1, 2)
    noisy = np.zeros((NK, 5))
    for k in range(NK):
        w = bin(SBOX[k]).count("1")
        noisy[k, w] += 1.0 - 2 * NOISE
        noisy[k, max(w - 1, 0)] += NOISE
        noisy[k, min(w + 1, 4)] += NOISE
    const = np.ones((NK, 1))
    return {"ident": ident, "hw": hw, "lsb": lsb,
            "noisy_hw": noisy, "const": const}


def mutual_info(chan, prior):
    """I(K; L) in bits, exact from the declared joint."""
    joint = prior[:, None] * chan
    pl = joint.sum(axis=0)
    out = 0.0
    for k in range(chan.shape[0]):
        for j in range(chan.shape[1]):
            if joint[k, j] > 0:
                out += joint[k, j] * math.log2(
                    joint[k, j] / (prior[k] * pl[j]))
    return out


def cond_mutual_info(b, a, prior):
    """I(K; B | A) in bits, with B and A conditionally independent
    given K, the declared leakage structure."""
    total = 0.0
    joint_a = prior[:, None] * a
    pa = joint_a.sum(axis=0)
    for ja in range(a.shape[1]):
        if pa[ja] <= 0:
            continue
        post = joint_a[:, ja] / pa[ja]
        val = mutual_info(b, post)
        total += pa[ja] * val
    return total


def main() -> int:
    record: dict = {"schema": "cr1-leakage-ordering-v1",
                    "label": "exploratory"}
    ch = channels()
    prior = np.full(NK, 1.0 / NK)
    mi = {k: mutual_info(v, prior) for k, v in ch.items()}
    items = {}
    names = ["ident", "hw", "lsb", "noisy_hw", "const"]

    # K1 identity dominates
    k1 = True
    k1_detail = {}
    for n in names:
        if n == "ident":
            continue
        resid = garbling_residual(ch["ident"], ch[n])
        cmi = cond_mutual_info(ch[n], ch["ident"], prior)
        k1_detail[n] = {"residual": float(resid),
                        "cmi_given_ident": float(cmi)}
        if not (resid < FEAS_TOL and abs(cmi) <= 1e-12):
            k1 = False
    items["K1_identity_dominates"] = k1

    # K2 constant is dominated
    k2 = True
    k2_detail = {}
    for n in names:
        if n == "const":
            continue
        resid = garbling_residual(ch[n], ch["const"])
        k2_detail[n] = float(resid)
        if resid >= FEAS_TOL:
            k2 = False
    items["K2_constant_dominated"] = k2

    # K3 hw above noisy_hw, reverse proved impossible
    r_fwd = garbling_residual(ch["hw"], ch["noisy_hw"])
    cmi_fwd = cond_mutual_info(ch["noisy_hw"], ch["hw"], prior)
    cmi_rev = cond_mutual_info(ch["hw"], ch["noisy_hw"], prior)
    gap = mi["hw"] - mi["noisy_hw"]
    items["K3_noise_is_garbling"] = (r_fwd < FEAS_TOL
                                     and abs(cmi_fwd) <= 1e-12
                                     and cmi_rev > 1e-6
                                     and gap > 0)

    # K4 hw and lsb proved incomparable
    cmi_hl = cond_mutual_info(ch["lsb"], ch["hw"], prior)
    cmi_lh = cond_mutual_info(ch["hw"], ch["lsb"], prior)
    items["K4_incomparable_proved"] = (cmi_hl > 1e-6
                                       and cmi_lh > 1e-6)

    # K5 data-processing control on the task battery
    rng = np.random.RandomState(20260901)
    tasks = [rng.uniform(-1, 1, size=(NK, NK)) for _ in range(200)]
    ml = np.eye(NK)
    tasks.append(ml)
    worst = -np.inf
    pairs = [("ident", "hw"), ("ident", "lsb"),
             ("ident", "noisy_hw"), ("hw", "noisy_hw"),
             ("hw", "const"), ("lsb", "const")]
    for a, b in pairs:
        for t in tasks:
            gain = (experiment_value(prior, t, ch[b])
                    - experiment_value(prior, t, ch[a]))
            worst = max(worst, gain)
    items["K5_dpi_on_tasks"] = worst < 1e-10

    record["measured"] = {
        "mutual_information_bits": {k: float(v)
                                    for k, v in mi.items()},
        "k1_detail": k1_detail,
        "k2_residuals": k2_detail,
        "k3": {"residual_hw_to_noisy": float(r_fwd),
               "cmi_noisy_given_hw": float(cmi_fwd),
               "cmi_hw_given_noisy": float(cmi_rev),
               "mi_gap_bits": float(gap)},
        "k4": {"cmi_lsb_given_hw": float(cmi_hl),
               "cmi_hw_given_lsb": float(cmi_lh)},
        "k5_worst_task_gain": float(worst),
        "battery_size": len(tasks)}
    record["items"] = {k: bool(v) for k, v in items.items()}
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items)}
    record["declared"] = {"n_keys": NK, "sbox": SBOX,
                          "noise": NOISE,
                          "certificate": "conditional mutual "
                                         "information, a proof, "
                                         "with the search residual "
                                         "as cross-check only"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "cr1-leakage-ordering.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("MI", {k: round(v, 4) for k, v in mi.items()})
    print("items", items)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
