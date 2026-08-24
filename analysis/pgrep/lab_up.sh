#!/bin/sh
# XPROTO-PG lab: primary (wal_level=logical) + replica (1s apply delay).
# Idempotent; teardown with lab_down.sh. Lessons baked in: replication
# hba line must be appended + reloaded before basebackup; PGDATA needs
# chmod 700 after basebackup (volume mountpoint arrives 0755).
set -e
docker rm -f ngpg-p ngpg-r >/dev/null 2>&1 || true
docker network rm ngpg >/dev/null 2>&1 || true
docker network create ngpg >/dev/null
docker run -d --name ngpg-p --network ngpg -p 127.0.0.1:55433:5432 \
  -e POSTGRES_PASSWORD=lab postgres:16-alpine \
  -c wal_level=logical -c max_wal_senders=5 -c max_replication_slots=5 >/dev/null
for i in $(seq 1 30); do
  docker exec ngpg-p pg_isready -U postgres >/dev/null 2>&1 && break; sleep 1
done
docker exec ngpg-p sh -c \
  "echo 'host replication all all trust' >> /var/lib/postgresql/data/pg_hba.conf"
docker exec -u postgres ngpg-p psql -c 'SELECT pg_reload_conf()' >/dev/null
docker run -d --name ngpg-r --network ngpg -p 127.0.0.1:55434:5432 \
  -u postgres -e PGDATA=/var/lib/postgresql/data postgres:16-alpine sh -c \
  'rm -rf /var/lib/postgresql/data/* && \
   pg_basebackup -h ngpg-p -U postgres -D /var/lib/postgresql/data -R -X stream && \
   chmod 700 /var/lib/postgresql/data && \
   exec postgres -c recovery_min_apply_delay=1000ms -c hot_standby=on' >/dev/null
for i in $(seq 1 40); do
  docker exec ngpg-r pg_isready -U postgres >/dev/null 2>&1 && break; sleep 1
done
sleep 2
docker exec ngpg-p psql -U postgres -tc \
  'SELECT count(*) FROM pg_stat_replication' | grep -q 1 && echo LAB_READY
