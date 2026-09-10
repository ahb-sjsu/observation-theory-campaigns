#!/bin/bash
export OMP_NUM_THREADS=2
cd /archive/ahb-sjsu/observation-theory-campaigns/experiments/OD/D1v2 || exit 1
ROLE=${1:-pilot}; OUT=pilot.json; [ "$ROLE" = run ] && OUT=results.json
echo "== start $(date) HEAD $(git rev-parse --short HEAD) role $ROLE seal $(git hash-object PREREG-D1V2.md 2>/dev/null)"
/home/claude/env/bin/python3 -u d1_identify.py --config prereg_config.json --seed-role $ROLE --out $OUT 2>&1
echo "== ${ROLE^^}_DONE rc=$?"
