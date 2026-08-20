#!/usr/bin/env python3
"""LM-1 pilot 1 data collection: blind read-geometry probing of gemma-small.

DISCLOSED CALIBRATION PILOT, not claim-bearing. Collects RAW losses for
every (state, perturbation) query; all analysis happens offline from
this log (logged-response reproducibility posture). Stdlib only.

Two planted consumers over x in R^6 (serialized 3-decimal record):
  A: "is 2*s1 - s2 greater than s4?"  oracle dir ~ (2,-1,0,-1,0,0)
  B: "is s3 + s5 greater than 1?"     oracle dir ~ (0,0,1,0,1,0)
Loss L(xhat; x) = -logprob(correct-for-x | prompt(xhat)) at T=0: the
consumer misled by a perturbed estimate, judged against fixed truth.
Probe: central differences at width h per component; h IS the smoothing
width (finite-perturbation construction, Paper VIII section VI).
  A at h in {0.10, 0.25} (width calibration), B at h = 0.15.
"""
import json, os, random, threading, time, urllib.request, urllib.error

BASE = "https://ellm.nrp-nautilus.io/v1/chat/completions"
TOKEN = os.environ.get("NRP_LLM_TOKEN", "")
MODEL = "gemma-small"
CONC = 6
MAX_TOKENS = 8
N_STATES = 32
D = 6
TOTAL_BUDGET = 1600
SEED = 20261005
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
          "truth": lambda x: "yes" if (2*x[0] - x[1]) > x[3] else "no",
          "widths": [0.10, 0.25]},
    "B": {"question": "is (s3 + s5) greater than 1?",
          "truth": lambda x: "yes" if (x[2] + x[4]) > 1.0 else "no",
          "widths": [0.15]},
}

def make_prompt(xhat, question):
    return ("A system state is measured as: " + serialize(xhat) +
            ". Question: " + question + " Answer with exactly one word: yes or no.")

def main():
    rng = random.Random(SEED)
    states = [[rng.uniform(-2, 2) for _ in range(D)] for _ in range(N_STATES)]
    jobs = []  # (cid, state_idx, width_or_0base, comp, sign, prompt, correct)
    for cid, spec in CONSUMERS.items():
        for si, x in enumerate(states):
            correct = spec["truth"](x)
            jobs.append((cid, si, 0.0, -1, 0, make_prompt(x, spec["question"]), correct))
            for h in spec["widths"]:
                for i in range(D):
                    for sign in (+1, -1):
                        xp = x[:]
                        xp[i] += sign * h
                        jobs.append((cid, si, h, i, sign,
                                     make_prompt(xp, spec["question"]), correct))
    print(f"jobs: {len(jobs)}", flush=True)
    results = [None] * len(jobs)
    sem = threading.Semaphore(CONC)
    def work(k):
        with sem:
            r = query(jobs[k][5])
            ly, ln = (yesno_logprobs(r) if r else (None, None))
            results[k] = (ly, ln)
    th = [threading.Thread(target=work, args=(k,)) for k in range(len(jobs))]
    for t in th: t.start()
    for t in th: t.join()

    rows = []
    for (cid, si, h, comp, sign, prompt, correct), (ly, ln) in zip(jobs, results):
        lp = ly if correct == "yes" else ln
        loss = -lp if lp is not None else 12.0
        rows.append({"consumer": cid, "state": si, "h": h, "comp": comp,
                     "sign": sign, "correct": correct, "lp_yes": ly,
                     "lp_no": ln, "loss": loss})
    out = {"pilot": "LM1-pilot1 raw probe log (disclosed; NOT claim-bearing)",
           "model": MODEL, "seed": SEED, "n_states": N_STATES, "d": D,
           "consumers": {k: {"question": v["question"], "widths": v["widths"]}
                          for k, v in CONSUMERS.items()},
           "states": states, "rows": rows, "ledger": dict(_led)}
    os.makedirs("/home/claude/lm1", exist_ok=True)
    with open("/home/claude/lm1/probe_log.json", "w") as f:
        json.dump(out, f)
    print("DONE", json.dumps(_led), flush=True)

if __name__ == "__main__":
    main()
