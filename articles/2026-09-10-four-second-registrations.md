# Four second registrations: what the OD track's INDETERMINATE gates were made of

Andrew H. Bond, 2026-09-10. Draft 0.1. Every number below is read from a sealed record in
`experiments/OD/` of this repository, cited by gate. Nothing here is a new claim.

## Summary

The Observational Discovery track ran its declared order to the end on 2026-09-10 with one
PASS (D3v2), one standing law with its scope (D2v7 with D2v9), one deferral (D4) and
INDETERMINATE at D1, D3, D5, D6 and D7. INDETERMINATE is the verdict a sealed grader returns
when some bar misses without any fail clause firing, and it says nothing by itself about
why. This note records the second registrations of four of those gates, D1, D5, D6 and D7,
each written after its first record named what had missed and whether the miss belonged to
the claim, to the instrument or to a definition. The rule for a second registration was
the same as for a first. Bars and tolerance rules went into code before the pilot, the
world got fresh seeds, the registration was sealed by rename with its blob hash in the track
document, and the run was graded by the sealed grader and committed as executed. What the
four second registrations found is that the misses of D5, D6 and D7 were the instrument's or a
definition's, and that removing them moves the record rather than the verdict, and that
the miss of D1 was its tolerance rule's. Three of the four returned INDETERMINATE again, each
by a different single bar, and each of those bars is now a boundary with a name. The fourth,
D1v2, passed every bar in every cell on a second fresh seed. Section 6 records the third
registrations that followed the same day, the definitions the second ones named: D7v3 passed on
a finer resolution ladder, D6v3 passed with feasibility decided at the cap and a tie-break for
the exact search, and D5v3 held the bar it changed and exposed one more definition in its
control.

## 1. What a second registration may and may not do

A second registration takes the first's claim and changes one thing that the first record
named. It may not move a bar after seeing a run. It may declare a scope the first run found,
provided the scope is stated before the second pilot and the region outside it is run and
reported. It may replace a part of the instrument the first record identified as the slack,
provided the replacement is fixed before the pilot and the old part is computed beside it
and recorded. It may replace a tolerance rule that the first record identified as carrying no
margin. It may drop a clause the first registration said in advance would fail and did. What
it may not do is search for a passing configuration, and the discipline that prevents it is
the one that governs first registrations, code before pilot and seal before run.

## 2. D5 and D5v2: the transition in Burgers shock formation

D5 asked whether the observer-relative transition approaching a shock, measured as the
share of a carried perturbation's energy that a spectral reader of budget B still sees,
converges in resolution, collapses on B over the front wavenumber, leads the classical
alarm, and stays silent on a regular two-dimensional flow. Its run held convergence (0.03
to 0.13 against 0.21) and the collapse inside the tolerance (median bin IQR 0.085, 0.048 and
0.034 against 0.13), and it beat the unscaled null by 0.54 and 0.48 at viscosities 0 and
0.005 but by only 0.87 at 0.02, outside the 0.8 the bar asked. The lead clause failed as the
registration had said it would, since the classical extrapolation is exact for inviscid
Burgers, and the control clause failed because a two-dimensional flow moves perturbation
energy past a small budget whether or not a front forms.

D5v2 took the collapse as the claim, declared the viscosity scope at 0.005, dropped the lead
and alarm clauses, and replaced the alarm control with the control the claim needs: the same
scaling on the two-dimensional flow must organise nothing. The control's own front
wavenumber was recorded so that the construction is identical on both flows. On the run the
collapse held inside the scope at 0.48 and 0.39 of the null against a bar of 0.75, and the
control's scaled scatter was 1.02 times its unscaled scatter against a bar of at least 0.75.
The collapse is the forming front's, not a general property of budget against gradient.
The verdict is INDETERMINATE by the convergence bar on one of four initial conditions,
whose read fractions at N = 256 and 512 differ by 0.18 against 0.16 at budgets 2 and 4 near
0.9 of the shock time, where its front is the sharpest of the four and the coarser grid
under-resolves it. The boundary now on record is that the instrument's convergence in
resolution is not uniform across initial conditions at the smallest budgets near the shock.
One more thing moved. At viscosity 0.02 the collapse on this draw was 0.64 of the null,
inside the bar the registration would have set, where D5's four initial conditions gave
0.87. The boundary D5 found at that viscosity was its initial conditions' and not the
viscosity's, so the declared scope stands unconfirmed and unneeded on this draw.

## 3. D6 and D6v2: sensor placement by the spectrum

D6 asked whether the count of directions identifiable at a budget on the window Gramian is
the right quantity to place sensors by. Greedy on that count needed strictly fewer sensors
than the energy ranking in 16 of 27 cells where placement mattered and never more than a
random ordering, was within 1.33 of the exhaustive optimum in all 50 checkable cells and
equal in 45, and left a tenth more forecast time on the growth worlds. It missed by two
single cells. In one, greedy reached the sensor cap of 12 without the required count. In
the other, an unseen Lorenz-96 world, the energy ranking found the optimum with one sensor
fewer than greedy. Both were greedy's misses and not the spectrum's, and the record named
the repair: the exhaustive optimum where feasible and greedy beyond.

D6v2 registered that selector. Its first pilot used a pruned lookahead without the exact
search and matched greedy in every cell including the one where greedy was one over the
optimum, so the exact search was put in front of it before the second pilot and both pilots
are on record. On the run the selector equalled the exhaustive minimum in all 50 checkable
cells, needed strictly fewer sensors than the energy ranking in 18 of 30 discriminating
cells and never more in any of 55, never more than D6's greedy and fewer in four, and its
placements left 16 percent more forecast time than the energy placement's pooled on the
growth worlds. The cell D6 lost to the energy ranking is closed. The verdict is
INDETERMINATE by two single cells again, and both are definitions. In the same Lorenz-96
cell where greedy had reached the cap, the exact search ran to completion over every subset
size up to 12 and found no placement of 12 or fewer sensors reaching 10 identifiable
directions, while all 20 sensors do. The count is unreachable under the cap, and the
registration's feasibility test, which asks only whether the full sensor set reaches the
count, does not see the cap. In one unseen cell the selector's horizon was 10.3 percent
shorter than the energy placement's against a tolerance of 10.0, because the smallest set is
not unique and the first one in index order reaches exactly the required count where greedy's
tie-break on the m-th eigenvalue picks a pair reaching six. The spectrum places sensors. The
two open items are a feasibility test that includes the cap and a tie-break for the exact
search, and neither is a claim.

## 4. D7 and D7v2: what closes a filtered flow

D7 asked whether the leading eigen-directions of the read operator of a filtered flow's
resolved tendency, probed blind on the solver, carry what a closure needs. They do not. The
eigen-direction closure was behind the energy closure in 87 of 96 rank cells by a median of
15 percent, and the record says why: the eigen-directions rank subfilter modes by the
resolved dynamics' response alone, and the flow's energy is elsewhere. D7's second arm,
registered beside the declared one before the probe, ranked modes by read distortion,
response times energy, and beat the energy closure pooled at every rank, by 0.4 and 0.7
percent at ranks 16 and 32 and by 1.4 and 6.1 percent at ranks 64 and 128, the margin
growing with rank and cutoff and growing with resolution.

D7v2 took the second arm as the claim inside a declared rank scope of 64 and above, with the
scope's separation as a bar: the advantage below the scope must be smaller than inside it.
On the run the read-distortion closure was ahead of the energy closure by 2.1 percent at
rank 64 and 8.1 percent at rank 128 against a margin of 2, behind in 9 of 48 in-scope cells
by at most 14.1 percent against 15, and ahead by nothing at ranks 16 and 32, so the scope is
the regime where the closure has a choice among modes of comparable energy and sensitivity
can decide. The verdict is INDETERMINATE by the convergence bar. The in-scope margin was 6.5
percent at n = 96 and 3.7 percent at n = 128, a change of 2.7 against an allowed 2.0, and it
fell with resolution on this draw where it had risen on D7's. The margin is real and its
size, at this ladder, is not a number.

## 5. D1 and D1v2: a tolerance that carries a margin

D1 held every bar in every cell but one, where the above-threshold recovery error of
mixed probes in the positive definite world at B = 1 was 0.303 of chance against a
tolerance of 0.30 that D1 had fixed as its own pilot's maximum in that cell, 0.299, rounded
up. D1's record named the lesson for the whole track: a tolerance fixed at a pilot's own
maximum is a bar with no margin, and later gates fixed theirs as declared multiples. D1v2
is D1 unchanged with that rule, one and a half times the pilot's largest graded ratio. Its
pilot gave 0.255 in the same cell and quantity, so the tolerance is 0.39. On the run every
bar held in every cell: single-direction verdicts and brackets exact in all fifteen cells,
recovery in all six well-crossed cells at 0.045 to 0.212 of chance for the operator, 0.049
to 0.303 for the above-threshold eigenvalues and 0.022 to 0.146 for the below-threshold
ones, the oracle constant where the theory says it must be, and the estimate nearer the
pencil's end than the truth in both positive definite cells. D1v2 is a PASS. The cell that
decided D1 returned 0.303 of chance again on the second fresh seed, 0.003 over D1's bar and
0.087 under this one, so that number is a property of the analytic-centre estimator at 960
queries and not a fluctuation, and D1's miss was its tolerance rule's.

## 6. Third registrations: the definitions the second ones named

Each second registration's record named one more revision and said whether it was a claim or a
definition. Three were registered the same day, under the same rule.

D5v3 kept D5v2's claim, scope, collapse bars and control and measured convergence on the
normalised read fraction at budgets 8 and above, the quantity the collapse uses at the budgets
the coarser grid resolves. That bar held on every initial condition, 0.014 to 0.062 against 0.10,
and the collapse held at 0.41 and 0.34 of the null, the tightest of the three registrations. The
verdict is INDETERMINATE by the control bar, and the grader's own numbers say why. Taken one
control at a time, each control's scaled and unscaled scatters coincide exactly, because a
control's front wavenumber barely moves and the scaling is then a constant shift of its points.
Pooled, the two controls' different front wavenumbers put their points in different bins, and
since their read fractions differ, the separation between the controls reads as a collapse, 0.57
against a bar of 0.70. D5v2's controls had escaped this because their trajectories were alike.
The bar as declared pools the controls; the quantity the claim needs is the within-control
comparison, which is exactly one on both. That is a definition, and it is on record as one.

D7v3 kept D7v2's claim, scope and bars and moved the ladder one step finer, n = 128 against 192.
It passed. The read-distortion closure was ahead of the energy closure by 2.8 percent at rank 64
and 10.0 percent at rank 128, behind in 6 of 48 cells by at most 3.6 percent, ahead by nothing
below the scope, and the in-scope margin was 6.3 percent at n = 128 and 6.6 percent at n = 192.
D7v2's fall from n = 96 to 128 was the coarse end of the ladder; the margin has settled. The read
operator's effective rank is the same at both resolutions, about 130 at the coarse cutoff and
360 at the fine one, so what the closure reads is the same operator and what grows with n is the
subfilter space it is read against. Across the three registrations the declared arm of D7, the
operator's leading eigen-directions, is refuted each time, and the theory's own quantity, the
read distortion, is what ranks, inside a scope that is itself a bar.

D6v3 kept D6v2's claim and selector and added the two definitions: feasibility decided at the cap
by the exact search, and ties among smallest sets broken by the m-th eigenvalue. Its pilot found
every cell reachable at the cap, the selector exact everywhere, strictly fewer sensors than the
energy ranking in 7 of 14 discriminating cells and never more, and the horizon 28 percent longer
than the energy placement's pooled. Its run passed. On five worlds with fresh seeds the exact
search proved one count unreachable under the cap, which was recorded and not graded, as the
registration defines; in the 54 feasible cells the selector was exact in all 50 that could be
checked, needed strictly fewer sensors than the energy ranking in 10 of 28 discriminating cells and
never more, never more than D6's greedy and fewer in six, and its placements left 12 percent more
forecast time than the energy placement's pooled on the growth worlds and were never materially
shorter. The cell that had decided D6v2's horizon miss is no longer short once the tie-break
picks, among equally small sets, the one with the most margin on the eigenvalue that has to
clear the threshold. Three registrations: D6's misses were greedy's, D6v2's were definitions,
D6v3 has none.

## 7. What the registrations say together

The declared order's INDETERMINATE verdicts were of three kinds, and the second
registrations separate them. Where the miss was the instrument's, as in D6, removing the
slack moved the record and closed the cell that had been lost, and what remains is a
definition. Where the miss was a clause the registration itself had predicted to fail, as
in D5, dropping it and replacing the control with the one the claim needs turned a
signature into a property of the forming front. Where the miss was the declared arm, as in
D7, the second arm holds inside a scope that is itself a bar, and what is left is the size
of a margin. Where the miss was a tolerance rule with no margin, as in D1, the same claim
on the same instrument with the rule the track adopted afterwards passed, and the number
that had decided the first verdict came back unchanged. In none of the first three did a
second registration produce a PASS, and each produced a boundary that a first registration
could not have named. That is what the discipline is for.
