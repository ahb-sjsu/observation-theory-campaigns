# RT Track: Routing Telemetry Under Projection

**Status:** design draft, unsealed, non-claim-bearing. Chip 🌐 RT.
No bar in this document is calibrated yet; every threshold below is
marked PENDING PILOT and no run may be sealed against it until a
disclosed pilot fixes it (PROTOCOL §5.1, power before bars).

## 1. Question

Every other track in this campaign declares its own consumer. This one
does not get to. BGP supplies consumers that exist whether or not
anyone is writing a paper: route selection specified in RFC 4271,
origin-change detectors, RPKI validators, AS-rank pipelines, churn-based
anomaly detectors. A route collector archives a stream that all of them
read, and it archives it at reconstruction fidelity, because that is
what an archive does.

The question is whether the *same discard* is lossless for one of these
consumers and destructive for another, provably and measurably. If it
is, consumer-relativity is not a modelling convenience — it is a
property of deployed infrastructure that current archival practice
cannot express.

## 2. Anchors (verified citations; page-verification owed before any seal)

The redundant-update phenomenon is **known and measured**, and this
track leads with that rather than rediscovering it.

- Park et al., *Investigating occurrence of duplicate updates in BGP
  announcements*, PAM 2010 — duplicate announcements measured; BGP
  communities identified as a large cause.
- Huston, Rossi, Armitage, *A technique for reducing BGP update
  announcements through path exploration damping*, IEEE 2010 — PED
  suppresses transient updates, reported up to 32% fewer announcements
  and 77% less path exploration.
- Chandrashekar et al. / Duan et al., *Limiting path exploration in
  BGP*, INFOCOM 2005 (EPIC).
- Villamizar et al., RFC 2439, route flap damping; MRAI timers, RFC 4271.
- *Utilizing duplicate announcements for BGP anomaly detection*,
  MDPI 2025 — duplicates as **signal** for a detector, i.e. a consumer
  for which they are not redundant at all.

A ~25–30% redundant-announcement share is therefore a **replication
target, not a finding**. Our own exploratory scout measured 30.25% on
one 15-minute `route-views2` window (2026-08-14 00:00, 81,047 records,
204,844 announcements, 25,955 prefixes). It agrees with the literature
and is recorded as an instrument check.

**What the anchors do not cover.** All of the above optimise *volume*:
send fewer updates without breaking convergence. None states a
consumer-relative asymmetry — that one discard is exactly lossless for
a state-reading consumer, by proof, while destroying a timing-reading
consumer's signal. That asymmetry is this track's only candidate
contribution, and the sweep above is what licenses saying so.

## 3. Anti-circularity contract

Forbidden inputs, mirroring CAMPAIGN.md §3. No consumer may be
constructed to make the asymmetry appear. Both consumers must be
externally attested: C1 from the collector's own semantics, C2 from the
published anomaly-detection line (MDPI 2025 and its antecedents). No
threshold, weighting or feature may be tuned on the confirmatory data.
No allocation may be chosen after seeing its error.

## 4. The claim, in three types, never conflated

**Instrument claim.** Pruning redundant updates leaves the collector's
final state identical, so it is exactly lossless for any consumer that
reads only that state. This is **proved**, not measured:
`proofs/Proofs/CollectorPrune.lean`, theorems `run_prune` and
`consumer_indistinguishable`, no `sorry`, axioms `propext` and
`Quot.sound` only. The empirical C1 check is therefore a **gate on the
implementation**, not evidence for the theory — if it fails, our parser
or pruner is wrong, and nothing about OT is learned.

**Structural claim.** The same pruning measurably degrades a
churn-reading consumer. Equal discard, opposite consequence, decided
entirely by what the consumer reads.

**Operational claim — not made.** Nothing here recommends a change to
collector or router practice, and no run will be labelled as supporting
one. Archives serve many consumers at once; that is a reason to keep
the full stream, not to prune it.

## 5. Consumers

- **C1, state-reading.** Per-prefix origin set at window close (the
  MOAS/origin-change input). Depends only on the final collector state.
  Attested by the collector's own semantics and the hijack-detection
  literature.
- **C2, churn-reading.** Per-prefix update-arrival features (count,
  inter-arrival dispersion) feeding an anomaly score. Attested by
  MDPI 2025, which uses duplicates *as* signal.

C1 and C2 are declared before any confirmatory data is touched, with
their features frozen.

## 6. Compressors, at equal budget

- **U — uniform.** Reconstruction-flavoured: subsample the stream
  uniformly to the budget.
- **K1 — C1-optimal.** Drop redundant updates only (definition as in
  the Lean file: re-announcement of the installed path; withdrawal of
  an absent prefix).
- **K2 — C2-optimal.** Retain arrival counts and timing; discard path
  detail.

Budget is defined as retained bytes of the MRT stream, and the three
compressors are matched on it. Matching is an instrument gate: if the
budgets differ by more than PENDING PILOT, the run is void.

## 7. Predictions and falsification

- **P1 (gate, must pass).** C1 error under K1 is exactly zero. Not a
  finding — the Lean theorem says it must be. Non-zero means our code
  disagrees with our model.
- **P2 (the structural claim).** C2 detection quality under K1 is worse
  than under U by at least PENDING PILOT.
- **P3 (the cross).** C1 error under K2 exceeds C1 error under U by at
  least PENDING PILOT, while C2 quality under K2 is at least that of U.
  P2 and P3 together are the asymmetry; either alone is not.
- **Control, must show nothing.** A constant consumer (reads nothing)
  scores identically under U, K1 and K2. Any difference means the
  harness is measuring itself.

**How this fails, written before it runs.** (a) If duplicates carry no
churn signal, P2 fails and the asymmetry is an artefact of the MDPI
framing rather than a property of the data — a real negative, and the
most likely one. (b) If pruning degrades C1 at all, P1 fails and the
instrument is broken. (c) If K2 preserves C1 as well as U does, P3
fails and the two consumers are not actually in tension. Any of these
is reported at equal prominence, per the honest-negatives rule.

## 8. Data discipline

The scout in §2 was exploratory, labelled before it ran, and measured
**room only** — base rates, not effects. It selected this candidate from
three (MOAS, update churn, path-length ties). Because selection used
data, the confirmatory run **must not** use it:

- scout: `route-views2`, 2026-08-14 00:00 UTC, 15 min — **burned**
- confirmatory: a different collector (RIPE RIS `rrc00`) and a
  different window, both fixed at seal time and neither inspected
  before.

The path-length-tie probe returned 91.9% and is **rejected as
degenerate**, not carried forward: when nearly every eligible prefix is
a near-tie, the predicate selects nothing and a "consumer-optimal"
allocation targeting it is uniform allocation under another name. The
MOAS probe returned 0.19% (49 prefixes in 15 minutes) — real but too
thin to power a bar from a short window; retained as a future candidate
with a longer window, not as this run's consumer.

## 9. What this track cannot claim

The Lean result models the **collector** RIB: last-writer-wins per
`(peer, prefix)`. It is not the BGP decision process — no local
preference, MED, tie-break order, IGP cost, MRAI or timers appear in
it, and no statement is made about any router's forwarding choice.
Local preference is policy and is absent from public archives, so
best-path selection cannot be fully reconstructed from this data at
all; that is why it is not the consumer here.

Nothing in this track is a claim about the global routing system's
behaviour, about operator practice, or about what any network *should*
do.
