# Open problems where Observation Theory might help, and where it cannot

Draft 0.1, 2026-10-11. Not claim-bearing. A literature survey written after the Navier–Stokes
work of `notes/dynamical-read-operator.md` and the OD gates D7 to D9. It asks one question of
each problem. Is the open question, or a sharp part of it, a question about what an observer must
or should read? Where it is, Observation Theory (OT) has an instrument to offer. Where it is not,
OT has nothing to add, however the problem is phrased.

How the sources were read. Searches were run on 2026-10-11. Most sources below were read at the
level of abstracts, search summaries and arXiv listing pages, not in full, and each entry says so
where it matters. Judgments marked "assessment" are this note's, not the sources'.

## 1. What OT has shown so far

OT's object is the read operator $P_C = J^T G J$ of an observer $O = (C, G, B)$, recovered blind as
$S = E[g g^T]$, together with the read distortion $\mathrm{tr}(P_C \Sigma_\delta)$. Its record on
dynamical and learned systems, in this repository and in `readscope`:

| Setting | Result | Status |
|---|---|---|
| Closure of a filtered 2-D flow (D7v3) | The read-distortion closure beats the energy closure inside the rank scope, pooled 2.8 percent at rank 64 and 10.0 percent at rank 128, converged between n = 128 and 192 | sealed, PASS |
| Theory note, Galerkin Navier–Stokes | Octave locality of the linear read, a resolution-uniform feedback bound, read distortion as the optimal ranking under random phases | proved, finite-dimensional |
| Barrier check of the theory note | Tao's averaged Navier–Stokes keeps every property the note uses and still blows up, so the note cannot reach regularity | recorded in Section 7 of the note |
| Nudging synchronization (D8 probe and pilot) | READ has not been ahead of the best simple control (BALL, ENSTROPHY or KE) on any probe world or any pilot cell graded so far | pilot incomplete, points to FAIL |
| Dyadic barrier gate (D9 probe) | C0 passes, C1 transparent, C3 passes but is classical; READ, ENSTROPHY and SENS unsettled | probe only |
| KV-cache heads of one 3B language model (GO-P-2026-021, `readscope`) | Blind read subspace overlap 0.647 against 0.126 chance; read distortion picked the worse quantizer arm 16 of 16 times | sealed, PASS, scope 16 cells |

Assessment. OT's positive results are about selection: which modes to keep, which directions a
consumer reads, which arm hurts the consumer. Its negative and barrier results are about proof:
the read structure it extracts is the structure that known obstructions already preserve. The
survey below sorts problems by that line.

## 2. Problems where OT does not help

### 2.1 Navier–Stokes regularity

Covered by the theory note. Every property the note proves is local up to twice the cutoff, and
Tao's averaged equation (J. AMS 29, 2016, eq. 1.12) keeps exactly that locality and blows up. A
proof of regularity therefore needs something the read operator does not see. D9 tests candidate
quantities against the dyadic analogue of this barrier.

### 2.2 P versus NP

No serious observer-based approach was found. Four papers combine observers with P versus NP.

| Paper | What it does | Assessment |
|---|---|---|
| Buono, arXiv:2606.27407 (June 2026) | Defines an observer as a map from input strings to a summary that limits what a machine sees, builds an observational hierarchy of language classes, and defines observer-parameterized classes $P_O$ and $NP_O$ | The nearest in spirit to OT. The listing reports only a collapse strictly inside P and no claim about the classical question. Full text not read. Any OT work on complexity should cite it |
| Edwards, arXiv:2512.11820 (v5, January 2026) | Claims P ≠ NP through observers of bounded "contextual entanglement width", 208 pages, claims immunity to all three barriers | Unreviewed. The author leaves community verification and formalization to future work. Not established |
| Nye, J. Modern Physics 16 (2025) 6–51, doi:10.4236/jmp.2025.161002 | Argues that gravitational time dilation makes the answer depend on the observer | The argument fails. A time-dilation factor does not depend on input length, so it cannot turn an exponential running time into a polynomial one |
| Ramezanian, arXiv:2609.10864 (September 2026) | Conditional, observer-relative unprovability of P = NP under axioms of shared history | An AI referee on Pith flags that the separation is for history-sensitive classes, not standard P and NP |

The legitimate work closest to OT's question is the theory of what must be read. Query-to-
communication lifting turns lower bounds on how many input bits must be read into communication
lower bounds and from there into circuit depth bounds. The line runs from Raz and McKenzie (1999)
through Göös, Pitassi and Watson to de Rezende, Meir, Nordström, Pitassi and Robere (FOCS 2020,
Comput. Complexity 33, 2024), who prove the monotone KRW conjecture for inner functions whose
depth is bounded by lifting. It separates monotone classes. For general circuits the open target
it serves is P ⊄ NC¹, not P versus NP.

Three barriers stand in front of a read-based argument.

- Relativization. Chen, Hu and Ren (arXiv:2511.14038, ITCS 2026) show that relativization
  barriers to circuit lower bounds amount to decision-tree lower bounds for the Missing-String
  problem. What an observer must read is the formal content of the oracle barrier, so an argument
  built only from reads sits inside it by default.
- Natural proofs (Razborov and Rudich, 1997) and algebrization (Aaronson and Wigderson, 2009).
  P versus NP needs techniques that are neither natural nor algebrizing.
- Locality. Chen, Hirahara, Oliveira, Pich, Rajgopal and Santhanam (ITCS 2020, arXiv:1911.08297)
  show that the problems used in hardness magnification have efficient circuits with small fan-in
  oracle gates, and that lower-bound techniques for weak models usually extend to such gates. This
  is the complexity-theoretic counterpart of Tao's averaged equation. Locality survives and the
  separation does not follow.

Assessment. An OT argument for P versus NP would hit relativization and locality first, as the
Navier–Stokes attempt hit Tao's construction. Meta-complexity (Ren and Santhanam, ECCC TR21-089)
and geometric complexity theory (Mulmuley, arXiv:0908.1936) are the active routes, and neither is
observer-based.

### 2.3 The remaining Millennium problems

Assessment, without a literature search. The Riemann hypothesis, the Hodge conjecture and the
Birch and Swinnerton-Dyer conjecture are questions in number theory and algebraic geometry with no
point at which an observer's read enters. The Yang–Mills existence and mass gap problem is first a
problem of constructing a four-dimensional quantum field theory rigorously, and OT has nothing to
say about the construction. The Poincaré conjecture is solved.

## 3. Problems where OT could help

Each entry gives the open question, its status in the sources, the OT test that would address it,
and an assessment of fit. They are ordered by fit to OT's record in Section 1.

### 3.1 Choosing observables for Koopman and EDMD approximations (best fit)

Open question. Extended dynamic mode decomposition approximates the Koopman operator on a
dictionary of observables, and its convergence guarantees depend on which dictionary is used. The
survey by Colbrook (arXiv:2312.00137) calls the selection of observables one of the most
significant open problems of the field and "more of an art than a science". The same survey lists
impossibility results, which no algorithm can beat, as an open direction. Recent work learns
dictionaries for approximate invariance (Johnson, Balakrishnan and Yeung 2022 on finite
approximate closure; a 2025 Grassmann-manifold optimization; a 2026 PageRank-based search).

OT test. This is D7's question in another basis. D7 ranked candidate modes by read distortion and
beat the energy ranking for a closure. The test is a preregistered comparison of a read-distortion
dictionary against POD and energy dictionaries on EDMD prediction error, on the flows D7 already
uses, with random dictionaries as the null.

Assessment. The strongest fit. It reuses D7's instrument and world, it targets a problem the field
names as open, and D7v3 is a sealed positive result in the nearest setting. The risk is the one D8
shows. A ranking that wins for a closure may not win for another task.

### 3.2 Closure models for large-eddy simulation and the Mori–Zwanzig memory term

Open question. Mori–Zwanzig gives an exact closure for resolved variables with a memory integral
that is costly to compute. Parish and Duraisamy (arXiv:1611.03311) build finite-memory closures and
record that the success of the simpler t-model "has remained a mystery and is an outstanding
question in the literature". Duraisamy notes that the formalism alone does not reduce cost, since
it requires the orthogonal dynamics.

OT test. Section 2 of the theory note derives the failure of closure for a spectral observer and
Proposition 3 bounds the feedback from the discarded modes. A test would ask whether the
read-distortion split of resolved and unresolved modes shortens the memory needed for a fixed
error, against the spectral split.

Assessment. Good fit. The theory note already contains the closure-failure algebra and D7 is a
closure gate. No search result reviews this area after 2020 in the material read, so the status
should be checked before any registration.

### 3.3 Sensor selection for nonlinear observability and data assimilation

Open question. Sensor selection is usually posed as maximizing an observability measure under a
cardinality or matroid constraint and solved greedily with submodular guarantees (Kazma et al.
2023, 2024). Greedy solutions are often suboptimal, and the empirical-Gramian formulation is a
mixed-integer nonlinear program (Serpas et al. 2013). Sensor placement for turbulent flow
reconstruction by data assimilation is active (Mons and Marquet, J. Fluid Mech. 2021).

OT test. D8 is this question for nudging on 2-D turbulence. Its pilot so far says READ does not
beat the best simple mode ranking.

Assessment. The question fits OT, but OT's own evidence here is negative so far. If D8 fails, that
failure is itself a result worth reporting beside Inubushi and Caulfield (arXiv:2508.16920), whose
setup D8's BALL arm reproduces. A positive OT contribution would need a different instrument, for
example the finite-gain observer exponent of the theory note's Section 6 as the selection
criterion.

### 3.4 The gap between determining-mode bounds and observed synchronization

Open question. Rigorous counts of determining modes and nodes for 2-D Navier–Stokes scale with the
Grashof number (Jones and Titi 1993, and the damped-driven estimates of arXiv:math/0507327 that
match attractor-dimension bounds). In practice far fewer low modes synchronize a nudged copy
(Inubushi and Caulfield report a threshold near the forcing wavenumber). In 3-D, Cheskidov, Dai
and Kavlie (arXiv:1507.05908) bound a time-averaged determining wavenumber.

OT test. Only the mode-choice part of this question is OT's. D8 asks it.

Assessment. Weak fit for OT specifically. The gap is about the size of the bounds, which is a
problem of analysis, and OT's contribution would be the choice of modes, which D8 suggests does
not beat the ball.

### 3.5 Probes and features in mechanistic interpretability

Open question. Sharkey et al., "Open Problems in Mechanistic Interpretability" (arXiv:2501.16496,
TMLR 2025), survey the field. The linear representation hypothesis is a working assumption
rather than a theorem. That paper's text on probing was not read for this note.

OT test. `readscope` already recovers a consumer's read subspace blind and has one sealed positive
cell family on a 3B model and one sealed negative (GO-P-2026-020). The open question OT can
address is which directions a downstream consumer actually reads, as opposed to which directions a
probe can decode.

Assessment. Good conceptual fit and an existing instrument, but the evidence base is one model
and the field's open problems are mostly about defining features, which OT does not settle.

### 3.6 Choosing observables in quantum state learning

Open question. Shadow tomography (Aaronson) and classical shadows (Huang, Kueng and Preskill)
estimate many observables from few copies. Classical shadows are independent of the observables,
so they sidestep choosing them in advance. A survey of learning complexity is arXiv:2305.20069.

Assessment. Weak fit. The leading protocol removes the selection question that OT would address.
Not pursued unless a setting appears where the observables must be chosen.

## 4. Suggested order, not decided

1. 3.1, observable selection for EDMD, as a preregistered gate reusing D7's world and instrument.
2. 3.2, Mori–Zwanzig memory length, after a status check of the post-2020 literature.
3. Finish D8 and report it whatever its grade, with 3.3 as its framing.

Nothing in this survey suggests an OT route to a Millennium problem.

## Sources

- Buono, Observers, symmetries, and the hierarchy of language classes. https://arxiv.org/abs/2606.27407
- Edwards, Toward P vs NP, an observer-theoretic separation. https://arxiv.org/abs/2512.11820
- Nye, Observer-dependence in P vs NP. https://www.scirp.org/journal/paperinformation?paperid=140045
- Ramezanian, Embedded observers and the provability of P = NP. https://pith.science/paper/2609.10864
- Chen, Hu, Ren, New algebrization barriers via Missing-String. https://arxiv.org/abs/2511.14038
- Aaronson, Wigderson, Algebrization. https://cris.huji.ac.il/en/publications/algebrization-a-new-barrier-in-complexity-theory/
- Chen, Hirahara, Oliveira, Pich, Rajgopal, Santhanam, Beyond natural proofs. https://arxiv.org/abs/1911.08297
- Ren, Santhanam, meta-complexity and relativization. https://eccc.weizmann.ac.il/report/2021/089
- de Rezende, Meir, Nordström, Pitassi, Robere, KRW composition theorems via lifting. https://arxiv.org/abs/2007.02740
- de Rezende, Recent advancements in monotone circuit complexity. https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2025.4
- Mulmuley, On P vs. NP and geometric complexity theory. https://arxiv.org/abs/0908.1936
- Colbrook, The multiverse of dynamic mode decomposition algorithms. https://arxiv.org/abs/2312.00137
- Finding Koopman invariant subspaces via personalized PageRank. https://arxiv.org/abs/2605.24666
- Parish, Duraisamy, Non-Markovian closure models for LES via Mori–Zwanzig. https://arxiv.org/abs/1611.03311
- Kazma et al., State-robust observability measures for sensor selection. https://cs.paperswithcode.com/paper/state-robust-observability-measures-for
- Mons, Marquet, Sensor placement for mean-flow reconstruction. https://resolve.cambridge.org/core/journals/journal-of-fluid-mechanics/article/linear-and-nonlinear-sensor-placement-strategies-for-meanflow-reconstruction-via-data-assimilation/AF93D708AE79F30D39CC5F58A0C241D6
- Cheskidov, Dai, Kavlie, Determining modes for the 3D Navier–Stokes equations. https://arxiv.org/abs/1507.05908
- Sharp estimates for the damped-driven 2D Navier–Stokes equations. https://arxiv.org/abs/math/0507327
- Sharkey et al., Open problems in mechanistic interpretability. https://arxiv.org/abs/2501.16496
- A survey on the complexity of learning quantum states. https://arxiv.org/abs/2305.20069
