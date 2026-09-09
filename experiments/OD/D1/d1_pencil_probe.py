"""Pre-seal probe: answers at one radius identify P only up to the pencil P(s) = s P + (1-s) c I,
c = B^2/rho^2; the analytic centre should return the pencil member with the largest s that is
positive semidefinite. Two radii should identify P. Prints errors of the estimate against P and
against the predicted pencil member P*, for one and two radii."""
import sys, json
import numpy as np
from d1_identify import make_operator, queries, oracle, estimate

worlds = json.load(open("prereg_config.json"))["worlds"]
rng = np.random.default_rng(7)
out = []
for w in worlds:
    n = w["n"]; lam0 = np.array(w["spectrum"], float)
    for B in (1.0, 1.5):
        for mode, radii in (("one", (1.0,)), ("two_1.5", (1.0, 1.5)), ("two_0.7", (1.0, 0.7))):
            errs_P = []; errs_Pstar = []; bal = []
            for e in range(4):
                P, lam, V = make_operator(n, w["spectrum"], rng)
                Ds = []; As = []
                for r in radii:
                    D = queries(n, r, 2000 // len(radii), rng); Ds.append(D); As.append(oracle(P, B, D))
                D = np.vstack(Ds); ans = np.concatenate(As)
                bal.append(float(min(ans.mean(), 1 - ans.mean())))
                if ans.all() or (~ans).all():
                    continue
                # estimator takes one rho only for the cap; the answers carry the radii through D
                Ph = estimate(D, ans, B, "CLARABEL", 1000.0, 1.0)
                c = B ** 2 / 1.0 ** 2
                lmin = lam.min()
                s = 1.0 if lmin <= 0 else (c / (c - lmin) if lmin < c else 1.0)
                Pstar = s * P + (1 - s) * c * np.eye(n)
                errs_P.append(np.linalg.norm(Ph - P) / np.linalg.norm(P))
                errs_Pstar.append(np.linalg.norm(Ph - Pstar) / np.linalg.norm(P))
            row = {"world": w["name"], "B": B, "mode": mode, "balance_median": float(np.median(bal)),
                   "n_graded": len(errs_P), "err_vs_P": float(np.median(errs_P)) if errs_P else None,
                   "err_vs_Pstar": float(np.median(errs_Pstar)) if errs_Pstar else None,
                   "s_star": (1.0 if lam0.min() <= 0 else float((B**2) / (B**2 - lam0.min())))}
            print(json.dumps(row)); out.append(row)
json.dump(out, open("pencil_probe.json", "w"), indent=1)
