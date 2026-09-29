# OT-DHT — the five principles on a live Kademlia router (UNSEALED, exploratory)

Owner idea 2026-09-29: make the BitTorrent DHT a showcase for Observation
Theory v1.0 (readscope `PRINCIPLES.md`, sealed 2026-08-18), one live
measurement per principle.

**Status: RUN 2026-09-29, FOUR OF FIVE PASS, P5 FAILS AS REGISTERED.** The
predictions and bars below were committed in `82e2bc7` before any measurement on
the live node set; the verdicts follow them, graded by the script as executed.
Results in `ot_dht_result.json`. The verdicts will be
added below as executed, misses at equal prominence.

## The object

The common object of the principles is a consumer C reading a representation x
through `P_C = E_D[JᵀGJ]`. Here:

- **x** is a 160-bit DHT id, a lookup target;
- **C** is Kademlia routing: C(x) = the node XOR-nearest to x among the node ids
  the `tqp-dht` daemon on Atlas has seen on the public DHT (an unprivileged,
  outbound-only libtorrent 2.1.1 session seeding two pinned open-source images);
- **P_C** is identified blind, as readscope does it: flip each of the 160 bits of
  x and ask whether the routing decision changes. The diagonal of P_C at bit i is
  the share of targets under D for which it does. The router is expected to read
  the leading bits and to stop near log₂N; everything past that is `ker P_C`.

The instrument is `plugins/tqp-dht/tqp_dht/observe.py` in turboquant-pro, pinned
at commit `adeb05221a445f1af6e81f9324f6e0c654b95778` (file sha256
`dd5c0cafbed9e849d49bf10eb48f3c000f6f587244b5399b819665d1490b45ba`). Before this
registration it was validated on synthetic node sets, where its answers are
known: exact against brute force (including ties on the top 64 bits), the knee
within 3 bits of log₂N, one more bit of read depth per doubling of N, invariant
under a common XOR relabelling, the flip reversing between routing and a
sharder, blind probing at k/d, and silence in the kernel.

## Substrate

The daemon writes, every 10 minutes and atomically, the node ids it has seen
(query senders, response senders and listed nodes, the newest 65,536), its own
lookup targets and its own node ids, each file named by SHA-256. The shakedown
freezes the dump it measures, checks the copy against its hash, and records the
hash. Probe distributions, 512 targets each, seed 20260929:

| D | targets |
|---|---|
| `D_uniform` | uniform 160-bit ids |
| `D_self` | ids sharing at least 16 leading bits with our first node id |
| `D_traffic` | the most recent 512 targets our node itself looked up |

The kernel is the set of bits with measured `diag P_C == 0` under `D_uniform`.

## Pre-stated predictions

| | principle | prediction | bar |
|---|---|---|---|
| P1 | consumer relativity | The router's read spectrum under `D_uniform` is not the isotropic observer's (1.0 on every bit): a knee K, then a kernel. And the flip: two codes with equal reconstruction error (the top 32 bits kept, A, or the bottom 32, B; 128 random bits each) are ranked oppositely by the router and by a sharder that buckets by the low 16 bits. | K in [log₂N − 6, log₂N + 2]; bits < K − 4 read ≥ 0.9; bits ≥ K + 8 read ≤ 0.05; router agrees with A ≥ 0.95 and with B ≤ 0.05 (the sharder's numbers hold by construction, printed, not graded) |
| P2 | measure dependence | The same probe reads differently depending on where it probes. | read depth tr P_C under `D_self` exceeds `D_uniform`'s by ≥ 3 bits, and under `D_traffic` by ≥ 1 bit (standard error ~0.1 bit at 512 targets) |
| P3 | observation complexity | Blind identification spends d = 160 flips per target to find a read subspace of effective rank r (bits read ≥ 50%). | d / r ≥ 5 (the k/d recovery table for blind probe subsets is an identity for random subsets, printed, not graded) |
| P4 | temporal nonstationarity | P_C is a process: over six successive node sets 10 minutes apart, with the same `D_uniform` targets, the read spectrum moves by more than sampling noise. | staleness price L1(first, last) ≥ 3 × the noise floor (L1 between two independent `D_uniform` draws on the last node set), and read depth moves ≥ 0.5 bit. Non-claim: no mechanism is named; P4 names drift as mechanism only where the staleness channel is shown to dominate, which this shakedown does not attempt |
| P5 | metric consequence | For random 1 to 5 bit perturbations δ, `δᵀPδ` predicts the damage to a graded consumer (the change in shared prefix between the target and its nearest node). The selection consumer (did the nearest node change) is printed beside it at equal prominence; P5 excludes selection consumers, so it is predicted to correlate less. Perturbations confined to the kernel meet silence. | Spearman(δᵀPδ, graded damage) ≥ 0.5; Spearman for selection < graded; kernel perturbations change the decision in ≤ 0.2% of trials |

## Verdicts, as executed (2026-09-29, 04:51 to 05:41 UTC)

The first frozen node set held 2,465 distinct node ids (log₂N = 11.27), seen by the
daemon in its first ten minutes on the public DHT; the five that followed, ten
minutes apart, held 3,455 to 5,223. Probing all three distributions took 1.4 s.

| | measured | bar | verdict |
|---|---|---|---|
| P1 | knee K = bit 8; bits 0 to 3 read 1.00; bits from 16 on read at most 0.008. The flip: the router agrees with the top-32 code 1.000 and with the bottom-32 code 0.004; the sharder agrees 0.000 and 1.000 | K in [5.27, 13.27], ≥ 0.9, ≤ 0.05, ≥ 0.95, ≤ 0.05 | **PASS** |
| P2 | read depth 9.22 bits uniform, 17.96 near our id (+8.74), 11.37 on our own targets (+2.15) | +3, +1 | **PASS** |
| P3 | effective rank r = 8 of d = 160: d / r = 20 | ≥ 5 | **PASS** |
| P4 | staleness price 1.375 bits against a noise floor of 0.115 (12 ×); read depth moved 1.37 bits (9.22, 9.90, 10.05, 10.38, 10.49, 10.59) | ≥ 3 ×, ≥ 0.5 | **PASS** |
| P5 | Spearman(δᵀPδ, graded damage) 0.529; kernel perturbations changed the decision 0 times in 2,048; **Spearman for the selection consumer 0.534, not below the graded one** | ≥ 0.5; selection < graded; ≤ 0.2 % | **FAIL** |

**The P5 miss.** Two of its three parts held: the quadratic form predicts the
graded consumer's damage (0.53), and the kernel met silence in every one of 2,048
trials, which is P5's floor ("silence, never confident error"). The part that
failed is mine, not the principle's statement: I predicted the selection consumer
would track δᵀPδ less well, because P5 excludes selection consumers from the
quadratic form. On this router the two came out equal (0.534 against 0.529). A
reading after the fact, labelled as such and not graded: the graded consumer as
registered, the change in the shared prefix of the nearest node, moves almost only
when the nearest node itself changes, so the two consumers carry nearly the same
signal here. A graded consumer that separates from the selection would need a
distance that moves without a change of node (the full XOR distance, say); that
is a successor registration, not a rescue of this one.

**P4 in detail.** The price of an old reading grows with its age: 0.10 bits at
10 minutes (inside the noise floor of 0.115), then 0.22, 0.54, 0.70 and 1.38
bits at 20 to 50 minutes. No mechanism is named, as registered. Descriptive,
not registered: the read depth rose 1.37 bits while the node set grew 2.12 times
(log₂ 2.12 = 1.08), close to the synthetic validation's one bit per doubling.

**Provenance.** Instrument `observe.py` sha256 `dd5c0caf…90b45ba` (turboquant-pro
`adeb052`), confirmed in the result; script sha256 `ad80060b…87ff27`, identical to
the committed file; first node set sha256 `b96bff9e…c55d0dc17`, every set frozen
under `/archive/tqp-dht/frozen/<t>` on Atlas with its hash in the result; seed
20260929; result file sha256 `9e670be8…b5fc1cc`.

## What would count against the program here

A flat or near-flat measured spectrum (P1), identical depths across the three
distributions (P2), a read subspace nearly as wide as the ambient dimension
(P3), a spectrum that does not move beyond noise as the network moves (P4), or a
kernel perturbation that changes the routing decision (P5's fail-closed floor)
would each be a miss for that principle on this substrate, and would be printed
as such.

## Where it runs

`ot_dht_shakedown.py` on Atlas, against `/archive/tqp-dht/observe`, freezing each
measured dump under `/archive/tqp-dht/frozen/<t>`. P1, P2, P3 and P5 are graded
on the first frozen dump; P4 needs the five dumps that follow, about 50 minutes.
The result is `ot_dht_result.json` here. The TurboQuant Pro console will show the
same five measurements live, as modes of the DHT page.
