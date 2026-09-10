#!/bin/bash
export OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8
cd /archive/ahb-sjsu/observation-theory-campaigns/experiments/OD/D6v2 || exit 1
echo "== probe start $(date)"
/home/claude/env/bin/python3 -u d6v2_placement.py --config prereg_config.json --seed-role probe --out probe.json 2>&1 | tee probe.log
echo "== PROBE_DONE"
echo "== pilot start $(date)"
/home/claude/env/bin/python3 -u d6v2_placement.py --config prereg_config.json --seed-role pilot --out pilot.json 2>&1 | tee pilot.log
echo "== PILOT_DONE"
