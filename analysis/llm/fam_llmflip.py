"""XPROTO-LLM-FLIP family (F-LLM-FLIP): the two-consumer verdict inversion (the
Flip) in AI deployment gating, with its taxonomy-predicted null.

Consumers are two fleets of HANS deployment slices that fail through different
syntactic heuristics: the LO-fleet (lexical_overlap subcases) and the CN-fleet
(constituent subcases). Each fleet reads its own axis of the model's failure
surface. The certificate gates deployment per slice: deploy when a small probe
estimate clears the accuracy bar plus that slice's safety margin. Policies: a
fixed fleet-mean margin budget allocated two ways. Policy A puts the margin on
the lexical-overlap axis, policy B puts the same total on the constituent axis.
A slice false-clears when it is deployed and its true accuracy is below the bar.
Claim: the LO-fleet does better under A, the CN-fleet under B, and the aggregate
cannot order the pair.

Registered null: the same fleets and policies judged at two accuracy bars (0.75
and 0.85). A bar shift leaves both consumers reading the same projection, so no
inversion is expected.

Substrate: real inference (roberta-large-mnli on real HANS). The per-example
correctness is computed ONCE and cached (LLM-hans-correct.json, deterministic for
a fixed model and dataset); seeds drive only the probe resamples. Emits
LLMFLIPREP-family.json.
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np

import fam_llm as base

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "LLM-hans-correct.json")
BAR = 0.80                 # deployment accuracy bar (flip construction)
NULL_BARS = (0.75, 0.85)   # threshold pair for the null
MARGIN_MEAN = 0.08         # fleet-mean margin on the probe estimate
PROBE_N = 50               # probe examples per slice


def _correctness():
    """Per-subcase per-example correctness, cached (one real inference pass)."""
    if os.path.exists(CACHE):
        d = json.load(open(CACHE))
        return {k: np.array(v, bool) for k, v in d.items()}
    print("cache miss: one real inference pass (roberta-large-mnli on HANS)...", flush=True)
    import torch  # noqa: F401
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(base.MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(base.MODEL)
    model.eval()
    sub = base._hans_by_subcase(tok, model)
    json.dump({k: v.astype(int).tolist() for k, v in sub.items()}, open(CACHE, "w"))
    return sub


def run_cell(seed, sub):
    rng = np.random.default_rng(seed)
    names = sorted(sub.keys())
    lo = [n for n in names if "lexical_overlap" in n]
    cn = [n for n in names if "constituent" in n]
    fleet = {**{n: "LO" for n in lo}, **{n: "CN" for n in cn}}
    members = lo + cn
    true_acc = {n: float(sub[n].mean()) for n in members}
    # matched-budget margins on the two axes
    m_a = {n: (2 * MARGIN_MEAN if fleet[n] == "LO" else 0.0) for n in members}
    m_b = {n: (2 * MARGIN_MEAN if fleet[n] == "CN" else 0.0) for n in members}
    out = {"seed": int(seed), "mode": "real-llm", "n_lo": len(lo), "n_cn": len(cn),
           "mean_margin_A": round(float(np.mean(list(m_a.values()))), 4),
           "mean_margin_B": round(float(np.mean(list(m_b.values()))), 4)}

    def fc(margins, bar):
        rates = {"LO": [], "CN": []}
        for n in members:
            probe = rng.choice(sub[n], PROBE_N, replace=False).mean()
            deployed = probe >= bar + margins[n]
            rates[fleet[n]].append(1.0 if (deployed and true_acc[n] < bar) else 0.0)
        return float(np.mean(rates["LO"])), float(np.mean(rates["CN"]))

    for m, tag in ((m_a, "A"), (m_b, "B")):
        l, c = fc(m, BAR)
        out[f"fc_LO_{tag}"] = round(l, 4); out[f"fc_CN_{tag}"] = round(c, 4)
        out[f"fc_fleet_{tag}"] = round(0.5 * (l + c), 4)
    out["flip"] = bool(out["fc_LO_A"] < out["fc_LO_B"] and out["fc_CN_B"] < out["fc_CN_A"])
    # null: same margins, two accuracy bars on the same slices (threshold pair)
    for m, tag in ((m_a, "A"), (m_b, "B")):
        l1, c1 = fc(m, NULL_BARS[0]); l2, c2 = fc(m, NULL_BARS[1])
        out[f"null_fc_t1_{tag}"] = round(0.5 * (l1 + c1), 4)
        out[f"null_fc_t2_{tag}"] = round(0.5 * (l2 + c2), 4)
    out["null_flip"] = bool(out["null_fc_t1_A"] < out["null_fc_t1_B"]
                            and out["null_fc_t2_B"] < out["null_fc_t2_A"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "LLMFLIPREP-family.json"))
    args = ap.parse_args()
    sub = _correctness()
    cells = [run_cell(s, sub) for s in args.seeds]
    for c in cells:
        print(f"seed {c['seed']}: LO A={c['fc_LO_A']} B={c['fc_LO_B']} | "
              f"CN A={c['fc_CN_A']} B={c['fc_CN_B']} | FLIP={c['flip']} "
              f"null_flip={c['null_flip']}", flush=True)
    rec = {"family": "F-LLM-FLIP", "mode": "real-llm",
           "constants": {"bar": BAR, "null_bars": list(NULL_BARS),
                         "margin_mean": MARGIN_MEAN, "probe_n": PROBE_N,
                         "substrate": "roberta-large-mnli on real HANS (cached "
                                      "per-example correctness)"},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
