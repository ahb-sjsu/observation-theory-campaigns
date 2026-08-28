"""XPROTO-QOT-GRAD family (F-QOT-GRAD): the reversal diagnostic run PROSPECTIVELY
on the optical flip pair. Operationalizes formal-core.tex steps 3-6.

The sealed flip pair (F-QOT-FLIP) is reused exactly: policy A allocates margin by
reach, policy B by band-centrality, both normalized to the same 1.0 dB fleet-mean
margin. This family parameterizes the segment m(t) = m^B + t*d, d = m^A - m^B,
t in [0,1], and runs the diagnostic:

  CALIBRATION (disclosed seeds CAL_SEEDS, disjoint from graded seeds): measure
  per-class risk at the stencil t in {0, 1/4, 1/2, 3/4, 1} (h = 1/4), averaged
  over N_NOISE_REP monitoring-noise redraws per seed (common draws across t).
  Per seed: g_c = (f_c(3/4) - f_c(1/4)) / (2h). In the t-parameterization the
  chain rule gives f_c'(t) = grad R_c(m(t))^T d, so the symmetric difference over
  t IS the directional derivative grad R_c(m_bar)^T d; no extra ||d||
  normalization is applied (consistent with formal-core Def. 4). Curvature
  witness per seed: sec_c = (f_c(1/4) - 2 f_c(1/2) + f_c(3/4)) / h^2, an
  estimate of d^T H R_c d; the directional floor uses
  M_c = |mean_seed(sec_c)| + CURV_SE_MULT * SE_seed(sec_c), the measured central
  curvature witness plus a declared noise allowance (the inflation). Disclosed
  pilot (2026-08-27, first calibration run): the floor M_c = 3 * max_seed |sec_c|
  charged the floor twice for sampling noise (the single-seed second differences
  are noise-dominated, spread ~0.3, sign flips across seeds) and ABSTAINED with
  ratios 0.586 / 0.721 on a pair whose graded signs are sealed and robust; the
  estimator was replaced BEFORE any seal and the pilot is disclosed in the
  prereg draft.

  GATE (formal-core Eq. 10, directional refinement M_c/4): exposure ratio
  E_c / (Z_CONF*SE_c + M_c/4) with E_c = |mean g_c|, SE_c = across-seed standard
  error. Both ratios > 1 -> REGISTER predicted signs of (dR_R, dR_P) and
  lambda* = g_P / (g_P - g_R) (the formal core's step-5 estimator; endpoint
  deltas are recorded alongside for comparison but do not set the registration).
  Either ratio <= 1 -> ABSTAIN (a legitimate registered outcome).

  GRADED: on disjoint seeds, evaluate the endpoints m^B, m^A with a single
  monitoring-noise draw (the sealed flip evaluation style) and grade the
  registered signs (every seed) and lambda* band (every seed).

MC4 control: the FEC pair (SD/HD classes, protect-low vs protect-high bumps,
ALIGNED reads) runs through the same gate and must NOT license an opposite-sign
(reversal) prediction.

Substrate: fam_qot's GNPy GN-model GSNR over CORONET-CONUS, via fam_qotflip's
fleet and false-clear code. Adaptation from fam_qotflip: the GSNR combs are
propagated ONCE and passed in (fam_qotflip re-propagates them inside each fleet
call); the fleet sampling code is otherwise draw-for-draw identical. Runs
locally in the qot venv (numpy<2), CPU. Emits QOTGRADREP-*.json.
"""
from __future__ import annotations

import argparse
import json
import os
import time
import warnings

import numpy as np

warnings.filterwarnings("ignore")
import fam_qot as q       # noqa: E402
import fam_qotflip as qf  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- diagnostic constants (all declared; see PREREG-XPROTO-QOT-GRAD.md) ----
H_STEP = 0.25                       # stencil half-step in t
STENCIL = [0.0, 0.25, 0.5, 0.75, 1.0]
N_NOISE_REP = 20                    # monitoring-noise redraws per calibration seed
CAL_SEEDS = [990, 991, 992, 993, 994, 995, 996, 997]
GRADED_SEEDS = [20260828, 20260829, 20260830]
SHAKEDOWN_SEEDS = [0, 1, 2]
Z_CONF = 2.0                        # gate confidence multiplier z
CURV_SE_MULT = 2.0                  # noise allowance on the curvature witness
SE_RATIO_CEIL = 0.5                 # MC3: SE_c / |mean g_c| ceiling for licensed configs
D_RMS_FLOOR_DB = 0.1                # MC2: RMS(d) floor in dB
LAMBDA_BAND_FLOOR = 0.05            # lambda* band = max(2*cal spread, this)
NOISE_STREAM_OFFSET = 5000          # this family's own noise stream (not the flip's)

SHAKEDOWN_NOTE = ("SHAKEDOWN RECORD. Seeds {0,1,2} stand in for the graded seeds. "
                  "Shakedown numbers are NEVER quoted in papers.")


def _combs():
    """Propagate the GNPy line systems once (ref + full loading, per reach)."""
    combs_ref = {ns: q._gsnr_comb(q.CH_REF, ns) for ns in q.SPAN_SET}
    combs_ful = {ns: q._gsnr_comb(q.CH_FULL, ns) for ns in q.SPAN_SET}
    return combs_ref, combs_ful


def _fleet_footprint(seed, combs_ref, combs_ful):
    """fam_qotflip._fleet_footprint with the combs precomputed; draws identical."""
    rng = np.random.default_rng(seed)
    spans = sorted(q.SPAN_SET)
    long_spans = spans[len(spans) // 2:]
    short_spans = spans[:len(spans) // 2]
    prov, dep, rn, ct, rmask = [], [], [], [], []
    smax = max(spans)
    for k in range(qf.K_SERVICES):
        if k % 2 == 0:
            ns = long_spans[rng.integers(0, len(long_spans))]
            p = rng.choice([rng.uniform(0.0, 0.15), rng.uniform(0.85, 1.0)])
            rmask.append(True)
        else:
            ns = short_spans[rng.integers(0, len(short_spans))]
            p = rng.uniform(0.35, 0.65)
            rmask.append(False)
        cr, cf = combs_ref[ns], combs_ful[ns]
        prov.append(float(cr[round(p * (len(cr) - 1))]))
        dep.append(float(cf[round(p * (len(cf) - 1))]))
        rn.append(ns / smax)
        ct.append(1.0 - 2.0 * abs(p - 0.5))
    return (np.array(prov), np.array(dep), np.array(rn), np.array(ct),
            np.array(rmask))


def _fleet(seed, combs_ref, combs_ful):
    """fam_qotflip._fleet (the FEC-control fleet) with combs precomputed."""
    rng = np.random.default_rng(seed)
    prov, dep = [], []
    for k in range(qf.K_SERVICES):
        ns = q.SPAN_POOL[rng.integers(0, len(q.SPAN_POOL))]
        p = rng.uniform(0.0, 1.0)
        cr, cf = combs_ref[ns], combs_ful[ns]
        prov.append(float(cr[round(p * (len(cr) - 1))]))
        dep.append(float(cf[round(p * (len(cf) - 1))]))
    return np.array(prov), np.array(dep)


def _policies_fp(rn, ct):
    m_a = rn * (qf.MARGIN_MEAN_DB / rn.mean())
    m_b = (ct + 0.05) * (qf.MARGIN_MEAN_DB / (ct + 0.05).mean())
    return m_a, m_b


def _risks_fp(est, dep, rmask, m):
    return (qf._fc(est[rmask], dep[rmask], m[rmask], 0.0),
            qf._fc(est[~rmask], dep[~rmask], m[~rmask], 0.0))


def _risks_fec(est, dep, sd_mask, m):
    return (qf._fc(est[sd_mask], dep[sd_mask], m[sd_mask], -qf.FEC_DELTA_DB),
            qf._fc(est[~sd_mask], dep[~sd_mask], m[~sd_mask], +qf.FEC_DELTA_DB))


def _stencil_curves(prov, dep, m_b, d, risk_fn, seed):
    """Mean per-class risk at each stencil t, averaged over N_NOISE_REP noise
    redraws (common draws across t: same est vectors at every stencil point)."""
    rng = np.random.default_rng(seed + NOISE_STREAM_OFFSET)
    noise = rng.normal(0, qf.NOISE_DB, size=(N_NOISE_REP, len(prov)))
    f1, f2 = [], []
    for t in STENCIL:
        m_t = m_b + t * d
        v1, v2 = [], []
        for r in range(N_NOISE_REP):
            r1, r2 = risk_fn(prov + noise[r], dep, m_t)
            v1.append(r1)
            v2.append(r2)
        f1.append(float(np.mean(v1)))
        f2.append(float(np.mean(v2)))
    return f1, f2


def _seed_diag(f1, f2):
    """Directional derivative, curvature witness, endpoint delta per class."""
    out = {}
    for tag, f in (("1", f1), ("2", f2)):
        out[f"g_{tag}"] = round((f[3] - f[1]) / (2 * H_STEP), 5)
        out[f"sec_{tag}"] = round((f[1] - 2 * f[2] + f[3]) / H_STEP ** 2, 5)
        out[f"dR_end_{tag}"] = round(f[4] - f[0], 5)
    return out


def _gate(cells, name1, name2):
    """Aggregate the per-seed diagnostics and decide: REGISTER or ABSTAIN."""
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


def calibrate(combs_ref, combs_ful):
    t0 = time.time()
    cal_cells, ctl_cells = [], []
    for seed in CAL_SEEDS:
        prov, dep, rn, ct, rmask = _fleet_footprint(seed, combs_ref, combs_ful)
        m_a, m_b = _policies_fp(rn, ct)
        d = m_a - m_b
        f1, f2 = _stencil_curves(prov, dep, m_b, d,
                                 lambda e, dp, m: _risks_fp(e, dp, rmask, m), seed)
        cell = {"seed": int(seed), "f_R": [round(v, 5) for v in f1],
                "f_P": [round(v, 5) for v in f2],
                "d_rms_db": round(float(np.sqrt((d ** 2).mean())), 4)}
        diag = _seed_diag(f1, f2)
        cell.update({"g_1": diag["g_1"], "g_2": diag["g_2"],
                     "sec_1": diag["sec_1"], "sec_2": diag["sec_2"],
                     "dR_end_1": diag["dR_end_1"], "dR_end_2": diag["dR_end_2"]})
        lam = (_lambda_from(cell["g_1"], cell["g_2"])
               if cell["g_1"] * cell["g_2"] < 0 else None)
        cell["lambda_g"] = round(lam, 4) if lam is not None else None
        cal_cells.append(cell)
        print(f"cal seed {seed}: g_R={cell['g_1']} g_P={cell['g_2']} "
              f"sec_R={cell['sec_1']} sec_P={cell['sec_2']} "
              f"lam_g={cell['lambda_g']} d_rms={cell['d_rms_db']}", flush=True)
        # ---- MC4 control: the FEC pair through the SAME gate machinery ----
        cprov, cdep = _fleet(seed, combs_ref, combs_ful)
        cm_a = qf._margins(cprov, "protect_low")
        cm_b = qf._margins(cprov, "protect_high")
        cd = cm_a - cm_b
        sd_mask = np.arange(len(cprov)) % 2 == 0
        cf1, cf2 = _stencil_curves(cprov, cdep, cm_b, cd,
                                   lambda e, dp, m: _risks_fec(e, dp, sd_mask, m),
                                   seed + 10 * NOISE_STREAM_OFFSET)
        cdiag = _seed_diag(cf1, cf2)
        ctl_cells.append({"seed": int(seed), "f_SD": [round(v, 5) for v in cf1],
                          "f_HD": [round(v, 5) for v in cf2], **cdiag,
                          "d_rms_db": round(float(np.sqrt((cd ** 2).mean())), 4)})

    gate = _gate(cal_cells, "R", "P")
    ctl_gate = _gate(ctl_cells, "SD", "HD")

    registration = {"decision": gate["decision"]}
    if gate["licensed"]:
        registration.update({
            "pred_sign_dR_R": int(np.sign(gate["g_mean_1"])),
            "pred_sign_dR_P": int(np.sign(gate["g_mean_2"])),
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
                "lambda_estimator": ("lambda* = g_P/(g_P - g_R) from the MEAN calibration "
                                     "directional derivatives (formal-core diagnostic "
                                     "step 5); band = max(2*across-seed spread of the "
                                     "per-seed lambda_g, 0.05)"),
            })

    mc = {
        "MC1_sane": bool(all(0.0 < v < 1.0 for c in cal_cells
                             for v in c["f_R"] + c["f_P"])),
        "MC2_policies_differ": bool(min(c["d_rms_db"] for c in cal_cells)
                                    >= D_RMS_FLOOR_DB),
        "MC3_stable": bool((not gate["licensed"]) or
                           (gate["se_1"] <= SE_RATIO_CEIL * abs(gate["g_mean_1"]) and
                            gate["se_2"] <= SE_RATIO_CEIL * abs(gate["g_mean_2"]))),
        "MC4_control_not_reversed": bool(not (ctl_gate["licensed"] and
                                              ctl_gate["opposite_signs"])),
    }
    rec = {"family": "F-QOT-GRAD", "phase": "calibration", "mode": "gnpy-coronet",
           "constants": {"h_step": H_STEP, "stencil": STENCIL,
                         "n_noise_rep": N_NOISE_REP, "cal_seeds": CAL_SEEDS,
                         "z_conf": Z_CONF, "curv_se_mult": CURV_SE_MULT,
                         "curv_estimator": "M_c = |mean_seed(sec_c)| + "
                                           "curv_se_mult*SE_seed(sec_c)",
                         "se_ratio_ceil": SE_RATIO_CEIL,
                         "d_rms_floor_db": D_RMS_FLOOR_DB,
                         "lambda_band_floor": LAMBDA_BAND_FLOOR,
                         "noise_stream_offset": NOISE_STREAM_OFFSET,
                         "k_services": qf.K_SERVICES,
                         "margin_mean_db": qf.MARGIN_MEAN_DB,
                         "noise_db": qf.NOISE_DB,
                         "substrate": "fam_qot GNPy GN-model over CORONET-CONUS, "
                                      "fam_qotflip footprint fleets"},
           "cal_cells": cal_cells, "gate": gate, "registration": registration,
           "control_cells": ctl_cells, "control_gate": ctl_gate, "mc": mc,
           "runtime_s": round(time.time() - t0, 1)}
    print(f"GATE: R ratio={gate['ratio_1']} P ratio={gate['ratio_2']} -> "
          f"{gate['decision']}; control(SD/HD): licensed={ctl_gate['licensed']} "
          f"opposite={ctl_gate['opposite_signs']} (MC4 "
          f"{'ok' if mc['MC4_control_not_reversed'] else 'FAIL'})", flush=True)
    print(f"registration: {registration}", flush=True)
    return rec


def graded(cal_rec, seeds, combs_ref, combs_ful, shakedown):
    t0 = time.time()
    reg = cal_rec["registration"]
    cells = []
    for seed in seeds:
        prov, dep, rn, ct, rmask = _fleet_footprint(seed, combs_ref, combs_ful)
        m_a, m_b = _policies_fp(rn, ct)
        d = m_a - m_b
        rng = np.random.default_rng(seed + NOISE_STREAM_OFFSET)
        est = prov + rng.normal(0, qf.NOISE_DB, len(prov))
        rR_B, rP_B = _risks_fp(est, dep, rmask, m_b)
        rR_A, rP_A = _risks_fp(est, dep, rmask, m_a)
        dR_R, dR_P = rR_A - rR_B, rP_A - rP_B
        cell = {"seed": int(seed),
                "fc_R_A": round(rR_A, 4), "fc_R_B": round(rR_B, 4),
                "fc_P_A": round(rP_A, 4), "fc_P_B": round(rP_B, 4),
                "dR_R": round(dR_R, 4), "dR_P": round(dR_P, 4),
                "d_rms_db": round(float(np.sqrt((d ** 2).mean())), 4)}
        lam = _lambda_from(dR_R, dR_P) if dR_R * dR_P < 0 else None
        cell["lambda_star"] = round(lam, 4) if lam is not None else None
        if reg["decision"] == "REGISTER":
            cell["sign_match"] = bool(
                np.sign(dR_R) == reg["pred_sign_dR_R"] and
                np.sign(dR_P) == reg["pred_sign_dR_P"])
            if reg.get("reversal_predicted"):
                lo, hi = reg["lambda_band"]
                cell["lambda_in_band"] = bool(lam is not None and lo <= lam <= hi)
        cells.append(cell)
        print(f"seed {seed}: dR_R={cell['dR_R']} dR_P={cell['dR_P']} "
              f"lam*={cell['lambda_star']} sign_match={cell.get('sign_match')} "
              f"in_band={cell.get('lambda_in_band')}", flush=True)

    grade = {"registered": reg["decision"] == "REGISTER"}
    if grade["registered"]:
        grade["B1_signs_all"] = bool(all(c["sign_match"] for c in cells))
        if reg.get("reversal_predicted"):
            grade["B2_lambda_all"] = bool(all(c["lambda_in_band"] for c in cells))
        grade["MC1_sane"] = bool(all(0.0 < v < 1.0 for c in cells for v in
                                     (c["fc_R_A"], c["fc_R_B"], c["fc_P_A"], c["fc_P_B"])))
        grade["MC2_policies_differ"] = bool(min(c["d_rms_db"] for c in cells)
                                            >= D_RMS_FLOOR_DB)
        mcs = grade["MC1_sane"] and grade["MC2_policies_differ"] and \
            all(cal_rec["mc"].values())
        bars = grade["B1_signs_all"] and grade.get("B2_lambda_all", True)
        grade["verdict"] = "VOID" if not mcs else ("PASS" if bars else "FAIL")
    else:
        grade["verdict"] = "ABSTAINED (registered abstention; deltas observational)"

    rec = {"family": "F-QOT-GRAD",
           "phase": "shakedown-graded" if shakedown else "graded",
           "mode": "gnpy-coronet", "seeds": [int(s) for s in seeds],
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
    ap.add_argument("--shakedown", action="store_true",
                    help="calibrate + graded stand-in on seeds {0,1,2}")
    ap.add_argument("--seeds", type=int, nargs="+", default=GRADED_SEEDS)
    args = ap.parse_args()
    t0 = time.time()
    print("propagating GNPy line systems once (ref + full loading, per reach)...",
          flush=True)
    combs_ref, combs_ful = _combs()
    print(f"combs ready in {time.time()-t0:.0f}s", flush=True)
    cal_path = os.path.join(HERE, "QOTGRADREP-calibration.json")
    if args.calibrate or args.shakedown:
        cal = calibrate(combs_ref, combs_ful)
        json.dump(cal, open(cal_path, "w"), indent=1)
        print(f"wrote {cal_path}", flush=True)
    else:
        cal = json.load(open(cal_path, encoding="utf-8"))
    if args.shakedown:
        rec = graded(cal, SHAKEDOWN_SEEDS, combs_ref, combs_ful, shakedown=True)
        out = os.path.join(HERE, "QOTGRADREP-shakedown.json")
        json.dump(rec, open(out, "w"), indent=1)
        print(f"wrote {out}", flush=True)
    elif args.graded:
        rec = graded(cal, args.seeds, combs_ref, combs_ful, shakedown=False)
        out = os.path.join(HERE, "QOTGRADREP-graded-raw.json")
        json.dump(rec, open(out, "w"), indent=1)
        print(f"wrote {out}", flush=True)


if __name__ == "__main__":
    main()
