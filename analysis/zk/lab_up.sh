#!/usr/bin/env bash
# XPROTO-ZK lab: a 3-node ZooKeeper ensemble on Atlas. Staleness is induced by
# a netem delay on the reader's follower (disclosed) -- the coordination-service
# analog of PostgreSQL recovery_min_apply_delay / a MongoDB delayed secondary /
# the geo-fleet Pauser: the follower lags the leader's committed zxid, so a local
# read returns a stale version, which the zxid witness detects. Writes remain
# linearizable through the leader (Zab); only local reads go stale.
#
#   bash lab_up.sh [delay_ms]      # default 200 ms
# Writes /home/claude/zk/topology.json {leader_port, follower_port, delay_ms}.
set -uo pipefail
NET=zknet
IMG=zookeeper:3.9
DELAY_MS=${1:-200}
JITTER_MS=${2:-0}          # optional lag jitter (normal); 0 = fixed delay (the cell)
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
LEADER=""; FOLLOWER=""
for i in 1 2 3; do
  m=$(docker exec "zk$i" zkServer.sh status 2>/dev/null | grep -oiE 'leader|follower' | head -1)
  echo "  zk$i  port $((2180+i))  mode=${m:-?}"
  [ "$m" = "leader" ]   && LEADER=$i
  [ "$m" = "follower" ] && FOLLOWER=$i
done
if [ -z "$LEADER" ] || [ -z "$FOLLOWER" ]; then
  echo "ELECTION INCOMPLETE -- aborting"; exit 1
fi
echo "LEADER=zk$LEADER (port $((2180+LEADER)))  READER_FOLLOWER=zk$FOLLOWER (port $((2180+FOLLOWER)))"

# Induce follower lag by delaying the Zab COMMIT stream (leader -> follower).
# Must be applied on the LEADER's egress toward the follower's IP: tc `root`
# netem shapes egress only, and the follower RECEIVES commits (ingress), so
# delaying the follower's own egress does nothing; and delaying the follower's
# whole link would also slow the client read path, letting it catch up before
# the read lands. Client reads (follower:2181) never traverse the leader, so
# they stay prompt while the follower's applied state lags -> stale local reads.
FIP=$(docker inspect -f '{{.NetworkSettings.Networks.zknet.IPAddress}}' "zk$FOLLOWER")
NETEM="delay ${DELAY_MS}ms"
[ "$JITTER_MS" -gt 0 ] && NETEM="delay ${DELAY_MS}ms ${JITTER_MS}ms distribution normal"
docker exec "zk$LEADER" bash -c \
  "apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq iproute2 >/dev/null 2>&1; \
   tc qdisc del dev eth0 root 2>/dev/null || true; \
   tc qdisc add dev eth0 root handle 1: prio; \
   tc qdisc add dev eth0 parent 1:3 handle 30: netem ${NETEM}; \
   tc filter add dev eth0 parent 1:0 protocol ip u32 match ip dst ${FIP}/32 flowid 1:3" \
  && echo "netem [${NETEM}] on leader zk$LEADER egress -> zk$FOLLOWER ($FIP)"

mkdir -p /home/claude/zk
echo "{\"leader_port\": $((2180+LEADER)), \"follower_port\": $((2180+FOLLOWER)), \"delay_ms\": ${DELAY_MS}}" \
  > /home/claude/zk/topology.json
echo "wrote topology.json:"; cat /home/claude/zk/topology.json
