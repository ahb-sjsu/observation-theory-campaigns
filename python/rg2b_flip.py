#!/usr/bin/env python3
"""RG-2b the flip in renormalization form, corrected regime.

Identical to RG-2 except the regime, K = 0.6 and separation 2,
where the odd correlation length makes the distant sign genuinely
predictable. RG-2 declared a task with no signal, its 5e-5
predictability was matched exactly inside the fidelity tie set.
Verdict computed from the measured items.

Exploratory label. No claim about material systems.
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

W = 4
K = 0.6
D_SEP = 2
TIE_TOL = 1e-12


def main() -> int:
    record: dict = {"schema": "rg2b-flip-v1",
                    "label": "exploratory"}
    items = {}
    states = list(itertools.product([-1, 1], repeat=W))
    n = len(states)

    def ring_e(s):
        return sum(s[i] * s[(i + 1) % W] for i in range(W))

    t_mat = np.empty((n, n))
    for a, sa in enumerate(states):
        for b, sb in enumerate(states):
            inter = sum(sa[i] * sb[i] for i in range(W))
            t_mat[a, b] = np.exp(K * inter
                                 + 0.5 * K * (ring_e(sa)
                                              + ring_e(sb)))
    evals, evecs = np.linalg.eigh(t_mat)
    order = np.argsort(evals)[::-1]
    evals, evecs = evals[order], evecs[:, order]
    lam1, v1 = evals[0], np.abs(evecs[:, 0])

    # joint of two columns at separation D_SEP, two exact routes
    pw = np.eye(n)
    for _ in range(D_SEP):
        pw = pw @ (t_mat / lam1)
    joint_direct = v1[:, None] * pw * v1[None, :]
    joint_eigen = np.zeros((n, n))
    for i in range(n):
        joint_eigen += ((evals[i] / lam1) ** D_SEP
                        * np.outer(v1 * evecs[:, i],
                                   v1 * evecs[:, i]))
    dev_route = float(np.max(np.abs(joint_direct - joint_eigen)))
    items["F3_route_agreement"] = dev_route <= 1e-12
    joint = joint_direct / joint_direct.sum()

    # task target, sign of distant magnetization, zero to +1
    y = np.array([1 if sum(s) >= 0 else -1 for s in states])
    j_plus = joint[:, y == 1].sum(axis=1)
    j_minus = joint[:, y == -1].sum(axis=1)
    p_state = joint.sum(axis=1)

    def acc(mask_bits):
        cell0 = [i for i in range(n) if not (mask_bits >> i) & 1]
        cell1 = [i for i in range(n) if (mask_bits >> i) & 1]
        v = 0.0
        for cell in (cell0, cell1):
            if cell:
                v += max(sum(j_plus[i] for i in cell),
                         sum(j_minus[i] for i in cell))
        return v

    def ent(mask_bits):
        m1 = sum(p_state[i] for i in range(n)
                 if (mask_bits >> i) & 1)
        out = 0.0
        for q in (m1, 1.0 - m1):
            if q > 0:
                out -= q * np.log2(q)
        return out

    # theorem partition, group by the sign of the mass difference
    thm_mask = 0
    for i in range(n):
        if j_plus[i] - j_minus[i] > 0:
            thm_mask |= 1 << i
    acc_thm = acc(thm_mask)

    best_acc, best_h = -1.0, -1.0
    h_arg: list = []
    for mask in range(1, 2 ** (n - 1)):
        a = acc(mask)
        h = ent(mask)
        best_acc = max(best_acc, a)
        if h > best_h + TIE_TOL:
            best_h, h_arg = h, [mask]
        elif h > best_h - TIE_TOL:
            h_arg.append(mask)
    items["F1_theorem_matches_search"] = \
        abs(best_acc - acc_thm) <= 1e-12
    fid_best_acc = max(acc(m) for m in h_arg)
    flip = acc_thm - fid_best_acc
    items["F2_flip_positive"] = flip >= 1e-4

    v_odd = None
    for i in range(1, n):
        flipped = np.array([evecs[states.index(
            tuple(-x for x in s)), i] for s in states])
        if np.allclose(flipped, -evecs[:, i]):
            v_odd = evecs[:, i]
            break
    dis = sum(1 for i in range(n)
              if ((j_plus[i] - j_minus[i] > 0)
                  != (v_odd[i] / evecs[i, 0] > 0))) if v_odd is not \
        None else -1

    record["measured"] = {
        "route_dev": dev_route,
        "acc_task_optimal": float(acc_thm),
        "acc_fidelity_best": float(fid_best_acc),
        "flip": float(flip),
        "entropy_task_partition": float(ent(thm_mask)),
        "entropy_fidelity_best": float(best_h),
        "n_fidelity_ties": len(h_arg),
        "eigen_sign_disagreements": int(dis)}
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
        / "rg2b-flip.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("flip", flip, "task", acc_thm, "fid", fid_best_acc,
          "ties", len(h_arg), "disagreements", dis)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
