"""WCNC Fig. 4: the same aging failure in four more NR adaptation certificates.

Reads the SEALED graded records XPROTO-BEAM (FR2 analog beam index) and
XPROTO-PHY (PMI precoder, RI rank, TA uplink timing advance), three graded
seeds each. Three policies per certificate: naive holds the periodic report,
witnessed re-reports on K=2 consecutive failures (BFR for the beam), fresh
re-reports every slot. Linear y so the 0.10 target line reads directly and a
zero stays a zero. Hatch and greyscale, not colour alone.
"""
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ANA = os.path.join(HERE, "..", "..", "..", "analysis")
DEF_BEAM = os.path.join(ANA, "beam", "XPROTO-BEAM-graded.json")
DEF_PHY = os.path.join(ANA, "phy", "XPROTO-PHY-graded.json")
plt.rcParams.update({"font.size": 8.5, "font.family": "serif", "axes.grid": True,
                     "grid.alpha": 0.3, "savefig.dpi": 300, "savefig.bbox": "tight"})


def _mm(vals):
    """mean and (mean-min, max-mean) whiskers across the sealed seeds."""
    v = np.array(vals, float)
    m = v.mean()
    return m, m - v.min(), v.max() - m


def _collect(beam_path, phy_path):
    """Return [(label, naive, witnessed, fresh)] with each entry a (mean, lo, hi)."""
    beam = json.load(open(beam_path))
    phy = json.load(open(phy_path))
    out = []

    bc = beam["cells"]
    out.append(("beam\n(FR2)",
                _mm([c["naive_bler"] for c in bc]),
                _mm([c["bfr_bler"] for c in bc]),
                _mm([c["fresh_bler"] for c in bc])))

    names = {"pmi": "PMI\n(precoder)", "ri": "RI\n(rank)", "ta": "TA\n(uplink)"}
    for key in ("pmi", "ri", "ta"):
        cs = [c for c in phy["cells"] if c["cell"] == key]
        out.append((names[key],
                    _mm([c["naive_fc"] for c in cs]),
                    _mm([c["witnessed_fc"] for c in cs]),
                    _mm([c["fresh_fc"] for c in cs])))
    return out, bc[0]["target_bler"]


def main(out=os.path.join(HERE, "family_sweep.pdf"), beam=DEF_BEAM, phy=DEF_PHY):
    rows, target = _collect(beam, phy)

    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    x = np.arange(len(rows))
    w = 0.26
    styles = [("0.3", "xx", "naive (periodic, held)"),
              ("0.55", "//", "witnessed (re-report on 2 failures)"),
              ("0.85", "", "fresh (re-report every slot)")]

    for i, (colour, hatch, label) in enumerate(styles):
        vals = [r[i + 1][0] for r in rows]
        err = np.array([[r[i + 1][1] for r in rows], [r[i + 1][2] for r in rows]])
        ax.bar(x + (i - 1) * w, vals, w, yerr=err, capsize=2.5, label=label,
               color=colour, hatch=hatch, edgecolor="k", linewidth=0.7)

    lt = ax.axhline(target, ls="--", color="0.15", lw=1.1,
                    label=f"target {target:g}")
    ax.set_xticks(x)
    ax.set_xticklabels([r[0] for r in rows])
    ax.set_ylabel("failure rate against own witness")
    ax.set_ylim(0, 0.48)
    for j, r in enumerate(rows):
        if r[3][0] == 0.0:
            ax.text(j + w, 0.012, "0", fontsize=7, ha="center", color="0.1")
    h, la = ax.get_legend_handles_labels()
    ax.legend(h, la, fontsize=6.3, loc="upper left", framealpha=0.92, handlelength=1.6)
    fig.tight_layout()
    fig.savefig(out)
    fig.savefig(os.path.splitext(out)[0] + ".png")
    for r in rows:
        print(f"{r[0][:4]:5s} naive {r[1][0]:.4f} | witnessed {r[2][0]:.4f} | "
              f"fresh {r[3][0]:.4f}", flush=True)
    print(f"-> {out}", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
