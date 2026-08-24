"""XPROTO-CSI substrate on REAL 5G NR PHY (NVIDIA Sionna 1.2, open source).

The rung the MATLAB/clean-room substrates could not reach: real 3GPP 5G
LDPC coding + real QAM + a 3GPP TR38.901 TDL channel with Doppler, all
from Sionna's standard-compliant PHY (no modeled decoder, no fabricated
BLER curves). The OT measurement layer is unchanged: CQI is the consumer
certificate, HARQ ACK/NACK the witness, false-clear = BLER under CSI aging,
graded over naive / OLLA / fresh policies.

Method:
  1. Measure a real BLER(SNR) curve per MCS with Sionna's 5G LDPC over
     AWGN (batched Monte Carlo on GPU). Cached.  <-- real NR decoder.
  2. Generate a per-TTI SNR trace from a 3GPP TDL-A channel with 200 Hz
     Doppler (narrowband SISO gain).             <-- real NR channel/aging.
  3. Run the three policies over that trace, drawing HARQ ACK/NACK from
     the real per-MCS BLER curve at the ACTUAL (aged) instantaneous SNR.
     This is the 3GPP link-to-system methodology with real link curves.

Emits CSIREP-family.json (mode "nrsionna"). Runs on Atlas GPU 1
(CUDA_VISIBLE_DEVICES=1 -> logical 0; Erebus on GPU 0 untouched).
"""
import os
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
import argparse
import json
import time

import numpy as np
import tensorflow as tf
from sionna.phy.fec.ldpc import LDPC5GEncoder, LDPC5GDecoder
from sionna.phy.mapping import Mapper, Demapper, BinarySource
from sionna.phy.channel import AWGN
from sionna.phy.channel.tr38901 import TDL

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "nr_bler_curves_sionna.npz")

# 3GPP NR MCS (TS 38.214 Table 5.1.3.1-1); floored at R>=1/5 (5G LDPC's
# minimum supported rate -- real NR reaches lower rates via repetition,
# which Sionna's encoder does not expose). 13-entry span:
MCS_TABLE = [(2, 308), (2, 449), (2, 602),
             (4, 378), (4, 490), (4, 616),
             (6, 466), (6, 567), (6, 666), (6, 772), (6, 873), (6, 910), (6, 948)]
MCS_QM = [m[0] for m in MCS_TABLE]
MCS_R = [m[1] / 1024.0 for m in MCS_TABLE]

K_INFO = 1024               # info bits per code block
SNR_GRID = np.arange(-8.0, 28.01, 2.0)
NBLOCKS = 400               # blocks per SNR point (real LDPC decodes)
LDPC_ITERS = 20

# ---- fading / aging constants (mirror fam_csi.py where shared) --------
FC_HZ = 3.5e9
C0 = 3e8
FD_HZ = 200.0               # Doppler (high mobility) -- the aging regime
TTI_S = 0.001
REPORT_PERIOD = 20          # TTIs between CQI reports
MEAN_SNR_DB = 12.0
CQI_NOISE_DB = 1.0
DURATION_TTI = 6000
DELAY_SPREAD_S = 30e-9
TARGET_BLER = 0.10
OLLA_UP_DB = 0.1
OLLA_DOWN_DB = OLLA_UP_DB * (1 - TARGET_BLER) / TARGET_BLER


def measure_bler_curves():
    """Real Sionna 5G LDPC BLER(SNR) per MCS over AWGN. Cached to npz."""
    if os.path.exists(CACHE):
        z = np.load(CACHE)
        if z["grid"].shape == SNR_GRID.shape and np.allclose(z["grid"], SNR_GRID):
            print("loaded cached BLER curves", flush=True)
            return z["curves"]
    src = BinarySource()
    awgn = AWGN()
    curves = np.ones((len(MCS_TABLE), len(SNR_GRID)))
    t0 = time.time()
    for mi, (qm, R) in enumerate(zip(MCS_QM, MCS_R)):
        n = int(round(K_INFO / R))
        n += (-n) % qm                      # codeword divisible by bits/symbol
        enc = LDPC5GEncoder(K_INFO, n)
        dec = LDPC5GDecoder(enc, num_iter=LDPC_ITERS, hard_out=True)
        mapper = Mapper("qam", qm)
        demapper = Demapper("app", "qam", qm)
        for si, snr_db in enumerate(SNR_GRID):
            no = tf.pow(10.0, -snr_db / 10.0)
            b = src([NBLOCKS, K_INFO])
            y = awgn(mapper(enc(b)), no)
            bhat = dec(demapper(y, no))
            curves[mi, si] = float(tf.reduce_mean(
                tf.cast(tf.reduce_any(tf.not_equal(b, bhat), axis=1), tf.float32)))
        print(f"  MCS{mi:2d} Qm{qm} R{R:.3f}: BLER curve done "
              f"({time.time()-t0:.0f}s)", flush=True)
    np.savez(CACHE, grid=SNR_GRID, curves=curves)
    return curves


def bler_at(curves, mi, snr_db):
    return float(np.interp(snr_db, SNR_GRID, curves[mi], left=1.0, right=curves[mi, -1]))


def required_snr(curves):
    """Per-MCS SNR at which real BLER crosses the target (interp)."""
    req = np.full(len(MCS_TABLE), np.inf)
    for mi in range(len(MCS_TABLE)):
        cv = curves[mi]
        if cv[0] <= TARGET_BLER:
            req[mi] = SNR_GRID[0]
            continue
        for si in range(len(SNR_GRID) - 1):
            if cv[si] > TARGET_BLER >= cv[si + 1]:
                frac = (cv[si] - TARGET_BLER) / (cv[si] - cv[si + 1] + 1e-12)
                req[mi] = SNR_GRID[si] + frac * (SNR_GRID[si + 1] - SNR_GRID[si])
                break
    return req


def fading_snr(seed, ntti):
    """Per-TTI SNR (dB) from a 3GPP TDL-A channel with FD_HZ Doppler."""
    tf.random.set_seed(seed)
    v = FD_HZ * C0 / FC_HZ
    tdl = TDL(model="A", delay_spread=DELAY_SPREAD_S, carrier_frequency=FC_HZ,
              min_speed=v, max_speed=v)
    out = tdl(1, ntti, 1.0 / TTI_S)
    a = out[0] if isinstance(out, (tuple, list)) else out
    h = tf.reduce_sum(tf.squeeze(a), axis=0)          # narrowband SISO gain
    p = np.abs(h.numpy()) ** 2
    p /= p.mean()
    return MEAN_SNR_DB + 10 * np.log10(p + 1e-12)


def run_policy(rng, snr_db, policy, curves, req):
    ntti = len(snr_db)
    est = snr_db[0]
    offset = 0.0
    nack = 0
    seen = set()
    err = 0.0
    for n in range(ntti):
        if policy == "fresh" or n % REPORT_PERIOD == 0:
            est = snr_db[n] + rng.normal(0, CQI_NOISE_DB)     # CQI report
        sel = est + (offset if policy == "olla" else 0.0)
        cand = np.where(req <= sel)[0]
        m = int(cand[-1]) if cand.size else 0
        seen.add(m)
        is_nack = rng.random() < bler_at(curves, m, snr_db[n])  # real BLER draw
        err += abs(snr_db[n] - est)
        if is_nack:
            nack += 1
        if policy == "olla":
            offset += (-OLLA_DOWN_DB if is_nack else OLLA_UP_DB)
    return {"bler": nack / ntti, "mcs_var": len(seen), "cqi_err_db": err / ntti}


def run_cell(seed, curves, req):
    snr_db = fading_snr(seed, DURATION_TTI)
    rng = np.random.default_rng(seed)
    naive = run_policy(rng, snr_db, "naive", curves, req)
    olla = run_policy(rng, snr_db, "olla", curves, req)
    fresh = run_policy(rng, snr_db, "fresh", curves, req)
    return {
        "seed": int(seed), "mode": "nrsionna", "fd_hz": FD_HZ,
        "report_period": REPORT_PERIOD,
        "naive_bler": float(round(naive["bler"], 4)),
        "olla_bler": float(round(olla["bler"], 4)),
        "fresh_bler": float(round(fresh["bler"], 4)),
        "cqi_err_db": float(round(naive["cqi_err_db"], 3)),
        "n_tti": DURATION_TTI, "mcs_var": int(naive["mcs_var"]),
        "target_bler": TARGET_BLER,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "CSIREP-family.json"))
    args = ap.parse_args()
    print("measuring real 5G NR LDPC BLER curves (Sionna, GPU)...", flush=True)
    curves = measure_bler_curves()
    req = required_snr(curves)
    print("required SNR (dB) per MCS @ target:",
          " ".join(f"{r:.1f}" for r in req), flush=True)
    cells = []
    for seed in args.seeds:
        c = run_cell(seed, curves, req)
        cells.append(c)
        print(f"seed {seed}: naive_bler={c['naive_bler']} olla_bler={c['olla_bler']} "
              f"fresh_bler={c['fresh_bler']} cqi_err={c['cqi_err_db']}dB "
              f"mcs_var={c['mcs_var']}", flush=True)
    rec = {
        "family": "F-CSI", "mode": "nrsionna",
        "sim_is_code_validation_not_evidence": False,
        "constants": {
            "fd_hz": FD_HZ, "report_period": REPORT_PERIOD, "target_bler": TARGET_BLER,
            "mean_snr_db": MEAN_SNR_DB, "duration_tti": DURATION_TTI,
            "carrier_hz": FC_HZ, "delay_spread_s": DELAY_SPREAD_S, "k_info": K_INFO,
            "ldpc_iters": LDPC_ITERS, "nblocks_per_snr": NBLOCKS,
            "substrate": ("real 5G NR PHY via NVIDIA Sionna 1.2 (open source): "
                          "3GPP 5G LDPC (TS 38.212) + QAM + TR38.901 TDL-A channel "
                          "with 200Hz Doppler; real LDPC-measured BLER curves; "
                          "3GPP link-to-system methodology; narrowband SISO"),
        },
        "cells": cells,
    }
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
