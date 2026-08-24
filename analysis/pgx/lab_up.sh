#!/bin/sh
# XPROTO-PGX lab: primary (wal_level=logical, pg_stat_statements) + ASYNC
# replica (NO apply-delay). Emergent WAN lag = netem on the PRIMARY's
# egress FILTERED to the replica IP (delays the WAL stream primary->
# replica; does NOT throttle client writes, which go to the docker
# gateway not the replica). Mirrors the proven XPROTO-PG lab; adds
# pg_stat_statements, two consumer roles, and the filtered netem.
# Idempotent. netem needs tc via a netshoot sidecar in the primary netns.
set -e
NETEM_DELAY=${NETEM_DELAY:-300ms}
NETEM_JITTER=${NETEM_JITTER:-120ms}

docker rm -f pgx-p pgx-r >/dev/null 2>&1 || true
docker network rm pgxnet >/dev/null 2>&1 || true
docker network create pgxnet >/dev/null

# --- primary ---
docker run -d --name pgx-p --network pgxnet -p 127.0.0.1:55445:5432 \
  -e POSTGRES_PASSWORD=lab postgres:16-alpine \
  -c wal_level=logical -c max_wal_senders=5 -c max_replication_slots=5 \
  -c shared_preload_libraries=pg_stat_statements >/dev/null
for i in $(seq 1 60); do
  docker exec pgx-p pg_isready -U postgres >/dev/null 2>&1 && break; sleep 1
done
# hba: replication + all logins (lab) from the subnet, appended BEFORE
# basebackup so the replica inherits it; then roles + extension.
docker exec pgx-p sh -c "printf 'host replication all all trust\nhost all all all trust\n' >> /var/lib/postgresql/data/pg_hba.conf"
docker exec -u postgres pgx-p psql -c 'SELECT pg_reload_conf()' >/dev/null
docker exec -u postgres pgx-p psql -c "CREATE EXTENSION IF NOT EXISTS pg_stat_statements" >/dev/null
docker exec -u postgres pgx-p psql -c "CREATE ROLE consumer_hot LOGIN PASSWORD 'lab'" >/dev/null
docker exec -u postgres pgx-p psql -c "CREATE ROLE consumer_cold LOGIN PASSWORD 'lab'" >/dev/null

# --- replica: basebackup, async, NO apply-delay, pg_stat_statements ---
docker run -d --name pgx-r --network pgxnet -p 127.0.0.1:55446:5432 \
  -u postgres -e PGDATA=/var/lib/postgresql/data postgres:16-alpine sh -c \
  'rm -rf /var/lib/postgresql/data/* && \
   pg_basebackup -h pgx-p -U postgres -D /var/lib/postgresql/data -R -X stream && \
   chmod 700 /var/lib/postgresql/data && \
   exec postgres -c hot_standby=on -c shared_preload_libraries=pg_stat_statements' >/dev/null
for i in $(seq 1 60); do
  docker exec pgx-r pg_isready -U postgres >/dev/null 2>&1 && break; sleep 1
done
sleep 2
docker exec -u postgres pgx-p psql -tc 'SELECT count(*) FROM pg_stat_replication' | grep -q 1 && echo REPL_OK

# --- emergent WAN lag: netem on PRIMARY egress, filtered to replica IP ---
RIP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' pgx-r)
docker run --rm --net container:pgx-p --cap-add NET_ADMIN nicolaka/netshoot sh -c "
  tc qdisc add dev eth0 root handle 1: prio &&
  tc qdisc add dev eth0 parent 1:3 handle 30: netem delay $NETEM_DELAY $NETEM_JITTER distribution normal &&
  tc filter add dev eth0 protocol ip parent 1:0 prio 3 u32 match ip dst $RIP/32 flowid 1:3
" && echo "NETEM_OK $NETEM_DELAY +/- $NETEM_JITTER primary->replica ($RIP)" \
  || echo "NETEM_FAIL (no emergent lag — cell will VOID on MC1/MC3)"
echo LAB_READY
