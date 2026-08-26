# Same Budget, Opposite Verdicts: Verdict Inversion in Optical and Radio Resource Allocation

**Status: OUTLINE (2026-08-26).** The dedicated flip paper, created when review
of the WCNC/OFC drafts forced the flip material out of both (each conference
paper now carries a two-sentence pointer to the sealed cells). This paper is
where the program's only genuinely novel cross-domain result gets its full
treatment. Evidence: XPROTO-QOT-FLIP and XPROTO-CSI-FLIP (families constructed +
shaken down 2026-08-26, sealing 2026-08-27, graded seeds 20260827-29), plus the
three disciplined negatives (grid, LLM, ZooKeeper) that map the phenomenon's
boundary.

## The claim (one paragraph)

Two allocation policies with identical aggregate budgets can receive opposite
verdicts from two consumer classes whose failures ride different axes of the
underlying state. The fleet-level metric is then not merely lossy but
non-ordering: it cannot rank the two policies for any consumer. We demonstrate
the inversion with sealed, pre-registered experiments in two unrelated
substrates (optical QoT margin allocation on GNPy; 5G NR margin allocation on
Sionna LDPC link simulation), state the preconditions it needs, and show with
matched controls and cross-domain negatives that both preconditions are
necessary: (1) the two consumers' read operators must be misaligned (read
different projections of the state), and (2) both consumers must operate near
their decision thresholds. Threshold-pair consumers (same read, shifted
requirement) provably show dominance, never inversion.

## Sections

1. **Introduction.** The aggregate-metric habit; the inversion as the sharpest
   failure of it; contributions list.
2. **The two sealed inversions.**
   - Optical: policy A by reach vs policy B by band-centrality at matched
     fleet-mean margin (1.0 dB); long-reach band-edge vs short-reach band-centre
     fleets. Graded numbers after 2026-08-27 seal.
   - Radio: policy A by Doppler vs policy B by SNR deficit at matched fleet-mean
     margin (1.5 dB); M-fleet (aging axis) vs S-fleet (fade axis). Graded
     numbers after seal.
   - In both: fleet aggregate nearly tied while per-fleet gaps are large.
3. **The taxonomy and its null.** Read-operator misalignment vs threshold
   shift; the registered two-FEC / +2 dB-table controls (no inversion); why the
   eMBB/URLLC budget pair in the WCNC paper shows dominance, not inversion.
4. **Where the flip refuses to appear (kept negatives).**
   - Grid (pandapower): one shared physical projection (voltage) -> no
     misaligned read available -> no flip.
   - LLM (MNLI/HANS): both consumers far from threshold at practical operating
     points -> no flip.
   - ZooKeeper: the two staleness axes exist but the L-axis effect lives only
     in a tuned sliver of lag/write-interval space; registering it would violate
     the discipline (EXPLORATION-ZK-FLIP.md, kept). Bonus finding: the witnessed
     correction's operating region (sync-breakdown).
   - These are not failures of the law; they instantiate its preconditions.
5. **Scheduler/operator interpretations.** What a twin/scheduler should report
   instead: per-consumer-class verdicts; when a fleet number is safe (aligned
   reads) and when it is meaningless (mixed portfolios). Goodput framing:
   the inversion survives translation from failure-rate to delivered goodput
   (to verify on the sealed records; if it does not, say so).
6. **Method/discipline appendix.** Prereg/seal/graded-seed protocol; the
   pilot trails; content hashes.

## Venue candidates (discuss with owner)

- IEEE/ACM Transactions on Networking (cross-layer, unhurried, right length)
- ACM SIGMETRICS / Performance (measurement + methodology emphasis)
- HotNets (if compressed to a position paper; fastest feedback)
- The theory/OT monograph track keeps the general theorem; this paper stays
  empirical.

## Rules

- No numbers in the manuscript until the 2026-08-27 seals land; then graded
  numbers only.
- The two conference papers keep only their pointer sentences; no duplication
  of tables or figures.
- House prose style per the academic-paper skill (short declarative sentences,
  no em-dashes, no label-speak).
