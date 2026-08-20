"""LM-2 gate evaluator. Local, deterministic from the committed raw log.
Usage: python lm2_gates.py <log.json> [--out <analysis.json>]

All comparison gates anchor to measured consumer behavior at matched
budgets, evaluated PAIRED on CRN-shared eval states (the same states,
same correct answers, across every arm).

  O1 aligned beats task-blind: pooled relative consumer-loss
     improvement of the aligned arm over the random-subset arm
     (mean over consumers of 1 - L_aligned/L_random).
  O1b per-consumer floor on the same quantity.
  O2 blind capture: (L_random - L_aligned)/(L_random - L_oracle),
     pooled (guarded: denominator must be positive).
  O3 anti-control: anti not better than random, pooled
     (1 - L_anti/L_random <= 0 + eps handled by bar sign).
  O4 headroom sanity (diagnostic, ungated unless sealed otherwise):
     all-coarse >= arms >= all-fine bracket ordering, pooled.
  O5 instrument: repeat |dloss| max; parse rate; fail rate.
  Probe-cost ledger reported (probe_req/probe_tok vs eval).
GATES None until frozen from >= 2 powered draws (the LM1-003 lesson).
"""
import json
import sys

# Frozen 2026-08-20 from the ACROSS-DRAW calibration of two
# independent powered pilot draws (pilotA 20261110 / pilotB 20261112):
# pooled O1 0.2914/0.2858 (per-consumer min 0.123); capture
# 0.872/0.993; pooled anti -0.279/-0.309 (one per-cell +0.099 where
# the random subset also missed the read components - why pooled is
# the load-bearing form); repeat max 0.124/0.054. The all-fine
# "bracket" diagnostic is VIOLATED in the aligned arm's favor
# (quantizing unread components actively helps - the spurious-channel
# finding); reported ungated.
GATES = {
    "O1_aligned_vs_random_pooled_min": 0.15,
    "O1b_per_consumer_floor": 0.05,
    "O2_capture_pooled_min": 0.60,
    "O3_anti_vs_random_pooled_max": 0.0,   # anti improvement must be <= this
    "O5_repeat_dloss_max": 0.50,
    "O6_parse_rate_min": 0.98,
    "O7_fail_rate_max": 0.01,
}

ARMS = ["aligned", "oracle", "anti", "random", "allcoarse", "allfine"]


def main():
    log_path = sys.argv[1]
    out_path = (sys.argv[sys.argv.index("--out") + 1]
                if "--out" in sys.argv else log_path.replace("_log", "_analysis"))
    d = json.load(open(log_path, encoding="utf-8"))

    parse_ok = parse_all = 0
    mean_loss = {}
    eval_rows = {}
    rep_pairs = []
    base_by_key = {}
    for r in d["rows"]:
        parse_all += 1
        if r["lp_yes"] is not None or r["lp_no"] is not None:
            parse_ok += 1
        if r["leg"] == "eval":
            eval_rows.setdefault((r["consumer"], r["arm"]), []).append(r)
            base_by_key[(r["consumer"], r["arm"], r["state"])] = r["loss"]
    for r in d["rows"]:
        if r["leg"] == "repeat":
            b = base_by_key.get((r["consumer"], r["arm"], r["state"]))
            if b is not None:
                rep_pairs.append(abs(r["loss"] - b))

    metrics = {}
    for cid in d["consumers"]:
        m = {}
        for arm in ARMS:
            rows = eval_rows.get((cid, arm), [])
            m[arm] = sum(x["loss"] for x in rows) / len(rows) if rows else None
        impr_aligned = 1.0 - m["aligned"] / m["random"]
        impr_anti = 1.0 - m["anti"] / m["random"]
        gap_oracle = m["random"] - m["oracle"]
        capture = ((m["random"] - m["aligned"]) / gap_oracle) if gap_oracle > 0 else None
        metrics[cid] = {
            "mean_loss_by_arm": {k: (round(v, 5) if v is not None else None) for k, v in m.items()},
            "impr_aligned_vs_random": round(impr_aligned, 4),
            "impr_anti_vs_random": round(impr_anti, 4),
            "capture_of_oracle": (round(capture, 4) if capture is not None else None),
            "bracket_ok": bool(m["allcoarse"] >= min(m["aligned"], m["oracle"], m["random"]) and
                               m["allfine"] <= min(m["aligned"], m["oracle"], m["random"])),
            "allocations": d["allocations"][cid]["arms"],
            "diag_Phat": [round(x, 5) for x in d["allocations"][cid]["diag_Phat"]],
        }

    pooled_o1 = sum(metrics[c]["impr_aligned_vs_random"] for c in metrics) / len(metrics)
    pooled_o3 = sum(metrics[c]["impr_anti_vs_random"] for c in metrics) / len(metrics)
    captures = [metrics[c]["capture_of_oracle"] for c in metrics
                if metrics[c]["capture_of_oracle"] is not None]
    pooled_o2 = (sum(captures) / len(captures)) if captures else None

    ledger = d["ledger"]
    inst = {
        "repeat_pairs": len(rep_pairs),
        "repeat_dloss_max": (max(rep_pairs) if rep_pairs else None),
        "parse_rate": parse_ok / parse_all,
        "fail_rate": ledger["fail"] / max(1, ledger["req"]),
        "probe_cost": {"probe_req": ledger["probe_req"], "probe_tok": ledger["probe_tok"],
                       "total_req": ledger["req"], "total_tok": ledger["tok"]},
    }

    verdicts = None
    if d["mode"] == "governed":
        if any(v is None for v in GATES.values()):
            raise SystemExit("GATES not frozen; refusing to grade a governed log.")
        verdicts = {
            "O1": pooled_o1 >= GATES["O1_aligned_vs_random_pooled_min"],
            "O1b": all(metrics[c]["impr_aligned_vs_random"] >= GATES["O1b_per_consumer_floor"] for c in metrics),
            "O2": pooled_o2 is not None and pooled_o2 >= GATES["O2_capture_pooled_min"],
            "O3": pooled_o3 <= GATES["O3_anti_vs_random_pooled_max"],
            "O5": inst["repeat_dloss_max"] is not None and inst["repeat_dloss_max"] <= GATES["O5_repeat_dloss_max"],
            "O6": inst["parse_rate"] >= GATES["O6_parse_rate_min"],
            "O7": inst["fail_rate"] <= GATES["O7_fail_rate_max"],
        }
        verdicts["ALL"] = bool(all(verdicts.values()))

    out = {"campaign": d["campaign"], "mode": d["mode"], "seed": d["seed"],
           "gates": GATES if d["mode"] == "governed" else None,
           "verdicts": verdicts,
           "pooled": {"O1_aligned_vs_random": round(pooled_o1, 4),
                      "O2_capture": (round(pooled_o2, 4) if pooled_o2 is not None else None),
                      "O3_anti_vs_random": round(pooled_o3, 4)},
           "metrics": metrics, "instrument": inst, "ledger": ledger}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2)
    print(json.dumps({"pooled": out["pooled"],
                      "per_consumer": {c: {k: metrics[c][k] for k in
                                           ("impr_aligned_vs_random", "impr_anti_vs_random",
                                            "capture_of_oracle", "bracket_ok",
                                            "mean_loss_by_arm")}
                                       for c in metrics},
                      "instrument": inst, "verdicts": verdicts}, indent=2))
    print("written:", out_path)


if __name__ == "__main__":
    main()
