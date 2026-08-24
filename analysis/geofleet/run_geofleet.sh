#!/usr/bin/env bash
# XPROTO-GEO driver (runs on ATLAS). Discovers the live replica pods,
# ships fam_geofleet.py as a ConfigMap, runs the measurement as an
# in-cluster Job (so it reaches the primary + every replica), and
# collects the RESULT_JSON into GEOREP-family.json.
#   run_geofleet.sh [seeds...]     (default "0 1 2")
set -uo pipefail
NS=ssu-atlas-ai
HERE="$(cd "$(dirname "$0")" && pwd)"
SEEDS="${*:-0 1 2}"
JOB="geofleet-measure-$(date +%s)"
OUT="$HERE/GEOREP-family.json"
log(){ echo "[$(date -u +%H:%M:%S)] $*"; }

log "discovering running replicas..."
REPLICAS=$(kubectl -n "$NS" get pods -l app=pgfleet-replica -o json | python3 -c '
import json,sys
d=json.load(sys.stdin); out=[]
for i,p in enumerate(d["items"]):
    ip=p["status"].get("podIP")
    if ip and p["status"].get("phase")=="Running":
        out.append({"name":f"r{i}","host":ip,"zone":p["spec"].get("nodeName","?").split(".")[0]})
print(json.dumps(out))')
NREP=$(printf '%s' "$REPLICAS" | python3 -c 'import json,sys;print(len(json.load(sys.stdin)))')
log "replicas ($NREP): $REPLICAS"
[ "${NREP:-0}" -ge 3 ] || { log "FATAL: fewer than 3 running replicas"; exit 1; }

log "shipping fam_geofleet.py as ConfigMap geofleet-code..."
kubectl -n "$NS" create configmap geofleet-code \
  --from-file=fam_geofleet.py="$HERE/fam_geofleet.py" \
  --dry-run=client -o yaml | kubectl apply -f - >/dev/null

log "submitting Job $JOB (seeds: $SEEDS)..."
kubectl -n "$NS" apply -f - <<YAML
apiVersion: batch/v1
kind: Job
metadata: { name: $JOB, namespace: $NS, labels: { geofleet.pilot: b, geofleet.role: measure } }
spec:
  backoffLimit: 1
  ttlSecondsAfterFinished: 1800
  template:
    metadata: { labels: { geofleet.pilot: b, geofleet.role: measure } }
    spec:
      restartPolicy: Never
      containers:
      - name: measure
        image: python:3.12-slim
        env:
        - { name: PRIMARY, value: "host=pgfleet-primary port=5432 user=postgres dbname=postgres connect_timeout=5" }
        - { name: REPLICAS, value: '$REPLICAS' }
        command: ["sh","-c"]
        args:
        - |
          set -e
          pip install --quiet --disable-pip-version-check "psycopg[binary]"
          python /code/fam_geofleet.py --seeds $SEEDS
        volumeMounts: [ { name: code, mountPath: /code } ]
        resources:
          requests: { cpu: "1", memory: "2Gi", ephemeral-storage: "2Gi" }
          limits:   { cpu: "1", memory: "2Gi", ephemeral-storage: "2Gi" }
      volumes: [ { name: code, configMap: { name: geofleet-code } } ]
YAML

log "waiting for Job to finish (<=800s)..."
if kubectl -n "$NS" wait --for=condition=complete "job/$JOB" --timeout=800s 2>/dev/null; then
  ST=complete
else
  ST=incomplete
fi
log "Job $ST. reading result from primary._geo_result (robust vs kubelet log timeouts)..."
PP=$(kubectl -n "$NS" get pod -l app=pgfleet-primary -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
kubectl -n "$NS" exec "$PP" -- psql -U postgres -tAc \
  "SELECT rec::text FROM _geo_result ORDER BY id DESC LIMIT 1" 2>/dev/null > "$OUT"
if [ ! -s "$OUT" ]; then      # fallback: the measure pod's log (may time out)
  MP=$(kubectl -n "$NS" get pod -l job-name="$JOB" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
  kubectl -n "$NS" logs "$MP" 2>/dev/null | sed -n 's/^RESULT_JSON://p' | tail -1 > "$OUT"
fi
log "measure-pod log tail (best effort):"
MP=$(kubectl -n "$NS" get pod -l job-name="$JOB" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
kubectl -n "$NS" logs "$MP" 2>&1 | grep 'HOT fc' | tail -6 | sed 's/^/  /' || true
if [ -s "$OUT" ]; then
  log "RESULT saved -> $OUT ($(wc -c <"$OUT") bytes)"
else
  log "NO RESULT_JSON (see the log above)"
fi
kubectl -n "$NS" delete job "$JOB" --wait=false >/dev/null 2>&1 || true
kubectl -n "$NS" delete configmap geofleet-code --wait=false >/dev/null 2>&1 || true
log "done."
