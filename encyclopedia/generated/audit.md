# audit

**id.** audit
**kind.** instrument

## definition

A check of a number or system against its record by a reader who did not produce it, bound to a sealed file. Chapter 8 section 8.9 and chapter 14 section 14.1.

## equation

Book equation 8.1.

    O_{\mathrm{harness}}=\big(C_{\mathrm{score}},\ G_{\mathrm{metric}},\ B=\text{folds}\times\text{samples}\times\text{seeds}\big).

Book equation 14.2.

    \mathrm{coverage\ difference}_c=\mathrm{AUROC}_c(\text{embedding})-\mathrm{AUROC}_c(\text{validated axes}),\qquad \text{floor}\approx0.08\ \text{to}\ 0.12.

Book equation 13.2.

    \begin{gathered} T_{\mathrm{coh}}=\frac{0.423}{f_D}, \\ \text{refuted fit:}\ \ \phi\approx0.177\,T_{\mathrm{coh}}\ (R^{2}=0.915), \qquad \text{sealed:}\ \ \phi\le 6\ \text{TTI at }10\ \text{Hz},\ \ 1\ \text{TTI at}\ \ge50\ \text{Hz}. \end{gathered}

## ledger

- NEG-15 (Bell boundary). *Query-conditioned hubness supplies a mechanism for Bell-inequality violation without action at a distance.* Refuted as a mechanism; the settings-as-queries reframing survives only as vocabulary. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:93` at 9f3829f.
- GO-B-legal (035→036). Legal-citation retrieval (CourtListener), cosine-ranking consumer, LaBSE embeddings — real large corpus, non-physical consumer `[predicted]`. `geometric-observation/claims/LEDGER.md:119` at 9f3829f.

## first stated

Chapter 8 section 8.9 and chapter 14 section 14.1 of *Data Mining as Observation*, with the audit binding in `xbse/README.md:195-219` and the Bell audit in `geometric-observation/articles/2026-08-03`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.6 | Bell audit, max S 2.00000 across 72 configurations, d 3 to 128, correlation negative 0.036, post-selected 2.7308, controls 2.748, 2.386, 3.174, seed 20260817, sealed at 6e825d8 | `geometric-observation\articles\2026-08-03-hubness-does-not-weaken-bell.md:1-60`; `geometric-observation\claims\LEDGER.md` row NEG-15; `geometric-observation\results\GO-bell-geometry-audit.json` |
| chapter 8 section 8.9 | twenty-seven errors, four in checking tools | `constraint-gap-measurements\README.md:273-282` |
| chapter 14 section 14.1 | the three questions, the trust beats, the audit binding | `gtc-prototype\README.md:10-58`; `xbse\README.md:195-219` |

## failures and corrections

none

## conditions

- A check of a published number or system against its record, by a reader who did not produce it. An audit binds a verdict to a sealed file whose digest proves it unchanged, and a witness's disagreement with a certificate is the audit's finding.
- The audit of the measurement notes found twenty-seven errors, four in the checking tools, and the constraint-first Bell audit reached a maximum of 2.00000 across 72 configurations.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Seal.lean`, theorems `changed_of_hash_ne`, `hash_eq_of_eq`, `exists_collision`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/Certificate.lean`, theorems `falseClear_mul_coverage`, `coverage_empty`, `falseClear_mem_unit`, `minOverStrata_passes_iff`, `minOverStrata_le_weighted_mean`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 1, 2, 3, 4, 8, 12, 14.

## related

sealed, witness, certificate, false-clear-rate, registered

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
