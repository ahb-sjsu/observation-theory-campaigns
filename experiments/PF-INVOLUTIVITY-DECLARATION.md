# Involutivity declaration: is the read operator's kernel a foliation?

Written and committed before the run. Bars are numerical and fixed here. The
verdict is computed from the data by `python/involutivity_gate.py` and is not
written in this file.

Status: declaration, unsealed, non-claim-bearing until the run records.

## 1. Question

`P_C(x) = J(x)^T G J(x)` and its kernel is the set of directions the consumer
cannot read at `x`. C-11c measured that the read operator MOVES with position,
so `K(x) = ker P_C(x)` is a distribution of subspaces rather than a fixed one.

A divergence, a quotient, or any notion of "consumer-equivalent states" that is
blind to `K` requires the blindness to foliate. By Frobenius that holds exactly
when `K` is INVOLUTIVE, `[X, Y]` in `K` whenever `X` and `Y` are in `K`.

If `K` is not involutive then three things follow, and they are the reason to
measure it. There is no generator blind to `K`, so the consumer-relative
Bregman construction of section 8.1 of `CONSUMER-CROSS-ENTROPY-NOTE.md` has no
varying-kernel analogue. The consumer quotient `X / ~_C` is not a manifold.
And consumer equivalence is not transitive, since a commutator moves along
directions the consumer cannot see and can arrive somewhere it distinguishes.

## 2. The measured quantity

Let `Pi(x)` be the orthogonal projector onto `K(x)`. For constant vectors `a`,
`b`, take the fields `X = Pi a` and `Y = Pi b`. Then

```
[X, Y] = (d_{Pi a} Pi) b - (d_{Pi b} Pi) a
```

and involutivity is the vanishing of the part outside the kernel,

```
T(a, b) = (I - Pi) [ (d_{Pi a} Pi) b - (d_{Pi b} Pi) a ]
```

Directional derivatives of `Pi` are taken by central differences along kernel
directions at step `eps`. The reported statistic is

```
tau = || T(a, b) ||  /  ( || Pi a ||  || Pi b || )
```

maximised over a declared set of probe pairs `(a, b)` per cell, so `tau = 0` is
involutive and larger is further from it.

## 3. Nulls, because comparing against zero is the C-11b error

C-11 and C-11b both FAILED anti-vacuity by comparing quantities against 1.0
rather than against a null, and C-11c passed only after pairing every quantity
with a random-split null. That lesson is applied here in advance.

**Ceiling null.** At each sampled position, replace `Pi(x)` by a projector of
the SAME RANK onto a uniformly random subspace, drawn independently per
position. This is a maximally non-involutive field of the same dimension and
gives the scale `tau_rand` that a structureless kernel produces.

**Floor null.** Recompute `tau` at `eps / 2`. A real bracket is a limit and is
stable under that halving, while finite-difference noise is not.

`tau` is reported against BOTH. A number near the ceiling means not involutive.
A number near the floor means involutive. A number that moves when `eps` halves
means the estimate is noise and the cell is not evaluable.

## 4. Bars

**V0, instrument live, per cell, on exact synthetic constructions.** Two
synthetic consumers with known answers must be classified correctly at every
cell. A consumer whose kernel is a fixed subspace, hence trivially involutive,
must give `tau <= 0.05`. A consumer whose kernel is the contact distribution
`span{ d/dx , d/dy + x d/dz }` on `R^3`, whose bracket is `d/dz` and which is
the textbook non-involutive example, must give `tau >= 0.5`. Per-cell is safe
here because these are exact constructions with no substrate freedom. **V0
gates the run.**

**V1, anti-vacuity, the kernel must actually vary.** If `Pi` is constant then
every derivative vanishes and `tau = 0` for reasons having nothing to do with
involutivity. Median over cells of `|| Pi(x + delta) - Pi(x) ||_F` must be
`>= 0.02` at the declared step. **If V1 fails the run is VOID for vacuity** and
no other number is reported as evidence.

**V2, the kernel must be well defined.** A numerical kernel needs a spectral
gap, otherwise which directions count as unread is arbitrary. Report per cell
the ratio `lambda_(m+1) / lambda_m` across the chosen cut. Median over cells
must be `>= 5`. Cells below 2 are marked NOT EVALUABLE and excluded, with the
excluded count reported.

**V3, finite-difference stability.** Median over cells of
`| tau(eps) - tau(eps/2) | / tau(eps)` must be `<= 0.15`. Cells failing this are
NOT EVALUABLE.

**V4, the measurement, reported as a distribution and barred only in
aggregate.** Involutivity is a property real attention heads have no obligation
to share, so per the standing rule earned at C-3c and C-6 the aggregate is
barred and the distribution is reported. Declared discriminator on evaluable
cells:

```
rho = median(tau) / median(tau_rand)
```

- `rho <= 0.15` is recorded as INVOLUTIVE, the kernel foliates
- `rho >= 0.60` is recorded as NOT INVOLUTIVE
- anything between is recorded as INDETERMINATE and reported as such

No outcome is preferred. The interesting result is whichever one occurs, and
INDETERMINATE is a real outcome rather than a failure.

## 5. Fixed configuration

```
MODEL         Qwen2.5-7B-Instruct
CELLS         layers {4, 14, 24} x 4 kv-heads = 12 cells
POSITIONS     32 sampled decode positions per cell, evenly spaced
PROBE_PAIRS   24 random (a, b) pairs per position, fixed seed
EPS           1e-3, with 5e-4 for the V3 halving
RANK_CUT      kernel = eigendirections below 1e-3 of the leading eigenvalue
N_RAND        5 draws for the ceiling null
SEED          20260808
V0_INVOL_BAR    0.05
V0_CONTACT_BAR  0.50
V1_VARY_BAR     0.02
V2_GAP_MEDIAN   5.0
V2_GAP_EXCLUDE  2.0
V3_STABILITY    0.15
V4_INVOL        0.15
V4_NOT_INVOL    0.60
```

## 6. Interpretation, fixed in advance

If INVOLUTIVE, the consumer quotient is a genuine foliation, section 8.1's
construction extends to the varying case, and consumer equivalence is a real
equivalence relation on states. That is the convenient outcome and it would
license the quotient language the programme already uses.

If NOT INVOLUTIVE, the quotient language is an approximation and the note's
section 8.2 obstruction is real for trained attention. That is the more
interesting outcome and it is a genuine constraint on the theory, not a defect
in the instrument. It would mean consumer equivalence holds locally and fails
globally, and the size of `rho` measures how fast it fails.

Either way the claim is about THIS model and THESE cells, and generalisation is
not asserted.
