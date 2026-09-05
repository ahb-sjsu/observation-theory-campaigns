#!/usr/bin/env python3
"""Figure: consumer-metric false-clear advantage Delta = fc_raw - fc_true vs
transform locality Lambda = identity-map held-out R^2, across all graded
(cell, layer) units of V1+V2 (V3 appends when graded). Reads committed
records only. Serif, 300dpi, marker shape encodes transform family."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "..", "..")   # analysis/cr-ieip

# Lambda (identity-map held-out R^2) per unit, from v2_graded.json posthoc +
# the V1 post-mortem identity values are not all recomputed; we use the V2
# family (which has both arms) plus V1 A/C paraphrase + bt from records.
# For the figure we read v2_graded.json's posthoc_identity_R2 (D,E,F,G) and the
# per-unit false-clears from each cell result.
gr = json.load(open(os.path.join(D, "v2_graded.json")))
lam = gr["posthoc_identity_R2"]           # {cell:{layer:Lambda}}
CELLS = {"cellD": ("de-bt", [12, 18]), "cellE": ("fr-bt", [14, 21]),
         "cellF": ("pegasus", [12, 18]), "cellG": ("de-bt", [14, 21])}
MARK = {"de-bt": "o", "fr-bt": "s", "pegasus": "^", "es-bt": "D",
        "synonym": "P", "shuffle": "X", "truncate": "v"}

pts = []
for tag, (fam, layers) in CELLS.items():
    res = json.load(open(os.path.join(D, f"cr_ieip_{tag}_result.json")))
    for L in layers:
        lval = lam[tag][str(L)]
        d = res[str(L)]["false_clear"]["raw"] - res[str(L)]["false_clear"]["true"]
        pts.append((lval, d, fam))

# append V3 cells H-L if their results + a lambda file exist
v3lam = os.path.join(D, "v3_gate.json")
if os.path.exists(v3lam):
    vg = json.load(open(v3lam))
    V3 = {"cellH": ("synonym", [12, 18]), "cellI": ("shuffle", [14, 21]),
          "cellJ": ("truncate", [12, 18]), "cellK": ("synonym", [14, 21]),
          "cellL": ("shuffle", [12, 18])}
    for tag, (fam, layers) in V3.items():
        rp = os.path.join(D, f"cr_ieip_{tag}_result.json")
        if not os.path.exists(rp):
            continue
        res = json.load(open(rp))
        for L in layers:
            lval = vg.get(tag, {}).get(str(L), {}).get("gate_R2")
            if lval is None:
                continue
            d = res[str(L)]["false_clear"]["raw"] - res[str(L)]["false_clear"]["true"]
            pts.append((lval, d, fam))

plt.rcParams.update({"font.family": "serif", "font.size": 9})
fig, ax = plt.subplots(figsize=(3.5, 2.9), dpi=300)
seen = set()
for lval, d, fam in pts:
    ax.scatter(lval, d, marker=MARK.get(fam, "o"), s=34,
               facecolor="#1a6b9a" if d >= 0.05 else ("#c0392b" if d <= 0.01 else "#888"),
               edgecolor="black", linewidth=0.4,
               label=fam if fam not in seen else None, zorder=3)
    seen.add(fam)
ax.axhline(0.05, ls="--", lw=0.7, color="#1a6b9a")
ax.axhline(0.0, lw=0.5, color="#bbb")
ax.axvspan(-0.2, 0.2, color="#f0f0f0", zorder=0)
ax.set_xlabel(r"transform locality $\Lambda$ (identity-map held-out $R^2$)")
ax.set_ylabel(r"advantage $\Delta = fc_{\rm raw}-fc_{\rm true}$")
ax.legend(fontsize=6, loc="lower right", frameon=False, ncol=2)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_delta_lambda.pdf"))
fig.savefig(os.path.join(HERE, "fig_delta_lambda.png"))
print(f"wrote fig_delta_lambda.{{pdf,png}} with {len(pts)} units")
