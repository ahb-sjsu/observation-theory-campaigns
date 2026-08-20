# LM Track: Language-Model Consumers

**Status:** design draft, unsealed, non-claim-bearing. Chip 🤖 LM.
No bar in this document is calibrated yet; every threshold below is
marked PENDING PILOT and no run may be sealed against it until a
disclosed pilot fixes it (PROTOCOL §5.1, power before bars).

## 1. Question

An LLM is the canonical query-access-only consumer: no gradients, no
attention access, often not even your model — exactly the third access
regime Paper VIII argues is the open one. The track's question: does
the program's sharpest claim survive contact with a real neural
consumer? Concretely — can a quadratic read geometry P_C = JᵀGJ of a
FROZEN LLM's task loss over a serialized numeric state be recovered by
query-only probing (logprob readout), composed with the quantization
covariance Σ that a serialization-precision choice induces, and used
to prospectively allocate per-component token/precision budget at
matched total budgets, probe cost charged — beating the baselines the
prior-art sweep says must be beaten?

## 2. Anchors ([`LM-PRIOR-ART-SWEEP.md`](LM-PRIOR-ART-SWEEP.md), 2026-08-19)

Structural ancestors, conceded: **LODL** (NeurIPS 2022; sampled-
perturbation quadratic surrogates of a black-box decision loss — the
estimator's mathematical heart) and **HAWQ-V2** (NeurIPS 2020;
Hessian-trace-weighted precision allocation, for weights). Nearest
applied neighbor and **required baseline**: **CompactPrompt**
(uniform, sensitivity-blind quantization of numeric prompt fields).
Second required comparator: **LLMLingua-style** proxy-perplexity
pruning. MeZO establishes forward-only finite-difference probing of
LLMs as practical. The open conjunction (and the ONLY claim this
track may aim at) is the assembly: probed quadratic metric over
serialized state × Σ composition × prospective matched-budget
allocation × probe cost charged × out of sample.

## 3. Compute posture (binding; user constraint 2026-08-19)

Heavy compute runs on **NRP's managed ellm gateway**
(`ellm.nrp-nautilus.io/v1`), not on Atlas (electricity cost — see the
project feedback memory). Feasibility verified 2026-08-19: gateway
reachable, catalog live at 14 models (IDs drift; re-check
`GET /v1/models` per run and record the catalog in the artifact),
**logprobs + top-5 alternatives returned** on chat completions at
temperature 0. Atlas is orchestration only (the probe driver, token
custody in `~/.primer.env`); a local cu128 torch venv + cached Qwen
models exist as a declared fallback if gateway instability breaks
gate design. Fair-use rules are encoded as **code guards in the
harness** (accounting, not recall): per-model concurrency caps
(kimi/glm-5 = 2; minimax-m2/gemma-small = 8; qwen3/gpt-oss = 16),
max_tokens ≤ context/16, exponential backoff on 4xx/5xx, and a
per-run request budget printed in the artifact.

## 4. Reproducibility posture (replaces bitwise reproduction)

Hosted endpoints are not bitwise-reproducible (batching, backend
drift). The seal discipline adapts as it would for hardware: the
governed artifact logs EVERY prompt and EVERY returned logprob
verbatim, so the entire analysis pipeline is bitwise-reproducible
FROM THE LOGS; the model-side instrument gate is **repeat-query
agreement** (a preregistered fraction of queries issued twice at
temperature 0; agreement rate and logprob deviation measured as their
own diagnostic, EC7-003 style). Model ID, catalog snapshot, and query
timestamps are recorded. Comparison gates are PAIRED and ordinal
wherever possible (same prompts across arms).

## 5. The claim, in three types, never conflated

**Instrument claim.** Repeat-query logprob agreement above its bar;
probe-response cliffs handled by the Paper VIII §VI belief-averaged
smoothed operator (token discreteness makes the raw loss a staircase;
the smoothed finite-perturbation probe is what gets measured).
PENDING PILOT: agreement bar, smoothing width, probe design.

**Structural claim (LM-1).** The recovered P̂_C is real geometry, not
noise: on planted tasks whose oracle read direction is KNOWN (the
question reads only components in a declared subspace), blind
recovery matches the oracle (EC-3's recover/match positive control);
and the two-consumer flip transfers (two questions over the same
state, opposite precision-allocation verdicts — the EC-2/DR-2
pattern).

**Operational claim (LM-2).** At matched total token budgets,
tr(P̂_C Σ(a))-driven per-component precision allocation beats
(i) uniform quantization (the CompactPrompt baseline), (ii)
proxy-perplexity allocation (the LLMLingua-style comparator), and
(iii) the anti-aligned allocation (pooled load-bearing form), on
held-out task loss, probe cost charged in tokens against the gains.
Oracle-vs-blind capture fraction preregistered. PENDING PILOT: all
bars.

## 6. Candidate campaign designs

- **LM-1 (recover/match + flip; the licensing campaign).** State
  x ∈ R^d (d ≈ 6–8) drawn from a declared prior; serialized as a
  labeled numeric record with per-component decimal precision; task =
  a question whose correct answer is a planted functional of a known
  subspace (threshold/comparison/lookup forms); consumer loss =
  −log p(correct answer tokens | prompt) at temperature 0. Probe:
  belief-averaged finite differences at declared per-component scales.
  Metrics: oracle-alignment of P̂_C (principal-angle / trace-overlap),
  flip prediction vs measurement across two planted questions.
- **LM-2 (matched-budget allocation; the operational campaign).**
  Precision vectors a with Σ(a) = diag(quantization variances
  step(a_i)²/12); allocation arms: aligned (tr P̂_C Σ greedy), oracle,
  uniform, perplexity-proxy, anti; matched total serialized-token
  count; held-out states; probe cost charged. Multi-model transfer
  arm across the ellm catalog (paired gates, per-model rows).
- **LM-3 (staleness/refresh; DR × LM).** Directional staleness of a
  cached serialized state for an LLM agent: refresh-by-S_C vs
  refresh-by-age at matched refresh budgets. Design-stage only until
  LM-1/LM-2 license the vocabulary.

## 7. Inherited discipline (EC + DR lessons, binding)

Sealed preregs with frozen gates and single governed runs, outcomes
reported regardless of sign; disclosed pilots before any bar; pooled
load-bearing anti-control forms (the 088 lesson); analytic instrument
quantities wherever possible and the instrument residual as its own
gate (EC7-003 / VI-13); signed-mean budget-skew gate for any
matched-budget comparison (the VI-15 protocol recommendation);
generator/task family frozen at seal; numpy bools cast before
json.dump; `git commit -F` for messages with quotes.

## 8. Pilot 0 — instrument (2026-08-19, disclosed; harness
[`python/lm0_instrument.py`](../python/lm0_instrument.py), results
[`results/lm0-instrument.json`](../results/lm0-instrument.json))

315 requests, 37k tokens, 0 failures, ~30 s per model. Task: 6-dim
state serialized at 3 decimals, planted question "is 2·s1−s2 > s4",
first-token yes/no logprob readout at temperature 0.

- **gemma-small — selected as the primary instrument.** Parse 100%,
  clean first token 100%, accuracy 92%, mean correct-answer loss 0.50.
  **Repeat queries return bitwise-identical logprobs** (Δlogprob mean
  and max = 0.0 over 20 pairs) — the hosted endpoint is deterministic
  at T=0, so the instrument gate can be strict. Boundary sweep shows
  the expected staircase-with-peak: low loss away from the decision
  boundary, uncertainty spike (3.83) at the crossing, verdicts N→Y
  with one non-monotonic point at the boundary — the cliff shape the
  §VI belief-averaged smoothed probe exists for.
- **qwen3-small — transfer-arm candidate.** Parse 100%, accuracy 71%,
  verdict agreement 1.0 on repeats but logprob jitter (mean 0.030,
  max 0.198): verdict-stable, value-noisy → usable under
  tolerance-banded paired gates only.
- **gpt-oss — excluded with reason.** Readout 0% parse: its
  reasoning/harmony output format never surfaces a yes/no token in
  content logprobs. Revisit only with a dedicated readout.

Calibration consequences: primary-instrument repeat gate can sit at
Δlogprob = 0 (measured, not assumed — re-verify per run since
endpoints drift); smoothing width for probes must span the boundary
peak (grid step 0.05 resolved it cleanly); probe budget trivial at
this scale (~100 requests/model/leg).

## 9. LM-1 pilot 1 — blind recovery works, and the deviations are the story
(2026-08-19, disclosed; harness
[`python/lm1_probe.py`](../python/lm1_probe.py) collects raw losses,
[`python/lm1_analyze.py`](../python/lm1_analyze.py) scores offline;
raw log [`results/lm1-pilot1-probe-log.json`](../results/lm1-pilot1-probe-log.json),
analysis [`results/lm1-pilot1-analysis.json`](../results/lm1-pilot1-analysis.json);
1216 requests, 124k tokens, 0 failures)

Two planted consumers on gemma-small, 32 prior draws, central-difference
probing where the step h IS the smoothing width; P̂ = mean gradient
outer-product; fixed-truth loss L(x̂; x) = −logprob(correct-for-x |
prompt(x̂)) — the consumer misled by a perturbed estimate.

- **Consumer A** (2s1−s2 vs s4; oracle dir ∝ (2,−1,0,−1,0,0)): top-eig
  alignment **0.942** (h=0.1) / 0.890 (h=0.25); split-half stability
  0.940/0.902; trace on oracle support axes 0.916/0.973.
- **Consumer B** (s3+s5 vs 1): alignment **0.907**, top-2 diagonal =
  the support exactly, split-half 0.883.
- **Flip precursor**: recovered top components fully disjoint across
  consumers ({1,2} vs {5,3}).
- **The consumer ≠ the task — and P̂ measures the consumer.** The
  recovered geometry says gemma-small UNDER-reads s4 (eigvec coeff
  0.14 vs the task's 0.41; consistent with its 92% accuracy) and, at
  fine probe width, carries SPURIOUS sensitivity to the irrelevant s6
  (diag 0.325 ≈ relevant s4's 0.316); the wider probe (h=0.25)
  suppresses the spurious channel (s6 → 0.023) at some alignment
  cost. These deviations are measurements about the consumer — the
  operational geometry OT claims exists — and they are exactly why
  LM-2's allocation arm must be driven by P̂ (consumer geometry), not
  by the task oracle.

Calibration notes for the seal: candidate bars R1 alignment ≥ 0.75,
split-half ≥ 0.75, support-axes trace fraction ≥ 0.7, disjointness of
flip supports as a boolean gate; probe width in [0.1, 0.25] with the
width choice frozen at seal (or both widths run and gated separately);
n_states = 32 gives split-half ~0.88–0.94, so 48–64 for margin.

## 10. Roadmap

Pilot 2 (if needed): n_states and width finalization. Then freeze →
seal (PREREG-LM1-001, recover/match + flip on gemma-small) → single
governed run → LM-2 (matched-budget allocation vs CompactPrompt-style
uniform + perplexity comparators) → LM-3. Nothing here is
claim-bearing until sealed.
