# hash

**id.** hash
**kind.** instrument

## definition

A short fixed-length fingerprint of a file, computed so that any change to the file changes the fingerprint. Chapter 0 section 0.12.

## equation

Book equation 8.3.

    \Pr[\text{at least one of } m\text{ null tests passes}]=1-(1-\alpha)^{m},\qquad \alpha_{\mathrm{Bonferroni}}=\frac{\alpha}{m}.

## ledger

- OT-7. The damage form, trace pairing, rank, and loading covariance are GL(d)-invariant under `P' = A⁻ᵀPA⁻¹`, while spectrum, effective rank, principal angles, and water-filling are O(d)-only — consumer-weighted damage is a geometric scalar, and P3's cliff cannot be bought down by reparameterization. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:30` at 7d91883.

## first stated

Chapter 0 section 0.12 of *Data Mining as Observation*, with the program's seal ledger, `observation-theory-campaigns/experiments/SEALS.md:1-10`, where every seal records a SHA-256.

## measurements

none

## failures and corrections

none

## conditions

- A short fixed-length fingerprint of a file, computed so that any change to the file changes the fingerprint. A changed hash proves a changed file, an unchanged file has an unchanged hash, and a digest with fewer values than there are files sends two distinct files to the same digest, so an equal hash is evidence and not proof.
- The seal ledger records the hash beside the commit, and the recognizer's templates and the probe's records carry theirs, so that a reader with the repository can check what was fixed before the measurement.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Seal.lean`, theorems `changed_of_hash_ne`, `hash_eq_of_eq`, `exists_collision`, at observation-data-mining 8d458b2.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14.

## related

sealed, preregistration, ledger-class, certificate

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 429cc9d, theory-radar 37c4e6c, observation-data-mining 8d458b2, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
