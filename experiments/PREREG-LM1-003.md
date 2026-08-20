# PREREG-LM1-003 — LM-1 third seal: consumer-anchored recovery, multi-draw bars

**SEALED at the commit ledgered in `SEALS.md`.** The governed run executes
ONCE after the sealing commit, on the governed seed below, and is reported
regardless of sign in the track document and README status ledger.

## Claim under test

Third seal of the LM-1 question, carrying both prior misses as design
inputs: [`PREREG-LM1-001`](PREREG-LM1-001.md) (FAIL — gates anchored to
the task oracle the consumer measurably deviates from) and
[`PREREG-LM1-002`](PREREG-LM1-002.md) (FAIL — H1's bar calibrated from
one powered draw + a null-SE formula, under a consumer whose
dominant-direction geometry makes random-direction ranking volatile).
The claim, unchanged in substance across all three seals: a quadratic
read operator P̂, recovered from a FROZEN, HOSTED, black-box LLM
(gemma-small, NRP ellm gateway; query-only logprob probing) over a
serialized 6-dim numeric state, **predicts the consumer's own response
to held-out perturbations** (pooled across the two planted consumers,
with per-consumer floors); the two consumers' recovered operators
differ by a preregistered operator distance (the flip, no reference to
planted supports); recovery is split-half stable; the instrument holds.
Task-oracle alignment and the full-vs-diagonal margin are ungated
diagnostics. On pass, class `[predicted]` — promoted on the third seal
with both misses on the record, the EC-7 pattern.

## Design (frozen)

Harness pair `python/lm1c_recover.py` (collection; Atlas orchestration,
NRP ellm compute, fair-use code guards: concurrency 6, max_tokens 8,
backoff, hard budget 6200) and `python/lm1c_gates.py` (evaluation;
local, numpy; deterministic from the committed raw log —
logged-response reproducibility). Model gemma-small, T = 0, first-token
yes/no logprob readout, fixed-truth loss. d = 6, prior U[−2,2]⁶,
3-decimal serialization, h = 0.15. Probe leg: 48 states ×
central differences per component, per consumer. Held-out leg: M = 48
directions — the 6 CANONICAL COORDINATE AXES (fixed pre-draw; gives
dominant-direction consumers rankable dynamic range) + 42 random per
draw — each evaluated on the SAME K = 24 shared fresh states (CRN);
estimand: direction-mean E_x[(D_u L)²] = u′P̂u. Instrument leg: 24
duplicated base queries. Consumers: A "is (2·s1−s2) > s4"; B "is
(s3+s5) > 1" (planted; oracles license diagnostics only).

## Two disclosed powered calibration draws (the across-draw lesson, applied)

Bars are frozen ONLY from the across-draw calibration of two
independent powered draws — the general lesson from LM1-002's miss:

|                | pilotA (20261030) | pilotB (20261101) |
|----------------|-------------------|-------------------|
| pooled H1      | 0.644             | 0.658             |
| consumer A ρ   | 0.610             | 0.569             |
| consumer B ρ   | 0.678             | 0.747             |
| flip distance  | 0.438             | 0.472             |
| stability      | 0.819 / 0.848     | 0.815 / 0.868     |
| repeat max     | 0.095             | 0.065             |

The axis block stabilized consumer A (0.25–0.68 across earlier draws →
0.57–0.61); every sealed bar sits below both draws with margin. The
LM1-002 chain's four disclosed held-out-estimand iterations (state
noise → unshared draws → metric SE → power) are incorporated by
reference and unchanged here.

```yaml
id: PREREG-LM1-003
date: 2026-08-20
retrospective: false
kind: consumer-anchored blind read-geometry recovery from a frozen
      hosted LLM (LM-1 third seal; successors chain LM1-001 -> LM1-002
      -> this)
harness: python/lm1c_recover.py
code_hash: sha256:bbd2980a9a37761988eb7dd933da9f170b8008582ae0684211c5fa5ba0e4fd82
gate_evaluator: python/lm1c_gates.py
gate_evaluator_hash: sha256:50b1e9443617e6839b548f0f48b0d017f6978578bcc4a0950189cdac684e3157
model: gemma-small (NRP ellm gateway; catalog re-checked per run)
governed_seed: 20261105
calibration_seeds: [20261030, 20261101]
frozen_config:
  d: 6
  n_states_probe: 48
  h: 0.15
  m_dir: 48
  canonical_axes: 6
  k_states_shared: 24
  n_repeat: 24
  prior: uniform[-2, 2]
  serialization_decimals: 3
  norm_floor: 0.05
  request_budget: 6200
sealed_gates:
  H1: POOLED held-out predictive power - mean of per-consumer
      Spearman(u'Pu, direction-mean realized (D_u L)^2) >= 0.45
      (across-draw cal 0.644 / 0.658)
  H1b: per-consumer floor - each consumer's rho >= 0.30 (cal min 0.569)
  H3: consumer-anchored flip - operator distance >= 0.25 (cal
      0.438 / 0.472)
  H4: split-half matrix cosine of the normalized operator >= 0.70 both
      (cal 0.815-0.868)
  H5: instrument - max repeat-pair |dloss| <= 0.50 (cal 0.095 / 0.065)
  H6: parse rate >= 0.98 (cal 1.00 both draws)
  H7: transport failure rate <= 0.01 (cal 0 both draws)
ungated_diagnostics: [task-oracle alignment, full-vs-diag margin,
      diag(P), top eigvec]
stopping: fixed-n, single governed run
falsification: H1/H1b fail -> with the anchor honest, the power
  adequate, and the bars set from two independent powered draws, the
  recovered operator does not predict the consumer - the campaign's
  answer, with no instrument or calibration excuse left; LM-1 closes
  REFUTED at this budget and the track's LM-2/LM-3 do not proceed on
  this foundation. H3 fail -> measured geometries do not separate.
  H4 fail -> noise-dominated. H5/H6/H7 fail -> instrument broken, no
  other gate interpreted (EC-7 discipline). All reported at equal
  prominence.
amendments: []
```

## Scope and non-claims

As the prior seals (one hosted model; planted numeric consumers;
recovery only; no probe-design optimality; H2 structure and oracle
alignment diagnostic-only). Promotion on pass follows the EC-7
precedent: third seal, both misses on the record as context, never as
evidence. Fair use: ~5.9k requests, ≈0.6M tokens per governed run.
