import Proofs.PauliRotation
import Proofs.EntropyGlue

/-!
# Discharging the matrix-logarithm interface via Mathlib's CFC

The companion file `EntropyGlue` proves the Pauli-rotation exactness
theorem over an interface: any function `matlog` that commutes with its
argument and is equivariant under the two conjugations used. This file
instantiates that interface with Mathlib's continuous functional
calculus for Hermitian matrices, `matrixLog A := cfc Real.log A`, and
discharges all three interface hypotheses:

* `matrixLog_comm` : a matrix commutes with any continuous function of
  itself (`Commute.cfc_real`);
* `matrixLog_conj_unitary` : for positive definite `ρ` and unitary `U`,
  `log (U ρ U†) = U (log ρ) U†`. This is the equivariance of the
  functional calculus under the star-algebra automorphism
  `x ↦ U x U†` (`Unitary.conjStarAlgAut` plus
  `StarAlgHomClass.map_cfc`), with `ContinuousOn Real.log` on the
  spectrum supplied by positivity of the eigenvalues.

Both `rot θ P` (for a Hermitian involution `P`, via
`star_rot : (rot θ P)† = rotAdj θ P`) and `P` itself are unitary, so
the final theorem `pauli_rotation_entropy_exactness_cfc` has no
interface hypotheses left: it assumes only that `ρ` is positive
definite and that `P` is a Hermitian involution.
-/

open Matrix
open scoped ComplexOrder

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- The matrix logarithm, via Mathlib's continuous functional calculus
for Hermitian matrices. Total by junk values; it is the true logarithm
on positive definite matrices. -/
noncomputable def matrixLog (A : Matrix n n ℂ) : Matrix n n ℂ :=
  cfc Real.log A

/-- The closed-form adjoint really is the star: `(rot θ P)† = rotAdj θ P`
for Hermitian `P`. -/
theorem star_rot (θ : ℝ) {P : Matrix n n ℂ} (hP : P.IsHermitian) :
    star (rot θ P) = rotAdj θ P := by
  simp only [rot, rotAdj, star_add, star_smul, star_one, hP.star_eq,
    star_mul', Complex.star_def, Complex.conj_ofReal, Complex.conj_I,
    neg_mul, neg_smul, ← sub_eq_add_neg]

/-- `rot θ P` is a unitary element for a Hermitian involution `P`. -/
theorem rot_mem_unitary (θ : ℝ) {P : Matrix n n ℂ} (hP : P.IsHermitian)
    (hP2 : P * P = 1) : rot θ P ∈ unitary (Matrix n n ℂ) := by
  rw [Unitary.mem_iff, star_rot θ hP]
  exact ⟨rotAdj_mul_rot θ P hP2, rot_mul_rotAdj θ P hP2⟩

/-- A Hermitian involution is a unitary element. -/
theorem involution_mem_unitary {P : Matrix n n ℂ} (hP : P.IsHermitian)
    (hP2 : P * P = 1) : P ∈ unitary (Matrix n n ℂ) := by
  rw [Unitary.mem_iff, hP.star_eq]
  exact ⟨hP2, hP2⟩

/-- Interface hypothesis 1: a matrix commutes with its own logarithm. -/
theorem matrixLog_comm (ρ : Matrix n n ℂ) :
    ρ * matrixLog ρ = matrixLog ρ * ρ :=
  ((Commute.refl ρ).cfc_real Real.log).symm.eq

/-- `Real.log` is continuous on the spectrum of a positive definite
matrix, because all eigenvalues are strictly positive. -/
theorem continuousOn_log_spectrum {ρ : Matrix n n ℂ} (hρ : ρ.PosDef) :
    ContinuousOn Real.log (spectrum ℝ ρ) := by
  refine Real.continuousOn_log.mono ?_
  rw [hρ.1.spectrum_real_eq_range_eigenvalues]
  rintro - ⟨i, rfl⟩
  simpa using (hρ.eigenvalues_pos i).ne'

/-- Interface hypothesis 2 and 3, master form: the matrix logarithm of
a positive definite matrix is equivariant under unitary conjugation.
This is `StarAlgHomClass.map_cfc` applied to the star-algebra
automorphism `x ↦ U * x * star U`. -/
theorem matrixLog_conj_unitary {U : Matrix n n ℂ}
    (hU : U ∈ unitary (Matrix n n ℂ)) {ρ : Matrix n n ℂ}
    (hρ : ρ.PosDef) :
    matrixLog (U * ρ * star U) = U * matrixLog ρ * star U := by
  have hsa : IsSelfAdjoint ρ := hρ.1.isSelfAdjoint
  have hcont :
      Continuous (Unitary.conjStarAlgAut ℂ (Matrix n n ℂ) ⟨U, hU⟩) := by
    change Continuous fun x : Matrix n n ℂ => U * x * star U
    exact (continuous_const.matrix_mul continuous_id).matrix_mul
      continuous_const
  have hconj :
      IsSelfAdjoint (Unitary.conjStarAlgAut ℂ (Matrix n n ℂ) ⟨U, hU⟩ ρ) := by
    change IsSelfAdjoint (U * ρ * star U)
    exact hsa.conjugate U
  have key := StarAlgHomClass.map_cfc
    (Unitary.conjStarAlgAut ℂ (Matrix n n ℂ) ⟨U, hU⟩) Real.log ρ
    (continuousOn_log_spectrum hρ) hcont hsa hconj
  exact key.symm

/-- The full Pauli-rotation entropy exactness theorem with the matrix
logarithm supplied by the continuous functional calculus. No interface
hypotheses remain: `ρ` positive definite, `P` a Hermitian involution.
With `S(σ‖ρ) = tr (σ log σ) - tr (σ log ρ)` this reads
`S(U ρ U† ‖ ρ) = sin² θ · S(P ρ P ‖ ρ)`. -/
theorem pauli_rotation_entropy_exactness_cfc
    (θ : ℝ) {ρ P : Matrix n n ℂ} (hρ : ρ.PosDef) (hP : P.IsHermitian)
    (hP2 : P * P = 1) :
    (trace ((rot θ P * ρ * rotAdj θ P)
        * matrixLog (rot θ P * ρ * rotAdj θ P))
      - trace ((rot θ P * ρ * rotAdj θ P) * matrixLog ρ))
    = ((Real.sin θ : ℂ) * Real.sin θ)
      * (trace ((P * ρ * P) * matrixLog (P * ρ * P))
         - trace ((P * ρ * P) * matrixLog ρ)) := by
  have hrot : matrixLog (rot θ P * ρ * rotAdj θ P)
      = rot θ P * matrixLog ρ * rotAdj θ P := by
    have h := matrixLog_conj_unitary (rot_mem_unitary θ hP hP2) hρ
    rwa [star_rot θ hP] at h
  have hp : matrixLog (P * ρ * P) = P * matrixLog ρ * P := by
    have h := matrixLog_conj_unitary (involution_mem_unitary hP hP2) hρ
    rwa [hP.star_eq] at h
  exact pauli_rotation_entropy_exactness θ ρ P matrixLog hP2
    (matrixLog_comm ρ) hrot hp
