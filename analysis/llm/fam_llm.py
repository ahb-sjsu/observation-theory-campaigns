"""XPROTO-LLM family (F-LLM): consumer-relative eval-vs-deployment vacuity for a
language model, on REAL data (MNLI benchmark -> HANS deployment).

A model's benchmark score is a CERTIFICATE -- "capable enough, deploy it." The
deployment distribution is not the benchmark: the consumer's actual inputs form a
FOOTPRINT the aggregate score is blind to. A model that passes the benchmark
**false-clears** on the deployment slices where it fails -- silently, because it
looked fine on the leaderboard. The false-clear is **consumer-relative**: which
deployment slice you serve decides whether the certified model works. This is the
KV-keys / XPROTO-AICSI lesson for AI evaluation.

  * consumer = a deployment slice (HANS subcase -- a structured input footprint).
  * certificate = benchmark accuracy >= target -> "deploy everywhere".
  * witness = the true per-slice accuracy (ground-truth labels on that slice).
  * naive: trust the aggregate benchmark; aware: measure the slice footprint.

Substrate: a REAL pretrained MNLI model (roberta-large-mnli) on the REAL MNLI
validation set (benchmark) and the REAL HANS challenge set (deployment; McCoy et
al.), whose 30 subcases are the consumer footprints. Emits LLMREP-family.json.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import urllib.request

import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
HANS_TXT = os.path.join(DATA, "hans_eval.txt")
HANS_URL = "https://raw.githubusercontent.com/tommccoy1/hans/master/heuristics_evaluation_set.txt"

MODEL = "roberta-large-mnli"       # entailment = idx 2 (id2label {0:C,1:N,2:E})
TARGET = 0.80                       # deployment reliability the certificate claims
N_MNLI = 1000                      # benchmark eval size
N_PER_SUBCASE = 150               # deployment eval per HANS subcase
N_PROBE = 50                      # footprint sample the AWARE policy measures
BATCH = 32
MAXLEN = 128


def _fetch_hans():
    if not os.path.exists(HANS_TXT):
        os.makedirs(DATA, exist_ok=True)
        urllib.request.urlretrieve(HANS_URL, HANS_TXT)


@torch.no_grad()
def _predict(tok, model, pairs):
    """Return predicted class index per (premise, hypothesis) pair."""
    out = []
    for i in range(0, len(pairs), BATCH):
        b = pairs[i:i + BATCH]
        enc = tok([p[0] for p in b], [p[1] for p in b], return_tensors="pt",
                  padding=True, truncation=True, max_length=MAXLEN)
        out.extend(model(**enc).logits.argmax(-1).tolist())
    return out


def _mnli_correct(tok, model):
    from datasets import load_dataset
    d = load_dataset("nyu-mll/multi_nli", split="validation_matched")
    d = d.select(range(min(N_MNLI, len(d))))
    pairs = list(zip(d["premise"], d["hypothesis"]))
    preds = _predict(tok, model, pairs)
    # model idx {0:contra,1:neutral,2:entail} -> MNLI gold {0:entail,1:neutral,2:contra}
    to_gold = {2: 0, 1: 1, 0: 2}
    return np.array([to_gold[p] == g for p, g in zip(preds, d["label"]) if g in (0, 1, 2)])


def _hans_by_subcase(tok, model):
    _fetch_hans()
    rows = list(csv.DictReader(open(HANS_TXT, encoding="utf-8"), delimiter="\t"))
    bysub = {}
    for r in rows:
        bysub.setdefault(r["subcase"], []).append(r)
    subcase_correct = {}
    for sub, rs in bysub.items():
        rs = rs[:N_PER_SUBCASE]
        pairs = [(r["sentence1"], r["sentence2"]) for r in rs]
        preds = _predict(tok, model, pairs)
        # HANS: entailment iff model idx==2; else non-entailment
        corr = [((p == 2) == (r["gold_label"] == "entailment")) for p, r in zip(preds, rs)]
        subcase_correct[sub] = np.array(corr)
    return subcase_correct


def run_cell(seed, bench_correct, subcase_correct):
    rng = np.random.default_rng(seed)
    # benchmark certificate (bootstrap)
    bench_acc = float(bench_correct[rng.integers(0, len(bench_correct), len(bench_correct))].mean())
    certified = bench_acc >= TARGET
    true_acc, naive_fc, aware_fc = {}, 0, 0
    for sub, corr in subcase_correct.items():
        true = float(corr.mean())                        # witness: true slice accuracy
        true_acc[sub] = true
        probe = float(corr[rng.integers(0, len(corr), N_PROBE)].mean())  # aware footprint sample
        if certified and true < TARGET:                  # naive deploys everywhere
            naive_fc += 1
        if (probe >= TARGET) and true < TARGET:          # aware deploys iff footprint clears
            aware_fc += 1
    k = len(subcase_correct)
    accs = np.array(list(true_acc.values()))
    return {
        "seed": int(seed), "mode": "roberta-large-mnli/hans",
        "benchmark_acc": round(bench_acc, 4), "certified": bool(certified),
        "naive_fc": round(naive_fc / k, 4), "aware_fc": round(aware_fc / k, 4),
        "consumer_acc_spread": round(float(accs.std()), 4),
        "deployment_mean_acc": round(float(accs.mean()), 4),
        "n_consumers": int(k), "target": TARGET,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "LLMREP-family.json"))
    args = ap.parse_args()
    print(f"loading {MODEL} + running REAL inference (MNLI benchmark + HANS deployment)...",
          flush=True)
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL); model.eval()
    bench = _mnli_correct(tok, model)
    subcase = _hans_by_subcase(tok, model)
    print(f"benchmark n={len(bench)} acc={bench.mean():.3f} | HANS subcases={len(subcase)}",
          flush=True)
    cells = [run_cell(s, bench, subcase) for s in args.seeds]
    for c in cells:
        print(f"seed {c['seed']}: bench_acc={c['benchmark_acc']} (cert={c['certified']}) | "
              f"naive_fc={c['naive_fc']} aware_fc={c['aware_fc']} | "
              f"spread={c['consumer_acc_spread']} deploy_mean={c['deployment_mean_acc']}", flush=True)
    rec = {"family": "F-LLM", "mode": "roberta-large-mnli/hans",
           "sim_is_code_validation_not_evidence": False,
           "constants": {"model": MODEL, "target": TARGET, "n_mnli": N_MNLI,
                         "n_per_subcase": N_PER_SUBCASE, "n_probe": N_PROBE,
                         "substrate": "REAL roberta-large-mnli on REAL MNLI val_matched "
                                      "(benchmark) + REAL HANS challenge set (deployment; "
                                      "30 subcase footprints)"},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
