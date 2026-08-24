"""OT-14 refresh-floor law, measured on the real 5G NR substrate (Sionna).

The refresh floor is the largest CQI report period that keeps the raw-CQI
(naive) false-clear rate within a threshold, as a function of the channel's
Doppler / coherence time. OT-14 predicts floor is proportional to coherence
time (Clarke: Tcoh = 0.423 / f_d). This sweeps f_d x report_period through
the real Sionna LDPC BLER curves + TDL channel and fits the law.

Exploration (not a sealed cell): it strengthens XPROTO-CSI and gives the
derivable-refresh-floor claim an empirical curve. Writes CSI-refreshfloor.json
+ CSI-refreshfloor.png.  Run on Atlas GPU 1.
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

FDS = [10, 25, 50, 100, 200, 400]          # Doppler (Hz) -> coherence times
PERIODS = [1, 2, 5, 10, 20, 40, 80]        # CQI report period (TTIs = ms)
NTTI = 6000
SEED = 0
THR = 0.15                                  # floor threshold (1.5x the target)


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


def naive_bler(snr_db, period, curves, req, rng):
    est = snr_db[0]
    nack = 0
    for n in range(len(snr_db)):
        if n % period == 0:
            est = snr_db[n] + rng.normal(0, cs.CQI_NOISE_DB)
        cand = np.where(req <= est)[0]
        m = int(cand[-1]) if cand.size else 0
        if rng.random() < cs.bler_at(curves, m, snr_db[n]):
            nack += 1
    return nack / len(snr_db)


def floor_of(periods, blers, thr):
    periods = np.asarray(periods, float)
    blers = np.asarray(blers)
    if blers[0] > thr:
        return periods[0], "censored_low"
    for i in range(len(periods) - 1):
        if blers[i] <= thr < blers[i + 1]:
            lp = np.interp(thr, [blers[i], blers[i + 1]],
                           [np.log(periods[i]), np.log(periods[i + 1])])
            return float(np.exp(lp)), "ok"
    return periods[-1], "censored_high"


def main():
    print("loading real NR BLER curves...", flush=True)
    curves = cs.measure_bler_curves()
    req = cs.required_snr(curves)
    grid = {}
    floors = {}
    for fd in FDS:
        snr = fading_fd(SEED, NTTI, fd)
        row = []
        for P in PERIODS:
            rng = np.random.default_rng(1000 + P)     # same noise seed across fd
            row.append(round(naive_bler(snr, P, curves, req, rng), 4))
        grid[fd] = row
        fl, flag = floor_of(PERIODS, row, THR)
        tcoh_ms = 0.423 / fd * 1000.0
        floors[fd] = {"floor_tti": round(fl, 2), "tcoh_ms": round(tcoh_ms, 2), "flag": flag}
        print(f"fd={fd:4d}Hz Tcoh={tcoh_ms:6.2f}ms  BLER@periods={row}  "
              f"floor={fl:.2f}ms [{flag}]", flush=True)

    # fit floor ~ k * Tcoh through the origin, using non-censored points
    xs = np.array([floors[fd]["tcoh_ms"] for fd in FDS if floors[fd]["flag"] == "ok"])
    ys = np.array([floors[fd]["floor_tti"] for fd in FDS if floors[fd]["flag"] == "ok"])
    if len(xs) >= 2:
        k = float(np.sum(xs * ys) / np.sum(xs * xs))       # LS through origin
        ss_res = float(np.sum((ys - k * xs) ** 2))
        ss_tot = float(np.sum((ys - ys.mean()) ** 2))
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    else:
        k, r2 = float("nan"), float("nan")
    print(f"\nOT-14 fit: refresh_floor_ms ~ {k:.3f} * Tcoh_ms  (R^2={r2:.3f}, "
          f"{len(xs)} non-censored points)", flush=True)

    out = {"fds_hz": FDS, "periods_tti": PERIODS, "threshold_bler": THR,
           "mean_snr_db": cs.MEAN_SNR_DB, "bler_grid": grid, "floors": floors,
           "fit": {"floor_ms_per_tcoh_ms": k, "r2": r2},
           "law": "OT-14 refresh floor proportional to Clarke coherence time 0.423/fd"}
    json.dump(out, open(os.path.join(cs.HERE, "CSI-refreshfloor.json"), "w"), indent=1)

    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for fd in FDS:
        ax[0].plot(PERIODS, grid[fd], "o-", label=f"{fd} Hz")
    ax[0].axhline(THR, ls="--", c="k", lw=1, label=f"floor thr {THR}")
    ax[0].axhline(cs.TARGET_BLER, ls=":", c="grey", lw=1, label=f"target {cs.TARGET_BLER}")
    ax[0].set_xscale("log"); ax[0].set_xlabel("CQI report period (TTI = ms)")
    ax[0].set_ylabel("naive BLER (false-clear)"); ax[0].legend(fontsize=7)
    ax[0].set_title("CSI aging: false-clear vs report period (real 5G NR / Sionna)")
    tc = np.array([floors[fd]["tcoh_ms"] for fd in FDS])
    fj = np.array([floors[fd]["floor_tti"] for fd in FDS])
    ax[1].plot(tc, fj, "s", ms=8)
    xline = np.linspace(0, tc.max() * 1.05, 50)
    ax[1].plot(xline, k * xline, "r-", lw=1.5, label=f"floor ~ {k:.2f}*Tcoh (R2={r2:.2f})")
    ax[1].set_xlabel("coherence time Tcoh = 0.423/fd (ms)")
    ax[1].set_ylabel("refresh floor (ms)"); ax[1].legend(fontsize=8)
    ax[1].set_title("OT-14 refresh-floor law")
    fig.tight_layout()
    fig.savefig(os.path.join(cs.HERE, "CSI-refreshfloor.png"), dpi=110)
    print("wrote CSI-refreshfloor.json + CSI-refreshfloor.png", flush=True)


if __name__ == "__main__":
    main()
