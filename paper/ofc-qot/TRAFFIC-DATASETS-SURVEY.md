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

- **Grounding fill on a real demand matrix is easy and worth doing** (SNDlib
  `janos-us-ca` or Abilene → heterogeneous per-route fill on/near CORONET-CONUS). It
  makes the uniform-margin baseline credible. **But** our measurement shows the
  footprint-aware *capacity* gain over a well-sized uniform margin is only **~5–6%**
  (0.2–0.27 b/sym, ~13–17 Gb/s/ch) even under heterogeneous fill — real traffic makes
  the modest number *credible*, it does not make it large.
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
