"""XPROTO-CSI-SWEEP2 family (F-CSI-SWEEP2): the CSI age horizon at the paper's own
target, properly calibrated. Replaces the 0.15-threshold exploration sweep
(csi_sweep.py) that the WCNC draft over-claimed as a 0.10 result (found in
review; the record is kept).

Design changes from the exploration sweep, each answering a review point:
  1. CALIBRATION FIRST. A fixed selection backoff D_cal is chosen on a disclosed
     calibration seed as the smallest multiple of 0.25 dB for which the FRESH
     policy (re-estimate every TTI) achieves BLER <= 0.09 at every Doppler. All
     policies then carry D_cal, so the fresh baseline genuinely meets the 0.10
     target before any aging is measured.
  2. FLOOR AT THE REAL TARGET. The age horizon P*(f_D) is the largest report
     period whose held-CSI BLER stays <= 0.10. If no period qualifies, the
     Doppler point is recorded as CENSORED, not clamped to one TTI.
  3. FIT ON NON-CENSORED POINTS ONLY, ordinary least squares through the origin
     of floor_ms against Clarke Tcoh = 0.423/f_D, slope and R^2 reported per
     seed and pooled. Censored points are listed alongside, never fitted.

Substrate: Sionna 5G NR LDPC decoder curves (AWGN-measured) driven through a
TR38.901 TDL-A per-TTI SNR trace -- an NR LDPC-based link-to-system simulation.
Run on Atlas (~/sionna-venv, CPU is fine). Emits CSISWEEP2REP-family.json.
"""
import os
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
import argparse
import json

import numpy as np
import tensorflow as tf
from sionna.phy.channel.tr38901 import TDL

import csi_sionna as cs

HERE = os.path.dirname(os.path.abspath(__file__))
FDS = [10, 25, 50, 100, 200, 400]
PERIODS = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32]   # pilot 2: finer grid, the
                                # 0.10-target floors live in 1-6 TTI
NTTI = 12000              # pilot 2: 2x length, stabilises the fd=10 floor
TARGET = 0.10                 # the paper's target; floor and calibration both use it
CAL_MARGIN = 0.09             # calibrate fresh to <= 0.09 (headroom under 0.10)
CAL_SEED = 999                # disclosed calibration seed (never a graded seed)
CAL_STEP_DB = 0.25
CAL_MAX_DB = 4.0


def fading_fd(seed, ntti, fd):
    tf.random.set_seed(seed)
    v = fd * cs.C0 / cs.FC_HZ
    tdl = TDL(model="A", delay_spread=cs.DELAY_SPREAD_S, carrier_frequency=cs.FC_HZ,
              min_speed=v, max_speed=v)
    out = tdl(1, ntti, 1.0 / cs.TTI_S)
    a = out[0] if isinstance(out, (tuple, list)) else out
    h = tf.reduce_sum(tf.squeeze(a), axis=0)
    p = np.abs(h.numpy()) ** 2
    p /= p.mean()
    return cs.MEAN_SNR_DB + 10 * np.log10(p + 1e-12)


def bler(snr_db, period, curves, req, backoff_db, rng, fresh=False):
    """Held-CSI (or fresh) achieved BLER with a fixed selection backoff."""
    est = snr_db[0]
    nack = 0
    for n in range(len(snr_db)):
        if fresh or n % period == 0:
            est = snr_db[n] + rng.normal(0, cs.CQI_NOISE_DB)
        cand = np.where(req + backoff_db <= est)[0]
        m = int(cand[-1]) if cand.size else 0
        if rng.random() < cs.bler_at(curves, m, snr_db[n]):
            nack += 1
    return nack / len(snr_db)


def calibrate(curves, req):
    """Smallest backoff (0.25 dB steps) with fresh BLER <= CAL_MARGIN at every fd."""
    rng = np.random.default_rng(CAL_SEED)
    for k in range(int(CAL_MAX_DB / CAL_STEP_DB) + 1):
        d = k * CAL_STEP_DB
        worst = 0.0
        for fd in FDS:
            snr = fading_fd(CAL_SEED, NTTI, fd)
            b = bler(snr, 1, curves, req, d, np.random.default_rng(CAL_SEED + fd),
                     fresh=True)
            worst = max(worst, b)
        print(f"  calibration: backoff {d:.2f} dB -> worst fresh BLER {worst:.4f}",
              flush=True)
        if worst <= CAL_MARGIN:
            return d, worst
    return CAL_MAX_DB, worst


def run_cell(seed, curves, req, d_cal):
    rng = np.random.default_rng(seed)
    floors, censored, fresh_ok = {}, [], {}
    rows = {}
    for fd in FDS:
        snr = fading_fd(seed * 13 + fd, NTTI, fd)
        fresh_ok[str(fd)] = round(
            bler(snr, 1, curves, req, d_cal, np.random.default_rng(seed + fd),
                 fresh=True), 4)
        row = [round(bler(snr, p, curves, req, d_cal,
                          np.random.default_rng(seed * 7 + fd * 101 + p)), 4)
               for p in PERIODS]
        rows[str(fd)] = row
        ok = [p for p, b in zip(PERIODS, row) if b <= TARGET]
        if ok:
            floors[str(fd)] = max(ok)
        else:
            censored.append(fd)
    # OLS through the origin on non-censored points
    xs = np.array([0.423 / fd * 1000.0 for fd in FDS if str(fd) in floors])
    ys = np.array([floors[str(fd)] * cs.TTI_S * 1000.0 for fd in FDS if str(fd) in floors])
    if len(xs) >= 2:
        k = float((xs * ys).sum() / (xs * xs).sum())
        r2 = 1 - float(((ys - k * xs) ** 2).sum()) / float(((ys - ys.mean()) ** 2).sum())
    else:
        k, r2 = float("nan"), float("nan")
    return {"seed": int(seed), "mode": "nrsionna", "d_cal_db": d_cal,
            "fresh_bler": fresh_ok, "bler_rows": rows, "floors_tti": floors,
            "censored_fds": censored, "slope": round(k, 4), "r2": round(r2, 4),
            "n_fit_points": int(len(xs))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "CSISWEEP2REP-family.json"))
    args = ap.parse_args()
    print("loading NR LDPC curves...", flush=True)
    curves = cs.measure_bler_curves()
    req = cs.required_snr(curves)
    print("calibrating the fresh baseline to <= 0.09 at every Doppler...", flush=True)
    d_cal, worst = calibrate(curves, req)
    print(f"D_cal = {d_cal} dB (worst fresh {worst:.4f})", flush=True)
    cells = []
    for s in args.seeds:
        c = run_cell(s, curves, req, d_cal)
        cells.append(c)
        print(f"seed {s}: floors={c['floors_tti']} censored={c['censored_fds']} "
              f"slope={c['slope']} R2={c['r2']} fresh_worst="
              f"{max(c['fresh_bler'].values())}", flush=True)
    rec = {"family": "F-CSI-SWEEP2", "mode": "nrsionna", "target": TARGET,
           "constants": {"fds": FDS, "periods": PERIODS, "ntti": NTTI,
                         "d_cal_db": d_cal, "cal_margin": CAL_MARGIN,
                         "cal_seed": CAL_SEED,
                         "substrate": "NR LDPC-based link-to-system simulation "
                                      "(Sionna curves + TDL-A trace)"},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
