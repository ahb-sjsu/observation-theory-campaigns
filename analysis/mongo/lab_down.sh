#!/usr/bin/env bash
# Tear down the XPROTO-MG lab.
set -uo pipefail
docker rm -f mongo-p mongo-s >/dev/null 2>&1 || true
docker network rm mgnet >/dev/null 2>&1 || true
echo "lab down"
