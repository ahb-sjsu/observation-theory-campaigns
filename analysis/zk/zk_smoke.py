"""Smoke test: confirm a local follower read goes stale under write load and
the zxid witness detects it; confirm sync() repairs it. Verifies the kazoo API
before writing the cell."""
import json
import os
import time

from kazoo.client import KazooClient

topo = json.load(open("/home/claude/zk/topology.json"))
leader = KazooClient(hosts=f"localhost:{topo['leader_port']}")
foll = KazooClient(hosts=f"localhost:{topo['follower_port']}")
leader.start(); foll.start()
leader.ensure_path("/z")

# a burst of writes on a hot znode, spaced under the netem delay
for i in range(30):
    leader.set("/z", str(i).encode())
    time.sleep(0.01)                       # 300 ms of writes vs 200 ms follower lag

dL, sL = leader.get("/z")
dF, sF = foll.get("/z")                     # local (delayed-follower) read
print(f"leader:   val={dL.decode():>3} mzxid={sL.mzxid}")
print(f"follower: val={dF.decode():>3} mzxid={sF.mzxid}  (stale={sF.mzxid < sL.mzxid})")
print(f"zxid gap (witness) = {sL.mzxid - sF.mzxid}")

foll.sync("/z"); time.sleep(0.3)           # the deployed freshness barrier
dF2, sF2 = foll.get("/z")
print(f"follower after sync(): val={dF2.decode():>3} mzxid={sF2.mzxid}  "
      f"(caught up={sF2.mzxid >= sL.mzxid})")

leader.stop(); foll.stop()
