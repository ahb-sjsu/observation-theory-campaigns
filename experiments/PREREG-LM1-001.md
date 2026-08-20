# PREREG-LM1-001 — LM-1: blind read-geometry recovery from a frozen hosted LLM

**SEALED at the commit ledgered in `SEALS.md`.** The governed run executes
ONCE after the sealing commit, on the governed seed below, and is reported
regardless of sign in the track document and README status ledger.

## Claim under test

The LM track's licensing campaign (experiments/LANGUAGE-MODEL-TRACK.md;
novelty posture sealed from [`LM-PRIOR-ART-SWEEP.md`](LM-PRIOR-ART-SWEEP.md):
LODL and HAWQ-V2 conceded as structural ancestors; the conjunction is the
claim). A quadratic read geometry of a FROZEN, HOSTED, black-box LLM
(gemma-small on the NRP ellm gateway; no gradients, no attention access,
logprob readout only) over a serialized 6-dim numeric state is
**recoverable by query-only finite-difference probing**: for two planted
consumers with known oracle directions, the recovered operator aligns
with the oracle, concentrates on the oracle support, is stable across
split halves, and the two consumers' recovered supports are disjoint
(the flip vocabulary transfers to a real neural consumer). Probing cost
is accounted (request/token ledger in the artifact). On pass, class
`[predicted]`; the deviations of P̂ from the task ideal (the consumer's
own imperfect reading) are reported as measurements, per the pilots.

## Design (frozen)

Collection harness `python/lm1_recover.py` on Atlas as orchestration;
compute = NRP ellm gateway (fair-use code guards: concurrency 6,
max_tokens 8, backoff, hard budget 1700 requests). Model `gemma-small`,
temperature 0, first-token yes/no logprob readout; loss
L(x̂; x) = −logprob(correct-for-x | prompt(x̂)) — the consumer misled by
a perturbed estimate, judged against fixed truth. d = 6, prior
U[−2,2]⁶, 3-decimal serialization, probe width h = 0.15 (frozen from
pilot 1's width calibration), n_states = 48, central differences per
component, N_repeat = 24 duplicated base queries as the instrument leg.
Consumers: A "is (2·s1−s2) > s4" (oracle ∝ (2,−1,0,−1,0,0), support
{1,2,4}); B "is (s3+s5) > 1" (oracle ∝ (0,0,1,0,1,0), support {3,5}).
The RAW LOG of every query's yes/no logprobs is the primary artifact
(logged-response reproducibility: the hosted endpoint is not
bitwise-reproducible; the gate evaluation is deterministic from the
committed log). Gate evaluator `python/lm1_gates.py` (local, numpy)
computes two estimators from the log: the magnitude-weighted
(belief-averaged) operator P = mean(ggᵀ) for alignment/support, and the
normalized operator P_n = mean(ĝĝᵀ, ‖g‖ > 0.05) for stability — the
pilot-2 respecification, disclosed below.

## Three disclosed calibration pilots

1. **Pilot 0** (instrument, seed 20260930, `results/lm0-instrument.json`):
   gemma-small selected (100% parse, 92% accuracy, repeat logprobs
   bitwise-identical in that sample); gpt-oss excluded (readout 0%);
   qwen3-small deferred to a transfer arm. Cliff shape characterized.
2. **Pilot 1** (seed 20261005, `results/lm1-pilot1-*.json`): recovery
   works at h ∈ {0.10, 0.25} (alignments 0.89–0.94); h = 0.15 frozen as
   the compromise (0.10 admits a spurious irrelevant-component channel,
   0.25 suppresses it at alignment cost); the deviations (under-read
   s4, spurious s6) identified as consumer measurements.
3. **Pilot 2** (seed 20261010, h = 0.15, n = 48,
   `results/lm1-pilot2-*.json`): A align 0.942 / support 0.965 / top-3
   exact; B align 0.986 / top-2 exact. TWO RESPECIFICATIONS, disclosed:
   (a) stability moved to the matrix cosine of half-sample operators
   (single-top-eigenvector cosine is ill-posed when the consumer reads
   two components near-equally — B's s3/s5 near-degeneracy rotates the
   eigenvector inside the plane while the operator stands); (b)
   stability computed on the NORMALIZED estimator (the magnitude-
   weighted operator's half-sample variance is heavy-tailed at the
   cliff; cal: B matrix-cos 0.577 magnitude-weighted vs 0.886
   normalized while alignment sits at 0.986). Also measured: the
   endpoint is NOT always bitwise-deterministic (repeat |Δloss| max
   0.128, mean 0.020 over 24 pairs) — G5 sized accordingly.

```yaml
id: PREREG-LM1-001
date: 2026-08-19
retrospective: false
kind: blind read-geometry recovery from a frozen hosted LLM (LM-1,
      licensing campaign); planted consumers, query-only logprob
      probing, logged-response artifact
harness: python/lm1_recover.py
code_hash: sha256:7c3bbeb4efc00c1f386d8925d413ca59bf4af4eaf2e045f765180089803d7d5a
gate_evaluator: python/lm1_gates.py
gate_evaluator_hash: sha256:baef83c83d8159de2d43ea7627a5019a41956e9cb45bb7f0626582aea9fb30ef
model: gemma-small (NRP ellm gateway; catalog re-checked per run)
governed_seed: 20261015
calibration_seeds: [20260930, 20261005, 20261010]
frozen_config:
  d: 6
  n_states: 48
  h: 0.15
  n_repeat: 24
  prior: uniform[-2, 2]
  serialization_decimals: 3
  norm_floor: 0.05
  request_budget: 1700
sealed_gates:
  G1: top-eig alignment of P with the oracle direction >= 0.80 for BOTH
      consumers (cal 0.942 / 0.986)
  G2: split-half matrix cosine of the normalized operator >= 0.75 both
      (cal 0.903 / 0.886)
  G3: trace fraction of P on the oracle support axes >= 0.65 both
      (cal 0.965 / 0.797)
  G4: recovered flip supports disjoint - A top-3 vs B top-2 by diag
      (cal {1,2,4} vs {3,5})
  G5: instrument - max repeat-pair |dloss| <= 0.50 (cal 0.128; the
      endpoint's measured nondeterminism, small vs the 0.5-12 loss scale)
  G6: parse rate >= 0.98 (cal 1.00)
  G7: transport failure rate <= 0.01 (cal 0)
stopping: fixed-n, single governed run
falsification: G1/G3 fail -> the probed operator does not recover
  planted geometry through a real LLM's tokenization and reasoning -
  the conjunction dies at its first step, reported as the campaign's
  answer. G2 fail -> recovery is noise-dominated at this probe budget.
  G4 fail -> the flip vocabulary does not transfer to neural consumers.
  G5/G6/G7 fail -> instrument integrity broken (endpoint drift,
  readout, or transport), NO other gate is interpreted (EC-7
  discipline); rerun only under a new seal after the instrument is
  fixed. All reported at equal prominence.
amendments: []
```

## Scope and non-claims

One hosted model (transfer across the catalog is a future arm);
planted numeric consumers (real task suites are future); recovery only
— no allocation claim (LM-2), no staleness claim (LM-3); no optimality
claim for the probe design; the oracle-alignment gates measure
recovery of PLANTED geometry, while the consumer's systematic
deviations from the task ideal (under-read components, spurious
sensitivities) are reported as findings, not failures. Fair use:
~1272 requests, ≈130k tokens against the gateway's research AUP.
