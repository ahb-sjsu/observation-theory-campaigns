#!/bin/bash
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4
cd /archive/ahb-sjsu/observation-theory-campaigns/experiments/OD/D8 || exit 1
PY=/home/claude/env/bin/python3
ROLE=${1:-probe}; OUT=$ROLE.json
if [ "$ROLE" = selftest ]; then
  $PY -u d8_sync.py --selftest 2>&1; echo "== SYNC_SELFTEST rc=$?"
  $PY -u d8_grade.py --selftest 2>&1; echo "== GRADE_SELFTEST rc=$?"
  $PY -u d8_fix_tols.py --selftest 2>&1; echo "== FIXTOLS_SELFTEST rc=$?"
  echo "== SELFTEST_DONE"; exit 0
fi
[ "$ROLE" = run ] && OUT=results.json
echo "== start $(date) HEAD $(git rev-parse --short HEAD) role $ROLE seal $(git hash-object PREREG-D8.md 2>/dev/null)"
$PY -u d8_sync.py --config prereg_config.json --seed-role $ROLE --out $OUT 2>&1
echo "== ${ROLE^^}_DONE rc=$?"
