# PE/QO instrument freeze

**Status:** SEALED.

**Registration ID:** PEQO-FREEZE-002

**Date sealed:** 2026-08-04

**Seal hash:** SHA-256 of this file's git blob at the sealing commit,
recorded in `experiments/SEALS.md`. Any edit to this file after the sealing
commit voids the seal and requires a new registration ID.

**Authorization:** sealed on the project owner's explicit instruction after
the full pre-seal recheck.

**Scope.** This seal covers the entropy-track and quantum-track instrument
layer: the coarea branch-weight and branch-entropy instruments
(`fiber_branch_weights`, `branch_entropy_bits`, `pf.fiber_entropy`,
`binned_fold_entropy`), the sampled-trajectory crossing detector
(`polyline_level_crossings`), the PE-2 reversible-cycle harness, and the
finite-dimensional quantum instruments (`relative_entropy`, `partial_trace`,
`dephase`, `pinch`, `merge_branches`, `uhlmann_fidelity`, the hierarchy
chain builders, the encoder family, `fit_quadratic_through_origin`). It
does not change the evidence labels of any result; PE-2 and QO-0..QO-3
results remain [exploratory] until claim-bearing preregistrations exist.
Every measured value below was recomputed from the committed evidence
records immediately before sealing; bounds round up, never down.

## Declared defaults (frozen with this seal)

- Divergence: Umegaki relative entropy in nats, bits derived by /ln 2.
  Support semantics: reference eigenvalues at or below the support floor
  (default 1e-12) are outside the support; excess mass there makes the
  divergence infinite by definition.
- The channel is the primitive consumer object; algebra restriction enters
  as the pinching channel.
- Commuting embedding of classical anchors: fiber branches ordered by
  increasing tau are computational basis states, coarea weights are
  eigenvalues, the uniform fiber is the reference, the branch-label algebra
  is the diagonal algebra.
- Non-generic refusal contract: branch counters refuse slices through
  critical points and levels that hit samples exactly; refusal is an error,
  never a silent count.

## Measured instrument performance

| Witness | Measured | Evidence |
|---|---|---|
| PE-0 branch entropies, both languages | P0 exactly 1 bit, M0 exactly 1.5 bits, band edge to 1 bit within 1e-3, N0/D0 exactly 0 | pytest + run_pe0_entropy_controls |
| PE-1 binned-entropy convergence | deviations 4.47e-3, 1.41e-3, 4.47e-4 at eps 1e-4..1e-6, sqrt-eps scaling | pytest + console |
| PE-2 hidden recovery residual | 1.1e-14 | results/pe2-cycle.json |
| PE-2 reverse-curve retrace defect | 0.0 (bit-identical) | results/pe2-cycle.json |
| PE-2 ensemble energy drift | 6.2e-9 | results/pe2-cycle.json |
| PE-2 signed path-degree rule | verified at every tested level | results/pe2-cycle.json |
| QO-0 anchors via divergence | 1.000000000000 and 1.500000000000 bits; orientation merge returns exactly 1 bit | results/qo0-instrument.json |
| QO-0 closed-form residuals | <= 1.8e-15 | results/qo0-instrument.json |
| QO-0 DPI margins | minimum +9.6e-8 over 32 checks, all finite | results/qo0-instrument.json |
| QO-0 spectral-floor spread | 0.0 across floors 1e-14..1e-10 | results/qo0-instrument.json |
| No-signalling null | <= 6.7e-16 | results/qo0-instrument.json |
| Symmetry null | <= 6.1e-16 | results/qo0-instrument.json |
| QO-1 hierarchy ordering | no inversion at any level, either axis | results/qo1-hierarchy.json |
| QO-1 sufficiency anchor | DPI equality gap 1.1e-16 | results/qo1-hierarchy.json |
| QO-1 nonzero-gap anchor | matches ln2/4 - ln(4/3)/2 within 5.6e-17 | results/qo1-hierarchy.json |
| QO-2 Uhlmann closed forms | pure-state overlap, classical Bhattacharyya, self-fidelity all < 1e-10 | pytest |
| QO-2 anti-arm separation | 1.289 vs <= 0.118 task distortion, every budget | results/qo2-flip.json |
| QO-3 quadratic-fit control | exact law recovered, residual < 1e-12 | pytest |
| QO-3 wedge no-signalling null | < 1e-10 at every coupling point | asserted in sweep |

## Frozen instrument bars

A claim-bearing PE or QO run that violates a bar invalidates the
instrument for that run. Bars may not move while this seal stands.

- B1 PE-0 closed-form branch entropies: absolute error < 1e-9.
- B2 PE-1 convergence: deviations strictly decreasing under eps refinement
  and consistent with sqrt-eps scaling within a factor 2.
- B3 Non-generic refusal: any silent count at a refused configuration
  invalidates the run.
- B4 PE-2-class reversibility: hidden recovery residual < 1e-9; retrace
  defect < 1e-9 for time-symmetric integrators; fixed-step drift < 1e-6
  (inherits T7 of PF0-FREEZE-001 and its dt = 1e-3, tau_max <= 40 domain).
- B5 Umegaki closed forms: residual < 1e-10.
- B6 DPI and monotonicity: no margin below -1e-10; every global divergence
  finite by assert.
- B7 Support-floor clearance: smallest reference eigenvalue at least 1e3
  times the support floor, asserted per model; divergences stable under
  floor variation across 1e-14..1e-10 within 1e-9.
- B8 Null controls: no-signalling and symmetry nulls < 1e-10 wherever the
  model admits them.
- B9 Classical anchors via the declared embedding: absolute error < 1e-9,
  including the orientation-merge equality (gap < 1e-9).
- B10 Uhlmann closed forms: residual < 1e-9.
- B11 Hierarchy ordering: any inversion beyond -1e-10 invalidates the
  instrument (the ordering is a theorem).
- B12 Flip protocol: arms drawn from one declared family with identical
  budget accounting; the anti-arm must be strictly worst on task or the
  run is uninterpretable rather than positive; verdicts read on held-out
  states only.
- B13 Quadratic-law fits: the fit-through-origin instrument must recover
  an exact quadratic law with residual < 1e-10.

## Instrument defect record

Four defects were found by failed first designs during the shakedowns and
are preserved here per the evidence discipline. Each is now a standing
control or assert.

1. **Exact-sample-hit blindness (PE-2).** A level equal to a sample value
   produced s = 0 at a grid point and the strict sign-change test silently
   missed both crossings. Exact hits are now refused as non-generic.
2. **No-signalling degeneracy (QO-0).** Excitation on the traced-out
   interior left every consumer divergence exactly zero by theorem; DPI
   passed vacuously. Interior excitation is now an asserted null control.
3. **Symmetry invisibility (QO-0).** The thermal single-site state
   (I + mX)/2 commutes with X rotations, hiding the excitation from the
   site-only consumer. Now an asserted null control and a concrete
   certificate-vacuity instance.
4. **Silent infinite divergence at the support floor (QO-0/QO-1).** At
   beta = 1 the smallest thermal weight (~2e-12) sat at the 1e-12 floor,
   a full-rank reference read as rank-deficient, the full-state divergence
   went silently infinite, and inf-minus-finite margins were vacuously
   positive. Fixed by the B7 clearance assert and per-divergence
   finiteness asserts; the affected first QO-0 record was regenerated and
   superseded.

## Non-claims

Sealing the instrument layer certifies measurement machinery only. No PE
or QO result changes label by virtue of this seal. Nothing here bears on
physical spacetime, thermodynamic entropy production, real horizons, or
quantum gravity.
