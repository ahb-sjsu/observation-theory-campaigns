# PREREG-LM2-001 — LM-2: matched-budget precision allocation by probed read geometry

**SEALED at the commit ledgered in `SEALS.md`.** The governed run executes
ONCE after the sealing commit, on the governed seed below, and is reported
regardless of sign in the track document and README status ledger.

## Claim under test

The LM track's operational campaign, standing on the LM1-003-licensed
recovery instrument ([`PREREG-LM1-003`](PREREG-LM1-003.md), promoted
`[predicted]`): at a MATCHED serialization budget, allocating precision
to the state components a frozen hosted black-box LLM actually READS —
per the diag of a freshly probed P̂, probe cost logged — **beats
task-blind allocation on the consumer's held-out task loss**, pooled
across two planted consumers with per-consumer floors; the blind
allocation captures a preregistered fraction of the oracle allocation's
advantage; and the anti-aligned allocation is not better than
task-blind (pooled — the 088 load-bearing form). On pass, class
`[predicted]`: the tr(P̂ Σ)-composition's resource-allocation
consequence, demonstrated on a real neural consumer. The
CompactPrompt/HAWQ-V2/LODL concessions of
[`LM-PRIOR-ART-SWEEP.md`](LM-PRIOR-ART-SWEEP.md) are incorporated; the
claim is the conjunction only.

## Design (frozen)

Harness pair `python/lm2_alloc.py` (collection; Atlas orchestration,
NRP ellm compute, fair-use code guards: concurrency 6, max_tokens 8,
backoff, hard budget 2800) and `python/lm2_gates.py` (evaluation;
local, deterministic from the committed raw log). Model gemma-small,
T = 0, first-token yes/no logprob readout. d = 6, prior U[−2,2]⁶.
**Fine/coarse serialization ladder** (design disclosure: a
decimals ladder was rejected — 1-decimal uniform serialization is
already near-lossless at these margins, so it measures nothing): each
component rendered fine (3 decimals) or coarse (integer; quantization
std ≈ 0.29); budget = exactly 3 of 6 components fine. Arms, all
budget-matched and evaluated on the SAME 96 fresh states per consumer
(CRN exact): aligned (top-3 by diag P̂ from a fresh 48-state probe leg
at h = 0.15, cost logged separately), oracle (planted read components,
filled to budget by P̂), anti (bottom-3 by P̂), random-subset
(seed-drawn task-blind 3-subset — the discrete-ladder stand-in for
CompactPrompt-style uniform, disclosed; a perplexity-proxy comparator
needs a local proxy LM and is deferred with disclosure). References
(diagnostics, not budget-matched): all-coarse, all-fine. Instrument:
24 duplicated eval queries. Endpoint: mean
−logprob(correct-for-TRUE-x | prompt(quantized x)). Consumers as
LM-1: A "is (2·s1−s2) > s4"; B "is (s3+s5) > 1".

## Two disclosed powered calibration draws (across-draw bars, the LM1-002 lesson)

|                        | pilotA (20261110) | pilotB (20261112) |
|------------------------|-------------------|-------------------|
| pooled aligned-vs-rand | +29.1%            | +28.6%            |
| blind capture          | 0.872             | 0.993             |
| pooled anti-vs-rand    | −27.9%            | −30.9%            |
| per-consumer aligned   | 0.261 / 0.322     | 0.123 / 0.448     |
| repeat max             | 0.124             | 0.054             |

Three of four cells: blind allocation MATCHES oracle within CRN noise.
One anti cell measured +0.099 (the random subset also missed the read
components) — the pooled form is load-bearing. **Disclosed finding,
reported ungated in the governed artifact as well: the all-fine
reference is BEATEN by the aligned arm** (e.g. 0.470 vs 0.564) —
coarse serialization of unread components actively improves the
consumer (the LM1-001 spurious channels in reverse; quantization as
prophylaxis). The monotone-information bracket assumption is
OT-naive and is not gated.

```yaml
id: PREREG-LM2-001
date: 2026-08-20
retrospective: false
kind: matched-budget precision allocation for an LLM consumer by
      probed read geometry (LM-2, operational claim; instrument
      licensed by PREREG-LM1-003)
harness: python/lm2_alloc.py
code_hash: sha256:d2335e14d66b18f092b68d6638e0fed2899262c68354de807b880ce01ae6db78
gate_evaluator: python/lm2_gates.py
gate_evaluator_hash: sha256:16dfe4e9c57e160599e707259f4c5715967b2e463adc80b278498d62c59c8296
model: gemma-small (NRP ellm gateway; catalog re-checked per run)
governed_seed: 20261115
calibration_seeds: [20261110, 20261112]
frozen_config:
  d: 6
  f_fine: 3
  n_probe: 48
  n_eval: 96
  h: 0.15
  n_repeat: 24
  prior: uniform[-2, 2]
  fine_decimals: 3
  coarse: integer rounding
  request_budget: 2800
sealed_gates:
  O1: pooled relative consumer-loss improvement of aligned over the
      task-blind random-subset baseline >= 0.15 (across-draw cal
      0.291 / 0.286)
  O1b: per-consumer floor on the same quantity >= 0.05 (cal min 0.123)
  O2: blind capture of the oracle allocation advantage, pooled,
      >= 0.60 (cal 0.872 / 0.993)
  O3: anti-aligned not better than task-blind, pooled improvement
      <= 0.0 (cal -0.279 / -0.309)
  O5: instrument - max repeat-pair |dloss| <= 0.50 (cal 0.124 / 0.054)
  O6: parse rate >= 0.98 (cal 1.00 both draws)
  O7: transport failure rate <= 0.01 (cal 0 both draws)
ungated_diagnostics: [all-coarse/all-fine references incl. the
      aligned-beats-all-fine finding, probe-cost ledger, diag(P̂),
      allocations per arm]
stopping: fixed-n, single governed run
falsification: O1/O1b fail -> probed geometry does not pay at matched
  budgets on a real neural consumer; the operational interface of the
  conjunction fails, reported as the campaign's answer. O2 fail -> the
  blind probe leaves most of the oracle's value on the table (recovery
  without operational capture). O3 fail -> the advantage is not
  geometry-borne. O5/O6/O7 fail -> instrument broken, no other gate
  interpreted (EC-7 discipline). All reported at equal prominence.
amendments: []
```

## Scope and non-claims

One hosted model; planted numeric consumers; the fine/coarse ladder is
the declared budget model (token-exact budget accounting on a decimals
ladder is future work, disclosed); the random-subset baseline carries
the task-blind role (CompactPrompt-uniform has no exact analog on a
discrete ladder; perplexity-proxy deferred); probe cost is REPORTED as
a separate capital-cost ledger, not amortized into the per-state
comparison (the claim is at matched SERIALIZATION budget; deployments
amortize probing over usage — disclosed framing). No optimality claim
for greedy top-k allocation. Fair use: ~2.4k requests, ~230k tokens
per governed run.
