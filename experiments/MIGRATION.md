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
| pgrep(→pg), mongo, pgx, geofleet, zk | DATABASE-FRESHNESS | yes (all 5/6) | pending |
| csi, beam, aicsi, ho | RADIO-FRESHNESS | yes (4) | pending |
| urllc, phy, cca | RADIO-FRESHNESS | no (unsealed / hw-gated) | pending |
| econ | MARKETS-FRESHNESS | no (sim/data-gated) | pending |
| rpki, xproto(routing core), d8 | ROUTING-TELEMETRY | yes (BGP/ISIS/OSPF/RPKI) | pending; **D8 after V1 data lands (live now)** |
| ran (RAN governor) | RADIO-FRESHNESS | ref impl | pending |
| freshread (read_fresh lib) | DATABASE-FRESHNESS (shared) | lib | pending |
| notes/ (Ricci note) | → paper/ or notes/ | note | pending |
| outreach/ (ben-reed, sjsu-quantum) | → outreach/ | — | pending |
| standards/ (IEEE-SA IC whitepaper) | → standards/ | — | pending |

## Stays in network-governor (routing/telemetry PRODUCT)

`emulation/` (GoBGP mesh, V1a, topo), `governor/` (store, ledger, api, sealed,
detector, pg), `dashboards/`, `migrations/`, product `tests/`, `docs/`,
packaging. `ip/INVENTION-DISCLOSURE-PG-CERT.md` stays (private, IP-gated).

## Provenance note

Original sealing commits live in network-governor's history; this repo's SEALS.md
rows cite them. Nothing is re-sealed by the move.
