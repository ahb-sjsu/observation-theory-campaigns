#!/bin/bash
# OP4 probe on one D8 pilot world (owner, 2026-10-12): the gram part, then GRAM's nudging on both test trajectories
cd /archive/ahb-sjsu/observation-theory-campaigns/experiments/OP/OP4
W=p_nu030_n96; PY=/home/claude/env/bin/python; C=../../OD/D8/prereg_config.json
$PY -u op4_gram.py --config $C --op4 op4_config.json --seed-role pilot --world $W --part gram --cache gram > probe_${W}_gram.log 2>&1 || exit 1
$PY -u op4_gram.py --config $C --op4 op4_config.json --seed-role pilot --world $W --part nudge --tests 0 --recheck-ball --cache gram --out probe_${W}_t0.json > probe_${W}_t0.log 2>&1 &
$PY -u op4_gram.py --config $C --op4 op4_config.json --seed-role pilot --world $W --part nudge --tests 1 --cache gram --out probe_${W}_t1.json > probe_${W}_t1.log 2>&1 &
wait
