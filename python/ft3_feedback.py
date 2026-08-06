#!/usr/bin/env python3
"""FT-3 feedback and measurement (exploratory).

Protocol declared in FLUCTUATION-TRACK.md before this run. The
FT-0 system with a declared noisy measurement after the fourth
relax step and declared feedback retargeting the remaining
protocol. The Sagawa-Ueda identity holds exactly with the
controller's pointwise information, the bare identity fails by the
measured efficacy, and a noisier bystander's information does not
restore it. Verdict computed from the measured items.

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
    E0, T_STEPS, energies, equilibrium, free_energy,
    metropolis_kernel)
from projection_fold import canonical_sha256  # noqa: E402

MEAS_STEP = 4
ERR = 0.2
ERR_BYSTANDER = 0.25
E_ALT_FINAL = np.array([0.2, 1.0, 0.3])


def branch_energies(y):
    """Stage energies k = 0..T for feedback branch y."""
    out = [energies(k) for k in range(MEAS_STEP + 1)]
    e_mid = energies(MEAS_STEP)
    for k in range(MEAS_STEP + 1, T_STEPS + 1):
        frac = (k - MEAS_STEP) / (T_STEPS - MEAS_STEP)
        if y == 2:
            out.append(e_mid + (E_ALT_FINAL - e_mid) * frac)
        else:
            out.append(energies(k))
    return out


def p_meas(y, s, err=ERR):
    return 1.0 - err if y == s else err / 2.0


def main() -> int:
    record: dict = {"schema": "ft3-feedback-v1",
                    "label": "exploratory"}
    items = {}
    pi0 = equilibrium(E0)
    pre_kernels = [metropolis_kernel(energies(k))
                   for k in range(1, MEAS_STEP + 1)]
    branch = {y: branch_energies(y) for y in range(3)}
    post_kernels = {y: [metropolis_kernel(branch[y][k])
                        for k in range(MEAS_STEP + 1, T_STEPS + 1)]
                    for y in range(3)}
    df_y = {y: free_energy(branch[y][-1]) - free_energy(E0)
            for y in range(3)}

    # marginal of the state at the measurement, then P(y)
    marg = pi0.copy()
    for k in range(MEAS_STEP):
        marg = marg @ pre_kernels[k]
    p_y = np.array([sum(marg[s] * p_meas(y, s) for s in range(3))
                    for y in range(3)])

    su_sum = 0.0
    bare_sum = 0.0
    by_sum = 0.0
    mean_w = 0.0
    mean_i = 0.0
    mean_df = 0.0
    for path in itertools.product(range(3), repeat=T_STEPS + 1):
        pr_pre = pi0[path[0]]
        for k in range(1, MEAS_STEP + 1):
            pr_pre *= pre_kernels[k - 1][path[k - 1], path[k]]
        if pr_pre == 0.0:
            continue
        s_meas = path[MEAS_STEP]
        for y in range(3):
            pr = pr_pre * p_meas(y, s_meas)
            if pr == 0.0:
                continue
            prot = branch[y]
            for k in range(MEAS_STEP + 1, T_STEPS + 1):
                pr *= post_kernels[y][k - MEAS_STEP - 1][
                    path[k - 1], path[k]]
            if pr == 0.0:
                continue
            w = sum(prot[k][path[k - 1]] - prot[k - 1][path[k - 1]]
                    for k in range(1, T_STEPS + 1))
            info = np.log(p_meas(y, s_meas) / p_y[y])
            core = np.exp(-(w - df_y[y]))
            su_sum += pr * core * np.exp(-info)
            bare_sum += pr * core
            mean_w += pr * w
            mean_i += pr * info
            mean_df += pr * df_y[y]
            # bystander sees y through extra symmetric noise
            for yb in range(3):
                q = (1.0 - ERR_BYSTANDER if yb == y
                     else ERR_BYSTANDER / 2.0)
                pb_lik = sum(p_meas(v, s_meas)
                             * ((1.0 - ERR_BYSTANDER) if yb == v
                                else ERR_BYSTANDER / 2.0)
                             for v in range(3))
                pb_marg = sum(
                    p_y[v] * ((1.0 - ERR_BYSTANDER) if yb == v
                              else ERR_BYSTANDER / 2.0)
                    for v in range(3))
                info_b = np.log(pb_lik / pb_marg)
                by_sum += pr * q * core * np.exp(-info_b)

    d_su = abs(su_sum - 1.0)
    d_bare = abs(bare_sum - 1.0)
    d_by = abs(by_sum - 1.0)
    items["T1_sagawa_ueda_exact"] = d_su <= 1e-12
    items["T2_bare_identity_broken"] = d_bare >= 1e-3
    items["T3_information_is_the_consumers"] = (d_by >= 1e-4
                                                and d_su <= 1e-12)
    margin = mean_w - mean_df + mean_i

    record["measured"] = {
        "su_deviation": float(d_su),
        "bare_efficacy": float(bare_sum),
        "bare_deviation": float(d_bare),
        "bystander_deviation": float(d_by),
        "mean_work": float(mean_w),
        "mean_df": float(mean_df),
        "mean_information_nats": float(mean_i),
        "t4_second_law_margin": float(margin),
        "reading": "the identity knows which observer acts, the "
                   "controller's information restores it exactly "
                   "and the bystander's does not"}
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
        / "ft3-feedback.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("items", items)
    print("su", d_su, "bare", bare_sum, "bystander", d_by,
          "margin", margin)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
