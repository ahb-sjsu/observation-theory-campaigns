#!/usr/bin/env bash
# XPROTO-ZK-FLIP lab: a 3-node ZooKeeper ensemble on Atlas with TWO netem
# profiles, one per follower. The flip needs two independent staleness axes:
#   fast follower (50 ms commit-stream delay)  -> lag small, churn dominates
#   slow follower (400 ms commit-stream delay) -> lag dominates
# Same mechanism as lab_up.sh (delay the Zab commit stream on the LEADER's
# egress toward each follower's IP; client reads never traverse the leader).
#
#   bash lab_up_flip.sh [fast_ms] [slow_ms]     # defaults 50 400
# Writes /home/claude/zk/topology_flip.json.
set -uo pipefail
NET=zknet
IMG=zookeeper:3.9
FAST_MS=${1:-50}
SLOW_MS=${2:-400}
SERVERS="server.1=zk1:2888:3888;2181 server.2=zk2:2888:3888;2181 server.3=zk3:2888:3888;2181"

docker network create "$NET" >/dev/null 2>&1 || true
for i in 1 2 3; do
  docker rm -f "zk$i" >/dev/null 2>&1 || true
  docker run -d --name "zk$i" --network "$NET" --cap-add NET_ADMIN \
    -p $((2180+i)):2181 \
    -e ZOO_MY_ID="$i" -e ZOO_SERVERS="$SERVERS" \
    -e ZOO_4LW_COMMANDS_WHITELIST='*' "$IMG" >/dev/null
done

echo "waiting for leader election..."
sleep 20
LEADER=""; FOLLOWERS=()
for i in 1 2 3; do
  m=$(docker exec "zk$i" zkServer.sh status 2>/dev/null | grep -oiE 'leader|follower' | head -1)
  echo "  zk$i  port $((2180+i))  mode=${m:-?}"
  [ "$m" = "leader" ]   && LEADER=$i
  [ "$m" = "follower" ] && FOLLOWERS+=("$i")
done
if [ -z "$LEADER" ] || [ "${#FOLLOWERS[@]}" -ne 2 ]; then
  echo "ELECTION INCOMPLETE -- aborting"; exit 1
fi
FAST=${FOLLOWERS[0]}; SLOW=${FOLLOWERS[1]}
echo "LEADER=zk$LEADER  FAST=zk$FAST(+${FAST_MS}ms)  SLOW=zk$SLOW(+${SLOW_MS}ms)"

FIP=$(docker inspect -f '{{.NetworkSettings.Networks.zknet.IPAddress}}' "zk$FAST")
SIP=$(docker inspect -f '{{.NetworkSettings.Networks.zknet.IPAddress}}' "zk$SLOW")
docker exec "zk$LEADER" bash -c \
  "apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq iproute2 >/dev/null 2>&1; \
   tc qdisc del dev eth0 root 2>/dev/null || true; \
   tc qdisc add dev eth0 root handle 1: prio bands 4; \
   tc qdisc add dev eth0 parent 1:3 handle 30: netem delay ${FAST_MS}ms; \
   tc qdisc add dev eth0 parent 1:4 handle 40: netem delay ${SLOW_MS}ms; \
   tc filter add dev eth0 parent 1:0 protocol ip u32 match ip dst ${FIP}/32 flowid 1:3; \
   tc filter add dev eth0 parent 1:0 protocol ip u32 match ip dst ${SIP}/32 flowid 1:4" \
  && echo "netem: leader->zk$FAST ${FAST_MS}ms, leader->zk$SLOW ${SLOW_MS}ms"

mkdir -p /home/claude/zk
cat > /home/claude/zk/topology_flip.json <<JSON
{"leader_port": $((2180+LEADER)), "fast_port": $((2180+FAST)),
 "slow_port": $((2180+SLOW)), "fast_ms": ${FAST_MS}, "slow_ms": ${SLOW_MS}}
JSON
echo "wrote topology_flip.json:"; cat /home/claude/zk/topology_flip.json
