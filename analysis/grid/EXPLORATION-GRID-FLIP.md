# EXPLORATION — the Flip in the grid security certificate (kept, NOT registered)

**Date: 2026-08-26. Status: inconclusive on case14; not pre-registered; no seal.**

We tried to transfer the two-consumer verdict inversion (XPROTO-QOT-FLIP,
XPROTO-CSI-FLIP) to the grid cell. The construction split the case14 loads into
two zones with independent AR(1) walks, sorted lines into fleets by which zone
dominates their AC power-flow sensitivity, and allocated a matched certification
margin budget by zone-1 sensitivity (policy A) or zone-2 sensitivity (policy B).

Two problems, both disqualifying, both kept.

1. **The inversion is present but the Z1 side is within noise.** Across seeds
   {0,1,2} the Z2-fleet clearly prefers B (0.031-0.042 against 0.036-0.052), but
   the Z1-fleet's preference for A is marginal (seed 2: 0.0119 against 0.0121).
   case14 is too small for this: the zone split leaves fleets of 4 and 6 lines
   with overlapping sensitivities, so the axes are barely misaligned.

2. **The control was mis-designed, and it caught us.** We ran the same margin
   policies under one global load walk as the intended null. It also inverted.
   That is because this "null" kept the consumers split by the same covariate the
   margins target, so it tests walk-independence rather than read-alignment. The
   correct null, as in the optical and radio cells, is a THRESHOLD PAIR: the same
   lines read at two loading limits, where redistribution cannot invert. The
   broken control also exposes what the weak flip here mostly is: margin aimed at
   a fleet helps that fleet. Without strongly misaligned axes, that is targeting,
   not the mechanism.

**What would make this registrable.** A grid with real zonal structure and enough
lines for clean sensitivity separation (case118 or 1354pegase, with zones from
the case's own areas), the threshold-pair null, and a dominance-ratio gate on
fleet membership set before the run. Until then the honest statement is: the flip
needs misaligned read operators, and case14's two zones do not provide them.

Record: `GRIDFLIPREP-family.json` (seeds {0,1,2}, kept as executed).
Code: `fam_gridflip.py`.
