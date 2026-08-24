"""XPROTO-CCA witness capture — RX-only IQ from the ADALM-Pluto tapped at
the Rx port. The independent witness: it records the RF the receiver
actually saw, so collision_detect.py can establish whether an interferer
was present at Rx during each of A's frames (collision vs weak-signal).

Runs on the bench (needs pyadi-iio + a Pluto). Saves an int16 IQ block
plus a meta.json with the reference-clock t0 and sample rate; offline
alignment (MC4) uses the shared 10 MHz/PPS reference and a marker frame.

    python3 witness_capture.py --uri ip:192.168.2.1 --seconds 20 \
        --out hw/seed_20260822/cca
"""

from __future__ import annotations

import argparse
import json
import os
import time

import numpy as np


def capture(uri: str, seconds: float, out_dir: str,
            fc_hz: int = 2_437_000_000, fs_hz: int = 20_000_000,
            gain_db: float = 40.0) -> None:
    import adi  # pyadi-iio; bench-only dependency

    sdr = adi.Pluto(uri=uri)
    sdr.rx_lo = int(fc_hz)
    sdr.sample_rate = int(fs_hz)
    sdr.rx_rf_bandwidth = int(fs_hz)
    sdr.gain_control_mode_chan0 = "manual"
    sdr.rx_hardwaregain_chan0 = float(gain_db)
    sdr.rx_buffer_size = 2 ** 18

    os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()                    # host clock; PPS gives the fine edge
    blocks = []
    n_target = int(seconds * fs_hz)
    got = 0
    while got < n_target:
        x = sdr.rx()                    # complex64
        blocks.append(x.astype(np.complex64))
        got += len(x)
    iq = np.concatenate(blocks)[:n_target]

    # store as interleaved int16 to keep it compact
    i16 = np.empty(iq.size * 2, dtype=np.int16)
    i16[0::2] = np.clip(np.real(iq), -32768, 32767).astype(np.int16)
    i16[1::2] = np.clip(np.imag(iq), -32768, 32767).astype(np.int16)
    i16.tofile(os.path.join(out_dir, "witness_iq.int16"))
    json.dump({"t0": t0, "sample_rate": fs_hz, "rx_lo": fc_hz,
               "n_samples": int(iq.size), "format": "int16 interleaved I,Q"},
              open(os.path.join(out_dir, "witness_meta.json"), "w"), indent=1)
    print(f"captured {iq.size} samples ({iq.size/fs_hz:.1f}s) -> {out_dir}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--uri", default="ip:192.168.2.1")
    ap.add_argument("--seconds", type=float, default=20.0)
    ap.add_argument("--out", required=True, help="hw/seed_<n>/<cond> dir")
    ap.add_argument("--fc", type=int, default=2_437_000_000)
    ap.add_argument("--fs", type=int, default=20_000_000)
    ap.add_argument("--gain", type=float, default=40.0)
    a = ap.parse_args()
    capture(a.uri, a.seconds, a.out, a.fc, a.fs, a.gain)


if __name__ == "__main__":
    main()
