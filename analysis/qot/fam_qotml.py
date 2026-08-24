"""XPROTO-QOT Result 2 (F-QOTML): the ML-QoT objective is consumer-misaligned.

An ML-QoT estimator trained to minimize AVERAGE GSNR error (reconstruction) is
optimizing the wrong thing: the consumer -- the FEC decoder -- reads a THRESHOLD, so
a small over-prediction near a modulation boundary flips a format decision and
false-clears. A consumer/threshold-aware objective (conservative lower-quantile
regression) wins the decision at a small capacity cost. The reconstruction-vs-
consumer dissociation (the book's VALUE thesis; the XPROTO-AICSI lesson) in ML-QoT.

  * feature = provisioning-time (reference-loading) GSNR + (position, reach, load).
  * label / witness = the true deployed GSNR (full loading).
  * mse: minimize mean error; aware: conservative quantile (decision-aware).
  * false-clear = the format selected from the prediction fails the true GSNR.

Substrate: GNPy GN-model GSNR (reuses fam_qot). scikit-learn estimators.
Emits QOTMLREP-family.json.
"""
from __future__ import annotations

import argparse
import json
import os
import warnings

import numpy as np

warnings.filterwarnings("ignore")
import fam_qot as q  # noqa: E402  (GNPy GSNR combs + MODS/REQ/BPS)
from sklearn.ensemble import GradientBoostingRegressor  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

REF_LOAD = 6                       # provisioning-time (reference) loading
LOADINGS = [6, 20, 40, 60, 76]     # deployed loading levels the estimator must predict
N_POS = 40                         # positions sampled per (reach, loading)
MARGIN_DB = 0.5                    # design margin applied to the prediction
AWARE_QUANTILE = 0.15              # consumer-aware objective: conservative lower quantile
HIDDEN_NOISE_DB = 0.8             # irreducible GSNR uncertainty (unmeasured state) the
                                  # estimator cannot predict -- the real ML-QoT regime


def _dataset():
    """Build (features, true GSNR) over reach x deployed-loading x position, from GNPy."""
    combs_ref = {ns: q._gsnr_comb(REF_LOAD, ns) for ns in q.SPAN_SET}
    combs = {(nch, ns): q._gsnr_comb(nch, ns) for ns in q.SPAN_SET for nch in LOADINGS}
    X, y = [], []
    pos = np.linspace(0.0, 1.0, N_POS)
    for ns in q.SPAN_SET:
        gref = combs_ref[ns]
        for nch in LOADINGS:
            gact = combs[(nch, ns)]
            for p in pos:
                ref_g = float(gref[round(p * (len(gref) - 1))])
                true_g = float(gact[round(p * (len(gact) - 1))])
                X.append([ref_g, p, ns, nch]); y.append(true_g)
    return np.array(X), np.array(y)


def _select(pred_gsnr):
    ok = np.where(q.REQ <= pred_gsnr - MARGIN_DB)[0]
    return ok[-1] if ok.size else -1


def _eval(pred, true):
    fc = fails = 0; bps = 0.0; n = len(true)
    for pr, tr in zip(pred, true):
        m = _select(pr)
        if m < 0:
            continue
        if q.REQ[m] > tr:                 # selected format fails the true GSNR
            fc += 1
        else:
            bps += q.BPS[m]               # delivered spectral efficiency
        fails += 0
    return fc / n, float(np.mean(np.abs(pred - true))), bps / n


def run_cell(seed, X, y):
    rng = np.random.default_rng(seed)
    # the true deployed GSNR carries an irreducible, unmeasured impairment the
    # estimator cannot predict from features (the real ML-QoT regime); it IS the witness.
    y_true = y + rng.normal(0, HIDDEN_NOISE_DB, len(y))
    idx = rng.permutation(len(y)); cut = int(0.7 * len(y))
    tr, te = idx[:cut], idx[cut:]
    mse = GradientBoostingRegressor(loss="squared_error", random_state=seed).fit(X[tr], y_true[tr])
    aware = GradientBoostingRegressor(loss="quantile", alpha=AWARE_QUANTILE,
                                      random_state=seed).fit(X[tr], y_true[tr])
    fc_m, mae_m, bps_m = _eval(mse.predict(X[te]), y_true[te])
    fc_a, mae_a, bps_a = _eval(aware.predict(X[te]), y_true[te])
    return {
        "seed": int(seed), "mode": "gnpy+sklearn",
        "mae_mse": round(mae_m, 4), "mae_aware": round(mae_a, 4),   # MSE wins reconstruction
        "fc_mse": round(fc_m, 4), "fc_aware": round(fc_a, 4),       # aware wins the consumer
        "bps_mse": round(bps_m, 3), "bps_aware": round(bps_a, 3),
        "n_test": int(len(te)),
    }


def _headroom(true):
    """GSNR above the nearest format threshold it supports (small => near the cliff)."""
    ok = np.where(q.REQ <= true)[0]
    return float(true - q.REQ[int(ok[-1])]) if ok.size else float("nan")


def _preds(seed, X, y):
    """Per-test-sample records for Fig. 2. Reproduces run_cell's split/fit/predict."""
    rng = np.random.default_rng(seed)
    y_true = y + rng.normal(0, HIDDEN_NOISE_DB, len(y))
    idx = rng.permutation(len(y)); cut = int(0.7 * len(y))
    tr, te = idx[:cut], idx[cut:]
    mse = GradientBoostingRegressor(loss="squared_error", random_state=seed).fit(X[tr], y_true[tr])
    aware = GradientBoostingRegressor(loss="quantile", alpha=AWARE_QUANTILE,
                                      random_state=seed).fit(X[tr], y_true[tr])
    pm, pa, yt = mse.predict(X[te]), aware.predict(X[te]), y_true[te]
    recs = []
    for i in range(len(te)):
        mm, ma = _select(pm[i]), _select(pa[i])
        recs.append({"seed": int(seed), "true": round(float(yt[i]), 3),
                     "pred_mse": round(float(pm[i]), 3), "pred_aware": round(float(pa[i]), 3),
                     "headroom": round(_headroom(yt[i]), 3),
                     "mse_fail": bool(mm >= 0 and q.REQ[mm] > yt[i]),
                     "aware_fail": bool(ma >= 0 and q.REQ[ma] > yt[i])})
    return recs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "QOTMLREP-family.json"))
    ap.add_argument("--preds-out", default=None,
                    help="also dump per-test-sample records (for Fig. 2) to this JSON")
    args = ap.parse_args()
    print("building GNPy GSNR dataset (reach x loading x position)...", flush=True)
    X, y = _dataset()
    cells = [run_cell(s, X, y) for s in args.seeds]
    for c in cells:
        print(f"seed {c['seed']}: MAE mse={c['mae_mse']} aware={c['mae_aware']} (mse wins recon) "
              f"| FC mse={c['fc_mse']} aware={c['fc_aware']} (aware wins consumer) "
              f"| bps mse={c['bps_mse']} aware={c['bps_aware']}", flush=True)
    rec = {"family": "F-QOTML", "mode": "gnpy+sklearn",
           "sim_is_code_validation_not_evidence": False,
           "constants": {"ref_load": REF_LOAD, "loadings": LOADINGS, "n_pos": N_POS,
                         "margin_db": MARGIN_DB, "aware_quantile": AWARE_QUANTILE,
                         "substrate": "GNPy GN-model GSNR (fam_qot) + sklearn GBR; MSE vs "
                                      "conservative-quantile objective; witness = true GSNR"},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)
    if args.preds_out:
        preds = [r for s in args.seeds for r in _preds(s, X, y)]
        json.dump({"family": "F-QOTML", "records": preds}, open(args.preds_out, "w"), indent=1)
        print(f"wrote {len(preds)} per-prediction records -> {args.preds_out}", flush=True)


if __name__ == "__main__":
    main()
