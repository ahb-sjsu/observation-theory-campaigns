# anti arm

**id.** anti-arm
**kind.** instrument

## definition

In a flip comparison, a third code built to destroy the consumer's read subspace at the same bits. It is expected to score worst, and a comparison in which it does not is not a flip. Chapter 4.

## equation

Book equation 4.5.

    \text{flip}:\quad \mathrm{task}(O)>\mathrm{task}(R)\ \ \text{and}\ \ \operatorname{tr}M^{O}_\delta>\operatorname{tr}M^{R}_\delta,\qquad \mathrm{task}(\text{anti})<\mathrm{task}(R),\qquad \text{bits}(O)=\text{bits}(R).

## ledger

- GO-2 (neg. half: not reconstruction). At matched bits, downstream preservation is not controlled by reconstruction error. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:63` at 7d91883.
- NEG-16 (KV serving, end-task). *At matched bits and matched reconstruction error, steering KV quantization error into the attention read subspace degrades LongBench task score by the registered floors on a deployed-class model.* Refuted at its registered effect sizes on this model and task. `[refuted]`. `geometric-observation/claims/LEDGER.md:92` at 7d91883.
- GO-B-whale (038). Sperm-whale coda dialect (DSWP/Sharma 2024), Clan classifier — cetacean communication; promotes the exploratory (A2) verdict to a sealed flip `[predicted]`. `geometric-observation/claims/LEDGER.md:120` at 7d91883.
- GO-B-blind (041). Blind, NON-ORACLE prospective flip on a fresh untouched domain (20 Newsgroups sci.space vs rec.autos), logistic classifier — the reviewer's decisive test: recover P_C non-oracle and commit the winning code + sign + magnitude *before* opening the test split `[predicted]`. `geometric-observation/claims/LEDGER.md:121` at 7d91883.

## first stated

Volume 14, chapter 8, `geometric-observation/chapters/ch08_value.md:1-30`, DOI 10.5281/zenodo.21776291, as the third arm of every registered flip.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.4 | the flip sealed in twelve domains and three physics, held in at least five domains and all three | `geometric-observation\chapters\ch08_value.md:40-70`; `geometric-observation\claims\LEDGER.md` rows GO-2, GO-B-AV163, D3, 038 |
| chapter 2 section 2.5 | whitened code wins at every budget | `geometric-observation\chapters\ch08_value.md:84-97` |
| chapter 4 section 4.3 | the flip definition, flip versus (A2) verdict | `geometric-observation\chapters\ch08_value.md:1-30,100-108` |
| chapter 4 section 4.3 | GO-2 0.0934 vs 0.0938, 2.53 times, 12 of 12, anti 21 times; retrieval 0.0964, negative 4.70 and positive 4.65, recon 0.40 | `geometric-observation\claims\LEDGER.md` rows GO-2 negative and positive halves |
| chapter 4 section 4.3 | acoustic 148 of 201, 201 of 201, 152 of 201; seismic 13 of 17, 17 of 17, 13 of 17; whale 0.934 vs 0.883, 2 times, 300 of 300; at least 5 domains and 3 physics; battery prediction met | `geometric-observation\chapters\ch08_value.md:40-70`; `geometric-observation\claims\LEDGER.md` rows GO-B-AV163, D3, 038 |
| chapter 4 section 4.3 | whitened code on whale 0.83, 0.85, 0.97 vs 0.41, 0.80, 0.89 | `geometric-observation\chapters\ch08_value.md:84-97` |
| chapter 4 section 4.4 | gradient compression anti 300 of 300, flip 27 percent, coupling boundary | `geometric-observation\chapters\ch08_value.md:108-116` |
| chapter 6 section 6.2 | whale clan classifier, 8718 codas, 0.934 vs 0.883, reconstructs twice as well, 300 of 300 | `geometric-observation\chapters\ch08_value.md:40-70`; `geometric-observation\claims\LEDGER.md` row 038 |

## failures and corrections

- NEG-16 (KV serving, end-task), `[refuted]`. *At matched bits and matched reconstruction error, steering KV quantization error into the attention read subspace degrades LongBench task score by the registered floors on a deployed-class model.* Refuted at its registered effect sizes on this model and task.

## conditions

- The anti arm is matched on bits with the other two codes, and its purpose is to show that the read subspace is what the comparison is about, since destroying it should be worst.
- A comparison in which the anti arm is not worst has not shown a flip, whatever the other two arms did.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/AntiArm.lean`, theorems `readDiag_le_max`, `readDiag_le_total`, `anti_arm_worst`, at observation-data-mining 43ea852.

## used in

*Data Mining as Observation* chapters 4, 6, 7, 12.

## related

flip, read-distortion, read-operator

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 97b2015, theory-radar 37c4e6c, observation-data-mining 43ea852, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
