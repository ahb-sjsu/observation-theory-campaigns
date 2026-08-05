# PREREG-PF6-001 (TEMPLATE — not sealed; bind and seal after PF-5 passes)

Slots marked <<...>> are bound before sealing; everything else is fixed now.

## Claim under test
The events of <<FAMILY>> are physical, not coordinate-specific folds:
their rates are invariant under passive transformations, and every
observer dependence is predicted by the declared detector model.

## Instrument (frozen)
`python/pf6_covariance.py` at commit <<COMMIT>>, validated in
`results/pf6-instrument.json` (evidence d064041): translation,
reparametrization, boost (hyperbolic family), gauge machinery,
observer/detector audits.

## Grid
<<Cells and members mirroring the sealed PF-5 grid; shift values,
alpha grid, observer-alpha grid — declared here>>

## Bars (fixed now)
1. Translation: every event worldpoint equivariant < 1e-6; per-cell
   event counts exactly equal.
2. Reparametrization (alpha = 2): per-worldline event counts exactly
   invariant; rate-per-parameter ratio = alpha within 1e-12.
3. If the family carries the hyperbolic structure: flow-boost
   commutation < 1e-10, invariant conservation < 1e-10, future-cone
   margin > 0 across the declared rapidity grid.
4. Gauge: binds only if the family declares an EM coupling; then both
   gauges must give identical histories < 1e-8 and the exact canonical
   shift, else the clause is recorded not-applicable.
5. Observer audit: N(alpha) from the observer record equals the
   detector-model prediction EXACTLY at every declared alpha, per
   member. One unpredicted mismatch rejects.

## Falsification
A rate that changes under any passive transformation or applicable
gauge change rejects the family. Observer-dependent counts are
retained only through bar 5.
