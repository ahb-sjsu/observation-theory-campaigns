#!/usr/bin/env python3
"""GD-3 prospect signatures from budgeted consumers (exploratory).

Protocol declared in GAMES-DECISIONS-TRACK.md before this run. Three
declared consumers, none containing a weighting function, a post hoc
reference point, or a loss-aversion coefficient. The verdict is
computed from the audits alone, the machinery must insert nothing,
symmetric environments must read symmetrically, and every distortion
must shrink along the declared budget ladders. The findings carry
declared directional bars and are recorded pass or fail
individually, either outcome is a result.

Exploratory label. No claim about human beings.
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

from projection_fold import canonical_sha256  # noqa: E402


def binom_pmf(n, p):
    """Exact binomial pmf vector via log-gamma, k = 0..n."""
    k = np.arange(n + 1)
    logc = (math.lgamma(n + 1)
            - np.array([math.lgamma(x + 1) + math.lgamma(n - x + 1)
                        for x in k]))
    with np.errstate(divide="ignore"):
        logp = np.where(k > 0, k * np.log(p), 0.0)
        logq = np.where(n - k > 0, (n - k) * np.log(1 - p), 0.0)
    return np.exp(logc + logp + logq)


def channel_weight(states_code, prior, decode_target, sigma,
                   m_grid):
    """Discrete-Gaussian channel on the code axis, exact posterior
    mean of decode_target, returns the channel-averaged read per
    state. sigma == 0 is the exact identity control."""
    if sigma == 0.0:
        return decode_target.copy()
    like = np.exp(-0.5 * ((m_grid[None, :] - states_code[:, None])
                          / sigma) ** 2)
    like /= like.sum(axis=1, keepdims=True)          # P(m|state)
    joint = prior[:, None] * like
    pm = joint.sum(axis=0)
    post = joint / np.where(pm > 0, pm, 1.0)[None, :]  # P(state|m)
    read = (post * decode_target[:, None]).sum(axis=0)  # E[target|m]
    return like @ read


def secant(pgrid, w, lo, hi):
    i = int(np.argmin(np.abs(pgrid - lo)))
    j = int(np.argmin(np.abs(pgrid - hi)))
    return float((w[j] - w[i]) / (pgrid[j] - pgrid[i]))


def main() -> int:
    record: dict = {"schema": "gd3-prospect-signatures-v1",
                    "label": "exploratory"}
    audits: dict = {}
    findings: dict = {}

    # P1 sample-budget reader, Beta(2,2) prior, posterior mean
    a_pr = b_pr = 2.0
    pgrid1 = np.round(np.arange(0.01, 1.0, 0.01), 10)
    ns = [1, 2, 5, 10, 50, 200]
    p1_dev, p1_curv, p1_id = [], [], []
    for n in ns:
        w_meas = np.array([
            float(np.sum(binom_pmf(n, p)
                         * (a_pr + np.arange(n + 1))
                         / (a_pr + b_pr + n)))
            for p in pgrid1])
        w_closed = (a_pr + n * pgrid1) / (a_pr + b_pr + n)
        p1_dev.append(float(np.max(np.abs(w_meas - w_closed))))
        p1_curv.append(float(np.max(np.abs(np.diff(w_meas, 2)))))
        p1_id.append(float(np.max(np.abs(w_meas - pgrid1))))
    audits["A1_p1_closed_form"] = max(p1_dev) <= 1e-10
    audits["A5_p1_budget_monotone"] = all(
        p1_id[i + 1] < p1_id[i] for i in range(len(ns) - 1))
    w10 = (a_pr + 10 * pgrid1) / (a_pr + b_pr + 10)
    findings["F1_linear_regressive"] = bool(
        max(p1_curv) <= 1e-10
        and np.all(w10[pgrid1 < 0.5] > pgrid1[pgrid1 < 0.5])
        and np.all(w10[pgrid1 > 0.5] < pgrid1[pgrid1 > 0.5]))
    record["P1"] = {"ns": ns, "closed_form_dev": p1_dev,
                    "max_curvature": p1_curv,
                    "max_dev_from_identity": p1_id}
    print("P1 closed-form dev", max(p1_dev), "curv", max(p1_curv))

    # P2 log-odds reader
    lgrid = np.round(np.arange(-6.0, 6.0 + 1e-9, 0.01), 10)
    mgrid2 = np.round(np.arange(-9.0, 9.0 + 1e-9, 0.01), 10)
    tau2 = 1.5
    prior2 = np.exp(-0.5 * lgrid ** 2 / tau2)
    prior2 /= prior2.sum()
    pvals = 1.0 / (1.0 + np.exp(-lgrid))
    sigmas2 = [1.0, 0.5, 0.25, 0.0]
    w_by_sigma = {s: channel_weight(lgrid, prior2, pvals, s, mgrid2)
                  for s in sigmas2}
    audits["A2_p2_zero_noise_identity"] = float(
        np.max(np.abs(w_by_sigma[0.0] - pvals))) <= 1e-12
    w2 = w_by_sigma[1.0]
    sym2 = float(np.max(np.abs(w2 + w2[::-1] - 1.0)))
    audits["A3_p2_symmetry"] = sym2 <= 1e-9
    ids2 = [float(np.max(np.abs(w_by_sigma[s] - pvals)))
            for s in sigmas2]
    audits["A4_p2_budget_monotone"] = all(
        ids2[i + 1] < ids2[i] for i in range(len(sigmas2) - 1))
    diff = w2 - pvals
    sgn = np.sign(diff)
    cross_idx = np.where(np.diff(sgn[(pvals > 0.05)
                                     & (pvals < 0.95)]) != 0)[0]
    pc = pvals[(pvals > 0.05) & (pvals < 0.95)]
    crossover = float(pc[cross_idx[0]]) if len(cross_idx) else -1.0
    band_over = diff[(pvals >= 0.02) & (pvals <= 0.2)]
    band_under = -diff[(pvals >= 0.8) & (pvals <= 0.98)]
    s_lo = secant(pvals, w2, 0.001, 0.05)
    s_hi = secant(pvals, w2, 0.95, 0.999)
    s_mid = secant(pvals, w2, 0.35, 0.65)
    findings["F2_inverse_s"] = bool(
        0.4 <= crossover <= 0.6
        and float(band_over.min()) > 0.01
        and float(band_under.min()) > 0.01
        and s_lo > 1.1 and s_hi > 1.1 and s_mid < 0.9)
    prior2s = np.exp(-0.5 * (lgrid + 1.0) ** 2 / tau2)
    prior2s /= prior2s.sum()
    w2s = channel_weight(lgrid, prior2s, pvals, 1.0, mgrid2)
    diffs = w2s - pvals
    sgns = np.sign(diffs[(pvals > 0.02) & (pvals < 0.98)])
    ps = pvals[(pvals > 0.02) & (pvals < 0.98)]
    ci = np.where(np.diff(sgns) != 0)[0]
    crossover_shift = float(ps[ci[0]]) if len(ci) else -1.0
    findings["F3_environment_tracks"] = bool(
        0 < crossover_shift < 0.35)
    record["P2"] = {"tau2": tau2, "sigmas": sigmas2,
                    "max_dev_from_identity": ids2,
                    "symmetry_dev": sym2, "crossover": crossover,
                    "overweight_min_margin_02_20":
                        float(band_over.min()),
                    "underweight_min_margin_80_98":
                        float(band_under.min()),
                    "secant_low": s_lo, "secant_high": s_hi,
                    "secant_mid": s_mid,
                    "crossover_shifted_env": crossover_shift}
    print("P2 crossover", crossover, "secants", s_lo, s_mid, s_hi,
          "shifted crossover", crossover_shift)

    # P3 magnitude reader
    xgrid = np.round(np.arange(-100.0, 100.0 + 1e-9, 0.5), 10)
    code = np.sign(xgrid) * np.log1p(np.abs(xgrid))
    mgrid3 = np.round(np.arange(-6.0, 6.0 + 1e-9, 0.01), 10)
    prior_sym = np.exp(-np.abs(xgrid) / 25.0)
    prior_sym /= prior_sym.sum()
    prior_asym = np.where(xgrid < 0,
                          np.exp(-np.abs(xgrid) / 40.0),
                          np.exp(-np.abs(xgrid) / 20.0))
    prior_asym /= prior_asym.sum()
    sigmas3 = [0.6, 0.3, 0.15, 0.0]
    v_by_sigma = {s: channel_weight(code, prior_sym, xgrid, s,
                                    mgrid3) for s in sigmas3}
    audits["A2_p3_zero_noise_identity"] = float(
        np.max(np.abs(v_by_sigma[0.0] - xgrid))) <= 1e-12
    v3 = v_by_sigma[0.6]
    odd = float(np.max(np.abs(v3 + v3[::-1])))
    audits["A3_p3_symmetry"] = odd <= 1e-9
    ids3 = [float(np.max(np.abs(v_by_sigma[s] - xgrid)))
            for s in sigmas3]
    audits["A4_p3_budget_monotone"] = all(
        ids3[i + 1] < ids3[i] for i in range(len(sigmas3) - 1))
    va = channel_weight(code, prior_asym, xgrid, 0.6, mgrid3)
    i_p = int(np.argmin(np.abs(xgrid - 50.0)))
    i_m = int(np.argmin(np.abs(xgrid + 50.0)))
    ratio = float(-va[i_m] / va[i_p])
    findings["F4_loss_side_less_compressed"] = bool(ratio >= 1.05)
    lag = 10  # 5 units at 0.5 spacing
    sel = (xgrid >= 5.0) & (xgrid <= 80.0)
    idx = np.where(sel)[0]
    second = (v3[idx + lag] - 2 * v3[idx] + v3[idx - lag])
    findings["F5_diminishing_sensitivity"] = bool(
        float(second.max()) <= 0.01
        and float(second.mean()) <= -0.01)
    record["P3"] = {"sigmas": sigmas3,
                    "max_dev_from_identity": ids3,
                    "oddness_dev_sym": odd,
                    "v_sym_at_10_50_80": [float(v3[np.argmin(
                        np.abs(xgrid - t))]) for t in (10, 50, 80)],
                    "asym_ratio_at_50": ratio,
                    "second_diff_max": float(second.max()),
                    "second_diff_mean": float(second.mean())}
    print("P3 ratio", ratio, "second diff max/mean",
          float(second.max()), float(second.mean()))

    verdict = "PASS" if all(audits.values()) else "FAIL"
    record["audits"] = {k: bool(v) for k, v in audits.items()}
    record["findings"] = {k: bool(v) for k, v in findings.items()}
    record["verdict"] = {
        "value": verdict, "computed_from": sorted(audits),
        "note": "findings recorded individually, either outcome "
                "a result per the declared protocol"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "gd3-prospect-signatures.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("audits", audits)
    print("findings", findings)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
