# rank certificate

**id.** rank-certificate
**kind.** instrument

## definition

A bound, computed from a compressed representation, that certifies which neighbour rankings the compression preserved for a consumer and which it did not. In its strict setting the floor is a guarantee, in its percentile setting an estimate. A vacuous result proves nothing about the corpus and is an instruction to fall back to exact reranking. Chapter 11.

## equation

Book equation 11.2.

    \begin{gathered} r=\frac{d_{\mathrm{compressed}}}{d_{\mathrm{exact}}},\qquad \kappa_{\text{strict}}=\frac{\max r}{\min r},\qquad \tau\ \ge\ 1-2\hat\mu(\kappa_{\text{strict}}),\qquad \rho_S\ \ge\ 1-3\hat\mu(\kappa_{\text{strict}}), \\ \kappa_{97.5/2.5}=\frac{q_{97.5}(r)}{q_{2.5}(r)}\ \text{ gives the same two expressions as estimates, not floors.} \end{gathered}

Book equation 11.3.

    \begin{gathered} \mathrm{recall}@k=\frac{\big|\text{returned top-}k\ \cap\ \text{true top-}k\big|}{k}, \\ \text{true top-}k\text{ computed from the uncompressed vectors}. \end{gathered}

## ledger

- GO-3. The certificate's vacuity threshold predicts where single-stage retrieval dies. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:65` at 7d91883.

## first stated

The compression program's certificate specification, `turboquant-pro/docs/CERTIFICATE_SPEC.md`, DOI 10.5281/zenodo.20660087, and chapter 11 section 11.3 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 4 section 4.5 | truncation claim reproducible, loses on compact sets | `turboquant-pro\CLAIMS.md:28-49` |
| chapter 8 section 8.9 | 13.7 ROUGE-L, 0.25/4.19/9.60/13.7 at 64/128/256/512, re-validation negative 0.31 n=40, 26.64 under symmetric nf4, `_quant_nf4a_group` unchanged since `289bdfc` before `4f7baab` | `turboquant-pro\CLAIMS.md:63-81`; `turboquant-pro\benchmarks\kvquant_matrix\REVAL-2026-08-08.md` |
| chapter 9 section 9.3 | the margin certificate, mu crit as the expected maximum of N minus 1 standard normals, rho, death at 0.948 within 6 percent, Spearman 0.991 vs 0.873, fourteen corpora, six gates, the v1 to v3 path, the standing correction | `geometric-observation\experiments\GO3-certificate-vacuity-v3-NOTES.md:1-60`; `geometric-observation\claims\LEDGER.md` row GO-3 |
| chapter 11 section 11.2 | cosine 0.995 | `turboquant-pro\README.md:86-88`; `turboquant-pro\CLAIMS.md` row `kv_keys_per_channel` |
| chapter 11 section 11.3 | tau floor 1 minus 2 mu, Spearman floor 1 minus 3 mu, example kappa 1.0148, mu 0.0664, floor 0.8671, 19900 pairs, max certifiable 1.83, vacuous means exact rerank, sha256 binding, reference field and the 0.3 overlap difference | `turboquant-pro\docs\CERTIFICATE_SPEC.md:1-80` |
| chapter 11 section 11.5 | 9.6x at recall 0.999 CI-gated on GloVe 1.18M; 32x at 0.9993 on private 199k LaBSE, ties OPQ, beats RaBitQ, 20x build; 27.7x and 114x reported; PCA truncation loses on compact sets; 20x at 199k and 4x at 1M over OPQ; RaBitQ builds in under a second | `turboquant-pro\CLAIMS.md:28-49` |
| chapter 11 section 11.5 | CI fails when CLAIMS.md and claims.yaml disagree | `turboquant-pro\CLAIMS.md:1-27`; `turboquant-pro\tests\test_claims_ledger.py` |

## failures and corrections

- `turboquant-pro/turboquant_pro/rank_certificate.py:25-36` at 856c4cb. * **Strict** (``lo=0, hi=100``): kappa is the true worst-case distortion (max/min per-pair ratio). The bound is then unconditional -- a genuine distribution-free floor over *all* pairs -- but a single collapsed or near-duplicate pair (ratio -> 0 or huge) sends kappa -> inf and makes the certificate vacuous, so it is brittle to data-artifact pairs. * **Robust** (the ``lo=2.5, hi=97.5`` default): kappa is the percentile-robust distortion, trimming the most-distorted ~5% of pairs. This is the sensible default and matches the source paper's torus protocol, but the resulting floor is **conditional**: it holds for the central 95% of pairs, *not* unconditionally over all of them. The trimmed tail can invert arbitrarily, so the reported floor is a robust estimate, not a hard worst-case guarantee. Use the strict regime when you need the unconditional bound.

## conditions

- In the strict setting, the zeroth and hundredth percentiles of the distance ratio, the floor is a guarantee for the anchor sample, broken by a single collapsed pair.
- In the percentile setting the implementation computes the distortion on the retained central pairs and the concentration over all pairs, and the floor is a robust estimate, not a guarantee on either set.
- The floor is about the global ordering of the sampled pairwise distances. It does not directly certify a query's top-k recall, one query's neighbour order, or the trimmed tail.
- A floor on a sample of anchors is a statement about that sample. Carrying it to the corpus needs a sampling argument the certificate records the inputs for and does not supply.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/RankCertificate.lean`, theorems `nn_preserved`, `nn_preserved_of_kappa_one`, `kappa_ge_one`, at observation-data-mining 7aab08c.

## used in

*Data Mining as Observation* chapters 11.

## related

certificate, vacuity-threshold, flip, hubness

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 92c643b, theory-radar 37c4e6c, observation-data-mining 7aab08c, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
