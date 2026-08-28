"""flip_theorem_checks.py -- verification companion to formal-core.tex.

Every number quoted in formal-core.tex is printed by this script.
Checks T1-T7; each prints PASS or FAIL. Exit code 0 iff all pass.

Run:  python flip_theorem_checks.py
Deps: numpy (scipy.stats.norm used if available, math.erf fallback).
"""

import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
QOT_JSON = os.path.join(REPO, "analysis", "qot", "QOTFLIPREP-graded-raw.json")
CSI_JSON = os.path.join(REPO, "analysis", "csi", "CSIFLIPREP-graded-raw.json")

try:
    from scipy.stats import norm

    def Phi(x):
        return float(norm.cdf(x))

    PHI_SOURCE = "scipy.stats.norm"
except ImportError:  # fallback, identical to double precision

    def Phi(x):
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

    PHI_SOURCE = "math.erf"


def phi(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


RESULTS = []


def check(name, ok, detail=""):
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {name}" + (f"  {detail}" if detail else ""))
    RESULTS.append((name, ok))
    return ok


def lam_star(d1, d2):
    """Crossover weight lambda* = dR2/(dR2-dR1); lambda is the class-1 weight."""
    return d2 / (d2 - d1)


# ----------------------------------------------------------------------
# T1  Midpoint error constant: |dR - grad R(mbar)^T d| <= (L/4)||d||^2.
#     The constant is 1/4, not 1/8. Quadratics: error exactly 0.
#     Near-tightness: the V-derivative instance attains the bound.
# ----------------------------------------------------------------------
def t1():
    print("\n== T1: midpoint bound, constant 1/4 ==")
    rng = np.random.default_rng(20260827)
    ok = True

    # (i) quadratics: midpoint estimate is EXACT (error ~ 0), bound holds.
    max_quad_err = 0.0
    for _ in range(400):
        n = int(rng.integers(1, 7))
        A = rng.normal(size=(n, n))
        H = 0.5 * (A + A.T)
        b = rng.normal(size=n)
        L = float(np.linalg.norm(H, 2))
        mB = rng.normal(size=n)
        d = rng.normal(size=n)
        d *= rng.uniform(0.1, 1.0) / max(np.linalg.norm(d), 1e-12)
        mA = mB + d
        mbar = mB + 0.5 * d

        def R(m):
            return 0.5 * float(m @ H @ m) + float(b @ m)

        dR = R(mA) - R(mB)
        g = float((H @ mbar + b) @ d)
        err = abs(dR - g)
        bound = (L / 4.0) * float(d @ d)
        max_quad_err = max(max_quad_err, err)
        ok &= err <= bound + 1e-12
    ok &= max_quad_err < 1e-10
    print(f"  quadratics (400 trials): max midpoint error = {max_quad_err:.2e}"
          " (exact: midpoint rule integrates linear f' exactly)")

    # (ii) Gaussian shortfall R(m) = Phi((tau - w^T m)/sigma).
    #      Hess = -z*pdf(z) w w^T / sigma^2 ; L = pdf(1) ||w||^2 / sigma^2.
    max_ratio_g = 0.0
    for _ in range(400):
        n = int(rng.integers(1, 7))
        w = rng.normal(size=n)
        sigma = float(rng.uniform(0.5, 3.0))
        tau = float(rng.normal())
        L = phi(1.0) * float(w @ w) / sigma**2
        mB = rng.normal(size=n)
        d = rng.normal(size=n)
        d *= rng.uniform(0.1, 2.0) / max(np.linalg.norm(d), 1e-12)
        mA = mB + d
        mbar = mB + 0.5 * d

        def R(m):
            return Phi((tau - float(w @ m)) / sigma)

        dR = R(mA) - R(mB)
        z = (tau - float(w @ mbar)) / sigma
        g = -phi(z) * float(w @ d) / sigma
        err = abs(dR - g)
        bound = (L / 4.0) * float(d @ d)
        if bound > 0:
            max_ratio_g = max(max_ratio_g, err / bound)
        ok &= err <= bound + 1e-12
    print(f"  Gaussian shortfall (400 trials): max error/bound = {max_ratio_g:.4f} (<= 1)")

    # (iii) sin mixtures, L = sum |a_i| ||b_i||^2.
    max_ratio_s = 0.0
    for _ in range(400):
        n = int(rng.integers(1, 5))
        k = int(rng.integers(1, 4))
        a = rng.normal(size=k)
        B = rng.normal(size=(k, n))
        c = rng.normal(size=k)
        L = float(sum(abs(a[i]) * float(B[i] @ B[i]) for i in range(k)))
        mB = rng.normal(size=n)
        d = rng.normal(size=n)
        d *= rng.uniform(0.1, 1.5) / max(np.linalg.norm(d), 1e-12)
        mA = mB + d
        mbar = mB + 0.5 * d

        def R(m):
            return float(sum(a[i] * math.sin(float(B[i] @ m) + c[i]) for i in range(k)))

        dR = R(mA) - R(mB)
        g = float(sum(a[i] * math.cos(float(B[i] @ mbar) + c[i]) * float(B[i] @ d)
                      for i in range(k)))
        err = abs(dR - g)
        bound = (L / 4.0) * float(d @ d)
        if bound > 0:
            max_ratio_s = max(max_ratio_s, err / bound)
        ok &= err <= bound + 1e-12
    print(f"  sin mixtures (400 trials): max error/bound = {max_ratio_s:.4f} (<= 1)")

    # (iv) tightness witness: R(x) = (L0/2)(x-c)|x-c|, grad Lipschitz L0,
    #      segment centred at c. Error = (L0/4)||d||^2 EXACTLY: ratio 1.
    L0, c, h = 1.7, 0.3, 0.45
    xB, xA = c - h, c + h
    d1 = xA - xB

    def RV(x):
        return 0.5 * L0 * (x - c) * abs(x - c)

    dR = RV(xA) - RV(xB)
    g = L0 * abs(c - c) * d1  # R'(c) = 0
    err = abs(dR - g)
    b14 = (L0 / 4.0) * d1 * d1
    b18 = (L0 / 8.0) * d1 * d1
    print(f"  V-instance: error = {err:.6f}, (L/4)||d||^2 = {b14:.6f}, "
          f"ratio = {err / b14:.6f}")
    print(f"  V-instance vs the 1/8 constant: (L/8)||d||^2 = {b18:.6f} < error "
          f"-> a 1/8 bound is FALSE; the sharp constant is 1/4")
    ok &= abs(err / b14 - 1.0) < 1e-12
    ok &= err > b18

    return check("T1 midpoint bound holds with constant 1/4; tight on the "
                 "V-instance; exact on quadratics; 1/8 refuted", ok)


# ----------------------------------------------------------------------
# T2  lambda* algebra: dR_lambda(lambda*) = 0; lambda* in (0,1) iff
#     dR_1 dR_2 < 0.
# ----------------------------------------------------------------------
def t2():
    print("\n== T2: lambda* identity and sign analysis ==")
    rng = np.random.default_rng(20260828)
    ok = True
    n_opp = n_same = 0
    for _ in range(100000):
        x, y = rng.normal(size=2) * rng.uniform(0.01, 2.0)
        x, y = float(x), float(y)
        if x == y:
            continue
        ls = lam_star(x, y)
        mix = ls * x + (1.0 - ls) * y
        ok &= abs(mix) <= 1e-9 * max(1.0, abs(x), abs(y))
        inside = 0.0 < ls < 1.0
        opp = x * y < 0.0
        ok &= inside == opp
        n_opp += opp
        n_same += not opp
    print(f"  100000 random draws: identity and equivalence hold on every draw "
          f"({n_opp} opposite-sign, {n_same} same-sign)")
    return check("T2 lambda* zero identity; lambda* in (0,1) iff opposite signs", ok)


# ----------------------------------------------------------------------
# Counterexample (a): reversal with an IDENTICAL read operator.
# m^A=(1,1), m^B=(0,2), C(m)=m1+m2 (both cost 2), d=(1,-1).
# Y ~ N(mu(m), sigma(m)^2), mu=(m2-1)/2, sigma=2-m1. Both classes read Y;
# risk_c = P(Y < tau_c), tau_1=-2, tau_2=+1.
# ----------------------------------------------------------------------
CA = dict(mB=np.array([0.0, 2.0]), d=np.array([1.0, -1.0]), tau1=-2.0, tau2=1.0)


def ca_risk(m, tau):
    mu = (m[1] - 1.0) / 2.0
    sg = 2.0 - m[0]
    return Phi((tau - mu) / sg)


def ca_dirderiv(t, tau):
    """f'(t) along the segment, closed form; z(t)=(tau-mu)/sigma."""
    m = CA["mB"] + t * CA["d"]
    mu = (m[1] - 1.0) / 2.0
    sg = 2.0 - m[0]
    z = (tau - mu) / sg
    # dz/dm1 = z/sigma ; dz/dm2 = -1/(2 sigma); d=(1,-1)
    dzdt = z / sg + 1.0 / (2.0 * sg)
    return phi(z) * dzdt


def ca_dircurv_sup(tau, npts=2001):
    ts = np.linspace(0.0, 1.0, npts)
    f1 = np.array([ca_dirderiv(t, tau) for t in ts])
    return float(np.max(np.abs(np.gradient(f1, ts))))


def t3():
    print("\n== T3: counterexample (a), crossing Gaussians, identical read operator ==")
    mB, d = CA["mB"], CA["d"]
    mA = mB + d
    r1A = ca_risk(mA, CA["tau1"])
    r1B = ca_risk(mB, CA["tau1"])
    r2A = ca_risk(mA, CA["tau2"])
    r2B = ca_risk(mB, CA["tau2"])
    dR1, dR2 = r1A - r1B, r2A - r2B
    ls = lam_star(dR1, dR2)
    print(f"  cost C(m)=m1+m2: C(m^A)={float(sum(mA)):.1f}, C(m^B)={float(sum(mB)):.1f}")
    print(f"  outcome law: A ~ N(0,1), B ~ N(0.5, 2^2); shared read Y; "
          f"thresholds tau1={CA['tau1']:.0f}, tau2={CA['tau2']:.0f}")
    print(f"  R1(A)={r1A:.4f}  R1(B)={r1B:.4f}  R2(A)={r2A:.4f}  R2(B)={r2B:.4f}")
    print(f"  dR1={dR1:+.4f}  dR2={dR2:+.4f}  lambda*={ls:.4f}")
    ok = (dR1 < 0.0 < dR2) and (0.0 < ls < 1.0)
    ok &= abs(sum(mA) - sum(mB)) < 1e-12
    return check("T3 reversal with identical read operator, resource-equivalent "
                 "policies", ok)


# ----------------------------------------------------------------------
# Counterexamples (b1), (b2): misalignment WITHOUT reversal.
# (b1) orthogonal: n=3, d=(0.5,-0.5,0), w1=(1,1,0.5), w2=(1,1,-0.5),
#      operating AT threshold: risks 0.5, ||grad|| large, grad^T d = 0,
#      dR_c = 0 exactly. Exposure E_c(d)=0: the gate abstains.
# (b2) far from threshold: n=2, w1=(1,0.3), w2=(1,0.5), mB=(3,3),
#      d=(0.5,-0.5): same-sign tiny deltas, E_c(d) far below the floor.
# ----------------------------------------------------------------------
def t4():
    print("\n== T4: counterexamples (b1) orthogonal and (b2) far-from-threshold ==")
    ok = True

    # (b1)
    w1 = np.array([1.0, 1.0, 0.5])
    w2 = np.array([1.0, 1.0, -0.5])
    mB = np.zeros(3)
    d = np.array([0.5, -0.5, 0.0])
    mA = mB + d
    mbar = mB + 0.5 * d
    tau = 0.0

    def risk(w, m):
        return Phi(tau - float(w @ m))

    def gradnorm(w, m):
        return phi(tau - float(w @ m)) * float(np.linalg.norm(w))

    dR1 = risk(w1, mA) - risk(w1, mB)
    dR2 = risk(w2, mA) - risk(w2, mB)
    E1 = phi(tau - float(w1 @ mbar)) * abs(float(w1 @ d))
    E2 = phi(tau - float(w2 @ mbar)) * abs(float(w2 @ d))
    gn1, gn2 = gradnorm(w1, mbar), gradnorm(w2, mbar)
    cosang = float(w1 @ w2) / (np.linalg.norm(w1) * np.linalg.norm(w2))
    print(f"  (b1) misaligned reads (cos angle {cosang:.3f}), both orthogonal to d:")
    print(f"       risks at operating point: {risk(w1, mB):.4f} and {risk(w2, mB):.4f} "
          f"(at threshold)")
    print(f"       ||grad R_1||={gn1:.4f}  ||grad R_2||={gn2:.4f}  (large)")
    print(f"       E_1(d)={E1:.4f}  E_2(d)={E2:.4f}  dR1={dR1:+.4f}  dR2={dR2:+.4f}")
    ok &= abs(dR1) < 1e-15 and abs(dR2) < 1e-15
    ok &= E1 < 1e-15 and E2 < 1e-15
    ok &= gn1 > 0.5 and gn2 > 0.5

    # (b2)
    w1 = np.array([1.0, 0.3])
    w2 = np.array([1.0, 0.5])
    mB = np.array([3.0, 3.0])
    d = np.array([0.5, -0.5])
    mA = mB + d
    mbar = mB + 0.5 * d
    dR1 = risk(w1, mA) - risk(w1, mB)
    dR2 = risk(w2, mA) - risk(w2, mB)
    E1 = phi(tau - float(w1 @ mbar)) * abs(float(w1 @ d))
    E2 = phi(tau - float(w2 @ mbar)) * abs(float(w2 @ d))
    L1 = phi(1.0) * float(w1 @ w1)
    L2 = phi(1.0) * float(w2 @ w2)
    fl1 = (L1 / 4.0) * float(d @ d)
    fl2 = (L2 / 4.0) * float(d @ d)
    print(f"  (b2) misaligned reads, ~4 sigma from threshold:")
    print(f"       R1(A)={risk(w1, mA):.2e}  R1(B)={risk(w1, mB):.2e}  "
          f"R2(A)={risk(w2, mA):.2e}  R2(B)={risk(w2, mB):.2e}")
    print(f"       dR1={dR1:+.2e}  dR2={dR2:+.2e}  (same sign: no reversal)")
    print(f"       E_1(d)={E1:.2e} vs floor {fl1:.4f} (ratio {E1 / fl1:.1e}); "
          f"E_2(d)={E2:.2e} vs floor {fl2:.4f} (ratio {E2 / fl2:.1e})")
    ok &= dR1 < 0 and dR2 < 0
    ok &= E1 < fl1 and E2 < fl2
    return check("T4 misalignment without reversal: (b1) exact zero along d with "
                 "large gradient norms; (b2) sub-floor exposure, same-sign deltas", ok)


# ----------------------------------------------------------------------
# T5  Worked instances from the graded records.
# ----------------------------------------------------------------------
def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def t5():
    print("\n== T5: worked instances (graded records) ==")
    ok = True
    tol = 1e-4  # records carry 4-decimal rounding

    qot = load(QOT_JSON)
    print("  XPROTO-QOT-FLIP (class 1 = R-fleet, class 2 = P-fleet, "
          "risk = false-clear rate, dR = A minus B):")
    for cell in qot["cells"]:
        d1 = cell["fp_fc_R_A"] - cell["fp_fc_R_B"]
        d2 = cell["fp_fc_P_A"] - cell["fp_fc_P_B"]
        rev = (d1 < 0.0 < d2) or (d2 < 0.0 < d1)
        ls = lam_star(d1, d2)
        fleet = cell["fp_fc_fleet_A"] - cell["fp_fc_fleet_B"]
        even = 0.5 * (d1 + d2)
        okA = abs(cell["fp_fc_fleet_A"]
                  - 0.5 * (cell["fp_fc_R_A"] + cell["fp_fc_P_A"])) <= tol
        okB = abs(cell["fp_fc_fleet_B"]
                  - 0.5 * (cell["fp_fc_R_B"] + cell["fp_fc_P_B"])) <= tol
        sign_ok = (fleet < 0) == (0.5 > ls) if d1 < d2 else (fleet > 0) == (0.5 > ls)
        # slope dR_1 - dR_2 < 0 here; dR_lambda = (lambda - lambda*)(dR_1 - dR_2)
        pred_even = (0.5 - ls) * (d1 - d2)
        print(f"    seed {cell['seed']}: dR_R={d1:+.4f} dR_P={d2:+.4f} "
              f"reversal={rev} lambda*={ls:.3f} fleetA-B={fleet:+.4f} "
              f"even-mix of class deltas={even:+.4f}")
        ok &= rev == cell["fp_flip"]
        ok &= okA and okB
        ok &= abs(fleet - even) <= 2 * tol
        ok &= (fleet < 0) == (pred_even < 0)
        ok &= sign_ok

    csi = load(CSI_JSON)
    print("  XPROTO-CSI-FLIP (class 1 = M-fleet, class 2 = S-fleet, "
          "risk = NACK rate, dR = A minus B):")
    for cell in csi["cells"]:
        d1 = cell["fc_M_A"] - cell["fc_M_B"]
        d2 = cell["fc_S_A"] - cell["fc_S_B"]
        rev = (d1 < 0.0 < d2) or (d2 < 0.0 < d1)
        ls = lam_star(d1, d2)
        fleet = cell["fc_fleet_A"] - cell["fc_fleet_B"]
        even = 0.5 * (d1 + d2)
        okA = abs(cell["fc_fleet_A"] - 0.5 * (cell["fc_M_A"] + cell["fc_S_A"])) <= tol
        okB = abs(cell["fc_fleet_B"] - 0.5 * (cell["fc_M_B"] + cell["fc_S_B"])) <= tol
        pred_even = (0.5 - ls) * (d1 - d2)
        print(f"    seed {cell['seed']}: dR_M={d1:+.4f} dR_S={d2:+.4f} "
              f"reversal={rev} lambda*={ls:.3f} fleetA-B={fleet:+.4f} "
              f"even-mix of class deltas={even:+.4f}")
        ok &= rev == cell["flip"]
        ok &= okA and okB
        ok &= abs(fleet - even) <= 2 * tol
        ok &= (fleet < 0) == (pred_even < 0)

    return check("T5 graded records: reversal indicators match recorded flip "
                 "fields; fleet = even mixture to rounding; even-mixture sign "
                 "agrees with lambda* vs 1/2", ok)


# ----------------------------------------------------------------------
# T6  Aligned controls: same-sign deltas, no reversal, every seed.
# ----------------------------------------------------------------------
def t6():
    print("\n== T6: aligned controls ==")
    ok = True
    qot = load(QOT_JSON)
    print("  QOT FEC control (SD/HD threshold pair, same read projection):")
    for cell in qot["cells"]:
        dsd = cell["fec_fc_sd_A"] - cell["fec_fc_sd_B"]
        dhd = cell["fec_fc_hd_A"] - cell["fec_fc_hd_B"]
        rev = (dsd < 0.0 < dhd) or (dhd < 0.0 < dsd)
        print(f"    seed {cell['seed']}: dR_SD={dsd:+.4f} dR_HD={dhd:+.4f} "
              f"same sign={dsd * dhd > 0} recorded fec_flip={cell['fec_flip']}")
        ok &= (not rev) and (not cell["fec_flip"]) and dsd * dhd > 0

    csi = load(CSI_JSON)
    print("  CSI null control (one trace, required tables shifted 0/+2 dB):")
    for cell in csi["cells"]:
        dt1 = cell["null_fc_t1_A"] - cell["null_fc_t1_B"]
        dt2 = cell["null_fc_t2_A"] - cell["null_fc_t2_B"]
        rev = (dt1 < 0.0 < dt2) or (dt2 < 0.0 < dt1)
        print(f"    seed {cell['seed']}: dR_t1={dt1:+.4f} dR_t2={dt2:+.4f} "
              f"same sign={dt1 * dt2 > 0} recorded null_flip={cell['null_flip']}")
        ok &= (not rev) and (not cell["null_flip"]) and dt1 * dt2 > 0

    return check("T6 aligned controls: same-sign deltas every seed, no reversal, "
                 "matching recorded null fields", ok)


# ----------------------------------------------------------------------
# T7  The exposure gate  E_c(d) > z SE_c + floor_c  (floor = curvature/4):
#     (a) passes deterministically; (b1) fails; false-license rate at z=2.
# ----------------------------------------------------------------------
def t7():
    print("\n== T7: exposure gate behavior ==")
    ok = True

    # Gate on counterexample (a): E_c from the closed form at the midpoint,
    # directional curvature floor M_c/4 with M_c = sup_t |f_c''(t)| (numeric).
    for c, tau in (("1", CA["tau1"]), ("2", CA["tau2"])):
        E = abs(ca_dirderiv(0.5, tau))
        M = ca_dircurv_sup(tau)
        floor = M / 4.0
        ratio = E / floor
        print(f"  (a) class {c}: E(d)=|f'(1/2)|={E:.4f}, curvature floor M/4={floor:.4f}, "
              f"exposure ratio={ratio:.2f}")
        ok &= ratio > 1.0
    g1 = ca_dirderiv(0.5, CA["tau1"])
    g2 = ca_dirderiv(0.5, CA["tau2"])
    print(f"  (a) signed midpoint directional derivatives: "
          f"grad R_1(mbar)^T d = {g1:+.4f}, grad R_2(mbar)^T d = {g2:+.4f} "
          f"(opposite signs)")
    ok &= g1 * g2 < 0

    # Gate on (b1): E=0 identically, any positive floor -> abstain.
    print("  (b1): E_c(d)=0 for both classes (printed in T4); the gate abstains")

    # False-license rate: true directional derivative 0, curvature floor 0,
    # estimator ~ N(0, SE^2), z=2. Licensed iff |est| > z*SE.
    rng = np.random.default_rng(20260829)
    z, SE, n = 2.0, 0.013, 200000
    est = rng.normal(0.0, SE, size=n)
    rate = float(np.mean(np.abs(est) > z * SE))
    nominal = 2.0 * Phi(-z)
    print(f"  false-license simulation (true derivative 0, z={z:.0f}, {n} draws): "
          f"rate={rate:.4f}, nominal 2*Phi(-2)={nominal:.4f}")
    ok &= abs(rate - nominal) < 0.005
    return check("T7 exposure gate: licenses (a), abstains on (b1), false-license "
                 "rate at z=2 matches 2*Phi(-2)", ok)


def main():
    print(f"flip_theorem_checks.py  (normal CDF: {PHI_SOURCE})")
    print(f"records: {QOT_JSON}\n         {CSI_JSON}")
    t1()
    t2()
    t3()
    t4()
    t5()
    t6()
    t7()
    n_fail = sum(1 for _, okk in RESULTS if not okk)
    print(f"\n{len(RESULTS) - n_fail}/{len(RESULTS)} checks passed.")
    if n_fail:
        print("OVERALL: FAIL")
        sys.exit(1)
    print("OVERALL: PASS")


if __name__ == "__main__":
    main()
