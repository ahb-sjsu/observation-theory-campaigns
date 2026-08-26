"""OFC review round 3: the freshness curve at add resolution, and its dependence
on the sync baseline N0. Deterministic (no seed), same substrate and certificate
as qot_sweep.py; extends it two ways, both reviewer-requested:

  1. FINE GRID at the crossing. The original sweep sampled deployed fill at
     {6,10,16,24,...}, so "crosses 0.05 at 8.1 adds" was an interpolation across
     a 6-channel gap. Here the fill steps by ONE channel through the crossing
     region, so the paper can say "k safe additions; the (k+1)-th exceeds 5%"
     as an observed integer, no interpolation.
  2. N0 SENSITIVITY. The original budget is conditional on syncing at the
     provisioning fill N0=6. Here the sweep repeats with the twin synced at
     N0 in {6, 20, 40, 60}: Delta-N*(N0) = the largest number of adds with
     FC <= 5%. If it is stable, the eight-add budget generalises; if not, the
     honest result is a baseline-dependent freshness surface.

Run locally (GNPy installed in the system python). Emits QOT-sweep2.json.
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np

warnings.filterwarnings("ignore")
import fam_qot as q  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET_FC = 0.05
N_POS = 40
N0S = [6, 20, 40, 60]
CH_FULL = 76
FINE_SPAN = 16              # fill N0+1 .. N0+16 by single adds
COARSE = [20, 26, 34, 46, 58, 70]   # additional Delta-N tail points where room allows


def fills_for(n0):
    fine = list(range(n0, min(n0 + FINE_SPAN, CH_FULL) + 1))
    tail = [n0 + d for d in COARSE if n0 + d <= CH_FULL]
    return sorted(set(fine + tail + [CH_FULL]))


def fc_at(combs, n0, fill, reaches, weights):
    """Weighted false-clear of the N0-synced certificate at a deployed fill."""
    pos = np.linspace(0.0, 1.0, N_POS)
    fails = tot = 0.0
    for ns, w in zip(reaches, weights):
        g_syn = combs[(n0, ns)]; g_dep = combs[(fill, ns)]
        for p in pos:
            fmt = q._select(float(g_syn[round(p * (len(g_syn) - 1))]))
            if fmt < 0:
                continue
            true = float(g_dep[round(p * (len(g_dep) - 1))])
            fails += w * (q.REQ[fmt] > true); tot += w
    return fails / tot if tot else 0.0


def main():
    reaches = q.SPAN_SET
    weights = [q.SPAN_POOL.count(ns) for ns in reaches]
    need = sorted({f for n0 in N0S for f in fills_for(n0)} | set(N0S))
    print(f"precomputing GSNR: {len(reaches)} reaches x {len(need)} fill levels...",
          flush=True)
    combs = {}
    for i, nch in enumerate(need):
        for ns in reaches:
            combs[(nch, ns)] = q._gsnr_comb(nch, ns)
        print(f"  fill {nch} done ({i + 1}/{len(need)})", flush=True)

    out = {"family": "F-QOT-sweep2", "mode": "gnpy-coronet", "target_fc": TARGET_FC,
           "n_pos": N_POS, "baselines": {}}
    for n0 in N0S:
        fills = fills_for(n0)
        curve = {f - n0: round(fc_at(combs, n0, f, reaches, weights), 4)
                 for f in fills}
        # last safe add on the single-add grid, and the first add that exceeds
        fine_dns = [d for d in sorted(curve) if 0 <= d <= FINE_SPAN]
        safe = [d for d in fine_dns if curve[d] <= TARGET_FC]
        exceed = [d for d in fine_dns if curve[d] > TARGET_FC]
        dn_star = max(safe) if safe else 0
        first_exceed = min(exceed) if exceed else None
        zero_through = max([d for d in fine_dns if curve[d] == 0.0], default=0)
        out["baselines"][str(n0)] = {
            "fc_curve": {str(k): v for k, v in sorted(curve.items())},
            "dn_star": dn_star, "first_exceed": first_exceed,
            "zero_through": zero_through}
        print(f"N0={n0}: safe adds={dn_star}, first exceed={first_exceed}, "
              f"zero through {zero_through}; "
              f"curve[1..10]={[curve.get(d) for d in range(1, 11)]}", flush=True)
    json.dump(out, open(os.path.join(HERE, "QOT-sweep2.json"), "w"), indent=1)
    print("wrote QOT-sweep2.json", flush=True)


if __name__ == "__main__":
    main()
