# teacher forcing

**id.** teacher-forcing
**kind.** concept

## definition

Feeding a language model the correct text as context rather than its own earlier outputs. Chapter 0 section 0.11.

## equation

Book equation 0.22.

    \mathrm{PPL}=2^{H},\qquad H=-\frac1T\sum_{t=1}^{T}\log_2 p\big(w_t\mid w_{<t}\big).

Book equation 11.1.

    \cos\big(k,\hat k\big)=0.995\qquad\text{while}\qquad \mathrm{PPL}:\ 12.24\ \to\ 10643.

## ledger

- OT-4. Operator drift predicts a real long-generation degradation and a derived refresh intervention moves it. `[refuted]`. `geometric-observation/claims/LEDGER.md:36` at 7d91883.

## first stated

Chapter 0 section 0.11 of *Data Mining as Observation*, with the program's C-12 record in readscope, `readscope/CALIBRATION.md:600-660`.

## measurements

none

## failures and corrections

- OT-4, `[refuted]`. Operator drift predicts a real long-generation degradation and a derived refresh intervention moves it.

## conditions

- Feeding a model the correct text as context rather than its own earlier outputs. The forced and free runs agree exactly as long as the forced predictions match the reference, and they part at the first token the model gets wrong, after which the free run's context is no longer the reference's.
- Perplexity is measured under teacher forcing, so a good perplexity does not certify a free run. The C-12 record's thirteen-point difference vanished under teacher forcing, and the operator-drift claim it was meant to support is refuted in the ledger.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/TeacherForcing.lean`, theorems `free_eq_take`, `free_length`, `free_ne_of_error`, at observation-data-mining ea18182.

## used in

*Data Mining as Observation* chapters 0, 11.

## related

perplexity, drift, harness, deployment-mismatch

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 4a95b35, theory-radar 37c4e6c, observation-data-mining ea18182, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
