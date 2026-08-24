"""XPROTO-QOT capacity result (OFC Sec. 3.1, steelmanned): capacity recovered vs
TODAY'S uniform-margin practice.

The realistic baseline is not "ignore fill" but a UNIFORM system margin: provision
each lightpath at the provisioning-time GSNR minus one blanket margin M, chosen so
the fleet stays safe (false-clear <= target) as the band fills. A uniform M must
cover the worst-filling footprint, so it over-margins lightpaths whose spectral
neighbourhood fills lightly -- stranded capacity. A footprint-aware certificate
provisions each against its own fill footprint (the GSNR it will actually see) and
recovers that capacity at the SAME safety. We report the recovered spectral
efficiency -- the operator's currency.

Substrate: fam_qot GNPy GSNR over CORONET-CONUS reaches. Run in the qot venv.
Emits QOT-capacity.json.
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np

warnings.filterwarnings("ignore")
import fam_qot as q  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET_FC = 0.01          # safe operating point both policies must meet
N_POS = 40
BAUD_GBD = 32.0           # for the Gb/s-per-channel figure (dual polarisation)
GAP_DB = 1.0              # SNR gap (soft-FEC + implementation) for the flex-rate model
SE_MAX = 6.0              # per-polarisation spectral-efficiency ceiling (64QAM-class)


def _se(gsnr_db):
    """Rate-flexible (PCS/flex-transceiver) spectral efficiency at a GSNR, capped.
    Modern coherent transceivers set rate near-continuously, so a uniform over-margin
    costs proportional capacity -- not masked by coarse-format quantization."""
    snr = 10 ** ((gsnr_db - GAP_DB) / 10)
    return float(min(SE_MAX, max(0.0, np.log2(1 + snr))))


def _population(combs):
    pos = np.linspace(0.0, 1.0, N_POS)
    gr, gf, w = [], [], []
    for ns in q.SPAN_SET:
        wt = q.SPAN_POOL.count(ns)                     # route frequency
        cr, cf = combs[(q.CH_REF, ns)], combs[(q.CH_FULL, ns)]
        for p in pos:
            gr.append(float(cr[round(p * (len(cr) - 1))]))
            gf.append(float(cf[round(p * (len(cf) - 1))]))
            w.append(wt)
    return np.array(gr), np.array(gf), np.array(w, float)


def _fc_cap(est_gsnr, true_gsnr, w, margin):
    """False-clear (weighted) and delivered flex-rate spectral efficiency at a margin.
    The provisioned rate requires GSNR (est - margin); it false-clears (outage) iff
    the true GSNR is below that, else it delivers that rate's SE."""
    fc = wsum = cap = 0.0
    for e, t, wi in zip(est_gsnr, true_gsnr, w):
        y = e - margin
        wsum += wi
        if y > t:
            fc += wi                                   # outage: delivers nothing
        else:
            cap += wi * _se(y)
    return fc / wsum, cap / wsum


def _min_margin(est, true, w, mgrid):
    for M in mgrid:
        fc, _ = _fc_cap(est, true, w, M)
        if fc <= TARGET_FC:
            return M
    return mgrid[-1]


def main():
    print("precomputing GSNR (ref + full) over CORONET reaches...", flush=True)
    combs = {}
    for ns in q.SPAN_SET:
        combs[(q.CH_REF, ns)] = q._gsnr_comb(q.CH_REF, ns)
        combs[(q.CH_FULL, ns)] = q._gsnr_comb(q.CH_FULL, ns)
    gr, gf, w = _population(combs)
    mgrid = np.round(np.arange(0.0, 8.01, 0.25), 2)

    # uniform-margin practice: provision at provisioning-time GSNR (gr) minus one
    # blanket margin sized for fleet safety as the band fills.
    m_uni = _min_margin(gr, gf, w, mgrid)
    fc_uni, cap_uni = _fc_cap(gr, gf, w, m_uni)
    # footprint-aware: provision at each lightpath's own full-fill footprint (gf).
    m_aware = _min_margin(gf, gf, w, mgrid)
    fc_aware, cap_aware = _fc_cap(gf, gf, w, m_aware)

    recovered = cap_aware - cap_uni
    pct = 100.0 * recovered / cap_uni if cap_uni else 0.0
    gbps = recovered * BAUD_GBD * 2                    # dual-pol Gb/s per channel
    print(f"uniform margin: M={m_uni} dB, FC={fc_uni:.4f}, capacity={cap_uni:.3f} b/sym", flush=True)
    print(f"footprint-aware: M={m_aware} dB, FC={fc_aware:.4f}, capacity={cap_aware:.3f} b/sym",
          flush=True)
    print(f"RECOVERED: {recovered:.3f} b/sym (+{pct:.1f}%), ~{gbps:.0f} Gb/s per channel, "
          f"at matched safety (FC<= {TARGET_FC})", flush=True)
    rec = {"family": "F-QOT-capacity", "mode": "gnpy-coronet", "target_fc": TARGET_FC,
           "uniform_margin_db": float(m_uni), "uniform_capacity_bpersym": round(cap_uni, 3),
           "uniform_fc": round(fc_uni, 4), "aware_margin_db": float(m_aware),
           "aware_capacity_bpersym": round(cap_aware, 3), "aware_fc": round(fc_aware, 4),
           "recovered_bpersym": round(recovered, 3), "recovered_pct": round(pct, 1),
           "recovered_gbps_per_channel": round(gbps, 1)}
    json.dump(rec, open(os.path.join(HERE, "QOT-capacity.json"), "w"), indent=1)
    print("wrote QOT-capacity.json", flush=True)


if __name__ == "__main__":
    main()
