# PREREG D6: sensor placement as the choice of an observer under a budget

Status: SEALED 2026-09-10 by the rename to `PREREG-D6.md`; blob hash recorded in
`experiments/DISCOVERY-TRACK.md` and the README status ledger. Gate D6 of the OD
track (`experiments/DISCOVERY-TRACK.md`), taken after D3v2 and the D2 line, and before D5 and D7 in
the track's declared order (D4 is deferred, its world not being in the committed logs).

## 1. Claim under test

The track's gate reads: for a linear system with candidate sensors, the observer that minimises the
number of sensors subject to d_obs(B, rho) reaching a required count is found by a greedy selection
on the read operator's spectrum, and the observational predictability horizon of the chosen observer
exceeds that of an energy-based or random placement at the same sensor count. This registration
fixes every term of that sentence.

The system is x' = A x with n states and n candidate sensors c_i (rows). A placement S is the observer
C_S, and its read operator is the exact window Gramian over [0, T],

    W_S(T) = int_0^T e^{A^T t} C_S^T C_S e^{A t} dt,

computed by the Van Loan block exponential and checked against quadrature in the self-test. By
Theorem 2 of the identifiability article (gate D0, `GET/Identifiability.lean`), a perturbation of
size rho along v is distinguishable at budget B exactly when v^T W_S v > B^2 / rho^2, so the number
of identifiable initial-state directions is d_obs(B, rho) = #{i : lambda_i(W_S) > B^2 / rho^2},
antitone in B (bar E1). The required count is m; the task is the fewest sensors with d_obs at least
m.

The registered selector is greedy on the spectrum: starting from the empty placement, add the
candidate that maximises d_obs of the enlarged placement, ties broken by the m-th eigenvalue of the
enlarged Gramian (the eigenvalue that has to clear the threshold) and then by index, until d_obs
reaches m or the cap of 12 sensors. Two baselines are compared at the same sensor count and by the
count they need: the energy placement ranks candidates by the energy of their readings under white
forcing, c_i^T Q c_i with Q the window controllability Gramian, and takes the top k; random
placements are seeded k-subsets (200 per cell) and seeded orderings (60 per cell). Where the number
of subsets permits (at most 200,000), an exhaustive search over subsets of size up to the greedy
count gives the true minimal count k*, and the greedy count over k* is the greedy factor.

The horizon. D3's horizon rewards an observer that reads less, which is the wrong direction for
placement, so this gate uses the forecast horizon of the state given the observer's data: the
unidentified subspace of a placement at budget B is spanned by the eigenvectors of W_S with
eigenvalue at most B^2 / rho^2; an initial error of size rho uniform on the unit sphere of that
subspace is propagated by e^{A t}; the horizon is the mean first time its Euclidean size reaches
ten rho, censored at t = 20 (100 draws for the greedy and energy placements, 40 for each of 20
random placements). A placement that identifies the growing directions leaves the error in the
slow ones and has the longer horizon. The horizon is defined on worlds whose leading real
eigenvalue exceeds 0.05; on the stable chain and the neutral shallow-water grid it is not a bar.

(P) Greedy reaches m in every feasible cell. (G) Greedy is within a factor of the exhaustive
optimum. (C) Greedy never needs more sensors than the energy ranking or a random ordering, and
needs strictly fewer than the energy ranking in a registered fraction of the cells where
placement matters. (H) On growth worlds, greedy's horizon is never materially shorter than the
energy placement's at the same count, and is longer by a registered margin pooled over the cells
where placement matters.

## 2. World

Four families. A diffusion chain with Dirichlet ends (stable). The Lorenz-96 Jacobian at its fixed
point x_i = F, A = -I + F (S_{+1} - S_{-2}) (unstable; the growth world). A linearised
one-dimensional shallow-water grid, h_t = -H u_x, u_t = -g h_x on m periodic cells (neutral). On the
run only, a periodic advection-diffusion chain (an unseen family) and Lorenz-96 at F = 10 and n = 24
(an unseen size and forcing). Candidate sensors on the chains and Lorenz-96 read a seeded weighted
average of two adjacent coordinates, weight uniform in [0.5, 1]; on the shallow-water grid each
sensor reads h or u at one cell. Window T = 0.5, rho = 1, sensor cap 12. Thresholds
c = frac x lambda_max(W_all) with frac in {0.001, 0.01, 0.1}, so B = sqrt(c); required counts m in
{4, 6, 8, 10}; twelve cells per world, of which a cell is feasible when the all-sensor placement
reaches m. Pilot worlds: the three families at n = 16, 16 and 20 with their own sensor draw
(seed 20261023). Run worlds: n = 20, 20 and 24 with fresh draws (seed 20261024) and the two unseen
worlds. Probe seed 20261022.

## 3. Estimators

`d6_placement.py`. The Gramian by Van Loan; d_obs by eigenvalues; the greedy, energy and random
selectors; exhaustive search; the horizon by the matrix exponential on a 0.01 grid. Self-test:
Van Loan against quadrature to 4e-6; d_obs antitone in the budget; full observation of an
observable chain counts n; greedy reaches m and the exhaustive minimum is at most the greedy count;
the horizon of a stable subspace is censored and of a unit-rate unstable direction is log 10; the
three families' leading eigenvalues have the declared signs.

## 4. Errors and nulls

The quantities are exact given the seeds; the randomness is in the sensor draw and the random
placements. The tolerances are multiples fixed from the pilot by the rules of Section 5.

## 5. Bars (FACTOR = 1.5, PHI = 0.20, TOL_H = 0.05, MARGIN_H = 0.05 fixed from the pilot; `tolerances.json`; Section 7)

- E1, exact: for every world and count, the all-sensor d_obs is antitone in the budget.
- P1: the greedy placement reaches m in every feasible cell.
- G1: in every cell where exhaustive search is feasible, the greedy factor is at most FACTOR
  (1.25 times the pilot's largest factor, rounded up to one decimal, at least 1.0).
- C1: in no feasible cell does the energy ranking reach m with fewer sensors than greedy; and in at
  least PHI of the discriminating cells (those where the median random ordering needs more sensors
  than greedy) greedy needs strictly fewer than the energy ranking (PHI = half the pilot's fraction,
  rounded down to 0.05).
- C2: in no feasible cell does the median random ordering reach m with fewer sensors than greedy.
- H1, growth worlds: in no cell is greedy's horizon shorter than (1 - TOL_H) times the energy
  placement's at the same count (TOL_H = 1.25 times the pilot's largest relative shortfall, rounded
  up to 0.05); and pooled over the discriminating growth cells greedy's mean horizon exceeds the
  energy placement's by at least MARGIN_H (half the pilot's pooled advantage, rounded down to 0.05).

Pass: E1, P1, G1, C1, C2, H1. Fail: a greedy factor above 2 anywhere; the energy ranking needing
fewer sensors than greedy in more than a tenth of the feasible cells; the pooled horizon advantage
negative. Otherwise INDETERMINATE.

## 6. What falsifies

The claim is that the Gramian's spectrum is the right thing to place sensors by, under a budget. A
baseline that matches d_obs and horizon at the same count, cell for cell, refutes it; an energy
ranking that needs fewer sensors refutes it outright. A greedy factor far from one says the
spectrum is the right quantity but greedy is the wrong search. A horizon no longer than the energy
placement's on the growth world says the count of identified directions does not by itself buy
forecast time. The unseen worlds say whether any of this depends on the three families the pilot
saw.

## 7. Self-test, probe, pilot (before sealing)

Self-test (Atlas 2026-09-10): PASS, seven checks.

Probe (`probe.json`, `probe.log`, seed 20261022, the three pilot worlds at their pilot sizes). Every
quantity exists. The first probe, at T = 1 and thresholds down to 1e-4, found the world too
observable to discriminate (greedy equal to the exhaustive optimum and to the energy ranking in
nearly every cell); the window, thresholds and counts of Section 2 were set after it and before the
pilot, by declaration, to the regime where placement matters, and the two per-cell counts (sensors
the energy ranking needs, sensors a random ordering needs) were added so that regime is visible.
At the declared settings 31 of 36 cells are feasible (Lorenz-96 loses five at the higher thresholds,
its all-sensor Gramian identifying at most 6 directions at frac 0.01 and 4 at 0.1). Placement
matters in eleven cells: on the diffusion chain at frac 0.01 greedy needs 3, 5 and 7 sensors where
the energy ranking needs 4, 7 and 8 and a random ordering 5, 7 and 9; on shallow water at frac 0.01
and m = 8 and 10 greedy needs 4 and 5 against 6 and 8; on Lorenz-96 greedy is one sensor ahead of
the energy ranking in two cells and three ahead of random in one. Greedy is not always optimal: one
sensor over the exhaustive minimum in two cells (factor 1.33). On Lorenz-96 the greedy horizon
exceeds the energy placement's in six of seven cells (0.65 against 0.57, 0.85 against 0.79, 0.62
against 0.55 in the cells that discriminate) and is shorter in one (0.93 against 1.05 at m = 10,
where both reach the count). The energy ranking never needs fewer sensors than greedy in the probe.

Pilot (`pilot.json`, `pilot.log`, `tolerances.json`, seed 20261023, the three families at n = 16, 16
and 20 with a fresh sensor draw, Atlas 2026-09-10). 31 of 36 cells feasible; placement matters in
15 (the median random ordering needs more sensors than greedy); greedy needs strictly fewer sensors
than the energy ranking in 6 of those 15 (0.40), overlapping the cells the probe found on its own
draw (the diffusion chain at frac 0.01 and m = 10, Lorenz-96 at frac 0.001 and m = 8, at frac 0.01 and
m = 6, and at frac 0.1 and m = 4, shallow water at frac 0.01 and m = 8 and m = 10, greedy at 3 to 8
sensors against the energy ranking's 4 to 9); the energy ranking needs fewer sensors than greedy in
no cell. Greedy equals the exhaustive minimum in 30 of 31 cells and is one sensor over it in one
(Lorenz-96 at frac 0.001 and m = 10, 6 against 5, a factor of 1.20), so FACTOR = 1.5 by the rule.
PHI = 0.20 by the rule from 0.40. On the seven growth cells the greedy horizon is shorter than the
energy placement's in two, by 2.7 and 0.7 percent, so TOL_H = 0.05; pooled over the six
discriminating growth cells greedy's horizon exceeds the energy placement's by 11.9 percent and the
random placements' by 12.9 percent, so MARGIN_H = 0.05 by the rule. The tolerances are fixed from
these numbers and the pilot's own cells hold every bar under them, as the rules make them.

## 8. Sealing procedure

1. Self-test, probe and pilot on Atlas; fix the tolerances; record them in Sections 5 and 7;
   commit `probe.json`, `pilot.json`, `tolerances.json`. Done.
2. Rename this file to `PREREG-D6.md`, commit, record its blob hash in the track document and
   the README status ledger. Done by this commit.
3. Run on the run seed, grade with `d6_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry tests in
   `claims/transformations/OD.toml`.
