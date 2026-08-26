"""XPROTO-QOT-FLIP family (F-QOT-FLIP): the two-consumer verdict inversion (the
Flip) in optical QoT. The house signature experiment, in the twin frame: one
digital-twin GSNR view, two FEC consumers, and two margin policies matched on the
aggregate that the consumers rank in OPPOSITE orders.

Consumers. Services come in two FEC classes reading the same twin estimate:
  SD : soft-decision FEC, required GSNR = base table - FEC_DELTA_DB
  HD : hard-decision FEC, required GSNR = base table + FEC_DELTA_DB
Half the fleet is SD, half HD (interleaved over footprints).

Policies. Two margin shapings with the SAME fleet-mean margin (matched aggregate):
  A "protect-low"  : margin concentrated where provisioning GSNR sits near the SD
                     class's format boundaries (low-GSNR half of the fleet range)
  B "protect-high" : the same total margin concentrated near the HD boundaries
                     (high-GSNR half)
Each is a smooth bump in provisioning-GSNR; both are normalized per seed so the
fleet-mean margin is exactly MARGIN_MEAN_DB. The aggregate cannot tell them apart
by construction. The claim: FC_SD(A) < FC_SD(B) and FC_HD(B) < FC_HD(A). Same
pair, opposite verdicts. State-MSE-style aggregates cannot order the pair.

Substrate = fam_qot's GNPy GN-model GSNR over CORONET-CONUS reaches (provisioning
= 6-ch band, deployed = full 76-ch C-band), 0.3 dB monitoring noise. Run in the
qot venv (numpy<2). Emits QOTFLIPREP-family.json.
"""
from __future__ import annotations

import argparse
import json
import os
import warnings

import numpy as np

warnings.filterwarnings("ignore")
import fam_qot as q  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FEC_DELTA_DB = 1.5          # SD reads base-1.5 dB, HD reads base+1.5 dB
MARGIN_MEAN_DB = 1.0        # matched fleet-mean margin for BOTH policies
BUMP_WIDTH_DB = 2.5         # width of the margin bump in provisioning-GSNR
K_SERVICES = 120            # services per seed (footprint = position x reach)
NOISE_DB = 0.3              # monitoring noise on the provisioning estimate


def _fleet(seed):
    """Sample K services over (reach, position); return provisioning + deployed GSNR."""
    rng = np.random.default_rng(seed)
    combs_ref = {ns: q._gsnr_comb(q.CH_REF, ns) for ns in q.SPAN_SET}
    combs_ful = {ns: q._gsnr_comb(q.CH_FULL, ns) for ns in q.SPAN_SET}
    prov, dep = [], []
    for k in range(K_SERVICES):
        ns = q.SPAN_POOL[rng.integers(0, len(q.SPAN_POOL))]
        p = rng.uniform(0.0, 1.0)
        cr, cf = combs_ref[ns], combs_ful[ns]
        prov.append(float(cr[round(p * (len(cr) - 1))]))
        dep.append(float(cf[round(p * (len(cf) - 1))]))
    return np.array(prov), np.array(dep)


def _margins(prov, kind):
    """Bump-shaped margin over provisioning GSNR, normalized to MARGIN_MEAN_DB."""
    lo, hi = np.percentile(prov, 25), np.percentile(prov, 75)
    centre = lo if kind == "protect_low" else hi
    raw = np.exp(-0.5 * ((prov - centre) / BUMP_WIDTH_DB) ** 2)
    return raw * (MARGIN_MEAN_DB / raw.mean())


def _fc(prov_est, dep, margin, delta_db):
    """Per-service false-clear under one FEC class: select the highest format whose
    (class-shifted) required GSNR + margin clears the estimate; it false-clears if
    the deployed GSNR is below that requirement."""
    req = np.array(q.REQ, float) + delta_db
    fails = 0
    for e, d, m in zip(prov_est, dep, margin):
        ok = np.where(req + m <= e)[0]
        f = int(ok[-1]) if ok.size else 0
        if d < req[f]:
            fails += 1
    return fails / len(prov_est)


def _fleet_footprint(seed):
    """Two disjoint sub-fleets reading ORTHOGONAL footprint axes (the flip needs
    read misalignment; the FEC construction below is the coupling null).
      R-fleet: long reach, band-edge positions (penalty dominated by span count)
      P-fleet: short reach, band-centre positions (penalty dominated by NLI position)
    Returns (prov, dep, reach_norm, centrality, r_mask)."""
    rng = np.random.default_rng(seed)
    combs_ref = {ns: q._gsnr_comb(q.CH_REF, ns) for ns in q.SPAN_SET}
    combs_ful = {ns: q._gsnr_comb(q.CH_FULL, ns) for ns in q.SPAN_SET}
    spans = sorted(q.SPAN_SET)
    long_spans = spans[len(spans) // 2:]
    short_spans = spans[:len(spans) // 2]
    prov, dep, rn, ct, rmask = [], [], [], [], []
    smax = max(spans)
    for k in range(K_SERVICES):
        if k % 2 == 0:                                  # R-fleet
            ns = long_spans[rng.integers(0, len(long_spans))]
            p = rng.choice([rng.uniform(0.0, 0.15), rng.uniform(0.85, 1.0)])
            rmask.append(True)
        else:                                           # P-fleet
            ns = short_spans[rng.integers(0, len(short_spans))]
            p = rng.uniform(0.35, 0.65)
            rmask.append(False)
        cr, cf = combs_ref[ns], combs_ful[ns]
        prov.append(float(cr[round(p * (len(cr) - 1))]))
        dep.append(float(cf[round(p * (len(cf) - 1))]))
        rn.append(ns / smax)
        ct.append(1.0 - 2.0 * abs(p - 0.5))             # 1 at band centre, 0 at edge
    return (np.array(prov), np.array(dep), np.array(rn), np.array(ct),
            np.array(rmask))


def run_cell(seed):
    rng = np.random.default_rng(seed + 1000)
    out = {"seed": int(seed), "mode": "gnpy-coronet", "n_services": K_SERVICES,
           "fec_delta_db": FEC_DELTA_DB, "margin_mean_db": MARGIN_MEAN_DB}

    # ---- construction 1: two FEC classes (the COUPLING NULL; flip predicted absent:
    # both consumers read the same GSNR projection, thresholds differ by a shift) ----
    prov, dep = _fleet(seed)
    est = prov + rng.normal(0, NOISE_DB, len(prov))
    sd_mask = np.arange(len(prov)) % 2 == 0
    for kind, tag in (("protect_low", "A"), ("protect_high", "B")):
        m = _margins(prov, kind)
        out[f"fec_fc_sd_{tag}"] = round(_fc(est[sd_mask], dep[sd_mask], m[sd_mask], -FEC_DELTA_DB), 4)
        out[f"fec_fc_hd_{tag}"] = round(_fc(est[~sd_mask], dep[~sd_mask], m[~sd_mask], +FEC_DELTA_DB), 4)
    out["fec_flip"] = bool(out["fec_fc_sd_A"] < out["fec_fc_sd_B"]
                           and out["fec_fc_hd_B"] < out["fec_fc_hd_A"])

    # ---- construction 2: two FOOTPRINT classes with orthogonal read axes (the flip
    # construction). Policy A allocates margin by reach, policy B by band-centrality;
    # both normalized to the SAME fleet-mean margin. ----
    prov, dep, rn, ct, rmask = _fleet_footprint(seed)
    est = prov + rng.normal(0, NOISE_DB, len(prov))
    m_a = rn * (MARGIN_MEAN_DB / rn.mean())             # reach-weighted margin
    m_b = (ct + 0.05) * (MARGIN_MEAN_DB / (ct + 0.05).mean())  # centrality-weighted
    for m, tag in ((m_a, "A"), (m_b, "B")):
        out[f"fp_mean_margin_{tag}"] = round(float(m.mean()), 4)
        out[f"fp_fc_R_{tag}"] = round(_fc(est[rmask], dep[rmask], m[rmask], 0.0), 4)
        out[f"fp_fc_P_{tag}"] = round(_fc(est[~rmask], dep[~rmask], m[~rmask], 0.0), 4)
    out[f"fp_fc_fleet_A"] = round(0.5 * (out["fp_fc_R_A"] + out["fp_fc_P_A"]), 4)
    out[f"fp_fc_fleet_B"] = round(0.5 * (out["fp_fc_R_B"] + out["fp_fc_P_B"]), 4)
    out["fp_flip"] = bool(out["fp_fc_R_A"] < out["fp_fc_R_B"]
                          and out["fp_fc_P_B"] < out["fp_fc_P_A"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "QOTFLIPREP-family.json"))
    args = ap.parse_args()
    print("propagating GNPy line systems (ref + full loading, per reach)...", flush=True)
    cells = []
    for s in args.seeds:
        c = run_cell(s)
        cells.append(c)
        print(f"seed {s} FEC(null): SD A={c['fec_fc_sd_A']} B={c['fec_fc_sd_B']} "
              f"HD A={c['fec_fc_hd_A']} B={c['fec_fc_hd_B']} flip={c['fec_flip']}", flush=True)
        print(f"seed {s} FOOTPRINT: R A={c['fp_fc_R_A']} B={c['fp_fc_R_B']} | "
              f"P A={c['fp_fc_P_A']} B={c['fp_fc_P_B']} | "
              f"fleet A={c['fp_fc_fleet_A']} B={c['fp_fc_fleet_B']} | FLIP={c['fp_flip']}",
              flush=True)
    rec = {"family": "F-QOT-FLIP", "mode": "gnpy-coronet",
           "constants": {"fec_delta_db": FEC_DELTA_DB, "margin_mean_db": MARGIN_MEAN_DB,
                         "bump_width_db": BUMP_WIDTH_DB, "k_services": K_SERVICES,
                         "substrate": "fam_qot GNPy GN-model over CORONET-CONUS"},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
