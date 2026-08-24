# Re-home manifest: network-governor freshness program → this repo

**Started 2026-08-24.** Owner directive: unify OT under
`observation-theory-campaigns`; dissolve the `DATABASE-TRACK.md` §0 boundary;
`network-governor` becomes the routing/telemetry **product** (deployable code)
only. See [FRESHNESS-PROGRAM.md](FRESHNESS-PROGRAM.md).

Method: **track-by-track, atomic.** Per track — copy cell files byte-identically
into `analysis/<cell>/` here, add the track doc + `SEALS.md` rows (sealed cells),
commit here; then `git rm` the cell from network-governor with a pointer commit.
Seal provenance preserved per FRESHNESS-PROGRAM.md.

## Mapping (source `network-governor/analysis/<cell>` → here)

| Cell(s) | Track | Sealed? | Status |
|---|---|---|---|
| quantum | QUANTUM-COMPUTING | no (gated: real IBM hw) | **DONE (template)** |
| pgrep, mongo, pgx, geofleet, zk | DATABASE-FRESHNESS | yes (5) | **DONE** |
| csi, beam, aicsi, ho | RADIO-FRESHNESS | yes (4) | **DONE** |
| urllc, phy, cca | RADIO-FRESHNESS | no (unsealed / hw-gated) | **DONE** |
| ran (RAN governor), freshread (lib) | RADIO / shared | ref impl / lib | **DONE** |
| econ | MARKETS-FRESHNESS | no (sim/data-gated) | **DONE** |
| notes/ (Ricci note) | notes/ | note | **DONE** |
| outreach/ (ben-reed, sjsu-quantum) | outreach/ | — | **DONE** |
| standards/ (IEEE-SA IC whitepaper) | standards/ | — | **DONE** |
| rpki, xproto (routing core), d8 | ROUTING-TELEMETRY | yes (BGP/ISIS/OSPF/RPKI) | **DEFERRED** — see below |

## Routing-telemetry: deferred (post-D8-V1)

The routing evidence (BGP/IS-IS/OSPF/RPKI/BMP cells in `analysis/xproto`,
`analysis/rpki`) is the most entangled with the deployable product (`emulation/`,
`governor/`) and `analysis/d8` is **live** (D8-V1 armed on Atlas 2026-08-24, data
lands over the following days). Separating routing evidence from the routing
product deserves a dedicated pass **after V1 data lands and its analysis + prereg
amendment complete**, so the live campaign is not disrupted mid-flight. Until
then, routing stays in `network-governor` and the ROUTING-TELEMETRY track doc
there governs it. This is the one remaining re-home step.

## Stays in network-governor (routing/telemetry PRODUCT)

`emulation/` (GoBGP mesh, V1a, topo), `governor/` (store, ledger, api, sealed,
detector, pg), `dashboards/`, `migrations/`, product `tests/`, `docs/`,
packaging. `ip/INVENTION-DISCLOSURE-PG-CERT.md` stays (private, IP-gated).

## Provenance note

Original sealing commits live in network-governor's history; this repo's SEALS.md
rows cite them. Nothing is re-sealed by the move.
