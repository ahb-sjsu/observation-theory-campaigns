"""XPROTO-CSI-GRAD family (F-CSI-GRAD): the reversal diagnostic run PROSPECTIVELY
on the radio flip pair. Operationalizes formal-core.tex steps 3-6. Radio twin of
fam_qotgrad.py; one protocol, two substrates.

The sealed flip pair (F-CSI-FLIP) is reused exactly: policy A allocates the
1.5 dB fleet-mean margin by Doppler, policy B by SNR deficit. This family
parameterizes the segment m(t) = m^B + t*d, d = m^A - m^B, t in [0,1]:

  CALIBRATION (disclosed seeds CAL_SEEDS, disjoint from graded seeds): per-class
  mean NACK rate at the stencil t in {0, 1/4, 1/2, 3/4, 1} (h = 1/4). The
  per-user HARQ/decode random streams are seeded exactly as in the sealed flip
  evaluation (seed*7+i), so all stencil points share common random numbers and
  differences isolate the margin effect. Per seed: g_c = (f_c(3/4) -
  f_c(1/4)) / (2h). In the t-parameterization f_c'(t) = grad R_c(m(t))^T d, so
  this symmetric difference IS the directional derivative; no extra ||d||
  normalization (formal-core Def. 4). Curvature witness per seed:
  sec_c = (f_c(1/4) - 2 f_c(1/2) + f_c(3/4)) / h^2; the directional floor uses
  M_c = |mean_seed(sec_c)| + CURV_SE_MULT * SE_seed(sec_c), the measured central
  curvature witness plus a declared noise allowance (same estimator as
  fam_qotgrad, adopted after the disclosed QOT pilot showed the max-based floor
  double-charges sampling noise).

  GATE (formal-core Eq. 10, directional refinement M_c/4): both exposure
  ratios |mean g_c| / (Z_CONF*SE_c + M_c/4) must exceed 1 to REGISTER the
  predicted signs of (dR_M, dR_S) and lambda* = g_S / (g_S - g_M) (the formal
  core's step-5 estimator; endpoint deltas recorded alongside). Otherwise
  ABSTAIN (a legitimate registered outcome).

  GRADED: on disjoint seeds, evaluate the endpoints m^B, m^A (this is
  draw-for-draw the sealed F-CSI-FLIP evaluation) and grade the registered
  signs (every seed) and lambda* band (every seed).

MC4 control: the F-CSI-FLIP null (one M-trace read at required-SNR shifts
0 / +2 dB under protect-low 3.0 dB vs protect-high 0.75 dB scalar margins,
ALIGNED reads) runs through the same gate and must NOT license an
opposite-sign (reversal) prediction.

Substrate: real Sionna 5G NR LDPC BLER curves + TDL-A fading via fam_csiflip's
_trace/_nack (csi_sionna, cached curves). Run on Atlas (~/sionna-venv), CPU
only, TF threads capped. Emits CSIGRADREP-*.json.
"""
import os

os.environ["CUDA_VISIBLE_DEVICES"] = ""      # CPU only (before csi_sionna import)
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
import argparse   # noqa: E402
import json       # noqa: E402
import time       # noqa: E402

import numpy as np                # noqa: E402
import tensorflow as tf           # noqa: E402

import fam_csiflip as cf          # noqa: E402  (pulls in csi_sionna from ~/csi)
import csi_sionna as cs           # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- diagnostic constants (all declared; see PREREG-XPROTO-CSI-GRAD.md) ----
H_STEP = 0.25
STENCIL = [0.0, 0.25, 0.5, 0.75, 1.0]
CAL_SEEDS = [990, 991, 992, 993, 994]
GRADED_SEEDS = [20260828, 20260829, 20260830]
SHAKEDOWN_SEEDS = [0, 1, 2]
Z_CONF = 2.0
CURV_SE_MULT = 2.0
SE_RATIO_CEIL = 0.5
D_RMS_FLOOR_DB = 0.5
LAMBDA_BAND_FLOOR = 0.05

SHAKEDOWN_NOTE = ("SHAKEDOWN RECORD. Seeds {0,1,2} stand in for the graded seeds. "
                  "Shakedown numbers are NEVER quoted in papers.")


def _users(seed):
    """The sealed F-CSI-FLIP fleet, draw-for-draw (fam_csiflip.run_cell)."""
    users = []
    for k in range(cf.N_PER_FLEET):
        users.append(("M", cf._trace(seed * 31 + k, cf.M_FD, cf.M_SNR),
                      cf.M_FD, cf.M_SNR))
    for k in range(cf.N_PER_FLEET):
        users.append(("S", cf._trace(seed * 31 + 100 + k, cf.S_FD, cf.S_SNR),
                      cf.S_FD, cf.S_SNR))
    return users


def _policies(users):
    fds = np.array([u[2] for u in users])
    deficit = np.array([max(0.0, 12.0 - u[3]) + 0.05 for u in users])
    m_a = fds / fds.mean() * cf.MARGIN_MEAN_DB
    m_b = deficit / deficit.mean() * cf.MARGIN_MEAN_DB
    return m_a, m_b


def _fleet_risks(users, m, curves, req, seed):
    """Per-fleet mean NACK under margin vector m; per-user streams seeded exactly
    as the sealed flip evaluation (seed*7+i), common across stencil points."""
    out = {}
    for fleet in ("M", "S"):
        vals = [cf._nack(u[1], m[i], curves, req, seed * 7 + i)
                for i, u in enumerate(users) if u[0] == fleet]
        out[fleet] = float(np.mean(vals))
    return out["M"], out["S"]


def _seed_diag(f1, f2):
    out = {}
    for tag, f in (("1", f1), ("2", f2)):
        out[f"g_{tag}"] = round((f[3] - f[1]) / (2 * H_STEP), 5)
        out[f"sec_{tag}"] = round((f[1] - 2 * f[2] + f[3]) / H_STEP ** 2, 5)
        out[f"dR_end_{tag}"] = round(f[4] - f[0], 5)
    return out


def _gate(cells, name1, name2):
    g = {}
    n = len(cells)
    for tag in ("1", "2"):
        gs = np.array([c[f"g_{tag}"] for c in cells])
        secs = np.array([c[f"sec_{tag}"] for c in cells])
        gbar = float(gs.mean())
        se = float(gs.std(ddof=1) / np.sqrt(n))
        sec_se = float(secs.std(ddof=1) / np.sqrt(n))
        curv = float(abs(secs.mean()) + CURV_SE_MULT * sec_se)
        floor = Z_CONF * se + curv / 4.0
        g[f"g_mean_{tag}"] = round(gbar, 5)
        g[f"se_{tag}"] = round(se, 5)
        g[f"curv_bound_{tag}"] = round(curv, 5)
        g[f"floor_{tag}"] = round(floor, 5)
        g[f"ratio_{tag}"] = round(abs(gbar) / floor, 3) if floor > 0 else float("inf")
    g["class_1"], g["class_2"] = name1, name2
    g["licensed"] = bool(g["ratio_1"] > 1.0 and g["ratio_2"] > 1.0)
    g["opposite_signs"] = bool(g["g_mean_1"] * g["g_mean_2"] < 0)
    g["decision"] = "REGISTER" if g["licensed"] else "ABSTAIN"
    return g


def _lambda_from(g1, g2):
    den = g2 - g1
    return float(g2 / den) if den != 0 else None


def calibrate(curves, req):
    t0 = time.time()
    cal_cells, ctl_cells = [], []
    for seed in CAL_SEEDS:
        ts = time.time()
        users = _users(seed)
        m_a, m_b = _policies(users)
        d = m_a - m_b
        f1, f2 = [], []
        for t in STENCIL:
            rM, rS = _fleet_risks(users, m_b + t * d, curves, req, seed)
            f1.append(rM)
            f2.append(rS)
        cell = {"seed": int(seed), "f_M": [round(v, 5) for v in f1],
                "f_S": [round(v, 5) for v in f2],
                "d_rms_db": round(float(np.sqrt((d ** 2).mean())), 4)}
        cell.update(_seed_diag(f1, f2))
        lam = (_lambda_from(cell["g_1"], cell["g_2"])
               if cell["g_1"] * cell["g_2"] < 0 else None)
        cell["lambda_g"] = round(lam, 4) if lam is not None else None
        cell["runtime_s"] = round(time.time() - ts, 1)
        cal_cells.append(cell)
        print(f"cal seed {seed}: g_M={cell['g_1']} g_S={cell['g_2']} "
              f"sec_M={cell['sec_1']} sec_S={cell['sec_2']} "
              f"lam_g={cell['lambda_g']} ({cell['runtime_s']}s)", flush=True)
        # ---- MC4 control: the flip null pair through the SAME gate machinery ----
        snr0 = cf._trace(seed * 31 + 500, cf.M_FD, cf.M_SNR)
        cm_a, cm_b = 2.0 * cf.MARGIN_MEAN_DB, 0.5 * cf.MARGIN_MEAN_DB
        cd = cm_a - cm_b
        cf1, cf2 = [], []
        for t in STENCIL:
            m_t = cm_b + t * cd
            cf1.append(cf._nack(snr0, m_t, curves, req, seed + 900, 0.0))
            cf2.append(cf._nack(snr0, m_t, curves, req, seed + 900, 2.0))
        ctl = {"seed": int(seed), "f_t1": [round(v, 5) for v in cf1],
               "f_t2": [round(v, 5) for v in cf2], "d_rms_db": round(cd, 4)}
        ctl.update(_seed_diag(cf1, cf2))
        ctl_cells.append(ctl)

    gate = _gate(cal_cells, "M", "S")
    ctl_gate = _gate(ctl_cells, "t1", "t2")

    registration = {"decision": gate["decision"]}
    if gate["licensed"]:
        registration.update({
            "pred_sign_dR_M": int(np.sign(gate["g_mean_1"])),
            "pred_sign_dR_S": int(np.sign(gate["g_mean_2"])),
            "reversal_predicted": gate["opposite_signs"],
        })
        if gate["opposite_signs"]:
            lam_pred = _lambda_from(gate["g_mean_1"], gate["g_mean_2"])
            lams = [c["lambda_g"] for c in cal_cells if c["lambda_g"] is not None]
            spread = float(np.std(lams, ddof=1)) if len(lams) > 1 else 0.0
            band = max(2 * spread, LAMBDA_BAND_FLOOR)
            registration.update({
                "lambda_star_pred": round(lam_pred, 4),
                "lambda_spread_cal": round(spread, 4),
                "lambda_band_halfwidth": round(band, 4),
                "lambda_band": [round(lam_pred - band, 4), round(lam_pred + band, 4)],
                "lambda_estimator": ("lambda* = g_S/(g_S - g_M) from the MEAN "
                                     "calibration directional derivatives "
                                     "(formal-core diagnostic step 5); band = "
                                     "max(2*across-seed spread of per-seed "
                                     "lambda_g, 0.05)"),
            })

    mc = {
        "MC1_sane": bool(all(0.0 < v < 1.0 for c in cal_cells
                             for v in c["f_M"] + c["f_S"])),
        "MC2_policies_differ": bool(min(c["d_rms_db"] for c in cal_cells)
                                    >= D_RMS_FLOOR_DB),
        "MC3_stable": bool((not gate["licensed"]) or
                           (gate["se_1"] <= SE_RATIO_CEIL * abs(gate["g_mean_1"]) and
                            gate["se_2"] <= SE_RATIO_CEIL * abs(gate["g_mean_2"]))),
        "MC4_control_not_reversed": bool(not (ctl_gate["licensed"] and
                                              ctl_gate["opposite_signs"])),
    }
    rec = {"family": "F-CSI-GRAD", "phase": "calibration", "mode": "nrsionna",
           "constants": {"h_step": H_STEP, "stencil": STENCIL,
                         "cal_seeds": CAL_SEEDS, "z_conf": Z_CONF,
                         "curv_se_mult": CURV_SE_MULT,
                         "curv_estimator": "M_c = |mean_seed(sec_c)| + "
                                           "curv_se_mult*SE_seed(sec_c)",
                         "se_ratio_ceil": SE_RATIO_CEIL,
                         "d_rms_floor_db": D_RMS_FLOOR_DB,
                         "lambda_band_floor": LAMBDA_BAND_FLOOR,
                         "n_per_fleet": cf.N_PER_FLEET,
                         "margin_mean_db": cf.MARGIN_MEAN_DB,
                         "duration": cf.DURATION,
                         "report_period": cf.REPORT_PERIOD,
                         "substrate": "real Sionna 5G NR LDPC + TDL-A, held CSI, "
                                      "fam_csiflip fleets"},
           "cal_cells": cal_cells, "gate": gate, "registration": registration,
           "control_cells": ctl_cells, "control_gate": ctl_gate, "mc": mc,
           "runtime_s": round(time.time() - t0, 1)}
    print(f"GATE: M ratio={gate['ratio_1']} S ratio={gate['ratio_2']} -> "
          f"{gate['decision']}; control(t1/t2): licensed={ctl_gate['licensed']} "
          f"opposite={ctl_gate['opposite_signs']} (MC4 "
          f"{'ok' if mc['MC4_control_not_reversed'] else 'FAIL'})", flush=True)
    print(f"registration: {registration}", flush=True)
    return rec


def graded(cal_rec, seeds, curves, req, shakedown):
    t0 = time.time()
    reg = cal_rec["registration"]
    cells = []
    for seed in seeds:
        ts = time.time()
        users = _users(seed)
        m_a, m_b = _policies(users)
        rM_B, rS_B = _fleet_risks(users, m_b, curves, req, seed)
        rM_A, rS_A = _fleet_risks(users, m_a, curves, req, seed)
        dR_M, dR_S = rM_A - rM_B, rS_A - rS_B
        d = m_a - m_b
        cell = {"seed": int(seed),
                "fc_M_A": round(rM_A, 4), "fc_M_B": round(rM_B, 4),
                "fc_S_A": round(rS_A, 4), "fc_S_B": round(rS_B, 4),
                "dR_M": round(dR_M, 4), "dR_S": round(dR_S, 4),
                "d_rms_db": round(float(np.sqrt((d ** 2).mean())), 4),
                "runtime_s": round(time.time() - ts, 1)}
        lam = _lambda_from(dR_M, dR_S) if dR_M * dR_S < 0 else None
        cell["lambda_star"] = round(lam, 4) if lam is not None else None
        if reg["decision"] == "REGISTER":
            cell["sign_match"] = bool(
                np.sign(dR_M) == reg["pred_sign_dR_M"] and
                np.sign(dR_S) == reg["pred_sign_dR_S"])
            if reg.get("reversal_predicted"):
                lo, hi = reg["lambda_band"]
                cell["lambda_in_band"] = bool(lam is not None and lo <= lam <= hi)
        cells.append(cell)
        print(f"seed {seed}: dR_M={cell['dR_M']} dR_S={cell['dR_S']} "
              f"lam*={cell['lambda_star']} sign_match={cell.get('sign_match')} "
              f"in_band={cell.get('lambda_in_band')} ({cell['runtime_s']}s)",
              flush=True)

    grade = {"registered": reg["decision"] == "REGISTER"}
    if grade["registered"]:
        grade["B1_signs_all"] = bool(all(c["sign_match"] for c in cells))
        if reg.get("reversal_predicted"):
            grade["B2_lambda_all"] = bool(all(c["lambda_in_band"] for c in cells))
        grade["MC1_sane"] = bool(all(0.0 < v < 1.0 for c in cells for v in
                                     (c["fc_M_A"], c["fc_M_B"], c["fc_S_A"], c["fc_S_B"])))
        grade["MC2_policies_differ"] = bool(min(c["d_rms_db"] for c in cells)
                                            >= D_RMS_FLOOR_DB)
        mcs = grade["MC1_sane"] and grade["MC2_policies_differ"] and \
            all(cal_rec["mc"].values())
        bars = grade["B1_signs_all"] and grade.get("B2_lambda_all", True)
        grade["verdict"] = "VOID" if not mcs else ("PASS" if bars else "FAIL")
    else:
        grade["verdict"] = "ABSTAINED (registered abstention; deltas observational)"

    rec = {"family": "F-CSI-GRAD",
           "phase": "shakedown-graded" if shakedown else "graded",
           "mode": "nrsionna", "seeds": [int(s) for s in seeds],
           "registration": reg, "calibration_mc": cal_rec["mc"],
           "cells": cells, "grade": grade,
           "runtime_s": round(time.time() - t0, 1)}
    if shakedown:
        rec["shakedown_disclaimer"] = SHAKEDOWN_NOTE
    print(f"verdict ({rec['phase']}): {grade['verdict']}", flush=True)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--graded", action="store_true")
    ap.add_argument("--shakedown", action="store_true")
    ap.add_argument("--seeds", type=int, nargs="+", default=GRADED_SEEDS)
    args = ap.parse_args()
    tf.config.threading.set_intra_op_parallelism_threads(16)   # Atlas thread cap
    tf.config.threading.set_inter_op_parallelism_threads(4)
    print("loading real 5G NR LDPC curves...", flush=True)
    curves = cs.measure_bler_curves()
    req = cs.required_snr(curves)
    cal_path = os.path.join(HERE, "CSIGRADREP-calibration.json")
    if args.calibrate or args.shakedown:
        cal = calibrate(curves, req)
        json.dump(cal, open(cal_path, "w"), indent=1)
        print(f"wrote {cal_path}", flush=True)
    else:
        cal = json.load(open(cal_path, encoding="utf-8"))
    if args.shakedown:
        rec = graded(cal, SHAKEDOWN_SEEDS, curves, req, shakedown=True)
        out = os.path.join(HERE, "CSIGRADREP-shakedown.json")
        json.dump(rec, open(out, "w"), indent=1)
        print(f"wrote {out}", flush=True)
    elif args.graded:
        rec = graded(cal, args.seeds, curves, req, shakedown=False)
        out = os.path.join(HERE, "CSIGRADREP-graded-raw.json")
        json.dump(rec, open(out, "w"), indent=1)
        print(f"wrote {out}", flush=True)


if __name__ == "__main__":
    main()
