# The sealed runs of D8, OP4, OP1 and OP2, with four declared variants

Status: PLAN, 2026-10-13, on the owner's decisions of the same day: redo the four gates recorded at
their pilots as sealed, preregistered runs, D8 first, and carry four variants as declared secondary
arms. Not claim-bearing. Every definition, parameter rule and bar below is fixed before any variant
is probed, except the parameters marked PROBE, which are fixed by the stated READ-blind rules on the
probe.

## 1. Why, and what "properly" means here

D8, OP1, OP2 and OP4 were recorded at their pilots or confirmation, and a pilot grade is not a sealed
verdict. Each gate is now sealed and run as this repository requires. Its registration is frozen
with the pilot's tolerances and renamed `PREREG-*.md` in one commit, its families are entered in the
transformation registry, and it runs on its run seeds at its run resolutions, graded by the sealed
grader. The recorded pilots stay as they are; the sealed runs are new evidence beside them.

## 2. Fixes made before sealing (each READ-blind)

- OP1: a regime check on every world. A world whose persistence error differs from its pair's at the
  other resolution by more than a factor of 1.5 is reported and not graded. The pilot's
  $\nu = 0.03$, $n = 128$ world (0.177 against 0.351) would have been caught. The factor is fixed here,
  from that one case and before any run, and it looks only at persistence, never at a ranking.
- OP4: the subspace rule states its cap. $m'$ = the smallest multiple of 8 that is at least $2d$, and at
  most $m_0$, with $m_0 = 32$, so the cap binds only when $d > 16$. $d$ is the required count of the
  arm, $d_u$ for GRAM and $d_{un}$ for the unstable-plus-neutral variant.
- D8: Jobs are split per graded observer from the start (the pilot's suggestion). An $n = 192$ observer
  is also split by ladder halves if its estimated time exceeds 16 hours.

## 3. The four variants

Each variant reduces to an arm already run in a stated limit, and that reduction is a self-test check.

V1, unstable-plus-neutral Gramian (GRAM-UN; OP4 and D8). GRAM with its required count raised from the
positive exponents to the unstable and neutral manifold, $d_{un} = \#\{\lambda_i > -0.1\,\lambda_1\}$. Source:
Trevisan, D'Isidoro and Talagrand (QJRMS 136, 2010), who find the best subspace dimension near that
manifold's. The factor 0.1 is fixed here. On OP4's probe world it would count 9 directions (the six
positive ones and $-0.0014$, $-0.0042$, $-0.0064$, all above $-0.0083$), against GRAM's 6. In the limit
where no exponent is near zero, GRAM-UN equals GRAM.

V2, full-covariance sensitivity (ESA; D8, OP1, OP2). READ ranks a mode by its own variance times its
own sensitivity, the diagonal form of ensemble-sensitivity targeting (Ancell and Hakim, Mon. Wea. Rev.
135, 2007). ESA keeps the cross-mode covariance. The first-order change of the target tendency $T$
along the training fluctuations is $v_t = DT(w_t)(w_t - \bar w)$, one tangent call per training sample.
Then
$$\mathrm{ESA}_k = \frac{\|E_t[v_t\,(x_{k,t} - \bar x_k)]\|^2}{\mathrm{Var}(x_k)},$$
summed over the pair's real and imaginary parts. Here $DT$ is $N_w$, the derivative of the nonlinear
term, as in READ's sensitivity, since the linear terms are diagonal and couple no modes. The numerator
is computed as $\delta x_k^T V \delta x_k / T^2$ with $V_{ts} = \langle v_t, v_s \rangle$, the $T \times T$ Gram matrix of the responses,
so no field is stored per pair. This is the variance of $T$ explained by observing
pair $k$ alone, under linear regression. $T$ is the full tendency in D8 and the consumer's tendency
$P_C T$ in OP1 and OP2, as READ's sensitivity is in each. When the modes are uncorrelated and $DT$ is
constant, ESA equals READ.

Dropped from every sealed run, D8 and OP4 and OP1 and OP2 (owner, 2026-10-14), when the probe's
stability rule for its sample count failed (Section 4). It is recorded as a declared variant that did
not reach a sealed arm.

V3, READ in the kinetic-energy metric (READ-KE; D8, OP1, OP2). OT's metric $G$ is a declared choice, and
targeting depends on it (Palmer, Gelaro, Barkmeijer and Buizza, J. Atmos. Sci. 55, 1998). READ
measures the read in the enstrophy norm (vorticity). READ-KE keeps each gate's READ exactly, its
amplitude factor and its averaging, and changes only the norm in which the response is measured to
the velocity norm of the theory note and D8. In D8, READ is $E_t[a_k(t)\,s_k(t)]$ with
$s_k = (\|N_w e_{re}\|^2 + \|N_w e_{im}\|^2)/2$ in the enstrophy norm. READ-KE is the same with
$s^{\mathrm{KE}}_k = (\|N_w e_{re}\|^2_{\mathrm{KE}} + \|N_w e_{im}\|^2_{\mathrm{KE}})/2$. In OP1 and OP2 the consumer's
mask stays in place. This is not D8's KE control, which ranks by the mode's own kinetic energy and has
no read. With the enstrophy norm in place of the velocity norm, READ-KE equals READ. (Corrected
2026-10-13 before any code ran: the first wording used the mode's fluctuation as the input, which is
not D8's READ and would not reduce to it.)

V4, singular-vector targeting (SV; OP4 and D8). The leading singular vectors of the tangent
propagator over the window, in the subspace approximation: propagate the leading tangent subspace
$U$ over $T_w$ as OP4 does, take the SVD $\Phi U = A S B^T$, and score pair $k$ by
$\sum_{i \le d_u} \sigma_i^2 \,\|(U b_i)[k]\|^2$, the targeting score of Buizza and Montani (J. Atmos. Sci. 56,
1999), summed over OP4's windows. Rank by score. It uses OP4's windows, $T_w$ rule and subspace. With a
single window and one singular vector, it ranks pairs by the leading direction's amplitude.

## 4. The probe of the variants (before sealing)

World and seeds: D8's pilot worlds and seeds, so the variants are paired with D8's recorded budgets for
BALL, READ, ENSTROPHY and KE and with OP4's GRAM budgets. The probe runs on the two $n = 96$ worlds
($\nu = 0.03$ and 0.02), both trajectories, which is 4 cells per variant, on Atlas. Every variant's
ranking or instrument is computed from the training trajectory alone. Its nudging budget is measured
by D8's protocol, unchanged. For OP1 and OP2, ESA and READ-KE are added as rankings and probed on OP1's
cached probe trajectories, at no simulation cost.

What the probe may set: only the items marked PROBE. That is the number of training samples ESA
needs, chosen by split-half stability of its ranking (Spearman of the two halves' scores at least
0.9, READ-blind). It is not the variants' standing, which the probe reports and which changes nothing.

Outcome for ESA (2026-10-14). On the probe world $\nu = 0.03$, $n = 96$ (`VARIANTS/esa_stability.py`), the
all-pairs Spearman of the two halves was 0.373 at 80 samples, 0.728 at 320, 0.878 at 1280, 0.886 at 2560
and 0.890 at 5120, about 0.004 more per doubling, and 5120 samples took about 4 hours of one Atlas core.
The rule was not met at any count tried and was not changed. It was reported to the owner with three
options (drop ESA, extend to 10240 and 20480 samples, or accept 5120 as a recorded revision), and the
owner dropped ESA. ESA's ranking was never nudged.

## 5. Claims and the correction for several arms

Each gate keeps one primary claim, as registered: D8's READ against the best control, OP4's GRAM
against BALL, OP1's and OP2's READ against the better control. The variants are secondary arms. Each
is reported in full, cell by cell, and none can rescue a primary claim.

A secondary arm "beats" a control only by a declared paired test with a correction across the arms of
its gate. On each gate's run cells, the sign test of the arm against the control is one-sided, with
Holm's correction across that gate's secondary arms at a family-wise level of 0.05. Ties are dropped
from the count. The run has 16 cells in D8 and OP4 at $K = 4$ (2 viscosities, 2 resolutions, 4
trajectories), or 32 at the proposed $K = 8$ (Section 6). With four arms, the smallest Holm threshold is
0.0125. At 16 untied cells that needs at least 13 ahead (the one-sided p is 0.0106 at 13 of 16 and 0.0384
at 12 of 16). At 32 untied cells it needs at least 23 ahead (0.0100 at 23 of 32, 0.0251 at 22 of 32).
Holm's thresholds for the remaining arms are 0.0167, 0.025 and 0.05. Margins in ladder steps, as D8's
bars use, are reported beside the test.

With ESA dropped (2026-10-14), D8 and OP4 have three secondary arms, READ-KE, GRAM-UN and SV, run at
$K = 8$. At 32 untied cells Holm's thresholds are 0.0167, 0.025 and 0.05, and they need at least 23, 23
and 22 cells ahead. OP1 and OP2 keep one secondary arm, READ-KE, tested at 0.05 with no correction.

## 6. Platform, order and cost (estimates, not measurements)

Platform. NRP has no cap on CPU Jobs that obey its rules (owner, 2026-10-13). So the constraint is
wall-clock and the per-Job bound, not CPU-hours, and the heavy work fans out on NRP. Every Job is in
the exempt class (1 CPU, 2 GiB), never sleeps, is bounded by `timeout`, is submitted through
nats-bursting with a fresh name, and passes the submitter's preflight. Usage stays within the policy
bands, at default priority. Jobs are split finely enough that the slowest node finishes inside its
bound. The pilot measured one graded observer at $n = 128$ at 4 to 11 hours, so each graded observer
at $n = 192$ is one Job split by ladder halves. Results travel by the saver and by a log-independent
path (`nats_results.py`, to be committed and tested first), since three pilot logs were lost. Atlas
keeps the small work: self-tests, and OP2, which reuses OP1's trajectories.

Decided by the owner (2026-10-13), before any run and READ-blind: the run uses $K = 8$ test trajectories
per world, in place of D8 draft's $K = 4$. D8 and OP4 therefore have 32 run cells, and Section 5's
sign test needs 23 of 32 untied cells ahead for the strictest Holm threshold. The extra trajectories
cost wall-clock only through the slowest Job.

1. Code the four variants (`op_variants.py`, importing D8's and OP4's modules), with a self-test that
   checks every reduction in Section 3. Commit and test `nats_results.py`.
2. Run the variant probe on NRP, one Job per (variant, world, trajectory), with the Gramian phase as its
   own Job per world. That is about half a day of wall-clock, set by the slowest nudging Job.
3. Write the registrations: D8 with READ-KE, GRAM-UN and SV as secondary arms (D8 and OP4 share the
   run); OP1 and OP2 with READ-KE. ESA was dropped from both (2026-10-14, Section 4). Seal all of them
   in one commit per gate.
4. Run D8 and OP4 on NRP, one Job per (world, trajectory, arm, ladder half where needed). The CPU total
   is several thousand hours, and the wall-clock is about one day, set by the slowest $n = 192$ Job. Run
   OP1's trajectories on NRP as one Job per world. Run OP2 on Atlas from them.
5. Grade by the sealed graders, and rewrite OP3 and the outline from the verdicts.

## 7. What would change the paper

A secondary arm that beats BALL under Section 5's test on D8's run would be a positive result about
choosing what a nudged turbulent copy must read. The paper would then report it as a variant found by
declared search over four arms, not as the primary claim. If no arm beats BALL, the "system" reading
stands as a sealed verdict, now tested against the strongest variants the literature supplies.
