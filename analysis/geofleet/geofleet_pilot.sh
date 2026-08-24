#!/usr/bin/env bash
# Geo-fleet Phase 2 pilot, Option B (all-in-NRP), orchestrated FROM ATLAS
# (stable 22ms link to the NRP API). Brings up a Postgres primary + N
# zone-spread streaming replicas in ssu-atlas-ai, all in-cluster (no
# public exposure, no router config). Self-cleans on PRIMARY failure;
# leaves partial replicas up + logged for inspection (one-command
# teardown). Everything is labeled geofleet.pilot=b.
#
#   geofleet_pilot.sh [N]        # default N=3
#   geofleet_pilot.sh teardown   # delete everything labeled geofleet.pilot=b
set -uo pipefail
NS=ssu-atlas-ai
SEL=geofleet.pilot=b
N="${1:-3}"
log(){ echo "[$(date -u +%H:%M:%S)] $*"; }

teardown(){
  log "TEARDOWN: deleting deploy,svc -l $SEL in $NS"
  kubectl -n "$NS" delete deploy,svc,configmap -l "$SEL" --ignore-not-found --wait=false 2>&1 | sed 's/^/  /'
}
if [ "${1:-}" = "teardown" ]; then teardown; exit 0; fi

log "=== geo-fleet pilot B: primary + $N zone-spread replicas in $NS ==="
log "preflight: Deployment, no GPU, no caps, exempt cpu=1/mem=2Gi, limits==requests, emptyDir + ephemeral-storage declared, in-cluster only"
log "orchestrated from $(hostname) ; kubectl ctx $(kubectl config current-context 2>/dev/null)"

# --- primary + ClusterIP service (teardown on failure: nothing works without it) ---
trap 'rc=$?; log "PRIMARY stage failed (rc=$rc) -> self-cleaning"; teardown; exit $rc' ERR
set -e
kubectl -n "$NS" apply -f - <<YAML
apiVersion: v1
kind: ConfigMap
metadata: { name: pgfleet-inithba, namespace: $NS, labels: { geofleet.pilot: b } }
data:
  00-repl-hba.sh: |
    #!/bin/sh
    # postgres image adds 'host all all all trust' but NOT a replication
    # line; pg_basebackup needs this. Runs once at initdb (fresh emptyDir).
    echo "host replication all all trust" >> /var/lib/postgresql/data/pg_hba.conf
---
apiVersion: v1
kind: Service
metadata: { name: pgfleet-primary, namespace: $NS, labels: { geofleet.pilot: b } }
spec:
  selector: { app: pgfleet-primary }
  ports: [ { port: 5432, targetPort: 5432 } ]
---
apiVersion: apps/v1
kind: Deployment
metadata: { name: pgfleet-primary, namespace: $NS, labels: { geofleet.pilot: b } }
spec:
  replicas: 1
  selector: { matchLabels: { app: pgfleet-primary } }
  template:
    metadata: { labels: { app: pgfleet-primary, geofleet.pilot: b } }
    spec:
      containers:
      - name: postgres
        image: postgres:16-alpine
        env:
        - { name: POSTGRES_PASSWORD, value: fleetpilot }
        - { name: POSTGRES_HOST_AUTH_METHOD, value: trust }   # in-cluster ClusterIP only
        args: ["-c","wal_level=replica","-c","max_wal_senders=10",
               "-c","max_replication_slots=10",
               "-c","shared_preload_libraries=pg_stat_statements",
               "-c","listen_addresses=*"]
        ports: [ { containerPort: 5432 } ]
        readinessProbe:
          exec: { command: ["pg_isready","-U","postgres"] }
          initialDelaySeconds: 10
          periodSeconds: 5
        volumeMounts:
        - { name: pgdata, mountPath: /var/lib/postgresql/data }
        - { name: inithba, mountPath: /docker-entrypoint-initdb.d }
        resources:
          requests: { cpu: "1", memory: "2Gi", ephemeral-storage: "4Gi" }
          limits:   { cpu: "1", memory: "2Gi", ephemeral-storage: "4Gi" }
      volumes:
      - { name: pgdata, emptyDir: { sizeLimit: "4Gi" } }
      - { name: inithba, configMap: { name: pgfleet-inithba } }
YAML
log "waiting for primary Ready (<=240s)..."
kubectl -n "$NS" rollout status deploy/pgfleet-primary --timeout=240s
trap - ERR                      # primary up: from here, don't auto-nuke on hiccups
set +e

# --- N zone-spread streaming replicas (in-cluster; real inter-zone latency = the geo lag) ---
kubectl -n "$NS" apply -f - <<YAML
apiVersion: apps/v1
kind: Deployment
metadata: { name: pgfleet-replica, namespace: $NS, labels: { geofleet.pilot: b, geofleet.role: pg-replica } }
spec:
  replicas: $N
  selector: { matchLabels: { app: pgfleet-replica } }
  template:
    metadata: { labels: { app: pgfleet-replica, geofleet.pilot: b, geofleet.role: pg-replica } }
    spec:
      securityContext: { runAsUser: 70, runAsGroup: 70, fsGroup: 70 }   # postgres uid in alpine
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: ScheduleAnyway         # best-effort geo spread
        labelSelector: { matchLabels: { app: pgfleet-replica } }
      initContainers:
      - name: basebackup
        image: postgres:16-alpine
        command: ["sh","-c"]
        args:
        - |
          set -e
          until pg_isready -h pgfleet-primary -U postgres; do sleep 2; done
          # basebackup into a SUBDIR we create (uid 70): pg_basebackup sets
          # it to 0700 itself. The emptyDir mount root is root-owned
          # (fsGroup only), so we cannot chmod it -> use a self-owned subdir.
          rm -rf /var/lib/postgresql/data/pgdata
          pg_basebackup -h pgfleet-primary -U postgres -D /var/lib/postgresql/data/pgdata -R -X stream
        volumeMounts: [ { name: pgdata, mountPath: /var/lib/postgresql/data } ]
        resources:
          requests: { cpu: "500m", memory: "512Mi", ephemeral-storage: "1Gi" }
          limits:   { cpu: "500m", memory: "512Mi", ephemeral-storage: "1Gi" }
      containers:
      - name: postgres
        image: postgres:16-alpine
        args: ["-c","hot_standby=on",
               "-c","shared_preload_libraries=pg_stat_statements",
               "-c","listen_addresses=*"]           # entrypoint starts standby on basebackup'd PGDATA
        env: [ { name: PGDATA, value: /var/lib/postgresql/data/pgdata } ]
        ports: [ { containerPort: 5432 } ]
        readinessProbe:
          exec: { command: ["pg_isready","-U","postgres"] }
          initialDelaySeconds: 15
          periodSeconds: 5
        volumeMounts: [ { name: pgdata, mountPath: /var/lib/postgresql/data } ]
        resources:
          requests: { cpu: "1", memory: "2Gi", ephemeral-storage: "8Gi" }
          limits:   { cpu: "1", memory: "2Gi", ephemeral-storage: "8Gi" }
      volumes: [ { name: pgdata, emptyDir: { sizeLimit: "8Gi" } } ]
YAML
log "waiting for $N replicas Ready (<=360s; best-effort)..."
kubectl -n "$NS" rollout status deploy/pgfleet-replica --timeout=360s \
  || log "replica rollout not fully Ready in time — leaving up for inspection"

# --- verify streaming ---
sleep 6
PP=$(kubectl -n "$NS" get pod -l app=pgfleet-primary -o jsonpath='{.items[0].metadata.name}')
WS=$(kubectl -n "$NS" exec "$PP" -- psql -U postgres -tAc \
       "SELECT count(*) FROM pg_stat_replication" 2>/dev/null | tr -d '[:space:]')
log "walsenders streaming on primary: ${WS:-?} / $N"
log "=== pod placement (node / zone spread) ==="
kubectl -n "$NS" get pods -l "$SEL" -o wide 2>&1 | sed 's/^/  /'
kubectl -n "$NS" get pods -l app=pgfleet-replica \
  -o jsonpath='{range .items[*]}{.spec.nodeName}{"\n"}{end}' 2>/dev/null \
  | sort | uniq -c | sed 's/^/  distinct-node /'
if [ "${WS:-0}" = "$N" ]; then
  log "PILOT UP: primary + $N replicas streaming in-cluster. Next: per-replica RTT + geo-fleet cell (nearest-CERTIFIED routing)."
else
  log "PARTIAL: ${WS:-0}/$N streaming. Inspect; teardown with: geofleet_pilot.sh teardown"
fi
log "DONE. Teardown anytime: bash geofleet_pilot.sh teardown"
