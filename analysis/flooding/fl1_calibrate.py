"""FL1 calibration: one row per measured random regular graph (routers N, degree d, seed, two-hop multiplicity m,
link-change LSP saving), and the bar the sealed test uses, computed by a fixed rule from those rows alone.

    fl1_calibrate.py OUT.csv OUT.json MEASUREMENTS::TOPOLOGY_DIR::SETUP [...]
    fl1_calibrate.py --from-csv CALIBRATION.csv OUT.json

The first form extracts the rows (each MEASUREMENTS file is matched to its topology files by sha256 under
TOPOLOGY_DIR; a record whose file is not found is counted and left out, and so is every graph with a run that did
not converge, since its windows compare against a network still flooding its bring-up) and then summarizes them.
The second form summarizes an existing table, so the summary can be recomputed and checked byte for byte.

The rule for the bar (percentage points of saving):
  sigma_seed = the largest sample standard deviation of the saving among graphs of the same N and d;
  loso_max   = the largest absolute error of the multiplicity law (isotonic in m) on one network size when fitted
               on the other sizes (leave one size out), counting only held-out graphs whose m lies inside the range
               of m the fit was made on: the test predicts inside the calibrated range, and an error made by
               extrapolating past it measures the extrapolation, not the transfer across size;
  bar        = max(3 * sigma_seed, loso_max)."""
import csv
import json
import os
import sys
from statistics import mean, stdev

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fl_common as F  # noqa: E402

FIELDS = ["routers", "degree", "seed", "m", "m_builder", "saving_pct", "windows_off", "windows_on", "setup",
          "measurements", "topology", "sha256"]


def extract(specs):
    rows, missing, unconverged = [], 0, []
    for spec in specs:
        meas, topo_dir, setup = spec.split("::")
        index = F.topology_index(topo_dir)
        for sha, recs in sorted(F.by_topology(F.read(meas)).items()):
            t = recs[0]["topology"]
            if t.get("family") != "random-regular":
                continue
            if sha not in index:
                missing += len(recs)
                continue
            if not all(r.get("converged") for r in recs):
                unconverged.append(f"{t['parameters']} in {meas}")
                continue
            g = F.load_graph(index[sha])
            saving, n_off, n_on = F.lsp_saving(recs)
            if saving is None:
                continue
            p = t["parameters"]
            rows.append({"routers": p["routers"], "degree": p["degree"], "seed": p["seed"],
                         "m": round(F.two_hop_multiplicity(g), 6),
                         "m_builder": g.graph.get("two_hop_multiplicity"),
                         "saving_pct": round(100 * saving, 4), "windows_off": n_off, "windows_on": n_on,
                         "setup": setup, "measurements": os.path.basename(os.path.dirname(meas)) or meas,
                         "topology": os.path.basename(index[sha]), "sha256": sha})
    rows.sort(key=lambda r: (r["routers"], r["degree"], r["seed"], r["sha256"]))
    return rows, {"records_without_topology_file": missing, "left_out_not_converged": unconverged}


def read_csv(path):
    with open(path, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        for k in ("routers", "degree", "seed", "windows_off", "windows_on"):
            r[k] = int(r[k])
        for k in ("m", "saving_pct"):
            r[k] = float(r[k])
        r["m_builder"] = float(r["m_builder"]) if r["m_builder"] not in ("", "None") else None
    return rows


def summarize(rows):
    """Everything the test uses, from the rows alone."""
    i0 = [abs(r["m"] - r["m_builder"]) for r in rows if r["m_builder"] is not None]
    groups = {}
    for r in rows:
        groups.setdefault((r["routers"], r["degree"]), []).append(r["saving_pct"])
    sds = {f"{k[0]}x{k[1]}": stdev(v) for k, v in sorted(groups.items()) if len(v) > 1}
    sigma_seed = max(sds.values())
    loso, outside = {}, {}
    for n in sorted({r["routers"] for r in rows}):
        rest = [r for r in rows if r["routers"] != n]
        knots = F.isotonic([r["m"] for r in rest], [r["saving_pct"] for r in rest])
        lo, hi = min(r["m"] for r in rest), max(r["m"] for r in rest)
        held = [r for r in rows if r["routers"] == n]
        loso[n] = [abs(F.interpolate(knots, r["m"]) - r["saving_pct"]) for r in held if lo <= r["m"] <= hi]
        outside[n] = sum(not lo <= r["m"] <= hi for r in held)
    loso_max = max(e for v in loso.values() for e in v)
    return {"rows": len(rows), "m_range": [min(r["m"] for r in rows), max(r["m"] for r in rows)],
            "I0_max_abs_m_vs_builder": max(i0) if i0 else None, "I0_checked": len(i0),
            "sigma_seed_pct": sigma_seed, "sigma_seed_by_cell": sds,
            "loso_max_abs_error_pct": loso_max,
            "loso_mean_abs_error_pct_by_size": {str(k): mean(v) for k, v in loso.items() if v},
            "loso_held_out_outside_fitted_range_by_size": {str(k): v for k, v in outside.items()},
            "bar_pct": max(3 * sigma_seed, loso_max),
            "m_law_knots": F.isotonic([r["m"] for r in rows], [r["saving_pct"] for r in rows]),
            "d_law_knots": F.isotonic([r["degree"] for r in rows if r["routers"] == 64],
                                      [r["saving_pct"] for r in rows if r["routers"] == 64])}


def write_json(path, obj):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True)
        fh.write("\n")


def main(argv):
    if argv[0] == "--from-csv":
        rows = read_csv(argv[1])
        summary = summarize(rows)
        write_json(argv[2], summary)
    else:
        rows, extraction = extract(argv[2:])
        with open(argv[0], "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=FIELDS, lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        summary = summarize(read_csv(argv[0]))
        write_json(argv[1], summary)
        write_json(os.path.splitext(argv[1])[0] + "-extraction.json", extraction)
        print(json.dumps(extraction, indent=1))
    print(json.dumps({k: v for k, v in summary.items() if not k.endswith("knots")}, indent=1, sort_keys=True))
    for r in rows:
        print(f"  N={r['routers']:>5} d={r['degree']:>3} seed={r['seed']} m={r['m']:.4f} saving={r['saving_pct']:.1f}% "
              f"({r['setup']}, {r['measurements']})")


if __name__ == "__main__":
    main(sys.argv[1:])
