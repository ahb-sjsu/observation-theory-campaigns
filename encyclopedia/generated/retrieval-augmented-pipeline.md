# retrieval-augmented pipeline

**id.** retrieval-augmented-pipeline
**kind.** concept

## definition

A system that answers a question by chunking documents, embedding the chunks, indexing them, retrieving the nearest to the embedded question, and handing them to a generator. A chain of observers. Chapter 12.

## equation

Book equation 12.1.

    \begin{gathered} x\sim_{\text{stage}} x'\ \Longrightarrow\ x\sim_{\text{pipeline}} x'\quad\text{for every stage, differentiable or not}, \\ \operatorname{rank}P_{\text{run}}(x)\le\min_{\text{stages in the run}}\operatorname{rank}J_{\text{stage}}(x)\quad\text{on a differentiable run of stages, at each row.} \end{gathered}

Book equation 13.1.

    \mathrm{FC}=\Pr\big[W\ \text{refutes}\ \big|\ \mathcal C_t\ \text{clears}\big],\qquad d_O(\Delta)=\operatorname{tr}\big(P_C\,M_{\mathrm{drift}}(\Delta)\big),\qquad M_{\mathrm{drift}}(\Delta)=\mathbb E\big[\delta_\Delta\delta_\Delta^{\top}\big].

## ledger

- OT-11. Feedback-free staleness: streaming-retrieval damage tracks measured drift; derived-cadence re-allocation removes it. `[void]`. `geometric-observation/claims/LEDGER.md:48` at 7d91883.
- GO-B-legal (035→036). Legal-citation retrieval (CourtListener), cosine-ranking consumer, LaBSE embeddings — real large corpus, non-physical consumer `[predicted]`. `geometric-observation/claims/LEDGER.md:119` at 7d91883.

## first stated

Chapter 12 of *Data Mining as Observation*, with the program's streaming-retrieval staleness row OT-11 and the legal-citation retrieval flip.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 12 section 12.3 | 035 miss 0.773 vs 0.757, identifiability diagnosis, 036 blind probe r 32, 0.779 vs 0.771, 200 of 200, recon 0.220 vs 0.584, 039 virgin split 0.796 vs 0.780, margin 0.008 to 0.016, edges baseline | `geometric-observation\chapters\ch10_the_blind_probe.md:53-90`; `geometric-observation\claims\LEDGER.md` rows GO-B-legal 035 and 036, GO-P-2026-039 |
| chapter 12 section 12.3 | uncompressed 0.79, centred 0.84 | `geometric-observation\claims\LEDGER.md` row GO-B-legal |
| chapter 12 section 12.6 | XPROTO-LLM, benchmark 0.909, 0.920, 0.909, thirty slices, target 0.8, naive 0.333, aware 0.033, spread 0.380, deployment mean 0.736, six bars on three seeds, sealed 2026-08-25 at b61f7f1 | `observation-theory-campaigns\experiments\LLM-EVAL-TRACK.md:1-50`; `observation-theory-campaigns\analysis\llm\XPROTO-LLM-graded.json`; `observation-theory-campaigns\experiments\SEALS.md:85` |

## failures and corrections

none

## conditions

- A system that chunks documents, embeds the chunks, indexes them, retrieves the nearest to the embedded question, and hands them to a generator. Whatever one stage declares the same, every later stage and the pipeline declare the same, and for linear stages the rank of the composition is at most the rank of any stage, so the pipeline's read subspace is no larger than its narrowest stage's.
- Both hold for every stage, differentiable or not. The benchmark score of the whole is a certificate whose false-clear rate on deployment slices is the chapter's measurement.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Pipeline.lean`, theorems `quotient_inherited`, `quotient_inherited_chain`, `rank_comp_le_first`, `rank_comp_le_second`, at observation-data-mining ea18182.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 8, 10, 11, 12, 13, 14.

## related

quotient, read-subspace, deployment-mismatch, freshness

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 4a95b35, theory-radar 37c4e6c, observation-data-mining ea18182, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
