"""FL3 (exploratory): among the neighbors of a late router that decided with the topology from before the failure,
how many did the lateness depend on?

    fl3_stale_relays.py results/mechanism/analysis-*-on.txt

Input: the analysis files of topology-builders results/mechanism (tools/model/analyze_events.py). For every
router-LSP pair that arrived more than 500 ms late they list each neighbor of the late router, the topology
snapshots that reproduce that neighbor's logged flooding decision for the LSP, and whether the decision on the fresh
topology (the failure removed) sends the LSP to the late router. Here a neighbor is
  stale         if only snapshots holding the failed element reproduce its decision ('old' and/or 'frozen' and/or
                'rebuilt', and not 'fresh');
  consequential if stale and the fresh decision sends to the late router (its staleness withheld the LSP);
  fresh         if 'fresh' reproduces it.
Printed per lab and event, and pooled: late pairs, neighbors, stale, consequential, and the pairs with no
consequential stale neighbor."""
import re
import sys
from collections import defaultdict

HEAD = re.compile(r"^(\S+): (.+?): \d+/\d+ new LSPs")
LATE = re.compile(r"^\s+late: (\S+) got (\S+)'s LSP after (\d+) ms via (\S+), from (\S+)")
NEIGH = re.compile(r"^\s+(\S+): reproduced by (.+?); fresh topology sends to (\S+): (True|False)")


def main(paths):
    tot = defaultdict(int)
    for path in paths:
        event = None
        stats = {}
        pair = None
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                if m := HEAD.match(line):
                    event = f"{m.group(1)} {m.group(2)}"
                    stats[event] = defaultdict(int)
                elif m := LATE.match(line):
                    pair = (m.group(1), m.group(2))
                    stats[event]["late pairs"] += 1
                    stats[event]["_pair_has_conseq"] = 0
                    stats[event]["_open"] = 1
                elif (m := NEIGH.match(line)) and pair:
                    s = stats[event]
                    snaps = {x.strip() for x in m.group(2).split(",")}
                    s["neighbors"] += 1
                    if "fresh" in snaps:
                        s["fresh"] += 1
                    elif snaps & {"old", "frozen", "rebuilt"}:
                        s["stale"] += 1
                        if m.group(4) == "True":
                            s["consequential"] += 1
                            if not s["_pair_has_conseq"]:
                                s["pairs with a consequential stale neighbor"] += 1
                                s["_pair_has_conseq"] = 1
                    else:
                        s["reproduced by none"] += 1
        for event, s in stats.items():
            keys = ["late pairs", "neighbors", "fresh", "stale", "consequential",
                    "pairs with a consequential stale neighbor", "reproduced by none"]
            print(f"{event}: " + ", ".join(f"{k} {s[k]}" for k in keys))
            for k in keys:
                tot[k] += s[k]
    print("POOLED: " + ", ".join(f"{k} {v}" for k, v in tot.items()))
    if tot["stale"]:
        print(f"consequential share of stale neighbors: {tot['consequential'] / tot['stale']:.3f}; "
              f"stale share of neighbors: {tot['stale'] / tot['neighbors']:.3f}; consequential stale neighbors per "
              f"late pair: {tot['consequential'] / tot['late pairs']:.2f}")


if __name__ == "__main__":
    main(sys.argv[1:])
