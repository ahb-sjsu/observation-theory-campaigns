"""XPROTO-QOT-CM family (F-QOT-CM): the optical flip pair re-matched in a TRUE
cost functional (formal-core Def. 1 / Eq. 1), not in nominal dB.

Nominal equivalence (the sealed F-QOT-FLIP pair) fixes the fleet-mean margin at
1.0 dB for both policies. That is C linear in m. The declared true cost here is
the Shannon capacity forgone by the margin at each service's provisioned
operating point:

    C(m) = sum_i [ log2(1 + gamma_i) - log2(1 + gamma_i * 10^(-m_i/10)) ],
    gamma_i = 10^(prov_GSNR_i / 10)   [bit/symbol, summed over services].

Justification (one sentence): the substrate exposes each service's provisioned
GSNR, and the capacity price of reserving m_i dB of margin is exactly the
Shannon capacity delta of backing the operating GSNR off by m_i dB, which is
what the margin removes from the service's usable operating point. This price
is nonlinear in dB and service-dependent (cheaper at high GSNR services in
relative terms), so equal mean dB is only nominal equivalence.

Rebalancing: policy B is rescaled by one scalar s (m^B_cm = s * m^B_nominal)
so that C(m^B_cm) = C(m^A) exactly. B is chosen for rescaling (not A) so the
reach-weighted policy A stays the fixed reference shared with F-QOT-FLIP and
F-QOT-GRAD, and the scalar preserves B's centrality shape, changing only its
level; the minimal change that restores C-equality. Solver: bisection on
s in [0.25, 4.0] (C is strictly increasing in s), 200 iterations, relative
residual reported (tolerance 1e-9).

Then the A/B class evaluation is re-run with the cost-matched pair, alongside
the nominal pair on the SAME monitoring-noise draw (paired). The future sealed
bar: the reversal survives cost re-matching (signs unchanged every graded
seed) and lambda* moves by less than a declared tolerance from the nominal
value. If the rebalancing is large and the reversal dies, that is a kept
negative and is reportable, not discardable.

Substrate: fam_qot GNPy GN-model over CORONET-CONUS via fam_qotflip's fleet
code (combs precomputed once, as in fam_qotgrad). Local, qot venv, CPU.
Emits QOTCMREP-*.json.
"""
from __future__ import annotations

import argparse
import json
import os
import time
import warnings

import numpy as np

warnings.filterwarnings("ignore")
import fam_qot as q         # noqa: E402
import fam_qotflip as qf    # noqa: E402
import fam_qotgrad as qg    # noqa: E402  (reuse the cached fleet builders)

HERE = os.path.dirname(os.path.abspath(__file__))

GRADED_SEEDS = [20260906, 20260907, 20260908]
SHAKEDOWN_SEEDS = [0, 1, 2]
S_LO, S_HI = 0.25, 4.0          # bisection bracket for the rebalancing scalar
N_BISECT = 200                  # bisection iterations
COST_RTOL = 1e-9                # MC3: relative cost-match residual ceiling
LAMBDA_SHIFT_TOL = 0.10         # B2: |lambda*_cm - lambda*_nom| ceiling (pilot; see prereg)
D_RMS_FLOOR_DB = 0.1            # MC2
NOISE_STREAM_OFFSET = 6000      # this family's own noise stream

SHAKEDOWN_NOTE = ("SHAKEDOWN RECORD. Seeds {0,1,2} stand in for the graded seeds. "
                  "Shakedown numbers are NEVER quoted in papers.")


def _cost(prov_db, m_db):
    gamma = 10.0 ** (np.asarray(prov_db) / 10.0)
    return float(np.sum(np.log2(1.0 + gamma) - np.log2(1.0 + gamma * 10.0 ** (-np.asarray(m_db) / 10.0))))


def _rebalance(prov, m_a, m_b_nom):
    """One scalar s with C(s*m_b_nom) = C(m_a); bisection, C monotone in s."""
    target = _cost(prov, m_a)
    lo, hi = S_LO, S_HI
    if not (_cost(prov, lo * m_b_nom) < target < _cost(prov, hi * m_b_nom)):
        raise RuntimeError("rebalancing target outside bisection bracket")
    for _ in range(N_BISECT):
        mid = 0.5 * (lo + hi)
        if _cost(prov, mid * m_b_nom) < target:
            lo = mid
        else:
            hi = mid
    s = 0.5 * (lo + hi)
    resid = abs(_cost(prov, s * m_b_nom) - target) / abs(target)
    return s, resid, target


def run_cell(seed, combs_ref, combs_ful):
    prov, dep, rn, ct, rmask = qg._fleet_footprint(seed, combs_ref, combs_ful)
    m_a, m_b_nom = qg._policies_fp(rn, ct)
    s, resid, cost_a = _rebalance(prov, m_a, m_b_nom)
    m_b_cm = s * m_b_nom
    cost_b_nom = _cost(prov, m_b_nom)
    rng = np.random.default_rng(seed + NOISE_STREAM_OFFSET)
    est = prov + rng.normal(0, qf.NOISE_DB, len(prov))

    def risks(m):
        return (qf._fc(est[rmask], dep[rmask], m[rmask], 0.0),
                qf._fc(est[~rmask], dep[~rmask], m[~rmask], 0.0))

    rR_A, rP_A = risks(m_a)
    rR_Bn, rP_Bn = risks(m_b_nom)
    rR_Bc, rP_Bc = risks(m_b_cm)
    d_cm = m_a - m_b_cm
    cell = {
        "seed": int(seed),
        "s_rebalance": round(s, 6), "cost_match_resid_rel": resid,
        "cost_A_bits": round(cost_a, 4), "cost_B_nominal_bits": round(cost_b_nom, 4),
        "cost_gap_nominal_bits": round(cost_a - cost_b_nom, 4),
        "cost_gap_nominal_rel": round((cost_a - cost_b_nom) / cost_a, 4),
        "mean_margin_A_db": round(float(m_a.mean()), 4),
        "mean_margin_B_nom_db": round(float(m_b_nom.mean()), 4),
        "mean_margin_B_cm_db": round(float(m_b_cm.mean()), 4),
        "d_rms_cm_db": round(float(np.sqrt((d_cm ** 2).mean())), 4),
        "fc_R_A": round(rR_A, 4), "fc_P_A": round(rP_A, 4),
        "fc_R_B_nom": round(rR_Bn, 4), "fc_P_B_nom": round(rP_Bn, 4),
        "fc_R_B_cm": round(rR_Bc, 4), "fc_P_B_cm": round(rP_Bc, 4),
    }
    dR_n, dP_n = rR_A - rR_Bn, rP_A - rP_Bn
    dR_c, dP_c = rR_A - rR_Bc, rP_A - rP_Bc
    cell.update({"dR_R_nom": round(dR_n, 4), "dR_P_nom": round(dP_n, 4),
                 "dR_R_cm": round(dR_c, 4), "dR_P_cm": round(dP_c, 4),
                 "flip_nom": bool(dR_n < 0 < dP_n), "flip_cm": bool(dR_c < 0 < dP_c),
                 "signs_survive": bool(np.sign(dR_c) == np.sign(dR_n) != 0 and
                                       np.sign(dP_c) == np.sign(dP_n) != 0)})
    lam_n = dP_n / (dP_n - dR_n) if dR_n * dP_n < 0 else None
    lam_c = dP_c / (dP_c - dR_c) if dR_c * dP_c < 0 else None
    cell["lambda_star_nom"] = round(lam_n, 4) if lam_n is not None else None
    cell["lambda_star_cm"] = round(lam_c, 4) if lam_c is not None else None
    cell["lambda_shift"] = (round(abs(lam_c - lam_n), 4)
                            if lam_n is not None and lam_c is not None else None)
    return cell


def grade(cells):
    g = {
        "B1_signs_survive_all": bool(all(c["flip_cm"] and c["signs_survive"]
                                         for c in cells)),
        "B2_lambda_shift_all": bool(all(c["lambda_shift"] is not None and
                                        c["lambda_shift"] <= LAMBDA_SHIFT_TOL
                                        for c in cells)),
        "MC1_sane": bool(all(0.0 < c[k] < 1.0 for c in cells for k in
                             ("fc_R_A", "fc_P_A", "fc_R_B_cm", "fc_P_B_cm"))),
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
    ap.add_argument("--graded", action="store_true",
                    help="write the graded-raw record instead of the shakedown one")
    args = ap.parse_args()
    t0 = time.time()
    print("propagating GNPy line systems once (ref + full loading, per reach)...",
          flush=True)
    combs_ref, combs_ful = qg._combs()
    print(f"combs ready in {time.time()-t0:.0f}s", flush=True)
    t1 = time.time()
    cells = []
    for s in args.seeds:
        c = run_cell(s, combs_ref, combs_ful)
        cells.append(c)
        print(f"seed {s}: s={c['s_rebalance']} costgapnom={c['cost_gap_nominal_rel']} "
              f"| nom dR_R={c['dR_R_nom']} dR_P={c['dR_P_nom']} lam={c['lambda_star_nom']} "
              f"| cm dR_R={c['dR_R_cm']} dR_P={c['dR_P_cm']} lam={c['lambda_star_cm']} "
              f"| flip_cm={c['flip_cm']} shift={c['lambda_shift']}", flush=True)
    g = grade(cells)
    rec = {"family": "F-QOT-CM", "mode": "gnpy-coronet",
           "phase": "graded" if args.graded else "shakedown",
           "constants": {"cost_functional": "Shannon capacity forgone by the margin "
                                            "at the provisioned GSNR, summed over "
                                            "services (bit/symbol)",
                         "rebalanced_policy": "B (single scalar s on m_B)",
                         "solver": f"bisection on s in [{S_LO},{S_HI}], "
                                   f"{N_BISECT} iterations",
                         "cost_rtol": COST_RTOL,
                         "lambda_shift_tol": LAMBDA_SHIFT_TOL,
                         "d_rms_floor_db": D_RMS_FLOOR_DB,
                         "noise_stream_offset": NOISE_STREAM_OFFSET,
                         "k_services": qf.K_SERVICES,
                         "margin_mean_db": qf.MARGIN_MEAN_DB,
                         "substrate": "fam_qot GNPy GN-model over CORONET-CONUS, "
                                      "fam_qotflip footprint fleets"},
           "cells": cells, "grade": g, "runtime_s": round(time.time() - t1, 1),
           "combs_precompute_s": round(t1 - t0, 1)}
    if not args.graded:
        rec["shakedown_disclaimer"] = SHAKEDOWN_NOTE
    out = os.path.join(HERE, "QOTCMREP-graded-raw.json" if args.graded
                       else "QOTCMREP-shakedown.json")
    json.dump(rec, open(out, "w"), indent=1)
    print(f"verdict ({rec['phase']}): {g['verdict']}; wrote {out}", flush=True)


if __name__ == "__main__":
    main()
