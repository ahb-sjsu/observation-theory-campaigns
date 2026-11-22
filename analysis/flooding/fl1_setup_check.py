"""FL1 setup checks of PREREG-FL1-002: the records' setup (gate I4) and calibration graphs re-measured in the test
setup (gate I3).

    fl1_setup_check.py CALIBRATION.csv CALIBRATION.json [SHA256 ...] -- MEASUREMENTS [...]

I4: every record in MEASUREMENTS carries the test setup in its lab settings and window: hello interval 3 s, hello
multiplier 10, LSP generation interval 30 s (FRR's defaults), 60 s windows. PASS iff all do.

Each SHA256 names a topology file of the calibration table. Its calibration saving is the mean of the table's
saving_pct over the rows with that sha256; its test-setup saving is the link-change LSP saving (fl_common.lsp_saving)
over the records in MEASUREMENTS written from that file. A graph is graded if it has records, every one converged,
and both variants have link windows. Verdict:
  PASS  - every named graph is graded and |test-setup saving - calibration saving| <= the calibration's bar;
  FAIL  - every named graph is graded and at least one differs by more than the bar;
  VOID  - a named graph is not graded (or not in the table).
With no SHA256 named, only I4 is checked."""
import csv
import json
import os
import sys
from statistics import mean

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fl_common as F  # noqa: E402

TEST_SETUP = {"hello_interval": 3, "hello_multiplier": 10, "lsp_gen_interval": 30}
TEST_WINDOW_S = 60


def setup_ok(r):
    return all(r["settings"].get(k) == v for k, v in TEST_SETUP.items()) and r.get("window_s") == TEST_WINDOW_S


def main(args):
    split = args.index("--")
    table, summary, shas = args[0], args[1], args[2:split]
    with open(table, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    with open(summary, encoding="utf-8") as fh:
        bar = json.load(fh)["bar_pct"]
    measured, records = {}, []
    for m in args[split + 1:]:
        recs = F.read(m)
        records += recs
        measured.update(F.by_topology(recs))
    off_setup = [r for r in records if not setup_ok(r)]
    i4 = "PASS" if records and not off_setup else "FAIL"
    print(f"  {len(records)} records, {len(off_setup)} outside the test setup; FL1_SETUP_I4 {i4}")
    if not shas:
        return i4
    results = []
    for sha in shas:
        cal_rows = [r for r in rows if r["sha256"] == sha]
        recs = measured.get(sha, [])
        saving, n_off, n_on = F.lsp_saving(recs) if recs else (None, 0, 0)
        graded = bool(cal_rows) and bool(recs) and all(r.get("converged") for r in recs) and saving is not None
        cal = mean(float(r["saving_pct"]) for r in cal_rows) if cal_rows else None
        obs = None if saving is None else 100 * saving
        diff = None if not graded else obs - cal
        results.append((sha, cal_rows[0] if cal_rows else None, cal, obs, diff, graded, len(recs), n_off, n_on))
        name = f"N={cal_rows[0]['routers']} d={cal_rows[0]['degree']}" if cal_rows else "not in the table"
        meas = "-" if obs is None else f"{obs:.2f}%"
        cals = "-" if cal is None else f"{cal:.2f}%"
        d = "-" if diff is None else f"{diff:+.2f}"
        print(f"  {sha[:12]} {name}: calibration {cals} ({len(cal_rows)} rows); test setup {meas} "
              f"({len(recs)} runs, {n_off}/{n_on} windows); difference {d} points; "
              f"{'graded' if graded else 'VOID'}")
    if not results or not all(r[5] for r in results):
        verdict = "VOID"
    else:
        verdict = "PASS" if all(abs(r[4]) <= bar for r in results) else "FAIL"
    print(f"bar {bar:.4f} points; FL1_SETUP_I3 {verdict}")
    return verdict


if __name__ == "__main__":
    main(sys.argv[1:])
