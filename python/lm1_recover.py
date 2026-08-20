#!/usr/bin/env python3
"""LM-1 collection harness: blind read-geometry recovery on gemma-small.

Modes: pilot2 (disclosed calibration) | governed (single run at the
sealed seed; gates evaluated offline by lm1_gates.py from this log).
Stdlib only; runs on Atlas as orchestration; compute = NRP ellm
gateway. Fair-use code guards: concurrency 6, max_tokens 8, backoff,
hard request budget. Raw log is the artifact: every query's yes/no
logprobs recorded verbatim (logged-response reproducibility posture).

Frozen design (PREREG-LM1-001):
  model gemma-small; d = 6; prior U[-2,2]^6; serialization 3 decimals;
  probe width H = 0.15 (pilot-1 calibration: 0.10 sharp but admits a
  spurious channel, 0.25 suppresses it at alignment cost; 0.15 frozen);
  N_STATES = 48; central differences per component; fixed-truth loss
  L(xhat; x) = -logprob(correct-for-x | prompt(xhat)) at T=0;
  N_REPEAT = 24 duplicated base queries appended as the instrument leg.
Consumers (planted; oracle directions known by construction):
  A: is (2*s1 - s2) > s4          oracle ~ (2,-1,0,-1,0,0)
  B: is (s3 + s5) > 1             oracle ~ (0,0,1,0,1,0)

Seeds: pilot2 = 20261010; governed = 20261015 (sealed).
"""
import json, os, random, sys, threading, time, urllib.request

BASE = "https://ellm.nrp-nautilus.io/v1/chat/completions"
TOKEN = os.environ.get("NRP_LLM_TOKEN", "")
MODEL = "gemma-small"
CONC = 6
MAX_TOKENS = 8
H = 0.15
N_STATES = 48
N_REPEAT = 24
D = 6
TOTAL_BUDGET = 1700
SEEDS = {"pilot2": 20261010, "governed": 20261015}
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

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "pilot2"
    assert mode in SEEDS, "mode must be pilot2 or governed"
    seed = SEEDS[mode]
    rng = random.Random(seed)
    states = [[rng.uniform(-2, 2) for _ in range(D)] for _ in range(N_STATES)]
    jobs = []  # (consumer, state, kind, comp, sign, prompt, correct)
    for cid, spec in CONSUMERS.items():
        for si, x in enumerate(states):
            correct = spec["truth"](x)
            jobs.append((cid, si, "base", -1, 0, make_prompt(x, spec["question"]), correct))
            for i in range(D):
                for sign in (+1, -1):
                    xp = x[:]
                    xp[i] += sign * H
                    jobs.append((cid, si, "probe", i, sign,
                                 make_prompt(xp, spec["question"]), correct))
    # instrument leg: duplicate the first N_REPEAT consumer-A base prompts
    rep_src = [j for j in jobs if j[0] == "A" and j[2] == "base"][:N_REPEAT]
    for j in rep_src:
        jobs.append((j[0], j[1], "repeat", -1, 0, j[5], j[6]))
    print(f"mode={mode} seed={seed} jobs={len(jobs)}", flush=True)

    results = [None] * len(jobs)
    sem = threading.Semaphore(CONC)
    def work(k):
        with sem:
            r = query(jobs[k][5])
            results[k] = yesno_logprobs(r) if r else (None, None)
    th = [threading.Thread(target=work, args=(k,)) for k in range(len(jobs))]
    for t in th: t.start()
    for t in th: t.join()

    rows = []
    for (cid, si, kind, comp, sign, prompt, correct), (ly, ln) in zip(jobs, results):
        lp = ly if correct == "yes" else ln
        rows.append({"consumer": cid, "state": si, "kind": kind, "comp": comp,
                     "sign": sign, "correct": correct, "lp_yes": ly, "lp_no": ln,
                     "loss": (-lp if lp is not None else 12.0)})
    out = {"campaign": "LM-1 blind read-geometry recovery (PREREG-LM1-001)",
           "mode": mode, "disclosure": ("DISCLOSED CALIBRATION PILOT" if mode != "governed"
                                        else "GOVERNED RUN at the sealed seed"),
           "model": MODEL, "seed": seed, "h": H, "n_states": N_STATES,
           "n_repeat": N_REPEAT, "d": D,
           "consumers": {k: {"question": v["question"]} for k, v in CONSUMERS.items()},
           "states": states, "rows": rows, "ledger": dict(_led)}
    os.makedirs("/home/claude/lm1", exist_ok=True)
    path = f"/home/claude/lm1/{mode}_log.json"
    with open(path, "w") as f:
        json.dump(out, f)
    print("DONE", path, json.dumps(_led), flush=True)

if __name__ == "__main__":
    main()
