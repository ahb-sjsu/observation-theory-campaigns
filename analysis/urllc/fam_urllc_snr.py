"""XPROTO-URLLC-SNR family (F-URLLC-SNR): SNR-robustness of the reliability-target
consumer-relativity. Answers the reviewer's "one mean SNR" concern.

Sweeps mean SNR from cell edge to cell centre and measures the eMBB, URLLC-naive, and
URLLC-aware achieved BLER at each point (real Sionna 5G NR LDPC curves + TDL-A fading, via
csi_sionna; fresh CSI, sigma=1 dB). Because AMC selects the MCS to ride the eMBB BLER
target at every SNR, the URLLC-naive false-clear multiple is expected to be roughly
SNR-INVARIANT across the operating range; at cell edge the lowest MCS cannot meet target,
so even the eMBB certificate false-clears -- the SNR-relativity the reviewer predicted.

Mean SNR is swept by offset: fading_snr(seed) = MEAN_SNR_DB + fluctuation, so
trace_M(t) = M + (fading_snr(seed) - MEAN_SNR_DB). Only K*seeds Sionna calls; the sweep
is arithmetic. Run on Atlas (imports csi_sionna). Emits URLLCSNRREP-family.json.
"""
import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "csi"))
import csi_sionna as cs   # noqa: E402  (real Sionna 5G NR LDPC curves + TDL fading)

HERE = os.path.dirname(os.path.abspath(__file__))
EMBB_TARGET = 1e-1
URLLC_TARGET = 1e-3          # measurable proxy for the real 1e-5
URLLC_MARGIN_DB = 4.0        # conservative-MCS backoff
DIVERSITY_K = 3             # independent frequency/spatial diversity branches
CQI_NOISE_DB = 1.0
DURATION = 6000
SNR_GRID_DB = [3, 6, 9, 12, 15, 18, 21]   # cell edge -> cell centre


def run_cell(seed, curves, req10):
    rng = np.random.default_rng(seed)
    # K independent fading FLUCTUATIONS (built-in mean removed so we can sweep it)
    fluct = [cs.fading_snr(seed * 7 + k, DURATION) - cs.MEAN_SNR_DB for k in range(DIVERSITY_K)]
    noise = rng.normal(0, CQI_NOISE_DB, DURATION)     # fresh-CSI report noise (fixed draw)
    sweep = {}
    for M in SNR_GRID_DB:
        branches = [M + f for f in fluct]
        true = branches[0]
        ae = an = aa = 0.0
        for t in range(DURATION):
            cqi = true[t] + noise[t]
            ce = np.where(req10 <= cqi)[0]
            m_embb = int(ce[-1]) if ce.size else 0
            cu = np.where(req10 + URLLC_MARGIN_DB <= cqi)[0]
            m_urllc = int(cu[-1]) if cu.size else 0
            ae += cs.bler_at(curves, m_embb, true[t])          # eMBB under its cert
            an += cs.bler_at(curves, m_embb, true[t])          # URLLC under the eMBB cert
            p = 1.0
            for br in branches:                                # K-branch diversity
                p *= cs.bler_at(curves, m_urllc, br[t])
            aa += p
        sweep[str(M)] = {"embb": round(ae / DURATION, 5),
                         "urllc_naive": round(an / DURATION, 5),
                         "urllc_aware": round(aa / DURATION, 7)}
    return {"seed": int(seed), "mode": "nrsionna", "snr_grid_db": SNR_GRID_DB,
            "embb_target": EMBB_TARGET, "urllc_target": URLLC_TARGET, "sweep": sweep}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "URLLCSNRREP-family.json"))
    args = ap.parse_args()
    print("loading real 5G NR LDPC curves...", flush=True)
    curves = cs.measure_bler_curves()
    req10 = cs.required_snr(curves)
    cells = [run_cell(s, curves, req10) for s in args.seeds]
    for c in cells:
        row = " ".join(f"{m}dB:{c['sweep'][str(m)]['embb']:.3f}/"
                       f"{c['sweep'][str(m)]['urllc_naive']:.3f}/"
                       f"{c['sweep'][str(m)]['urllc_aware']:.1e}" for m in SNR_GRID_DB)
        print(f"seed {c['seed']} (embb/un/ua): {row}", flush=True)
    rec = {"family": "F-URLLC-SNR", "mode": "nrsionna",
           "constants": {"snr_grid_db": SNR_GRID_DB, "embb_target": EMBB_TARGET,
                         "urllc_target": URLLC_TARGET, "urllc_margin_db": URLLC_MARGIN_DB,
                         "diversity_k": DIVERSITY_K, "cqi_noise_db": CQI_NOISE_DB,
                         "duration": DURATION,
                         "substrate": "real Sionna 5G NR LDPC curves + TDL-A fading, fresh CSI"},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
