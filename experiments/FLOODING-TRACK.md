# FL Track: Flood Reduction Read Through Two Hops

**Status:** design note, non-claim-bearing. Chip 📣 FL. Registrations, all SEALED 2026-11-22 (`SEALS.md`):
`PREREG-FL1-001` (the two-hop law at 1,024 and 2,048 routers on the Atlas host) and `PREREG-FL2-001` (the aging
reference of the CPU harness), after a logged calibration pilot. Their test labs never ran: the 512-router lab queued
before them overloaded the host and its uplink failed, and labs on Atlas now run only in KVM guests. FL1-001 is VOID
without data. Its successor `PREREG-FL1-002` (the same law, calibration and bar at 512 and 1,024 routers in KVM
guests under FRR's default timers) ran on 2026-11-22/23 and is VOID: its setup gates passed, but both discriminating
512-router cells failed at deployment (a 120 s limit in the lab harness), so the 1,024-router cells were not run
(`analysis/flooding/fl1-002/`). Its successor `PREREG-FL1-003` (SEALED 2026-11-23), the same test with that
limit raised, is VOID too: both 512-router cells deployed, but at degree 8 the run with flood reduction on never
converged and at degree 16 the guest ran out of memory, so the 1,024-router cells were not run
(`analysis/flooding/fl1-003/`). The law is untested at these sizes on this host. FL2-001's status is open.

## Substrate

IS-IS distributed flooding reduction (draft-ietf-lsr-distoptflood-14) as FRR implements it in pull request 24128
(riw777/frr at e263c441), measured with topology-builders 0.2.0 ([public
repository](https://github.com/ahb-sjsu/topology-builders), `results/`): labs of real FRR routers, flood reduction
off and on taking turns, a quiet window, then links taken down and brought back up one at a time with a 30 s window
after each change. Per window: LSPs sent, isisd CPU, isisd CPU per event handler (`--profile`), and whether every
router ended with the same LSPs. Measured so far on Atlas (HP Z840, routers pinned to 20 CPUs): 64 to 180 routers in
Docker labs, 256 routers and up in network-namespace labs; on Colab: four sessions of 8 CPUs. Every number in this
note traces to a `results/` folder there.

## The read

A router that receives a changed LSP decides whether to send it on from a two-hop view of the transmitter's
neighborhood: it re-floods only if it is the neighbor that still covers some router two hops from the transmitter.
A copy can be dropped only where two routers are joined by more than one two-hop path. The decision is a consumer
whose read is the two-hop neighborhood; the **two-hop multiplicity** m (for two routers two hops apart, the mean
number of neighbors they share) summarizes how much of the flooding lies outside that read.

What the measurements already show, before any registration (exploratory, `results/`): matched by m instead of
degree, 64- and 128-router random graphs save alike; at a fixed degree the saving falls with size (degree 16: 75% at
64 routers, 53% at 128) while the spanning-tree bound 1 - (n - 1)/m_links, which for a d-regular graph is
1 - 2(n - 1)/(nd), depends on the degree alone up to O(1/n); and within
flattened butterflies m stays at 2 while the saving rises with degree, so m is not the whole story across families.

## Anchors (quote-verify before any seal)

- The spanning-tree bound 1 - (n - 1)/m_links on the attainable saving, and "savings grow with density" as known
  qualitatively (IETF 114 minutes: "look at the average fan out of your network").
- Two-hop relay selection in MANETs: multipoint relays (Qayyum, Viennot, Laouiti, HICSS 2002,
  doi:10.1109/HICSS.2002.994521) and OSPF-MDR (RFC 5614), whose savings are read through two-hop coverage.
- The draft's own numbers (about 40 copies per router down to about 2 on a 2,500-router butterfly) and FRR PR
  24128's simulator (about 2.2 copies per router against 3.7), neither at a stated degree.
- Measurement methodology: RFC 6412/6413 (variance accounting, no trial count fixed); the topology-builders results
  showing CPU savings that do not repeat across setups while LSP counts do (`results/seeds-n64`,
  `results/colab-sessions`).

What the anchors do not contain: a size-transfer test of a one-number law for the saving at fixed degree, and any
measurement of how a harness's single CPU reference ages within a run.

## Exploratory: staleness is common, harm is directional (FL3, not registered)

`analysis/flooding/fl3_stale_relays.py` on the analysis files of `results/mechanism` (router and three-link
failures on the 4x4x4 butterfly and leaf-spine 48 x 16, flood reduction on; "late" here is the files' 500 ms
threshold, not the README's 1 s), 2026-11-21, after the data were public, so exploratory only:

| | pooled over 8 failure events |
|---|---:|
| late router-LSP pairs | 659 |
| decisions by the late routers' neighbors on those LSPs | 10,709 |
| stale: reproduced only by a snapshot still holding the failed element | 6,538 (61%) |
| consequential: stale, and the decision on the fresh topology sends to the late router | 371 (5.7% of stale) |
| late pairs with a consequential stale neighbor | 368 (0.56 per late pair) |

Most neighbors decided with a topology from before the failure, at about the same time on the same LSP; for almost
all of them it did not matter. It mattered for the one relay whose decision on the fresh topology would have covered
the late router. Same age, different consequence, set by what the relay's decision reads about that router: the
shape Paper VIII's dynamic relevance predicts (staleness weighted by the consumer's read, not by the clock).
Caveat: "consequential" is defined through coverage, so the concentration is partly by construction; the
informative numbers are the base rates (61% stale against 0.56 consequential per late pair).

What it suggests for FL3, a registration not yet drafted: FRR rebuilds the snapshot on a clock (at each SPF start,
at least 1 s apart). Three refresh policies at a matched rebuild budget: the clock; rebuild on every new LSP
(isotropic); rebuild only when a new LSP reports an adjacency change inside the receiving router's two-hop view
(directional). Prediction: the directional policy removes nearly all consequential stale decisions at a small
fraction of the isotropic budget. It needs an FRR patch (two refresh triggers behind a knob), which is the owner's
decision and Russ White's code.

## Discipline

One lab at a time on Atlas; nothing else of ours runs on the routers' CPUs while a lab measures; analysis runs in
the gaps between labs (the queue's gap step). Every prediction file is hashed into the queue log before the first
measurement it predicts. Test sizes are those whose labs start after the sealing commit.
