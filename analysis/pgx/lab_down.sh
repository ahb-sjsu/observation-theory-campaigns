#!/usr/bin/env bash
# Tear down the XPROTO-PGX lab.
set -u
docker rm -f pgx-p pgx-r >/dev/null 2>&1 || true
docker network rm pgxnet >/dev/null 2>&1 || true
echo "lab down"
