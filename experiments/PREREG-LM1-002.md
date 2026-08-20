# PREREG-LM1-002 — LM-1 rehabilitation: consumer-anchored recovery

**SEALED at the commit ledgered in `SEALS.md`.** The governed run executes
ONCE after the sealing commit, on the governed seed below, and is reported
regardless of sign in the track document and README status ledger.

## Claim under test

Designated successor to [`PREREG-LM1-001`](PREREG-LM1-001.md) (honest
FAIL, 5/7: its gates anchored recovery to the planted TASK oracle,
which the pilots had already measured the consumer deviating from —
the anchor, not the phenomenon, produced the miss). The rehabilitated
claim anchors every gate to MEASURED consumer behavior:

A quadratic read operator P̂, recovered from a FROZEN, HOSTED,
black-box LLM (gemma-small, NRP ellm gateway; query-only logprob
probing, no gradients, no attention access) over a serialized 6-dim
numeric state, **predicts the consumer's own response to held-out
perturbations**: on fresh unit directions evaluated over shared fresh
states, the rank correlation between u'P̂u and the realized
direction-mean squared directional derivative E_x[(D_u L)²] — the
operator's defining property — clears its bar for BOTH planted
consumers; the two consumers' recovered operators differ by a
preregistered operator distance (the flip, with no reference to
planted supports); and the recovery is split-half stable. Task-oracle
alignment appears ONLY as an ungated diagnostic. Probe cost is
accounted (request/token ledger in the artifact). On pass, class
`[predicted]`.

## Design (frozen)

Collection harness `python/lm1b_recover.py`; gate evaluator
`python/lm1b_gates.py` (local, numpy; deterministic from the committed
raw log — logged-response reproducibility, as LM1-001). Model
gemma-small, T = 0, first-token yes/no logprob readout, fixed-truth
loss. d = 6, prior U[−2,2]⁶, 3-decimal serialization, probe width
h = 0.15. Probe leg: 48 states × central differences per component,
per consumer. Held-out leg (v4): 48 fresh unit directions × the SAME
16 shared fresh states (CRN pairing across directions), central
differences along u at the same h. Instrument leg: 24 duplicated base
queries. Consumers as LM1-001: A "is (2·s1−s2) > s4"; B "is
(s3+s5) > 1" — planted so the DIAGNOSTIC is available, gated nowhere.
Fair-use code guards: concurrency 6, max_tokens 8, backoff, hard
budget 4800 requests.

## Four disclosed calibration pilots (the gate's own derivation chain)

1. **v1** (seed 20261020): held-out as one fresh state per direction —
   Spearman −0.07/−0.29: realized (D_uL)² at a single state is
   dominated by cliff distance, not direction. Respecified.
2. **v2** (seed 20261022): direction-mean over 12 INDEPENDENT states
   per direction — A 0.55 / B 0.05: unshared draws still the variance.
3. **v3** (seed 20261024): CRN (16 shared states) — A −0.09 / B 0.46:
   state noise fixed, exposing Spearman's own SE ≈ 0.26 at
   n_dirs = 16. The metric was the binding noise.
4. **v4** (seed 20261026, power-sized: 48 dirs × 16 CRN states):
   **A 0.684 / B 0.516**, both > 3σ at SE ≈ 0.15. Constant across all
   four: stability 0.80–0.90, flip distance 0.34–0.48, instrument
   clean (repeat ≤ 0.148, parse 1.00, fail 0).

Disclosed demotion: the full-vs-diagonal structure margin sat at ~0 or
below in every pilot — off-diagonal operator estimates are
noise-limited at this probe budget — so it is reported as an ungated
diagnostic (H2), never gated.

```yaml
id: PREREG-LM1-002
date: 2026-08-20
retrospective: false
kind: consumer-anchored blind read-geometry recovery from a frozen
      hosted LLM (LM-1 rehabilitation; successor to PREREG-LM1-001)
harness: python/lm1b_recover.py
code_hash: sha256:d41162da5affd56bfe00ee248baaa1577004eb0ef20efc45761641f1901e5b78
gate_evaluator: python/lm1b_gates.py
gate_evaluator_hash: sha256:7c342e2402859915a9e4ab90ece3454229919e8646db293f520dfae8cd2bbbb6
model: gemma-small (NRP ellm gateway; catalog re-checked per run)
governed_seed: 20261028
calibration_seeds: [20261020, 20261022, 20261024, 20261026]
frozen_config:
  d: 6
  n_states_probe: 48
  h: 0.15
  m_dir: 48
  k_states_shared: 16
  n_repeat: 24
  prior: uniform[-2, 2]
  serialization_decimals: 3
  norm_floor: 0.05
  request_budget: 4800
sealed_gates:
  H1: held-out predictive power - Spearman(u'Pu, direction-mean
      realized (D_u L)^2) >= 0.30 for BOTH consumers (cal 0.684/0.516,
      SE ~ 0.15 at n_dirs = 48)
  H3: consumer-anchored flip - operator distance 1 - matrixcos(Pn_A,
      Pn_B) >= 0.25, no reference to planted supports (cal 0.34-0.48
      across pilots)
  H4: split-half matrix cosine of the normalized operator >= 0.70 both
      (cal 0.80-0.90 across all pilots)
  H5: instrument - max repeat-pair |dloss| <= 0.50 (cal <= 0.148)
  H6: parse rate >= 0.98 (cal 1.00)
  H7: transport failure rate <= 0.01 (cal 0)
ungated_diagnostics: [task-oracle alignment, H2 full-vs-diag margin,
      diag(P), top eigvec]
stopping: fixed-n, single governed run
falsification: H1 fail -> the recovered operator does not predict the
  consumer's own held-out behavior at this probe budget - the
  conjunction's first step fails on ITS OWN terms (no task-oracle
  excuse available), reported as the campaign's answer. H3 fail -> the
  two consumers' measured geometries do not separate: the flip
  vocabulary does not transfer. H4 fail -> recovery noise-dominated.
  H5/H6/H7 fail -> instrument integrity broken, NO other gate is
  interpreted (EC-7 discipline). All reported at equal prominence.
amendments: []
```

## Scope and non-claims

As PREREG-LM1-001 (one hosted model; planted numeric consumers;
recovery only — allocation is LM-2, staleness LM-3; no probe-design
optimality claim), plus: no claim about off-diagonal structure (H2
diagnostic only); the planted oracles license the diagnostics, not the
gates. Fair use: ~4.3k requests, ≈0.45M tokens per governed run.
