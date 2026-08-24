# LLM-Eval Track: eval-vs-deployment vacuity for language models

**Status:** constructed 2026-08-24. Chip 🕒🤖 LLM. Freshness program
([FRESHNESS-PROGRAM.md](FRESHNESS-PROGRAM.md)). Substrate: a **real pretrained
MNLI model** on **real** MNLI (benchmark) + **real** HANS (deployment). Cell
**XPROTO-LLM** — shakedown in progress; seal ≥ 2026-08-25. A "dark place": the
false-clear is silent (it looks fine on the leaderboard).

## Question

A model's **benchmark score is a certificate** — "capable enough, deploy it." The
deployment distribution is not the benchmark; the consumer's actual inputs are a
**footprint** the aggregate score is blind to. A benchmark-certified model
**false-clears** on the deployment slices where it fails — silently. The
false-clear is **consumer-relative**: which slice you serve decides whether the
certified model works. This is the KV-keys / XPROTO-AICSI lesson for AI evaluation:
minimising an *aggregate* metric is blind to what a specific consumer reads.

## Cell

**XPROTO-LLM** (`analysis/llm`): a real `roberta-large-mnli` that passes the MNLI
benchmark (~0.90) is deployed across the 30 **HANS** subcases (the consumer
footprints; McCoy et al.'s syntactic-heuristic challenge set). Certificate =
benchmark ≥ target → deploy everywhere; witness = the true per-slice accuracy.
naive trusts the aggregate benchmark; aware measures the slice footprint on a small
sample. Bars B1 naive_fc≥0.25 / B2 aware_fc≤0.10 / B3 dominance + MC1 model actually
passes the benchmark / MC2 consumer-relativity (per-slice spread) / MC3
non-degenerate. Substrate = real model + real data (the evidence rung); production
traffic / incident logs are the external-validity graduation.

## Why it's a dark place

The failure is invisible on the leaderboard — the model *did* pass the benchmark.
Naming the per-slice false-clear rate makes the eval-vs-deployment gap a measured,
first-class number rather than a post-incident surprise. The witness (ground-truth
on the deployment footprint) exists but is rarely graded against the benchmark
claim. HANS is the canonical demonstration that a benchmark can be aced while a
structured deployment slice collapses.
