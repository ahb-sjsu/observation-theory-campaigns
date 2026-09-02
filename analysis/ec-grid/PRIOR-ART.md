# EC-grid prior-art sweep — 2026-09-02

Instruments: arXiv API + DBLP API (session WebSearch budget spent; Semantic
Scholar rate-limited twice, 429). Coverage caveat, stated up front: the PES
placement literature lives heavily in IEEE Xplore, which none of these
instruments index fully. This sweep is binding for arXiv-visible work; an
IEEE Xplore pass (owner login) is a REQUIRED pre-submission item and is on
the prereg checklist.

## Found — cite and delineate

1. **Application-specific PMU placement exists** and must be credited as a
   category: placement for ambient-data mode estimation / oscillation
   monitoring (ISGT Europe 2016 and the modal-observability line), and
   multi-objective placement including a voltage-stability index (2020).
   Delineation: these optimize an application's own observability or an
   index, not a decision-derived weighting of the ESTIMATOR's covariance;
   none score individual sensors by V_C = tr(P_C ΔΣ) with P_C from the
   decision's Jacobian.
2. **Covariance-optimal placement** (A/D-optimal): empirical-Gramian dynamic
   placement (2014), MISDP Kalman-covariance placement for DAE models (2025).
   Generic estimation accuracy; the classical baseline our Δtr column
   implements.
3. **Joint sensor deployment + downstream model** (2026, physics-informed
   graph transformer for attack detection): the closest in spirit — placement
   co-optimized with a learned end task. Delineation: the task weighting is
   LEARNED end-to-end for one task; ours is DERIVED (the decision function's
   Jacobian, no training against placement outcomes), applies to any consumer
   the operator names, and the paper's content is the measured
   dissociation/inversion, which that work does not examine.
4. **Decision-focused learning in power systems**: task-based end-to-end
   model learning (Donti–Amos–Kolter 2017, grid example) and successors (ILO
   for ramping cost 2025; decision-focused EV demand response 2024). These
   optimize FORECAST/MODEL parameters for downstream decisions; none value
   sensors or measurements. The forecasting-side analogue of our claim —
   cite as the movement the sensor-side result joins.
5. **Generic weighted-trace sensor selection** (Joshi–Boyd; weighted-trace
   scheduling; Tzoumas et al. LQG co-design): already cited in Paper VIII,
   which positions the OT contribution as the PROVENANCE of the weight.

## Not found (the open flank, two readings disclosed)

Zero arXiv results for: "value of information" × power × measurement;
"data valuation" × state estimation; "sensor selection" × "weighted trace";
"goal-oriented" × state estimation × power. No paper found that (a) scores
grid sensors by a decision-derived P_C, (b) demonstrates the
equal-variance-reduction / divergent-decision-value dissociation, (c) shows
a cross-consumer inversion (no consumer-independent sensor ranking), or
(d) evaluates sensor selection on a violation false-clear endpoint. Reading
one: the corner is open. Reading two: vocabulary mismatch with PES usage —
which the IEEE Xplore pass must settle before any novelty sentence is
written.

## Consequence for the campaign

Position exactly as Paper VIII does: the covariance algebra and
weighted-trace objectives are classical; application-specific placement
exists as a category. The registered contributions are (1) P_C derived from
the named decision's own read, uniformly across consumers; (2) the measured
dissociation and structural inversion on standard test cases (this
shakedown); (3) the operational false-clear endpoint at matched budget (next
cell); (4) the Lean-verified rank-one identity closing to realized error
(2.1% MC agreement). Never claim "first application-aware placement."
