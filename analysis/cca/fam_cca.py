"""XPROTO-CCA family (F-CCA): measurement/grading core + a synthetic
hidden-node SIMULATOR for validating the grading logic before hardware.

The vacuity taxonomy's first PHY cell (see draft-bond-ot80211-freshness).
Certificate = 802.11 CCA ("medium idle -> transmit"), issued at the
transmitter A; consumer = the receiver Rx; false-clear = A's CCA reported
clear, A transmitted, and Rx failed BECAUSE a station A could not sense
(the hidden node C) transmitted concurrently and collided at Rx. The
independent witness is an ADALM-Pluto at the Rx port that establishes
whether C's energy was actually present at Rx (collision vs weak-signal).

The cell grades TWO conditions per seed and compares them (the RFC's
comparative claim): CCA-alone (naive) vs RTS/CTS-enabled (witnessed —
the CTS silences C if it can hear Rx). Bars grade the false-clear rate.

TWO run modes:
  * mode="sim": generate synthetic A/C/Rx/witness logs from the
    hidden-node model, then grade. This validates the grading CODE and
    calibrates the bars. **It is NOT evidence about real 802.11** — it is
    a unit test of the instrument. cca_check.py refuses to seal on sim.
  * mode="hw":  read the four real logged streams from the RF bench
    (see HARDWARE.md) and grade. This is the sealed measurement.

    python3 fam_cca.py --sim              # grading-logic validation, seeds 0 1 2
    python3 fam_cca.py --sim --seeds 7 8  # exploration
"""

from __future__ import annotations

import argparse
import bisect
import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- sealed cell constants (bars reference these; do not tune) -------
DURATION_S = 20.0
FRAME_S = 0.0006          # ~1500 B @ 24 Mbps + overhead
A_RATE = 200.0           # A frames/s (offered)
C_DUTY = 0.30            # fraction of time the hidden node C is on
C_BURST_S = (0.002, 0.010)   # C burst length band

# hidden-node physics (the regime the MCs verify was actually realized)
P_A_SENSES_C = 0.03     # A's CCA detects a concurrent C (LOW = hidden)
P_CTS_HEARD = 0.90      # C hears Rx's CTS and defers (C<->Rx path exists)
P_FAIL_ON_COLLISION = 0.95   # a real collision breaks Rx decode
P_FAIL_CLEAN = 0.03          # clean-link loss (SNR), no interferer


def _c_intervals(rng: random.Random) -> list[tuple[float, float]]:
    """Poisson-ish on/off schedule for the hidden node C over the run,
    targeting duty C_DUTY."""
    ivals, t = [], 0.0
    while t < DURATION_S:
        burst = rng.uniform(*C_BURST_S)
        ivals.append((t, min(t + burst, DURATION_S)))
        gap = burst * (1.0 - C_DUTY) / C_DUTY
        t += burst + rng.expovariate(1.0 / max(gap, 1e-4))
    return ivals


def _overlaps(starts: list[float], ends: list[float],
              a: float, b: float) -> bool:
    """Does [a,b] overlap any C interval? starts sorted."""
    i = bisect.bisect_right(starts, b) - 1
    while i >= 0 and ends[i] >= a:
        if starts[i] <= b and ends[i] >= a:
            return True
        i -= 1
        if i >= 0 and ends[i] < a - C_BURST_S[1]:
            break
    return False


def simulate_scenario(seed: int, rts_cts: bool) -> dict:
    """Generate the four logged streams for one condition. Returns
    per-A-frame records with the witness truth, plus C's schedule."""
    rng = random.Random(seed * 7919 + (1 if rts_cts else 0))
    c_iv = _c_intervals(rng)
    c_starts = [s for s, _ in c_iv]
    c_ends = [e for _, e in c_iv]

    frames = []
    t = 0.0
    period = 1.0 / A_RATE
    while t < DURATION_S:
        # A's CCA at t: senses C only if C is on now AND A can hear it
        c_now = _overlaps(c_starts, c_ends, t - 1e-5, t)
        cca_clear = not (c_now and rng.random() < P_A_SENSES_C)
        rec = {"t": round(t, 6), "cca_clear": cca_clear}
        if cca_clear:
            # concurrent C during the frame airtime = the witness truth,
            # UNLESS RTS/CTS silenced C for this frame.
            concurrent = _overlaps(c_starts, c_ends, t, t + FRAME_S)
            if rts_cts and concurrent and rng.random() < P_CTS_HEARD:
                concurrent = False          # C heard CTS and deferred
            rec["concurrent"] = concurrent   # what the Pluto witness sees
            p_fail = P_FAIL_ON_COLLISION if concurrent else P_FAIL_CLEAN
            rec["decoded"] = rng.random() >= p_fail
        frames.append(rec)
        t += period
    return {"frames": frames, "c_intervals": c_iv,
            "condition": "rtscts" if rts_cts else "cca"}


def grade_condition(logs: dict) -> dict:
    """Per-condition rates + the raw counts the MCs need."""
    fr = logs["frames"]
    clear = [f for f in fr if f["cca_clear"]]
    n_clear = len(clear)
    # false-clear: CCA said clear, A transmitted, Rx failed, witness saw C
    fc = sum(1 for f in clear if not f["decoded"] and f["concurrent"])
    fc_rate = fc / n_clear if n_clear else 0.0
    # witness-confirmed collision opportunities + clean-link sanity
    n_concurrent = sum(1 for f in clear if f["concurrent"])
    clean = [f for f in clear if not f["concurrent"]]
    clean_decode = (sum(1 for f in clean if f["decoded"]) / len(clean)
                    if clean else 0.0)
    return {"n_clear": n_clear, "fc": fc, "fc_rate": round(fc_rate, 4),
            "n_concurrent": n_concurrent,
            "clean_decode_rate": round(clean_decode, 4)}


def _hidden_and_witness_mcs(logs_cca: dict) -> dict:
    """MC1 (A can't sense C) + MC2 (C reaches Rx), from the CCA-alone run
    where the witness truth is unmodified by CTS."""
    fr = logs_cca["frames"]
    c_iv = logs_cca["c_intervals"]
    c_starts = [s for s, _ in c_iv]
    c_ends = [e for _, e in c_iv]
    # sample A opportunities that fell during a C burst
    during_c = [f for f in fr
                if _overlaps(c_starts, c_ends, f["t"] - 1e-5, f["t"])]
    a_clear_during_c = (sum(1 for f in during_c if f["cca_clear"])
                        / len(during_c) if during_c else 1.0)
    # witness detection: fraction of A frames overlapping C that the
    # witness flags concurrent (in sim, the witness is exact -> ~1.0)
    clear = [f for f in fr if f["cca_clear"]]
    frames_over_c = [f for f in clear
                     if _overlaps(c_starts, c_ends, f["t"], f["t"] + FRAME_S)]
    witness_detect = (sum(1 for f in frames_over_c if f["concurrent"])
                      / len(frames_over_c) if frames_over_c else 0.0)
    return {"a_clear_during_c": round(a_clear_during_c, 4),
            "witness_detect": round(witness_detect, 4)}


def run_cell(seed: int, mode: str = "sim") -> dict:
    if mode == "sim":
        logs_cca = simulate_scenario(seed, rts_cts=False)
        logs_rts = simulate_scenario(seed, rts_cts=True)
    elif mode == "hw":
        logs_cca, logs_rts = load_hw_logs(seed)   # HARDWARE.md format
    else:
        raise ValueError(mode)

    g_cca = grade_condition(logs_cca)
    g_rts = grade_condition(logs_rts)
    mc = _hidden_and_witness_mcs(logs_cca)
    return {
        "seed": seed, "mode": mode,
        "fc_cca": g_cca["fc_rate"],          # naive certificate false-clear
        "fc_rtscts": g_rts["fc_rate"],       # witnessed alternative
        "n_clear": g_cca["n_clear"],
        "n_concurrent": g_cca["n_concurrent"],
        "clean_decode_rate": g_cca["clean_decode_rate"],
        "a_clear_during_c": mc["a_clear_during_c"],   # MC1
        "witness_detect": mc["witness_detect"],       # MC2
        "witness_aligned": True if mode == "sim" else None,  # MC4 (hw: xcorr)
    }


def load_hw_logs(seed: int, root: str | None = None):
    """Read the four bench-logged streams for a graded seed (both the
    CCA-alone and RTS/CTS conditions) and rebuild the per-frame records
    grade_condition() expects. Log schema (JSONL, see HARDWARE.md):
      hw/seed_<seed>/<cond>/a_log.jsonl   {"t","cca_clear","frame_id"}
                            /c_log.jsonl   {"t_start","t_end"}
                            /rx_log.jsonl  {"frame_id","decoded"}
                            /witness.jsonl {"frame_id","concurrent"}  (from
                              collision_detect.py over the Pluto capture)
    where <cond> is "cca" and "rtscts". Raises if the logs are absent."""
    base = os.path.join(root or os.path.join(HERE, "hw"), f"seed_{seed}")

    def _jsonl(path):
        with open(path, encoding="utf-8") as fh:
            return [json.loads(ln) for ln in fh if ln.strip()]

    def load_cond(cond):
        d = os.path.join(base, cond)
        if not os.path.isdir(d):
            raise FileNotFoundError(
                f"hardware logs missing: {d} — run the RF bench (HARDWARE.md)")
        a = _jsonl(os.path.join(d, "a_log.jsonl"))
        c = _jsonl(os.path.join(d, "c_log.jsonl"))
        rx = {r["frame_id"]: bool(r["decoded"])
              for r in _jsonl(os.path.join(d, "rx_log.jsonl"))}
        wit = {w["frame_id"]: bool(w["concurrent"])
               for w in _jsonl(os.path.join(d, "witness.jsonl"))}
        frames = []
        for e in a:
            f = {"t": e["t"], "cca_clear": bool(e["cca_clear"])}
            if f["cca_clear"]:
                fid = e["frame_id"]
                f["concurrent"] = wit.get(fid, False)
                f["decoded"] = rx.get(fid, False)
            frames.append(f)
        c_iv = [(x["t_start"], x["t_end"]) for x in c]
        return {"frames": frames, "c_intervals": c_iv, "condition": cond}

    return load_cond("cca"), load_cond("rtscts")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sim", action="store_true",
                    help="grading-logic validation on synthetic scenarios "
                         "(NOT evidence about real 802.11)")
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default="CCA-SIM-validation.json")
    args = ap.parse_args()
    mode = "sim" if args.sim else "hw"
    cells = []
    for seed in args.seeds:
        c = run_cell(seed, mode=mode)
        cells.append(c)
        print(f"seed {seed}: fc_cca={c['fc_cca']} fc_rtscts={c['fc_rtscts']} "
              f"n_clear={c['n_clear']} n_conc={c['n_concurrent']} "
              f"clean_decode={c['clean_decode_rate']} "
              f"MC1_a_clear_during_c={c['a_clear_during_c']} "
              f"MC2_witness={c['witness_detect']}", flush=True)
    rec = {"family": "F-CCA", "mode": mode,
           "sim_is_code_validation_not_evidence": (mode == "sim"),
           "constants": {"duration_s": DURATION_S, "frame_s": FRAME_S,
                         "a_rate": A_RATE, "c_duty": C_DUTY},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
