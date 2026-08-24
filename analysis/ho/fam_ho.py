"""XPROTO-HO family (F-HO): the handover / mobility cell — the geo-fleet
cellular twin.

Certificate = the UE's RSRP measurement report ("cell X is best / adequate").
Consumer = the served link. Under mobility the report ages: the UE moves past
the cell-edge crossover but the stale periodic report keeps it on the old
serving cell, whose RSRP has dropped and whose ex-neighbor now interferes —
the serving SINR collapses and the link fails (HARQ NACK / radio-link
failure). Witness = the post-handover outcome (HARQ on the serving cell).
The deployed witnessed correction is fast re-selection on radio-link-
monitoring failure (RLM): consecutive serving failures trigger an immediate
handover to the current best cell.

This is the exact shape of the geo-fleet cell (which replica/cell to route to
when the freshness certificate is stale) at the RAN mobility layer.

Three policies over the SAME trajectory + channel:
  naive : hand over only on the stale periodic RSRP report (trust the cert).
  rlm   : periodic + immediate re-select on serving failure (K NACKs) --
          the HARQ/RLM-witnessed correction (credited prior art).
  fresh : re-select the best cell every slot (no aging) -- the control.

Serving-link BLER from the real Sionna 5G NR LDPC curves. Run on Atlas GPU 1
(imports the cached curves). Emits HOREP-family.json.
"""
import os
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
import argparse
import json
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "csi"))
import csi_sionna as cs   # noqa: E402  (real Sionna 5G NR LDPC BLER curves)

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- sealed cell constants (bars reference these; do not tune) -------
CELL_X = np.array([0.0, 500.0])        # two cells, 500 m apart
TXP_DBM = 46.0
PL0, PL_N = 30.0, 3.5                   # pathloss: PL0 + 10*N*log10(d)
SHADOW_STD_DB = 6.0
SHADOW_DCORR_M = 20.0                   # shadowing decorrelation distance
FAST_RHO = 0.5                          # fast-fade AR correlation per slot
FAST_STD_DB = 3.0                       # fast-fade depth (PHY only; L3 filters it)
NOISE_DBM = -95.0
V_MPS = 30.0                            # UE speed (high mobility -> aging regime)
SLOT_S = 1e-3
DURATION_SLOT = 6000
REPORT_PERIOD = 300                     # slots between RSRP reports (L3 filter + TTT)
N_SWEEPS = 5                            # edge crossings (mobility events)
HYST_DB = 2.0                           # handover hysteresis
RLM_NACK_THRESH = 3                     # consecutive NACKs -> RLM failure
MCS_SEL_SINR_DB = 2.0                   # fixed MCS ~ this SINR (cell-edge operating pt)
TARGET_BLER = 0.10


def _pl(d):
    return PL0 + 10 * PL_N * np.log10(np.maximum(d, 1.0))


def channel(seed):
    """Per-slot L3-filtered RSRP (dBm) for handover decisions (pathloss +
    correlated shadowing, NO fast fade) and a mild PHY fast-fade term for the
    link SINR. Returns (rsrp_slow, fast), each (n,2)."""
    rng = np.random.default_rng(seed)
    n = DURATION_SLOT
    # UE oscillates deep cell0 <-> deep cell1, crossing the edge quickly (so
    # the CORRECT cell is comfortably decodable except brief transits, while a
    # stale report strands the UE deep in the wrong cell's territory).
    tri = np.abs(((np.arange(n) / (n / (2 * N_SWEEPS))) % 2) - 1)   # 0..1..0
    x = 80.0 + 340.0 * tri                     # sweep x in [80, 420]
    dx = np.abs(np.diff(x, prepend=x[0])).mean()
    rho_sh = np.exp(-dx / SHADOW_DCORR_M)
    rsrp_slow = np.zeros((n, 2))
    fast = np.zeros((n, 2))
    for c in range(2):
        pl = _pl(np.abs(x - CELL_X[c]))
        s, f = rng.normal(0, SHADOW_STD_DB), 0.0
        for i in range(n):
            s = rho_sh * s + np.sqrt(1 - rho_sh ** 2) * rng.normal(0, SHADOW_STD_DB)
            f = FAST_RHO * f + np.sqrt(1 - FAST_RHO ** 2) * rng.normal(0, FAST_STD_DB)
            rsrp_slow[i, c] = TXP_DBM - pl[i] + s      # L3 metric (HO decisions)
            fast[i, c] = f                              # PHY only (link SINR)
    return rsrp_slow, fast


def serving_sinr_db(rsrp_slow_row, fast_row, s, offset):
    lin = 10 ** ((rsrp_slow_row + fast_row + offset) / 10.0)
    inter = lin.sum() - lin[s] + 10 ** (NOISE_DBM / 10.0)
    return 10 * np.log10(lin[s] / inter)


def _calibrate_offset(rsrp_slow, fast):
    """Shift RSRP so the best-cell SINR medians ~GOOD_SINR_DB (operating point;
    the interference-limited cell edge is unaffected -- that outage is real)."""
    best = np.argmax(rsrp_slow, axis=1)
    sinr = np.array([serving_sinr_db(rsrp_slow[i], fast[i], best[i], 0.0)
                     for i in range(len(rsrp_slow))])
    return GOOD_SINR_DB - np.median(sinr)


def run_policy(rng, rsrp_slow, fast, offset, policy, curves, mcs):
    n = len(rsrp_slow)
    serving = int(np.argmax(rsrp_slow[0]))
    nack = consec = n_ho = lag = 0
    last_report = rsrp_slow[0].copy()
    for i in range(n):
        if policy == "fresh" or i % REPORT_PERIOD == 0:
            last_report = rsrp_slow[i].copy()          # (aged) L3 measurement report
        target = serving
        if policy == "fresh":
            target = int(np.argmax(rsrp_slow[i]))
        else:
            best_rep = int(np.argmax(last_report))
            if best_rep != serving and last_report[best_rep] > last_report[serving] + HYST_DB:
                target = best_rep
            if policy == "rlm" and consec >= RLM_NACK_THRESH:
                last_report = rsrp_slow[i].copy()       # RLM failure -> re-measure
                target = int(np.argmax(last_report))    # ...then re-select on fresh CSI
                consec = 0
        if target != serving:
            serving = target
            n_ho += 1
            consec = 0
        s = serving_sinr_db(rsrp_slow[i], fast[i], serving, offset)
        if serving != int(np.argmax(rsrp_slow[i])):
            lag += 1
        is_nack = rng.random() < cs.bler_at(curves, mcs, s)
        if is_nack:
            nack += 1
            consec += 1
        else:
            consec = 0
    return {"bler": nack / n, "n_ho": n_ho, "ho_lag_frac": lag / n}


def run_cell(seed, curves, req):
    rsrp_slow, fast = channel(seed)
    offset = 0.0                               # interference-limited; no shift needed
    mcs = int(np.where(req <= MCS_SEL_SINR_DB)[0][-1])
    naive = run_policy(np.random.default_rng(seed * 10 + 1), rsrp_slow, fast, offset, "naive", curves, mcs)
    rlm = run_policy(np.random.default_rng(seed * 10 + 2), rsrp_slow, fast, offset, "rlm", curves, mcs)
    fresh = run_policy(np.random.default_rng(seed * 10 + 3), rsrp_slow, fast, offset, "fresh", curves, mcs)
    return {
        "seed": int(seed), "mode": "nrsionna_ho", "v_mps": V_MPS,
        "report_period": REPORT_PERIOD, "mcs": mcs,
        "naive_bler": float(round(naive["bler"], 4)),
        "rlm_bler": float(round(rlm["bler"], 4)),
        "fresh_bler": float(round(fresh["bler"], 4)),
        "ho_lag_frac": float(round(naive["ho_lag_frac"], 4)),
        "n_slot": DURATION_SLOT, "n_ho": int(naive["n_ho"] + rlm["n_ho"] + fresh["n_ho"]),
        "target_bler": TARGET_BLER,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "HOREP-family.json"))
    args = ap.parse_args()
    print("loading real 5G NR LDPC BLER curves (Sionna)...", flush=True)
    curves = cs.measure_bler_curves()
    req = cs.required_snr(curves)
    cells = []
    for seed in args.seeds:
        c = run_cell(seed, curves, req)
        cells.append(c)
        print(f"seed {seed}: naive_bler={c['naive_bler']} rlm_bler={c['rlm_bler']} "
              f"fresh_bler={c['fresh_bler']} ho_lag={c['ho_lag_frac']} "
              f"n_ho={c['n_ho']} mcs={c['mcs']}", flush=True)
    rec = {"family": "F-HO", "mode": "nrsionna_ho",
           "sim_is_code_validation_not_evidence": False,
           "constants": {"v_mps": V_MPS, "report_period": REPORT_PERIOD,
                         "cell_sep_m": float(CELL_X[1]), "shadow_std_db": SHADOW_STD_DB,
                         "target_bler": TARGET_BLER, "rlm_nack_thresh": RLM_NACK_THRESH,
                         "substrate": ("2-cell mobility geometry (pathloss + correlated "
                                       "shadowing + fast fade) + real Sionna 5G NR LDPC "
                                       "BLER curves for the serving link; RSRP-report aging")},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
