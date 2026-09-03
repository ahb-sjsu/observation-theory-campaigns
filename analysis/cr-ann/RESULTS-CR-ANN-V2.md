# RESULTS — PREREG-CR-ANN-V2 graded run

**Verdict: FAIL** (executed 2026-09-03, as sealed at 16b2f4c; record
`prereg/graded_v2.json`, runner `cr_ann_v2_graded.py`). Valid run: MC1
isotropic control passed on every unit and seed, MC3 pre-satisfied at seal
(4 misaligned + 1 matched), MC4 sealed scan, MC2 by commit order. B1 failed
2/4 misaligned units; B2 passed; B3 failed. Verdict = B1 ∧ B2 = FAIL,
committed as executed. Nothing is re-graded.

## Graded results (three seeds; sealed bars)

| unit (arm, H_xfit) | gains by seed | mean | bar | result |
|---|---|---|---|---|
| privacy_aita (mis, .043) | +.101/+.082/+.063 | **+.082** | ≥.010 | **pass** (conv ≈ 190%) |
| epistemic_sc (mis, .041) | +.034/+.033/+.025 | **+.030** | ≥.010 | **pass** (conv ≈ 74%) |
| fairness_mhs (mis, .085) | +.006/+.008/+.009 | +.008 | ≥.010 | **fail by .002** (conv ≈ 9%) |
| societal_env (mis, .065) | +.000/+.006/−.013 | −.003 | ≥.010 | **fail** (conv ≈ 0; one seed < 0) |
| autonomy_dark (matched, −.003) | +.012/+.008/+.010 | +.0099 | ≤.010 | **pass by .0001** |
| care_moralstories (excluded, D .673, H .270) | **+.266/+.292/+.263** | **+.274** | descriptive | conv ≈ 101% — the campaign's largest effect, in the excluded row |

B3: Spearman(H_xfit, mean gain) = **0.143** (< 0.6, fail); S2 slope 0.990
(driven by care's point). Embedding-fidelity collapse universal: recall@1
0.006–0.049 on every unit and seed against ~1.0 for L2. Oracle ceiling ≥ 0.999
everywhere — candidate generation never binds, again.

## Honest read — what two sealed FAILs now establish

1. **The dissociation phenomenon is real and repeatedly demonstrated.** Gains
   up to +0.29 with recall@1 collapsed to 0.014; qualitatively positive in
   5 of 6 units here (13 of 16 graded anisotropic consumer-units across V1+V2);
   the matched null held both times; the isotropic control has never once
   moved. That part of the law survives everything thrown at it.
2. **The quantitative bar family is refuted, twice, for a deeper reason than
   either post-mortem guessed:** per-unit conversion of measured headroom
   spans TWO ORDERS OF MAGNITUDE (190%, 74%, 9%, ≈0% in this single sealed
   family — after cross-fit qualification and single-domain units fixed V1's
   instrument defects). No single conversion constant can cover that spread,
   and cross-fit H does not order it (B3 0.143). Neither headroom (V2) nor
   published reliability (V1) predicts which units convert.
3. **The D-floor keeps excluding the largest effects.** V1: identity_attack
   (excluded at H+0.026) produced the run's biggest gains. V2:
   care_moralstories (excluded at D 0.673) converted ~101% of a +0.270
   headroom — three seeds tightly clustered. A qualification floor built to
   protect the misaligned arm from weak probes has now twice filtered out the
   strongest confirmations of the effect it guards.
4. **privacy_aita converted ~190% of its measured headroom** — gain exceeding
   H means cross-fit point-accuracy D UNDERESTIMATES what the probe's read
   retrieves (retrieval-by-P_C is not bounded by the probe's own
   classification accuracy). H = D − A is the wrong potential function for
   this effect.

## Where this leaves the campaign (owner's call)

Two sealed families, two honest FAILs, one twice-replicated phenomenon whose
magnitude-determinant is demonstrably not what either prereg posited. The
options as we see them: (a) a V3 with a claim restructured to what is actually
supported — per-unit existence + fidelity collapse + matched null, no
universal conversion constant (an "existence and boundary" family, much
weaker but honest); (b) stop bar-chasing and write the paper on the graded
record as it stands: the conditional dissociation exists, its conversion is
unit-idiosyncratic, and the two FAILed preregs are the evidence of an honest
search for its law; (c) investigate the conversion determinant exploratorily
(what separates privacy/care/epistemic from fairness/societal?) BEFORE any
new seal. No new family is drafted here; per the amendment discipline this
document only records what was executed.
