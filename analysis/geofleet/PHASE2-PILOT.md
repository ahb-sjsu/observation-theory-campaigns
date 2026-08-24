# Geo-fleet Phase 2 — pilot runbook

The real-WAN graduation of XPROTO-PGX: 2-3 Postgres read-replicas on NRP,
pinned to distinct regions, streaming from the public Atlas primary, with
the consumer-relative certificate routing each consumer to the nearest
CERTIFIED replica. This runbook is **staged and ready**; the actual NRP
submission is gated on connectivity (see the gate below).

## CONNECTIVITY GATE (status: BLOCKED as of 2026-08-21, boat/weak link)

Standing up pods on shared NRP infra REQUIRES being able to verify the
submission and tear it down. On 2026-08-21 (owner on the boat) the NRP
API was unreachable (`kubectl get ns` timed out) and Atlas RTT was ~1.4 s.
**Do NOT submit until:** `kubectl --request-timeout=10s get ns
ssu-atlas-ai` returns promptly AND Atlas RTT is sane (< ~100 ms). A
mid-submit connection drop can orphan Deployments on a 50-university
shared cluster — that is the one thing the do-no-harm rule forbids.

## Preflight — score EVERY submission (from reference_nrp_job_policies)

| rule | this pilot |
|---|---|
| Deployment, no GPU | ✅ plain `postgres:16-alpine`, no GPU |
| exempt class ≤1 CPU / ≤2 GB | ✅ `cpu=1 / mem=2Gi` (replica_manifest.py) |
| limits within 20% of requests | ✅ limits == requests |
| ephemeral-storage declared | ✅ requests+limits on both init & main |
| no sleep / real service | ✅ runs `postgres` as a hot standby |
| no capability requests | ✅ unprivileged; outbound-only to Atlas; no netem/tailscale caps |
| submit via toolchain, not bare kubectl apply | route through nats-bursting / a managed submit; verify `creationTimestamp` fresh |
| Deployment auto-deleted after 2 weeks | ✅ acknowledged; pilot, re-deploy |
| throttle / no fair-queue abuse | ✅ 2-3 replicas |
| PVC near Ceph | N/A — emptyDir (deliberate: enables zone spread) |

## Step 0 — Atlas public primary (once)

The replicas connect OUT to Atlas. On Atlas (`atlas_primary_setup.sh`,
run when Atlas is reachable):
- a primary Postgres with `ssl=on` (self-signed or LE cert), a
  **replication-only** role `fleet_replicator`, and `pg_hba` allowing
  `hostssl replication fleet_replicator 0.0.0.0/0 scram-sha-256`;
- the port (e.g. 5444) reachable via `atlas-sjsu.duckdns.org` (Atlas
  firewall / port-forward — Atlas-admin step);
- k8s secret `geofleet-repl` (key `password`) created in `ssu-atlas-ai`
  with the replicator password.

## Step 1 — render + submit the replicas (NRP reachable)

Pick 2-3 distinct region labels (from `kubectl get nodes
--show-labels | grep zone`), then:

```
python3 replica_manifest.py --name pgfleet-<r> \
  --region-label topology.kubernetes.io/zone=<zone> \
  --atlas-host atlas-sjsu.duckdns.org --atlas-port 5444 > r-<r>.yaml
# submit via the managed path; then IMMEDIATELY verify:
kubectl -n ssu-atlas-ai get deploy pgfleet-<r> -o jsonpath='{.metadata.creationTimestamp}'
kubectl -n ssu-atlas-ai get pods -l app=pgfleet-<r>
```

Confirm each pod reaches Ready (readinessProbe = `pg_isready`) and is
streaming (`pg_stat_wal_receiver` on the replica, or `pg_stat_replication`
on Atlas shows N walsenders).

## Step 2 — measure per-replica min-RTT → the guard

For each replica, measure the inter-site min replication latency (the
XPROTO-PGX probe: write a beacon on Atlas, poll the replica). This feeds
each replica's derived guard/tick DIRECTLY — the PGX rule
`tick=clamp(0.3*min_lat,[0.01,0.03]), guard=2*tick` already does this;
real geo min-RTT replaces the netem floor. No cell code changes.

## Step 3 — the geo-fleet cell (nearest-CERTIFIED routing)

With N geo replicas, the certificate stops being "fall back to primary if
stale" and becomes "route each consumer to the nearest replica CERTIFIED
for its footprint" — the `routing.py pick()` locality-ordering change
(order candidates by measured RTT, take the first CERTIFIED). Grade the
certificate router vs naive "nearest" and "least-global-lag" routers,
under the replicas' independent network weather. Prereg → shakedown →
fresh-day seal, same arc as the DB cells. This is the survey's geo-fleet
cell on real infrastructure.

## Teardown

```
kubectl -n ssu-atlas-ai delete deploy -l geofleet.role=pg-replica
```
Verify zero `pgfleet-*` pods remain. (emptyDir data is ephemeral — nothing
to purge; re-basebackup on redeploy.)

## Artifacts

- `replica_manifest.py` — exempt-sized region-pinned replica Deployment
  (validated: valid YAML, policy-clean).
- `atlas_primary_setup.sh` — the Atlas public-primary setup (owed; run on
  Atlas when reachable).
- Scoping: `../pgx/GEO-FLEET-PHASE1.md`; instrument: XPROTO-PGX (sealed).
