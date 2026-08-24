#!/usr/bin/env bash
# Tear down the XPROTO-ZK ensemble.
for i in 1 2 3; do docker rm -f "zk$i" >/dev/null 2>&1 || true; done
docker network rm zknet >/dev/null 2>&1 || true
echo "zk lab torn down"
