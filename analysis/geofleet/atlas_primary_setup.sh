#!/usr/bin/env bash
# Geo-fleet Phase 2 — stand up the PUBLIC Atlas primary the NRP replicas
# cascade from. Runs ON ATLAS (docker), when Atlas is reachable. Exposes
# Postgres with TLS + a replication-only role; NRP pods connect OUT to
# atlas-sjsu.duckdns.org:$PORT (no inbound to NRP, no tailscale-in-pod).
#
# NOTE: opening the port to the internet (firewall / duckdns / port
# forward) is an Atlas-admin step done OUTSIDE this script. Keep the
# replicator password out of git; pass it in the environment.
set -euo pipefail

PORT="${PORT:-5444}"
REPL_USER="${REPL_USER:-fleet_replicator}"
REPL_PW="${REPL_PW:?set REPL_PW in the environment (do not commit it)}"
NAME="${NAME:-geofleet-primary}"
VOL="${VOL:-geofleet-pgdata}"

docker volume create "$VOL" >/dev/null 2>&1 || true
docker rm -f "$NAME" >/dev/null 2>&1 || true

# self-signed cert for TLS (replace with a real cert for anything lasting)
docker run -d --name "$NAME" -p "${PORT}:5432" -v "$VOL:/var/lib/postgresql/data" \
  -e POSTGRES_PASSWORD="$REPL_PW" postgres:16-alpine \
  -c wal_level=replica -c max_wal_senders=10 -c max_replication_slots=10 \
  -c ssl=on \
  -c ssl_cert_file=/var/lib/postgresql/data/server.crt \
  -c ssl_key_file=/var/lib/postgresql/data/server.key \
  -c shared_preload_libraries=pg_stat_statements >/dev/null

for i in $(seq 1 30); do docker exec "$NAME" pg_isready -U postgres >/dev/null 2>&1 && break; sleep 1; done

docker exec "$NAME" sh -c '
  cd "$PGDATA"
  if [ ! -f server.crt ]; then
    openssl req -new -x509 -days 365 -nodes -subj "/CN=atlas-sjsu.duckdns.org" \
      -keyout server.key -out server.crt
    chmod 600 server.key; chown postgres:postgres server.key server.crt
  fi'
docker exec "$NAME" psql -U postgres -c \
  "DO \$\$ BEGIN IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname='${REPL_USER}') THEN
     CREATE ROLE ${REPL_USER} REPLICATION LOGIN PASSWORD '${REPL_PW}'; END IF; END \$\$;"
docker exec "$NAME" sh -c \
  "grep -q '${REPL_USER}' \$PGDATA/pg_hba.conf || \
   echo 'hostssl replication ${REPL_USER} 0.0.0.0/0 scram-sha-256' >> \$PGDATA/pg_hba.conf"
docker exec "$NAME" psql -U postgres -c 'SELECT pg_reload_conf()' >/dev/null
docker restart "$NAME" >/dev/null   # ssl=on needs a restart

echo "primary up on :${PORT}, TLS on, replication role ${REPL_USER}."
echo "Next (in the ssu-atlas-ai namespace, when NRP reachable):"
echo "  kubectl -n ssu-atlas-ai create secret generic geofleet-repl \\"
echo "    --from-literal=password='<REPL_PW>'"
echo "Then open the port to the internet (Atlas firewall/duckdns) and submit replicas."
