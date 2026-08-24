# XPROTO-CCA — RF bench harness

The hardware half of the CCA cell: what to assemble, how to instrument
it, and the on-disk log schema that `fam_cca.load_hw_logs` reads. The
software half (`fam_cca.py` grading + simulator, `cca_check.py`) is built
and validated; this is the part that needs a bench. Scoping rationale:
`../../../geometric-observation/docs/cca-cell-scoping.md`.

## Bill of materials

| item | qty | role | note |
|---|---|---|---|
| ADALM-Pluto (or USRP B210) | 2 | A (Tx) + Rx, running `gr-ieee802-11` | need observable CCA → SDR MAC |
| ADALM-Pluto | 1 | **W** — RX-only witness at the Rx port | 2.4 GHz native, 20 MHz |
| SDR (Pluto/USRP) | 1 | **C** — hidden interferer (OFDM/802.11 bursts) | |
| SMA cables, 50 Ω | ~6 | conducted RF paths | |
| step attenuators (0–60 dB) | 3 | set A↔C (high), C→Rx, A→Rx | the "hidden" relationship |
| power combiner + splitter (2.4 GHz) | 1 ea | mix A+C into Rx; tap Rx→W | |
| 10 MHz + PPS reference / distribution | 1 | shared clock for A/Rx/C/W | time alignment (MC4) |

Conducted (cabled) — **no over-the-air emission**. That removes
regulatory exposure, makes the hidden relationship a *set* attenuator
quantity (not geometry), and makes runs reproducible. OTA is a later
external-validity cell, not this one.

## Wiring

```
 A ─[att_A]─┐
            ├─ combiner ─ splitter ─┬─> Rx
 C ─[att_C]─┘                       └─> W (Pluto witness)
```

Set attenuators so: (1) the A↔C coupling seen at A is **below A's CCA
threshold** (A cannot sense C → MC1); (2) C→Rx is a **colliding** level
(C reaches Rx → MC2); (3) A→Rx decodes cleanly when C is silent (clean
link → MC3). Calibrate by sweeping `att_A` up until A's CCA-clear rate
during C bursts exceeds 0.8, and `att_C` until the witness sees C on
≥0.8 of overlapping frames while clean-link decode stays ≥0.9.

## Radios / flowgraphs

- **A, Rx**: `gr-ieee802-11` (Bloessl) 802.11a/g OFDM transceiver, 2.4 GHz,
  low-mid MCS (6–24 Mbps — within the AD9363/Pluto 20 MHz envelope). A's
  flowgraph must **log its CCA decision per transmission opportunity**
  (the carrier-sense / energy block output) → `a_log.jsonl`. Rx logs
  per-frame decode success → `rx_log.jsonl`. Both stamp frames with a
  monotonic `frame_id` and a reference-clock timestamp.
- **C**: scheduled OFDM/802.11 bursts on the same channel; log burst
  on/off edges → `c_log.jsonl`. The seed drives the schedule.
- **W (witness)**: RX-only IQ capture at the Rx port, reference-clocked →
  `witness_capture.py`. Offline, `collision_detect.py` turns the IQ +
  A's frame schedule into `witness.jsonl` (per A-frame: was C energy
  present at Rx during the frame's airtime).

Each seed is run **twice**: `cca` (RTS/CTS off) and `rtscts` (on). In the
RTS/CTS condition A does the RTS/CTS handshake; C, hearing Rx's CTS,
should defer — the witness then shows no concurrent energy for those
frames (the measured reduction).

## Time alignment (MC4)

All four SDRs share the 10 MHz + PPS reference so their sample clocks are
locked; PPS gives coarse alignment. Residual alignment between the
witness capture and A's frame schedule is measured by cross-correlating a
known A marker frame present in W's IQ against A's logged TX time; the
residual must be ≤ one OFDM symbol (≈ 4 µs) or the run VOIDs (MC4). If a
shared reference is unavailable, embed a periodic marker and align by
correlation offline.

## On-disk log schema (what `fam_cca.load_hw_logs` reads)

Per seed and condition: `hw/seed_<seed>/<cond>/` with `<cond>` ∈
{`cca`, `rtscts`}:

```
a_log.jsonl     {"t": <ref-clock s>, "cca_clear": true/false, "frame_id": <int>}
c_log.jsonl     {"t_start": <s>, "t_end": <s>}
rx_log.jsonl    {"frame_id": <int>, "decoded": true/false}
witness.jsonl   {"frame_id": <int>, "concurrent": true/false}
```

`a_log` has one row per A transmission *opportunity* (whether or not CCA
was clear); `rx_log`/`witness` cover the frames A actually sent
(`cca_clear=true`). `collision_detect.py` produces `witness.jsonl`.

## Bench procedure (shakedown → seal)

1. Assemble + calibrate attenuators (above); confirm MC1/MC2/MC3 hold on
   a scratch run.
2. **Shakedown**: run seeds {0,1,2} (bench), write `CCAREP-family.json`
   (same record shape as `fam_cca` emits, `mode:"hw"`). Iterate the bench
   until the family record passes `cca_check.py --check-family`. Expect
   instrument surprises (as the DB and MG cells had) — attenuator
   calibration, CCA-log semantics, witness threshold, clock residual.
3. **Seal** (fresh day, ≥ 2026-08-22): flip the prereg STATUS, commit,
   then `cca_check.py` on graded seeds {20260822-24} (`mode:"hw"`),
   commit `XPROTO-CCA-graded.json` as executed.

A PASS is the first measured 802.11 CCA false-clear rate + the RTS/CTS
reduction — the number that replaces the illustrative example in
`draft-bond-ot80211-freshness`.
