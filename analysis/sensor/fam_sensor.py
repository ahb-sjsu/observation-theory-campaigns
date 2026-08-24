"""XPROTO-SENSOR family (F-SENSOR): consumer-relative staleness of a sensor
calibration certificate, on REAL field data (UCI Air Quality co-location, De Vito
et al.) -- the physical-sensing twin of XPROTO-QUANTUM (device calibration).

A low-cost metal-oxide gas sensor is calibrated once against a co-located
reference analyser; the calibration is a CERTIFICATE -- "this reading is accurate
to within tolerance." Over months the sensor **drifts** (metal-oxide aging), so
the frozen calibration **false-clears**: the reported reading is trusted as
accurate while its true error (vs the reference witness) exceeds tolerance. The
false-clear is **consumer-relative**: different pollutants' sensors drift
differently, so the certificate is adequate for one measurand and badly stale for
another. Periodic recalibration against the reference (the witness) holds it.

  * consumer = a pollutant channel (CO, C6H6, NOx, NO2).
  * certificate = a frozen calibration -> "reading accurate to +/- tol".
  * witness = the co-located reference analyser (the true concentration).
  * naive: freeze the initial calibration; refreshed: recalibrate every REFRESH_DAYS.

Substrate: REAL hourly field measurements (~1 year). Seeds bootstrap the test
period (sampling CI on a fixed dataset). Emits SENSORREP-family.json.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import urllib.request
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
CSV = os.path.join(DATA, "AirQualityUCI.csv")
URL = "https://archive.ics.uci.edu/static/public/360/air+quality.zip"

# ---- sealed cell constants -------------------------------------------
POLLUTANTS = {"CO": (2, 3), "C6H6": (5, 6), "NOx": (7, 8), "NO2": (9, 10)}  # (ref, sensor) col
T_COL, RH_COL = 12, 13
TRAIN_HOURS = 30 * 24         # initial calibration window
REFRESH_HOURS = 14 * 24      # recalibration period
REFRESH_WIN = 30 * 24        # trailing window each recalibration fits
TOL_FRAC = 0.5               # tolerance = 0.5 * (training-period reference std)
MISSING = -200.0


def _fetch():
    if os.path.exists(CSV):
        return
    os.makedirs(DATA, exist_ok=True)
    zp = os.path.join(DATA, "aq.zip")
    urllib.request.urlretrieve(URL, zp)
    with zipfile.ZipFile(zp) as z:
        z.extract("AirQualityUCI.csv", DATA)


def _num(s):
    s = s.strip().replace(",", ".")
    if not s:
        return np.nan
    v = float(s)
    return np.nan if v == MISSING else v


def _load():
    _fetch()
    rows = list(csv.reader(open(CSV, encoding="latin1"), delimiter=";"))
    data = [r for r in rows[1:] if r and r[0].strip()]
    cols = {}
    for name, (rc, sc) in POLLUTANTS.items():
        cols[name + "_ref"] = np.array([_num(r[rc]) for r in data])
        cols[name + "_sen"] = np.array([_num(r[sc]) for r in data])
    cols["T"] = np.array([_num(r[T_COL]) for r in data])
    cols["RH"] = np.array([_num(r[RH_COL]) for r in data])
    return cols, len(data)


def _fit(sen, T, RH, ref, idx):
    m = idx & np.isfinite(sen) & np.isfinite(T) & np.isfinite(RH) & np.isfinite(ref)
    if m.sum() < 50:
        return None
    A = np.column_stack([sen[m], T[m], RH[m], np.ones(m.sum())])
    beta, *_ = np.linalg.lstsq(A, ref[m], rcond=None)
    return beta


def _apply(beta, sen, T, RH):
    return beta[0] * sen + beta[1] * T + beta[2] * RH + beta[3]


def run_cell(seed, cols, n):
    rng = np.random.default_rng(seed)
    hours = np.arange(n)
    train_mask = hours < TRAIN_HOURS
    test_mask = hours >= TRAIN_HOURS
    refresh_points = list(range(TRAIN_HOURS, n, REFRESH_HOURS))
    naive_flags, refr_flags, pol_of = [], [], []
    early_err, late_err = [], []
    mid = TRAIN_HOURS + (n - TRAIN_HOURS) // 2
    for pi, name in enumerate(POLLUTANTS):
        ref, sen = cols[name + "_ref"], cols[name + "_sen"]
        T, RH = cols["T"], cols["RH"]
        beta0 = _fit(sen, T, RH, ref, train_mask)
        if beta0 is None:
            continue
        tol = TOL_FRAC * np.nanstd(ref[train_mask])
        # rolling recalibrations (refreshed policy)
        cals = {}
        for rp in refresh_points:
            win = (hours >= rp - REFRESH_WIN) & (hours < rp)
            b = _fit(sen, T, RH, ref, win)
            cals[rp] = b if b is not None else beta0
        valid = test_mask & np.isfinite(sen) & np.isfinite(T) & np.isfinite(RH) & np.isfinite(ref)
        for h in np.where(valid)[0]:
            e_naive = abs(_apply(beta0, sen[h], T[h], RH[h]) - ref[h])
            rp = max([p for p in refresh_points if p <= h], default=refresh_points[0])
            e_refr = abs(_apply(cals[rp], sen[h], T[h], RH[h]) - ref[h])
            naive_flags.append(e_naive > tol); refr_flags.append(e_refr > tol); pol_of.append(pi)
            (early_err if h < mid else late_err).append(e_naive / (tol + 1e-9))
    naive_flags = np.array(naive_flags); refr_flags = np.array(refr_flags); pol_of = np.array(pol_of)
    bs = rng.integers(0, len(naive_flags), len(naive_flags))     # bootstrap the test set
    naive_fc = float(naive_flags[bs].mean()); refr_fc = float(refr_flags[bs].mean())
    per_pol = [float(naive_flags[pol_of == pi].mean()) for pi in range(len(POLLUTANTS))
               if (pol_of == pi).any()]
    return {
        "seed": int(seed), "mode": "uci-airquality",
        "naive_fc": round(naive_fc, 4), "refreshed_fc": round(refr_fc, 4),
        "pol_fc_spread": round(float(np.std(per_pol)), 4),          # consumer-relative
        "drift_ratio": round(float(np.mean(late_err) / (np.mean(early_err) + 1e-9)), 3),
        "n_readings": int(len(naive_flags)), "n_pollutants": len(per_pol),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "SENSORREP-family.json"))
    args = ap.parse_args()
    print("loading REAL UCI Air Quality co-location field data...", flush=True)
    cols, n = _load()
    cells = [run_cell(s, cols, n) for s in args.seeds]
    for c in cells:
        print(f"seed {c['seed']}: naive_fc={c['naive_fc']} refreshed_fc={c['refreshed_fc']} "
              f"| pol_fc_spread={c['pol_fc_spread']} drift_ratio={c['drift_ratio']}", flush=True)
    rec = {"family": "F-SENSOR", "mode": "uci-airquality",
           "sim_is_code_validation_not_evidence": False,
           "constants": {"pollutants": list(POLLUTANTS), "train_hours": TRAIN_HOURS,
                         "refresh_hours": REFRESH_HOURS, "refresh_win": REFRESH_WIN,
                         "tol_frac": TOL_FRAC,
                         "substrate": "UCI Air Quality (De Vito et al.) co-located metal-oxide "
                                      "sensors + reference analysers, ~1 yr hourly; witness = reference"},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
