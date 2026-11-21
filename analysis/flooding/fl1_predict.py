"""FL1 predictions for new random regular graphs, written before their labs run.

    fl1_predict.py CALIBRATION.json OUT.json TOPOLOGY.json [...]

For each topology file: its two-hop multiplicity m and three predictions of the link-change LSP saving (percent):
  m_law  - the isotonic fit of saving on m over the calibration (the claim under test), linear between knots and
           constant beyond them;
  d_law  - the rival: the isotonic fit of saving on degree over the 64-router calibration graphs;
  model  - topology_builders.flood_model in lockstep, for the three links `measure --links 3 --seed 1` will take
           down in this file (chosen from its sha256), averaged over their down and up changes.
The output's sha256 is printed so a queue log can record it before the first measurement."""
import hashlib
import json
import os
import sys
from statistics import mean

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fl_common as F  # noqa: E402
from topology_builders import clab, measure  # noqa: E402
from topology_builders import flood_model as fm  # noqa: E402


def model_saving(g, sha):
    routers, links = clab.plan(g)
    chosen = measure.pick_links({"source_sha256": sha, "links": links}, 1, 3)
    topo = fm.Topology.from_lab(routers, links)
    sent = {on: mean(fm.flood_link_change(topo, (x["a"], x["b"]), state, on)["sent"]
                     for x in chosen for state in ("down", "up")) for on in (False, True)}
    return 100 * (1 - sent[True] / sent[False]), [f"{x['a']}-{x['b']}" for x in chosen]


def main(calibration, out, paths):
    with open(calibration, encoding="utf-8") as fh:
        cal = json.load(fh)
    preds = []
    for p in paths:
        g, sha = F.load_graph(p), F.sha256(p)
        par = g.graph.get("parameters", {})
        m = F.two_hop_multiplicity(g)
        model, links = model_saving(g, sha)
        preds.append({"topology": os.path.basename(p), "sha256": sha, "routers": g.number_of_nodes(),
                      "degree": par.get("degree"), "seed": par.get("seed"), "m": round(m, 6),
                      "m_law_pct": round(F.interpolate(cal["m_law_knots"], m), 4),
                      "d_law_pct": round(F.interpolate(cal["d_law_knots"], par.get("degree")), 4),
                      "model_lockstep_pct": round(model, 4), "links": links})
    body = json.dumps({"calibration_bar_pct": cal["bar_pct"], "predictions": preds}, indent=1) + "\n"
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(body)
    for x in preds:
        print(f"  {x['topology']}: m={x['m']:.4f} m-law {x['m_law_pct']:.1f}%  d-law {x['d_law_pct']:.1f}%  "
              f"model {x['model_lockstep_pct']:.1f}%")
    print("FL1_PREDICTIONS_SHA256", hashlib.sha256(body.encode()).hexdigest(), out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
