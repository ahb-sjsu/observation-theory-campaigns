# PREREG-XPROTO-QOT — consumer-relative QoT-certificate vacuity in optical networks

**STATUS: UNSEALED.** FAMILY-CONSTRUCTED: 2026-08-24. Earliest compliant seal
**2026-08-25** (`qot_check.py` codes the cooling-off). Graded seeds {20260825,
20260826, 20260827}, disjoint from the shakedown's {0,1,2}. Substrate = **GNPy**
(the optical-networking-standard GN-model QoT engine) — the evidence rung, as
Sionna is for the cellular cells.

**IP posture:** public methodology; the optical-networking instance of the
witnessed-freshness-certificate grammar. Nothing gated. **Venue:** targets OFC 2027
(deadline 2026-10-20; student/early-career prize eligible).

## The claim

Before provisioning a lightpath an operator computes a **QoT (GSNR) estimate** and
selects the highest modulation format it clears — a **certificate** ("this
lightpath meets its FEC threshold at format X"). The estimate is made under the
**reference channel loading** (the band as provisioned). As neighbouring channels
are added, nonlinear interference grows and the real GSNR drops: the certificate
**false-clears** — the provisioned format now fails its FEC threshold. The
false-clear is **consumer-relative**: whether a lightpath crosses its threshold
depends on its **footprint** (spectral position + reach), so a blanket margin is
adequate for one lightpath and catastrophic for another. A **consumer-aware**
certificate (QoT under the actual loading footprint) holds. Margins are the price
of the un-witnessed certificate; the false-clear rate is the number that sets how
much margin can be safely removed (recovered capacity).

## Family F-QOT (constructed + shaken down 2026-08-24)

GNPy `gn_model_analytic` NLI over an SSMF (0.2 dB/km, D=17 ps/nm/km) + EDFA
(NF 6 dB) line system, 80 km spans, +2 dBm/ch launch, 32 GBd / 50 GHz grid.
Reference loading = 6 channels (sparse initial provisioning); actual = full 76-ch
C-band. Consumers = `K=60` lightpaths, each (spectral position p∈[0,1], reach
∈{4..16} spans). Witness = true GSNR under full loading. naive certificate =
GSNR under reference loading (+ 0.3 dB monitoring noise) → select format with a
1 dB design margin; aware = GSNR under actual loading. Required GSNR per format
(declared): QPSK 6.5, 8QAM 9.0, 16QAM 12.5, 32QAM 16.0, 64QAM 19.0 dB.

## Bars (bind at seal; checked against the family record first)

*Demonstrated (seeds {0,1,2}): naive_fc ≈ 0.40, aware_fc = 0.0, loading penalty
≈ 2.6 dB, fc_spread ≈ 0.49.*

- **B1 — QoT-cert vacuity.** Per seed: `naive_fc ≥ 0.25`.
- **B2 — footprint-aware holds.** Per seed: `aware_fc ≤ 0.10`.
- **B3 — dominance.** Per seed: `aware_fc ≤ naive_fc / 2`.

**Manipulation checks (bars too):**
- **MC1 — the certificate genuinely ages.** `mean_loading_penalty_db ≥ 0.5` (the
  reference→actual loading really degrades GSNR; if it doesn't there is no story).
- **MC2 — consumer-relativity.** `fc_spread ≥ 0.10` (both false-clears AND clears
  exist — the vacuity is a footprint property, not uniform; a blanket margin
  cannot be right for all).
- **MC3 — non-degenerate.** `n_paths ≥ 30`, `mean_bits_per_symbol_aware ≥ 2` (the
  aware policy delivers real capacity, not a degenerate all-fail / all-QPSK pass).

**Verdict:** any MC fail → VOID; all MCs + B1–B3 every seed → PASS; else FAIL,
kept. **Kills:** `naive_fc < 0.15` (no QoT vacuity in this regime) or `aware_fc >
0.20` (the footprint certificate does not hold).

## Seal procedure

On 2026-08-25+: confirm `QOTREP-family.json` PASSes `--check-family`, reread, flip
STATUS to SEALED, commit; run `fam_qot.py --seeds 20260825 20260826 20260827 --out
QOTREP-graded-raw.json`, `qot_check.py` → commit `XPROTO-QOT-graded.json`.

## Scope

GNPy's GN model is the field-standard **analytical** NLI model (Gaussian-noise
assumption); it is the evidence rung as Sionna is for the cellular cells. External
-validity graduations (declared, not claimed here): a coherent-receiver **pre-FEC
BER** witness on a fibre testbed / field trace; the split-step or EGN model as a
higher-fidelity reference; real ROADM/EDFA gain-ripple and add/drop dynamics. The
credited prior art is margin reduction via ML-QoT and physical-layer-aware RSA;
OT's delta is the **measured, consumer-relative, footprint-witnessed false-clear
rate** as a first-class number, and the refresh floor from add/drop churn.

## Provenance

- Exploration: the OFC 2027 CFP — QoT/margins as the optical instance of the
  witnessed-freshness-certificate grammar.
- Family + grading: `fam_qot.py` (GNPy substrate) + `qot_check.py` (seal-guard +
  coded cooling-off + GNPy-only sealed grading + pre-seal record check).
