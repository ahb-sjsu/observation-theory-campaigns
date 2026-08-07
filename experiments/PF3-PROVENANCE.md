# PF-3 provenance note: the Land 2016 configuration

**Status:** replication in progress, exploratory. This note records, line by
line, which published equations are transcribed into
`python/shp_land2016.py`, under which conventions, and which checks guard
the transcription. Per AUTHOR-NOTES, PF-3 lives in its own commits.

## Source

Martin Land, "Pair production in classical Stueckelberg-Horwitz-Piron
electrodynamics", arXiv:1604.01625 [physics.gen-ph], v1, 6 Apr 2016.
Related DOI 10.1088/1742-6596/615/1/012007 (J. Phys.: Conf. Ser. 615,
012025, 2017, IARD proceedings). Equation numbers below are the arXiv v1
numbers. The PDF consulted is the arXiv v1 PDF, retrieved 2026-08-04.

## What the source establishes

SHP electrodynamics evolves events x^mu(tau) under a tau-dependent
five-potential a_alpha(x, tau). The Lorentz force (source Eq. 12) is
M xddot^mu = e0 f^mu_alpha xdot^alpha with f^mu_alpha = d^mu a_alpha -
d_alpha a^mu and xdot^5 = 1. Mass exchange with the field (source Eq. 14)
lifts the mass-shell constraint, so dt/dtau may change sign along one
worldline; that sign change is the classical pair event in Stueckelberg's
sense (source Fig. 1, worldline types B and C).

The worked configuration replicated here is the impulsive Coulomb
scattering of Section 3. An event with incoming velocity
u = tdot_in (1, v, 0, 0), tdot_in = 1/sqrt(1 - v^2) (source Eqs. 47-48),
scatters in the field of a nucleus at rest, whose induced potential is
a^0 = a^5 = (Ze/4 pi R) delta(tau - tau_1) in the small-correlation-length
approximation (source Eq. 56). Integrating the force through the impulse
with midpoint velocities (source Eq. 63) gives the linear system (source
Eq. 66) with alpha_x = (1/2) g_e Rhat_x, alpha_y = (1/2) g_e Rhat_y, and
the closed-form final velocity (source Eq. 67), where the dimensionless
coupling is

g_e = (lambda / M) (Z e^2 / 4 pi R^2)   (source Eq. 64),

lambda the correlation length, R the interaction distance, Rhat the unit
vector to the interaction point.

Key consequences transcribed:

- Source Eq. 76: tdot_f = [tdot_in (1 - g_e v Rhat_x) + (1/4) g_e^2
  (tdot_in + 2)] / (1 - (1/4) g_e^2).
- Source Eq. 78: the numerator of Eq. 76 is positive definite because
  (v Rhat_x)^2 < 1 + 2/tdot_in.
- Source Eqs. 79-80: tdot_f < 0 (time reversal, the pair-annihilation
  condition) exactly when g_e > 2, equivalently Z e^2 / 4 pi R > 2 M; the
  interaction energy must exceed the rest energy of the annihilated pair.
- Source Eq. 81: tdot_f -> -(tdot_in + 2) as g_e -> infinity, so
  E_f = -(E_in + 2M) and the outgoing trajectory is timelike for all g_e.
- Source Eq. 74 with constraint Eq. 72: in the low-velocity
  energy-conserving limit, cot(theta/2) = Rhat_y / Rhat_x.

## Transcription map (source -> code)

| Source | Code |
|---|---|
| Eq. 64 g_e | `coupling_ge(lam, mass, strength, radius)` |
| Eq. 66 linear system | `impulse_system(tdot_in, v, rhat, ge)` |
| Eq. 67 closed form | `final_velocity(tdot_in, v, rhat, ge)` |
| Eq. 76 time component | `tdot_final(tdot_in, v, rhat_x, ge)` |
| Eq. 74/72 Rutherford limit | `rutherford_cot_half_angle(rhat)` |
| Eqs. 59-60 smoothed force | `integrate_smoothed(...)` (see below) |

Sign and convention notes: metric signature follows the source
(mostly-plus is implied by u^2 = -1 on-shell language in source Eq. 14 and
by xdot mu xdot^mu = -1 for timelike normalization; the transcription
never uses the metric explicitly, only the component equations as
printed). Units M = 1. The code treats Eq. 67 exactly as printed,
including the (Rhat_x^2 - Rhat_y^2) and 2 Rhat_x Rhat_y structure of the
g_e^2 spatial term.

## Transcription guards (all asserted in tests)

1. **System-vs-closed-form guard.** `final_velocity` must equal the
   numerical solution of the Eq. 66 linear system to 1e-12 across a
   parameter grid. A transcription slip in either form breaks agreement.
2. **Internal-consistency guard.** The 0-component of Eq. 67 must equal
   Eq. 76 identically.
3. **Positive-definiteness guard.** The Eq. 78 discriminant inequality
   holds on the physical domain (0 < v < 1, |Rhat_x| < 1).
4. **Threshold guard.** tdot_f > 0 for all g_e < 2; sign change only
   through the denominator zero at g_e = 2.
5. **Asymptote guard.** tdot_f -> -(tdot_in + 2) as g_e grows.
6. **Timelike guard, corrected scope.** The first version of this guard
   asserted tdot_f^2 - |xdot_f|^2 > 0 over the whole sweep grid and
   failed. The failure is a finding, preserved per the evidence
   discipline: at intermediate g_e the outgoing velocity can be
   spacelike, which is exactly Stueckelberg's requirement that a
   time-reversing worldline cross the spacelike region twice (source
   page 2), and the source's timelike sentence after Eq. 81 attaches to
   the g_e -> infinity limiting value, where tdot_f -> -(tdot_in + 2)
   against spatial speed v tdot_in, timelike for every v < 1. The
   corrected guard asserts the asymptotic-limit statement and records
   every spacelike cell of the sweep in the evidence record.
7. **Rutherford-limit guard.** cot(theta/2) = Rhat_y/Rhat_x under the
   Eq. 72 constraint at low velocity.

## The smoothed bridge to the PF instrument net (this campaign's addition)

The impulse approximation makes tdot jump discontinuously, which the fold
instruments cannot classify. The source's own pre-impulse dynamics
(Eqs. 59-60) is a smooth ODE once the delta kernel is replaced by a
finite-width kernel, which is exactly the small-lambda limit the source
takes (Eq. 92 uses a box kernel of width 2 lambda). The code integrates

ttdot = (lambda/M) [ xdot . grad U  phi_lam(tau - tau_1)
                    + (1 + 1/tdot_in) U  phi_lam'(tau - tau_1) ]
xddot = (lambda/M) (tdot + 1) grad U  phi_lam(tau - tau_1)

with U(x) = k/|x|, k = Z e^2 / 4 pi, and phi_lam a raised-cosine kernel of
half-width lambda (smooth, so its tau-derivative is defined pointwise;
the box kernel of source Eq. 92 is its sharp limit). This is a
transcription of source Eqs. 59-62 with the delta replaced by its
smoothing, not a new model. Expected and accepted deviations from the
impulse closed form are O(lambda) because the event moves during the
interaction window and the impulse algebra uses the midpoint convention
(source Eq. 63); the measured deviation is recorded, not hidden.

### Replication findings (both preserved per the evidence discipline)

**Finding F1, kernel artifact.** The first bridge evaluated U and grad U
along the moving trajectory. The kernel-derivative term then produced
transient tdot excursions scaling like the inverse kernel width, which
crossed zero even below threshold, where the impulse algebra forbids
reversal. Those crossings are smoothing artifacts, not folds. The
source's own delta collapse (Eq. 61) evaluates the potential at the
fixed interaction point, making that term integrate to exactly zero,
and the corrected treatments below follow that convention.

**Finding F2, the threshold belongs to the midpoint prescription.** With
the frozen-point convention, the accumulated-kernel variable
s = integral phi dtau turns Eqs. 59-60 into the linear kick system
d(tdot)/ds = -g_e w, dw/ds = -g_e (tdot + 1) for w the R-hat velocity
component. Continuous integration gives hyperbolic evolution,
tdot(1) + 1 = (tdot_in + 1) cosh g_e - w_in sinh g_e, which never
reverses tdot for any physical initial condition (w_in < tdot_in + 1),
verified by independent RK4 against the closed form. The source's
midpoint convention (Eq. 63) applies the same generator as the Cayley
transform (I - G/2)^{-1}(I + G/2), the Pade(1,1) approximant of the
exponential, whose pole at g_e = 2 is exactly the published
annihilation threshold. The published classical pair event is therefore
a property of the impulsive midpoint prescription, not of continuous
accumulation of the same force; whether the full field dynamics
(trajectory-varying potential, radiation reaction) restores a reversal
threshold is an open question this replication does not answer. The
closed-form replication of the source's published algebra is unaffected
by this finding and passes all guards.

**The bridge to the fold instruments.** Given F2, the honest smooth
worldline attached to the impulsive solution is the source's own
midpoint reading: the velocity transitions from incoming to outgoing
across the kernel window, tdot(tau) = tdot_in + (tdot_f - tdot_in)
S(tau) with S the kernel's cumulative integral. Under the sealed
classifier this worldline has no tdot crossing below threshold and
exactly one above, classified as an annihilation fold. This ties the
published pair event to the PF-0 fold kinematics using only the
source's velocities and kernel.

## What this replication does not claim

No statement about rates, about the Schwinger exponent, about quantum
pair production, or about the physical correctness of SHP electrodynamics
is made or implied. PF-3 establishes only that the campaign's instruments
reproduce a published classical pair trajectory with its stated
conservation structure. PF-4 remains gated behind this and the campaign's
other controls.
