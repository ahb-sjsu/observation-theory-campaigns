#!/usr/bin/env bash
# XPROTO-MG lab: mongo:7 replica set rs0 = primary + DELAYED secondary
# (secondaryDelaySecs=1, priority 0). The delayed member is the analog
# of the PG cell's recovery_min_apply_delay=1000ms. Idempotent.
set -euo pipefail

IMG=mongo:7
docker rm -f mongo-p mongo-s >/dev/null 2>&1 || true
docker network create mgnet >/dev/null 2>&1 || true

docker run -d --name mongo-p --network mgnet -p 55437:27017 \
  "$IMG" --replSet rs0 --oplogSize 128 >/dev/null
docker run -d --name mongo-s --network mgnet -p 55438:27017 \
  "$IMG" --replSet rs0 --oplogSize 128 >/dev/null

echo "waiting for mongod on both nodes…"
for n in mongo-p mongo-s; do
  for i in $(seq 1 60); do
    if docker exec "$n" mongosh --quiet --eval 'db.runCommand({ping:1}).ok' \
         >/dev/null 2>&1; then break; fi
    sleep 1
  done
done

echo "initiating replica set (delayed secondary)…"
docker exec mongo-p mongosh --quiet --eval '
rs.initiate({_id:"rs0", members:[
  {_id:0, host:"mongo-p:27017", priority:2},
  {_id:1, host:"mongo-s:27017", priority:0, secondaryDelaySecs:1, votes:1}
]})'

echo "waiting for PRIMARY…"
for i in $(seq 1 90); do
  S=$(docker exec mongo-p mongosh --quiet --eval \
        'try{rs.status().myState}catch(e){0}' 2>/dev/null || echo 0)
  [ "$S" = "1" ] && { echo "lab up (primary elected)"; exit 0; }
  sleep 1
done
echo "ERROR: primary not elected in time" >&2
exit 1
