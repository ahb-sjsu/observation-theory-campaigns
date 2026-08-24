# XPROTO-CSI — RFsim substrate

The sealed substrate for the CSI-aging cell: a full 5G PHY + link
adaptation + HARQ over a modeled time-varying channel, **no SDR
hardware**. The software half (`fam_csi.py` simulator + grading,
`csi_check.py`) is built and validated; this is what the sealed run uses.

## Substrate as run (2026-08-22): MATLAB real-fading, NOT 5G-standard

Atlas's MATLAB has **Communications Toolbox + DSP System Toolbox but NOT
5G Toolbox** (nor the 6G Exploration Library) — verified by license check.
So a *3GPP-standard* NR RFsim is not available in MATLAB here. The
shakedown therefore ran on `csi_shakedown.m` using
**`comm.RayleighChannel` (real Jakes Doppler fading)** + adaptive
modulation/coding + a link-level BLER model + HARQ — the PHY *mechanism*
behind CQI aging, one step MORE real than the Python AR(1) sim (a true
Jakes process, not an AR(1) approximation), one step LESS than a
standard-compliant NR PHY. Result (`CSIREP-family.json`, mode
`matlab_fading`, seeds {0,1,2}): naive BLER ~0.35 vs OLLA ~0.10 vs fresh
~0.09; `--check-family` **PASS** on all bars + MCs.

**Honest ladder of substrates for this cell**, weakest→strongest external
validity: Python AR(1) sim (code validation) → MATLAB real Jakes fading
(real channel, modeled decoder) → clean-room NR link-to-system (`nr_link.py`
— real 3GPP tables + MIESM/RBIR, modeled decoder) → **Sionna real 5G NR
PHY (SEALED SUBSTRATE — real 5G LDPC decode + 3GPP TDL, below)** →
srsRAN/OAI RFsim (system-level NR + real scheduler) → over-the-air. The
seal names the substrate it runs on; the Sionna rung is the first with a
*real NR decoder*, which is what "5G-standard" needs.

## Sionna — real 5G NR PHY (the SEALED substrate, 2026-08-22)

`csi_sionna.py` runs on Atlas GPU 1 in `/home/claude/sionna-venv`
(**NVIDIA Sionna 1.2.2**, open source, Apache-2.0; TensorFlow 2.21, CUDA
12.9 bundled — isolated from the system CUDA/torch). It is standard-
compliant NR PHY at the link level, exactly this cell's level:

- **Real 5G LDPC** (`LDPC5GEncoder`/`LDPC5GDecoder`, TS 38.212, 20 iters) +
  real Gray M-QAM (`Mapper`/`Demapper`, APP LLRs) → a **real BLER(SNR)
  curve per MCS** measured over AWGN (batched Monte Carlo on the GV100),
  cached to `nr_bler_curves_sionna.npz`. This is a *real NR decoder*, not a
  model. (5G LDPC floors the code rate at 1/5, so the two lowest CQI
  entries — reached via repetition in real NR — are dropped; the MCS set is
  a 13-entry span of TS 38.214 Table 5.1.3.1-1 with R≥0.30.)
- **Real 3GPP channel** — TR38.901 **TDL-A** (`sionna.phy.channel.tr38901`)
  at f_d = 200 Hz (v = 17.1 m/s @ 3.5 GHz), narrowband SISO gain per TTI →
  the CSI-aging dynamics.
- **3GPP link-to-system**: per TTI, HARQ ACK/NACK is drawn from the real
  per-MCS BLER curve at the *actual aged* SNR (the standard, unbiased way
  to measure a policy's false-clear rate; not a shortcut). Full per-block
  per-TTI decoding is a later fidelity rung.

Shakedown (`CSIREP-family.json`, mode `nrsionna`, seeds {0,1,2}):
naive ~0.36 / OLLA ~0.10 / fresh ~0.11, cqi_err ~5.5 dB, mcs_var 11–12;
`csi_check.py --check-family` **PASS** all bars + MCs. GPU 0 (Erebus)
untouched throughout (`CUDA_VISIBLE_DEVICES=1`).

## srsRAN / OAI RFsim (the system-level NR substrate)

## Stack (software only)

| item | role | note |
|---|---|---|
| **srsRAN Project** (gNB) + **srsUE**, ZMQ RF, OR **OpenAirInterface** `--rfsim` | full 5G NR gNB+UE in software | no USRP; the RF is virtual |
| a time-varying channel | induces CSI aging | OAI RFsim channel models (e.g. `TDL` with a Doppler/UE-speed) or srsRAN's ZMQ channel emulator (e.g. GNU Radio between the ZMQ endpoints) |
| iperf / DL traffic | keeps the DL scheduler + link adaptation busy | so CQI→MCS is exercised continuously |

Everything runs on one host (Atlas). No RF, no regulatory exposure —
unlike the CCA cell, this cell needs only compute.

## Inducing aging (the regime)

Set the channel's **maximum Doppler / UE speed** high enough that the
coherence time is short relative to the CSI report period:
- OAI RFsim: a TDL profile with a UE speed (e.g. 100–200 km/h at FR1) or an
  explicit `max_doppler`; CSI/CQI reporting period from the gNB config.
- srsRAN: drive the ZMQ samples through a Jakes/TDL fading block with the
  target Doppler.
Target the same corner as the sim (f_d ~ 200 Hz, report period ~ 20 ms) so
`cqi_err_db` (MC1) is comfortably ≥ 2 dB and `fresh_bler` (MC2, a
short-report control) stays ≤ 0.15.

## The three policy runs (per seed)

Per graded seed, run three configurations over the same channel seed:
- **naive** — link adaptation using the raw CQI (OLLA off, if the stack
  allows disabling it; else a fixed CQI→MCS offset).
- **olla** — outer-loop link adaptation ON (srsRAN/OAI both implement it).
- **fresh** — CSI report period = 1 slot (aging removed) — the control.

Both stacks expose per-transmission MCS + HARQ ACK/NACK in their metrics/
logs (srsRAN `--metrics`, MAC/PHY logs; OAI T-tracer / nrL1/nrMAC logs).

## Log schema (what `fam_csi.load_rfsim` reads)

Per seed and policy: `rfsim/seed_<seed>/<policy>/tx.jsonl`, one row per DL
transmission:

```
{"cqi": <int>, "mcs": <int>, "ack": true|false}
```

`<policy>` ∈ {`naive`, `olla`, `fresh`}. BLER = NACK fraction. (Log the
reported vs realized SINR too, if available, to compute `cqi_err_db`
directly for MC1; otherwise MC1 is asserted from the configured f_d ×
report period.) A small adapter turns the stack's native metrics
(CSV/JSON) into these `tx.jsonl` files.

## Procedure (shakedown → seal)

1. Bring up gNB+UE (RFsim) + the fading channel; confirm DL traffic flows
   and MCS varies.
2. **Shakedown** seeds {0,1,2}: run the three policies, emit
   `CSIREP-family.json` (mode `rfsim`), iterate until
   `csi_check.py --check-family` PASSes. Expect stack surprises (OLLA
   on/off knobs; how to read HARQ; channel-model Doppler units).
3. **Seal** (fresh day, ≥ 2026-08-23): flip the prereg STATUS, commit,
   run graded seeds {20260823-25}, `csi_check.py` → commit
   `XPROTO-CSI-graded.json` as executed.

A PASS is the first measured 5G CQI-aging false-clear rate + the
HARQ-witnessed reduction — the cellular entry in the vacuity taxonomy,
and the empirical anchor for the 6G exploration (AI-native CSI, the
turboquant-pro→CSI-compression bridge, cell-free = geo-fleet routing).
