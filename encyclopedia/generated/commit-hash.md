# commit hash

**id.** commit-hash
**kind.** instrument

## definition

The fingerprint git assigns to a snapshot of a repository, which fixes the time at which a file existed in that state. Chapter 0 section 0.12.

## equation

Book equation 8.3.

    \Pr[\text{at least one of } m\text{ null tests passes}]=1-(1-\alpha)^{m},\qquad \alpha_{\mathrm{Bonferroni}}=\frac{\alpha}{m}.

## ledger

- OT-7. The damage form, trace pairing, rank, and loading covariance are GL(d)-invariant under `P' = A⁻ᵀPA⁻¹`, while spectrum, effective rank, principal angles, and water-filling are O(d)-only — consumer-weighted damage is a geometric scalar, and P3's cliff cannot be bought down by reparameterization. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:30` at 7d91883.

## first stated

Chapter 0 section 0.12 of *Data Mining as Observation*, with the program's seal ledger, `observation-theory-campaigns/experiments/SEALS.md:1-10`, where every seal is a registration id, a sealing commit, and a hash.

## measurements

none

## failures and corrections

none

## conditions

- The fingerprint git assigns to a snapshot of a repository, which fixes the time at which a file existed in that state. A changed hash proves a changed file and an equal hash is evidence, since a fixed-length digest of longer inputs cannot be injective.
- Every row of a sources table cites its commit, every seal records its sealing commit, and the book's own colophon names the commit it was built from, so that a number can be reproduced at the state it was measured in.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Seal.lean`, theorems `changed_of_hash_ne`, `hash_eq_of_eq`, `exists_collision`, at observation-data-mining 416c9a3.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14.

## related

hash, sealed, sources-table, preregistration

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 994ee12, theory-radar 37c4e6c, observation-data-mining 416c9a3, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
