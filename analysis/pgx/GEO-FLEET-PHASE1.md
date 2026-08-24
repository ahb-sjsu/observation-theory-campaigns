# Geo-fleet — Phase 1 scoping (NRP real-WAN graduation of XPROTO-PGX)

The real-WAN graduation: replace the netem lag simulation with genuine
geo-distribution across NRP.ai's 50+ university sites, and grade the
consumer-relative certificate as a **nearest-certified router** across a
real geo fleet (the survey's geo-fleet cell). Phase 1 = scope + preflight,
no NRP writes. Phase 2 (pilot) needs an explicit go — it puts pods on
shared infra.

## Findings

### F1 — NRP access is live
`kubectl` context `nautilus`, namespace `ssu-atlas-ai` active (128d),
`auth can-i create deployments -n ssu-atlas-ai` → **yes** (pods too).
Working kubeconfig + RBAC; no access request needed.

### F2 — nats-bursting supports persistent Deployments (open question: resolved YES)
`python/nats_bursting/pool.py`: `PoolDescriptor` + `pool_manifest()` render
a `kind: Deployment` for always-on pods, and it is **already NRP-sized** —
defaults `cpu=1/memory=2Gi` with the in-code note *"stay at cpu=1/memory=
2Gi to remain in swarm-mode; bigger pods trigger the heavy-mode 4-pod
cap."* `requests == limits` (satisfies the ≤20% rule). So the toolchain
has the Deployment shape; we do NOT hand-roll `kubectl apply`.

**Adaptation needed (small):** `pool_manifest()` hardcodes a NATS-worker
container (`command: bash -c … exec worker_entry`). A Postgres replica
needs a custom container + an init/basebackup step. Two options:
- (a) extend `pool_manifest` / add a sibling `service_manifest(pod_spec)`
  that accepts a caller-provided container spec (preferred — keeps the
  policy-safe sizing/labels and the submit path);
- (b) a dedicated `pgreplica_manifest()` in the geo-fleet code reusing the
  same resource/label conventions.
Either way the submit path is the existing coordinator, not raw apply.
**Gap to fix in the manifest:** it does not declare `ephemeral-storage`
(requests+limits) — required by policy for anything writing node disk,
and our replica's pgdata is on `emptyDir`. Add it (e.g. 8Gi/8Gi).

### F3 — Connectivity: public Atlas PG endpoint, NOT tailscale-in-pod
The NRP replica's walreceiver **connects out** to the cascade source to
pull WAL. A Tailscale sidecar would need kernel mode (TUN + `NET_ADMIN`),
which NRP will not grant and we will not request (standing rule). Userspace
Tailscale only offers a SOCKS proxy, which Postgres streaming can't use.
**Design:** the primary lives on **Atlas**, exposed on a public port via
`atlas-sjsu.duckdns.org` with **TLS required + a replication-only role**
(ideally TLS client-cert auth); NRP pods reach it over plain egress (the
V1a canary already proved NRP → public-internet egress works). No inbound
to NRP, no tailscale in the pod, no caps. Atlas as primary (stable, public)
is also simpler than cascading off the roaming laptop — the geo lives in
the NRP replicas' physical distribution, not in the source.

### F4 — Geo-diversity placement
Pin each replica to a distinct region with `nodeAffinity` on the node
topology/region labels; because pgdata is `emptyDir` (not a Ceph PVC),
replicas are free to scatter across zones — the exact thing a Ceph-PVC
workload can't do. Re-basebackup on pod loss (ephemeral is fine for a
read replica).

## NRP policy preflight — scorecard (Deployment)

| rule | status |
|---|---|
| Deployment cannot request GPU | ✅ no GPU |
| exempt class ≤1 CPU / ≤2 GB | ✅ `cpu=1/memory=2Gi` (pool default) |
| limits within 20% of requests | ✅ `requests == limits` |
| **ephemeral-storage declared** | ⚠️ **must add** to the manifest (emptyDir pgdata) |
| no sleep / terminates-or-serves | ✅ runs `postgres`, a real service |
| no capability requests | ✅ unprivileged PG; no netem on NRP (real lag replaces it); no tailscale caps |
| submit via nats-bursting, not `kubectl apply` | ✅ via `pool` coordinator (after F2 adaptation) |
| Deployment auto-deleted after 2 weeks | ✅ acknowledged — fine for a pilot; re-deploy |
| no fair queue / throttle | ✅ pilot = 2–3 replicas |
| PVC pinned near Ceph | N/A — emptyDir, deliberately (enables zone spread) |

Net: a stock, unprivileged, exempt-sized Postgres-replica Deployment is
policy-clean; the only concrete gaps are (i) the `ephemeral-storage`
declaration and (ii) the custom-container manifest path.

## Instrument readiness

XPROTO-PGX is instrument-clean (seed-stable shakedown PASS). Its derived
guard rule — `tick = clamp(0.3·min_lat, [0.01,0.03])`, `guard = 2·tick`,
`min_lat` measured by probing — is exactly what a real geo fleet needs:
each NRP replica's measured inter-site min-RTT (tens of ms) sets its own
tick/guard. Nothing about the certificate changes; only the lag source
does. The routing extension (certificate picks the nearest CERTIFIED
replica) is the `routing.py pick()` locality-ordering change.

## Phase 2 (pilot) — gated on explicit go

1. Land the `pool.py` custom-container/`ephemeral-storage` adaptation (F2).
2. Stand up the Atlas public TLS primary + replication role (F3).
3. Submit 2–3 exempt-sized PG-replica Deployments pinned to distinct NRP
   regions (F4), cascading/streaming from Atlas.
4. Measure per-replica inter-site min-RTT → feeds each replica's guard.
5. Run the geo-fleet cell: certificate = nearest-CERTIFIED router, graded
   vs naive nearest / least-lag routers. Then prereg → shakedown →
   fresh-day seal (the real-WAN graduation).

**Gate:** steps 3+ put Postgres on shared NRP nodes → checkpoint before
submitting. Build ≠ run.
