"""Fig. 2 for the OFC XPROTO-QOT paper: the ML-QoT reconstruction-vs-consumer
dissociation. Reads per-prediction records from `fam_qotml.py --preds-out`.
(a) MAE (reconstruction) vs false-clear (consumer) for the two objectives -- the
MSE estimator is better on MAE yet worse on false-clear. (b) false-clear vs the
gap from the true GSNR up to the NEXT format threshold -- a small gap means the
prediction needs only a small upward error to clear one format too high; that is
the cliff, and the MSE estimator false-clears there while the quantile objective
mostly does not. (The old panel binned headroom ABOVE the supported threshold,
which inverts the intuition -- corrected 2026-08-26 after review.) Samples whose
true GSNR clears the top format have no next threshold and cannot false-clear;
they are excluded (count printed). Marker shape, not colour, distinguishes
objectives.

    python plot_fig2.py QOTML-preds.json ../../paper/ofc-qot/ml_cliff.pdf
"""
import json
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
mpl.rcParams.update({"font.size": 11, "axes.titlesize": 11, "legend.fontsize": 10})
import matplotlib.pyplot as plt  # noqa: E402


def main(preds_json="QOTML-preds.json", out_pdf="ml_cliff.pdf"):
    r = json.load(open(preds_json))["records"]
    true = np.array([x["true"] for x in r], float)
    pm = np.array([x["pred_mse"] for x in r], float)
    pa = np.array([x["pred_aware"] for x in r], float)
    hr = np.array([x["headroom"] for x in r], float)
    mf = np.array([x["mse_fail"] for x in r], bool)
    af = np.array([x["aware_fail"] for x in r], bool)
    mae_m, mae_a = np.mean(np.abs(pm - true)), np.mean(np.abs(pa - true))
    fc_m, fc_a = mf.mean(), af.mean()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.9))

    # (a) reconstruction (MAE) vs consumer (false-clear): the dissociation
    ax1.scatter([mae_m], [fc_m], marker="s", s=70, color="0.25", label="average-error")
    ax1.scatter([mae_a], [fc_a], marker="^", s=80, color="0.6", label="quantile-aware")
    ax1.annotate("MSE", (mae_m, fc_m), textcoords="offset points", xytext=(6, 4), fontsize=8)
    ax1.annotate("aware", (mae_a, fc_a), textcoords="offset points", xytext=(6, 4), fontsize=8)
    ax1.set_xlabel("MAE (dB) — reconstruction"); ax1.set_ylabel("false-clear — consumer")
    ax1.set_title("(a) dissociation"); ax1.legend(frameon=False, fontsize=10, loc="upper center")
    ax1.margins(0.3)

    # (b) false-clear vs gap up to the NEXT format threshold: the FEC cliff
    REQ = np.array([6.5, 9.0, 12.5, 16.0, 19.0])
    nxt = np.searchsorted(REQ, true, side="right")
    has = nxt < len(REQ)
    gap = np.where(has, REQ[np.clip(nxt, 0, len(REQ) - 1)] - true, np.inf)
    print(f"excluded (true GSNR clears the top format, no next threshold): "
          f"{int((~has).sum())} of {len(r)}")
    edges = [0, 1, 2, 3, 100]
    ctrs = ["0-1", "1-2", "2-3", "3+"]
    sel = [(gap >= a) & (gap < b) & has for a, b in zip(edges[:-1], edges[1:])]
    fm = [mf[s].mean() if s.any() else 0 for s in sel]
    fa = [af[s].mean() if s.any() else 0 for s in sel]
    xs = np.arange(len(ctrs))
    ax2.plot(xs, fm, marker="s", color="0.25", label="average-error")
    ax2.plot(xs, fa, marker="^", color="0.6", label="quantile-aware")
    ax2.set_xticks(xs); ax2.set_xticklabels(ctrs)
    ax2.set_xlabel("gap below next format threshold (dB)")
    ax2.set_ylabel("false-clear rate")
    ax2.set_title("(b) the FEC cliff"); ax2.legend(frameon=False, fontsize=10)

    fig.tight_layout()
    fig.savefig(out_pdf)
    print(f"MAE mse={mae_m:.3f} aware={mae_a:.3f} | FC mse={fc_m:.3f} aware={fc_a:.3f} "
          f"n={len(r)} -> {out_pdf}")


if __name__ == "__main__":
    main(*sys.argv[1:])
