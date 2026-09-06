# sealed

**id.** sealed
**kind.** instrument

## definition

Of a prediction, committed with its hash recorded before the measurement was run, so that anyone with the repository can verify it has not changed. Chapter 0 section 0.12.

## equation

Book equation 8.1.

    O_{\mathrm{harness}}=\big(C_{\mathrm{score}},\ G_{\mathrm{metric}},\ B=\text{folds}\times\text{samples}\times\text{seeds}\big).

## ledger

- OT-7. The damage form, trace pairing, rank, and loading covariance are GL(d)-invariant under `P' = A⁻ᵀPA⁻¹`, while spectrum, effective rank, principal angles, and water-filling are O(d)-only — consumer-weighted damage is a geometric scalar, and P3's cliff cannot be bought down by reparameterization. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:30` at 9f3829f.
- OT-11. Feedback-free staleness: streaming-retrieval damage tracks measured drift; derived-cadence re-allocation removes it. `[void]`. `geometric-observation/claims/LEDGER.md:48` at 9f3829f.

## first stated

The program's seal ledger, `observation-theory-campaigns/experiments/SEALS.md:1-10`, a seal being the registration id, the sealing commit, and the SHA-256 of the sealed file at that commit, and chapter 0 section 0.12 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 8 section 8.8 | seal = commit plus SHA-256 | `observation-theory-campaigns\experiments\SEALS.md:1-10` |
| chapter 8 section 8.8 | Second Crucible 1 of 5, four instrument deaths, rate-limit rule; Third Crucible 2 of 3 | `geometric-observation\claims\LEDGER.md:50`; `geometric-observation\crucible\OT-CRUCIBLE-3-VERDICT.md:1-20` |
| chapter 8 section 8.8 | declaration drafted 2026-08-17, sealed 2026-08-18, one count corrected, G2 | `geometric-observation\crucible\DECLARATION-V1.md:1-20`; `geometric-observation\crucible\OT-CRUCIBLE-4.md:31-35` |
| chapter 12 section 12.6 | XPROTO-LLM, benchmark 0.909, 0.920, 0.909, thirty slices, target 0.8, naive 0.333, aware 0.033, spread 0.380, deployment mean 0.736, six bars on three seeds, sealed 2026-08-25 at b61f7f1 | `observation-theory-campaigns\experiments\LLM-EVAL-TRACK.md:1-50`; `observation-theory-campaigns\analysis\llm\XPROTO-LLM-graded.json`; `observation-theory-campaigns\experiments\SEALS.md:85` |
| chapter 13 section 13.4 | sealed correction, 0.5 dB calibration, floors 4/6/4, 2/2/3, 1, slopes 0.1008, 0.1398, 0.1086, R² 0.7376, 0.9218, 0.6174, bars B1 to B4 and MC1 to MC4 all true, seeds 20260827 to 20260829, sealed 1d3de4a | `observation-theory-campaigns\analysis\csi\PREREG-XPROTO-CSI-SWEEP2.md:1-60`; `observation-theory-campaigns\analysis\csi\XPROTO-CSI-SWEEP2-graded.json`; `observation-theory-campaigns\experiments\SEALS.md:90` |

## failures and corrections

- `observation-theory-campaigns/ERRATA.md:111-120` at 859676b. ## Standing note on records and runners Two failures this session shared one shape. A record was committed from a runner later found defective, and the correction was left uncommitted where nothing reading the repository could see it. The rule adopted in response is that a rerun writes to a new path and never over a committed record, and that the superseded record stays in the repository naming what replaced it. See the PF4-007 subsection of `experiments/CAMPAIGN.md`.

## conditions

- A prediction is sealed when its file is committed and the commit and the content hash are recorded in the seal ledger before the measurement is run, so that anyone with the repository can verify it has not changed.
- A seal fixes the text, not its correctness. The version 1.0 declaration was sealed with one count wrong, and the correction is recorded beside the seal rather than by editing the sealed file.
- An unsealed exploration can be reported and cannot carry a claim, and the refuted refresh-floor law is the program's standing example.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Seal.lean`, theorems `changed_of_hash_ne`, `hash_eq_of_eq`, `exists_collision`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14.

## related

preregistration, ledger-class, certificate, refresh-floor

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
