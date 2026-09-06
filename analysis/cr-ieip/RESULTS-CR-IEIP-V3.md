# RESULTS — PREREG-CR-IEIP-V3 graded family (the locality law)

**Verdict: FAIL** (as executed; prereg sealed 2026-09-05, cells graded
2026-09-06). The locality law does not hold: consumer-metric false-clear
advantage is **not** a monotone function of transform locality Λ. Four of the
eight bar-bearing units fail their arm, and P2 monotonicity is essentially
zero (Spearman −0.055, floor 0.70). MC-S sufficiency is satisfied (six local
units, two non-local), so this is a valid FAIL, not a VOID. Records:
`cr_ieip_cell{H,I,J,K,L}_result.json`, `v3_lambda.json` (measured Λ by the
sealed identity-map gate), `cr_ieip_v3_lambda.py` and `lambda_checksum.py`
(the gate machinery; the checksum reproduces the V2 post-hoc identity numbers
per the seal record). State caches on Atlas at
`/home/claude/cr-ieip/ieip_cell{H..L}_states.npz`.

## Graded table (Λ measured before grading; arm by measured Λ, not prediction)

Δ = fc_raw − fc_true (the consumer-metric advantage). Local arm (Λ ≥ 0.20)
bar Δ ≥ +0.05; non-local arm (Λ ≤ −0.20) bar Δ ≤ +0.01; Λ in (−0.20, 0.20)
is the transition band, reported descriptively with no bar. Two graded units
per cell (the mid-two layers): 0.5B → L12/L18, 1.5B → L14/L21.

| cell (model × transform) | layer | Λ (measured) | arm (predicted) | fc raw → true | Δ | bar | result |
|---|---|---|---|---|---|---|---|
| H (0.5B × synonym) | 12 | +0.872 | LOCAL (local) | 0.4535 → 0.3256 | +0.128 | Δ ≥ +0.05 | PASS |
| H | 18 | +0.854 | LOCAL (local) | 0.4070 → 0.2442 | +0.163 | Δ ≥ +0.05 | PASS |
| I (1.5B × shuffle) | 14 | +0.144 | **BAND (local)** | 0.2869 → 0.4708 | −0.184 | descriptive | (band) |
| I | 21 | −0.006 | **BAND (local)** | 0.2813 → 0.3649 | −0.084 | descriptive | (band) |
| J (0.5B × truncate) | 12 | −0.802 | NON-LOCAL (non-local) | 0.8465 → 0.6614 | +0.185 | Δ ≤ +0.01 | **FAIL** |
| J | 18 | −0.723 | NON-LOCAL (non-local) | 0.7913 → 0.6024 | +0.189 | Δ ≤ +0.01 | **FAIL** |
| K (1.5B × synonym) | 14 | +0.802 | LOCAL (local) | 0.5437 → 0.4250 | +0.119 | Δ ≥ +0.05 | PASS |
| K | 21 | +0.767 | LOCAL (local) | 0.5312 → 0.4062 | +0.125 | Δ ≥ +0.05 | PASS |
| L (0.5B × shuffle) | 12 | +0.385 | LOCAL (local) | 0.3349 → 0.4245 | −0.090 | Δ ≥ +0.05 | **FAIL** |
| L | 18 | +0.297 | LOCAL (local) | 0.3255 → 0.3443 | −0.019 | Δ ≥ +0.05 | **FAIL** |

**P1 (the verdict): FAIL.** Every graded unit must pass its arm bar. Four do
not: J at both layers (deeply non-local yet the largest advantage in the
family) and L at both layers (measured local yet a negative advantage).

**P2 (monotonicity, secondary): FAIL.** Spearman(Λ, Δ) = **−0.055** over all
ten units (−0.214 over the eight bar-bearing units). Floor was 0.70. There is
no monotone relationship; the sign is slightly negative.

**MC-S (sufficiency): satisfied.** Six units land local (Λ ≥ 0.20), two land
non-local (Λ ≤ −0.20). Both arms populated, so the family is a valid FAIL.

Arm-vs-prediction mismatch (reportable per the seal): cell I (1.5B shuffle),
predicted the local discriminator, measured into the transition band at both
layers (Λ = +0.144, −0.006). The 1.5B shuffle is less representation-local
than the 0.5B design probe suggested (0.446/0.360 at 0.5B).

## What the family says

The advantage does not track locality. It appears strongly at **both**
extremes of Λ and vanishes or reverses in the middle:

- **Synonym (most local, Λ ≈ 0.77–0.87):** advantage present at both scales,
  +0.119 to +0.163. As the law predicts.
- **Truncate-half (most non-local, Λ ≈ −0.72 to −0.80):** the **largest**
  advantage in the family, +0.185/+0.189 — the exact opposite of the law's
  prediction of no advantage. The false-clear rates are high across the board
  (raw ≈ 0.79–0.87), yet the consumer read still strips ~19 points off them.
- **Shuffle (the discriminator, Λ ≈ −0.01 to +0.39):** **negative** advantage
  at every layer (−0.019 to −0.184). The cell the prereg named as the one
  that would distinguish the locality law from the ρ̂-fit law is exactly where
  the law breaks: representation-local by Λ, no advantage in fact.

So identity-map locality Λ is not the regime variable. This is the **third**
proposed gating variable to fail across three sealed families: nothing (V1),
ρ̂ held-out fit (V2), identity-map locality (V3).

The V2 story also needs qualifying. V2 read the paraphrase inversion as "the
transform is non-local, so patching is anti-informative." Truncate-half is
non-local too (Λ ≈ −0.75, more negative than several V2 bt units) and it does
**not** invert; it gives the biggest advantage here. Non-locality alone does
not predict inversion. The two transforms that lose the advantage (shuffle,
paraphrase) reorder or rewrite tokens while preserving length and surface
plausibility; the two that keep it (synonym, truncate) either barely move the
tokens or delete them outright. Whatever governs the advantage is closer to
whether the true decision-relevant change survives into the patched residual
than to any single scalar measured on the representation. No variable is
sealed to that; it is a hypothesis for a future family, not a claim here.

## Standing of the arc after three sealed families

- The mid-layer consumer-read advantage is **sealed-confirmed again** for the
  clearly-local transform: synonym at both scales (H, K), +0.119 to +0.163,
  adding to the backtranslation confirmations from B/D/E-L14/G-L14.
- The phenomenon is real and replicated; what keeps failing is the **forecast**
  — which transform gets the advantage. Three scalars have now missed.
- The paraphrase-inversion reading from V2 is complicated by truncate: a
  non-local transform that does not invert. "Non-local ⇒ inversion" is not a
  law.
- No V4 is drafted by this document. The natural next probe is a
  perturbation-survival measure (how much of the true δ the patched residual
  recovers) rather than a property of the representation alone, but that is a
  new family with its own seal, not an amendment here.

## Sizing ledger additions (time -v peaks)

J 13.80 GiB (0.5B truncate), K 11.69 GiB (1.5B synonym), L 11.82 GiB (0.5B
shuffle); all `rc=0`. H (0.5B synonym) and I (1.5B shuffle) ran in the same
envelope in the earlier waves.
