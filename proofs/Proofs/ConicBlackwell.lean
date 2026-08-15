import Mathlib

/-!
# The conic residual bound behind GD-1b

`gd1b_exhibit_certificate.py` proves Blackwell incomparability rather than
thresholding a search residual. Its `conic_lower_bound` rests on one fact,
formalised here.

Setting: binary state, so a joint column is a point of `ℝ²`. If experiment `B`
is a garbling of `A`, every joint column of `B` is a conic combination of the
joint columns of `A`; with a binary state that forces its ratio into
`[r_min, r_max]`, the ratio range of `A`'s own columns. A column of `B` lying
outside that range therefore cannot be reached, and the distance by which it
misses is a *lower bound* on the garbling residual — not an artefact of the
search that looked for one.

The two lemmas below are the two sides of that range.
-/

namespace ConicBlackwell

/-- **Lower side.** The cone spanned by columns of ratio at least `r` is
`{c | r * c₁ ≤ c₀}`. If the target `(t₀, t₁)` sits below it (`t₀ < r * t₁`),
every cone point is at `L∞` distance at least `(r * t₁ - t₀) / (1 + r)`.

Formalisation note: the outside-the-cone hypothesis `t₀ < r * t₁` turns out to
be unnecessary for the inequality — inside the cone the numerator is
non-positive and the bound holds vacuously. It is needed only to make the
bound *positive*, which is `bound_pos` below. Stating it unconditionally is
strictly stronger and separates the estimate from the certificate. -/
theorem conic_residual_lower_bound
    {r t₀ t₁ c₀ c₁ : ℝ} (hr : 0 ≤ r)
    (hcone : r * c₁ ≤ c₀) :
    (r * t₁ - t₀) / (1 + r) ≤ max |c₀ - t₀| |c₁ - t₁| := by
  set d := max |c₀ - t₀| |c₁ - t₁| with hd
  have h1 : c₀ - t₀ ≤ d := le_trans (le_abs_self _) (le_max_left _ _)
  have h2 : t₁ - c₁ ≤ d := by
    calc t₁ - c₁ ≤ |t₁ - c₁| := le_abs_self _
      _ = |c₁ - t₁| := abs_sub_comm _ _
      _ ≤ d := le_max_right _ _
  have hpos : (0 : ℝ) < 1 + r := by linarith
  have key : r * (t₁ - c₁) ≤ r * d := mul_le_mul_of_nonneg_left h2 hr
  rw [div_le_iff₀ hpos]
  nlinarith [key, h1, hcone]

/-- **Upper side.** Symmetric statement for the other end of the ratio range:
the cone `{c | c₀ ≤ R * c₁}` and a target above it. -/
theorem conic_residual_lower_bound'
    {R t₀ t₁ c₀ c₁ : ℝ} (hR : 0 ≤ R)
    (hcone : c₀ ≤ R * c₁) :
    (t₀ - R * t₁) / (1 + R) ≤ max |c₀ - t₀| |c₁ - t₁| := by
  set d := max |c₀ - t₀| |c₁ - t₁| with hd
  have h1 : t₀ - c₀ ≤ d := by
    calc t₀ - c₀ ≤ |t₀ - c₀| := le_abs_self _
      _ = |c₀ - t₀| := abs_sub_comm _ _
      _ ≤ d := le_max_left _ _
  have h2 : c₁ - t₁ ≤ d := le_trans (le_abs_self _) (le_max_right _ _)
  have hpos : (0 : ℝ) < 1 + R := by linarith
  have key : R * (c₁ - t₁) ≤ R * d := mul_le_mul_of_nonneg_left h2 hR
  rw [div_le_iff₀ hpos]
  nlinarith [key, h1, hcone]

/-- The bound is strictly positive exactly when the target is outside the cone,
which is what makes it a *certificate* rather than a threshold. -/
theorem bound_pos
    {r t₀ t₁ : ℝ} (hr : 0 ≤ r) (hout : t₀ < r * t₁) :
    0 < (r * t₁ - t₀) / (1 + r) :=
  div_pos (by linarith) (by linarith)

/-! ## Why the cone is the right object

A garbling `B = A M` with `M` row-stochastic sends joint columns to
*nonnegative combinations* of joint columns, with the same weights: the prior
scales rows, and the garbler mixes columns, so the two commute. Cone
membership is then preserved because the defining constraint is linear and
homogeneous. Together these say the residual bound above applies to every
garbling, not merely to the ones a search happened to try. -/

/-- The prior scales rows, the garbler mixes columns, and the two commute:
the joint column of a garbled experiment is the same nonnegative combination
of the source's joint columns. -/
theorem joint_of_garbling {ι : Type*} (s : Finset ι) (p : ℝ) (A M : ι → ℝ) :
    p * (∑ x ∈ s, A x * M x) = ∑ x ∈ s, M x * (p * A x) := by
  rw [Finset.mul_sum]
  exact Finset.sum_congr rfl fun x _ => by ring

/-- Cone membership survives nonnegative combination. With `v₀ x, v₁ x` the two
coordinates of source joint column `x` and `w x ≥ 0` the garbler's weights, a
combination that stays in `{c | r * c₁ ≤ c₀}` cannot escape it. -/
theorem cone_closed_under_conic
    {ι : Type*} {s : Finset ι} {w v₀ v₁ : ι → ℝ} {r : ℝ}
    (hw : ∀ i ∈ s, 0 ≤ w i) (hv : ∀ i ∈ s, r * v₁ i ≤ v₀ i) :
    r * (∑ i ∈ s, w i * v₁ i) ≤ ∑ i ∈ s, w i * v₀ i := by
  rw [Finset.mul_sum]
  refine Finset.sum_le_sum fun i hi => ?_
  have hrw : r * (w i * v₁ i) = w i * (r * v₁ i) := by ring
  rw [hrw]
  exact mul_le_mul_of_nonneg_left (hv i hi) (hw i hi)

/-- The mirror, for the upper end of the ratio range. -/
theorem cone_closed_under_conic'
    {ι : Type*} {s : Finset ι} {w v₀ v₁ : ι → ℝ} {R : ℝ}
    (hw : ∀ i ∈ s, 0 ≤ w i) (hv : ∀ i ∈ s, v₀ i ≤ R * v₁ i) :
    (∑ i ∈ s, w i * v₀ i) ≤ R * ∑ i ∈ s, w i * v₁ i := by
  rw [Finset.mul_sum]
  refine Finset.sum_le_sum fun i hi => ?_
  have hrw : R * (w i * v₁ i) = w i * (R * v₁ i) := by ring
  rw [hrw]
  exact mul_le_mul_of_nonneg_left (hv i hi) (hw i hi)

/-! ## From joint columns back to likelihood columns

The certificate is computed on joint columns but the search that it bounds
works on likelihood columns. Since `joint = prior * likelihood` entrywise,
dividing by the *largest* prior weight turns a joint-column bound into a valid
likelihood-column bound — the direction that keeps it a lower bound. -/

/-- If a joint-coordinate residual is at least `bound`, the corresponding
likelihood residual is at least `bound / πmax`. Dividing by the largest prior
weight is what keeps this a lower bound rather than an overstatement. -/
theorem likelihood_residual_of_joint
    {p pmax dL dJ bound : ℝ}
    (hp : 0 < p) (hpmax : p ≤ pmax) (hJ : dJ = p * dL) (hb : bound ≤ |dJ|) :
    bound / pmax ≤ |dL| := by
  have hpmax0 : 0 < pmax := lt_of_lt_of_le hp hpmax
  have habs : |dJ| = p * |dL| := by rw [hJ, abs_mul, abs_of_pos hp]
  rw [div_le_iff₀ hpmax0]
  have h1 : p * |dL| ≤ pmax * |dL| :=
    mul_le_mul_of_nonneg_right hpmax (abs_nonneg _)
  have h2 : bound ≤ pmax * |dL| := by rw [habs] at hb; linarith
  linarith [h2]

end ConicBlackwell
