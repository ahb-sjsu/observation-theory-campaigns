"""Clean-room 5G NR link-level substrate for XPROTO-CSI.

STATUS: written but NOT run/validated -- superseded by csi_sionna.py (real
5G LDPC via Sionna) before this was executed. Kept as the documented
"modeled-decoder" fallback rung in SUBSTRATE.md's substrate ladder, usable
if Sionna is ever unavailable. Not part of the sealed evidence.


Built from PUBLIC 3GPP specifications only -- no third-party source
(no MATLAB 5G Toolbox, no srsRAN/OAI/Sionna code was read). Provenance of
every constant is cited inline so the clean-room boundary is auditable:

  * CQI table   -- TS 38.214 v17, Table 5.2.2.1-2 (up to 64QAM).
  * MCS table   -- TS 38.214 v17, Table 5.1.3.1-1 (64QAM table, MCS 0-28).
  * Modulation  -- Gray-mapped square M-QAM (TS 38.211 clause 5.1); the
                   constellation-constrained (CM) capacity of each order is
                   measured here by Monte Carlo (real symbols + real AWGN).
  * Channel     -- a tapped-delay-line with an EXPONENTIAL power-delay
                   profile (a standard, exactly-specifiable TDL; NOT the
                   38.901 TDL-C 24-tap profile -- that is a drop-in later
                   fidelity rung) + Clarke/Jakes Doppler (sum-of-sinusoids).
  * Link->system -- MIESM / RBIR (Received Bit-mutual-Information Rate): a
                   coded block decodes iff the mean received MI-per-bit over
                   the allocation reaches the code rate. This is the
                   3GPP-endorsed, decoder-agnostic link-to-system mapping;
                   it needs no fabricated BLER curves and no LDPC decoder.
                   Real LDPC (TS 38.212) would be the next rung.

The MEASUREMENT layer on top -- CQI as a consumer certificate, HARQ
ACK/NACK as the witness, false-clear rate under CSI aging, naive/OLLA/
fresh policies -- is the OT contribution and is identical to fam_csi.py.
This module only replaces the *substrate* with real NR PHY physics.

Pure numpy; runs anywhere (locally or on Atlas). Emits CSIREP-family.json
with mode "nrclean".
"""

from __future__ import annotations

import argparse
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "nr_capacity_cache.npz")

# ---- 3GPP NR MCS table (TS 38.214 Table 5.1.3.1-1): (Qm, R*1024) ------
MCS_TABLE = [
    (2, 120), (2, 157), (2, 193), (2, 251), (2, 308), (2, 379), (2, 449),
    (2, 526), (2, 602), (2, 679),                                    # 0-9  QPSK
    (4, 340), (4, 378), (4, 434), (4, 490), (4, 553), (4, 616), (4, 658),  # 10-16 16QAM
    (6, 438), (6, 466), (6, 517), (6, 567), (6, 616), (6, 666), (6, 719),
    (6, 772), (6, 822), (6, 873), (6, 910), (6, 948),                # 17-28 64QAM
]
MCS_QM = np.array([m[0] for m in MCS_TABLE])
MCS_R = np.array([m[1] / 1024.0 for m in MCS_TABLE])   # code rate (info/coded)

# ---- sealed cell constants (mirror fam_csi.py; bars reference these) --
TTI_S = 0.001
FD_HZ = 200.0            # Doppler (high mobility) -- the aging regime
REPORT_PERIOD = 20       # TTIs between CQI reports
MEAN_SNR_DB = 12.0
CQI_NOISE_DB = 1.0
TARGET_BLER = 0.10
DURATION_TTI = 6000
N_SC = 100               # PDSCH subcarriers (freq-selectivity sample)
SCS_HZ = 30e3            # numerology mu=1
DS_S = 300e-9            # RMS delay spread (exponential PDP)
N_TAPS = 8
N_SINUSOIDS = 20         # Clarke/Jakes oscillators per tap
RBIR_W = 0.03            # link-to-system transition width (RBIR units)
OLLA_UP_DB = 0.1
OLLA_DOWN_DB = OLLA_UP_DB * (1 - TARGET_BLER) / TARGET_BLER   # eq. at target

SNR_GRID_DB = np.arange(-12.0, 36.0, 0.5)
QMS = [2, 4, 6, 8]


# ---- real QAM + constellation-constrained capacity (Monte Carlo) ------
def qam_constellation(qm: int) -> np.ndarray:
    m = int(round(math.sqrt(2 ** qm)))          # PAM levels per axis
    lv = np.arange(-(m - 1), m, 2, dtype=float)
    I, Q = np.meshgrid(lv, lv)
    pts = (I + 1j * Q).ravel()
    return pts / math.sqrt(np.mean(np.abs(pts) ** 2))   # unit avg energy


def _cm_capacity(qm: int, snr_db_grid: np.ndarray, rng, nmc: int) -> np.ndarray:
    """CM capacity (bits/symbol) of Gray M-QAM over AWGN, by Monte Carlo:
    I = Qm - E_{x,n}[ log2 sum_{x'} exp(-(|x+n-x'|^2 - |n|^2)/N0) ]."""
    pts = qam_constellation(qm)
    M = len(pts)
    out = np.empty_like(snr_db_grid)
    n = (rng.standard_normal(nmc) + 1j * rng.standard_normal(nmc)) / math.sqrt(2)
    for gi, snr_db in enumerate(snr_db_grid):
        N0 = 10 ** (-snr_db / 10.0)
        noise = n * math.sqrt(N0)
        acc = 0.0
        for x in pts:
            y = x + noise                                   # (nmc,)
            d = np.abs(y[:, None] - pts[None, :]) ** 2      # (nmc, M)
            dx = np.abs(noise) ** 2                         # (nmc,)
            inner = np.exp(-(d - dx[:, None]) / N0).sum(axis=1)
            acc += np.mean(np.log2(inner))
        out[gi] = qm - acc / M
    return out


def capacity_tables():
    """Precompute (and cache) CM-capacity curves for each Qm."""
    if os.path.exists(CACHE):
        z = np.load(CACHE)
        if z["grid"].shape == SNR_GRID_DB.shape and np.allclose(z["grid"], SNR_GRID_DB):
            return {q: z[f"cap{q}"] for q in QMS}
    rng = np.random.default_rng(12345)          # fixed -> reproducible tables
    tabs = {}
    for q in QMS:
        nmc = 4000 if q < 8 else 1500           # 256QAM is heavier
        tabs[q] = _cm_capacity(q, SNR_GRID_DB, rng, nmc)
    np.savez(CACHE, grid=SNR_GRID_DB, **{f"cap{q}": tabs[q] for q in QMS})
    return tabs


CAP = None      # {Qm: capacity(bits/sym) over SNR_GRID_DB}


def _cap(qm: int, snr_db):
    return np.interp(snr_db, SNR_GRID_DB, CAP[qm])


def rbir(qm: int, sinr_db_row: np.ndarray) -> float:
    """Received bit-MI rate over the allocation: mean CM-capacity / Qm."""
    return float(np.mean(_cap(qm, sinr_db_row)) / qm)


def eff_sinr_db(sinr_db_row: np.ndarray, ref_qm: int = 6) -> float:
    """MIESM effective SINR: the flat SINR giving the same mean MI (ref
    modulation) as this frequency-selective allocation."""
    mean_mi = float(np.mean(_cap(ref_qm, sinr_db_row)))
    cap_ref = CAP[ref_qm]
    return float(np.interp(mean_mi, cap_ref, SNR_GRID_DB))   # cap_ref monotone


def required_sinr_db():
    """Per-MCS flat SINR at which decode succeeds w.p. 0.9 (BLER=target)."""
    tgt_logit = math.log((1 - TARGET_BLER) / TARGET_BLER)     # logit(0.9)
    req = np.empty(len(MCS_TABLE))
    for i, (qm, R) in enumerate(zip(MCS_QM, MCS_R)):
        target_rbir = R + RBIR_W * tgt_logit
        curve = CAP[qm] / qm
        if target_rbir >= curve[-1]:
            req[i] = np.inf
        else:
            req[i] = float(np.interp(target_rbir, curve, SNR_GRID_DB))
    return req


# ---- exponential-PDP TDL channel with Clarke/Jakes Doppler ------------
def channel_sinr(rng: np.random.Generator, ntti: int, fd: float,
                 mean_snr_db: float) -> np.ndarray:
    """Return per-TTI, per-subcarrier SINR in dB, shape (ntti, N_SC).
    Exponential PDP (RMS delay spread DS_S), each tap Rayleigh via a
    Clarke sum-of-sinusoids in time (Doppler fd)."""
    delays = np.arange(N_TAPS) * (DS_S)                 # tap delays (s)
    powers = np.exp(-delays / DS_S)
    powers /= powers.sum()                               # sum-power = 1
    t = np.arange(ntti) * TTI_S
    g = np.zeros((ntti, N_TAPS), dtype=complex)
    for l in range(N_TAPS):
        alpha = rng.uniform(0, 2 * math.pi, N_SINUSOIDS)   # AoA per oscillator
        phi = rng.uniform(0, 2 * math.pi, N_SINUSOIDS)     # random phase
        # sum_m exp(j[2*pi*fd*t*cos(alpha_m) + phi_m]) / sqrt(M) -> ~CN(0,1)
        ph = (2 * math.pi * fd) * np.outer(t, np.cos(alpha)) + phi[None, :]
        g[:, l] = math.sqrt(powers[l]) * np.exp(1j * ph).sum(axis=1) / math.sqrt(N_SINUSOIDS)
    k = np.arange(N_SC)
    steer = np.exp(-2j * math.pi * SCS_HZ * np.outer(delays, k))   # (N_TAPS, N_SC)
    H = g @ steer                                        # (ntti, N_SC)
    gain = np.abs(H) ** 2                                # avg ~1 (power-normed)
    return mean_snr_db + 10 * np.log10(gain + 1e-12)


# ---- the three policies over one channel realization -----------------
def _run_policy(rng, sinr_db, policy, report_period, req_sinr):
    ntti = sinr_db.shape[0]
    eff_series = np.array([eff_sinr_db(sinr_db[n]) for n in range(ntti)])
    est = eff_series[0]
    offset = 0.0
    nacks = 0
    mcs_seen = set()
    err = 0.0
    for n in range(ntti):
        if policy == "fresh" or n % report_period == 0:
            est = eff_series[n] + rng.normal(0, CQI_NOISE_DB)   # CQI report
        sel = est + (offset if policy == "olla" else 0.0)
        cand = np.where(req_sinr <= sel)[0]
        m = int(cand[-1]) if cand.size else 0
        mcs_seen.add(m)
        p_ack = 1.0 / (1.0 + math.exp(-(rbir(MCS_QM[m], sinr_db[n]) - MCS_R[m]) / RBIR_W))
        nack = rng.random() > p_ack                # HARQ on the AGED channel
        err += abs(eff_series[n] - est)
        if nack:
            nacks += 1
        if policy == "olla":
            offset += (-OLLA_DOWN_DB if nack else OLLA_UP_DB)
    return {"bler": nacks / ntti, "mcs_var": len(mcs_seen), "cqi_err_db": err / ntti}


def run_cell(seed: int, fd: float = FD_HZ, report_period: int = REPORT_PERIOD,
             duration: int = DURATION_TTI) -> dict:
    rng = np.random.default_rng(seed)
    sinr_db = channel_sinr(rng, duration, fd, MEAN_SNR_DB)   # one channel
    req = required_sinr_db()
    naive = _run_policy(rng, sinr_db, "naive", report_period, req)
    olla = _run_policy(rng, sinr_db, "olla", report_period, req)
    fresh = _run_policy(rng, sinr_db, "fresh", report_period, req)
    return {
        "seed": seed, "mode": "nrclean", "fd_hz": fd, "report_period": report_period,
        "naive_bler": round(naive["bler"], 4),
        "olla_bler": round(olla["bler"], 4),
        "fresh_bler": round(fresh["bler"], 4),
        "cqi_err_db": round(naive["cqi_err_db"], 3),
        "n_tti": duration, "mcs_var": naive["mcs_var"],
        "target_bler": TARGET_BLER,
    }


def main():
    global CAP
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "CSIREP-family.json"))
    args = ap.parse_args()
    print("precomputing NR constellation capacities (real QAM + AWGN MC)...", flush=True)
    CAP = capacity_tables()
    cells = []
    for seed in args.seeds:
        c = run_cell(seed)
        cells.append(c)
        print(f"seed {seed}: naive_bler={c['naive_bler']} olla_bler={c['olla_bler']} "
              f"fresh_bler={c['fresh_bler']} cqi_err={c['cqi_err_db']}dB "
              f"mcs_var={c['mcs_var']}", flush=True)
    rec = {
        "family": "F-CSI", "mode": "nrclean",
        "sim_is_code_validation_not_evidence": False,
        "constants": {
            "fd_hz": FD_HZ, "report_period": REPORT_PERIOD, "target_bler": TARGET_BLER,
            "mean_snr_db": MEAN_SNR_DB, "duration_tti": DURATION_TTI,
            "n_sc": N_SC, "scs_hz": SCS_HZ, "rms_delay_spread_s": DS_S, "n_taps": N_TAPS,
            "substrate": ("clean-room 5G NR link level from public 3GPP specs: "
                          "TS 38.214 CQI/MCS tables, Gray M-QAM CM-capacity (MC), "
                          "exponential-PDP TDL + Clarke/Jakes Doppler, MIESM/RBIR "
                          "link-to-system decode; no third-party PHY source"),
        },
        "cells": cells,
    }
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
