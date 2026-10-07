import Mathlib

/-!
# Deductive claims of the WCNC 2027 paper, machine-checked

"One Report Cannot Serve Every Budget" makes a handful of claims that follow from
definitions or arithmetic rather than from simulation. This file proves them.

* `overrun_hundredfold`: the overrun `Ω(β) = B/β` of one achieved rate `B`
  against a budget a hundred times stricter is exactly a hundred times larger,
  whatever `B` is (Sec. III: "partly mechanical and we say so").
* `olla_equilibrium`, `olla_pushes_up`, `olla_pushes_down`: with
  `δdn = δup (1-β)/β`, the mean OLLA offset drift vanishes exactly when the NACK
  rate equals `β`, and points toward `β` otherwise (Sec. II, Eq. (3)).
* `zero_count_bound`, `rule_of_three_6000`, `rule_of_three_400`: zero events in
  `n` trials with `n p = 3` exclude the rate `p` at the 95 % level, so the fresh
  rates in Sec. V sit below `5e-4` and a zero-error curve point at 400 blocks
  below `7.5e-3` (Sec. II).
* `diversity_product`, `diversity_margin`: three independent branches each
  failing at most 3 % fail together more than thirty times below the `1e-3`
  budget (Sec. II; the measured margin is about fifty).
* `pick_antitone`, `expected_bler_antitone`: in the selection rule Eq. (1) a
  larger backoff never picks a higher MCS, so with error curves ordered by MCS
  it never raises the expected BLER.
* `doppler_*`: 10 Hz and 50 Hz at 3.5 GHz are about 3 km/h and 15 km/h.
-/

namespace WcncCsi

/-! ## Overrun -/

/-- Budget overrun of an achieved block error rate `B` against budget `β`. -/
noncomputable def overrun (B β : ℝ) : ℝ := B / β

theorem overrun_hundredfold (B : ℝ) : overrun B 1e-3 = 100 * overrun B 1e-1 := by
  unfold overrun
  ring

/-! ## OLLA equilibrium -/

/-- Mean offset drift per TTI at NACK rate `p`: up on ACK, down on NACK. -/
noncomputable def drift (δ β p : ℝ) : ℝ := (1 - p) * δ - p * (δ * (1 - β) / β)

theorem drift_eq {δ β p : ℝ} (hβ : 0 < β) : drift δ β p = δ * (β - p) / β := by
  unfold drift
  field_simp
  ring

theorem olla_equilibrium {δ β p : ℝ} (hβ : 0 < β) (hδ : 0 < δ) :
    drift δ β p = 0 ↔ p = β := by
  rw [drift_eq hβ]
  constructor
  · intro h
    rcases (div_eq_zero_iff.mp h) with h1 | h1
    · rcases mul_eq_zero.mp h1 with h2 | h2
      · linarith
      · linarith
    · linarith
  · intro h
    subst h
    simp

theorem olla_pushes_up {δ β p : ℝ} (hβ : 0 < β) (hδ : 0 < δ) (hp : p < β) :
    0 < drift δ β p := by
  rw [drift_eq hβ]
  exact div_pos (mul_pos hδ (by linarith)) hβ

theorem olla_pushes_down {δ β p : ℝ} (hβ : 0 < β) (hδ : 0 < δ) (hp : β < p) :
    drift δ β p < 0 := by
  rw [drift_eq hβ]
  exact div_neg_of_neg_of_pos (mul_neg_of_pos_of_neg hδ (by linarith)) hβ

/-- Table I: `δdn = 0.1 (1 - 0.1)/0.1 = 0.9` dB. -/
theorem olla_down_step : (0.1 : ℝ) * (1 - 0.1) / 0.1 = 0.9 := by norm_num

/-! ## Zero-count bounds -/

theorem exp_neg_three_lt : Real.exp (-3) < 0.05 := by
  have e1 := Real.exp_one_gt_d9
  have h3 : Real.exp 3 = Real.exp 1 ^ 3 := by
    rw [← Real.exp_nat_mul]
    norm_num
  have h20 : (20 : ℝ) < Real.exp 3 := by
    rw [h3]
    calc (20 : ℝ) < 2.7182818283 ^ 3 := by norm_num
      _ < Real.exp 1 ^ 3 := by gcongr
  have hprod : Real.exp (-3) * Real.exp 3 = 1 := by
    rw [← Real.exp_add]
    norm_num
  nlinarith [Real.exp_pos (-3)]

/-- Zero events in `n` independent trials exclude any rate `p` with `n p = 3`
at the 95 % level: the chance of seeing none is below `0.05`. -/
theorem zero_count_bound {p : ℝ} {n : ℕ} (hp1 : p ≤ 1)
    (h : (n : ℝ) * p = 3) : (1 - p) ^ n < 0.05 := by
  have h1 : 1 - p ≤ Real.exp (-p) := by linarith [Real.add_one_le_exp (-p)]
  have h2 : (1 - p) ^ n ≤ Real.exp (-p) ^ n := pow_le_pow_left₀ (by linarith) h1 n
  have h3 : Real.exp (-p) ^ n = Real.exp (-3) := by
    rw [← Real.exp_nat_mul]
    congr 1
    linarith
  calc (1 - p) ^ n ≤ Real.exp (-3) := h3 ▸ h2
    _ < 0.05 := exp_neg_three_lt

/-- Sec. V: no failure in 6000 slots bounds the fresh rate below `5e-4`. -/
theorem rule_of_three_6000 : (1 - (5e-4 : ℝ)) ^ 6000 < 0.05 :=
  zero_count_bound (by norm_num) (by norm_num)

/-- Sec. II: no error in 400 decoded blocks leaves a 95 % bound near `7.5e-3`. -/
theorem rule_of_three_400 : (1 - (7.5e-3 : ℝ)) ^ 400 < 0.05 :=
  zero_count_bound (by norm_num) (by norm_num)

/-! ## Diversity product -/

theorem diversity_product {p₁ p₂ p₃ q : ℝ} (h₁ : 0 ≤ p₁) (h₂ : 0 ≤ p₂) (h₃ : 0 ≤ p₃)
    (k₁ : p₁ ≤ q) (k₂ : p₂ ≤ q) (k₃ : p₃ ≤ q) : p₁ * p₂ * p₃ ≤ q ^ 3 := by
  have hq : 0 ≤ q := le_trans h₁ k₁
  have h12 : p₁ * p₂ ≤ q * q := mul_le_mul k₁ k₂ h₂ hq
  have h123 : p₁ * p₂ * p₃ ≤ q * q * q := mul_le_mul h12 k₃ h₃ (mul_nonneg hq hq)
  calc p₁ * p₂ * p₃ ≤ q * q * q := h123
    _ = q ^ 3 := by ring

/-- Branches failing at most 3 % each (the measured product, about `1.7e-5`,
implies about 2.6 % per branch) fail together more than thirty times below
the `1e-3` budget; the measured margin is about fifty. -/
theorem diversity_margin {p₁ p₂ p₃ : ℝ} (h₁ : 0 ≤ p₁) (h₂ : 0 ≤ p₂) (h₃ : 0 ≤ p₃)
    (k₁ : p₁ ≤ 0.03) (k₂ : p₂ ≤ 0.03) (k₃ : p₃ ≤ 0.03) : 30 * (p₁ * p₂ * p₃) < 1e-3 := by
  have := diversity_product h₁ h₂ h₃ k₁ k₂ k₃
  have h27 : (0.03 : ℝ) ^ 3 = 2.7e-5 := by norm_num
  linarith

/-! ## The selection rule, Eq. (1) -/

variable {n : ℕ}

/-- MCS `m` is cleared by estimate `g` at backoff `Δ` given thresholds `ρ`. -/
def Clears (ρ : Fin n → ℝ) (g Δ : ℝ) (m : Fin n) : Prop := ρ m + Δ ≤ g

/-- `m` is the MCS Eq. (1) picks: the highest cleared one. -/
def IsPick (ρ : Fin n → ℝ) (g Δ : ℝ) (m : Fin n) : Prop :=
  Clears ρ g Δ m ∧ ∀ j, Clears ρ g Δ j → j ≤ m

theorem pick_antitone {ρ : Fin n → ℝ} {g Δ Δ' : ℝ} (h : Δ ≤ Δ') {m m' : Fin n}
    (hm : IsPick ρ g Δ m) (hm' : IsPick ρ g Δ' m') : m' ≤ m := by
  apply hm.2 m'
  have := hm'.1
  unfold Clears at *
  linarith

theorem expected_bler_antitone {ρ : Fin n → ℝ} (e : Fin n → ℝ) (he : Monotone e)
    {g Δ Δ' : ℝ} (h : Δ ≤ Δ') {m m' : Fin n}
    (hm : IsPick ρ g Δ m) (hm' : IsPick ρ g Δ' m') : e m' ≤ e m :=
  he (pick_antitone h hm hm')

/-! ## Doppler to speed at 3.5 GHz (v = f_D c / f_c) -/

theorem doppler_walk :
    (3 : ℝ) < 10 * 299792458 / 3.5e9 * 3.6 ∧ (10 : ℝ) * 299792458 / 3.5e9 * 3.6 < 3.1 := by
  norm_num

theorem doppler_bike :
    (15 : ℝ) < 50 * 299792458 / 3.5e9 * 3.6 ∧ (50 : ℝ) * 299792458 / 3.5e9 * 3.6 < 15.5 := by
  norm_num

end WcncCsi
