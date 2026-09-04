# identity reader

**id.** identity-reader
**kind.** concept

## definition

The consumer whose read operator is the identity, for which read distortion is mean squared error. Every consumer-blind metric assumes it. Chapter 0 section 0.5.

## equation

Book equation 0.10.

    d_O=\operatorname{tr}(P_C\,M_\delta)=\mathbb E\!\left[\delta^{\top}P_C\,\delta\right],\qquad M_\delta=\mathbb E\!\left[\delta\delta^{\top}\right],\qquad P_C=I\ \Rightarrow\ d_O=\operatorname{tr}M_\delta.

Book equation 1.2.

    d_O=\operatorname{tr}(P_C\,M_\delta),\qquad \big(d_O=\operatorname{tr}M_\delta\ \text{ for every admissible } M_\delta\big)\ \Longleftrightarrow\ P_C=I.

Book equation 4.1.

    d_O=\operatorname{tr}(P_C\,M_\delta)\qquad\text{against}\qquad \operatorname{tr}M_\delta=d_O\big|_{P_C=I}.

## ledger

- GO-2 (neg. half: not reconstruction). At matched bits, downstream preservation is not controlled by reconstruction error. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:63` at 7d91883.

## first stated

Volume 14, chapter 2, `geometric-observation/chapters/ch02_failure_of_observer_free_measurement.md`, DOI 10.5281/zenodo.21776291, where reconstruction error is the distortion of the reader that reads every direction equally.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.4 | three virtues one vice, the identity slice | `geometric-observation\chapters\ch02_failure_of_observer_free_measurement.md:1-40` |
| chapter 1 section 1.4 | cosine 0.995 and perplexity of order ten thousand, the recalibration negative | `geometric-observation\chapters\ch02_failure_of_observer_free_measurement.md:40-60`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-2 and NEG-4; `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |
| chapter 1 section 1.4 | the flip sealed in twelve domains and three physics, held in at least five domains and all three | `geometric-observation\chapters\ch08_value.md:40-70`; `geometric-observation\claims\LEDGER.md` rows GO-2, GO-B-AV163, D3, 038 |
| chapter 4 section 4.3 | GO-2 0.0934 vs 0.0938, 2.53 times, 12 of 12, anti 21 times; retrieval 0.0964, negative 4.70 and positive 4.65, recon 0.40 | `geometric-observation\claims\LEDGER.md` rows GO-2 negative and positive halves |
| chapter 4 section 4.5 | GloVe table, 73 percent at 64 components, 0.685 vs 0.862 and 0.866, 0.906 at matched bytes, 0.989 at 37 bytes, 768 to 256 keeps about 99 percent, the 95 percent rule | `turboquant-pro\benchmarks\RESULTS_glove.md:1-40` |

## failures and corrections

none

## conditions

- Read distortion equals the trace of the error's second moment for every admissible error exactly when the read operator is the identity. A particular error can make the two agree by accident.
- Explained variance and the rule of picking rank at 95 percent are the identity reader's criteria, and the book records them as the benchmark's rules rather than its own.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ReadDistortion.lean`, theorems `read_distortion`, `identity_reader`, `quad_one`, at observation-data-mining a9fd869.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 8, 9, 10, 12, 13.

## related

read-operator, read-distortion, flip, quotient

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns c5a03d7, theory-radar 37c4e6c, observation-data-mining a9fd869, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
