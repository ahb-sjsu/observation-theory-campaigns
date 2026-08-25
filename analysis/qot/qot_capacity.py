"""XPROTO-QOT capacity result (OFC Sec. 3.2, steelmanned): capacity recovered vs
TODAY'S uniform-margin practice, with deployed fill drawn from a REAL demand matrix.

The realistic baseline is not "ignore fill" but a UNIFORM system margin: provision
each lightpath at the provisioning-time GSNR minus one blanket margin M, chosen so
the fleet stays safe (false-clear <= target) as the band fills. A uniform M must
cover the worst-filling footprint, so it over-margins lightpaths whose spectral
neighbourhood fills lightly -- stranded capacity. A footprint-aware certificate
provisions each against its own fill footprint (the GSNR it will actually see) and
recovers that capacity at the SAME safety. We report the recovered spectral
efficiency -- the operator's currency.

The deployed fill is NOT assumed uniform: each lightpath's fill is drawn from the
per-link channel-fill distribution of the real SNDlib janos-us-ca demand matrix
(SNDlib-fill.json, built by sndlib_fill.py -- median 10 ch, 90th pctile 35, of 76).
Its deployed GSNR is linearly interpolated between the two GN-model anchors (the
provisioning band CH_REF and a full C-band CH_FULL). Real traffic is heavy-tailed:
most lightpaths fill lightly while a few approach full, so a single uniform margin
sized for the tail strands capacity on the majority -- exactly what a footprint-aware
certificate reclaims. Real traffic makes the number credible, not large.

Substrate: fam_qot GNPy GSNR over CORONET-CONUS reaches; fill from SNDlib. Run in the
qot venv. Emits QOT-capacity.json.
"""
from __future__ import annotations

import json
import math
import os
import warnings

import numpy as np

warnings.filterwarnings("ignore")
import fam_qot as q  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET_FC = 0.01          # safe operating point both policies must meet
N_POS = 8                 # spectral positions per (reach, fill) cell
BAUD_GBD = 32.0           # for the Gb/s-per-channel figure (dual polarisation)
GAP_DB = 1.0              # SNR gap (soft-FEC + implementation) for the flex-rate model
SE_MAX = 6.0              # per-polarisation spectral-efficiency ceiling (64QAM-class)
EST_SIGMA_DB = 0.5        # QoT-estimator RMSE (Rottondi-class); BOTH policies carry it
FILL_JSON = os.path.join(HERE, "SNDlib-fill.json")


def _phi(x):
    """Standard-normal CDF (deterministic; no scipy)."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _se(gsnr_db):
    """Rate-flexible (PCS/flex-transceiver) spectral efficiency at a GSNR, capped.
    Modern coherent transceivers set rate near-continuously, so a uniform over-margin
    costs proportional capacity -- not masked by coarse-format quantization."""
    snr = 10 ** ((gsnr_db - GAP_DB) / 10)
    return float(min(SE_MAX, max(0.0, np.log2(1 + snr))))


def _population(combs, fills):
    """Population over (reach, spectral position, deployed fill). Fill is drawn from
    the real SNDlib per-link distribution; deployed GSNR is linearly interpolated
    between the provisioning anchor (CH_REF) and full C-band (CH_FULL).
    Returns provisioning GSNR gr, deployed GSNR gd (at the real fill), and weight w."""
    pos = np.linspace(0.0, 1.0, N_POS)
    span = float(q.CH_FULL - q.CH_REF)
    gr, gd, w = [], [], []
    for ns in q.SPAN_SET:
        wt = q.SPAN_POOL.count(ns)                     # route frequency
        cr, cf = combs[(q.CH_REF, ns)], combs[(q.CH_FULL, ns)]
        for p in pos:
            gprov = float(cr[round(p * (len(cr) - 1))])
            gfull = float(cf[round(p * (len(cf) - 1))])
            for F in fills:                            # empirical fill distribution
                frac = min(1.0, max(0.0, (F - q.CH_REF) / span))
                gr.append(gprov)
                gd.append(gprov + (gfull - gprov) * frac)
                w.append(wt)
    return np.array(gr), np.array(gd), np.array(w, float)


def _fc_cap(est_gsnr, true_gsnr, w, margin):
    """False-clear (weighted) and delivered flex-rate spectral efficiency at a margin,
    under a realistic QoT-estimator error N(0, EST_SIGMA_DB). The provisioned rate
    requires GSNR (est - margin); the TRUE deployed GSNR is Gaussian around `true`, so
    the per-lightpath false-clear probability is Phi((est - margin - true)/sigma).
    Both policies carry this same estimator uncertainty; the uniform policy carries an
    ADDITIONAL blanket margin for the fill it cannot see."""
    fc = wsum = cap = 0.0
    for e, t, wi in zip(est_gsnr, true_gsnr, w):
        y = e - margin
        wsum += wi
        fc += wi * _phi((y - t) / EST_SIGMA_DB)        # P(true deployed GSNR < y)
        cap += wi * _se(y)                             # provisioned spectral efficiency
    return fc / wsum, cap / wsum


def _min_margin(est, true, w, mgrid):
    for M in mgrid:
        fc, _ = _fc_cap(est, true, w, M)
        if fc <= TARGET_FC:
            return M
    return mgrid[-1]


def main():
    fj = json.load(open(FILL_JSON))
    fills = fj["fill_levels"]
    print(f"deployed fill from {fj['source']}: {len(fills)} links, "
          f"pctiles {fj['fill_pctiles']} of {fj['max_fill']} ch", flush=True)
    print("precomputing GSNR (ref + full) over CORONET reaches...", flush=True)
    combs = {}
    for ns in q.SPAN_SET:
        combs[(q.CH_REF, ns)] = q._gsnr_comb(q.CH_REF, ns)
        combs[(q.CH_FULL, ns)] = q._gsnr_comb(q.CH_FULL, ns)
    gr, gd, w = _population(combs, fills)
    print(f"population: {len(gr)} lightpath cells (reach x position x real-fill)", flush=True)
    mgrid = np.round(np.arange(0.0, 8.01, 0.25), 2)

    # uniform-margin practice: provision at provisioning-time GSNR (gr) minus one
    # blanket margin sized for fleet safety across the real deployed-fill distribution.
    m_uni = _min_margin(gr, gd, w, mgrid)
    fc_uni, cap_uni = _fc_cap(gr, gd, w, m_uni)
    # footprint-aware: provision at each lightpath's own deployed-fill footprint (gd).
    m_aware = _min_margin(gd, gd, w, mgrid)
    fc_aware, cap_aware = _fc_cap(gd, gd, w, m_aware)

    recovered = cap_aware - cap_uni
    pct = 100.0 * recovered / cap_uni if cap_uni else 0.0
    gbps = recovered * BAUD_GBD * 2                    # dual-pol Gb/s per channel
    print(f"uniform margin: M={m_uni} dB, FC={fc_uni:.4f}, capacity={cap_uni:.3f} b/sym", flush=True)
    print(f"footprint-aware: M={m_aware} dB, FC={fc_aware:.4f}, capacity={cap_aware:.3f} b/sym",
          flush=True)
    print(f"RECOVERED: {recovered:.3f} b/sym (+{pct:.1f}%), ~{gbps:.0f} Gb/s per channel, "
          f"at matched safety (FC<= {TARGET_FC})", flush=True)
    rec = {"family": "F-QOT-capacity", "mode": "gnpy-coronet",
           "fill_source": fj["source"], "fill_pctiles": fj["fill_pctiles"],
           "target_fc": TARGET_FC,
           "uniform_margin_db": float(m_uni), "uniform_capacity_bpersym": round(cap_uni, 3),
           "uniform_fc": round(fc_uni, 4), "aware_margin_db": float(m_aware),
           "aware_capacity_bpersym": round(cap_aware, 3), "aware_fc": round(fc_aware, 4),
           "recovered_bpersym": round(recovered, 3), "recovered_pct": round(pct, 1),
           "recovered_gbps_per_channel": round(gbps, 1)}
    json.dump(rec, open(os.path.join(HERE, "QOT-capacity.json"), "w"), indent=1)
    print("wrote QOT-capacity.json", flush=True)


if __name__ == "__main__":
    main()
