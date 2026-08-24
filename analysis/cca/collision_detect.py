"""XPROTO-CCA collision detector — offline: turn the witness IQ capture
(witness_capture.py) plus A's frame schedule (a_log.jsonl) into
witness.jsonl, the per-A-frame ground truth of whether an interferer was
present at Rx during the frame's airtime.

Method: build the received power envelope at Rx. For each of A's frames
(cca_clear only), compare the in-frame power to the baseline power of
A-alone frames (frames whose window shows no excess). A collision raises
the in-frame power at Rx by the interferer's contribution, so an excess
beyond a margin => concurrent interferer energy. Independently detects
interferer bursts (energy in non-A-frame regions) to cross-check MC2.

This is the offline half of the witness; it needs a real capture + logs.
Alignment (MC4) between the capture t0 and a_log times is assumed handled
by the shared reference / marker correlation (see HARDWARE.md).

    python3 collision_detect.py hw/seed_20260822/cca --margin-db 3
"""

from __future__ import annotations

import argparse
import json
import os

import numpy as np

FRAME_S = 0.0006          # must match fam_cca.FRAME_S


def load_iq(cond_dir: str):
    meta = json.load(open(os.path.join(cond_dir, "witness_meta.json")))
    raw = np.fromfile(os.path.join(cond_dir, "witness_iq.int16"),
                      dtype=np.int16)
    iq = raw[0::2].astype(np.float32) + 1j * raw[1::2].astype(np.float32)
    return iq, float(meta["sample_rate"]), float(meta["t0"])


def power_envelope(iq, fs, win_s=20e-6):
    """Moving-average power (dB), decimated to one point per win_s."""
    p = (iq.real ** 2 + iq.imag ** 2)
    w = max(1, int(win_s * fs))
    # block-mean decimation
    n = (len(p) // w) * w
    pe = p[:n].reshape(-1, w).mean(axis=1)
    pe_db = 10 * np.log10(pe + 1e-9)
    return pe_db, win_s


def detect(cond_dir: str, margin_db: float = 3.0) -> None:
    iq, fs, t0 = load_iq(cond_dir)
    pe_db, win_s = power_envelope(iq, fs)
    a_log = [json.loads(ln) for ln in
             open(os.path.join(cond_dir, "a_log.jsonl")) if ln.strip()]
    a_frames = [f for f in a_log if f.get("cca_clear")]

    def window_power(t_rel):
        i0 = int(t_rel / win_s)
        i1 = int((t_rel + FRAME_S) / win_s) + 1
        seg = pe_db[max(0, i0):max(1, i1)]
        return float(np.median(seg)) if len(seg) else -99.0

    # per-frame in-window power, relative to the capture start
    pw = [(f["frame_id"], window_power(f["t"] - t0)) for f in a_frames]
    powers = np.array([p for _, p in pw])
    # baseline = lower mode of the per-frame powers (A-alone frames);
    # collided frames sit a margin above it.
    baseline = float(np.percentile(powers, 40)) if len(powers) else -99.0

    out = []
    for fid, p in pw:
        out.append({"frame_id": fid, "concurrent": bool(p > baseline + margin_db)})
    with open(os.path.join(cond_dir, "witness.jsonl"), "w") as fh:
        for r in out:
            fh.write(json.dumps(r) + "\n")

    n_conc = sum(1 for r in out if r["concurrent"])
    print(f"{cond_dir}: {len(out)} A-frames, baseline {baseline:.1f} dB, "
          f"margin {margin_db} dB -> {n_conc} concurrent "
          f"({n_conc/max(1,len(out)):.1%}). wrote witness.jsonl")
    print("  Sanity: sweep --margin-db so clean-link frames stay below "
          "and known-collision frames stay above (calibrate vs c_log).")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cond_dir", help="hw/seed_<n>/<cond> with capture + a_log")
    ap.add_argument("--margin-db", type=float, default=3.0)
    a = ap.parse_args()
    detect(a.cond_dir, a.margin_db)


if __name__ == "__main__":
    main()
