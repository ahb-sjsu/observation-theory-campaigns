"""XPROTO-QOT family (F-QOT): consumer-relative QoT-certificate vacuity in
elastic optical networks, on the GNPy physical layer.

Before a lightpath is provisioned an operator computes a QoT (GSNR) estimate and
picks the highest modulation format whose required GSNR it clears -- a CERTIFICATE.
That estimate is made under the *reference* channel loading (the band as
provisioned). As neighbouring channels are later added the nonlinear interference
grows and the real GSNR drops: the certificate **false-clears** -- the provisioned
modulation now fails its FEC threshold. Operators hide this with margin (stranded
capacity). The false-clear is **consumer-relative**: whether a given lightpath
crosses its threshold depends on its FOOTPRINT (spectral position + reach), so a
blanket margin is adequate for one lightpath and catastrophic for another.

  * consumer = a lightpath (spectral position, number of spans / reach).
  * certificate = GSNR estimated under REFERENCE loading -> a modulation format.
  * witness = the true GSNR under ACTUAL (full) loading (the deployed pre-FEC BER).
  * naive: estimate under reference loading; aware: estimate under actual loading.

Substrate: **GNPy** (oopt-gnpy) GN-model NLI over an SSMF+EDFA line system + a
textbook ASE model. Emits QOTREP-family.json. Run: python3 fam_qot.py.
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np
from gnpy.core.parameters import SimParams
from gnpy.core.elements import Fiber
from gnpy.core.info import create_input_spectral_information
from gnpy.core.utils import db2lin

SimParams.set_params({"raman_params": {"flag": False},
                      "nli_params": {"method": "gn_model_analytic",
                                     "dispersion_tolerance": 1,
                                     "phase_shift_tolerance": 0.1,
                                     "computed_channels": None}})
H = 6.62607015e-34
HERE = os.path.dirname(os.path.abspath(__file__))

# ---- sealed line-system + cell constants -----------------------------
CH_FULL = 76               # fully-loaded C-band comb (50 GHz)
CH_REF = 6                 # reference/provisioned loading (band starts sparse, fills over time)
MAX_ROUTE_KM = 2500       # transparent (unregenerated) reach cap
POWER_DBM = 2.0            # near-optimal launch power


def _coronet_reaches():
    """Reach set = span counts of the CORONET-CONUS reference topology's transparent
    city-pair routes (route length / 80 km). Each consumer is thus a REAL route."""
    import itertools
    import gnpy
    import networkx as nx
    topo = os.path.join(os.path.dirname(gnpy.__file__), "example-data",
                        "CORONET_CONUS_Topology.json")
    c = json.load(open(topo))
    length = {e["uid"]: e["params"]["length"] for e in c["elements"] if e["type"] == "Fiber"}
    g = nx.DiGraph()
    for k in c["connections"]:
        g.add_edge(k["from_node"], k["to_node"], weight=length.get(k["from_node"], 0.0))
    trx = [e["uid"] for e in c["elements"] if e["type"] == "Transceiver"]
    pool = []
    for a, b in itertools.combinations(trx, 2):
        try:
            d = nx.shortest_path_length(g, a, b, weight="weight")
        except Exception:
            continue
        ns = round(d / 80.0)
        if d <= MAX_ROUTE_KM and ns >= 2:
            pool.append(int(ns))
    return sorted(pool)


SPAN_POOL = _coronet_reaches()             # real CORONET route reaches (with multiplicity)
SPAN_SET = sorted(set(SPAN_POOL))          # unique reaches (for GSNR precompute)
NF_DB = 6.0
SPAN_KM = 80
K_PATHS = 60               # lightpaths per seed
MARGIN_DB = 1.0            # design margin the certificate applies
MON_NOISE_DB = 0.3        # GSNR monitoring/estimation uncertainty (1 sigma)
# required GSNR (dB) per modulation format @32 GBd, ~20% SD-FEC (declared)
MODS = [("QPSK", 6.5, 2), ("8QAM", 9.0, 3), ("16QAM", 12.5, 4),
        ("32QAM", 16.0, 5), ("64QAM", 19.0, 6)]
REQ = np.array([m[1] for m in MODS])
BPS = np.array([m[2] for m in MODS])


def _gsnr_comb(nch, spans):
    f_min = 191.35e12; spacing = 50e9
    f_max = f_min + (nch - 1) * spacing + 1e9
    si = create_input_spectral_information(f_min=f_min, f_max=f_max, roll_off=0.15,
                                           baud_rate=32e9, spacing=spacing, tx_osnr=40,
                                           tx_power=db2lin(POWER_DBM) * 1e-3)
    for _ in range(spans):
        fiber = Fiber(uid="f", type_variety="SSMF",
                      params={"length": SPAN_KM, "length_units": "km", "loss_coef": 0.2,
                              "dispersion": 1.67e-5, "effective_area": 8.3e-11,
                              "pmd_coef": 1.265e-15, "con_in": 0, "con_out": 0, "att_in": 0})
        fiber.ref_pch_in_dbm = POWER_DBM
        si = fiber(si)
        si.apply_gain_db(SPAN_KM * 0.2)
        g = 10 ** (SPAN_KM * 0.2 / 10); nf = 10 ** (NF_DB / 10)
        si.add_ase(H * si.frequency * (nf * g - 1) * si.baud_rate)
    return np.asarray(si.gsnr_db, float)


def _select(gsnr_est):
    """Highest modulation whose required GSNR fits the estimate minus margin."""
    ok = np.where(REQ <= gsnr_est - MARGIN_DB)[0]
    return int(ok[-1]) if ok.size else -1


def run_cell(seed, combs):
    rng = np.random.default_rng(seed)
    naive_fc = aware_fc = 0
    penalties = []; nfc_by_path = []; bps_deliv = []
    for _ in range(K_PATHS):
        ns = int(rng.choice(SPAN_POOL))
        p = rng.random()                                   # spectral position 0..1
        g_full = combs[(CH_FULL, ns)]; g_ref = combs[(CH_REF, ns)]
        gsnr_full = float(g_full[round(p * (len(g_full) - 1))])   # witness (true, actual loading)
        gsnr_ref = float(g_ref[round(p * (len(g_ref) - 1))])      # certificate view (ref loading)
        penalties.append(gsnr_ref - gsnr_full)
        naive_est = gsnr_ref + rng.normal(0, MON_NOISE_DB)     # blind to future loading
        aware_est = gsnr_full + rng.normal(0, MON_NOISE_DB)    # footprint-aware
        mn, ma = _select(naive_est), _select(aware_est)
        naive_fail = mn >= 0 and REQ[mn] > gsnr_full           # picked format fails FEC
        aware_fail = ma >= 0 and REQ[ma] > gsnr_full
        naive_fc += naive_fail; aware_fc += aware_fail
        nfc_by_path.append(int(naive_fail))
        bps_deliv.append(int(BPS[ma]) if (ma >= 0 and not aware_fail) else 0)
    n = K_PATHS
    return {
        "seed": int(seed), "mode": "gnpy-coronet",
        "naive_fc": round(naive_fc / n, 4), "aware_fc": round(aware_fc / n, 4),
        "mean_loading_penalty_db": round(float(np.mean(penalties)), 4),
        "fc_spread": round(float(np.std(nfc_by_path)), 4),   # >0 => footprint-relative
        "n_fc": int(naive_fc), "mean_bits_per_symbol_aware": round(float(np.mean(bps_deliv)), 3),
        "n_paths": n,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "QOTREP-family.json"))
    args = ap.parse_args()
    print("propagating GNPy line systems (ref + full loading, per reach)...", flush=True)
    combs = {}
    for ns in SPAN_SET:
        combs[(CH_FULL, ns)] = _gsnr_comb(CH_FULL, ns)
        combs[(CH_REF, ns)] = _gsnr_comb(CH_REF, ns)
    cells = [run_cell(s, combs) for s in args.seeds]
    for c in cells:
        print(f"seed {c['seed']}: naive_fc={c['naive_fc']} aware_fc={c['aware_fc']} | "
              f"loading_penalty={c['mean_loading_penalty_db']}dB fc_spread={c['fc_spread']} "
              f"| bps_aware={c['mean_bits_per_symbol_aware']}", flush=True)
    rec = {"family": "F-QOT", "mode": "gnpy-coronet",
           "sim_is_code_validation_not_evidence": False,
           "constants": {"ch_full": CH_FULL, "ch_ref": CH_REF, "span_set": SPAN_SET,
                         "power_dbm": POWER_DBM, "nf_db": NF_DB, "margin_db": MARGIN_DB,
                         "mon_noise_db": MON_NOISE_DB, "mods": [m[0] for m in MODS],
                         "req_gsnr_db": REQ.tolist(),
                         "substrate": "GNPy gn_model_analytic NLI over CORONET-CONUS transparent city-pair routes (<=2500 km, reach=len/80 spans) on SSMF+EDFA; "
                                      "system; witness = true GSNR under full loading"},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
