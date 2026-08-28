"""XPROTO-CSI-CM family (F-CSI-CM): the radio flip pair re-matched in a TRUE
cost functional (formal-core Def. 1 / Eq. 1), not in nominal dB. Radio twin of
fam_qotcm.py.

Nominal equivalence (the sealed F-CSI-FLIP pair) fixes the fleet-mean margin at
1.5 dB for both policies. The declared true cost here is the spectral-efficiency
cost of the backoff at each user's operating SNR, read from the substrate's own
MCS mapping:

    C(m) = sum_i [ SE(snr_i) - SE(snr_i - m_i) ],

where snr_i is the user's mean SNR (12 dB for fleet M, 7 dB for fleet S) and
SE(x) is the piecewise-linear interpolation of the per-MCS spectral efficiency
Qm*R over the required-SNR points measured from the real Sionna LDPC curves at
the 0.10 BLER target (clamped at the table ends). Justification (one
sentence): a dB of selection backoff costs the link exactly the MCS spectral
efficiency it forgoes at the operating SNR, and that price is nonlinear and
SNR-dependent, so equal mean dB is only nominal equivalence; policy B spends
its margin on 7 dB users where the SE price per dB differs from the 12 dB
users policy A protects.

Rebalancing: policy B is rescaled by one scalar s (m^B_cm = s * m^B_nominal)
so that C(m^B_cm) = C(m^A) exactly. B is rescaled (not A) so the
Doppler-weighted policy A stays the fixed reference shared with F-CSI-FLIP and
F-CSI-GRAD; the scalar preserves B's deficit shape, changing only its level.
Solver: bisection on s in [0.25, 4.0] (C nondecreasing in s, continuous
piecewise-linear), 200 iterations, relative residual reported (<= 1e-9).

Then the A/B fleet evaluation is re-run with the cost-matched pair alongside
the nominal pair, per-user random streams seeded exactly as the sealed flip
evaluation (paired). The future sealed bar: the reversal survives cost
re-matching (signs unchanged every graded seed) and lambda* moves by less
than a declared tolerance from the nominal value. If the rebalancing is large
and the reversal dies, that is a kept negative and is reportable, not
discardable.

Substrate: real Sionna 5G NR LDPC BLER curves + TDL-A fading via fam_csiflip's
_trace/_nack. Run on Atlas (~/sionna-venv), CPU only, TF threads capped.
Emits CSICMREP-*.json.
"""
import os

os.environ["CUDA_VISIBLE_DEVICES"] = ""      # CPU only (before csi_sionna import)
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
import argparse   # noqa: E402
import json       # noqa: E402
import time       # noqa: E402

import numpy as np                # noqa: E402
import tensorflow as tf           # noqa: E402

import fam_csiflip as cf          # noqa: E402
import csi_sionna as cs           # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

GRADED_SEEDS = [20260906, 20260907, 20260908]
SHAKEDOWN_SEEDS = [0, 1, 2]
S_LO, S_HI = 0.25, 4.0
N_BISECT = 200
COST_RTOL = 1e-9
LAMBDA_SHIFT_TOL = 0.10          # pilot; see prereg draft
D_RMS_FLOOR_DB = 0.5

SHAKEDOWN_NOTE = ("SHAKEDOWN RECORD. Seeds {0,1,2} stand in for the graded seeds. "
                  "Shakedown numbers are NEVER quoted in papers.")


def _se_curve(curves):
    """Piecewise-linear SE(x) over the measured required-SNR points."""
    req = cs.required_snr(curves)
    se = np.array(cs.MCS_QM, float) * np.array(cs.MCS_R, float)
    order = np.argsort(req)
    req_s, se_s = req[order], se[order]
    if not np.all(np.diff(req_s) > 0):
        raise RuntimeError("required-SNR points not strictly increasing")
    return req_s, se_s


def _cost(snr_op, m, req_s, se_s):
    def se_at(x):
        return np.interp(x, req_s, se_s, left=se_s[0], right=se_s[-1])
    return float(np.sum(se_at(snr_op) - se_at(snr_op - m)))


def _rebalance(snr_op, m_a, m_b_nom, req_s, se_s):
    target = _cost(snr_op, m_a, req_s, se_s)
    lo, hi = S_LO, S_HI
    if not (_cost(snr_op, lo * m_b_nom, req_s, se_s) < target <
            _cost(snr_op, hi * m_b_nom, req_s, se_s)):
        raise RuntimeError("rebalancing target outside bisection bracket")
    for _ in range(N_BISECT):
        mid = 0.5 * (lo + hi)
        if _cost(snr_op, mid * m_b_nom, req_s, se_s) < target:
            lo = mid
        else:
            hi = mid
    s = 0.5 * (lo + hi)
    resid = abs(_cost(snr_op, s * m_b_nom, req_s, se_s) - target) / abs(target)
    return s, resid, target


def _users(seed):
    users = []
    for k in range(cf.N_PER_FLEET):
        users.append(("M", cf._trace(seed * 31 + k, cf.M_FD, cf.M_SNR),
                      cf.M_FD, cf.M_SNR))
    for k in range(cf.N_PER_FLEET):
        users.append(("S", cf._trace(seed * 31 + 100 + k, cf.S_FD, cf.S_SNR),
                      cf.S_FD, cf.S_SNR))
    return users


def _fleet_risks(users, m, curves, req, seed):
    out = {}
    for fleet in ("M", "S"):
        vals = [cf._nack(u[1], m[i], curves, req, seed * 7 + i)
                for i, u in enumerate(users) if u[0] == fleet]
        out[fleet] = float(np.mean(vals))
    return out["M"], out["S"]


def run_cell(seed, curves, req, req_s, se_s):
    ts = time.time()
    users = _users(seed)
    fds = np.array([u[2] for u in users])
    deficit = np.array([max(0.0, 12.0 - u[3]) + 0.05 for u in users])
    snr_op = np.array([u[3] for u in users], float)
    m_a = fds / fds.mean() * cf.MARGIN_MEAN_DB
    m_b_nom = deficit / deficit.mean() * cf.MARGIN_MEAN_DB
    s, resid, cost_a = _rebalance(snr_op, m_a, m_b_nom, req_s, se_s)
    m_b_cm = s * m_b_nom
    cost_b_nom = _cost(snr_op, m_b_nom, req_s, se_s)
    rM_A, rS_A = _fleet_risks(users, m_a, curves, req, seed)
    rM_Bn, rS_Bn = _fleet_risks(users, m_b_nom, curves, req, seed)
    rM_Bc, rS_Bc = _fleet_risks(users, m_b_cm, curves, req, seed)
    d_cm = m_a - m_b_cm
    cell = {
        "seed": int(seed),
        "s_rebalance": round(s, 6), "cost_match_resid_rel": resid,
        "cost_A_se": round(cost_a, 4), "cost_B_nominal_se": round(cost_b_nom, 4),
        "cost_gap_nominal_se": round(cost_a - cost_b_nom, 4),
        "cost_gap_nominal_rel": round((cost_a - cost_b_nom) / cost_a, 4),
        "mean_margin_A_db": round(float(m_a.mean()), 4),
        "mean_margin_B_nom_db": round(float(m_b_nom.mean()), 4),
        "mean_margin_B_cm_db": round(float(m_b_cm.mean()), 4),
        "d_rms_cm_db": round(float(np.sqrt((d_cm ** 2).mean())), 4),
        "fc_M_A": round(rM_A, 4), "fc_S_A": round(rS_A, 4),
        "fc_M_B_nom": round(rM_Bn, 4), "fc_S_B_nom": round(rS_Bn, 4),
        "fc_M_B_cm": round(rM_Bc, 4), "fc_S_B_cm": round(rS_Bc, 4),
    }
    dM_n, dS_n = rM_A - rM_Bn, rS_A - rS_Bn
    dM_c, dS_c = rM_A - rM_Bc, rS_A - rS_Bc
    cell.update({"dR_M_nom": round(dM_n, 4), "dR_S_nom": round(dS_n, 4),
                 "dR_M_cm": round(dM_c, 4), "dR_S_cm": round(dS_c, 4),
                 "flip_nom": bool(dM_n < 0 < dS_n), "flip_cm": bool(dM_c < 0 < dS_c),
                 "signs_survive": bool(np.sign(dM_c) == np.sign(dM_n) != 0 and
                                       np.sign(dS_c) == np.sign(dS_n) != 0)})
    lam_n = dS_n / (dS_n - dM_n) if dM_n * dS_n < 0 else None
    lam_c = dS_c / (dS_c - dM_c) if dM_c * dS_c < 0 else None
    cell["lambda_star_nom"] = round(lam_n, 4) if lam_n is not None else None
    cell["lambda_star_cm"] = round(lam_c, 4) if lam_c is not None else None
    cell["lambda_shift"] = (round(abs(lam_c - lam_n), 4)
                            if lam_n is not None and lam_c is not None else None)
    cell["runtime_s"] = round(time.time() - ts, 1)
    return cell


def grade(cells):
    g = {
        "B1_signs_survive_all": bool(all(c["flip_cm"] and c["signs_survive"]
                                         for c in cells)),
        "B2_lambda_shift_all": bool(all(c["lambda_shift"] is not None and
                                        c["lambda_shift"] <= LAMBDA_SHIFT_TOL
                                        for c in cells)),
        "MC1_sane": bool(all(0.0 < c[k] < 1.0 for c in cells for k in
                             ("fc_M_A", "fc_S_A", "fc_M_B_cm", "fc_S_B_cm"))),
        "MC2_policies_differ": bool(min(c["d_rms_cm_db"] for c in cells)
                                    >= D_RMS_FLOOR_DB),
        "MC3_cost_matched": bool(max(c["cost_match_resid_rel"] for c in cells)
                                 <= COST_RTOL),
        "MC4_nominal_flip_holds": bool(all(c["flip_nom"] for c in cells)),
    }
    mcs = all(g[k] for k in ("MC1_sane", "MC2_policies_differ",
                             "MC3_cost_matched", "MC4_nominal_flip_holds"))
    bars = g["B1_signs_survive_all"] and g["B2_lambda_shift_all"]
    g["verdict"] = "VOID" if not mcs else ("PASS" if bars else "FAIL")
    return g


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=SHAKEDOWN_SEEDS)
    ap.add_argument("--graded", action="store_true")
    args = ap.parse_args()
    tf.config.threading.set_intra_op_parallelism_threads(16)   # Atlas thread cap
    tf.config.threading.set_inter_op_parallelism_threads(4)
    print("loading real 5G NR LDPC curves...", flush=True)
    curves = cs.measure_bler_curves()
    req = cs.required_snr(curves)
    req_s, se_s = _se_curve(curves)
    t0 = time.time()
    cells = []
    for s in args.seeds:
        c = run_cell(s, curves, req, req_s, se_s)
        cells.append(c)
        print(f"seed {s}: s={c['s_rebalance']} costgapnom={c['cost_gap_nominal_rel']} "
              f"| nom dR_M={c['dR_M_nom']} dR_S={c['dR_S_nom']} lam={c['lambda_star_nom']} "
              f"| cm dR_M={c['dR_M_cm']} dR_S={c['dR_S_cm']} lam={c['lambda_star_cm']} "
              f"| flip_cm={c['flip_cm']} shift={c['lambda_shift']} "
              f"({c['runtime_s']}s)", flush=True)
    g = grade(cells)
    rec = {"family": "F-CSI-CM", "mode": "nrsionna",
           "phase": "graded" if args.graded else "shakedown",
           "constants": {"cost_functional": "spectral-efficiency cost of the "
                                            "backoff at the operating SNR from the "
                                            "measured Sionna MCS mapping "
                                            "(piecewise-linear SE over required-SNR "
                                            "points, Qm*R)",
                         "rebalanced_policy": "B (single scalar s on m_B)",
                         "solver": f"bisection on s in [{S_LO},{S_HI}], "
                                   f"{N_BISECT} iterations",
                         "cost_rtol": COST_RTOL,
                         "lambda_shift_tol": LAMBDA_SHIFT_TOL,
                         "d_rms_floor_db": D_RMS_FLOOR_DB,
                         "n_per_fleet": cf.N_PER_FLEET,
                         "margin_mean_db": cf.MARGIN_MEAN_DB,
                         "duration": cf.DURATION,
                         "report_period": cf.REPORT_PERIOD,
                         "substrate": "real Sionna 5G NR LDPC + TDL-A, held CSI, "
                                      "fam_csiflip fleets"},
           "cells": cells, "grade": g, "runtime_s": round(time.time() - t0, 1)}
    if not args.graded:
        rec["shakedown_disclaimer"] = SHAKEDOWN_NOTE
    out = os.path.join(HERE, "CSICMREP-graded-raw.json" if args.graded
                       else "CSICMREP-shakedown.json")
    json.dump(rec, open(out, "w"), indent=1)
    print(f"verdict ({rec['phase']}): {g['verdict']}; wrote {out}", flush=True)


if __name__ == "__main__":
    main()
