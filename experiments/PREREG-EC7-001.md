# PREREG-EC7-001 — EC-7: closed-loop control (OT-EC Campaign 7)

**SEALED at the commit ledgered in `SEALS.md`.** The governed run executes
ONCE after the sealing commit, on the governed seed below, and is reported
regardless of sign in the track document and README status ledger.

## Claim under test

The final campaign of the OT-EC paper (Paper VIII §XI), whose own gate —
"only after the estimation and sensing claims survive" — was opened by
EC-2/3/4/5: a **consumer-derived state penalty inside an LQG loop**, judged
on the actual downstream consumer at **matched control effort**, with
stability independently audited. Interface 1 of the paper (consumer
geometry as the provenance of the control objective), in its simplest
certainty-equivalent instantiation.

## Design

Plant `x⁺ = Ax + Bu + w` (d=12, m_u=4, random stabilizable B); planted
rank-3 linear consumer `z = Lx`; endpoint = mean `‖Lx‖²` over held-out
closed-loop rollouts (regulation judged AT THE CONSUMER). Controllers are
certainty-equivalent LQG: Kalman filter with a FIXED consumer-agnostic
sensing schedule (iso-greedy, k=3 — the scheduling question was Campaigns
2/3; only the control OBJECTIVE varies here), `u = −Kx̂` with K from the
DARE for penalty (Q_ctrl, ρI). Per (system, arm), ρ is bisected so mean
`‖u‖²` on calibration bundles hits a common target (the oracle arm's effort
at ρ=1); evaluation on held-out bundles, common random numbers across arms.

Arms: `oracle` (Q_ctrl = P_C), `blind` (Q_ctrl = P̂_C from query-only
probing exactly as GO-087, probe cost charged against the sensing budget),
`iso` (I), `hand-diag` (best of a 5-member diagonal family granted
calibration-endpoint access — the competent-engineer baseline; a tie is
the paper's "operationally unnecessary" boundary and is reported either
way), `shuffled` and `anti` controls (charged).

**Integrity gates** (audits, not predictions): closed-loop spectral radius
< 1 for every (system, arm); no rollout state-norm divergence; realized
efforts near the common target.

## One disclosed calibration pilot

**Pilot 1** (K1 0.069, K2 0.714, K3 0.061, all integrity and controls
True): healthy at first light with THIN margins on K1 and K2 — the DARE
amplifies probe noise in the recovered operator more than scheduling did,
so the blind-capture ratio (0.714) sits well below the 0.87–0.95 range of
the earlier campaigns. Floors frozen conservatively below the observations
(K1 0.04, K2 capture 0.60) rather than at the draft values the pilot would
have brushed. An aborted first launch (killed before any output for a
performance-only change: effort-matching bundles 12→3, bisection 18→14 —
CRN makes few bundles sufficient since every arm matches on the same ones)
is disclosed for completeness; it produced no measurements.

```yaml
id: PREREG-EC7-001
date: 2026-08-19
retrospective: false
kind: consumer-derived LQG penalty at matched control effort, stability
      audited, with the blind recover/match arm (Campaign 7, OT-EC paper)
harness: python/ec7_closedloop.py
code_hash: sha256:59a1cb5d37728c26bca9e092bbcf65f430de526b62edf1e87e7e6b59da79ef8a
governed_seed: 20260828
calibration_seed: 20260827
frozen_config:
  N_sys: 20
  M_U: 4
  N_cal_bundles: 3
  diag_family: 5
  lambda_p: 0.002
  delta_k1: 0.04      # K1 gate (cal 0.069)
  eps_k2: 0.40        # K2 gate: blind capture >= 0.60 (cal 0.714, thin)
  delta_k3: 0.00      # K3: at least tie vs best-diagonal (cal 0.061)
  effort_band: 0.10
internal_calibration:
  pilot1: {K1: 0.069, K2: 0.714, K3: 0.061, stable: true, bounded: true,
           effort_matched: true, shuffled_gap: 0.162, anti_ok: true}
sealed_predictions:
  K1: oracle-penalty LQG beats iso-penalty LQG on the consumer endpoint at
      matched effort by >= 4% mean relative
  K2: the probe-charged blind penalty captures >= 60% of the oracle
      advantage over iso (pooled)
  K3: the full consumer geometry at least ties the best hand-tuned
      diagonal (>= 0); a positive margin claims structure-beyond-diagonal,
      a tie is the operationally-unnecessary boundary — either is reported
integrity: [all closed loops spectral radius < 1, states bounded,
            efforts within band of the common target]
controls: [shuffled-vs-iso >= -0.02, anti loses to oracle and not better
           than iso (2% slack)]
stopping: fixed-n, single governed run
falsification: K1 fail -> consumer geometry adds nothing to the control
  objective at matched effort; Interface 1's simplest instantiation is
  refuted. K2 fail with K1 pass -> the control interface needs privileged
  consumer access (the recovery boundary, in the loop). Integrity fail ->
  no comparison is claimed. All reported at equal prominence.
amendments: []
```

## Scope and non-claims

Certainty-equivalent LQG on linear plants with a planted linear consumer —
the simplest closed-loop instantiation; nonlinear consumers inside MPC
(where P_C(x) is trajectory-dependent and Proposition 1's failure bites),
constraint handling, and robust-stability margins are follow-on. The
sensing schedule is deliberately consumer-agnostic to isolate the
objective question; combining consumer-aware scheduling AND control is
future work. Stability is audited by spectral radius and bounded states in
simulation — not a robust-control certificate.
