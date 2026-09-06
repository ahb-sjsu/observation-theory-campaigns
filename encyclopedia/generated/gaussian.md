# Gaussian

**id.** gaussian
**kind.** concept

## definition

The normal distribution, in many dimensions the one whose density falls with the Mahalanobis distance. An isotropic Gaussian has every direction the same. Chapter 9 and chapter 10.

## equation

Book equation 0.33.

    d_M(x)=\sqrt{(x-\mu)^{\top}\Sigma^{-1}(x-\mu)}.

Book equation 0.6.

    x_{\mathrm w}=\Sigma^{-1/2}(x-\mu),\qquad \Sigma^{-1/2}=\sum_i\lambda_i^{-1/2}\,v_i v_i^{\top}.

Book equation 9.3.

    \hat\mu=\frac{\bar s_{\mathrm{true}}-\bar s_{\mathrm{distr}}}{\sigma_{\mathrm{distr}}},\qquad \mu_{\mathrm{crit}}=\mathbb E\Big[\max_{N-1}\mathcal N(0,1)\Big],\qquad \rho=\frac{\hat\mu}{\mu_{\mathrm{crit}}},\qquad \rho=1\ \text{vacuous}.

## ledger

- GO-3. The certificate's vacuity threshold predicts where single-stage retrieval dies. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:65` at 9f3829f.
- GO-8. On two independent source families (binary Markov; Gaussian AR(1)), a fixed stored record's operational reset threshold rises with the age of the retained side information exactly as the staleness–work complement prices it: same record, same bins, same decoder — the decodable bin rate climbs $0.10\to0.55$ bits/symbol across ages 0–64 of a $p=0.05$ Markov chain, tracking $R_c-1+h_2(\hat d \ast q_t)$ within one grid step at every age, and a fixed bin rate flips from 1% error (age 0) to 100% (age 32). `[replicated]`. `geometric-observation/claims/LEDGER.md:71` at 9f3829f.

## first stated

Chapter 9 section 9.3 and chapter 10 section 10.3 of *Data Mining as Observation*, with the isotropic Gaussian control in `turboquant-pro/turboquant_pro/anatomy.py:98-170`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 10 section 10.3 | hierarchical typing, tails 0.95 and 0.85, prescriptions, two designs that died, correlation above 0.8 on an isotropic Gaussian | `turboquant-pro\turboquant_pro\anatomy.py:98-170` |
| chapter 13 section 13.5 | GO-8, 0.10 to 0.55 across ages 0 to 64, flip probability 0.05, 1 percent to 100 percent at age 32, Gaussian pass 5 of 5, the control-statistic caveat | `geometric-observation\claims\LEDGER.md` row GO-8; `geometric-observation\experiments\GO-landauer-gaussian-secondsettings-NOTES.md` |

## failures and corrections

none

## conditions

- The normal distribution, in many dimensions the one with density falling with the Mahalanobis distance. An isotropic Gaussian has every direction the same, so every reader reads the same variance and no code can flip, and whitening turns any Gaussian into an isotropic one.
- The isotropic Gaussian is the control on which hub typing correlated above 0.8 with nothing, and the Gaussian pass of GO-8 was five of five with the control-statistic caveat.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Isotropy.lean`, theorems `isotropic_reads_same`, `isotropic_no_flip`, `anisotropic_readers_differ`, `flip_iff_anisotropic`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/Mahalanobis.lean`, theorems `dM2_nonneg`, `dM2_mean`, `dM2_scale`, `dM2_eq_whitened`, `dM2_antitone_in_variance`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 9, 10, 11, 13.

## related

isotropic, mahalanobis-distance, null-model, whitening, standard-error

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
