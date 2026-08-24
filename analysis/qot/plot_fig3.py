"""Optional Fig. 3 for the OFC XPROTO-QOT paper (Sec. 3.2, the refresh floor).
Reads QOT-sweep.json; plots naive false-clear vs number of added channels, the
target line, and the refresh floor. Add to the paper only if the 3-page budget
allows a third figure; otherwise Sec. 3.2 reports the numbers inline.

    python plot_fig3.py QOT-sweep.json ../../paper/ofc-qot/refresh_floor.pdf
"""
import json
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def main(sweep_json="QOT-sweep.json", out_pdf="refresh_floor.pdf"):
    d = json.load(open(sweep_json))
    prov = d["fill"][0]
    dn = np.array([f - prov for f in d["fill"]], float)
    fc = np.array(d["fc_curve"], float)
    tgt = d["target_fc"]; floor = d["refresh_floor_added_ch"]

    fig, ax = plt.subplots(figsize=(3.6, 2.9))
    ax.plot(dn, fc, marker="o", color="0.25", label="naive false-clear")
    ax.axhline(tgt, ls="--", color="0.6", lw=1, label=f"target {tgt}")
    ax.axvline(floor, ls=":", color="k", lw=1)
    ax.annotate(f"refresh floor\n$\\approx${floor:.0f} added ch", (floor, tgt),
                textcoords="offset points", xytext=(8, 30), fontsize=8,
                arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.set_xlabel("added channels ($\\Delta N$)"); ax.set_ylabel("false-clear rate")
    ax.set_title("QoT refresh floor (fill sweep)")
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    fig.tight_layout(); fig.savefig(out_pdf)
    print(f"floor={floor} added ch @FC<={tgt}; slope={d['fc_vs_dn_slope']} "
          f"R2={d['fc_vs_dn_r2']} -> {out_pdf}")


if __name__ == "__main__":
    main(*sys.argv[1:])
