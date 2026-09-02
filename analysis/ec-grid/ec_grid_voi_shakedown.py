#!/usr/bin/env python3
"""EC-grid shakedown (UNSEALED, exploratory) -- consumer-relative sensor value
on a transmission network (owner idea 2026-09-02).

Paper VIII's rank-one value-of-observation identity (Lean-verified;
V_C = (g^T S h)^2 / (h^T S h + r)) instantiated on the New England 39-bus
system under DC-linear WLS state estimation. The empirical question is
TOPOLOGY-DEPENDENT, not algebraic: does a real grid produce candidate sensors
that are near-equal in classical value (trace reduction) yet differ by
multiples in value to a specific operational consumer -- and do different
consumers order the sensors oppositely?

Substrate: pandapower case39 -> DC model (branch susceptances from the ppc
branch reactances; slack = ext_grid bus, reduced state theta in R^{n-1}).
Base measurement set (pinned): P injections at ALL buses (sigma 0.05 pu) +
flows on 10 seeded branches (sigma 0.02) -- observable, with meaningful
uncertainty structure. Sigma = (H^T R^-1 H)^-1.

Candidates (84): every branch flow measurement (sigma 0.01) and every non-slack
bus angle PMU (sigma 0.005 rad).

Consumers (rank-one, chosen MECHANICALLY from the base case, no discretion):
  C_thermal   g = flow row of the branch with max |P| at the DC base case
  C_interface g = theta_i - theta_j for the generator-bus pair with max
                  base-case angle separation (stability proxy)
  C_local     g = flow row of the branch with min |P| (a consumer no
                  contingency cares about -- the contrast arm)

PRE-STATED PREDICTIONS (graded after the run, disclosed either way):
  P1 divergence: Spearman(dtr, V_thermal) <= 0.5 over the 84 candidates
     (classical value is a poor proxy for operational value).
  P2 dissociation pair: there exist candidates a,b with dtr within 10% of
     each other and V_thermal ratio >= 5x.
  P3 inversion: the top-5 candidate sets by V_thermal and by V_interface are
     disjoint, and Spearman(V_thermal, V_interface) <= 0.5 -- no
     consumer-independent sensor ranking.
  P4 validation: 4000-draw Monte Carlo -- realized reduction in the thermal
     consumer's squared error under the best thermal candidate matches the
     rank-one V_C within 5% relative (pipeline exactness check).
  P5 isotropic control: P_C = I ranking reproduces the dtr ranking
     (Spearman >= 0.999).

Output: ~/ec-grid/ec_grid_voi_result.json
"""

import json
import os

import numpy as np

HERE = os.path.expanduser("~/ec-grid")
SEED = 0
SIG_INJ, SIG_FLOW_BASE, SIG_FLOW_CAND, SIG_PMU = 0.05, 0.02, 0.01, 0.005
N_BASE_FLOWS = 10
MC_DRAWS = 4000


def dc_model():
    import pandapower as pp
    import pandapower.networks as pn
    net = pn.case39()
    pp.rundcpp(net)
    ppc = net._ppc   # pandapower 3.x: PYPOWER arrays live on the net after rundcpp
    branch = ppc["branch"].real
    f = branch[:, 0].astype(int)
    t = branch[:, 1].astype(int)
    x = branch[:, 3]
    b = 1.0 / x
    n = ppc["bus"].shape[0]
    slack = int(np.where(ppc["bus"][:, 1] == 3)[0][0])
    A = np.zeros((len(f), n))
    A[np.arange(len(f)), f] = 1.0
    A[np.arange(len(f)), t] = -1.0
    Bf = (b[:, None] * A)
    keep = [i for i in range(n) if i != slack]
    Bf_r = Bf[:, keep]
    # base-case flows and angles for the mechanical consumer choices
    theta = ppc["bus"][:, 8].real * np.pi / 180.0
    flows = Bf @ theta
    gen_buses = sorted(set(ppc["gen"][:, 0].real.astype(int)))
    return {"n": n, "slack": slack, "keep": keep, "Bf_r": Bf_r,
            "A": A, "b": b, "f": f, "t": t, "flows": flows,
            "theta": theta, "gen_buses": gen_buses}


def main():
    os.makedirs(HERE, exist_ok=True)
    from scipy.stats import spearmanr
    rng = np.random.default_rng(SEED)
    m = dc_model()
    nbr, nred = m["Bf_r"].shape[0], m["Bf_r"].shape[1]
    print(f"[grid] case39: {m['n']} buses, {nbr} branches, slack={m['slack']}, "
          f"state dim {nred}", flush=True)

    # base measurement set: all injections + 10 seeded branch flows
    Binj = ((m["A"].T * m["b"]) @ m["A"])[:, m["keep"]]   # n x nred (row per bus)
    H_rows = [Binj[i] for i in range(m["n"])]
    R_diag = [SIG_INJ ** 2] * m["n"]
    base_flow_idx = rng.choice(nbr, N_BASE_FLOWS, replace=False)
    for i in base_flow_idx:
        H_rows.append(m["Bf_r"][i])
        R_diag.append(SIG_FLOW_BASE ** 2)
    H = np.array(H_rows)
    Rinv = np.diag(1.0 / np.array(R_diag))
    G = H.T @ Rinv @ H
    S = np.linalg.inv(G)          # Sigma, symmetric by construction
    S = 0.5 * (S + S.T)
    print(f"[grid] base set: {H.shape[0]} measurements, tr(Sigma)={np.trace(S):.4e}",
          flush=True)

    # consumers, mechanically
    order = np.argsort(-np.abs(m["flows"]))
    l_max, l_min = int(order[0]), int(order[-1])
    g_th = m["Bf_r"][l_max].copy()
    g_lo = m["Bf_r"][l_min].copy()
    gb = m["gen_buses"]
    seps = [(abs(m["theta"][i] - m["theta"][j]), i, j)
            for ii, i in enumerate(gb) for j in gb[ii + 1:]]
    _, bi, bj = max(seps)
    e = np.zeros(nred)
    kidx = {b: k for k, b in enumerate(m["keep"])}
    if bi in kidx:
        e[kidx[bi]] += 1.0
    if bj in kidx:
        e[kidx[bj]] -= 1.0
    g_if = e
    print(f"[grid] consumers: thermal=branch {l_max} (|P|={abs(m['flows'][l_max]):.2f}), "
          f"interface=buses {bi}-{bj}, local=branch {l_min} "
          f"(|P|={abs(m['flows'][l_min]):.4f})", flush=True)

    # candidates: every branch flow + every non-slack bus angle
    cands = []
    for i in range(nbr):
        cands.append((f"flow_{i}", m["Bf_r"][i], SIG_FLOW_CAND ** 2))
    for k, bus in enumerate(m["keep"]):
        h = np.zeros(nred)
        h[k] = 1.0
        cands.append((f"pmu_{bus}", h, SIG_PMU ** 2))

    def score(h, r, g):
        return float((g @ S @ h) ** 2 / (h @ S @ h + r))

    rows = []
    for name, h, r in cands:
        den = h @ S @ h + r
        dtr = float((S @ h) @ (S @ h) / den)
        rows.append({"name": name, "dtr": dtr,
                     "V_thermal": score(h, r, g_th),
                     "V_interface": score(h, r, g_if),
                     "V_local": score(h, r, g_lo),
                     "V_iso": dtr})
    dtr = np.array([r["dtr"] for r in rows])
    vth = np.array([r["V_thermal"] for r in rows])
    vif = np.array([r["V_interface"] for r in rows])

    # P1
    p1 = float(spearmanr(dtr, vth).statistic)
    # P2: best dissociation pair
    best = None
    for a in range(len(rows)):
        for bIdx in range(len(rows)):
            if a == bIdx or vth[bIdx] <= 0 or dtr[bIdx] <= 0:
                continue
            if abs(dtr[a] / dtr[bIdx] - 1) <= 0.10:
                ratio = vth[a] / max(vth[bIdx], 1e-18)
                if best is None or ratio > best[0]:
                    best = (float(ratio), rows[a]["name"], rows[bIdx]["name"],
                            float(dtr[a]), float(dtr[bIdx]),
                            float(vth[a]), float(vth[bIdx]))
    # P3
    top_th = set(np.argsort(-vth)[:5])
    top_if = set(np.argsort(-vif)[:5])
    p3_disjoint = len(top_th & top_if) == 0
    p3_rho = float(spearmanr(vth, vif).statistic)
    # P5
    p5 = float(spearmanr(dtr, [r["V_iso"] for r in rows]).statistic)

    # P4: MC validation on the best thermal candidate
    bi_ = int(np.argmax(vth))
    name_b, h_b, r_b = cands[bi_]
    den = h_b @ S @ h_b + r_b
    K = (S @ h_b) / den
    Spost = S - np.outer(K, h_b @ S)
    pred = vth[bi_]
    L = np.linalg.cholesky(S + 1e-12 * np.eye(nred))
    xerr = (L @ rng.standard_normal((nred, MC_DRAWS)))
    v = rng.standard_normal(MC_DRAWS) * np.sqrt(r_b)
    y = h_b @ xerr + v
    xpost = xerr - np.outer(K, y)
    mse_pre = float(np.mean((g_th @ xerr) ** 2))
    mse_post = float(np.mean((g_th @ xpost) ** 2))
    realized = mse_pre - mse_post
    p4_rel = abs(realized - pred) / pred

    verdicts = {
        "P1_divergence": {"spearman_dtr_vthermal": p1, "pass": bool(p1 <= 0.5)},
        "P2_dissociation_pair": {"ratio": best[0], "a": best[1], "b": best[2],
                                 "dtr_a": best[3], "dtr_b": best[4],
                                 "Vth_a": best[5], "Vth_b": best[6],
                                 "pass": bool(best[0] >= 5.0)},
        "P3_inversion": {"top5_disjoint": bool(p3_disjoint),
                         "spearman_vth_vif": p3_rho,
                         "pass": bool(p3_disjoint and p3_rho <= 0.5)},
        "P4_mc_validation": {"predicted": float(pred), "realized": realized,
                             "rel_err": float(p4_rel), "candidate": name_b,
                             "pass": bool(p4_rel <= 0.05)},
        "P5_iso_control": {"spearman": p5, "pass": bool(p5 >= 0.999)},
    }
    for k, v_ in verdicts.items():
        print(f"[grade] {k}: {v_}", flush=True)

    out = {"seed": SEED, "case": "case39 DC", "n_candidates": len(cands),
           "consumers": {"thermal_branch": l_max, "interface_buses": [bi, bj],
                         "local_branch": l_min},
           "base_tr_sigma": float(np.trace(S)),
           "verdicts": verdicts, "candidates": rows}
    def np_safe(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        raise TypeError(type(o))

    with open(os.path.join(HERE, "ec_grid_voi_result.json"), "w") as fjs:
        json.dump(out, fjs, indent=2, default=np_safe)
    print(f"wrote {HERE}/ec_grid_voi_result.json", flush=True)


if __name__ == "__main__":
    main()
