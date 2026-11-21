"""FL1 grading: measured savings against the predictions written before the labs ran.

    fl1_grade.py PREDICTIONS.json [PREDICTIONS.json ...] -- MEASUREMENTS [...]

A cell is one predicted topology file with a measured saving. It is graded if every run of it converged and it has
link windows with flood reduction off and on; otherwise it is VOID. A graded cell is discriminating if its m-law and
d-law predictions differ by at least twice the bar. Verdict:
  PASS  - at least two discriminating cells are graded, every one has |measured - m_law| <= bar, and the m-law's mean
          absolute error over them is below the d-law's;
  FAIL  - at least two discriminating cells are graded and either condition fails;
  VOID  - fewer than two discriminating cells are graded."""
import json
import os
import sys
from statistics import mean

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fl_common as F  # noqa: E402


def main(args):
    split = args.index("--")
    preds, bars = {}, set()
    for p in args[:split]:
        with open(p, encoding="utf-8") as fh:
            d = json.load(fh)
        bars.add(d["calibration_bar_pct"])
        preds.update({x["sha256"]: x for x in d["predictions"]})
    if len(bars) != 1:
        sys.exit(f"predictions disagree on the bar: {bars}")
    bar = bars.pop()
    measured = {}
    for m in args[split + 1:]:
        measured.update(F.by_topology(F.read(m)))
    cells = []
    for sha, x in sorted(preds.items(), key=lambda kv: (kv[1]["routers"], kv[1]["degree"])):
        recs = measured.get(sha, [])
        saving, n_off, n_on = F.lsp_saving(recs) if recs else (None, 0, 0)
        ok = bool(recs) and all(r.get("converged") for r in recs) and saving is not None
        disc = abs(x["m_law_pct"] - x["d_law_pct"]) >= 2 * bar
        obs = None if saving is None else 100 * saving
        cells.append({**x, "measured_pct": obs, "graded": ok, "discriminating": disc,
                      "err_m_law": None if obs is None else obs - x["m_law_pct"],
                      "err_d_law": None if obs is None else obs - x["d_law_pct"],
                      "err_model": None if obs is None else obs - x["model_lockstep_pct"],
                      "runs": len(recs), "windows_off": n_off, "windows_on": n_on})
    graded = [c for c in cells if c["graded"] and c["discriminating"]]
    if len(graded) < 2:
        verdict = "VOID"
    else:
        within = all(abs(c["err_m_law"]) <= bar for c in graded)
        better = mean(abs(c["err_m_law"]) for c in graded) < mean(abs(c["err_d_law"]) for c in graded)
        verdict = "PASS" if within and better else "FAIL"
    for c in cells:
        tag = "graded" if c["graded"] else "VOID"
        tag += ", discriminating" if c["discriminating"] else ""
        meas = "-" if c["measured_pct"] is None else f"{c['measured_pct']:.1f}%"
        print(f"  N={c['routers']} d={c['degree']} m={c['m']:.4f}: measured {meas}; m-law {c['m_law_pct']:.1f}%, "
              f"d-law {c['d_law_pct']:.1f}%, model {c['model_lockstep_pct']:.1f}% ({tag}; {c['runs']} runs)")
    print(f"bar {bar:.2f} points; discriminating cells graded: {len(graded)}")
    print("FL1_VERDICT", verdict)
    out = os.path.splitext(args[0])[0] + "-graded.json"
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"bar_pct": bar, "verdict": verdict, "cells": cells}, fh, indent=1)
        fh.write("\n")


if __name__ == "__main__":
    main(sys.argv[1:])
