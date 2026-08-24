"""Geo-fleet Phase 2 — render an exempt-sized Postgres read-replica
Deployment for NRP, pinned to a region, streaming from the public Atlas
primary. This is the custom-container path Phase 1 flagged as owed (the
nats-bursting pool.py renders a NATS *worker*, not Postgres) plus the
ephemeral-storage declaration the policy requires for emptyDir pgdata.

NRP-policy-safe by construction (score in PHASE2-PILOT.md): no GPU, no
caps, requests==limits, exempt class (cpu=1/mem=2Gi), ephemeral-storage
declared, emptyDir pgdata (so replicas scatter across zones), a plain
`postgres:16-alpine` container. Connectivity is OUTBOUND to the public
Atlas endpoint (TLS + a replication-only role) — no tailscale-in-pod
(NET_ADMIN NRP won't grant).

    python3 replica_manifest.py --name pgfleet-ucsd \
        --region-label topology.kubernetes.io/zone=ucsd-suncave \
        --atlas-host atlas-sjsu.duckdns.org --atlas-port 5444 > r-ucsd.yaml

Submit via the toolchain (NRP reachable) — see PHASE2-PILOT.md; NEVER a
bare kubectl apply on shared infra without the preflight.
"""

from __future__ import annotations

import argparse

TEMPLATE = """\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {name}
  namespace: {ns}
  labels:
    app: {name}
    geofleet.role: pg-replica
    geofleet.region: {region_val}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {name}
  template:
    metadata:
      labels:
        app: {name}
        geofleet.role: pg-replica
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: {region_key}
                operator: In
                values: ["{region_val}"]
      volumes:
      - name: pgdata
        emptyDir:
          sizeLimit: {disk}
      initContainers:
      - name: basebackup
        image: postgres:16-alpine
        command: ["sh","-c"]
        args:
        - |
          set -e
          rm -rf /pgdata/* 2>/dev/null || true
          until pg_isready -h {atlas_host} -p {atlas_port} -U {repl_user}; do sleep 2; done
          PGSSLMODE=require pg_basebackup -h {atlas_host} -p {atlas_port} \\
            -U {repl_user} -D /pgdata -R -X stream
          chmod 700 /pgdata
        env:
        - name: PGPASSWORD
          valueFrom:
            secretKeyRef:
              name: {secret}
              key: password
        volumeMounts:
        - {{name: pgdata, mountPath: /pgdata}}
        resources:
          requests: {{cpu: "500m", memory: "512Mi", ephemeral-storage: "1Gi"}}
          limits:   {{cpu: "500m", memory: "512Mi", ephemeral-storage: "1Gi"}}
      containers:
      - name: postgres
        image: postgres:16-alpine
        command: ["postgres","-D","/pgdata","-c","hot_standby=on",
                  "-c","shared_preload_libraries=pg_stat_statements",
                  "-c","listen_addresses=*"]
        ports:
        - containerPort: 5432
        volumeMounts:
        - {{name: pgdata, mountPath: /pgdata}}
        readinessProbe:
          exec:
            command: ["pg_isready","-U","postgres"]
          initialDelaySeconds: 20
          periodSeconds: 10
        resources:
          requests: {{cpu: "1", memory: "2Gi", ephemeral-storage: "{disk}"}}
          limits:   {{cpu: "1", memory: "2Gi", ephemeral-storage: "{disk}"}}
"""


def render(name, ns, region_key, region_val, atlas_host, atlas_port,
           repl_user, secret, disk):
    return TEMPLATE.format(
        name=name, ns=ns, region_key=region_key, region_val=region_val,
        atlas_host=atlas_host, atlas_port=atlas_port, repl_user=repl_user,
        secret=secret, disk=disk)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--namespace", default="ssu-atlas-ai")
    ap.add_argument("--region-label", required=True,
                    help="k8s nodeAffinity label, e.g. "
                         "topology.kubernetes.io/zone=ucsd-suncave")
    ap.add_argument("--atlas-host", default="atlas-sjsu.duckdns.org")
    ap.add_argument("--atlas-port", default="5444")
    ap.add_argument("--repl-user", default="fleet_replicator")
    ap.add_argument("--secret", default="geofleet-repl")
    ap.add_argument("--disk", default="8Gi")
    a = ap.parse_args()
    key, _, val = a.region_label.partition("=")
    print(render(a.name, a.namespace, key, val, a.atlas_host, a.atlas_port,
                 a.repl_user, a.secret, a.disk), end="")


if __name__ == "__main__":
    main()
