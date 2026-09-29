# OT-DHT — the five principles on a live Kademlia router (UNSEALED, exploratory)

Owner idea 2026-09-29: make the BitTorrent DHT a showcase for Observation
Theory v1.0 (readscope `PRINCIPLES.md`, sealed 2026-08-18), one live
measurement per principle.

**Status: PRE-STATED PREDICTIONS COMMITTED, NOT YET RUN.** The predictions and
bars below are the ones in the header of `ot_dht_shakedown.py` (which the grading
code implements), committed before any measurement on the live node set. The verdicts will be
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
