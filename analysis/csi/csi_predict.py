"""6G AI-native channel prediction vs the OT-14 refresh floor.

The refresh-floor law (OT-14) says a CSI certificate must be refreshed on the
timescale the channel decorrelates (report period proportional to coherence
time). The 6G "AI-native" hope is to REPORT LESS OFTEN and PREDICT the aged
channel forward instead. This asks, rigorously: does prediction extend the
usable report period, or does the coherence time cap it?

We give prediction its best case -- the optimal LINEAR (Wiener) predictor for the
real Sionna TDL fading process, using the M most recent CSI samples to predict
the effective SINR Delta steps ahead. We compare its error to the naive
(hold-the-last-report) error, versus lookahead Delta, across Doppler regimes.
If even the optimal linear predictor cannot beat naive beyond ~one coherence
time, the refresh floor is a fundamental wall, not an artifact of not predicting.

Exploration (no seal), on the same real 5G NR substrate as XPROTO-CSI.
Emits CSI-PREDICT.json + CSI-PREDICT.png.
"""
import os
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
import json

import numpy as np
import tensorflow as tf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sionna.phy.channel.tr38901 import TDL

import csi_sionna as cs

FDS = [50.0, 200.0]          # two coherence regimes (Tcoh = 0.423/fd)
NTTI = 12000
M = 8                        # predictor taps (recent CSI samples)
DELTAS = list(range(1, 61))  # lookahead in TTIs (= ms)
SEED = 0


def fading_snr_fd(seed, ntti, fd):
    tf.random.set_seed(seed)
    v = fd * cs.C0 / cs.FC_HZ
    tdl = TDL(model="A", delay_spread=cs.DELAY_SPREAD_S, carrier_frequency=cs.FC_HZ,
              min_speed=v, max_speed=v)
    out = tdl(1, ntti, 1.0 / cs.TTI_S)
    a = out[0] if isinstance(out, (tuple, list)) else out
    h = tf.reduce_sum(tf.squeeze(a), axis=0)
    p = np.abs(h.numpy()) ** 2
    p /= p.mean()
    return cs.MEAN_SNR_DB + 10 * np.log10(p + 1e-12)   # effective SINR (dB)


def errors(sinr, deltas, m):
    """Mean |error| in dB for the naive (hold) estimator and the optimal M-tap
    linear (Wiener) predictor, at each lookahead Delta."""
    s = sinr - sinr.mean()
    n = len(s)
    maxlag = m + max(deltas) + 1
    r = np.array([float(np.mean(s[:n - k] * s[k:])) for k in range(maxlag)])
    R = np.array([[r[abs(i - j)] for j in range(m)] for i in range(m)])
    R += 1e-6 * np.eye(m)
    naive, pred = {}, {}
    for D in deltas:
        w = np.linalg.solve(R, r[D:D + m])          # Wiener weights (Delta-step)
        en, ep = [], []
        for t in range(D + m, n):
            past = s[t - D:t - D - m:-1]             # [s[t-D], ..., s[t-D-M+1]]
            ep.append(abs(s[t] - w @ past))
            en.append(abs(s[t] - s[t - D]))          # naive: hold s[t-D]
        naive[D] = float(np.mean(en)); pred[D] = float(np.mean(ep))
    return naive, pred


def main():
    cells = {}
    fig, axes = plt.subplots(1, len(FDS), figsize=(11, 4.2), sharey=True)
    for ax, fd in zip(axes, FDS):
        sinr = fading_snr_fd(SEED, NTTI, fd)
        naive, pred = errors(sinr, DELTAS, M)
        tcoh_ms = 0.423 / fd * 1000.0
        # "usable" error budget = naive error at the sealed 20 ms report period
        budget = naive[20]
        # horizons: max Delta with error <= budget (naive vs predicted)
        nf = max([D for D in DELTAS if naive[D] <= budget], default=DELTAS[0])
        pf = max([D for D in DELTAS if pred[D] <= budget], default=DELTAS[0])
        cells[fd] = {"tcoh_ms": round(tcoh_ms, 2), "budget_db": round(budget, 3),
                     "naive_horizon_ms": nf, "pred_horizon_ms": pf,
                     "extension_ms": pf - nf,
                     "extension_in_tcoh": round((pf - nf) / tcoh_ms, 3),
                     "naive_err": {D: round(naive[D], 3) for D in DELTAS},
                     "pred_err": {D: round(pred[D], 3) for D in DELTAS}}
        print(f"fd={fd:.0f}Hz Tcoh={tcoh_ms:.1f}ms: naive horizon {nf}ms, "
              f"pred horizon {pf}ms, extension {pf-nf}ms (~{(pf-nf)/tcoh_ms:.2f} Tcoh)",
              flush=True)
        xs = DELTAS
        ax.plot(xs, [naive[D] for D in xs], "o-", ms=3, label="naive (hold last report)")
        ax.plot(xs, [pred[D] for D in xs], "s-", ms=3, label="Wiener prediction")
        ax.axhline(budget, ls=":", c="grey", lw=1, label="error budget (naive@20ms)")
        ax.axvline(tcoh_ms, ls="-.", c="green", lw=1, label=f"Tcoh={tcoh_ms:.0f}ms")
        ax.set_xlabel("lookahead Δ (ms)"); ax.set_title(f"fd={fd:.0f} Hz")
        ax.legend(fontsize=7)
    axes[0].set_ylabel("mean SINR estimate error (dB)")
    fig.suptitle("Channel prediction vs the OT-14 refresh floor: "
                 "the coherence time is a wall prediction shifts but does not break")
    fig.tight_layout()
    fig.savefig(os.path.join(cs.HERE, "CSI-PREDICT.png"), dpi=120)
    json.dump({"fds_hz": FDS, "m_taps": M, "note": "extension is the extra lookahead "
               "the optimal linear predictor buys at the naive@20ms error budget",
               "cells": {str(k): v for k, v in cells.items()}},
              open(os.path.join(cs.HERE, "CSI-PREDICT.json"), "w"), indent=1)
    print("wrote CSI-PREDICT.json + CSI-PREDICT.png", flush=True)


if __name__ == "__main__":
    main()
