"""FL2: does the quiet-window reference age within a run?

    fl2_baseline_age.py LABEL::MEASUREMENTS [...]

`measure` subtracts one quiet window, taken once after bring-up, from every event window of the run. The handler
that sends hellos (`send_hello_cb`, in `--profile` runs) does the same work in every window whatever the event, so
its net-of-quiet CPU, e_j = |net send_hello_cb| in the j-th link-down window of a run, measures how far the host's
background has moved since the reference was taken. If the reference ages, e grows with j.

Per run with at least two link-down windows: D = e_last - e_first. Per dataset (and pooled): runs, runs with D > 0
and D < 0 (ties dropped), the one-sided sign-test p for D > 0, mean e by window index, and mean e_last / mean
e_first. The same for link-up windows, as a secondary (a link coming up changes the hello work at its two ends)."""
import os
import sys
from math import comb
from statistics import mean

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fl_common as F  # noqa: E402

HANDLER = "send_hello_cb"


def runs(records, phase):
    out = []
    for r in records:
        if r.get("timing") or not r.get("profile"):
            continue
        e = [abs((p.get("net_of_quiet") or {}).get("event_cpu_ms", {}).get(HANDLER, 0.0))
             for p in r["phases"] if p["phase"] == phase and (p.get("net_of_quiet") or {}).get("event_cpu_ms")]
        if len(e) >= 2:
            out.append(e)
    return out


def sign_p(pos, neg):
    n = pos + neg
    return sum(comb(n, k) for k in range(pos, n + 1)) / 2 ** n if n else None


def summary(label, es):
    d = [e[-1] - e[0] for e in es]
    pos, neg = sum(x > 0 for x in d), sum(x < 0 for x in d)
    k = max(len(e) for e in es) if es else 0
    by_j = [mean(e[j] for e in es if len(e) > j) for j in range(k)]
    first, last = mean(e[0] for e in es), mean(e[-1] for e in es)
    p = sign_p(pos, neg)
    return (f"  {label:<22} runs {len(es):>3}  D>0 {pos:>3}  D<0 {neg:>3}  sign-test p {p:.3g}  "
            f"mean e by window {', '.join(f'{x:.0f}' for x in by_j)} ms  last/first {last / first:.2f}"
            if es and p is not None and first else f"  {label:<22} runs {len(es)}")


def main(specs):
    pooled = {"link-down": [], "link-up": []}
    for phase in ("link-down", "link-up"):
        print(f"{phase} windows: e_j = |net {HANDLER}|, ms summed over the routers")
        for spec in specs:
            label, path = spec.split("::")
            es = runs(F.read(path), phase)
            pooled[phase] += es
            print(summary(label, es))
        print(summary("POOLED", pooled[phase]))


if __name__ == "__main__":
    main(sys.argv[1:])
