"""XPROTO-CSI-FLIP family (F-CSI-FLIP): the two-consumer verdict inversion (the
Flip) in 5G NR link adaptation, with its taxonomy-predicted null.

Fleets (disjoint, interleaved), reading ORTHOGONAL axes of the radio state:
  M-fleet: high mobility (fd = 200 Hz), mid SNR (12 dB). Failures come from CSI
           aging between reports (the time axis).
  S-fleet: low mobility (fd = 10 Hz), low SNR (7 dB). Failures come from deep
           fades the MCS floor cannot duck (the amplitude axis).

Policies: a fixed fleet-mean SNR-margin budget (1.5 dB), allocated two ways:
  A "protect-mobility": margin proportional to each user's Doppler.
  B "protect-depth"   : the same total proportional to each user's SNR deficit.
Claim: M-fleet does better under A, S-fleet under B. Full verdict inversion at a
matched aggregate; the fleet-mean NACK rate cannot order the pair for anyone.

Registered NULL (taxonomy: aligned reads cannot invert): the SAME fleet read at
two reliability thresholds (0.1 vs 0.01) under margin policies protect-low /
protect-high in mean SNR. Thresholds are a shift of one projection, so no
inversion is expected; a policy better for one class is better for both.

Substrate: real Sionna 5G NR LDPC BLER curves + TDL-A fading (csi_sionna), held
CSI (20-TTI reports), empirical HARQ NACK rate. Run on Atlas (sionna-venv, CPU).
Emits CSIFLIPREP-family.json.
"""
import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.expanduser("~/csi"))
import csi_sionna as cs   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DURATION = 6000
REPORT_PERIOD = 20
CQI_NOISE_DB = 1.0
MARGIN_MEAN_DB = 1.5
M_FD, M_SNR = 200.0, 12.0        # mobility readers
S_FD, S_SNR = 10.0, 7.0          # depth readers
N_PER_FLEET = 12                 # users per fleet per seed


def _trace(seed, fd, mean_snr):
    cs.FD_HZ = fd
    return cs.fading_snr(seed, DURATION) - cs.MEAN_SNR_DB + mean_snr


def _nack(snr, margin, curves, req, seed, target_shift_db=0.0):
    """Empirical HARQ NACK rate: held CSI, MCS from estimate - margin, decode drawn
    from the real LDPC curve at the true SNR. target_shift_db shifts the required
    table (the threshold-pair null)."""
    rng = np.random.default_rng(seed)
    r = req + target_shift_db
    est = snr[0]
    nack = 0
    for n, s in enumerate(snr):
        if n % REPORT_PERIOD == 0:
            est = s + rng.normal(0, CQI_NOISE_DB)
        cand = np.where(r + margin <= est)[0]
        m = int(cand[-1]) if len(cand) else 0
        if rng.random() < cs.bler_at(curves, m, s):
            nack += 1
    return nack / len(snr)


def run_cell(seed, curves, req):
    out = {"seed": int(seed), "mode": "nrsionna", "n_per_fleet": N_PER_FLEET,
           "margin_mean_db": MARGIN_MEAN_DB}
    # ---- flip construction: misaligned reads (time axis vs amplitude axis) ----
    users = []
    for k in range(N_PER_FLEET):
        users.append(("M", _trace(seed * 31 + k, M_FD, M_SNR), M_FD, M_SNR))
    for k in range(N_PER_FLEET):
        users.append(("S", _trace(seed * 31 + 100 + k, S_FD, S_SNR), S_FD, S_SNR))
    fds = np.array([u[2] for u in users])
    deficit = np.array([max(0.0, 12.0 - u[3]) + 0.05 for u in users])
    m_a = fds / fds.mean() * MARGIN_MEAN_DB                 # protect-mobility
    m_b = deficit / deficit.mean() * MARGIN_MEAN_DB         # protect-depth
    for m, tag in ((m_a, "A"), (m_b, "B")):
        out[f"mean_margin_{tag}"] = round(float(m.mean()), 4)
        for fleet in ("M", "S"):
            vals = [_nack(u[1], m[i], curves, req, seed * 7 + i)
                    for i, u in enumerate(users) if u[0] == fleet]
            out[f"fc_{fleet}_{tag}"] = round(float(np.mean(vals)), 4)
        out[f"fc_fleet_{tag}"] = round(0.5 * (out[f"fc_M_{tag}"] + out[f"fc_S_{tag}"]), 4)
    out["flip"] = bool(out["fc_M_A"] < out["fc_M_B"] and out["fc_S_B"] < out["fc_S_A"])
    # ---- null construction: one fleet (M), two thresholds (0.1 vs 0.01-equivalent
    # +2 dB shift), margin bumps protect-low / protect-high in mean SNR ----
    snr0 = _trace(seed * 31 + 500, M_FD, M_SNR)
    for kind, tag in (("low", "A"), ("high", "B")):
        m = 2.0 * MARGIN_MEAN_DB if kind == "low" else 0.5 * MARGIN_MEAN_DB
        out[f"null_fc_t1_{tag}"] = round(_nack(snr0, m, curves, req, seed + 900, 0.0), 4)
        out[f"null_fc_t2_{tag}"] = round(_nack(snr0, m, curves, req, seed + 900, 2.0), 4)
    out["null_flip"] = bool(out["null_fc_t1_A"] < out["null_fc_t1_B"]
                            and out["null_fc_t2_B"] < out["null_fc_t2_A"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "CSIFLIPREP-family.json"))
    args = ap.parse_args()
    print("loading real 5G NR LDPC curves...", flush=True)
    curves = cs.measure_bler_curves()
    req = cs.required_snr(curves)
    cells = []
    for s in args.seeds:
        c = run_cell(s, curves, req)
        cells.append(c)
        print(f"seed {s}: M A={c['fc_M_A']} B={c['fc_M_B']} | S A={c['fc_S_A']} "
              f"B={c['fc_S_B']} | fleet A={c['fc_fleet_A']} B={c['fc_fleet_B']} | "
              f"FLIP={c['flip']} null_flip={c['null_flip']}", flush=True)
    rec = {"family": "F-CSI-FLIP", "mode": "nrsionna",
           "constants": {"m_fd_hz": M_FD, "m_snr_db": M_SNR, "s_fd_hz": S_FD,
                         "s_snr_db": S_SNR, "margin_mean_db": MARGIN_MEAN_DB,
                         "report_period": REPORT_PERIOD, "duration": DURATION,
                         "substrate": "real Sionna 5G NR LDPC + TDL-A, held CSI"},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
