# codebook

**id.** codebook
**kind.** concept

## definition

The small set of allowed values a quantizer replaces each number with. Chapter 0 section 0.11.

## equation

Book equation 4.2.

    D(b)=\sum_i s_i\sigma_i^{2}\,2^{-2b_i},\qquad s_i=v_i^{\top}P_C\,v_i,\qquad b_i^{\star}=\max\!\Big(0,\ \tfrac12\log_2\frac{s_i\sigma_i^{2}}{\theta}\Big),\qquad \sum_i b_i^{\star}=B,

Book equation 0.13.

    D(b)=\sum_i s_i v_i\,4^{-b_i},\qquad b_i=\max\!\Big(0,\ \tfrac12\log_2\frac{s_i v_i}{\theta}\Big),\qquad \sum_i b_i=B.

## ledger

- GO-7. A stored description's description rate and its conditional Landauer reset content are operationally separate resources: the same finite-$n$ code index needing $\hat R\approx0.67$ bits/symbol to describe is fully recoverable from retained side information at bin rate $0.26=0.39\hat R$, fails increasingly below its conditional content, and fails absolutely (err 1.00 at every bin rate) without $S$. `[replicated]`. `geometric-observation/claims/LEDGER.md:69` at 01e53bc.
- NEG-4. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL. `[refuted]`. `geometric-observation/claims/LEDGER.md:97` at 01e53bc.

## first stated

Chapter 0 section 0.11 and chapter 4 section 4.2 of *Data Mining as Observation*, with the six codebooks of ledger row GO-7 and the codebook confound of the honest negatives.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 4 section 4.2 | GO-6, d 8 and r 4, output at or below surrogate at or below reconstruction at every rate, about 500 times, gap 0.41 to 0.005, isotropic control collapses | `geometric-observation\claims\LEDGER.md` row GO-6; `geometric-observation\chapters\ch07_cost.md` |
| chapter 4 section 4.4 | GO-4 budget inversion, fixed m 10 rises, matched m 121, 126, 159 collapses, 3 seeds | `geometric-observation\claims\LEDGER.md` row GO-4 |
| chapter 6 section 6.2 | planted probe, overlap 0.936 vs 0.059, twelve of twelve, reconstruction 0.40, five of five | `geometric-observation\claims\LEDGER.md` row GO-1 |
| chapter 7 section 7.2 | curvature reader, identical reconstruction 0.298, flip twelve of twelve both, projected variance twelve of twelve, reconstruction Spearman negative 0.20, identity curvature tie | `geometric-observation\experiments\GO2-gradient-curvature-NOTES.md:1-40`; `geometric-observation\claims\LEDGER.md` row GO-B |
| chapter 7 section 7.2 | real logistic model, exact Hessian, anti 300 of 300, flip 82 of 300, coupling diagnosis, bound not refutation | `geometric-observation\claims\LEDGER.md` row GO-B-optim-D4 |
| chapter 9 section 9.3 | the margin certificate, mu crit as the expected maximum of N minus 1 standard normals, rho, death at 0.948 within 6 percent, Spearman 0.991 vs 0.873, fourteen corpora, six gates, the v1 to v3 path, the standing correction | `geometric-observation\experiments\GO3-certificate-vacuity-v3-NOTES.md:1-60`; `geometric-observation\claims\LEDGER.md` row GO-3 |
| chapter 11 section 11.7 | GO-1 overlap 0.936 vs 0.059, flip 12 of 12, reconstruction 0.40 | `geometric-observation\claims\LEDGER.md` row GO-1; `geometric-observation\chapters\ch10_the_blind_probe.md:34-52` |
| chapter 12 section 12.2 | recall 0.999 vs 0.592, the derived death point within 6 percent across fourteen corpora | `openvector-bench\README.md:60-96`; `geometric-observation\claims\LEDGER.md` row GO-3 |
| chapter 12 section 12.3 | uncompressed 0.79, centred 0.84 | `geometric-observation\claims\LEDGER.md` row GO-B-legal |
| chapter 12 section 12.3 | 041 non-oracle, frozen LSA TF-IDF to SVD 100 train-only, AUROC 0.975 vs 0.910, flip tied, magnitude overshot, partial | `geometric-observation\chapters\ch10_the_blind_probe.md:100-118`; `geometric-observation\claims\LEDGER.md` row GO-B-blind 041 |
| chapter 13 section 13.5 | GO-7, 0.67 bits per symbol, bin rate 0.26 equals 0.39, error 1.00 without side information, two families, six codebooks | `geometric-observation\claims\LEDGER.md` row GO-7 |
| chapter 13 section 13.5 | GO-8, 0.10 to 0.55 across ages 0 to 64, flip probability 0.05, 1 percent to 100 percent at age 32, Gaussian pass 5 of 5, the control-statistic caveat | `geometric-observation\claims\LEDGER.md` row GO-8; `geometric-observation\experiments\GO-landauer-gaussian-secondsettings-NOTES.md` |
| chapter 13 section 13.6 | attempt three, windows 1024, 256, 32, uncertainty 0.982 to 0.892, 5 of 6, 0.4375 with SE 0.070 at 5 percent keep vs 0.30, 97 percent eviction, oracle-miss 0.370 vs 0.25, V4 0.078 vs 0.0625, contrast 0.359 with SE 0.068, n 64, seed 20260812, 89 duty cycles | `geometric-observation\claims\LEDGER.md` row GO-2/GO-12/GO-13 operational; `geometric-observation\prereg\GO-P-2026-077-kv-consumer-relative.md`; `geometric-observation\results\GO13-kvaw2-governed.json` |

## failures and corrections

- NEG-4, `[refuted]`. Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL.

## conditions

- The small set of allowed values a quantizer replaces each input with, under the nearest-codeword rule. The distortion of an input is its distance to the nearest codeword, nonnegative, zero when the input is a codeword, achieved by some codeword, and never larger for a larger codebook.
- Two arms compared at unequal codebooks are not a flip comparison, which is the twenty-five percent codebook confound the ledger carries, and the reset content of a stored description is separate from its rate, which is row GO-7's finding across six codebooks.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Codebook.lean`, theorems `distortion_nonneg`, `distortion_codeword`, `distortion_anti`, `exists_nearest`, at observation-data-mining 17f3e9f.

## used in

*Data Mining as Observation* chapters 0, 4, 8, 11, 13.

## related

quantization, product-quantization, confound, flip

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 01e53bc, observation-theory-campaigns 0c2e3f9, theory-radar 37c4e6c, observation-data-mining 17f3e9f, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
