# Exploration (substrate probe + inconclusive prototype): stellarator QS-vs-consumer

**Status: EXPLORATION / PROTOTYPE, NOT a sealed cell.** 2026-08-24. Chip 🕒🌀.
Recorded honestly (the program keeps negatives), with the correct path forward.
`fam_stell.py`, substrate = `qsc` (pyQSC, Landreman) near-axis QS construction.

## What was probed and what held

The **substrate probe succeeded**: `qsc` installs and computes real near-axis
quasi-symmetric stellarators fast, exposing both the proxy (`B20_variation`, the QS
residual) and consumer geometry (`r_singularity` = usable-surface radius,
`max_elongation`, `d2_volume_d_psi2` = magnetic well). The consumer-vs-proxy
**tension is real at the base configs**: `precise QA` is QS-excellent
(`B20_variation` 0.015) yet a magnetic *hill* (`V''` +93.7, interchange-unstable at
order r²) — the QS certificate is blind to the stability the confinement consumer
reads. (`SIMSOPT`/`DESC` are the heavier full-equilibrium/optimization substrates.)

## Why the quick prototype is inconclusive (honest)

The prototype family — random near-axis perturbations of the QS-good bases (QA, QH)
— **does not exhibit the false-clear**. Across seeds: `qs_certified_frac` → 0 at a
tight threshold (perturbing a QS-good base only worsens QS), and the QS↔consumer
**rank correlation is ~0.85** (positive), not the near-zero dissociation the claim
needs. The reason is structural: random perturbation of a jointly-good base worsens
*all* metrics together (distance-from-base co-variation), so QS and the consumer
co-vary. **The real QS-vs-consumer tradeoff is a *directed* phenomenon** — a
QS-*optimization* trajectory drives the residual down while elongation rises and
usable volume shrinks — which random sampling around a good base never reaches.
Recorded as inconclusive; not tuned into a pass.

## The cell that would work (not yet built)

- **Directed substrate:** a **QS-optimization trajectory on SIMSOPT or DESC** —
  minimize the QS residual and watch the consumer metrics (elongation, usable
  volume) and, crucially, a **transport-grade consumer** (`ε_eff` neoclassical
  ripple, or a fast-ion loss fraction) degrade. The false-clear = QS-certified along
  the trajectory but transport/buildability failing.
- **The expensive-witness caveat stands:** a faithful consumer needs real transport
  (a reduced gyrokinetic / neoclassical proxy), which is costly — this is a
  **collaborator-gated** cell (a stellarator-optimization group; SIMSOPT/DESC
  authors), like XPROTO-CCA (SDR) and XPROTO-QUANTUM (IBM hardware).
- The OT delta remains a **reframing + the κ/alignment quantification** of a tension
  the fusion field already works on (QS ≠ good transport/stability), not new plasma
  physics.

Conclusion: substrate viable, framing sound, quick prototype negative for the honest
reason above. Hardening requires an optimization trajectory + a transport consumer +
a domain collaborator.
