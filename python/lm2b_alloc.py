#!/usr/bin/env python3
"""LM-2 pilot collector: matched-budget precision allocation for an LLM
consumer, driven by the probed read geometry.

DISCLOSED CALIBRATION PILOT unless run as governed (gates in
lm2_gates.py; refuses until frozen). Stdlib only; Atlas orchestration;
NRP ellm gateway compute; fair-use code guards.

The operational question (LM track §5, on the LM1-003-licensed
instrument): at a MATCHED serialization budget, does allocating
precision to the components the consumer READS (per the probed P̂)
beat task-blind allocation, and does the blind P̂ capture most of the
oracle allocation's advantage?

Design:
  State x in R^6 ~ U[-2,2]^6. FINE/COARSE ladder (disclosed design
  choice): each component is serialized either COARSE (rounded to
  integer; quantization std ~0.29 — damaging near decision margins) or
  FINE (3 decimals; effectively lossless). Budget = exactly F = 3 of 6
  components fine. Decimals-ladder budgets were rejected in design:
  1-decimal uniform is already near-lossless at these margins, so the
  uniform baseline saturates and the comparison measures nothing.
  Arms (all budget-matched, same eval states, same noise — CRN exact):
    aligned : top-3 components by the diag of P̂ from a fresh probe leg
              (probe cost logged in the artifact)
    oracle  : the planted read components (A {1,2,4}; B {3,5}+next-best
              by P̂ among the rest)
    anti    : bottom-3 by P̂ diag (pooled load-bearing control)
    random  : a seed-drawn task-blind 3-subset (the budget-matched
              stand-in for uniform allocation on a discrete ladder;
              CompactPrompt-style uniform has no exact analog here —
              disclosed)
  References (not budget-matched; bracket diagnostics): all-coarse,
  all-fine.
  Endpoint: mean over N_EVAL shared fresh states of
  -logprob(correct-for-TRUE-x | prompt(quantized x)).
  Probe leg: as LM1-003 (48 states x central differences, h = 0.15),
  diag(P̂) computed in-collector (pure python) to build the arms.
  Instrument: 24 duplicated eval queries.

Consumers as LM-1: A "is (2*s1 - s2) > s4"; B "is (s3 + s5) > 1".

LM2-002 CHANGE (successor to PREREG-LM2-001, which failed by baseline
degeneracy — the single seed-drawn task-blind subset coincided with
the aligned allocation, probability 1/20 per consumer): the task-blind
baseline is now the MEAN over N_RAND = 4 seed-drawn subsets, each
rejection-sampled to be DISTINCT from both the aligned and oracle sets
(conditioning that only hardens the test) and pairwise distinct.
Degenerate comparisons are impossible by construction; baseline
variance drops as a bonus.

Seeds: pilotA = 20261120; pilotB = 20261122; governed = 20261125.
"""
import json, os, random, sys, threading, time, urllib.request

BASE = "https://ellm.nrp-nautilus.io/v1/chat/completions"
TOKEN = os.environ.get("NRP_LLM_TOKEN", "")
MODEL = "gemma-small"
CONC = 6
MAX_TOKENS = 8
H = 0.15
N_PROBE = 48
N_EVAL = 96
N_REPEAT = 24
D = 6
F_FINE = 3
N_RAND = 4
TOTAL_BUDGET = 3400
SEEDS = {"pilotA": 20261120, "pilotB": 20261122, "governed": 20261125}
_lock = threading.Lock()
_led = {"req": 0, "tok": 0, "fail": 0, "probe_req": 0, "probe_tok": 0}

def guard():
    with _lock:
        if _led["req"] >= TOTAL_BUDGET:
            raise RuntimeError("request budget exhausted")
        _led["req"] += 1

def query(prompt, probe=False):
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
                t = r.get("usage", {}).get("total_tokens", 0)
                _led["tok"] += t
                if probe:
                    _led["probe_req"] += 1
                    _led["probe_tok"] += t
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

def ser_full(x):
    return ", ".join(f"s{i+1}={v:.3f}" for i, v in enumerate(x))

def ser_alloc(x, fine):
    parts = []
    for i, v in enumerate(x):
        if i in fine:
            parts.append(f"s{i+1}={v:.3f}")
        else:
            parts.append(f"s{i+1}={round(v):.0f}")
    return ", ".join(parts)

CONSUMERS = {
    "A": {"question": "is (2*s1 - s2) greater than s4?",
          "truth": lambda x: "yes" if (2*x[0] - x[1]) > x[3] else "no",
          "oracle_support": [0, 1, 3]},
    "B": {"question": "is (s3 + s5) greater than 1?",
          "truth": lambda x: "yes" if (x[2] + x[4]) > 1.0 else "no",
          "oracle_support": [2, 4]},
}

def prompt_of(ser, question):
    return ("A system state is measured as: " + ser +
            ". Question: " + question + " Answer with exactly one word: yes or no.")

def run_batch(jobs):
    """jobs: list of (tag_dict, prompt, correct, probe_flag)."""
    results = [None] * len(jobs)
    sem = threading.Semaphore(CONC)
    def work(k):
        with sem:
            r = query(jobs[k][1], probe=jobs[k][3])
            results[k] = yesno_logprobs(r) if r else (None, None)
    th = [threading.Thread(target=work, args=(k,)) for k in range(len(jobs))]
    for t in th: t.start()
    for t in th: t.join()
    rows = []
    for (tag, prompt, correct, _pf), (ly, ln) in zip(jobs, results):
        lp = ly if correct == "yes" else ln
        row = dict(tag)
        row.update({"correct": correct, "lp_yes": ly, "lp_no": ln,
                    "loss": (-lp if lp is not None else 12.0)})
        rows.append(row)
    return rows

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "pilotA"
    assert mode in SEEDS
    seed = SEEDS[mode]
    rng = random.Random(seed)
    probe_states = [[rng.uniform(-2, 2) for _ in range(D)] for _ in range(N_PROBE)]
    eval_states = {cid: [[rng.uniform(-2, 2) for _ in range(D)] for _ in range(N_EVAL)]
                   for cid in CONSUMERS}
    # task-blind subsets are drawn AFTER the probe (they must avoid the
    # aligned set); a dedicated child rng keeps the draw deterministic.
    rand_rng = random.Random(seed + 7)

    all_rows = []
    alloc_record = {}
    for cid, spec in CONSUMERS.items():
        # --- probe leg (cost logged separately) ---
        jobs = []
        for si, x in enumerate(probe_states):
            correct = spec["truth"](x)
            for i in range(D):
                for sign in (+1, -1):
                    xp = x[:]
                    xp[i] += sign * H
                    jobs.append(({"consumer": cid, "leg": "probe", "state": si,
                                  "comp": i, "sign": sign},
                                 prompt_of(ser_full(xp), spec["question"]), correct, True))
        rows = run_batch(jobs)
        all_rows.extend(rows)
        # diag(P̂) in pure python: mean over states of g_i^2
        diag = [0.0] * D
        tab = {(r["state"], r["comp"], r["sign"]): r["loss"] for r in rows}
        for si in range(N_PROBE):
            for i in range(D):
                gp, gm = tab.get((si, i, 1)), tab.get((si, i, -1))
                if gp is not None and gm is not None:
                    g = (gp - gm) / (2 * H)
                    diag[i] += g * g / N_PROBE
        order = sorted(range(D), key=lambda i: -diag[i])
        aligned = sorted(order[:F_FINE])
        anti = sorted(order[-F_FINE:])
        osup = list(spec["oracle_support"])
        if len(osup) < F_FINE:  # fill oracle to budget by P̂ among the rest
            osup += [i for i in order if i not in osup][: F_FINE - len(osup)]
        oracle = sorted(osup[:F_FINE])
        # LM2-002 baseline: N_RAND distinct task-blind subsets, none equal
        # to aligned or oracle, pairwise distinct (rejection sampling).
        forbidden = {tuple(aligned), tuple(oracle)}
        rand_sets = []
        while len(rand_sets) < N_RAND:
            cand = tuple(sorted(rand_rng.sample(range(D), F_FINE)))
            if cand not in forbidden:
                forbidden.add(cand)
                rand_sets.append(list(cand))
        arms = {"aligned": aligned, "oracle": oracle, "anti": anti,
                "allcoarse": [], "allfine": list(range(D))}
        for ri, rs in enumerate(rand_sets):
            arms[f"random{ri+1}"] = rs
        alloc_record[cid] = {"diag_Phat": diag, "arms": {k: v for k, v in arms.items()}}
        # --- eval legs, CRN: same states for every arm ---
        jobs = []
        for arm, fine in arms.items():
            for si, x in enumerate(eval_states[cid]):
                correct = spec["truth"](x)
                jobs.append(({"consumer": cid, "leg": "eval", "arm": arm,
                              "state": si},
                             prompt_of(ser_alloc(x, set(fine)), spec["question"]),
                             correct, False))
        # instrument repeats: duplicate first N_REPEAT aligned-arm queries (A only)
        if cid == "A":
            for si in range(N_REPEAT):
                x = eval_states[cid][si]
                jobs.append(({"consumer": cid, "leg": "repeat", "arm": "aligned",
                              "state": si},
                             prompt_of(ser_alloc(x, set(arms["aligned"])), spec["question"]),
                             spec["truth"](x), False))
        all_rows.extend(run_batch(jobs))
        print(f"[{cid}] probe+eval done; aligned={aligned} oracle={oracle} "
              f"anti={anti} rand={rand_sets}", flush=True)

    out = {"campaign": "LM2-002 matched-budget precision allocation, degeneracy-proof baseline (successor to PREREG-LM2-001)",
           "mode": mode,
           "disclosure": ("DISCLOSED CALIBRATION PILOT" if mode != "governed"
                          else "GOVERNED RUN at the sealed seed"),
           "model": MODEL, "seed": seed, "h": H, "n_probe": N_PROBE,
           "n_eval": N_EVAL, "n_repeat": N_REPEAT, "d": D, "f_fine": F_FINE,
           "consumers": {k: {"question": v["question"],
                             "oracle_support": v["oracle_support"]} for k, v in CONSUMERS.items()},
           "allocations": alloc_record,
           "eval_states": eval_states, "rows": all_rows, "ledger": dict(_led)}
    os.makedirs("/home/claude/lm2b", exist_ok=True)
    path = f"/home/claude/lm2b/{mode}_log.json"
    with open(path, "w") as f:
        json.dump(out, f)
    print("DONE", path, json.dumps(_led), flush=True)

if __name__ == "__main__":
    main()
