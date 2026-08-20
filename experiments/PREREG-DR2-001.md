# PREREG-DR2-001 — DR-2: the staleness flip (freshness is consumer-relative)

**SEALED at the commit ledgered in `SEALS.md`.** The governed run executes
ONCE after the sealing commit, on the governed seed below, and is reported
regardless of sign in the track document and README status ledger.

## Claim under test

DR-2 of the DR track (experiments/DYNAMIC-RELEVANCE-TRACK.md §5): EC-2's
two-consumer verdict inversion, transported from WHERE (which directions
to sense) to WHEN (which history is fresh). Per random system, the same
pair of information sets as DR-1 — arm A an OLD scalar measurement of
the slow mode, arm B a FRESH one of the fast mode. Age of information is
a property of the histories alone: it ranks B fresher for every
consumer. Two rank-one consumers at **fixed canonical angles declared in
the harness before any system draw** (g₁ at 15°, g₂ at 75°; identical
across systems — nothing is tuned to any system's crossover):

  **the flip**: S₁(A) < S₁(B) and S₂(A) > S₂(B) — consumer 1 calls the
  OLD history fresher, consumer 2 the FRESH one, on identical data with
  identical AoI profiles.

Predicted per system by the signs of gᵢᵀ(Σ_A − Σ_B)gᵢ (closed form,
before rollout); measured on realized Monte-Carlo consumer losses. On
pass, the claim at class `[predicted]`: freshness orderings are
consumer-relative over the declared system class — a consumer-blind
freshness scalar (any AoI-style clock) cannot serve two consumers whose
read geometries straddle the crossover.

## Design

Harness `python/dr2_staleness_flip.py`, governed mode; machinery
imported unmodified from the sealed `dr1_crossover.py` (generator,
propagation, rollout — the EC-6 reuse pattern). 20 fresh random systems
from the DR-1 generator, n = 200,000 rollouts per arm per system,
consumers fixed at 15°/75°. F4 is the integrity gate in the EC7-003
sense: analytic instrument residual measured as its own diagnostic; on
F4 failure no other gate is interpreted.

## One disclosed calibration pilot

**Pilot 1** (2026-08-19, seed 20260910, 20 generator draws,
`results/dr2-pilot1.json`): flip predicted 20/20, measured 20/20,
pooled min-rel-gap 0.395 (smallest single system 0.107), residual max
0.0106, trace-null consistent in all 20. Bars frozen below this with
margin. No design changes were needed after the pilot; the canonical
angles were declared before the first draw.

```yaml
id: PREREG-DR2-001
date: 2026-08-19
retrospective: false
kind: two-consumer staleness flip (DR-2); planted canonical consumers at
      15/75 deg, old-slow vs fresh-fast histories, closed-form flip
      prediction vs realized MC loss orderings
harness: python/dr2_staleness_flip.py
code_hash: sha256:a64b4ae414d35399997a624013cc7aa662ae816128f2a8f0c9ed23555deded07
imports_sealed: python/dr1_crossover.py (PREREG-DR1-001,
      code_hash sha256:caeb9f4141982bb5a37228247ace8a8c5b26ad007401765934b160e1004c292a)
governed_seed: 20260915
calibration_seed: 20260910
frozen_config:
  n_sys: 20
  n_mc: 200000
  consumer_angles_deg: [15.0, 75.0]
  generator: inherited from PREREG-DR1-001 (identical ranges)
sealed_gates:
  F1: flip predicted by closed form in >= 80% of systems (cal 100%)
  F2: of predicted-flip systems, realized-loss inversion measured in
      >= 90% (cal 100%)
  F3: pooled min relative staleness gap over predicted-flip systems
      >= 0.10 (cal 0.395)
  F4: instrument integrity — max relative analytic-vs-MC residual over
      all consumers, arms, systems <= 0.02 (cal 0.0106)
  F5: trace-consumer null — analytic and MC trace orderings consistent
      in all systems; a rank-deficient consumer-blind scalar cannot
      invert (cal all 20)
stopping: fixed-n, single governed run
falsification: F1 fail -> the canonical window misses the crossover
  class; the flip is not generic over the declared generator (reported;
  no angle retuning without a new seal). F2 fail -> the closed form does
  not predict realized orderings; the flip is not preregisterable and
  DR-2's headline is FALSE. F3 fail -> the flip exists but rests on
  margins too thin to matter operationally. F4 fail -> instrument
  integrity broken, NO other gate is interpreted (EC-7 discipline).
  F5 fail -> harness inconsistency on the null leg; treated as an
  instrument failure. All reported at equal prominence.
amendments: []
```

## Scope and non-claims

Planted known consumers (the clean case, as EC-2 before it); blind
recovery of the consumers is EC-track machinery, not re-litigated. No
scheduling claim, no matched-budget advantage claim (DR-3). Exact-linear
plant. The 15°/75° window was chosen for coverage of the generator's
crossover distribution as observed in DR-1's disclosed pilots — that
choice is itself part of the sealed design, and F1 prices it honestly.

## Post-run clarification (2026-08-19; wording only, no verdict touched)

The independent R-IND-5 verification pass (geometric-observation
claims ledger, VI-14) flagged that F3's phrase "pooled min relative
staleness gap … ≥ 0.10" tolerates a per-system-minimum misreading.
The sealed meaning — fixed by the harness code sealed at the same
commit and by the calibration value 0.395 (the pilot's MEAN of
per-system minimum gaps; its smallest single system, 0.107, is listed
separately) — is the POOLED MEAN over predicted-flip systems of each
system's smaller consumer gap. The governed run passes under the
sealed reading (0.388 ≥ 0.10); under the stricter misreading it would
not (one system at 0.056). Recorded at the verifier's recommendation
so no future reader can mistake which bar was sealed. The sealed body
above is unmodified; this section is a dated addition and the SEALS
ledger row is annotated with the clarification commit.
