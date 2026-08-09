"""PF-7b instrument development: why do the positive controls die in some cells?

Not claim bearing. No bars here. This measures the controls so that a per-cell
B0 can be declared honestly in PF-7b, instead of weakening the bar after seeing
the data.

Hypothesis: every control applies a FIXED coefficient to an inner product
L . q whose magnitude falls as 1/sqrt(d), so each perturbation vanishes in high
dimension. If true, the fix is to normalise each control's strength by the
natural scale of L . q rather than to lower the bar.

Also trials a PR box as a geometry independent guaranteed control: outputs
satisfying a XOR b = x.y give S = 4 in every cell by construction, which is the
only way a per-cell anti-vacuity bar can be safe.
"""
import numpy as np

SEED = 20260808
N_ORIENT = 40000
N_DRAW = 120000
DIMS = (3, 8, 32, 128)


def fold_orientations(n, d, kappa, zipf_a, rng):
    X = rng.standard_normal((n, d))
    if kappa > 0.0:
        ax = rng.standard_normal(d)
        ax /= np.linalg.norm(ax)
        X = X + kappa * ax[None, :]
    X /= np.linalg.norm(X, axis=1, keepdims=True) + 1e-12
    if zipf_a > 0:
        w = 1.0 / np.power(np.arange(1, n + 1), zipf_a)
        rng.shuffle(w)
        w /= w.sum()
    else:
        w = np.full(n, 1.0 / n)
    return X, w


def plane(d, rng):
    e1 = rng.standard_normal(d)
    e1 /= np.linalg.norm(e1)
    e2 = rng.standard_normal(d)
    e2 -= (e2 @ e1) * e1
    e2 /= np.linalg.norm(e2)
    return e1, e2


def dirn(e1, e2, t):
    return np.cos(t) * e1 + np.sin(t) * e2


def chsh(E):
    return abs(E[(0, 0)] + E[(0, 1)] + E[(1, 0)] - E[(1, 1)])


def run(X, w, qA, qB, rng, arm, sharp=None, tilt=None, leak=None):
    E_all, E_ps = {}, {}
    base = rng.choice(len(X), N_DRAW, p=w)
    for x in (0, 1):
        for y in (0, 1):
            if arm == "C2":
                t = w * np.exp(tilt * (X @ qA[x]) * (X @ qB[y]))
                t /= t.sum()
                idx = rng.choice(len(X), N_DRAW, p=t)
            else:
                idx = base
            L = X[idx]
            if arm == "C0":                      # PR box, nonlocal by construction
                a = rng.integers(0, 2, N_DRAW)
                b = (a ^ (x * y)).astype(int)
                A = 1.0 - 2.0 * a
                B = 1.0 - 2.0 * b
            else:
                sa = L @ qA[x]
                if arm == "C3":
                    sa = sa + leak * (L @ qB[y])
                A = np.where(sa >= 0, 1.0, -1.0)
                B = np.where((L @ qB[y]) >= 0, -1.0, 1.0)
                if sharp is not None:
                    eta = lambda Z, q: 1.0 / (1.0 + np.exp(-sharp * (Z @ q)))
                    A = np.where(rng.random(N_DRAW) < eta(L, qA[x]), A, 0.0)
                    B = np.where(rng.random(N_DRAW) < eta(L, qB[y]), B, 0.0)
            E_all[(x, y)] = float((A * B).mean())
            both = (A != 0) & (B != 0)
            E_ps[(x, y)] = float((A[both] * B[both]).mean()) if both.sum() > 50 else 0.0
    return chsh(E_all), chsh(E_ps)


rng = np.random.default_rng(SEED)
grid = [dict(d=d, kappa=k, zipf_a=z) for d in DIMS for k in (0.0, 2.0) for z in (0.0, 1.5)]

print("scale of |L . q| by dimension (the suspected cause)")
for d in DIMS:
    X, w = fold_orientations(N_ORIENT, d, 0.0, 0.0, rng)
    e1, e2 = plane(d, rng)
    q = dirn(e1, e2, 0.0)
    print(f"  d={d:3d}  mean|L.q| = {np.abs(X @ q).mean():.4f}   1/sqrt(d) = {1/np.sqrt(d):.4f}")

print("\ncandidate scalings, S per cell (want > 2 in ALL 16)")
hdr = f"{'cell':<22}{'C0 PR':>8}{'C1 fix':>9}{'C2 fix':>9}{'C3 fix':>9}{'C1 old':>9}{'C2 old':>9}{'C3 old':>9}"
print(hdr)
res = {k: [] for k in ("C0", "C1", "C2", "C3", "C1o", "C2o", "C3o")}
for g in grid:
    X, w = fold_orientations(N_ORIENT, g["d"], g["kappa"], g["zipf_a"], rng)
    e1, e2 = plane(g["d"], rng)
    qA = {0: dirn(e1, e2, 0.0), 1: dirn(e1, e2, np.pi / 2)}
    qB = {0: dirn(e1, e2, np.pi / 4), 1: dirn(e1, e2, -np.pi / 4)}
    d = g["d"]
    s = np.sqrt(d)
    c0, _ = run(X, w, qA, qB, rng, "C0")
    _, c1 = run(X, w, qA, qB, rng, "C1", sharp=3.0 * s)          # scaled
    c2, _ = run(X, w, qA, qB, rng, "C2", tilt=1.2 * d)           # scaled
    c3, _ = run(X, w, qA, qB, rng, "C3", leak=0.45)              # weaker leak
    _, c1o = run(X, w, qA, qB, rng, "C1", sharp=3.0)
    c2o, _ = run(X, w, qA, qB, rng, "C2", tilt=1.2)
    c3o, _ = run(X, w, qA, qB, rng, "C3", leak=0.9)
    for k, v in zip(("C0", "C1", "C2", "C3", "C1o", "C2o", "C3o"),
                    (c0, c1, c2, c3, c1o, c2o, c3o)):
        res[k].append(v)
    lbl = f"d={d} k={g['kappa']:.0f} z={g['zipf_a']:.1f}"
    print(f"{lbl:<22}{c0:>8.3f}{c1:>9.3f}{c2:>9.3f}{c3:>9.3f}{c1o:>9.3f}{c2o:>9.3f}{c3o:>9.3f}")

print("\nfires in all 16 cells?")
for k in ("C0", "C1", "C2", "C3", "C1o", "C2o", "C3o"):
    v = np.array(res[k])
    print(f"  {k:4s} min {v.min():6.3f}  fires {int((v > 2.0).sum())}/16")
