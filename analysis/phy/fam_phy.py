"""XPROTO-PHY family (F-PHY): the remaining PHY adaptation certificates --
PMI (spatial precoder), RI (rank), TA (uplink timing advance) -- as three
aging-certificate cells sharing the vacuity grammar.

Each is a certificate that ages under its own coherence process; graded against
the served-link outcome (HARQ, or UL decode for TA). naive holds the periodic
report; witnessed re-reports on a failure (the deployed loop: PMI re-selection,
RI down-rank, the TA command loop); fresh re-reports every slot.

  pmi : reported precoder (top eigen-direction) misaligns as the channel rotates
        -> beamforming-gain loss -> NACK. (MIMO sibling of XPROTO-BEAM.)
  ri  : reported rank ages; a stale-high rank transmits a layer the current
        channel can no longer carry -> that layer fails.
  ta  : the UE's round-trip delay drifts with radial motion; a stale timing
        advance leaves a residual that, past the cyclic prefix, causes ISI ->
        UL decode failure. (The first UPLINK cell.)

  mode "model": self-contained parametric NR waterfall (validation, not evidence,
                as fam_csi's sim is not evidence). The sealed rung uses the real
                Sionna 5G NR LDPC curves (mode "nrsionna"); phy_check refuses to
                seal on "model".

    python3 fam_phy.py --model
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np
from scipy.special import erfc, erfcinv

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- parametric NR-ish link (model rung) -----------------------------
W_CURVE = 1.0
MCS_SNR50 = np.array([-4.0 + 2.0 * i for i in range(13)])   # per-MCS 50%-BLER SINR
SQRT2 = np.sqrt(2.0)
REQ10 = MCS_SNR50 + SQRT2 * W_CURVE * erfcinv(2 * 0.10)      # 10% points


def bler(m, snr):
    return 0.5 * erfc((snr - MCS_SNR50[m]) / (SQRT2 * W_CURVE))


def sel(est):
    c = np.where(REQ10 <= est)[0]
    return int(c[-1]) if c.size else 0


# ---- sealed constants -------------------------------------------------
DURATION = 6000
OPERATING_SINR = 14.0
MCS_MARGIN = 2.0
FIXED_MCS = int(np.where(REQ10 <= OPERATING_SINR - MCS_MARGIN)[0][-1])
TARGET = 0.10
BFR_NACK = 2                       # consecutive NACKs -> witnessed re-report
SLOT_S = 1e-3
# per-mode report cadence (slots) + aging driver
PMI_REPORT, OMEGA_PMI = 20, 1200.0            # precoder angular drift (deg/s)
PMI_LOSS_DB_PER_DEG = 0.3                      # beamforming-gain loss vs misalignment
RI_REPORT, RANK_FLIP_HZ = 20, 270.0           # rank-change rate (per s)
TA_REPORT, TA_DRIFT_US_PER_S = 200, 20.0      # TA cadence (200 ms) + drift (us/s)
CP_US = 4.7                                    # normal cyclic prefix (us)


def _report(policy, i, consec, period):
    return (policy == "fresh" or i % period == 0
            or (policy == "bfr" and consec >= BFR_NACK))


def run_pmi(seed, policy):
    rng = np.random.default_rng(seed)
    a = rng.uniform(-30, 30); v = OMEGA_PMI * (1 if rng.random() < 0.5 else -1)
    held = a; nack = consec = nre = 0; loss = 0.0
    for i in range(DURATION):
        a += v * SLOT_S
        if a > 40: a, v = 40.0, -abs(v)
        if a < -40: a, v = -40.0, abs(v)
        if _report(policy, i, consec, PMI_REPORT):
            held = a + rng.normal(0, 1.0); consec = 0; nre += 1   # re-report precoder
        sinr = OPERATING_SINR - PMI_LOSS_DB_PER_DEG * abs(a - held)   # monotonic loss
        loss += OPERATING_SINR - sinr
        is_nack = rng.random() < bler(FIXED_MCS, sinr)
        nack += is_nack; consec = consec + 1 if is_nack else 0
    return nack / DURATION, loss / DURATION, nre


def run_ri(seed, policy):
    rng = np.random.default_rng(seed)
    p_flip = RANK_FLIP_HZ * SLOT_S
    rank = int(rng.integers(1, 5)); held = rank; nack = consec = nre = 0; mism = 0
    for i in range(DURATION):
        if rng.random() < p_flip:
            rank = int(np.clip(rank + rng.choice([-1, 1]), 1, 4))
        if _report(policy, i, consec, RI_REPORT):
            held = rank; consec = 0; nre += 1                     # re-report rank
        # valid layers are reliable; a stale-high rank transmits a layer the
        # current channel can no longer carry -> that layer collapses.
        if held > rank:
            mism += 1; layer_sinr = OPERATING_SINR - 12.0
        else:
            layer_sinr = OPERATING_SINR                          # supported -> reliable
        is_nack = rng.random() < bler(FIXED_MCS, layer_sinr)
        nack += is_nack; consec = consec + 1 if is_nack else 0
    return nack / DURATION, mism / DURATION, nre


def run_ta(seed, policy):
    rng = np.random.default_rng(seed)
    drift = TA_DRIFT_US_PER_S * (1 if rng.random() < 0.5 else -1)
    delay = rng.uniform(0, CP_US); ta = delay; nack = consec = nre = 0; res = 0.0
    for i in range(DURATION):
        delay += drift * SLOT_S
        if _report(policy, i, consec, TA_REPORT):
            ta = delay + rng.normal(0, 0.1); consec = 0; nre += 1  # TA command
        residual = abs(delay - ta)
        res += residual / CP_US
        # ISI penalty grows with residual; past the CP the block is destroyed
        sinr = OPERATING_SINR - 9.0 * (residual / CP_US) - (30.0 if residual > CP_US else 0.0)
        is_nack = rng.random() < bler(FIXED_MCS, sinr)
        nack += is_nack; consec = consec + 1 if is_nack else 0
    return nack / DURATION, res / DURATION, nre


RUNNERS = {"pmi": run_pmi, "ri": run_ri, "ta": run_ta}
AGING_NAME = {"pmi": "mean_gain_loss_db", "ri": "rank_mismatch_frac",
              "ta": "mean_residual_over_cp"}


def run_cell(mode, seed):
    naive, aging, _ = RUNNERS[mode](seed, "naive")
    bfr, _, nre = RUNNERS[mode](seed, "bfr")
    fresh, _, _ = RUNNERS[mode](seed, "fresh")
    return {"cell": mode, "seed": int(seed), "mode": "model",
            "naive_fc": round(naive, 4), "witnessed_fc": round(bfr, 4),
            "fresh_fc": round(fresh, 4), "aging": round(aging, 4),
            "aging_name": AGING_NAME[mode], "n_tti": DURATION, "n_requotes": nre,
            "target": TARGET}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", action="store_true")
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "PHYREP-family.json"))
    args = ap.parse_args()
    cells = []
    for mode in ("pmi", "ri", "ta"):
        for s in args.seeds:
            c = run_cell(mode, s); cells.append(c)
            print(f"{mode} seed {s}: naive_fc={c['naive_fc']} witnessed_fc={c['witnessed_fc']} "
                  f"fresh_fc={c['fresh_fc']} {c['aging_name']}={c['aging']}", flush=True)
    rec = {"family": "F-PHY", "mode": "model",
           "sim_is_code_validation_not_evidence": True,
           "constants": {"pmi_report": PMI_REPORT, "ri_report": RI_REPORT,
                         "ta_report": TA_REPORT, "operating_sinr": OPERATING_SINR,
                         "target": TARGET, "omega_pmi": OMEGA_PMI,
                         "rank_flip_hz": RANK_FLIP_HZ, "ta_drift_us_per_s": TA_DRIFT_US_PER_S,
                         "cp_us": CP_US,
                         "substrate": "parametric NR waterfall (model validation); "
                                      "sealed rung = real Sionna LDPC curves"},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
