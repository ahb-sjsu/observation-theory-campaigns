import Proofs.PauliRotation

/-!
# The analytic glue, formalized over a functional-calculus interface

The companion file machine-checks the trace identity. This file
closes the remaining distance to the entropy statement itself,
parameterized over a matrix-logarithm interface. The two hypotheses,
that `matlog ρ` commutes with `ρ` and that `matlog` is equivariant
under the specific conjugations used, are exactly the properties any
functional calculus supplies for the logarithm of a positive
definite matrix. With
`S(σ‖ρ) := trace (σ * matlog σ) - trace (σ * matlog ρ)` the theorem
below is the full Pauli-rotation exactness statement.
-/

open Matrix

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- The reverse unitarity, `(rot θ P)† * rot θ P = 1` under
`P * P = 1`. -/
theorem rotAdj_mul_rot (θ : ℝ) (P : Matrix n n ℂ) (hP : P * P = 1) :
    rotAdj θ P * rot θ P = 1 := by
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

/-- Full exactness with the entropy defined through the interface.
`S(UρU†‖ρ) = sin²θ · S(PρP‖ρ)`. -/
theorem pauli_rotation_entropy_exactness
    (θ : ℝ) (ρ P : Matrix n n ℂ)
    (matlog : Matrix n n ℂ → Matrix n n ℂ)
    (hP : P * P = 1)
    (hcomm : ρ * matlog ρ = matlog ρ * ρ)
    (hconj_rot : matlog (rot θ P * ρ * rotAdj θ P)
      = rot θ P * matlog ρ * rotAdj θ P)
    (hconj_p : matlog (P * ρ * P) = P * matlog ρ * P) :
    (trace ((rot θ P * ρ * rotAdj θ P)
        * matlog (rot θ P * ρ * rotAdj θ P))
      - trace ((rot θ P * ρ * rotAdj θ P) * matlog ρ))
    = ((Real.sin θ : ℂ) * Real.sin θ)
      * (trace ((P * ρ * P) * matlog (P * ρ * P))
         - trace ((P * ρ * P) * matlog ρ)) := by
  set U := rot θ P with hU
  set V := rotAdj θ P with hV
  set L := matlog ρ with hL
  have hVU : V * U = 1 := rotAdj_mul_rot θ P hP
  -- unitary invariance of the entropy term for the rotation
  have e1 : trace (U * ρ * V * matlog (U * ρ * V))
      = trace (ρ * L) := by
    rw [hconj_rot]
    have hmid : U * ρ * V * (U * L * V) = U * (ρ * L) * V := by
      calc U * ρ * V * (U * L * V)
          = U * ρ * (V * U) * (L * V) := by
            simp only [mul_assoc]
        _ = U * (ρ * L) * V := by
            rw [hVU]
            simp only [mul_one, mul_assoc]
    rw [hmid, trace_mul_comm (U * (ρ * L)) V, ← mul_assoc,
      hVU, one_mul]
  -- the same invariance for the involution conjugation
  have e2 : trace ((P * ρ * P) * matlog (P * ρ * P))
      = trace (ρ * L) := by
    rw [hconj_p]
    have hmid : P * ρ * P * (P * L * P) = P * (ρ * L) * P := by
      calc P * ρ * P * (P * L * P)
          = P * ρ * (P * P) * (L * P) := by
            simp only [mul_assoc]
        _ = P * (ρ * L) * P := by
            rw [hP]
            simp only [mul_one, mul_assoc]
    rw [hmid, trace_mul_comm (P * (ρ * L)) P, ← mul_assoc,
      hP, one_mul]
  -- the verified trace identity supplies the difference
  have key := rotation_trace_identity θ ρ P L hcomm
  simp only [sub_mul, trace_sub] at key
  rw [e1, e2]
  linear_combination key
