import Mathlib

/-!
# Redundant-update pruning is observationally lossless

A route collector's view is last-writer-wins per `(peer, prefix)`: an
announcement installs a path, a withdrawal removes one. An update is
*redundant* when it re-installs the path already installed, or withdraws a
prefix already absent. Measurements put the redundant-announcement share at
roughly a quarter to a third of the stream.

The theorem below is the correctness statement behind discarding them: pruning
redundant updates leaves the final state **identical**, so any consumer that
reads the collector state — reachability, origin set, best path, an anomaly
detector — cannot tell the pruned stream from the full one. Compression here
is not lossy-but-tolerable; it is exactly lossless *for every state-reading
consumer*.

Scope, stated rather than assumed. This models the collector RIB, which is
last-writer-wins per peer. It is **not** the BGP decision process: no local
preference, MED, tie-breaking, timers or MRAI appear here, and nothing is
claimed about a router's forwarding choice. It also says nothing about
*timing* — a consumer that reads the state's history, or the arrival times,
is outside this statement.
-/

namespace CollectorPrune

variable {K V : Type*} [DecidableEq K] [DecidableEq V]

/-- A collector update: install a path, or withdraw the prefix. -/
inductive Upd (K V : Type*) where
  | ann : K → V → Upd K V
  | wdr : K → Upd K V
  deriving DecidableEq

/-- Collector state: the path currently installed for each key, if any. -/
abbrev St (K V : Type*) := K → Option V

/-- Applying one update. -/
def step (σ : St K V) : Upd K V → St K V
  | .ann k v => Function.update σ k (some v)
  | .wdr k   => Function.update σ k none

/-- Applying a stream, left to right. -/
def run (σ : St K V) (l : List (Upd K V)) : St K V :=
  l.foldl step σ

/-- An update is redundant exactly when applying it changes nothing. -/
def redundant (σ : St K V) : Upd K V → Prop
  | .ann k v => σ k = some v
  | .wdr k   => σ k = none

instance (σ : St K V) (u : Upd K V) : Decidable (redundant σ u) := by
  cases u <;> unfold redundant <;> infer_instance

/-- Dropping redundant updates as the state evolves. -/
def prune (σ : St K V) : List (Upd K V) → List (Upd K V)
  | [] => []
  | u :: t => if redundant σ u then prune σ t else u :: prune (step σ u) t

/-- Folding over a cons, as a rewrite rule. -/
theorem run_cons (σ : St K V) (u : Upd K V) (l : List (Upd K V)) :
    run σ (u :: l) = run (step σ u) l := rfl

/-- A redundant update is a no-op on the state. -/
theorem step_redundant {σ : St K V} {u : Upd K V} (h : redundant σ u) :
    step σ u = σ := by
  cases u with
  | ann k v =>
    simp only [redundant] at h
    funext x
    by_cases hx : x = k
    · subst hx; simp [step, h]
    · simp [step, Function.update, hx]
  | wdr k =>
    simp only [redundant] at h
    funext x
    by_cases hx : x = k
    · subst hx; simp [step, h]
    · simp [step, Function.update, hx]

/-- **Pruning is observationally lossless.** The pruned stream and the full
stream drive the collector to the *same* final state. -/
theorem run_prune (σ : St K V) (l : List (Upd K V)) :
    run σ (prune σ l) = run σ l := by
  induction l generalizing σ with
  | nil => rfl
  | cons u t ih =>
    by_cases h : redundant σ u
    · rw [prune, if_pos h, run_cons, step_redundant h]
      exact ih σ
    · rw [prune, if_neg h, run_cons, run_cons]
      exact ih (step σ u)

/-- Consequently no state-reading consumer can distinguish them. -/
theorem consumer_indistinguishable {W : Type*} (f : St K V → W)
    (σ : St K V) (l : List (Upd K V)) :
    f (run σ (prune σ l)) = f (run σ l) := by
  rw [run_prune]

end CollectorPrune
