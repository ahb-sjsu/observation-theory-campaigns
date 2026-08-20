# PREREG-LM2-002 — LM-2 rehabilitation: allocation with a degeneracy-proof baseline

**SEALED at the commit ledgered in `SEALS.md`.** The governed run executes
ONCE after the sealing commit, on the governed seed below, and is reported
regardless of sign in the track document and README status ledger.

## Claim under test

Designated successor to [`PREREG-LM2-001`](PREREG-LM2-001.md) (honest
FAIL, 6/7: consumer A's single seed-drawn task-blind subset coincided
with the aligned allocation — probability 1/20 per consumer, calculable
at design time and unhandled — making its per-consumer floor
structurally unmeetable while every substantive gate passed). The claim
is unchanged: at a MATCHED serialization budget, allocating precision
to the components a frozen hosted black-box LLM actually reads — per
the diag of a freshly probed P̂ (instrument licensed by
[`PREREG-LM1-003`](PREREG-LM1-003.md)) — beats task-blind allocation on
held-out consumer loss, pooled with per-consumer floors; the blind
allocation captures a preregistered fraction of the oracle advantage;
anti-aligned does not meaningfully beat task-blind. On pass, class
`[predicted]`.

**The fix**: the task-blind baseline is the MEAN loss over FOUR
seed-drawn subsets, each rejection-sampled distinct from the aligned
and oracle sets and pairwise distinct — degeneracy impossible by
construction (the conditioning only hardens the test: subsets that
would coincide with the aligned choice are excluded from the
baseline), and baseline variance is halved.

## Design (frozen)

As PREREG-LM2-001 except the baseline construction: harness pair
`python/lm2b_alloc.py` / `python/lm2b_gates.py`. Model gemma-small,
T = 0; d = 6, prior U[−2,2]⁶; fine/coarse ladder (3 of 6 fine at 3
decimals vs integer coarse); arms aligned / oracle / anti / random1–4
(the baseline quartet) + all-coarse/all-fine references; 96 CRN-shared
eval states per consumer; fresh 48-state probe leg (cost logged
separately as capital); 24 duplicated instrument queries. Fair-use
code guards; hard budget 3400 requests.

## Two disclosed powered calibration draws (across-draw bars)

|                          | pilotA (20261120) | pilotB (20261122) |
|--------------------------|-------------------|-------------------|
| pooled aligned-vs-base   | +24.4%            | +29.7%            |
| per-consumer aligned     | 0.249 / 0.238     | 0.267 / 0.328     |
| blind capture            | 0.997             | 1.001             |
| pooled anti              | −6.5%             | −35.9%            |
| repeat max               | 0.087             | 0.057             |

Blind allocation matches the oracle in every cell; per-consumer
minimum 0.238 (vs 0.123 under the failed single-subset design); the
quantize-the-unread finding (aligned beats all-fine — coarse
serialization of UNREAD components actively helps; the LM1-001
spurious channels in reverse) replicated in all four cells and remains
an ungated reported finding. Calibration honesty on the anti control:
pooled anti reached only −0.065 in one draw and its per-cell noise has
swung positive across LM-2 history, so O3's bar is +0.10 ("anti must
not meaningfully beat blind") — documented, not wishfully tight.

```yaml
id: PREREG-LM2-002
date: 2026-08-20
retrospective: false
kind: matched-budget precision allocation for an LLM consumer by
      probed read geometry, degeneracy-proof mean-4 baseline (LM-2
      rehabilitation; instrument licensed by PREREG-LM1-003)
harness: python/lm2b_alloc.py
code_hash: sha256:8e499bfe85f7e5060607645518c29af4f7676bd5530db5bc1d7856aac291b43d
gate_evaluator: python/lm2b_gates.py
gate_evaluator_hash: sha256:f19dee01885f3ee03eb8aaaaeac7bd42e40c76a636e2f079721fb9fe0773fa72
model: gemma-small (NRP ellm gateway; catalog re-checked per run)
governed_seed: 20261125
calibration_seeds: [20261120, 20261122]
frozen_config:
  d: 6
  f_fine: 3
  n_rand_baseline: 4
  n_probe: 48
  n_eval: 96
  h: 0.15
  n_repeat: 24
  prior: uniform[-2, 2]
  fine_decimals: 3
  coarse: integer rounding
  request_budget: 3400
sealed_gates:
  O1: pooled relative consumer-loss improvement of aligned over the
      mean-4 task-blind baseline >= 0.12 (across-draw cal 0.244/0.297)
  O1b: per-consumer floor on the same quantity >= 0.05 (cal min 0.238)
  O2: blind capture of the oracle allocation advantage, pooled,
      >= 0.60 (cal 0.997 / 1.001)
  O3: anti-aligned pooled improvement over the baseline <= +0.10 -
      anti must not meaningfully beat task-blind (cal -0.065 / -0.359;
      per-cell positive swings documented across LM-2 history)
  O5: instrument - max repeat-pair |dloss| <= 0.50 (cal 0.087/0.057)
  O6: parse rate >= 0.98 (cal 1.00 both draws)
  O7: transport failure rate <= 0.01 (cal 0 both draws)
ungated_diagnostics: [all-coarse/all-fine references incl. the
      quantize-the-unread finding, probe-cost ledger, diag(P̂),
      allocations per arm incl. the four baseline subsets]
stopping: fixed-n, single governed run
falsification: O1/O1b fail -> with the baseline degeneracy-proof, the
  bars across-draw-calibrated, and the instrument licensed, probed
  geometry does not pay at matched budgets - the operational
  interface's answer, with no design excuse left. O2 fail -> recovery
  without operational capture. O3 fail -> the advantage is not
  geometry-borne. O5/O6/O7 fail -> instrument broken, no other gate
  interpreted (EC-7 discipline). All reported at equal prominence.
amendments: []
```

## Scope and non-claims

As PREREG-LM2-001 (one hosted model; planted consumers; fine/coarse
budget model; probe cost as a separate capital ledger; no greedy
optimality claim; perplexity-proxy comparator deferred). Promotion on
pass follows the program's successor-seal precedent: second seal, the
first miss on the record as context, never as evidence. Fair use:
~2.9k requests, ~280k tokens per governed run.
