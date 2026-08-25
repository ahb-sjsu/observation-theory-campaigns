# Traffic / optical-monitoring datasets — survey for grounding XPROTO-QOT

Purpose: a real anchor for the OFC paper — (i) **heterogeneous fill** from a real
demand matrix (so the uniform-margin baseline is steelmanned, not synthetic), and
ideally (ii) a **real signal-quality witness** (measured GSNR/Q-factor over time) to
graduate off the GN-model evidence rung.

## Demand / traffic-matrix datasets (ground the fill distribution)

| Dataset | What it is | Fit for XPROTO-QOT | Access |
|---|---|---|---|
| **SNDlib** (Survivable Network Design Library) | Real topologies + **demand matrices** (nobel-us, janos-us-ca, germany50, cost266, geant, atlanta, …) | **Best for fill**: a US backbone with real demands → per-route channel count → heterogeneous fill. Optical-planning standard. | Open, sndlib.zib.de (XML/native) |
| **Abilene / Internet2** | Real OD traffic matrices, 12 nodes, 5-min, 6 mo (2004) | US backbone, real measured TM → heterogeneous per-OD load; smaller than CORONET | Open (TOTEM project, IEEE DataPort) |
| **GÉANT** | Real OD TMs, 23 nodes, 15-min, 4 mo, XML | European R&E backbone, real TM; pairs well with Abilene as a 2nd network | Open (TOTEM, IEEE DataPort) |
| **Internet Topology Zoo / TopoHub** | Topologies (incl. CORONET-scale) + precomputed link loads under demand models | Topology only (no measured TM); TopoHub gives ECMP link loads under models | Open |

## Real optical-monitoring datasets (the real witness — the bigger prize)

| Dataset | What it is | Fit | Access |
|---|---|---|---|
| **Microsoft wide-area optical backbone** | 14 mo (2015-16), ~50 OXCs, ~100 WAN segments, ~1000 channels, **15-min signal-quality (Q-factor/SNR) polling** | **The gold anchor**: real per-channel signal-quality *time series* = the actual QoT witness + real aging/fill. Directly graduates off the GN model. | Microsoft Research project page; availability/request needs checking |
| CAIDA / MAWI | Packet traces | IP-level, not lightpath demand or QoT — **not a fit** | Open |

## Honest read for the paper

- **DONE — grounded on SNDlib `janos-us-ca`** (`sndlib_fill.py` → `SNDlib-fill.json`;
  wired into `qot_capacity.py`). Routing the 1482 real demands gives a heavy-tailed
  per-link fill (median 10, 90th-pct 35 of 76 ch): most links fill lightly, a few
  approach full. Under that real distribution — and giving BOTH policies a realistic
  0.5 dB QoT-estimator RMSE so the footprint-aware certificate is not assumed perfect —
  the footprint-aware *capacity* gain over a well-sized uniform margin is **~8%**
  (0.33 b/sym, ~21 Gb/s/ch) at matched safety. (With no estimator uncertainty it is
  16.6%; with the old synthetic all-fill-to-full it was ~5–6%. 8% is the honest,
  real-traffic, uncertainty-carrying middle.) Real traffic makes the number both
  *credible* and *larger than the synthetic strawman* — because real fill is
  heavy-tailed, the uniform margin strands more on the lightly-filled majority.
- **The Microsoft optical dataset is the real lever** for the paper's weakest point
  (GN-model-only): real measured Q-factor/SNR is the actual witness and would let us
  report a *measured* false-clear rate, not a modelled one. It is also the natural
  ask for an **industry collaborator** (as with the SIMSOPT/DESC and SJSU-quantum
  outreach). Access/terms need checking before relying on it.

## Recommendation

1. For the OFC submission (Oct 20): ground the fill on **SNDlib `janos-us-ca`** (US,
   real demands) or Abilene — a small, tractable add that steelmans the baseline.
2. Pursue the **Microsoft optical-backbone** dataset (or an operator collaborator)
   as the real-witness graduation — the strongest single credibility upgrade, likely
   post-submission / for the journal version.
