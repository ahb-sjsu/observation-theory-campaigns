"""FL1 calibration: one row per measured random regular graph (routers N, degree d, seed, two-hop multiplicity m,
link-change LSP saving), and the bar the sealed test uses, computed by a fixed rule.

    fl1_calibrate.py OUT.csv OUT.json MEASUREMENTS::TOPOLOGY_DIR::SETUP [...]

Each MEASUREMENTS file is matched to its topology files by sha256 under TOPOLOGY_DIR; a record whose file is not
found is counted and left out, and so is every graph with a run that did not converge (its windows compare against
a network still flooding its bring-up). The rule for the bar (percentage points of saving):
  sigma_seed = the largest sample standard deviation of the saving among graphs of the same N and d;
  loso_max   = the largest absolute error of the multiplicity law (isotonic in m) on one network size when fitted on
               the other sizes (leave one size out);
  bar        = max(3 * sigma_seed, loso_max)."""
import csv
import json
import os
import sys
from statistics import mean, stdev

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fl_common as F  # noqa: E402


def main(out_csv, out_json, specs):
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
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    # instrument check I0: our multiplicity equals the builder's where the file records one
    i0 = [abs(r["m"] - r["m_builder"]) for r in rows if r["m_builder"] is not None]
    groups = {}
    for r in rows:
        groups.setdefault((r["routers"], r["degree"]), []).append(r["saving_pct"])
    sds = {f"{k[0]}x{k[1]}": stdev(v) for k, v in groups.items() if len(v) > 1}
    sigma_seed = max(sds.values()) if sds else None
    loso = {}
    for n in sorted({r["routers"] for r in rows}):
        rest = [r for r in rows if r["routers"] != n]
        if not rest:
            continue
        knots = F.isotonic([r["m"] for r in rest], [r["saving_pct"] for r in rest])
        loso[n] = [abs(F.interpolate(knots, r["m"]) - r["saving_pct"]) for r in rows if r["routers"] == n]
    loso_max = max(e for v in loso.values() for e in v) if loso else None
    bar = max(3 * sigma_seed, loso_max) if sigma_seed is not None and loso_max is not None else None
    summary = {"rows": len(rows), "records_without_topology_file": missing,
               "left_out_not_converged": unconverged,
               "I0_max_abs_m_vs_builder": max(i0) if i0 else None, "I0_checked": len(i0),
               "sigma_seed_pct": sigma_seed, "sigma_seed_by_cell": sds,
               "loso_max_abs_error_pct": loso_max,
               "loso_mean_abs_error_pct_by_size": {str(k): mean(v) for k, v in loso.items()},
               "bar_pct": bar,
               "m_law_knots": F.isotonic([r["m"] for r in rows], [r["saving_pct"] for r in rows]),
               "d_law_knots": F.isotonic([r["degree"] for r in rows if r["routers"] == 64],
                                         [r["saving_pct"] for r in rows if r["routers"] == 64])}
    with open(out_json, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1)
        fh.write("\n")
    print(json.dumps({k: v for k, v in summary.items() if not k.endswith("knots")}, indent=1))
    for r in rows:
        print(f"  N={r['routers']:>5} d={r['degree']:>3} seed={r['seed']} m={r['m']:.4f} saving={r['saving_pct']:.1f}% "
              f"({r['setup']}, {r['measurements']})")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
