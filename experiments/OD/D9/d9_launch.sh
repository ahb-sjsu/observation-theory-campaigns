#!/bin/bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd /archive/ahb-sjsu/observation-theory-campaigns/experiments/OD/D9 || exit 1
PY=/home/claude/env/bin/python3
ROLE=${1:-selftest}
if [ "$ROLE" = selftest ]; then $PY -u d9_barrier.py --selftest 2>&1; echo "== SELFTEST_DONE rc=$?"; exit 0; fi
echo "the probe, pilot and run go to NRP through a submitter (not yet written); refusing to compute on Atlas"; exit 2
