"""ESA's split-half stability against training length (SEALED-RUN-PLAN.md Section 4, the PROBE item). READ-blind: it
looks only at the agreement of ESA with itself, never at any nudging result or at READ.

    python esa_stability.py p_nu030_n96 80,320,1280
"""
import json
import sys

import numpy as np

from op_variants import esa_scores, initial_field, spin_up, training_samples, world_model

world_name, sizes = sys.argv[1], [int(x) for x in sys.argv[2].split(",")]
cfg8 = json.load(open("../../OD/D8/prereg_config.json", encoding="utf-8")); world = next(w for w in cfg8["worlds"] if w["name"] == world_name)
cfg = {**cfg8, **world.get("overrides", {})}; model, cand, dt = world_model(world, cfg); off = int(world["seed_offset"])
rng = np.random.default_rng(int(cfg["seed_pilot_train"]) + off); uh = spin_up(model, initial_field(model, rng, int(cfg["ic_kmax"]), float(cfg["omega_rms"])), float(cfg["T_spin"]), dt)
per = int(round(float(cfg["dt_sample"]) / dt)); W, _ = training_samples(model, uh, max(sizes), per, dt)
rank = lambda x: np.argsort(np.argsort(-x))
for n in sizes:
    a, b = esa_scores(model, W[: n // 2], cand), esa_scores(model, W[n // 2: n], cand); full = esa_scores(model, W[:n], cand)
    sp_all = float(np.corrcoef(rank(a), rank(b))[0, 1])
    top = np.union1d(np.argsort(-a)[:64], np.argsort(-b)[:64]); sp_top = float(np.corrcoef(rank(a)[top], rank(b)[top])[0, 1])
    ov = {k: len(set(np.argsort(-a)[:k]) & set(np.argsort(-b)[:k])) for k in (8, 24, 48)}
    print(json.dumps({"world": world_name, "samples": n, "spearman_all_pairs": round(sp_all, 3), "spearman_top64_union": round(sp_top, 3), "halves_top_k_overlap": ov,
                      "full_first12_kmag": [round(float(cand.kmag[i]), 2) for i in np.argsort(-full)[:12]]}), flush=True)
