#!/usr/bin/env python3
"""GD-5 Matejka-McKay replication and budgeted equilibrium.

Protocol declared in GAMES-DECISIONS-TRACK.md before this run. Part
one replicates the rational-inattention logit in a declared finite
model, Blahut-Arimoto to machine fixed point, with stationarity,
the weighted-logit identity, independent perturbation optimality,
closed-form limits, and consideration-set exclusion as bars. Part
two puts two budgeted consumers in a coordination game and measures
the equilibrium, symmetry, deattention ladder, and the declared
attention-complementarity finding. Verdict computed from the bars.

Exploratory label. No claim about human beings.
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


def ba_solve(pi, u, lam, iters=200_000, tol=1e-14):
    """Blahut-Arimoto for rational inattention, log-space logit.
    Returns conditional P(a|s), marginal p0, value, information."""
    n_s, n_a = u.shape
    p0 = np.full(n_a, 1.0 / n_a)
    for _ in range(iters):
        with np.errstate(divide="ignore"):
            logw = np.log(p0)[None, :] + u / lam
        logw -= logw.max(axis=1, keepdims=True)
        cond = np.exp(logw)
        cond /= cond.sum(axis=1, keepdims=True)
        p0_new = pi @ cond
        if np.max(np.abs(p0_new - p0)) < tol:
            p0 = p0_new
            break
        p0 = p0_new
    with np.errstate(divide="ignore"):
        logw = np.log(p0)[None, :] + u / lam
    logw -= logw.max(axis=1, keepdims=True)
    cond = np.exp(logw)
    cond /= cond.sum(axis=1, keepdims=True)
    p0 = pi @ cond
    value = float(np.sum(pi[:, None] * cond * u))
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(cond > 0, cond / p0[None, :], 1.0)
        info = float(np.sum(pi[:, None] * cond
                            * np.where(cond > 0, np.log(ratio), 0.0)))
    return cond, p0, value, info


def net_objective(pi, u, lam, cond):
    p0 = pi @ cond
    value = float(np.sum(pi[:, None] * cond * u))
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(cond > 0, cond / p0[None, :], 1.0)
        info = float(np.sum(pi[:, None] * cond
                            * np.where(cond > 0, np.log(ratio), 0.0)))
    return value - lam * info, value, info


def main() -> int:
    record: dict = {"schema": "gd5-budgeted-equilibrium-v1",
                    "label": "exploratory"}
    bars: dict = {}

    # part one, the replication
    pi = np.full(4, 0.25)
    u = np.array([[0.6, 1.0, 0.0],
                  [0.6, 1.0, 0.0],
                  [0.6, 0.0, 1.0],
                  [0.6, 0.0, 1.0]])
    lams = [1e-6, 0.05, 0.2, 1.0, 5.0]
    rng = np.random.RandomState(20260809)
    part1 = {}
    r1 = r2 = r3 = 0.0
    for lam in lams:
        cond, p0, value, info = ba_solve(pi, u, lam)
        r1 = max(r1, float(np.max(np.abs(pi @ cond - p0))))
        with np.errstate(divide="ignore"):
            w = p0[None, :] * np.exp(u / lam - (u / lam).max(
                axis=1, keepdims=True))
        w /= w.sum(axis=1, keepdims=True)
        r2 = max(r2, float(np.max(np.abs(cond - w))))
        base, _, _ = net_objective(pi, u, lam, cond)
        for _ in range(200):
            pert = 0.95 * cond + 0.05 * rng.dirichlet(
                np.ones(3), size=4)
            r3 = max(r3, net_objective(pi, u, lam, pert)[0] - base)
        part1[str(lam)] = {"p0": [float(x) for x in p0],
                           "value": value, "info_nats": info}
        print(f"lam {lam} p0 {np.round(p0, 6)} value "
              f"{value:.6f} info {info:.6f}", flush=True)
    bars["R1_stationarity"] = r1 <= 1e-12
    bars["R2_mm_logit_identity"] = r2 <= 1e-10
    bars["R3_perturbation_optimality"] = r3 <= 1e-10
    lim = part1["1e-06"]
    bars["R4_limits"] = (abs(lim["value"] - 1.0) <= 1e-9
                         and abs(lim["info_nats"] - np.log(2))
                         <= 1e-9
                         and part1["5.0"]["p0"][0] >= 1.0 - 1e-9)
    bars["R5_consideration_set"] = part1["0.05"]["p0"][0] <= 1e-6
    record["part1"] = {"lambdas": [float(x) for x in lams],
                       "results": part1,
                       "residuals": {"r1": float(r1),
                                     "r2": float(r2),
                                     "r3": float(r3)}}

    # part two, budgeted equilibrium in the coordination game
    pi2 = np.full(2, 0.5)

    def eff_payoff(q_opp):
        # u(a, s) = 1[a == s] + 0.5 * Q_opp(a | s)
        base = np.eye(2)
        return base + 0.5 * q_opp

    def equilibrium(l1, l2, rounds=10_000, tol=1e-12):
        q1 = np.full((2, 2), 0.5)
        q2 = np.full((2, 2), 0.5)
        res = np.inf
        for _ in range(rounds):
            n1 = ba_solve(pi2, eff_payoff(q2), l1)[0]
            n2 = ba_solve(pi2, eff_payoff(n1), l2)[0]
            res = max(float(np.max(np.abs(n1 - q1))),
                      float(np.max(np.abs(n2 - q2))))
            q1, q2 = n1, n2
            if res < tol:
                break
        i1 = net_objective(pi2, eff_payoff(q2), l1, q1)[2]
        i2 = net_objective(pi2, eff_payoff(q1), l2, q2)[2]
        acc1 = float(np.sum(pi2[:, None] * q1 * np.eye(2)))
        return q1, q2, i1, i2, acc1, res

    ladder = [0.05, 0.2, 0.5, 1.0, 2.0]
    e1 = 0.0
    sym_dev = 0.0
    infos, accs = [], []
    part2 = {}
    for lam in ladder:
        q1, q2, i1, i2, acc1, res = equilibrium(lam, lam)
        e1 = max(e1, res)
        sym_dev = max(sym_dev,
                      float(np.max(np.abs(q1 - q2))),
                      float(np.max(np.abs(q1 - q1[::-1, ::-1]))))
        infos.append(i1)
        accs.append(acc1)
        part2[str(lam)] = {"info_nats": float(i1),
                           "accuracy": float(acc1)}
        print(f"eq lam {lam} info {i1:.6f} acc {acc1:.6f} "
              f"res {res:.2e}", flush=True)
    bars["E1_convergence"] = e1 <= 1e-10
    bars["E2_symmetry"] = sym_dev <= 1e-8
    fp_resid = max(
        abs(q - 1.0 / (1.0 + np.exp(-(1.0 + 0.5 * (2 * q - 1))
                                    / lam)))
        for q, lam in zip(accs, ladder))
    bars["E3_deattention"] = (
        all(infos[i + 1] <= infos[i] + 1e-12
            for i in range(len(ladder) - 1))
        and accs[0] >= 0.95 and fp_resid <= 1e-8)

    l2_ladder = [0.05, 0.2, 1.0, 5.0]
    i1s = []
    for l2 in l2_ladder:
        q1, q2, i1, i2, acc1, res = equilibrium(0.2, l2)
        e1 = max(e1, res)
        i1s.append(i1)
        print(f"comp l2 {l2} I1 {i1:.6f}", flush=True)
    bars["E1_convergence"] = e1 <= 1e-10
    f6 = (all(i1s[i + 1] <= i1s[i] + 1e-10
              for i in range(len(l2_ladder) - 1))
          and i1s[0] - i1s[-1] >= 1e-4)
    record["part2"] = {"common_ladder": part2,
                       "symmetry_dev": float(sym_dev),
                       "fixed_point_resid": float(fp_resid),
                       "complementarity_l2_ladder":
                           [float(x) for x in l2_ladder],
                       "complementarity_I1":
                           [float(x) for x in i1s]}
    record["findings"] = {"F6_attention_complementarity": bool(f6)}

    verdict = "PASS" if all(bars.values()) else "FAIL"
    record["bars"] = {k: bool(v) for k, v in bars.items()}
    record["verdict"] = {
        "value": verdict, "computed_from": sorted(bars),
        "note": "finding F6 recorded individually per the declared "
                "protocol"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "gd5-budgeted-equilibrium.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("bars", bars)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
