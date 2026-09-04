# deployment mismatch

**id.** deployment-mismatch
**kind.** concept

## definition

The failure in which the consumer that was evaluated is not the consumer that was deployed, or time moved between the two. Chapters 1 and 13.

## equation

Book equation 13.1.

    \mathrm{FC}=\Pr\big[W\ \text{refutes}\ \big|\ \mathcal C_t\ \text{clears}\big],\qquad d_O(\Delta)=\operatorname{tr}\big(P_C\,M_{\mathrm{drift}}(\Delta)\big),\qquad M_{\mathrm{drift}}(\Delta)=\mathbb E\big[\delta_\Delta\delta_\Delta^{\top}\big].

## ledger

- OT-4. Operator drift predicts a real long-generation degradation and a derived refresh intervention moves it. `[refuted]`. `geometric-observation/claims/LEDGER.md:36` at 7d91883.
- GO-2/GO-12/GO-13 operational (KV serving, 077). Consumer-relative access width measured on a production serving stack (Qwen2.5-7B KV-cache eviction, matched budget): task quality tracks measured predictive uncertainty u about the consumer's future reads, not nominal scorer width — the 32-query snapshot beats the 1024-query scorer +0.4375±0.070 at 5% keep (bar 0.30) and survives 97% eviction with zero drop, while wide-window scoring is statistically indistinguishable from random eviction at extreme budgets; the recency-hoarding starvation signature replicated across three disjoint prompt sets (oracle-miss gap 0.370 vs bar 0.25). The novel equal-uncertainty analytic-equality control (degradation-titrated, constructible by design) REFUTED its own equality prediction on the pre-registered branch: with calibration health 4×–130× inside gates, equal scalar u did NOT give equal quality (V4 +0.078 vs 0.0625 tolerance; the pre-registered ρ=0.03 contrast firmed to +0.359±0.068, 5.3 SE) — equal scalar uncertainty is insufficient, error structure matters, consistent with GO-13 Theorem 1's own r≥2 scoping of equal-q universality (a scalar-context privilege). Successor arc: 056 honest miss → 075 ID burned on a disclosed design failure → 077 sealed and split-verdict. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:81` at 7d91883.

## first stated

Chapter 1 section 1.7 and chapter 13 of *Data Mining as Observation*, with the program's case in the radio slice sweep, `observation-theory-campaigns/analysis/llm/PREREG-XPROTO-LLM.md`, and the serving-stack measurement of ledger row GO-2/GO-12/GO-13 operational.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 12 section 12.6 | XPROTO-LLM, benchmark 0.909, 0.920, 0.909, thirty slices, target 0.8, naive 0.333, aware 0.033, spread 0.380, deployment mean 0.736, six bars on three seeds, sealed 2026-08-25 at b61f7f1 | `observation-theory-campaigns\experiments\LLM-EVAL-TRACK.md:1-50`; `observation-theory-campaigns\analysis\llm\XPROTO-LLM-graded.json`; `observation-theory-campaigns\experiments\SEALS.md:85` |
| chapter 13 section 13.6 | attempt two, broken proxy, control did not exist, identifier burned, 16 prompts, 1360 s | `geometric-observation\prereg\GO-P-2026-077-kv-consumer-relative.md:1-15`; `geometric-observation\results\GO13-kvaw-pilot-disclosed.json` |
| chapter 13 section 13.6 | attempt three, windows 1024, 256, 32, uncertainty 0.982 to 0.892, 5 of 6, 0.4375 with SE 0.070 at 5 percent keep vs 0.30, 97 percent eviction, oracle-miss 0.370 vs 0.25, V4 0.078 vs 0.0625, contrast 0.359 with SE 0.068, n 64, seed 20260812, 89 duty cycles | `geometric-observation\claims\LEDGER.md` row GO-2/GO-12/GO-13 operational; `geometric-observation\prereg\GO-P-2026-077-kv-consumer-relative.md`; `geometric-observation\results\GO13-kvaw2-governed.json` |

## failures and corrections

- OT-4, `[refuted]`. Operator drift predicts a real long-generation degradation and a derived refresh intervention moves it.

## conditions

- The failure in which the consumer that was evaluated is not the consumer that was deployed, or time moved between the two. A deployment score is a weighted mean over the slices actually served, so it lies between the worst slice and the best, and a benchmark drawn from the best slice overstates it unless every weighted slice matches.
- The chapter's case scores 0.909 on the benchmark against a target of 0.8 and 0.736 on the deployment mean, and the six bars that separate the two are preregistered.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/DeploymentMismatch.lean`, theorems `deployment_le_max`, `min_le_deployment`, `deployment_lt_max_of_gap`, `book_numbers`, at observation-data-mining 9034ccc.

## used in

*Data Mining as Observation* chapters 1, 12.

## related

observer, certificate, coherence-time, min-over-strata

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 0c81b38, theory-radar 37c4e6c, observation-data-mining 9034ccc, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
