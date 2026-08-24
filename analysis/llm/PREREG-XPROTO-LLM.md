# PREREG-XPROTO-LLM — eval-vs-deployment vacuity for a language model

**STATUS: UNSEALED.** FAMILY-CONSTRUCTED: 2026-08-24. Earliest compliant seal
**2026-08-25** (`llm_check.py` codes the cooling-off). Graded seeds {20260825,
20260826, 20260827}, disjoint from the shakedown's {0,1,2}. Substrate = a **real
pretrained MNLI model** (`roberta-large-mnli`) on **real** MNLI validation
(benchmark) + the **real HANS** challenge set (deployment) — the evidence rung.

**IP posture:** public methodology; the AI-evaluation instance of the
witnessed-certificate grammar. Nothing gated.

## The claim

A model's **benchmark score is a certificate** — "capable enough, deploy it." The
deployment distribution is not the benchmark; the consumer's actual inputs are a
**footprint** the aggregate score is blind to. A benchmark-certified model
**false-clears** on the deployment slices where it fails, silently (it looked fine
on the leaderboard). The false-clear is **consumer-relative**: which slice you serve
decides whether the certified model works. This is the KV-keys / XPROTO-AICSI lesson
for AI evaluation — minimizing an *aggregate* metric is blind to what a specific
consumer reads.

## Family F-LLM (constructed + shaken down 2026-08-24)

`roberta-large-mnli` (entailment = class 2). Benchmark = 1000 MNLI validation_matched
examples → the certificate ("accuracy ≥ 0.80 → deploy everywhere"). Deployment
consumers = the **30 HANS subcases** (McCoy et al.'s syntactic-heuristic challenge
set; 150 examples each) — structured input footprints. Witness = the true per-subcase
accuracy (ground-truth labels). **naive** trusts the aggregate benchmark and deploys
on every subcase; **aware** measures each subcase on a small footprint sample (50)
and deploys only where it clears. Seeds bootstrap the benchmark estimate + the aware
probe (sampling CI on a fixed model+dataset).

## Bars (bind at seal; checked against the family record first)

*Demonstrated (seeds {0,1,2}): benchmark_acc ≈ 0.91 (certified), naive_fc = 0.333
(10/30 subcases certified-but-failing), aware_fc ≈ 0–0.033, consumer_acc_spread ≈
0.38, deployment_mean_acc ≈ 0.74.*

- **B1 — eval-vs-deployment vacuity.** Per seed: `naive_fc ≥ 0.25` (the
  benchmark-certified model false-clears on ≥ 1/4 of deployment consumers).
- **B2 — footprint-aware holds.** Per seed: `aware_fc ≤ 0.10`.
- **B3 — dominance.** Per seed: `aware_fc ≤ naive_fc / 2`.

**Manipulation checks (bars too):**
- **MC1 — the model genuinely passes the benchmark.** `certified` True (benchmark
  acc ≥ 0.80) — naive is not wrong *about the benchmark*, only wrong to generalize
  it. Guards against a broken model.
- **MC2 — consumer-relativity.** `consumer_acc_spread ≥ 0.15` (per-slice accuracy
  genuinely varies — from ~1.0 on entailment subcases to ~0 on the non-entailment
  heuristic subcases). Guards against a uniform deployment.
- **MC3 — non-degenerate.** `n_consumers ≥ 20` and `0 < naive_fc < 1` (a real mix
  of passing and failing slices).

**Verdict:** any MC fail → VOID; all MCs + B1–B3 every seed → PASS; else FAIL,
kept. **Kills:** `naive_fc < 0.10` (no eval-vs-deployment gap) or `aware_fc > 0.20`
(the footprint certificate does not hold).

## Seal procedure

On 2026-08-25+: confirm `LLMREP-family.json` PASSes `--check-family`, reread, flip
STATUS to SEALED, commit; run `fam_llm.py --seeds 20260825 20260826 20260827 --out
LLMREP-graded-raw.json`, `llm_check.py` → commit `XPROTO-LLM-graded.json`.

## Scope

A real model + two real datasets; HANS is the canonical demonstration that a
benchmark can be aced while a *structured* deployment slice collapses. The
consumers are HANS's built-in subcases (a controlled shift), not arbitrary
production traffic; production logs / incident data are the external-validity
graduation. Credited prior art: McCoy et al. (HANS); the broad benchmark-vs-
robustness literature. OT's delta is the **measured, consumer-relative,
footprint-witnessed false-clear rate** of the deployment decision as a first-class
number — the eval-vs-deployment gap stated as a certificate vacuity.

## Provenance

- Exploration: the "dark places" survey — AI evaluation as a witnessed certificate
  whose false-clear is silent on the leaderboard.
- Family + grading: `fam_llm.py` (real inference) + `llm_check.py` (seal-guard +
  coded cooling-off + real-substrate-only sealed grading + pre-seal record check).
