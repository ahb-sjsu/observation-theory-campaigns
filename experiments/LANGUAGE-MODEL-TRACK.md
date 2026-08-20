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

## 10. LM-1 pilot 2 and seal (2026-08-19)

Pilot 2 (seed 20261010, h = 0.15 frozen, n = 48,
[`results/lm1-pilot2-*.json`](../results/lm1-pilot2-analysis.json)):
A align 0.942 / support 0.965 / top-3 exact; B align 0.986 / top-2
exact. Two disclosed respecifications: stability moved to the matrix
cosine of half-sample operators, computed on the NORMALIZED estimator
(single-eigenvector stability is ill-posed under B's s3/s5
near-degeneracy; magnitude-weighted half-sample variance is
heavy-tailed at the cliff). Also measured: the endpoint is NOT always
bitwise-deterministic (repeat |Δloss| max 0.128). Sealed as
[`PREREG-LM1-001`](PREREG-LM1-001.md) at `2a66fa5` (SEALS `9b2327c`),
governed seed 20261015, harness pair hashes in the prereg.

## 11. LM-1 governed run: **FAIL (5/7 gates; no claim made)**

Seed 20261015, single run per seal
([`results/LM1-governed-log.json`](../results/LM1-governed-log.json),
[`results/LM1-governed-analysis.json`](../results/LM1-governed-analysis.json);
1272 requests, 130k tokens, 0 failures):

- **G1 FAIL by 0.0013**: B's oracle alignment 0.7987 vs the 0.80 bar
  (A passed at 0.923).
- **G4 FAIL (structural)**: A's top-3 support read {1,3,4} — the true
  s2 (diag 0.182) fell below a spurious s3 channel (0.190); B's top-2
  read {4,5} — the true s3 (0.408) fell below a spurious s4 channel
  (0.488). Supports intersect at {4}: not disjoint.
- Passed: G2 stability (0.785/0.871), G3 support concentration
  (0.947/0.787), G5/G6/G7 instrument (repeat max 0.126; parse 1.00;
  fail 0). **The instrument held; the claim as sealed failed.**

**Diagnosis, recorded not defended.** The pilots had already measured
that gemma-small's actual read geometry deviates from the task ideal
(under-read true components, spurious sensitivity to irrelevant ones)
— and the sealed gates nonetheless anchored recovery to the TASK
oracle. The governed run measured the consequence: the consumer's
weak-but-real components are magnitude-comparable to its spurious
channels, so task-oracle-anchored support and disjointness gates are
brittle exactly where the consumer is imperfect. This is a
design-anchor miss of the EC-7 class (instrument/anchor, not
phenomenon): the probe plausibly recovered the CONSUMER faithfully,
but the seal did not test that.

**Designated successor (LM1-002, not yet sealed):** gate the probe
against the consumer itself, not the task ideal — held-out predictive
gates (does P̂, fit on half the probe data, predict the loss change of
FRESH perturbations better than a diagonal/isotropic surrogate at
matched query budget?), plus a consumer-anchored flip gate (the
recovered supports of A and B differ in operator distance by a
preregistered margin, without reference to planted supports).
Task-oracle alignment drops to a reported diagnostic. No bar may be
set without a fresh disclosed pilot of the new gates.

## 12. LM1-002 pilots — the consumer-anchored gates, calibrated the hard way
(2026-08-19, four disclosed pilots; harness pair
[`python/lm1b_recover.py`](../python/lm1b_recover.py) /
[`python/lm1b_gates.py`](../python/lm1b_gates.py); logs and analyses
`results/lm1b-pilot{1..4}-*.json`; ~10.1k requests, ~1.03M tokens
total, 0 failures)

The successor's central gate — does the probed operator PREDICT the
consumer's response to held-out perturbations — took four pilot
iterations to specify honestly, each miss disclosed:

1. **v1** (one fresh state per fresh direction): Spearman −0.07/−0.29.
   Realized (D_uL)² at a single state is dominated by that state's
   distance to the decision cliff, not by u — state-position noise
   swamps the direction signal.
2. **v2** (direction-mean over 12 independent states per direction):
   A 0.55 / B 0.05 — the unshared state draws were still the variance.
3. **v3** (CRN: 16 shared states across all directions): A −0.09 /
   B 0.46 — pairing fixed the state noise and exposed the next layer:
   Spearman over n_dirs = 16 has SE ≈ 0.26; the METRIC was now the
   binding noise. (The program's oldest lesson — CRN — and its
   second-oldest — power before bars — in one pilot.)
4. **v4** (48 directions × 16 CRN states): **A 0.684 / B 0.516**, both
   > 3σ from zero at SE ≈ 0.15. The consumer-anchored predictive claim
   is real and measurable at this budget.

Constant across all pilots: stability 0.80–0.90; flip operator
distance 0.34–0.48; instrument clean (repeat |Δloss| ≤ 0.148, parse
1.00, fail 0); oracle alignment 0.86–0.98 as the ungated diagnostic.
Persistent finding: the full-vs-diagonal margin sits at ~0 or below —
off-diagonal operator estimates are noise-limited at this probe
budget — so H2 is DEMOTED to an ungated diagnostic (recorded, not
gated).

**Bars frozen in the gate evaluator** (pending seal): H1 ≥ 0.30 both
consumers (cal 0.684/0.516); H3 flip distance ≥ 0.25 (cal 0.468);
H4 stability ≥ 0.70 both (cal 0.80/0.87); H5 repeat ≤ 0.50 (cal
0.124); H6 parse ≥ 0.98; H7 fail ≤ 0.01. Governed seed 20261028 in
the harness. NOT yet sealed; seal is the next instruction.

## 13. LM1-002 governed run: **FAIL (5/6 gates; no claim made)**

Sealed [`PREREG-LM1-002`](PREREG-LM1-002.md) at `9ef831b` (SEALS
`8a89122`), governed seed 20261028, single run
([`results/LM1B-governed-log.json`](../results/LM1B-governed-log.json),
[`results/LM1B-governed-analysis.json`](../results/LM1B-governed-analysis.json);
4344 requests, 443k tokens, 0 failures):

- **H1 FAIL**: A's held-out Spearman **0.248** vs the 0.30 bar; B
  passed at **0.502**. Per the sealed clause no claim is made — and
  the clause's own words apply: the operator failed to predict the
  consumer's held-out behavior *on its own terms* for consumer A at
  this probe budget and bar.
- Passed: H3 flip distance 0.475 ≥ 0.25; H4 stability 0.893/0.860 ≥
  0.70; H5/H6/H7 instrument clean (repeat max 0.127, parse 1.00,
  fail 0). Ungated diagnostics: H2 margin POSITIVE this draw
  (+0.109/+0.137 — the first draw where full beat diag); oracle
  alignment 0.986/0.873.

**Diagnosis, recorded not defended.** The H1 bar was set from ONE
powered pilot draw (A 0.684) with the Spearman-null SE (~0.15) as the
noise scale; A's own across-draw history at power (0.55, 0.684, now
0.248) shows variance well beyond that null. Mechanism: A's measured
geometry is one dominant direction (s1) plus weak ones — u'Pu then
varies little across random directions except through the dominant
component, so the ranking is largely a ranking of noise-level
directions, and the realized direction-means remain heavy-tailed at
K = 16. B, whose geometry spreads over two comparable directions
(s3, s5), scored 0.516 / 0.502 on consecutive powered draws — the
predictive claim is plainly real where the geometry has usable spread.
Bar-setting lesson (new, general): **calibrate bars from the
ACROSS-DRAW distribution at final power (≥ 2 independent powered
draws), never from one draw plus a null-SE formula.**

**Designated successor (LM1-003, not yet sealed):** (a) two or more
independent powered calibration draws; bars set below their minimum
with margin; (b) K raised (24–32 shared states) to cut realized-mean
noise; (c) consider the pooled-across-consumers form of H1 as the
load-bearing quantity (the 088 lesson) with per-consumer floors as
secondary; (d) optionally a spread-aware direction sample (mix random
u with top-eigvector-plane u) so dominant-direction consumers
contribute rankable signal. No bar may be set without the fresh
disclosed pilots.

## 14. LM1-003 pilots — two independent powered draws; the fixes hold
(2026-08-20, disclosed; harness pair
[`python/lm1c_recover.py`](../python/lm1c_recover.py) /
[`python/lm1c_gates.py`](../python/lm1c_gates.py); artifacts
`results/lm1c-pilot{A,B}-*.json`; 11,760 requests, ~1.2M tokens, 0
failures)

Design per the LM1-002 designation: K = 24 shared CRN states; the
48-direction set leads with the 6 canonical coordinate axes (declared
pre-draw; gives dominant-direction consumers rankable dynamic range);
pooled H1 load-bearing with per-consumer floors secondary; and — the
new lesson made structural — bars frozen only from the ACROSS-DRAW
calibration of two independent powered draws:

| | draw A (20261030) | draw B (20261101) |
|---|---|---|
| pooled H1 | 0.644 | 0.658 |
| consumer A ρ | 0.610 | 0.569 |
| consumer B ρ | 0.678 | 0.747 |
| flip distance | 0.438 | 0.472 |
| stability | 0.819/0.848 | 0.815/0.868 |
| repeat max | 0.095 | 0.065 |

The axis block stabilized consumer A (previously 0.25–0.68 across
draws; now 0.57–0.61), and the pooled quantity is tight (0.644/0.658).
**Bars frozen in the gate evaluator** (pending seal): H1 pooled ≥ 0.45;
H1b per-consumer floor ≥ 0.30; H3 ≥ 0.25; H4 ≥ 0.70; H5 ≤ 0.50;
H6 ≥ 0.98; H7 ≤ 0.01. Governed seed 20261105 in the harness. NOT yet
sealed.

## 15. Roadmap

Seal PREREG-LM1-003 → single governed run at 20261105. LM-2
(allocation) and LM-3 (staleness) remain design-stage; they inherit
the anchor lesson AND the across-draw bar-calibration lesson. Nothing
in this track is claim-bearing.
