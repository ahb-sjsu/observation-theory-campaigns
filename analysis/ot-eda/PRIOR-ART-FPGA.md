# OT-EDA / FPGA silicon cell — prior-art sweep (2026-09-04, owner-promoted)

Instruments: Crossref API (arXiv 429'd, DBLP 500'd tonight); citations located
with DOIs. Three literatures border the cell; all three are thick; the sweep's
job was to find the closest empirical work and carve what survives.

## The three bordering literatures (cite all, claim none)

1. **Timing speculation / better-than-worst-case design** (the mechanism
   line): Ernst et al., "Razor: a low-power pipeline based on circuit-level
   timing speculation," MICRO-36 2003 (10.1109/micro.2003.1253179; IEEE Micro
   2004 10.1109/mm.2004.85); Austin et al., "Deployment of better than
   worst-case design," ICCD 2005 (10.1109/iccd.2005.43, the canonical
   statement). These EXPLOIT the fact that typical operands rarely sensitize
   worst-case paths; they build recovery hardware. The workload-dependence of
   real timing margin is their founding observation, owned outright.
2. **FPGA guardband characterization, voltage axis**: the Salami line ("Fault
   Characterization Through FPGA Undervolting," FPL 2018,
   10.1109/fpl.2018.00023, plus the ECC and harsh-conditions successors) and
   workload-specific DL undervolting studies (Koc et al., IEEE Micro 2022,
   10.1109/mm.2022.3153891; Souvatzoglou ICFPT 2025). Real error-onset vs
   vendor margins, measured on silicon, workload-dependence noted. The
   voltage-axis twin of our frequency sweep.
3. **FPGA overclocking, frequency axis — THE CLOSEST WORK**: Kan Shi et al.,
   "Accuracy-Performance Tradeoffs on an FPGA through Overclocking," FCCM
   2013 (10.1109/fccm.2013.10) and the ISCAS 2013 companion
   (10.1109/iscas.2013.6572395): datapaths clocked past fmax, error behavior
   characterized on hardware, motivated by approximate computing (accept
   error magnitude for throughput). Plus overclocking-with-error-detection
   lines (Gharehbaghi FPGA 2010; Marty FPT 2018). Classical false-path /
   functional timing analysis is the STA-side ancestor of "paths this
   workload never sensitizes."

## What survives (the carved kernel, consistent with every sweep this week)

The phenomenon — real silicon margin beyond the STA verdict, data-dependent —
is owned three ways over. Never claim it. The surviving OT shape:

1. **The two-consumer verdict inversion on ONE artifact.** Shi et al. measure
   an accuracy-frequency TRADEOFF for one computation; nobody found runs two
   autonomous consumers (input-pattern families sensitizing disjoint path
   classes) against the SAME bitstream and shows the operational verdict
   (errors / clean) INVERTING between them at fixed clock — including the P3
   build that fails STA on consumer-B paths and runs provably clean for
   consumer A. Tradeoff curves are theirs; the verdict-inversion structure is
   the program's signature and is not in this literature.
2. **The certificate framing with measured error rates.** STA's clean/dirty
   is treated here as a consumer-independent CERTIFICATE, and the cell
   measures its per-consumer false-alarm rate (and, in the guardband
   direction, false-clear) against silicon at matched thresholds — the same
   endpoint discipline as EC-grid/D8, absent from all three literatures,
   which aim at mechanisms (Razor), reliability margins (Salami), or
   approximate-computing budgets (Shi).
3. **Pre-stated conjunction-law bars + the validity-attestation tie**
   (P3787): sealed predictions, both arms, verdicts as executed; and the
   product-facing clause "this timing certificate is valid FOR THIS
   CONSUMER'S read at this operating point."

## Consequence for the cell design

- P1 (guardband exists) is a REPLICATION of known results on our substrate —
  label it so, never a claim.
- P2 (consumer-relative onset beyond noise) and P3 (certificate false-alarms
  consumer-relatively; the STA-failing bitstream clean for the non-sensitizing
  consumer) carry the novelty; P3 is the headline and must be carved against
  Shi et al. explicitly in any draft.
- Cite Razor/Austin as the literature that built MECHANISMS on this physics;
  position the cell as the LAW + certificate measurement.

## Status

PROMOTED by the owner 2026-09-04; sweep complete; next concrete steps (behind
the CR-I-EIP-V2 obligations): Vivado/Vitis container recon on NRP (FlexLM
reachability, U55C platform files), then the kernel design with two
sensitization families, then pre-stated predictions committed before any
hardware run. NRP rules pinned in the project memory: XRT xclbin flow only,
no shell reflashing, measured-sizing guard on all build jobs.
