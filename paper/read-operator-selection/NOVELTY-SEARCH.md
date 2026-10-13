# Novelty search for the write-up (paper/read-operator-selection)

2026-10-13. Open item 3 of `OUTLINE.md`. A search for prior work on each claim the write-up could
make about novelty, run before any novelty sentence is written.

## How it was searched, and what that does not cover

The outline asked for Google Scholar and Web of Science. Neither was reachable from this session.
Web of Science needs a subscription login, and Scholar has no programmatic access. The search used
OpenAlex (an open index of about 250 million works, which covers Crossref, arXiv and PubMed), with
fifteen keyword queries, the top eight results of each, and targeted lookups of the papers found.
Semantic Scholar was tried and rate-limited after one query. Abstracts were read from OpenAlex's
stored abstracts, not from the full papers. This is a keyword search of one index, not a
systematic review. A paper the queries did not phrase can be missing, and a Scholar or Web of
Science pass by the owner is still worth doing before submission. The queries and the raw output
are in the session's scratch files, `novelty_search.py` and its two output files.

## Findings, claim by claim

### Read distortion as a selection criterion (the ranking READ)

Not new in form. Meteorology's observation targeting ranks where to observe by a sensitivity of a
forecast to the initial state, weighted by the initial uncertainty. Ancell and Hakim (Mon. Wea. Rev.
135, 2007, doi:10.1175/2007MWR1904.1) show that ensemble sensitivity "is proportional to the
projection of the analysis-error covariance onto the adjoint-sensitivity field". The variance
reduction expected from observing a variable is then of the form (sensitivity)² × variance. READ is
the diagonal form of that criterion, with the consumer's one-step tendency as the forecast metric.
Adjoint-sensitivity targeting predates it: Baker and Daley (QJRMS 126, 2000,
doi:10.1002/qj.49712656511). For reduced models, Daescu and Navon's dual-weighted approach to order
reduction in 4D-Var (Mon. Wea. Rev. 136, 2008, doi:10.1175/2007MWR2102.1) weights snapshots by adjoint
sensitivity.

Consequence. The write-up must present read distortion as OT's derivation of a known targeting
criterion (Proposition 4: optimal under random phases) and cite this line. It may not present it as
a new selector. The contribution is the cross-task map, which this search did not find elsewhere:
one criterion compared with energy and scale on placement, closure, nudging, Koopman forecasting and
memory, under preregistered graders.

### The Gramian instrument of OP4 (GRAM)

Not new. Three lines cover it.
- Singular-vector targeting. The leading singular vectors of the tangent propagator over an
  optimization window choose where to observe. Palmer, Gelaro, Barkmeijer and Buizza, J. Atmos. Sci.
  55, 1998, doi:10.1175/1520-0469(1998)055<0633:SVMAAO>2.0.CO;2, 477 citations, argue that the choice
  of metric matters, which is OT's $G$. Buizza and Montani, J. Atmos. Sci. 56, 1999.
- Empirical and variational Gramians for nonlinear sensor placement. Singh and Hahn (2004); Serpas,
  Chu and Hahn (2013); Kazma and Taha, "Observability for nonlinear systems: connecting variational
  dynamics, Lyapunov exponents, and empirical Gramians" (IEEE Trans. Control Netw. Syst., 2026,
  doi:10.1109/TCNS.2026.3721959). Their Variational Gramian, built from the tangent dynamics, is
  OP4's instrument in substance.
- Assimilation in the unstable subspace (AUS). Trevisan and Uboldi (J. Atmos. Sci. 61, 2004,
  doi:10.1175/1520-0469(2004)061<0103:AOSATO>2.0.CO;2); Carrassi and coauthors (2007, 2008); Trevisan,
  D'Isidoro and Talagrand (QJRMS 136, 2010, doi:10.1002/qj.571); review by Palatella, Carrassi and
  Trevisan (J. Phys. A 2013).

Consequence. OP4 is a test of a known instrument family on D8's task against D8's controls, and the
write-up must say so. Its result ("system" on the probe) is the contribution, not the instrument.

### The near-neutral hypothesis recorded in OP4

Prior art, and it points the same way. Trevisan, D'Isidoro and Talagrand (2010) find that the
analysis error of 4D-Var confined to a subspace "is a minimum for N approximately equal to the
dimension of the unstable and neutral manifold". OP4's registered rule counted only the six positive
exponents ($d_u = 6$) and left out the four near-zero ones, so by this result its required count was
too small. This does not change OP4's probe reading, which used the rule as registered. It does
mean the hypothesis is not OP4's to claim. It also means that any re-registration of OP4 with an
unstable-plus-neutral count should cite this result as its reason, so that it is not a choice made
after seeing the probe.

### Which modes to nudge in turbulence (D8's BALL and the scale result)

Established, and D8 replicates it. Clark Di Leoni, Mazzino and Biferale (Phys. Rev. X 10, 011023,
2020, doi:10.1103/PhysRevX.10.011023) measure the scale-by-scale transition to synchronization in
three-dimensional turbulence under Fourier nudging. Inubushi and Caulfield (J. Fluid Mech., 2026,
doi:10.1017/jfm.2025.11057; arXiv:2508.16920) treat D8's own flow family and identify the threshold
with the leading Lyapunov exponent. Li, Si, Li and Xu (J. Fluid Mech., 2025, doi:10.1017/jfm.2025.133)
relate synchronization thresholds to Lyapunov vectors. Inubushi, Saiki, Kobayashi and Goto (Phys.
Rev. Lett. 131, 254001, 2023) use transverse Lyapunov exponents. None of those found ranks modes by a
sensitivity-weighted criterion against scale. That comparison, D8's, appears to be new, and its
outcome (scale wins in all 8 cells) is consistent with them.

### Observable selection for EDMD dictionaries by the consumer's sensitivity (OP1)

Nothing found. The dictionary-selection literature found chooses by fit to data or by sparsity:
EDMD with dictionary learning (Li et al. 2017), sparsity-promoting Koopman-invariant subspaces (Pan,
Arnold and Duraisamy, J. Fluid Mech. 2021, doi:10.1017/jfm.2021.271), ResDMD residuals (Colbrook and
Townsend). OP1's comparison appears new. Its result is a tie with scale and a pilot FAIL.

### Choosing explicit modes to shorten Mori–Zwanzig memory (OP2)

Nothing found that selects modes to shorten memory. Tian, Lin, Anghel and Livescu (Phys. Fluids 33,
125118, 2021) compare hand-chosen observable sets. Lin and coauthors (SIAM J. Appl. Dyn. Syst. 2021,
doi:10.1137/21M1401759; 2023, doi:10.1137/22M1506146) give the learning framework. OP2's comparison
appears new. Its result is slightly behind scale and a pilot FAIL.

### Closure mode selection by sensitivity times energy (D7v3)

Nothing found that selects the subfilter modes a closure keeps by sensitivity times energy. Daescu
and Navon's dual-weighted reduction (above) is the nearest relative. D7v3's sealed PASS appears to
be the campaign's least anticipated positive result.

## What changes in the outline

1. Section 2 presents read distortion as OT's derivation of the observation-targeting criterion,
   with Ancell and Hakim, Baker and Daley, and Palmer and coauthors cited, and not as a new selector.
2. Section 6 presents OP4 as a test of the singular-vector, variational-Gramian and AUS family on
   D8's task. The near-neutral point is attributed to Trevisan, D'Isidoro and Talagrand.
3. The contribution sentence is the preregistered cross-task map and the scale result for nudging
   with a sensitivity criterion. Neither was found in this search.
4. Before submission, the owner runs a Scholar or Web of Science pass on the two claims of novelty
   that remain, the cross-task comparison and D7v3's closure criterion.
