#!/bin/sh
docker rm -f ngpg-p ngpg-r >/dev/null 2>&1 || true
docker network rm ngpg >/dev/null 2>&1 || true
echo LAB_DOWN
