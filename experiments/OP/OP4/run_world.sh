#!/bin/bash
# OP4 on one D8 pilot world (owner, 2026-10-12: confirm the probe's reading on the other three worlds):
# the gram part, then GRAM's nudging on both test trajectories in parallel. Usage: run_world.sh <world>
cd /archive/ahb-sjsu/observation-theory-campaigns/experiments/OP/OP4
W=$1; PY=/home/claude/env/bin/python; C=../../OD/D8/prereg_config.json
$PY -u op4_gram.py --config $C --op4 op4_config.json --seed-role pilot --world $W --part gram --cache gram > pilot_${W}_gram.log 2>&1 || exit 1
$PY -u op4_gram.py --config $C --op4 op4_config.json --seed-role pilot --world $W --part nudge --tests 0 --cache gram --out pilot_${W}_t0.json > pilot_${W}_t0.log 2>&1 &
$PY -u op4_gram.py --config $C --op4 op4_config.json --seed-role pilot --world $W --part nudge --tests 1 --cache gram --out pilot_${W}_t1.json > pilot_${W}_t1.log 2>&1 &
wait
