#!/usr/bin/env python3
"""LM1-003 collection harness: consumer-anchored recovery, multi-draw
bar calibration.

Successor to PREREG-LM1-002 (honest FAIL: H1's bar came from ONE
powered pilot draw + a null-SE formula; consumer A's across-draw
history at power showed variance far beyond the null). LM1-003 fixes
per the designation: (a) BARS FROM TWO INDEPENDENT POWERED
CALIBRATION DRAWS, set below their minimum with margin; (b) K raised
to 24 shared states (cut realized-mean noise); (c) pooled-across-
consumers H1 as the load-bearing quantity (the 088 lesson), with
per-consumer floors secondary; (d) the 48-direction set includes the
6 COORDINATE AXES (a fixed canonical set declared here, before any
draw — no circularity), so dominant-direction consumers contribute
genuine dynamic range to the ranking; the remaining 42 directions
are random per draw.

Modes: pilotA | pilotB (the two disclosed powered calibration draws)
| governed (sealed seed; gates in lm1c_gates.py). Stdlib only; Atlas
orchestration; NRP ellm gateway compute; fair-use code guards
(concurrency 6, max_tokens 8, backoff, hard budget).

Design (candidate, PREREG-LM1-003): model gemma-small; d = 6; prior
U[-2,2]^6; 3-decimal serialization; probe width H = 0.15; N_STATES =
48 probe states per consumer; held-out M_DIR = 48 (6 axes + 42
random) x K_STATES = 24 shared fresh states (CRN); estimand
direction-mean E_x[(D_u L)^2] = u'Pu; N_REPEAT = 24.
Consumers as before (planted; oracles are diagnostics only):
  A: is (2*s1 - s2) > s4      B: is (s3 + s5) > 1

Seeds: pilotA = 20261030; pilotB = 20261101; governed = 20261105.
"""
import json, os, random, sys, threading, time, urllib.request

BASE = "https://ellm.nrp-nautilus.io/v1/chat/completions"
TOKEN = os.environ.get("NRP_LLM_TOKEN", "")
MODEL = "gemma-small"
CONC = 6
MAX_TOKENS = 8
H = 0.15
N_STATES = 48
M_DIR = 48   # 6 coordinate axes + 42 random per draw
K_STATES = 24
N_REPEAT = 24
D = 6
TOTAL_BUDGET = 6200
SEEDS = {"pilotA": 20261030, "pilotB": 20261101, "governed": 20261105}
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
    mode = sys.argv[1] if len(sys.argv) > 1 else "pilotA"
    assert mode in SEEDS, "mode must be one of " + "/".join(SEEDS)
    seed = SEEDS[mode]
    rng = random.Random(seed)
    probe_states = [[rng.uniform(-2, 2) for _ in range(D)] for _ in range(N_STATES)]
    # held-out: 6 canonical coordinate axes + 42 random directions, all
    # evaluated on the SAME K_STATES shared fresh states (CRN pairing).
    ho = {}
    for cid in CONSUMERS:
        axes = [[1.0 if j == i else 0.0 for j in range(D)] for i in range(D)]
        dirs = axes + [unit(rng, D) for _ in range(M_DIR - D)]
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
    out = {"campaign": "LM1-003 consumer-anchored recovery, multi-draw calibration (successor to PREREG-LM1-002)",
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
    os.makedirs("/home/claude/lm1c", exist_ok=True)
    path = f"/home/claude/lm1c/{mode}_log.json"
    with open(path, "w") as f:
        json.dump(out, f)
    print("DONE", path, json.dumps(_led), flush=True)

if __name__ == "__main__":
    main()
