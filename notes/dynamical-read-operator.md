# The dynamical read operator of a spectral observer of the Navier–Stokes equations

Draft 0.1, 2026-10-09. Not claim-bearing. Step 1 of the plan that follows the OD track's D7v3
PASS. The statements below are for the Galerkin system at a fixed truncation, so every object is
finite-dimensional and the representation theorem of `geometric-observation/paper/observer-representation.tex`
applies as written. What is classical is labelled classical. What is new is small and named in
Section 7. Proofs are written out so that the Lean pass (Section 8) can follow them line by line.

## 1. Setting

Periodic box $\mathbb{T}^d = [0, 2\pi)^d$, $d \in \{2, 3\}$. Fields are written
$f(x) = \sum_k \hat f_k e^{i k \cdot x}$ with $\|f\|^2 = \int |f|^2 dx = (2\pi)^d \sum_k |\hat f_k|^2$.
$H_M$ is the space of real, mean-zero, divergence-free vector fields whose Fourier support lies in
$\{k \neq 0 : |k|_\infty \le M\}$. The Galerkin Navier–Stokes system on $H_M$ is

$$u_t = F(u) = -\nu A u - \Pi_M B(u, u) + f,$$

with $A = -\Delta$, $B(u, v) = \Pi_L[(u \cdot \nabla) v]$, $\Pi_L$ the Leray projection, $\Pi_M$ the
Fourier truncation and $f$ a forcing supported on modes with $|k| \le N$ (zero for the unforced
problem). The observer is the spectral cutoff $C = P_N$, the orthogonal projection onto the modes
$|k| \le N$ (Euclidean norm), with $N < M$, and $Q_N = I - P_N$. Write $p = P_N u$ and $q = Q_N u$.
For a Fourier shell write $\Pi_{(a, b]}$ for the projection onto $a < |k| \le b$.

Two facts are used throughout. Antisymmetry: for $u$ divergence-free,
$(B(u, v), w) = -(B(u, w), v)$, so $(B(u, v), v) = 0$. Triad support: the Fourier coefficient of
$B(u, v)$ at $k$ is a sum over pairs $j + l = k$ of terms linear in $\hat u_j$ and $\hat v_l$.

## 2. The closure condition and its failure (classical)

Since $C$ is linear, $DC(u) F(u) = P_N F(u)$, and the observation obeys an autonomous law
$y_t = g(y)$ exactly when $P_N F(p + q)$ does not depend on $q$. The viscous term and the forcing
commute with $P_N$, so

$$r_N(p, q) := P_N F(p + q) - P_N F(p) = L_p q + R(q), \qquad L_p q = -P_N[B(p, q) + B(q, p)], \qquad R(q) = -P_N B(q, q).$$

$r_N$ is the diagnostic proposed in the planning thread, and it is the subgrid contribution D7
measured, $T(\bar w + w') - T(\bar w)$ at `experiments/OD/D7v3/d7_closure.py:8`, in vorticity form.
$L_p$ is the linear read of the discarded state and $R$ the part of the feedback that no linear
read sees.

**Proposition 1 (no spectral observer closes).** For $d = 2$ (and so for $d = 3$, by planar
flows) and every $N \ge 1$, $M \ge N + 1$, the map $q \mapsto R(q)$ is not identically zero on
$Q_N H_M$. Hence no spectral cutoff observer of the Galerkin system obeys an exact closed law.

*Proof.* In two dimensions write the flow by its stream function. For
$\psi = a\cos(j \cdot x) + b \cos(l \cdot x)$ the vorticity tendency $-J(\psi, \omega)$,
$\omega = -\Delta\psi$, has a component at $j + l$ proportional to
$ab\,(j \times l)(|j|^2 - |l|^2)$. Take $j = (N + 1, 1)$, $l = (-N, -1)$. Then
$j + l = (1, 0)$ lies in the observed ball, $|j|^2 = (N+1)^2 + 1 > N^2$ and $|l|^2 = N^2 + 1 > N^2$
so both lie in the discarded space, both have $|\cdot|_\infty \le N + 1 \le M$,
$j \times l = -1$ and $|j|^2 - |l|^2 = 2N + 1$. The coefficient is nonzero. $\square$

This is the closure problem of turbulence modelling. It is stated only to fix the object.

## 3. Octave locality of the linear read

**Proposition 2.** $L_p q = L_p\,\Pi_{(N, 2N]}\,q$. Consequently the linear read operator
$P^{\rm lin}_p = L_p^* L_p$ annihilates every discarded mode with $|k| > 2N$, its rank is at most
the dimension of $\Pi_{(N, 2N]} H_M$, and for $M \ge 2N$ (in the $\infty$-norm sense that contains
the Euclidean $2N$ ball) its nonzero spectrum does not depend on $M$.

*Proof.* A term of $L_p q$ at an output mode $k$, $|k| \le N$, pairs $\hat p_j$, $|j| \le N$, with
$\hat q_l$, $l = k - j$. Then $|l| \le |k| + |j| \le 2N$. Discarded modes with $|l| > 2N$ appear in
no such term. Once $H_M$ contains every mode with $|l| \le 2N$, raising $M$ adds only modes in the
kernel. $\square$

The linear part of the feedback from the discarded scales comes from the first octave and from
nowhere else, at every resolution. All coupling to scales finer than $2N$ goes through $R$, which is
quadratic in the discarded state.

Relation to D7 (a consistency check, not an implication). D7v3 recorded that the effective rank of
its probed operator was 130 at $k_c = 8$ and 360 at $k_c = 16$ at both $n = 128$ and $n = 192$. D7's
probe differentiates the full tendency at the true discarded state, $J = L_p + DR(q)$, not $L_p$
at $q = 0$, so Proposition 2 does not imply that observation. It predicts it for the leading part
whenever $\|q\|$ is small against $\|p\|$, which is the case at $k_c = 16$ in D7's fields, where the
full-rank remainder was 0.001 to 0.002.

## 4. A resolution-uniform bound on the feedback

Let $K_N = \#\{k \in \mathbb{Z}^d : 0 < |k| \le N\}$ and $c_N = N\sqrt{K_N}\,(2\pi)^{-d/2}$, so
$c_N \sim \pi^{1/2} N^2 / (2\pi)$ in two dimensions and $c_N \sim (4\pi/3)^{1/2} N^{5/2} / (2\pi)^{3/2}$ in three.

**Proposition 3.** For every $M > N$, every $p \in P_N H_M$ and $q \in Q_N H_M$,

$$\|L_p q\| \le 2 c_N \|p\|\,\|\Pi_{(N, 2N]} q\|, \qquad \|R(q)\| \le c_N \|q\|^2, \qquad \|r_N(p, q)\| \le c_N\bigl(2\|p\|\,\|\Pi_{(N,2N]}q\| + \|q\|^2\bigr).$$

*Proof.* For $w \in P_N H_M$, $|\nabla w(x)|_{\rm op} \le \sum_{|k| \le N} |k|\,|\hat w_k| \le N \sqrt{K_N}\,(\sum |\hat w_k|^2)^{1/2} = c_N \|w\|$.
By antisymmetry $(B(q, q), w) = -(B(q, w), q)$, and $|(B(q, w), q)| \le \|\nabla w\|_\infty \|q\|^2$.
Taking the supremum over $\|w\| = 1$ gives the bound on $R$. For $L_p$, $(B(p, q), w) = -(B(p, w), q)$
and $(B(q, p), w) = -(B(q, w), p)$, each bounded by $\|\nabla w\|_\infty \|p\|\,\|q\|$, and
Proposition 2 replaces $q$ by $\Pi_{(N, 2N]} q$. $\square$

By the energy inequality, unforced Galerkin solutions satisfy $\|u(t)\| \le \|u(0)\|$ for all $t$
and $M$, so $\|r_N(t)\| \le 3 c_N \|u(0)\|^2$, uniformly in time and in resolution, in two and three
dimensions alike. This is the classical fact that the low-mode projection of the nonlinearity is
bounded on the energy space, which is why the low modes of a Leray solution are smooth in time. It
answers the planning thread's step 2 ("bounds that remain useful as spatial resolution increases")
for a fixed observer, and it shows why that step is not where the difficulty lies. The bound is
uniform in $M$ and grows like $N^{1 + d/2}$ in the budget. Regularity is a statement about every
budget at once, and a bound that grows with $N$ says nothing about the flux into arbitrarily fine
scales.

## 5. Which discarded directions to keep: the read distortion is the optimal ranking

The question D7 posed is which $r$ discarded modes a closure should keep. Keeping a set $S$ of
discarded modes exactly leaves the error $r_N(p, q) - r_N(p, q_S) = L_p q_{S^c} + R(q) - R(q_S)$.

**Proposition 4.** Let $q$ be random with a law symmetric under $q \mapsto -q$ and with diagonal
covariance in the Fourier basis (independent phases), $\sigma_k^2 = \mathbb{E}|\hat q_k|^2$. Let
$s_k = \|L_p e_k\|^2$ be the sensitivity of the observed tendency to mode $k$, averaged over its two
real directions. Then

$$\mathbb{E}\,\|r_N(p, q) - r_N(p, q_S)\|^2 = \sum_{k \notin S} \sigma_k^2 s_k + \mathbb{E}\|R(q) - R(q_S)\|^2,$$

and among all sets $S$ of $r$ discarded modes the linear term is smallest for the $r$ modes of
largest read distortion $\sigma_k^2 s_k$.

*Proof.* The cross term $\mathbb{E}\langle L_p q_{S^c}, R(q) - R(q_S)\rangle$ is odd in $q$ and
vanishes under the symmetric law. With diagonal covariance,
$\mathbb{E}\|L_p q_{S^c}\|^2 = \operatorname{tr}(L_p \Sigma_{S^c} L_p^*) = \sum_{k \notin S}\sigma_k^2 s_k$.
For fixed $|S| = r$ the sum over the complement is smallest exactly when $S$ holds the $r$ largest
terms $\sigma_k^2 s_k$. $\square$

Three corollaries are the three D7 arms. The energy ranking is optimal for the linear term only
when $s_k$ is constant over the candidates. The eigen-direction closure, the leading eigenvectors of
$L_p^* L_p$, is optimal among all rank-$r$ projections when $\Sigma$ is a multiple of the identity,
and turbulent spectra are far from that, which accounts for D7's refuted declared arm (behind energy
in 87 of 96, 43 of 48 and 40 of 48 cells). The read-distortion ranking is optimal for the linear term
among coordinate selections under random phases, which is the ranking D7v3 passed with (ahead of
energy by 2.8 percent at rank 64 and 10.0 at rank 128). Proposition 2 adds that the linear term
only ever selects among first-octave modes, so the ranking's advantage must come from the shell
$(N, 2N]$ and from $R$.

Status of this account. It was written after the D7 data, so it is a retrodiction. D7's error is a
single-snapshot ratio, not an expectation, and real snapshots have correlated phases. D8 is the
out-of-sample test, in a dynamical problem the proposition does not cover.

## 6. Dynamics: when discarded directions stay harmless (classical criterion, new question)

Let $S$ be any set of $m$ observed Fourier modes and nudge a second solution toward the observed
modes of the first (Azouani, Olson and Titi 2014),

$$v_t = F(v) - \mu P_S (v - u).$$

The error $e = v - u$ obeys $e_t = (DF(u) - \mu P_S)e + O(\|e\|^2)$. At a finite gain $\mu$ the
local synchronization diagnostic is the top Lyapunov exponent of this full time-dependent linear
system along the trajectory. It is the exponent of the observer that is actually run, coupling
between observed and discarded error included. As $\mu \to \infty$ the observed error is slaved to
zero and the discarded error follows $Q_S\,DF(u(t))\,Q_S$, and the criterion becomes the
conditional Lyapunov exponent of synchronization (Pecora and Carroll 1990), with discarded
directions harmless when that block's exponent is negative. The block exponent misses the
finite-gain coupling, so D8 records it only as the limit, beside the full observer's exponent
(revised 2026-10-09 after an outside review). For the ball observer the
asymptotic statement is the determining-modes theorem of Foias and Prodi (1967), with rigorous
counts in terms of the Grashof number (Jones and Titi 1993). In two dimensions all of this is known,
and the known sufficient counts are far above what simulations need.

What is not known, and what an observer theory can contribute, is which $m$ modes to observe. At
$t = 0$ with $v(0) = 0$ the discarded error is $-q_{S^c}$, and under the independent-phase model of
Proposition 4 its nonlinear spreading rate is
$\mathbb{E}\|N_u e_{S^c}\|^2 = \sum_{k \notin S}\sigma_k^2 \|N_u e_k\|^2$, with
$N_u e = -[B(u, e) + B(e, u)]$ the nonlinear Jacobian. Observing the modes of largest dynamical read
distortion $\sigma_k^2 \|N_u e_k\|^2$ minimizes it. This is exact at $t = 0$ only. Whether the same
ranking lowers the number of observed modes at which the two flows synchronize is an empirical
question, and it is gate D8 (`experiments/OD/D8/PREREG-D8-DRAFT.md`).

## 7. What is new, what is classical, and what this cannot do

Classical: Proposition 1 (the closure problem), the bound of Proposition 3 (low-mode boundedness),
the criterion of Section 6 (conditional Lyapunov exponents, determining modes, nudging).
Elementary but stated here for the first time in this program, as far as I know: Proposition 2 as a
statement about the rank and resolution-independence of the read operator of a spectral observer,
and Proposition 4 as the reason the read distortion, and neither energy nor the operator's
eigen-directions, is the ranking for the linear feedback. I have not searched the closure and
data-assimilation literature for prior statements of Proposition 4. That search comes before any
claim of novelty.

What it cannot do. The statements use three properties of the nonlinearity: the antisymmetry
$(B(u, v), v) = 0$, the triad support in Fourier space, and the resulting energy inequality. Tao
(2016, J. Amer. Math. Soc. 29, 601–674) constructs an averaged Navier–Stokes operator $\tilde B$ on
$\mathbb{R}^3$ that keeps the cancellation $\langle \tilde B(u, u), u\rangle = 0$, and so the energy
identity, and whose solutions blow up in finite time. Its definition (arXiv:1402.0290v3, eq. 1.12)
is
$\langle \tilde B(u, v), w\rangle = \mathbb{E}\,\langle B(m_1(D)\mathrm{Rot}_{R_1}\mathrm{Dil}_{\lambda_1}u,\ m_2(D)\mathrm{Rot}_{R_2}\mathrm{Dil}_{\lambda_2}v),\ m_3(D)\mathrm{Rot}_{R_3}\mathrm{Dil}_{\lambda_3}w\rangle$.
Here $m_i(D)$ are random real Fourier multipliers of order 0, $R_i$ are random rotations, and
$\lambda_i$ are random dilations, independent for the two inputs and the output, with
$C^{-1} \le \lambda_i \le C$ almost surely. Tao notes that every Sobolev estimate on $B$ implies
one on $\tilde B$ with a larger constant (his remark after eq. 1.13 and eq. 1.14).

Checked against the paper on 2026-10-09. Draft 0.1 had guessed here that $\tilde B$ keeps
Proposition 2's triad localisation exactly. It does not. Rotating and dilating the two inputs
independently breaks the exact relation $k = j + l$. A weaker locality survives. Under (1.12) a
discarded mode $l$ reaches an observed output $|k| \le N$ from an observed input $|j| \le N$ only
if $|l| \le 2C^2 N$. (This is my derivation from the definition. Tao does not state it.) The exact
cutoff $2N$ becomes $2C^2N$. Proposition 3's argument goes through with constants that depend on
$C$ and on the multipliers' seminorms, because it uses only the cancellation and a Bernstein bound
on band-limited test functions, and both survive. Propositions 2 to 4 therefore hold for $\tilde B$
in this weakened form, with bounded-factor locality in place of the exact octave and larger
constants, and $\tilde B$'s solutions blow up. Tao's construction is on $\mathbb{R}^3$ and this
note is on the torus, so the transfer is by analogy and not a theorem.

The conclusion stands. No argument assembled only from statements of this kind can give the
planning thread's step 3, a bound on $\int_0^T\!\!\int |u|^5\,dx\,dt$. Tao's own abstract
says the same, that a positive resolution must use finer structure of $B(u, u)$ than the energy
identity and the harmonic-analysis estimates provide. The test that follows is concrete. Any
dynamical bound the program proposes is run on a dyadic model known to blow up (Katz and Pavlović
2005; Cheskidov 2008, Trans. Amer. Math. Soc.), and it must fail there. That gate is D9, not drafted.

The classical criterion closest to "the discarded directions are harmless above a budget" is the
dissipation wavenumber $\Lambda(t)$ of Cheskidov and Shvydkoy (2014, J. Math. Fluid Mech. 16). They
define $\Lambda(t) = 2^{Q(t)}$, with $Q(t)$ the first dyadic shell beyond which every
Littlewood–Paley piece satisfies $2^{-p}\|u_p(t)\|_\infty < c_0\nu$. Viscosity dominates the
nonlinear term above that shell. A Leray–Hopf solution is regular on $(0, T]$ if
$\Lambda \in L^{5/2}(0, T)$. Their earlier condition was $\Lambda \in L^\infty$. Every Leray–Hopf
solution satisfies $\Lambda \in L^1(0, T)$. They also show their vorticity condition is weaker
than every Ladyzhenskaya–Prodi–Serrin condition. (Checked 2026-10-09 against the abstract and
Section 1 of arXiv:1102.1944v2. Draft 0.1 left the exponents unstated, and the journal version
has not been compared line by line.) The open gap is integrability $L^1$ against $L^{5/2}$ for a
budget above which the discarded scales are dynamically harmless, which is the scaling gap in
another form. A dynamical observer theory would earn its place on the regularity question only by
closing part of that gap. Nothing here does.

## 8. Machine checking

Proposition 2 is a statement about finite sums over a lattice and is the first Lean target
(`proofs/`, Mathlib). Proposition 4 is linear algebra over a finite index set and is the second.
Proposition 3 needs the antisymmetry identity for the truncated operator and a finite
Cauchy–Schwarz, both within reach. Proposition 1 is a single explicit coefficient and can be
checked by `decide`-style computation for small $N$ and by hand in general. Section 6 is not a
theorem here and is not a Lean target.

D8's instrument checks Propositions 2 and 3 numerically on the solver before anything is claimed
(bars T1 and T2 of the draft).

## References

Checked on 2026-10-09 against the Crossref API (title, authors, journal, volume, pages). Eight
records matched with a DOI. The three not in Crossref were then checked the same day against
MathSciNet through the AMS's free MR Lookup, and all three match as cited. Both sources confirm only
the bibliographic record. The two content claims of Section 7 were checked the same day against
the arXiv texts, Tao arXiv:1402.0290v3 eq. 1.12 and Cheskidov and Shvydkoy arXiv:1102.1944v2
Section 1. One draft guess was corrected (Tao's operator does not keep Proposition 2's exact
octave), and the exponents ($L^{5/2}$ sufficient, $L^1$ for every Leray–Hopf solution) were
filled in.

- C. Foias and G. Prodi (1967), Sur le comportement global des solutions non-stationnaires des
  équations de Navier-Stokes en dimension 2, Rend. Sem. Mat. Univ. Padova 39, 1–34, MR0223716
  (not in Crossref; confirmed on MathSciNet).
- D. A. Jones and E. S. Titi (1993), Upper bounds on the number of determining modes, nodes, and
  volume elements for the Navier-Stokes equations, Indiana Univ. Math. J. 42 (3), 875–887,
  MR1254122, doi:10.1512/iumj.1993.42.42039 (the DOI resolves to the journal's page but is not in
  Crossref's index; confirmed on MathSciNet). (Crossref holds the same authors' 1992
  papers, Physica D 60, 165–174, doi:10.1016/0167-2789(92)90233-D, and J. Math. Anal. Appl. 168,
  72–88, doi:10.1016/0022-247X(92)90190-O.)
- L. M. Pecora and T. L. Carroll (1990), Synchronization in chaotic systems, Phys. Rev. Lett. 64,
  821–824, doi:10.1103/PhysRevLett.64.821.
- A. Azouani, E. Olson and E. S. Titi (2014), Continuous data assimilation using general
  interpolant observables, J. Nonlinear Sci. 24, 277–304, doi:10.1007/s00332-013-9189-y (online
  2013).
- N. H. Katz and N. Pavlović (2005), Finite time blow-up for a dyadic model of the Euler equations,
  Trans. Amer. Math. Soc. 357, 695–708, doi:10.1090/S0002-9947-04-03532-9 (online 2004).
- A. Cheskidov (2008), Blow-up in finite time for the dyadic model of the Navier-Stokes equations,
  Trans. Amer. Math. Soc. 360, 5101–5120, doi:10.1090/S0002-9947-08-04494-2. (Corrected
  2026-10-09. Draft 0.1 gave "Adv. Math. 218, 1–45", which was wrong.)
- A. Cheskidov and R. Shvydkoy (2014), A unified approach to regularity problems for the 3D
  Navier-Stokes and Euler equations: the use of Kolmogorov's dissipation range, J. Math. Fluid
  Mech. 16, 263–273, doi:10.1007/s00021-014-0167-4.
- T. Tao (2016), Finite time blowup for an averaged three-dimensional Navier-Stokes equation,
  J. Amer. Math. Soc. 29, 601–674, doi:10.1090/jams/838 (online 2015).
- G. Prodi (1959), Un teorema di unicità per le equazioni di Navier-Stokes, Ann. Mat. Pura Appl.
  48, 173–182, doi:10.1007/BF02410664.
- J. Serrin (1962), On the interior regularity of weak solutions of the Navier-Stokes equations,
  Arch. Rational Mech. Anal. 9, 187–195, doi:10.1007/BF00253344.
- O. A. Ladyzhenskaya (1967), Uniqueness and smoothness of generalized solutions of Navier-Stokes
  equations, Zap. Nauchn. Sem. LOMI 5, 169–185, MR0236541 (not in Crossref; confirmed on
  MathSciNet).

The last three are the sources of the $L^p_t L^q_x$ criterion, $2/p + 3/q = 1$, of which
$p = q = 5$ is the planning thread's case.
