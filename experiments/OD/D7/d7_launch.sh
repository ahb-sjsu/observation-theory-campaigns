#!/bin/bash
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4
cd /archive/ahb-sjsu/observation-theory-campaigns/experiments/OD/D7 || exit 1
ROLE=${1:-pilot}; OUT=$ROLE.json
[ "$ROLE" = selftest ] && { /home/claude/env/bin/python3 -u d7_closure.py --selftest 2>&1; echo "== SELFTEST_DONE rc=$?"; exit 0; }
[ "$ROLE" = run ] && OUT=results.json
echo "== start $(date) HEAD $(git rev-parse --short HEAD) role $ROLE seal $(git hash-object PREREG-D7.md 2>/dev/null)"
/home/claude/env/bin/python3 -u d7_closure.py --config prereg_config.json --seed-role $ROLE --out $OUT 2>&1
echo "== ${ROLE^^}_DONE rc=$?"
