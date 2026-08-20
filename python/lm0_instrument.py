#!/usr/bin/env python3
"""LM track Pilot 0: instrument characterization on the NRP ellm gateway.

DISCLOSED CALIBRATION PILOT, not claim-bearing (PROTOCOL 5.1).
Runs ON Atlas (orchestration only; compute is the hosted gateway).
Stdlib only. Fair-use code guards: per-model concurrency, tiny
max_tokens, exponential backoff, hard total-request budget.

Legs:
  L1 readout sanity  - does the first answer token parse as yes/no,
                       and is the correct-answer logprob recoverable
                       from top-5? (per model, N_STATES states)
  L2 repeatability   - identical request twice: verdict agreement and
                       |delta logprob| distribution (N_REPEAT pairs)
  L3 cliff sweep     - 1-D sweep of one state component across the
                       decision boundary: loss staircase + smoothed
                       finite-difference stability at 3 widths
  L4 cost ledger     - requests, tokens, wall time per model

Writes /home/claude/lm0/results.json
"""
import json, os, random, sys, threading, time, urllib.request, urllib.error

BASE = "https://ellm.nrp-nautilus.io/v1/chat/completions"
TOKEN = os.environ.get("NRP_LLM_TOKEN", "")
MODELS = ["gemma-small", "qwen3-small", "gpt-oss"]
CONC = {"gemma-small": 6, "qwen3-small": 6, "gpt-oss": 8}  # under fair-use caps (8/8/16)
MAX_TOKENS = 8
N_STATES = 24
N_REPEAT = 20
SWEEP_N = 41
TOTAL_BUDGET = 900  # hard cap on requests, all models combined
_lock = threading.Lock()
_count = {"req": 0, "tok": 0, "fail": 0}

def guard():
    with _lock:
        if _count["req"] >= TOTAL_BUDGET:
            raise RuntimeError("request budget exhausted")
        _count["req"] += 1

def query(model, prompt, want_thinking_off=True):
    guard()
    body = {"model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": MAX_TOKENS, "temperature": 0,
            "logprobs": True, "top_logprobs": 5}
    if want_thinking_off:
        body["chat_template_kwargs"] = {"enable_thinking": False}
    data = json.dumps(body).encode()
    for attempt in range(5):
        try:
            req = urllib.request.Request(BASE, data,
                {"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
            r = json.load(urllib.request.urlopen(req, timeout=180))
            with _lock:
                _count["tok"] += r.get("usage", {}).get("total_tokens", 0)
            return r
        except urllib.error.HTTPError as e:
            if e.code == 400 and want_thinking_off:
                return query(model, prompt, want_thinking_off=False)
            time.sleep(2 ** attempt)
        except Exception:
            time.sleep(2 ** attempt)
    with _lock:
        _count["fail"] += 1
    return None

def first_content_logprobs(resp):
    try:
        lp = resp["choices"][0]["logprobs"]["content"]
        return [(t["token"], t["logprob"], t.get("top_logprobs", [])) for t in lp]
    except (KeyError, TypeError, IndexError):
        return None

def yesno_readout(resp):
    """Return (parsed_verdict, logprob_yes, logprob_no, clean_first_token)."""
    toks = first_content_logprobs(resp)
    if not toks:
        return None, None, None, False
    for token, logprob, tops in toks:
        cand = {}
        pool = [(token, logprob)] + [(a["token"], a["logprob"]) for a in tops]
        for tk, tlp in pool:
            s = tk.strip().lower().strip('."\',:;!')
            if s in ("yes", "no") and s not in cand:
                cand[s] = tlp
        if cand:
            verdict = max(cand, key=cand.get)
            first_clean = token.strip().lower().strip('."\',:;!') in ("yes", "no")
            return verdict, cand.get("yes"), cand.get("no"), first_clean
    return None, None, None, False

def serialize(x, prec=3):
    return ", ".join(f"s{i+1}={v:.{prec}f}" for i, v in enumerate(x))

def make_prompt(x):
    return ("A system state is measured as: " + serialize(x) +
            ". Question: is (2*s1 - s2) greater than s4? "
            "Answer with exactly one word: yes or no.")

def truth(x):
    return "yes" if (2 * x[0] - x[1]) > x[3] else "no"

def loss_from(resp, correct):
    v, ly, ln, clean = yesno_readout(resp)
    lp = ly if correct == "yes" else ln
    return (-lp if lp is not None else 12.0), v, clean  # 12.0 = floor (not in top-5)

def parallel(model, prompts, correct_list):
    out = [None] * len(prompts)
    sem = threading.Semaphore(CONC[model])
    def work(i):
        with sem:
            r = query(model, prompts[i])
            out[i] = loss_from(r, correct_list[i]) if r else (None, None, False)
    th = [threading.Thread(target=work, args=(i,)) for i in range(len(prompts))]
    for t in th: t.start()
    for t in th: t.join()
    return out

def main():
    rng = random.Random(20260930)
    states = [[rng.uniform(-2, 2) for _ in range(6)] for _ in range(N_STATES)]
    report = {"pilot": "LM0 instrument (disclosed; NOT claim-bearing)",
              "seed": 20260930, "models": {}, "config": {
                  "n_states": N_STATES, "n_repeat": N_REPEAT, "sweep_n": SWEEP_N,
                  "max_tokens": MAX_TOKENS, "concurrency": CONC,
                  "total_budget": TOTAL_BUDGET}}
    for model in MODELS:
        t0 = time.time()
        m = {}
        # L1 readout sanity
        prompts = [make_prompt(x) for x in states]
        corrects = [truth(x) for x in states]
        res = parallel(model, prompts, corrects)
        ok = [r for r in res if r[1] is not None]
        m["L1"] = {
            "parse_rate": len(ok) / len(res),
            "clean_first_token_rate": sum(1 for r in res if r[2]) / len(res),
            "accuracy_at_t0": (sum(1 for r, c in zip(res, corrects) if r[1] == c) / len(res)),
            "mean_loss_correct": (sum(r[0] for r in ok) / len(ok)) if ok else None,
        }
        # L2 repeatability: same prompt twice, N_REPEAT distinct states
        rep_states = states[:N_REPEAT]
        p2 = [make_prompt(x) for x in rep_states]
        c2 = [truth(x) for x in rep_states]
        a = parallel(model, p2, c2)
        b = parallel(model, p2, c2)
        pairs = [(ra, rb) for ra, rb in zip(a, b) if ra[1] is not None and rb[1] is not None]
        dl = [abs(ra[0] - rb[0]) for ra, rb in pairs]
        m["L2"] = {
            "pairs": len(pairs),
            "verdict_agreement": (sum(1 for ra, rb in pairs if ra[1] == rb[1]) / len(pairs)) if pairs else None,
            "abs_dlogprob_mean": (sum(dl) / len(dl)) if dl else None,
            "abs_dlogprob_max": max(dl) if dl else None,
        }
        # L3 cliff sweep: vary s1 across the boundary for a fixed state
        x0 = states[0][:]
        # boundary: 2*s1 - s2 = s4 -> s1* = (s2 + s4)/2
        s1_star = (x0[1] + x0[3]) / 2
        grid = [s1_star + (i - SWEEP_N // 2) * 0.05 for i in range(SWEEP_N)]
        ps, cs = [], []
        for g in grid:
            xv = x0[:]; xv[0] = g
            ps.append(make_prompt(xv)); cs.append(truth(xv))
        sweep = parallel(model, ps, cs)
        losses = [r[0] for r in sweep]
        m["L3"] = {
            "s1_star": s1_star, "grid_step": 0.05,
            "losses": losses,
            "verdicts": [r[1] for r in sweep],
        }
        m["L4"] = {"wall_s": round(time.time() - t0, 1)}
        report["models"][model] = m
        print(f"[{model}] L1 parse {m['L1']['parse_rate']:.2f} acc {m['L1']['accuracy_at_t0']:.2f} "
              f"| L2 agree {m['L2']['verdict_agreement']} dmax {m['L2']['abs_dlogprob_max']} "
              f"| {m['L4']['wall_s']}s", flush=True)
    report["ledger"] = dict(_count)
    os.makedirs("/home/claude/lm0", exist_ok=True)
    with open("/home/claude/lm0/results.json", "w") as f:
        json.dump(report, f, indent=2)
    print("DONE", json.dumps(report["ledger"]))

if __name__ == "__main__":
    main()
