# surrogate

**id.** surrogate
**kind.** instrument

## definition

A quadratic stand-in for the consumer's output metric, the read distortion, used to allocate bits when the output itself cannot be. Chapter 4 section 4.2.

## equation

Book equation 4.2.

    D(b)=\sum_i s_i\sigma_i^{2}\,2^{-2b_i},\qquad s_i=v_i^{\top}P_C\,v_i,\qquad b_i^{\star}=\max\!\Big(0,\ \tfrac12\log_2\frac{s_i\sigma_i^{2}}{\theta}\Big),\qquad \sum_i b_i^{\star}=B,

Book equation 4.6.

    \kappa=\operatorname{tr}\big(\bar P_C\,\bar\Sigma_x\big)\in[0,1],\qquad \kappa\to1\ \text{is the coupling null (no flip)}.

Book equation 0.11.

    P_C(x)=J(x)^{\top}G\big(C(x)\big)\,J(x),\qquad J(x)=\frac{\partial C}{\partial x}(x),\qquad \bar P_{C,\mu}=\mathbb E_{\mu}\!\left[P_C(x)\right].

## ledger

- GO-6. At matched rate, output coding ≤ surrogate ≤ reconstruction on the consumer metric; the output–reconstruction gap is governed by the $\ker P_C$ entropy share, and the surrogate–output gap vanishes as rate grows. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:68` at 9f3829f.
- NEG-9. The projected-variance trace tr(P_C·Σ_δ) is a complete rank statistic for softmax-KL across all arms. `[refuted]`. `geometric-observation/claims/LEDGER.md:102` at 9f3829f.

## first stated

Chapter 4 section 4.2 of *Data Mining as Observation*, with the surrogate ordering in `geometric-observation/claims/LEDGER.md` row GO-6.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 4 section 4.2 | water-filling formula, directions below the water get no bits, the surrogate caveat | `readscope\readscope\allocate.py:1-100` |
| chapter 4 section 4.2 | GO-6, d 8 and r 4, output at or below surrogate at or below reconstruction at every rate, about 500 times, gap 0.41 to 0.005, isotropic control collapses | `geometric-observation\claims\LEDGER.md` row GO-6; `geometric-observation\chapters\ch07_cost.md` |

## failures and corrections

- NEG-9, `[refuted]`. The projected-variance trace tr(P_C·Σ_δ) is a complete rank statistic for softmax-KL across all arms.

## conditions

- A quadratic stand-in for the consumer's output metric, the read distortion, used to allocate bits when the output itself cannot be. The read distortion is a quadratic form in the read operator, and two readers at different angles rank the same two errors differently.
- At every rate the output coder is at or below the surrogate, which is at or below reconstruction, and the surrogate-to-output gap shrinks from 0.41 to 0.005 as the rate grows, while the read distortion is a control and not a complete rank statistic.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ReadDistortion.lean`, theorems `read_distortion`, `identity_reader`, `quad_one`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/Isotropy.lean`, theorems `isotropic_reads_same`, `isotropic_no_flip`, `anisotropic_readers_differ`, `flip_iff_anisotropic`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 4, 8.

## related

read-distortion, distortion, output-metric, identity-reader, flip-the

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
