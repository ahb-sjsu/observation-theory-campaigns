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

# LM2-002: the task-blind BASELINE is the mean loss over four
# seed-drawn subsets, each distinct from the aligned and oracle sets
# (degeneracy impossible by construction — the LM2-001 lesson).
# GATES None until frozen from >= 2 powered draws (the LM1-003
# lesson). The quantize-the-unread finding remains ungated.
# Frozen 2026-08-20 from the ACROSS-DRAW calibration of two
# independent powered draws (pilotA 20261120 / pilotB 20261122):
# pooled O1 0.2436/0.2974; per-consumer min 0.238 (the mean-4 baseline
# halves per-cell variance); capture 0.997/1.001 (blind == oracle in
# every cell); pooled anti -0.065/-0.359 with per-cell swings to +0.05
# observed across LM-2 history, so O3's bar is +0.10 ("anti must not
# meaningfully beat blind"), documented rather than wishfully tight;
# repeat max 0.087/0.057.
GATES = {
    "O1_aligned_vs_baseline_pooled_min": 0.12,
    "O1b_per_consumer_floor": 0.05,
    "O2_capture_pooled_min": 0.60,
    "O3_anti_vs_baseline_pooled_max": 0.10,
    "O5_repeat_dloss_max": 0.50,
    "O6_parse_rate_min": 0.98,
    "O7_fail_rate_max": 0.01,
}

RAND_ARMS = ["random1", "random2", "random3", "random4"]
ARMS = ["aligned", "oracle", "anti"] + RAND_ARMS + ["allcoarse", "allfine"]


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
        base = sum(m[a] for a in RAND_ARMS) / len(RAND_ARMS)
        m["baseline_mean4"] = base
        impr_aligned = 1.0 - m["aligned"] / base
        impr_anti = 1.0 - m["anti"] / base
        gap_oracle = base - m["oracle"]
        capture = ((base - m["aligned"]) / gap_oracle) if gap_oracle > 0 else None
        metrics[cid] = {
            "mean_loss_by_arm": {k: (round(v, 5) if v is not None else None) for k, v in m.items()},
            "impr_aligned_vs_baseline": round(impr_aligned, 4),
            "impr_anti_vs_baseline": round(impr_anti, 4),
            "capture_of_oracle": (round(capture, 4) if capture is not None else None),
            "bracket_ok": bool(m["allcoarse"] >= min(m["aligned"], m["oracle"], base) and
                               m["allfine"] <= min(m["aligned"], m["oracle"], base)),
            "allocations": d["allocations"][cid]["arms"],
            "diag_Phat": [round(x, 5) for x in d["allocations"][cid]["diag_Phat"]],
        }

    pooled_o1 = sum(metrics[c]["impr_aligned_vs_baseline"] for c in metrics) / len(metrics)
    pooled_o3 = sum(metrics[c]["impr_anti_vs_baseline"] for c in metrics) / len(metrics)
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
            "O1": pooled_o1 >= GATES["O1_aligned_vs_baseline_pooled_min"],
            "O1b": all(metrics[c]["impr_aligned_vs_baseline"] >= GATES["O1b_per_consumer_floor"] for c in metrics),
            "O2": pooled_o2 is not None and pooled_o2 >= GATES["O2_capture_pooled_min"],
            "O3": pooled_o3 <= GATES["O3_anti_vs_baseline_pooled_max"],
            "O5": inst["repeat_dloss_max"] is not None and inst["repeat_dloss_max"] <= GATES["O5_repeat_dloss_max"],
            "O6": inst["parse_rate"] >= GATES["O6_parse_rate_min"],
            "O7": inst["fail_rate"] <= GATES["O7_fail_rate_max"],
        }
        verdicts["ALL"] = bool(all(verdicts.values()))

    out = {"campaign": d["campaign"], "mode": d["mode"], "seed": d["seed"],
           "gates": GATES if d["mode"] == "governed" else None,
           "verdicts": verdicts,
           "pooled": {"O1_aligned_vs_baseline": round(pooled_o1, 4),
                      "O2_capture": (round(pooled_o2, 4) if pooled_o2 is not None else None),
                      "O3_anti_vs_baseline": round(pooled_o3, 4)},
           "metrics": metrics, "instrument": inst, "ledger": ledger}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2)
    print(json.dumps({"pooled": out["pooled"],
                      "per_consumer": {c: {k: metrics[c][k] for k in
                                           ("impr_aligned_vs_baseline", "impr_anti_vs_baseline",
                                            "capture_of_oracle", "bracket_ok",
                                            "mean_loss_by_arm")}
                                       for c in metrics},
                      "instrument": inst, "verdicts": verdicts}, indent=2))
    print("written:", out_path)


if __name__ == "__main__":
    main()
