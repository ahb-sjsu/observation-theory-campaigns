#!/usr/bin/env python
"""EC track: committed-artifact self-consistency for GO-P-2026-087/088/089.

Re-derives every gate from the committed result JSONs against their frozen
configs, and re-derives the 087 headline metrics (P1 pooled ratio, P2 mean
relative improvement) from the raw per-system losses. No harness re-run (the
governed harnesses are 8-20 minutes each; re-running them is reproduction,
not verification — the seeds are sealed and the runs are deterministic).

Ported from geometric-observation's ci/reproduce.py sections [2b]/[2c] when
the EC campaigns migrated to this repository.

Run from repo root:  python python/verify_ec_gates.py
Exit 0 iff everything is self-consistent.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
failures = []


def check(jname, derive, extra=None):
    try:
        d = json.load(open(os.path.join(ROOT, "results", jname)))
        g = derive(d["config"], d["metrics"])
        bad = []
        if g != d["gates"]:
            bad.append(f"gates rederived {g} != committed {d['gates']}")
        if (d["verdict"] == "ALL PASS") != all(g.values()):
            bad.append(f"verdict '{d['verdict']}' inconsistent with gates")
        if extra:
            bad.extend(extra(d))
        if bad:
            failures.append(f"{jname}: " + "; ".join(bad))
            print(f"  FAIL {jname}: " + "; ".join(bad))
        else:
            print(f"  PASS {jname}")
    except Exception as e:
        failures.append(f"{jname} crashed: {e}")
        print(f"  FAIL {jname}: {e}")


def extra_87(d):
    m = d["metrics"]
    g_ot = sum(s["iso-trace"]["loss"] - s["ot-blind"]["loss"] for s in d["armP"])
    g_or = sum(s["iso-trace"]["loss"] - s["oracle"]["loss"] for s in d["armP"])
    p1 = g_ot / g_or
    p2 = sum((min(s["iso-trace"]["loss"], s["logdet"]["loss"]) - s["ot-blind"]["loss"])
             / min(s["iso-trace"]["loss"], s["logdet"]["loss"]) for s in d["armN"]) / len(d["armN"])
    out = []
    if abs(p1 - m["P1_match_fraction"]) > 1e-9:
        out.append(f"P1 rederived {p1:.6f} != committed {m['P1_match_fraction']:.6f}")
    if abs(p2 - m["P2_rel_improvement"]) > 1e-9:
        out.append(f"P2 rederived {p2:.6f} != committed {m['P2_rel_improvement']:.6f}")
    return out


print("EC track committed-artifact self-consistency")
print("=" * 60)
check("GO87-blind-scheduling.json", lambda c, m: {
    "P1_match": m["P1_match_fraction"] >= 1 - c["eps_match"],
    "P2_improve": m["P2_rel_improvement"] >= c["delta_N"],
    "P3_ordering": m["P3_ordering"] >= c["q_order"],
    "C_shuffled_no_free_lunch": m["shuffled_gap"] >= -0.02,
    "C_anti_worst": bool(m["anti_worst"]),
}, extra=extra_87)
check("GO88-consumer-flip.json", lambda c, m: {
    "F1_flip": m["F1"] >= c["q_flip"],
    "F2_prediction": m["F2"] >= c["q_pred"],
    "F3_magnitude": m["F3"] >= c["delta_flip"],
    "I_min_matched": m["n_matched"] >= 6,   # min_matched per the sealed prereg
    "C_iso_bounded": m["iso_frac"] <= c["iso_frac"],
    "C_random_worst": bool(m["random_worst"]),
})
check("GO89-operational-trigger.json", lambda c, m: {
    "T1_armP": m["T1_armP"] >= c["delta_T"],
    "T1_armN": m["T1_armN"] >= c["delta_T"],
    "T2_blind_match": m["T2"] >= 1 - c["eps_T"],
    "T3_budget_band": bool(m["T3"]),
    "C_shuffled_no_free_lunch": m["shuffled_gap"] >= -0.02,
    "C_anti_worst": bool(m["anti_worst"]),
})
check("EC5-fso-consumer.json", lambda c, m: {
    "E1_prediction": (m["E1"] == m["E1"]) and m["E1"] >= c["q_pred"],
    "I_min_pairs": m["E1_pairs"] >= c["min_pairs"],
    "E2_win": m["E2"] >= c["delta_e2"],
    "E3_capture": m["E3"] >= 1 - c["eps_e3"],
    "C_shuffled_no_free_lunch": m["shuffled_gap"] >= -0.02,
    "C_anti_worst": bool(m["anti_worst"]),
})
check("EC6-multiconsumer.json", lambda c, m: {
    "M1_free_when_aligned": m["M1"] <= 1 + c["m1_band"],
    "M2_tax_rises": m["M2"] >= c["m2_gap"],
    "M3_tax_at_orthogonal": m["M3"] >= 1 + c["m3_tax"],
    "M4_geometry_beats_blind": m["M4"] >= c["m4_impr"],
    "C_dedicated_sane": bool(m["dedicated_sane"]),
    "C_random_worst": bool(m["random_worst"]),
})
# EC-7's committed verdict is FAIL (integrity gate); the self-consistency
# check re-derives that FAIL — verification is sign-agnostic.
check("EC7-closedloop.json", lambda c, m: {
    "K1_consumer_penalty_wins": m["K1"] >= c["delta_k1"],
    "K2_blind_capture": m["K2"] >= 1 - c["eps_k2"],
    "K3_vs_hand_diag": m["K3"] >= c["delta_k3"],
    "I_stable": bool(m["stable"]),
    "I_bounded": bool(m["bounded"]),
    "I_effort_matched": bool(m["effort_matched"]),
    "C_shuffled_no_free_lunch": m["shuffled_gap"] >= -0.02,
    "C_anti": bool(m["anti_ok"]),
})

print("=" * 60)
if failures:
    print(f"RESULT: FAIL ({len(failures)})")
    sys.exit(1)
print("RESULT: GREEN — all EC gates and headline metrics re-derive from the "
      "committed artifacts.")
sys.exit(0)
