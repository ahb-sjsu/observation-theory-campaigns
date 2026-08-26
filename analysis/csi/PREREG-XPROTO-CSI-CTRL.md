# PREREG-XPROTO-CSI-CTRL — event-triggered CSI reporting that auto-realizes the refresh floor

**STATUS: UNSEALED.** FAMILY-CONSTRUCTED: 2026-08-25. Earliest compliant seal
**2026-08-26** (`csi_ctrl_check.py` codes the cooling-off). Graded seeds {20260826,
20260827, 20260828}, disjoint from the shakedown's {0,1,2}. Substrate = real Sionna 5G NR
LDPC curves + TDL-A fading (`csi_sionna`); empirical HARQ NACK rate. The *technique* cell
of the WCNC paper (turns the two measured relativities into a controller).

## The claim

The refresh floor $P^\star\!\approx\!0.177\,T_{\mathrm{coh}}$ (XPROTO-CSI) can be realized
*without estimating Doppler* by an **event-triggered (send-on-delta) reporting rule**: hold
the last reported CSI, and fire a new report the moment the live channel drifts from it by
$>\theta$ dB (a sample-and-hold + comparator; analog-realizable). Because a faster-fading
channel crosses $\theta$ sooner, the effective report period shrinks $\propto
T_{\mathrm{coh}}$ automatically. We claim: (i) send-on-delta holds BLER roughly constant
across an order of magnitude of mobility; (ii) its emergent effective period recovers the
coherence-floor slope ($P_{\rm eff}\!\approx\!\kappa\,T_{\mathrm{coh}}$, $\kappa\!\sim\!0.2$),
re-deriving OT-14 from a one-comparator circuit; (iii) it Pareto-dominates fixed
periodicity---matching report-every-TTI reliability at a fraction of the feedback, while a
low-overhead fixed period false-clears. The threshold $\theta$ is the consumer knob.

## Family F-CSI-CTRL (constructed + shaken down 2026-08-25)

`fam_csi_ctrl.py`: Doppler swept $f_D\in\{5,10,25,50,100,200,400\}$\,Hz. Policies over the
same TDL-A trace: **send-on-delta** ($\theta{=}2$\,dB), **fixed period** $P\in\{1,10,40,80\}$
TTI, and a parametric $P^\star{=}$round$(0.177\,T_{\mathrm{coh}})$ for reference. Metric =
empirical HARQ NACK rate + feedback overhead (reports/TTI). Target BLER $0.10$.

*Demonstrated (seeds {0,1,2}): SoD BLER $\approx 0.11$--$0.13$ for $f_D\ge 10$\,Hz;
$P_{\rm eff}/T_{\mathrm{coh}}\approx 0.18$--$0.30$ (low--mid mobility); SoD overhead
$0.12$@10\,Hz $\to 0.78$@400\,Hz; fixed-$P{=}40$ BLER $0.25$--$0.38$; fixed-$P{=}1$ BLER
$\approx 0.10$--$0.12$ at overhead $1.0$.*

## Bars (bind at seal; checked against the family record first)

- **B1 — send-on-delta holds reliability across mobility.** Per seed:
  $\max_{f_D\in\{10,\dots,400\}}\texttt{sod.bler} \le 0.16$.
- **B2 — Pareto dominance over report-every-TTI.** Per seed, at $f_D{=}25$:
  $\texttt{sod.overhead}\le 0.5$ AND $\texttt{sod.bler}\le 1.4\,\texttt{fixed1.bler}$
  (matches the safe reference's reliability at $\le$ half its feedback).
- **B3 — a low-overhead fixed period false-clears.** Per seed:
  $\texttt{fixed40.bler}(f_D{=}100)\ge 0.20$ (the tradeoff is real).

**Manipulation checks (bars too):**
- **MC1 — overhead auto-scales with mobility.** Per seed:
  $\texttt{sod.overhead}(400)\ge 3\,\texttt{sod.overhead}(10)$.
- **MC2 — the floor emerges ($P_{\rm eff}\!\propto\!T_{\mathrm{coh}}$).** Per seed, for
  $f_D\in\{10,25,50\}$: $0.1 \le \texttt{sod.p\_eff}/\texttt{tcoh\_ms} \le 0.4$
  (TTI $=1$\,ms, so $T_{\mathrm{coh}}$ in TTI equals tcoh\_ms; the ratio is the emergent
  $\kappa$, bracketing the measured $0.177$).
- **MC3 — safe reference sane.** Per seed: $\max_{f_D}\texttt{fixed1.bler}\le 0.14$.

**Verdict:** any MC fail → VOID; all MCs + B1–B3 every seed → PASS; else FAIL, kept.
**Kills:** $\texttt{sod.bler}(200) > 0.25$ (SoD fails to hold reliability) or
$\texttt{sod.p\_eff}(10)/\texttt{tcoh\_ms}(10) > 0.6$ (no coherence tracking).

## Seal procedure

On 2026-08-26+: confirm `CTRLREP-family.json` PASSes `--check-family`, reread, flip STATUS
to SEALED, commit; on Atlas run `fam_csi_ctrl.py --seeds 20260826 20260827 20260828 --out
CTRLREP-graded-raw.json`, pull, `csi_ctrl_check.py` → commit `XPROTO-CSI-CTRL-graded.json`.

## Scope

Same substrate/limits as XPROTO-CSI. $\theta{=}2$\,dB holds BLER $\approx 0.12$ (near, and
tunable to, the $0.10$ target; $\theta$ trades overhead for reliability---the consumer
knob). The controller is one held value + one comparator (analog-realizable as a
level-crossing / Lebesgue sampler); no Doppler estimator. OT's delta: the refresh-floor law
realized as an event-triggered rule that Pareto-dominates fixed periodicity. Provenance:
the reviewer's "add a technique" + "analog circuit" prompts; `fam_csi_ctrl.py` +
`csi_ctrl_check.py`.
