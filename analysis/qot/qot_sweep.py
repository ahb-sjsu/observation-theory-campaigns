"""XPROTO-QOT fill-sweep (OFC Sec. 3.2): the QoT refresh floor.

A certificate provisioned at light fill ages as the band fills. Sweeping the
deployed channel count from provisioning (6) to full (76), we measure how the naive
false-clear rate rises with the fill INCREMENT, and read off the refresh floor: the
largest number of added channels a certificate tolerates before its false-clear rate
crosses a target -- i.e. re-certify before the band grows by that much. The floor is
consumer-relative: longer reaches tolerate less fill (they sit nearer thresholds).

Substrate: fam_qot's GNPy GN-model GSNR over CORONET-CONUS reaches. Run in the qot
venv (numpy<2). Emits QOT-sweep.json.
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np

warnings.filterwarnings("ignore")
import fam_qot as q  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FILL = [6, 10, 16, 24, 32, 44, 56, 68, 76]     # deployed channel counts (provisioning=6)
PROV = 6
TARGET_FC = 0.05
N_POS = 40


def _fc_at(combs, fill, reaches, weights):
    """Weighted false-clear of the provisioning-time certificate at a deployed fill."""
    pos = np.linspace(0.0, 1.0, N_POS)
    fails = tot = 0.0
    for ns, w in zip(reaches, weights):
        g_prov = combs[(PROV, ns)]; g_dep = combs[(fill, ns)]
        for p in pos:
            fmt = q._select(float(g_prov[round(p * (len(g_prov) - 1))]))   # provisioned format
            if fmt < 0:
                continue
            true = float(g_dep[round(p * (len(g_dep) - 1))])
            fails += w * (q.REQ[fmt] > true); tot += w
    return fails / tot if tot else 0.0


def _floor(fc_curve):
    """Largest added-channel count with FC <= target (linear interp on the crossing)."""
    dn = np.array([f - PROV for f in FILL], float)
    fc = np.array(fc_curve, float)
    below = np.where(fc <= TARGET_FC)[0]
    if not below.size:
        return 0.0
    last = below[-1]
    if last == len(fc) - 1 or fc[last + 1] <= TARGET_FC:
        return float(dn[last])
    # interpolate between last (<=target) and last+1 (>target)
    x0, x1, y0, y1 = dn[last], dn[last + 1], fc[last], fc[last + 1]
    return float(x0 + (TARGET_FC - y0) * (x1 - x0) / (y1 - y0))


def main():
    reaches = q.SPAN_SET
    weights = [q.SPAN_POOL.count(ns) for ns in reaches]        # route frequency
    print(f"precomputing GSNR over {len(reaches)} reaches x {len(FILL)} fill levels...", flush=True)
    combs = {}
    for ns in reaches:
        for nch in set(FILL + [PROV]):
            combs[(nch, ns)] = q._gsnr_comb(nch, ns)
    fc_curve = [round(_fc_at(combs, f, reaches, weights), 4) for f in FILL]
    floor = round(_floor(fc_curve), 1)
    # per-reach floor (consumer-relativity of the refresh floor)
    per_reach = {}
    for ns in reaches:
        c = [_fc_at(combs, f, [ns], [1.0]) for f in FILL]
        per_reach[ns] = round(_floor(c), 1)
    # linear fit of FC vs added-channels over the rising region (report slope + R^2)
    dn = np.array([f - PROV for f in FILL], float)
    fc = np.array(fc_curve, float)
    A = np.vstack([dn, np.ones_like(dn)]).T
    (slope, icpt), *_ = np.linalg.lstsq(A, fc, rcond=None)
    pred = A @ [slope, icpt]
    ss_res = float(np.sum((fc - pred) ** 2)); ss_tot = float(np.sum((fc - fc.mean()) ** 2))
    r2 = 1 - ss_res / ss_tot if ss_tot else 0.0

    print("FC vs deployed fill:", dict(zip(FILL, fc_curve)), flush=True)
    print(f"refresh floor @FC<= {TARGET_FC}: ~{floor} added channels (pooled)", flush=True)
    print(f"per-reach floor (spans->added-ch): "
          f"short={per_reach[min(reaches)]} long={per_reach[max(reaches)]}", flush=True)
    print(f"FC ~ {slope:.4f}*(added channels) + {icpt:.3f}, R^2={r2:.3f}", flush=True)
    rec = {"family": "F-QOT-sweep", "mode": "gnpy-coronet", "fill": FILL,
           "fc_curve": fc_curve, "target_fc": TARGET_FC, "refresh_floor_added_ch": floor,
           "per_reach_floor": {str(k): v for k, v in per_reach.items()},
           "fc_vs_dn_slope": round(float(slope), 5), "fc_vs_dn_r2": round(float(r2), 4)}
    json.dump(rec, open(os.path.join(HERE, "QOT-sweep.json"), "w"), indent=1)
    print("wrote QOT-sweep.json", flush=True)


if __name__ == "__main__":
    main()
