import Mathlib

/-!
# The algebraic core of the Pauli-rotation exactness theorem

TB-3, observation-theory campaigns.

Paper statement. For a full-rank density matrix `ρ` and a Hermitian
involution `P`, with `U θ = exp (i θ P)`,

  `S (U ρ U* ‖ ρ) = sin² θ * S (P ρ P ‖ ρ)`.

The analytic glue (existence of `log ρ` for positive definite `ρ`,
unitary invariance of von Neumann entropy, and the decomposition
`S(σ‖ρ) = tr σ log σ - tr σ log ρ`) reduces the theorem to a pure
matrix-trace identity. Writing `L` for `log ρ`, the only property of
`L` that is used is that it commutes with `ρ`, and the target is

  `trace ((ρ - U ρ U*) * L) = sin² θ * trace ((ρ - P ρ P) * L)`.

This file machine-checks that reduction target.

* `rot_mul_rotAdj` : `U θ * (U θ)* = 1` when `P * P = 1`, so the
  conjugation really is unitary;
* `conj_expand` : the three-harmonic expansion of `U ρ U*`;
* `cross_trace_vanishes` : the odd harmonic dies under
  `ρ * L = L * ρ`, the step where "ρ commutes with its own
  logarithm" kills the linear term;
* `rotation_trace_identity` : the assembled identity.

Only `rot_mul_rotAdj` uses `P * P = 1`. The trace identity itself is
hypothesis-minimal: it holds for arbitrary square complex matrices
`ρ P L` with `ρ * L = L * ρ`.
-/

open Matrix

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- `exp (i θ P)` for an involution `P`, in closed form. -/
noncomputable def rot (θ : ℝ) (P : Matrix n n ℂ) : Matrix n n ℂ :=
  (Real.cos θ : ℂ) • (1 : Matrix n n ℂ) + (Complex.I * Real.sin θ) • P

/-- The adjoint of `rot θ P` for Hermitian `P`, in closed form. -/
noncomputable def rotAdj (θ : ℝ) (P : Matrix n n ℂ) : Matrix n n ℂ :=
  (Real.cos θ : ℂ) • (1 : Matrix n n ℂ) - (Complex.I * Real.sin θ) • P

/-- Unitarity of the closed-form rotation, given `P * P = 1`. -/
theorem rot_mul_rotAdj (θ : ℝ) (P : Matrix n n ℂ) (hP : P * P = 1) :
    rot θ P * rotAdj θ P = 1 := by
  have hC := Complex.sin_sq_add_cos_sq (θ : ℂ)
  unfold rot rotAdj
  simp only [mul_sub, sub_mul, mul_add, add_mul, smul_mul_assoc,
    mul_smul_comm, smul_smul, one_mul, mul_one, hP, smul_add, smul_sub]
  match_scalars
  all_goals (try ring)
  all_goals (try rw [Complex.I_sq])
  all_goals (try ring)
  all_goals (try linear_combination hC)
  all_goals (try linear_combination -hC)

/-- The three-harmonic expansion of the conjugated state. No
hypothesis on `P` or `ρ` is needed. -/
theorem conj_expand (θ : ℝ) (ρ P : Matrix n n ℂ) :
    rot θ P * ρ * rotAdj θ P
      = ((Real.cos θ : ℂ) * Real.cos θ) • ρ
        + ((Real.sin θ : ℂ) * Real.sin θ) • (P * ρ * P)
        + (Complex.I * Real.sin θ * Real.cos θ) • (P * ρ - ρ * P) := by
  have hC := Complex.sin_sq_add_cos_sq (θ : ℂ)
  unfold rot rotAdj
  simp only [mul_sub, sub_mul, mul_add, add_mul, smul_mul_assoc,
    mul_smul_comm, smul_smul, one_mul, mul_one, smul_add, smul_sub,
    mul_assoc]
  match_scalars
  all_goals (try ring)
  all_goals (try rw [Complex.I_sq])
  all_goals (try ring)
  all_goals (try linear_combination hC)
  all_goals (try linear_combination -hC)

/-- The odd harmonic is killed by `ρ * L = L * ρ`, the trace-level
form of "ρ commutes with its own logarithm". -/
theorem cross_trace_vanishes (ρ P L : Matrix n n ℂ)
    (hL : ρ * L = L * ρ) :
    trace ((P * ρ - ρ * P) * L) = 0 := by
  rw [sub_mul, trace_sub]
  have h1 : trace (P * ρ * L) = trace (P * L * ρ) := by
    rw [mul_assoc, hL, ← mul_assoc]
  have h2 : trace (ρ * P * L) = trace (P * L * ρ) := by
    rw [mul_assoc]
    exact trace_mul_comm ρ (P * L)
  rw [h1, h2, sub_self]

/-- The assembled trace identity. With `L = log ρ` and the analytic
glue in the module docstring, this is
`S(U ρ U* ‖ ρ) = sin² θ * S(P ρ P ‖ ρ)`. -/
theorem rotation_trace_identity (θ : ℝ) (ρ P L : Matrix n n ℂ)
    (hL : ρ * L = L * ρ) :
    trace ((ρ - rot θ P * ρ * rotAdj θ P) * L)
      = ((Real.sin θ : ℂ) * Real.sin θ)
        * trace ((ρ - P * ρ * P) * L) := by
  have hC := Complex.sin_sq_add_cos_sq (θ : ℂ)
  rw [conj_expand θ ρ P]
  have expand : ρ - (((Real.cos θ : ℂ) * Real.cos θ) • ρ
        + ((Real.sin θ : ℂ) * Real.sin θ) • (P * ρ * P)
        + (Complex.I * Real.sin θ * Real.cos θ) • (P * ρ - ρ * P))
      = ((Real.sin θ : ℂ) * Real.sin θ) • (ρ - P * ρ * P)
        - (Complex.I * Real.sin θ * Real.cos θ) • (P * ρ - ρ * P) := by
    match_scalars
    all_goals (try ring)
    all_goals (try rw [Complex.I_sq])
    all_goals (try ring)
    all_goals (try linear_combination hC)
    all_goals (try linear_combination -hC)
  rw [expand, sub_mul, smul_mul_assoc, smul_mul_assoc, trace_sub,
    trace_smul, trace_smul, cross_trace_vanishes ρ P L hL,
    smul_zero, sub_zero, smul_eq_mul]
