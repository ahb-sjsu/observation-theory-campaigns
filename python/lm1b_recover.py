#!/usr/bin/env python3
"""LM1-002 collection harness: consumer-anchored read-geometry recovery.

Successor to PREREG-LM1-001 (honest FAIL: task-oracle-anchored gates
were brittle where the consumer deviates from the task ideal). This
harness adds a HELD-OUT leg so the probe can be gated against the
CONSUMER: fresh states x fresh random unit directions u, central
differences along u, whose realized squared directional derivatives
the fitted operator must rank-predict. Task-oracle alignment is
collected for the diagnostic only.

Modes: pilot1 (disclosed) | governed (sealed seed; gates in lm1b_gates.py).
Stdlib only; Atlas orchestration; NRP ellm gateway compute; fair-use
code guards (concurrency 6, max_tokens 8, backoff, hard budget).

Frozen design (candidate, PREREG-LM1-002):
  model gemma-small; d = 6; prior U[-2,2]^6; 3-decimal serialization;
  probe width H = 0.15; N_STATES = 48 probe states per consumer;
  HELD-OUT (v4, power-sized after pilot 3): M_DIR = 48 fresh unit
  directions, each evaluated on the SAME K_STATES = 16 shared fresh
  states (common random numbers: state-position/cliff-distance noise
  is common-mode across directions, so the direction ranking is
  paired). Estimand: direction-mean E_x[(D_u L)^2] = u'Pu, the
  operator's defining property. History: v1 (one state per direction)
  swamped by state noise; v2 (independent states per direction)
  A 0.55 / B 0.05; v3 (CRN, 16 dirs) A -0.09 / B 0.46 — the Spearman
  at n_dirs = 16 has SE ~ 0.26 and was itself the binding noise, so
  v4 sizes n_dirs to 48 (SE ~ 0.15). All disclosed. N_REPEAT = 24.
Consumers as LM1-001 (planted; oracles now diagnostics only):
  A: is (2*s1 - s2) > s4      B: is (s3 + s5) > 1

Seeds: pilot1 = 20261020; governed = 20261025 (sealed if/when frozen).
"""
import json, os, random, sys, threading, time, urllib.request

BASE = "https://ellm.nrp-nautilus.io/v1/chat/completions"
TOKEN = os.environ.get("NRP_LLM_TOKEN", "")
MODEL = "gemma-small"
CONC = 6
MAX_TOKENS = 8
H = 0.15
N_STATES = 48
M_DIR = 48
K_STATES = 16
N_REPEAT = 24
D = 6
TOTAL_BUDGET = 4800
SEEDS = {"pilot1": 20261020, "pilot2": 20261022, "pilot3": 20261024,
         "pilot4": 20261026, "governed": 20261028}
_lock = threading.Lock()
_led = {"req": 0, "tok": 0, "fail": 0}

def guard():
    with _lock:
        if _led["req"] >= TOTAL_BUDGET:
            raise RuntimeError("request budget exhausted")
        _led["req"] += 1

def query(prompt):
    guard()
    body = {"model": MODEL, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": MAX_TOKENS, "temperature": 0,
            "logprobs": True, "top_logprobs": 5}
    data = json.dumps(body).encode()
    for attempt in range(5):
        try:
            req = urllib.request.Request(BASE, data,
                {"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
            r = json.load(urllib.request.urlopen(req, timeout=180))
            with _lock:
                _led["tok"] += r.get("usage", {}).get("total_tokens", 0)
            return r
        except Exception:
            time.sleep(2 ** attempt)
    with _lock:
        _led["fail"] += 1
    return None

def yesno_logprobs(resp):
    try:
        content = resp["choices"][0]["logprobs"]["content"]
    except (KeyError, TypeError, IndexError):
        return None, None
    for t in content:
        cand = {}
        pool = [(t["token"], t["logprob"])] + \
               [(a["token"], a["logprob"]) for a in t.get("top_logprobs", [])]
        for tk, lp in pool:
            s = tk.strip().lower().strip('."\',:;!')
            if s in ("yes", "no") and s not in cand:
                cand[s] = lp
        if cand:
            return cand.get("yes"), cand.get("no")
    return None, None

def serialize(x):
    return ", ".join(f"s{i+1}={v:.3f}" for i, v in enumerate(x))

CONSUMERS = {
    "A": {"question": "is (2*s1 - s2) greater than s4?",
          "truth": lambda x: "yes" if (2*x[0] - x[1]) > x[3] else "no"},
    "B": {"question": "is (s3 + s5) greater than 1?",
          "truth": lambda x: "yes" if (x[2] + x[4]) > 1.0 else "no"},
}

def make_prompt(xhat, question):
    return ("A system state is measured as: " + serialize(xhat) +
            ". Question: " + question + " Answer with exactly one word: yes or no.")

def unit(rng, d):
    while True:
        v = [rng.gauss(0, 1) for _ in range(d)]
        n = sum(a * a for a in v) ** 0.5
        if n > 1e-9:
            return [a / n for a in v]

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "pilot4"
    assert mode in SEEDS, "mode must be one of " + "/".join(SEEDS)
    seed = SEEDS[mode]
    rng = random.Random(seed)
    probe_states = [[rng.uniform(-2, 2) for _ in range(D)] for _ in range(N_STATES)]
    # held-out v3: M_DIR fresh directions, all evaluated on the SAME
    # K_STATES shared fresh states (CRN pairing across directions).
    ho = {}
    for cid in CONSUMERS:
        dirs = [unit(rng, D) for _ in range(M_DIR)]
        shared = [[rng.uniform(-2, 2) for _ in range(D)] for _ in range(K_STATES)]
        cells = []
        for di, u in enumerate(dirs):
            for kj in range(K_STATES):
                cells.append((di, shared[kj], u))
        ho[cid] = {"dirs": dirs, "shared_states": shared, "cells": cells}

    jobs = []  # (consumer, index, kind, comp, sign, u_or_None, prompt, correct)
    for cid, spec in CONSUMERS.items():
        for si, x in enumerate(probe_states):
            correct = spec["truth"](x)
            jobs.append((cid, si, "base", -1, 0, None, make_prompt(x, spec["question"]), correct))
            for i in range(D):
                for sign in (+1, -1):
                    xp = x[:]
                    xp[i] += sign * H
                    jobs.append((cid, si, "probe", i, sign, None,
                                 make_prompt(xp, spec["question"]), correct))
        for ci, (di, x, u) in enumerate(ho[cid]["cells"]):
            correct = spec["truth"](x)
            for sign in (+1, -1):
                xp = [x[j] + sign * H * u[j] for j in range(D)]
                jobs.append((cid, ci, "heldout", di, sign, u,
                             make_prompt(xp, spec["question"]), correct))
    rep_src = [j for j in jobs if j[0] == "A" and j[2] == "base"][:N_REPEAT]
    for j in rep_src:
        jobs.append((j[0], j[1], "repeat", -1, 0, None, j[6], j[7]))
    print(f"mode={mode} seed={seed} jobs={len(jobs)}", flush=True)

    results = [None] * len(jobs)
    sem = threading.Semaphore(CONC)
    def work(k):
        with sem:
            r = query(jobs[k][6])
            results[k] = yesno_logprobs(r) if r else (None, None)
    th = [threading.Thread(target=work, args=(k,)) for k in range(len(jobs))]
    for t in th: t.start()
    for t in th: t.join()

    rows = []
    for (cid, idx, kind, comp, sign, u, prompt, correct), (ly, ln) in zip(jobs, results):
        lp = ly if correct == "yes" else ln
        rows.append({"consumer": cid, "idx": idx, "kind": kind, "comp": comp,
                     "sign": sign, "u": u, "correct": correct,
                     "lp_yes": ly, "lp_no": ln,
                     "loss": (-lp if lp is not None else 12.0)})
    out = {"campaign": "LM1-002 consumer-anchored recovery (successor to PREREG-LM1-001)",
           "mode": mode, "disclosure": ("DISCLOSED CALIBRATION PILOT" if mode != "governed"
                                        else "GOVERNED RUN at the sealed seed"),
           "model": MODEL, "seed": seed, "h": H, "n_states": N_STATES,
           "m_dir": M_DIR, "k_states": K_STATES, "n_repeat": N_REPEAT, "d": D,
           "consumers": {k: {"question": v["question"]} for k, v in CONSUMERS.items()},
           "probe_states": probe_states,
           "heldout": {cid: {"dirs": ho[cid]["dirs"],
                             "shared_states": ho[cid]["shared_states"],
                             "cells": [{"dir": di, "x": x} for di, x, _u in ho[cid]["cells"]]}
                       for cid in ho},
           "rows": rows, "ledger": dict(_led)}
    os.makedirs("/home/claude/lm1b", exist_ok=True)
    path = f"/home/claude/lm1b/{mode}_log.json"
    with open(path, "w") as f:
        json.dump(out, f)
    print("DONE", path, json.dumps(_led), flush=True)

if __name__ == "__main__":
    main()
