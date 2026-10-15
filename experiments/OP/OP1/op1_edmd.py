"""OP1: on which coordinates should a Koopman dictionary be built? (OP track, gate OP1).

The open problem. Extended dynamic mode decomposition (EDMD) approximates the Koopman operator on a dictionary of
observables, and which observables to put in the dictionary is open (Colbrook, arXiv:2312.00137, calls it one of the
field's most significant open problems). OP1 takes the slice of that problem an observer defines. A consumer reads the
large scales of a flow and wants to predict them. Its dictionary always holds its own coordinates. Which r further
coordinates of the flow should be added, and does the read distortion choose them better than energy or scale?

World. D8's forced two-dimensional turbulence (`experiments/OD/D8/d8_sync.py`, imported, not copied): Kolmogorov
forcing at k_f = 4, linear drag, pseudo-spectral RK4, spun up to a statistically stationary state. One training and one
independent test trajectory per world, sampled every dt_sample.

Consumer and pool. The consumer reads the Fourier pairs with |k| <= k_c. The pool is the pairs with k_c < |k| <= k_pool,
the same physical modes at every resolution. A coordinate is a pair's real and imaginary part in math units.

Rankings of the pool (computed on the training trajectory only).
  READ     E_t[ s_k(t) |w_k(t) - mean w_k|^2 ], the read distortion of pair k for the consumer, with
           s_k = (|P_C N_w e_re|^2 + |P_C N_w e_im|^2) / 2 the sensitivity of the consumer's tendency to a unit
           perturbation of the pair (notes/dynamical-read-operator.md, Proposition 4 and Section 6)
  ENERGY   the training variance of w_k (graded control)
  BALL     |k| ascending (graded control, the scale-based choice)
  SENS     E_t[s_k] alone (recorded)
  RANDOM   seeded permutations (the null, median over draws)
  READ_KE  with --read-ke only: READ with the consumer's response measured in the kinetic-energy norm, sum |.|^2 / |k|^2,
           instead of the enstrophy norm; the mask and the amplitude factor unchanged (the secondary arm READ-KE of
           PREREG-OP1-RUN-DRAFT.md Section 3)
Records beside them: POD, the leading 2r principal components of the pool coordinates (a different basis, matched real
dimension); GREEDY, forward selection on a validation split of the training trajectory (the data-fitted selector); NONE,
the consumer's coordinates alone.

Why READ is the hypothesis and not a guess. The consumer's one-step increment is dt times its tendency T_C(w). At first
order around the training mean, coordinate k contributes J_k (x_k - mean x_k), with J_k the consumer tendency's derivative
along the pair. Under random phases the variance it adds is |J_k|^2 Var(x_k), which is READ. So READ orders coordinates by
their first-order share of the consumer's one-step increment. Whether that order survives a nonlinear lift and iteration
over many steps is the question.

Dictionaries and prediction. z = standardized [consumer coordinates, selected coordinates]. Lift LIN: [1, z] (DMD with
augmentation). Lift RFF: [1, z, sqrt(2/D) cos(z W + b)], random Fourier features of a Gaussian kernel with length scale
sqrt(dim z), W and b seeded by dim z, so every arm at the same r sees the same draw. K by ridge regression of psi(t+1) on
psi(t). Prediction iterates K from psi(x_0) without re-lifting (a Koopman forecast), and reads the consumer's coordinates
off the iterate. Error at horizon h: sqrt(sum |p_hat - p|^2 / sum |p - mean p|^2) over test starts, so 0 is exact and 1 is
the climatology. The graded cell value is the mean over the declared horizons of min(e_h, cap).

    python op1_edmd.py --selftest
    python op1_edmd.py --config prereg_config.json --seed-role probe --out probe.json [--world NAME] [--traj-dir DIR] [--read-ke]
"""
from __future__ import annotations

import argparse
import json
import os
import math
import sys
import time
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):  # one core per run, set before numpy loads
    os.environ.setdefault(_v, "1")
import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "OD" / "D8"))
from d8_sync import Candidates, ForcedNS2D, initial_field, sq, spectrum_tail, spin_up, stability, vel_norm  # noqa: E402

ARMS_GRADED = ("READ", "ENERGY", "BALL")
LIFTS = ("lin", "rff", "tend")


# ---------------------------------------------------------------- the consumer, the pool, coordinates

class Split:
    """Consumer pairs |k| <= kc and pool pairs kc < |k| <= kpool, as indices into Candidates; `keep` is their union in
    the order the trajectory records them (consumer first)."""

    def __init__(self, cand: Candidates, kc: float, kpool: float):
        self.cons = np.nonzero(cand.kmag <= kc)[0]; self.pool = np.nonzero((cand.kmag > kc) & (cand.kmag <= kpool))[0]
        self.keep = np.concatenate([self.cons, self.pool]); self.nc = len(self.cons); self.npool = len(self.pool)

    def cols(self, local: np.ndarray, offset: int) -> np.ndarray:
        """Real coordinate columns (real parts then imaginary parts) of pairs at positions `local` in keep[offset:]."""
        m = len(self.keep); loc = offset + np.asarray(local, int); return np.concatenate([loc, m + loc])


def coords(model, wh, cand: Candidates, keep: np.ndarray) -> np.ndarray:
    v = wh[cand.ix[keep], cand.iy[keep]] / model.n ** 2; return np.concatenate([v.real, v.imag])


def consumer_mask(model, kc: float) -> np.ndarray:
    return (model.kmag <= kc) & model.dealias


def ke_sq(model, X):
    """Sum of |X_k|^2 / |k|^2 over the last two axes in math units: the squared velocity norm over (2 pi)^2, the
    kinetic-energy norm of a vorticity field (as in experiments/OP/VARIANTS/op_variants.py)."""
    k2 = model.k2true.copy(); k2[0, 0] = np.inf
    return np.sum(np.abs(X) ** 2 / k2, axis=(-2, -1)) / model.n ** 4


def consumer_sens(model, wh, cand: Candidates, pairs: np.ndarray, cmask: np.ndarray, chunk: int, norms=(sq,)) -> np.ndarray:
    """s_k = (|P_C N_w e_re|^2 + |P_C N_w e_im|^2) / 2 for the given pairs, in math units, with the response measured in
    `norms[0]`. With several norms, one row per norm from the same tangent evaluations (READ-KE: norms=(sq, ke_sq))."""
    s = np.empty((len(norms), len(pairs)))
    for a in range(0, len(pairs), chunk):
        sel = pairs[a:a + chunk]
        dre = cmask * model.tangent_nl(wh, cand.unit(sel, model.n, False)); dim = cmask * model.tangent_nl(wh, cand.unit(sel, model.n, True))
        for i, norm in enumerate(norms):
            s[i, a:a + len(sel)] = 0.5 * (norm(model, dre) + norm(model, dim))
    return s[0] if len(norms) == 1 else s


def record_trajectory(model, wh, T: float, dt: float, ds: float, cand, keep, sens_every: float = 0.0, sens_fn=None):
    """Integrate for T, recording coordinates every ds; every sens_every (if > 0) also call sens_fn(wh) -> vector."""
    per = int(round(ds / dt)); ns = int(round(T / ds)); X = np.empty((ns + 1, 2 * len(keep))); S = []; S_at = []
    se = int(round(sens_every / ds)) if sens_every > 0 else 0
    for i in range(ns + 1):
        X[i] = coords(model, wh, cand, keep)
        if se and i % se == 0: S.append(sens_fn(wh)); S_at.append(i)
        if i < ns:
            for _ in range(per):
                wh = model.fstep(wh, dt)
    return X, (np.array(S) if S else None), np.array(S_at, int), wh


def make_tend(cand: Candidates, split: Split, nt: int = 40):
    """The consumer's tendency T_C evaluated on chosen pairs alone, from their coordinates: the field holding only those
    pairs is built on an nt x nt grid and D8's nonlinear term is applied. Products of recorded pairs reach twice the
    largest recorded component, so nothing aliases onto the consumer when nt - 2 max|k_i| > max consumer |k_i|.
    Returns tend(X, pairs) -> (N, 2 n_c) real, in math units."""
    m40 = ForcedNS2D(nt, 1.0, 0.0, 0.0, 4); kx = cand.kx[split.keep]; ky = cand.ky[split.keep]; m = len(split.keep)
    if nt - 2 * int(np.max(np.abs(np.concatenate([kx, ky])))) <= int(np.max(np.abs(np.concatenate([kx[:split.nc], ky[:split.nc]])))):
        raise ValueError("grid too small for an alias-free consumer tendency")
    ix, iy, nix, niy = kx % nt, ky % nt, (-kx) % nt, (-ky) % nt; ci, cj = ix[:split.nc], iy[:split.nc]

    def tend(X: np.ndarray, pairs: np.ndarray) -> np.ndarray:
        out = []
        for a in range(0, len(X), 400):
            Xa = X[a:a + 400]; W = np.zeros((len(Xa), nt, nt), complex); v = (Xa[:, pairs] + 1j * Xa[:, m + pairs]) * nt ** 2
            W[:, ix[pairs], iy[pairs]] = v; W[:, nix[pairs], niy[pairs]] = np.conj(v)
            T = -m40.nl_hat(W)[:, ci, cj] / nt ** 2; out.append(np.hstack([T.real, T.imag]))
        return np.vstack(out)
    return tend


# ---------------------------------------------------------------- rankings

def pair_fluct(X: np.ndarray, m: int, local: np.ndarray, offset: int) -> np.ndarray:
    """|x_k - mean x_k|^2 per sample for pairs at positions local in keep[offset:] (real and imaginary parts summed)."""
    Xc = X - X.mean(axis=0); re = Xc[:, offset + local]; im = Xc[:, m + offset + local]; return re ** 2 + im ** 2


def rankings(X: np.ndarray, S: np.ndarray, S_at: np.ndarray, split: Split, kmag: np.ndarray, draws: int, rng, S_ke=None) -> dict:
    """Orders of the pool (positions 0..npool-1). X is the training record, S the consumer sensitivities at rows S_at.
    With S_ke (the same sensitivities in the kinetic-energy norm) the secondary arm READ_KE is added; the RANDOM draws
    come after it from the same rng, so they are the same with or without it."""
    m = len(split.keep); loc = np.arange(split.npool); F = pair_fluct(X, m, loc, split.nc)
    read = np.mean(S * F[S_at], axis=0); energy = F.mean(axis=0); sens = S.mean(axis=0)
    idx = np.arange(split.npool)  # ties in |k| broken by index, which is deterministic
    o = {"READ": np.argsort(-read, kind="stable"), "ENERGY": np.argsort(-energy, kind="stable"),
         "BALL": np.lexsort((idx, np.round(kmag, 12))), "SENS": np.argsort(-sens, kind="stable")}
    scores = {"read": read, "energy": energy, "sens": sens}
    if S_ke is not None:
        scores["read_ke"] = np.mean(S_ke * F[S_at], axis=0); o["READ_KE"] = np.argsort(-scores["read_ke"], kind="stable")
    for j in range(draws):
        o[f"RANDOM{j}"] = rng.permutation(split.npool)
    return o, scores


# ---------------------------------------------------------------- EDMD

def rff_draw(d: int, D: int, seed: int):
    r = np.random.default_rng(seed + 1009 * d); return r.normal(0.0, 1.0 / math.sqrt(d), size=(d, D)), r.uniform(0, 2 * math.pi, size=D)


def lift(Z: np.ndarray, kind: str, W=None, b=None) -> np.ndarray:
    one = np.ones((len(Z), 1))
    if kind == "lin": return np.hstack([one, Z])
    return np.hstack([one, Z, math.sqrt(2.0 / W.shape[1]) * np.cos(Z @ W + b)])


def fit_koopman(P: np.ndarray, ridge: float) -> np.ndarray:
    """Ridge EDMD on one contiguous record P (rows are psi at successive samples): K with psi(t+1) ~ psi(t) K."""
    Px, Py = P[:-1], P[1:]; G = Px.T @ Px; lam = ridge * np.trace(G) / len(G)
    return np.linalg.solve(G + lam * np.eye(len(G)), Px.T @ Py)


class Problem:
    """One (world, cutoff, lift): fits a dictionary for any choice of extra coordinates and scores it on the test record."""

    def __init__(self, Xtr, Xte, split: Split, kind: str, cfg: dict, seed: int, tend=None):
        self.Xtr, self.Xte, self.split, self.kind, self.seed, self.tend = Xtr, Xte, split, kind, seed, tend
        self.D = int(cfg["rff_features"]); self.ridge = float(cfg["ridge"])
        self.H = [int(h) for h in cfg["horizons"]]; self.cap = float(cfg["error_cap"])
        self.ccols = split.cols(np.arange(split.nc), 0)  # the consumer's columns in X
        self.starts = np.arange(0, len(Xte) - max(self.H), int(cfg["test_start_stride"]))

    def _raw(self, X, extra):
        """[consumer coordinates, extra]; extra is a feature map of X (callable) or column indices into X."""
        cons = X[:, self.ccols]
        if callable(extra): return np.hstack([cons, extra(X)])
        return np.hstack([cons, X[:, extra]]) if len(extra) else cons

    def score(self, extra, radius: bool = True) -> dict | None:
        Ztr = self._raw(self.Xtr, extra); Zte = self._raw(self.Xte, extra)
        if self.kind == "tend":  # append T_C on the consumer's and the selected pairs; a feature-map extra (POD) has no pairs
            if callable(extra): return None
            ex = np.asarray(extra, int); pairs = np.concatenate([np.arange(self.split.nc), ex[:len(ex) // 2]])
            Ztr = np.hstack([Ztr, self.tend(self.Xtr, pairs)]); Zte = np.hstack([Zte, self.tend(self.Xte, pairs)])
        mu = Ztr.mean(axis=0); sd = Ztr.std(axis=0); sd[sd == 0] = 1.0; Ztr = (Ztr - mu) / sd; Zte = (Zte - mu) / sd
        W, b = rff_draw(Ztr.shape[1], self.D, self.seed) if self.kind == "rff" else (None, None)
        base = "rff" if self.kind == "rff" else "lin"  # TEND is the linear lift of [consumer, selected, T_C]
        K = fit_koopman(lift(Ztr, base, W, b), self.ridge); Pte = lift(Zte, base, W, b)
        nc2 = len(self.ccols); e = self._errors(K, Pte, mu[:nc2], sd[:nc2])
        vals = [min(e[h], self.cap) for h in self.H]
        rho = float(np.max(np.abs(np.linalg.eigvals(K)))) if radius else None
        return {"e": {str(h): (e[h] if math.isfinite(e[h]) else None) for h in self.H}, "E": float(np.mean(vals)),
                "diverged": any(not math.isfinite(e[h]) for h in self.H), "spectral_radius": rho, "dim": int(K.shape[0])}

    def persist(self) -> dict:
        """The persistence forecast p_hat(t + h) = p(t), the trivial baseline every forecast is read against."""
        tru_all = self.Xte[:, self.ccols]; mu = self.Xtr[:, self.ccols].mean(axis=0); e = {}
        for h in self.H:
            tru = tru_all[self.starts + h]; e[str(h)] = math.sqrt(float(np.sum((tru_all[self.starts] - tru) ** 2)) / float(np.sum((tru - mu) ** 2)))
        return {"e": e, "E": float(np.mean([min(v, self.cap) for v in e.values()]))}

    def _errors(self, K, Pte, mu, sd) -> dict:
        """Iterate K from psi at each start without re-lifting; read the consumer's coordinates off the iterate (columns
        1..nc2 of psi, standardized) and score them in math units against the truth. mu is the training mean of the
        consumer's coordinates, so the denominator is the climatology's error."""
        out = {}; Ph = Pte[self.starts]; tru_all = self.Xte[:, self.ccols]; nc2 = len(mu)
        with np.errstate(all="ignore"):
            for h in range(1, max(self.H) + 1):
                Ph = Ph @ K
                if h in self.H:
                    est = Ph[:, 1:1 + nc2] * sd + mu; tru = tru_all[self.starts + h]
                    num = float(np.sum((est - tru) ** 2)); den = float(np.sum((tru - mu) ** 2))
                    out[h] = math.sqrt(num / den) if np.isfinite(num) else math.inf
        return out


def pool_cols(split: Split, order: np.ndarray, r: int) -> np.ndarray:
    return split.cols(order[:r], split.nc)


def pod_extra(Xtr: np.ndarray, split: Split, q: int):
    """The leading q principal components of the pool coordinates (training fluctuations), as a feature map."""
    cols = split.cols(np.arange(split.npool), split.nc); A = Xtr[:, cols]
    mu = A.mean(axis=0); _, _, Vt = np.linalg.svd(A - mu, full_matrices=False); V = Vt[:q].T
    return lambda X: (X[:, cols] - mu) @ V


def greedy_order(Xtr: np.ndarray, split: Split, kind: str, cfg: dict, seed: int, rmax: int, log=None, tend=None) -> list[int]:
    """Forward selection of pool pairs on a validation split of the training record: fit on the first part, score E on the
    rest. The data-fitted selector, recorded beside the rankings."""
    cut = int(len(Xtr) * float(cfg["greedy_fit_fraction"]))
    prob = Problem(Xtr[:cut], Xtr[cut:], split, kind, cfg, seed, tend); chosen = []
    for step in range(rmax):
        best, bestE = None, math.inf
        for j in range(split.npool):
            if j in chosen: continue
            E = prob.score(pool_cols(split, np.array(chosen + [j]), len(chosen) + 1), radius=False)["E"]
            if E < bestE: best, bestE = j, E
        chosen.append(best)
        if log: log(json.dumps({"greedy": kind, "step": step + 1, "E_val": round(bestE, 4)}))
    return chosen


# ---------------------------------------------------------------- one world

def run_world(world: dict, cfg: dict, seed: int, log=print, traj_dir: str | None = None, read_ke: bool = False) -> dict:
    """read_ke adds the secondary arm READ_KE (the run registration's READ-KE): the consumer sensitivities are also taken
    in the kinetic-energy norm, from the same tangent evaluations, and stored in the trajectory file as S_ke. A cached
    file without S_ke is simulated again, and the new record must equal the cached one exactly before it replaces it."""
    cfg = {**cfg, **world.get("overrides", {})}; t0 = time.time(); n = int(world["n"]); off = int(world["seed_offset"])
    model = ForcedNS2D(n, float(world["nu"]), float(cfg["alpha"]), float(cfg["F0"]), int(cfg["kf"])); cand = Candidates(model)
    dt = float(cfg["dt_base"]) * int(cfg["n_ref"]) / n; ds = float(cfg["dt_sample"]); kpool = float(cfg["k_pool"])
    keep_all = np.nonzero(cand.kmag <= kpool)[0]
    out = {"name": world["name"], "group": world["group"], "n": n, "nu": model.nu, "dt": dt, "cutoffs": {}}
    # one training and one independent test trajectory; the sensitivities for every cutoff are taken on the training run
    splits = {str(kc): Split(cand, float(kc), kpool) for kc in cfg["cutoffs"]}
    masks = {k: consumer_mask(model, float(k)) for k in splits}

    norms = (sq, ke_sq) if read_ke else (sq,); npool_tot = sum(s.npool for s in splits.values())

    def sens_fn(wh):  # [enstrophy rows of every cutoff, then kinetic-energy rows of every cutoff]
        rows = [np.atleast_2d(consumer_sens(model, wh, cand, s.pool, masks[k], int(cfg["chunk"]), norms)) for k, s in splits.items()]
        return np.concatenate([np.concatenate([r[i] for r in rows]) for i in range(len(norms))])

    cache = Path(traj_dir) / f"{world['name']}_seed{seed}.npz" if traj_dir else None
    z = np.load(cache) if cache is not None and cache.exists() else None
    if z is not None and not np.array_equal(z["keep"], keep_all): raise SystemExit(f"{cache}: cached pairs differ from this config's")
    Ske_all = None
    if z is not None and (not read_ke or "S_ke" in z.files):  # the trajectories are seed-deterministic; a cached copy is the same record
        Xtr_all, S_all, S_at, Xte_all = z["Xtr"], z["S"], z["S_at"], z["Xte"]; Ske_all = z["S_ke"] if read_ke else None
        out.update(json.loads(str(z["meta"]))); out["trajectory_cache"] = cache.name
    else:
        rng = np.random.default_rng(seed + off); u = spin_up(model, initial_field(model, rng, int(cfg["ic_kmax"]), float(cfg["omega_rms"])), float(cfg["T_spin"]), dt)
        out["stability"] = stability(model, u, dt, 0.0)
        if not out["stability"]["ok"]:
            out["refused"] = "explicit RK4 stability guard failed"; log(json.dumps({"world": world["name"], "refused": out["refused"]})); return out
        Xtr_all, S_all, S_at, u = record_trajectory(model, u, float(cfg["T_train"]), dt, ds, cand, keep_all, float(cfg["sens_every"]), sens_fn)
        if read_ke: Ske_all = S_all[:, npool_tot:]; S_all = S_all[:, :npool_tot]
        out["train_spectrum_tail"] = spectrum_tail(model, u)
        rng = np.random.default_rng(seed + off + 5000); v = spin_up(model, initial_field(model, rng, int(cfg["ic_kmax"]), float(cfg["omega_rms"])), float(cfg["T_spin"]), dt)
        Xte_all, _, _, v = record_trajectory(model, v, float(cfg["T_test"]), dt, ds, cand, keep_all)
        out["test_spectrum_tail"] = spectrum_tail(model, v); out["trajectory_seconds"] = round(time.time() - t0, 1)
        if z is not None:  # a cached record without S_ke: the new one must be the same record, or nothing is replaced
            same = {k: bool(np.array_equal(a, z[k])) for k, a in (("Xtr", Xtr_all), ("S", S_all), ("S_at", S_at), ("Xte", Xte_all))}
            out["trajectory_recheck"] = {"cache": cache.name, "identical": same}; log(json.dumps({"world": world["name"], "trajectory_recheck": same}))
            if not all(same.values()): raise SystemExit(f"{cache}: the simulated record differs from the cached one {same}; cache left as it was")
        if cache is not None:
            meta = {k: out[k] for k in ("stability", "train_spectrum_tail", "test_spectrum_tail", "trajectory_seconds")}
            extra = {"S_ke": Ske_all} if read_ke else {}
            tmp = cache.with_suffix(".tmp.npz"); np.savez_compressed(tmp, Xtr=Xtr_all, S=S_all, S_at=S_at, Xte=Xte_all, keep=keep_all, meta=json.dumps(meta, default=float), **extra); tmp.replace(cache)
    log(json.dumps({"world": world["name"], "phase": "trajectories", "samples": [len(Xtr_all), len(Xte_all)], "tail": [round(out["train_spectrum_tail"], 9), round(out["test_spectrum_tail"], 9)], "seconds": out["trajectory_seconds"]}))

    pos = {int(j): i for i, j in enumerate(keep_all)}; m_all = len(keep_all); sofs = 0
    for kc, split in splits.items():
        # re-index the recorded coordinates to this split's keep order (consumer first, then pool)
        idx = np.array([pos[int(j)] for j in split.keep]); colmap = np.concatenate([idx, m_all + idx])
        Xtr = Xtr_all[:, colmap]; Xte = Xte_all[:, colmap]; S = S_all[:, sofs:sofs + split.npool]
        S_ke = Ske_all[:, sofs:sofs + split.npool] if read_ke else None; sofs += split.npool
        orders, scores = rankings(Xtr, S, S_at, split, cand.kmag[split.pool], int(cfg["random_draws"]), np.random.default_rng(seed + off + 977), S_ke)
        arms = ("READ", "ENERGY", "BALL", "SENS") + (("READ_KE",) if read_ke else ())
        ladder = [r for r in cfg["ladder"] if r <= split.npool]
        rec = {"n_consumer_pairs": split.nc, "n_pool_pairs": split.npool, "ladder": ladder,
               "rankings": {k: [[int(cand.kx[split.pool[i]]), int(cand.ky[split.pool[i]])] for i in o[:max(ladder)]] for k, o in orders.items()},
               "scores_top": {k: [float(x) for x in np.sort(v)[::-1][:max(ladder)]] for k, v in scores.items()}, "lifts": {}}
        # overlap of READ's top r with the controls' top r, the first thing to read if READ and a control tie
        rec["overlap"] = {c: {str(r): len(set(orders["READ"][:r]) & set(orders[c][:r])) for r in ladder} for c in ("ENERGY", "BALL", "SENS")}
        if read_ke:  # READ-KE's top r against its control's and READ's
            rec["overlap_read_ke"] = {c: {str(r): len(set(orders["READ_KE"][:r]) & set(orders[c][:r])) for r in ladder} for c in ("READ", "ENERGY", "BALL")}
        tend = make_tend(cand, split)
        for kind in cfg["lifts"]:
            prob = Problem(Xtr, Xte, split, kind, cfg, seed + 31, tend); cells = {"NONE": prob.score(np.array([], int)), "PERSIST": prob.persist()}
            for r in ladder:
                c = {name: prob.score(pool_cols(split, orders[name], r)) for name in arms}
                rnd = [prob.score(pool_cols(split, orders[f"RANDOM{j}"], r)) for j in range(int(cfg["random_draws"]))]
                c["RANDOM_median_E"] = float(np.median([x["E"] for x in rnd])); c["RANDOM_E"] = [x["E"] for x in rnd]
                c["POD"] = prob.score(pod_extra(Xtr, split, 2 * r))
                cells[str(r)] = c
                log(json.dumps({"world": world["name"], "kc": kc, "lift": kind, "r": r, **{k: (round(c[k]["E"], 4) if c[k] else None) for k in arms + ("POD",)}, "RANDOM": round(c["RANDOM_median_E"], 4), "seconds": round(time.time() - t0, 1)}))
            if kind in cfg.get("greedy_lifts", []):
                g = greedy_order(Xtr, split, kind, cfg, seed + 31, max(ladder), tend=tend)
                for r in ladder:
                    cells[str(r)]["GREEDY"] = prob.score(pool_cols(split, np.array(g), r))
                rec.setdefault("greedy_order", {})[kind] = [[int(cand.kx[split.pool[i]]), int(cand.ky[split.pool[i]])] for i in g]
            rec["lifts"][kind] = cells
        out["cutoffs"][kc] = rec
    out["seconds"] = time.time() - t0
    return out


def footprint(t_wall0: float) -> dict:
    import resource
    ru = resource.getrusage(resource.RUSAGE_SELF); wall = time.time() - t_wall0
    return {"peak_rss_mib": ru.ru_maxrss / 1024.0, "cpu_seconds": ru.ru_utime + ru.ru_stime, "wall_seconds": wall}


def run(cfg: dict, seed_role: str, out_path: str, only_world: str | None = None, traj_dir: str | None = None, read_ke: bool = False) -> dict:
    t_wall0 = time.time(); seed = int(cfg[f"seed_{seed_role}"]); groups = cfg["groups_by_role"][seed_role]
    result = {"config": cfg, "seed_role": seed_role, "seed": seed, "read_ke": read_ke, "started": time.strftime("%Y-%m-%d %H:%M:%S"), "worlds": []}
    for world in cfg["worlds"]:
        if world["group"] not in groups or (only_world and world["name"] != only_world): continue
        result["worlds"].append(run_world(world, cfg, seed, traj_dir=traj_dir, read_ke=read_ke)); result["footprint"] = footprint(t_wall0)
        json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1, default=float)
    if only_world and not result["worlds"]: raise SystemExit(f"no world named {only_world} in role {seed_role}")
    result["finished"] = time.strftime("%Y-%m-%d %H:%M:%S"); result["footprint"] = footprint(t_wall0)
    json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1, default=float)
    return result


# ---------------------------------------------------------------- self-test

def selftest() -> int:
    fails = 0

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"{label}: {detail}", "PASS" if ok else "FAIL"); fails += 0 if ok else 1

    base = {"rff_features": 64, "ridge": 1e-10, "horizons": [1, 4, 16], "error_cap": 2.0, "test_start_stride": 1, "greedy_fit_fraction": 0.7}
    # 1. A synthetic consumer driven by a quiet pair it reads, beside a loud pair it does not. Pair 1 rotates
    # deterministically with amplitude 0.1; pair 2 is AR(1) noise forty times louder and never read;
    # p_{t+1} = 0.9 p + 0.5 Re(y1). READ must rank pair 1 first and ENERGY pair 2. With pair 1 the linear dictionary
    # (p, Re y1, Im y1) is closed and forecasts exactly at every horizon; with pair 2 it gains nothing over p alone.
    rng = np.random.default_rng(1); N = 3000; th = 0.3
    t_ = np.arange(N); y1 = 0.1 * np.exp(1j * th * t_); y2 = np.zeros(N, complex); p = np.zeros(N)
    for t in range(N - 1):
        y2[t + 1] = 0.95 * y2[t] + 4.0 * complex(rng.normal(), rng.normal()); p[t + 1] = 0.9 * p[t] + 0.5 * y1[t].real

    class Fake:  # a Split with one consumer pair (p) and two pool pairs (y1, y2)
        keep = np.arange(3); nc = 1; npool = 2; cons = np.array([0]); pool = np.array([1, 2])

        def cols(self, local, offset):
            loc = offset + np.asarray(local, int); return np.concatenate([loc, 3 + loc])

    X = np.stack([p, y1.real, y2.real, np.zeros(N), y1.imag, y2.imag], axis=1); split = Fake()
    S_at = np.arange(0, N, 10); S = np.tile(np.array([[0.125, 0.0]]), (len(S_at), 1))  # s = (0.5^2 + 0^2) / 2 for pair 1
    o, _ = rankings(X, S, S_at, split, np.array([2.0, 3.0]), 2, np.random.default_rng(0))
    check("READ ranks the read pair first, ENERGY the loud one", o["READ"][0] == 0 and o["ENERGY"][0] == 1, f"READ {o['READ'].tolist()} ENERGY {o['ENERGY'].tolist()}")
    half = N // 2; prob = Problem(X[:half], X[half:], split, "lin", base, 7)
    e_none = prob.score(np.array([], int))["E"]; e_y1 = prob.score(pool_cols(split, o["READ"], 1))["E"]; e_y2 = prob.score(pool_cols(split, o["ENERGY"], 1))["E"]
    check("dictionary with the read pair is exact at every horizon; the loud pair adds nothing", e_y1 < 1e-6 and abs(e_y2 - e_none) < 0.02 * e_none and e_none > 0.1, f"E none {e_none:.3f}, y1 {e_y1:.1e}, y2 {e_y2:.3f}")
    g = greedy_order(X[:half], split, "lin", base, 7, 1)
    check("greedy forward selection picks the read pair", g == [0], str(g))
    # 2. EDMD on an exactly linear system recovers the operator and forecasts exactly at every horizon
    A = np.array([[0.9, 0.2], [-0.2, 0.9]]); Z = np.zeros((400, 2)); Z[0] = [1.0, 0.0]
    for t in range(399):
        Z[t + 1] = Z[t] @ A.T
    P = lift(Z, "lin"); K = fit_koopman(P, 1e-14); Ph = P[:10] @ np.linalg.matrix_power(K, 16)
    check("linear EDMD forecasts a linear system exactly", np.max(np.abs(Ph[:, 1:] - Z[16:26])) < 1e-8, f"{np.max(np.abs(Ph[:, 1:] - Z[16:26])):.1e}")
    # 3. the error is 0 for the truth and about 1 for the climatology
    rng = np.random.default_rng(2); truth = rng.normal(size=(200, 3)); clim = truth.mean(axis=0)
    e0 = math.sqrt(np.sum((truth - truth) ** 2) / np.sum((truth - clim) ** 2)); e1 = math.sqrt(np.sum((clim - truth) ** 2) / np.sum((truth - clim) ** 2))
    check("error scale: truth 0, climatology 1", e0 == 0.0 and abs(e1 - 1.0) < 1e-12, f"{e0}, {e1}")
    # 4. random Fourier features are seeded by dimension (every arm at the same r sees the same draw) and approximate the kernel
    W1, b1 = rff_draw(5, 4096, 3); W2, b2 = rff_draw(5, 4096, 3); x = np.random.default_rng(4).normal(size=(2, 5))
    phi = math.sqrt(2.0 / 4096) * np.cos(x @ W1 + b1); approx = float(phi[0] @ phi[1]); exact = math.exp(-np.sum((x[0] - x[1]) ** 2) / (2 * 5))
    check("RFF deterministic per dimension and close to the Gaussian kernel", np.array_equal(W1, W2) and abs(approx - exact) < 0.05, f"{approx:.3f} vs {exact:.3f}")
    # 5. on the flow: the consumer sensitivity equals the central difference of the consumer's tendency (exact, quadratic)
    model = ForcedNS2D(32, 0.02, 0.1, 1.0, 4); cand = Candidates(model); sp = Split(cand, 3.0, 8.0); cm = consumer_mask(model, 3.0)
    wh = initial_field(model, np.random.default_rng(5), 6, 3.0); s = consumer_sens(model, wh, cand, sp.pool[:5], cm, 4); eps = 0.3
    cd = []
    for j in sp.pool[:5]:
        tot = 0.0
        for imag in (False, True):
            e = cand.unit(np.array([j]), 32, imag)[0]
            d = (-model.nl_hat(wh + eps * e) + model.nl_hat(wh - eps * e)) / (2 * eps); tot += sq(model, cm * d)
        cd.append(0.5 * tot)
    err = float(np.max(np.abs(np.array(cd) - s)) / np.max(s))  # relative to the largest: a pair the consumer cannot read has s ~ 1e-37
    check("consumer sensitivity = central difference of the consumer tendency", err < 1e-9, f"{err:.1e}")
    # 6. the split partitions the pairs |k| <= kpool into consumer and pool, and coordinates read back the field
    ok = len(set(sp.cons) & set(sp.pool)) == 0 and set(sp.keep) == set(np.nonzero(cand.kmag <= 8.0)[0]) and np.all(cand.kmag[sp.cons] <= 3.0)
    c = coords(model, wh, cand, sp.keep); back = np.zeros((32, 32), complex); m = len(sp.keep)
    back[cand.ix[sp.keep], cand.iy[sp.keep]] = (c[:m] + 1j * c[m:]) * 32 ** 2; back[cand.nix[sp.keep], cand.niy[sp.keep]] = np.conj(back[cand.ix[sp.keep], cand.iy[sp.keep]])
    low = cand.kmag <= 8.0; mask = np.zeros((32, 32), bool); mask[cand.ix[low], cand.iy[low]] = True; mask[cand.nix[low], cand.niy[low]] = True
    check("split partitions the pairs; coordinates read back the field", ok and np.allclose(back[mask], wh[mask]), f"{sp.nc} consumer, {sp.npool} pool pairs")
    # 7. on a short flow record: rankings are permutations, NONE is the consumer alone, POD has the matched dimension
    dt = 0.01; Xr, Sr, Sat, _ = record_trajectory(model, wh, 6.0, dt, 0.5, cand, sp.keep, 1.0, lambda w: consumer_sens(model, w, cand, sp.pool, cm, 16))
    o, _ = rankings(Xr, Sr, Sat, sp, cand.kmag[sp.pool], 2, np.random.default_rng(6))
    perm = all(sorted(v.tolist()) == list(range(sp.npool)) for v in o.values())
    pr = Problem(Xr[:8], Xr[8:], sp, "rff", {**base, "horizons": [1, 2]}, 9); nd = pr.score(np.array([], int))["dim"]; pd = pr.score(pod_extra(Xr[:8], sp, 4))["dim"]
    check("rankings are permutations; NONE and POD dimensions", perm and nd == 1 + 2 * sp.nc + 64 and pd == nd + 4, f"NONE {nd}, POD(4) {pd}")
    # 8. the TEND observable equals D8's consumer tendency on a field holding only the chosen pairs (n = 96 against nt = 40)
    m96 = ForcedNS2D(96, 0.02, 0.1, 1.0, 4); c96 = Candidates(m96); s96 = Split(c96, 3.0, 12.0); kk = s96.keep
    full = initial_field(m96, np.random.default_rng(8), 12, 3.0); X1 = coords(m96, full, c96, kk)[None, :]; tf = make_tend(c96, s96); errs = []
    for sub in (np.arange(len(kk)), np.concatenate([np.arange(s96.nc), s96.nc + np.arange(5)])):
        only = np.zeros_like(full); k2 = kk[sub]
        only[c96.ix[k2], c96.iy[k2]] = full[c96.ix[k2], c96.iy[k2]]; only[c96.nix[k2], c96.niy[k2]] = full[c96.nix[k2], c96.niy[k2]]
        ref = -m96.nl_hat(only)[c96.ix[s96.cons], c96.iy[s96.cons]] / 96 ** 2; ref = np.concatenate([ref.real, ref.imag])
        errs.append(float(np.max(np.abs(tf(X1, sub)[0] - ref)) / np.max(np.abs(ref))))
    check("TEND = the consumer tendency on the chosen pairs (all recorded, and consumer plus 5)", max(errs) < 1e-10, ", ".join(f"{e:.1e}" for e in errs))
    # 9. READ-KE. The kinetic-energy norm is the velocity norm squared over (2 pi)^2
    e = abs(ke_sq(model, wh) * (2 * math.pi) ** 2 - vel_norm(model, wh) ** 2) / vel_norm(model, wh) ** 2
    check("ke_sq = velocity norm^2 / (2 pi)^2", e < 1e-12, f"{e:.1e}")
    # 10. READ-KE reduces to READ in the enstrophy norm: the sensitivity rows are READ's exactly, the order and score are
    # READ's, and adding the arm leaves every other order (the RANDOM draws included) unchanged
    s2 = consumer_sens(model, wh, cand, sp.pool[:5], cm, 4, (sq, sq))
    o0, sc0 = rankings(Xr, Sr, Sat, sp, cand.kmag[sp.pool], 2, np.random.default_rng(6))
    o1, sc1 = rankings(Xr, Sr, Sat, sp, cand.kmag[sp.pool], 2, np.random.default_rng(6), Sr)
    same = all(np.array_equal(o0[k], o1[k]) for k in o0)
    check("READ-KE in the enstrophy norm = READ (sensitivity, score, order); other orders unchanged",
          np.array_equal(s2[0], s) and np.array_equal(s2[1], s) and np.array_equal(sc1["read_ke"], sc1["read"]) and np.array_equal(o1["READ_KE"], o1["READ"]) and same, "")
    # 11. the kinetic-energy sensitivity equals the central difference of the consumer tendency measured in that norm
    s_both = consumer_sens(model, wh, cand, sp.pool[:5], cm, 4, (sq, ke_sq)); cdk = []
    for j in sp.pool[:5]:
        tot = 0.0
        for imag in (False, True):
            e = cand.unit(np.array([j]), 32, imag)[0]
            d = (-model.nl_hat(wh + eps * e) + model.nl_hat(wh - eps * e)) / (2 * eps); tot += ke_sq(model, cm * d)
        cdk.append(0.5 * tot)
    err = float(np.max(np.abs(np.array(cdk) - s_both[1])) / np.max(s_both[1]))
    check("kinetic-energy sensitivity = central difference of the consumer tendency in the KE norm", err < 1e-9 and np.array_equal(s_both[0], s), f"{err:.1e}")
    # 12. the two norms differ on the flow, so READ-KE is a different ranking and not a relabelling of READ
    check("the kinetic-energy sensitivity differs from the enstrophy one", not np.allclose(s_both[1], s) and np.all(s_both[1] >= 0), "")
    # 13. the whole world path on a tiny world: without READ-KE it writes the trajectory file; with it, the file is
    # simulated again, found identical, and given S_ke; a third pass reads it back. READ_KE is scored in every cell
    import tempfile
    tcfg = {**base, "F0": 1.0, "kf": 4, "alpha": 0.1, "omega_rms": 3.0, "ic_kmax": 6, "dt_base": 0.01, "n_ref": 32, "T_spin": 1.0,
            "T_train": 20.0, "T_test": 10.0, "dt_sample": 0.5, "sens_every": 2.0, "k_pool": 8.0, "cutoffs": [3], "ladder": [2, 4],
            "lifts": ["rff"], "horizons": [1, 2], "test_start_stride": 1, "random_draws": 2, "chunk": 64, "greedy_lifts": []}
    tw = {"name": "selftest_n32", "group": "probe", "nu": 0.02, "n": 32, "seed_offset": 0}; quiet = lambda *_: None
    with tempfile.TemporaryDirectory() as td:
        w0 = run_world(tw, tcfg, 11, quiet, td); z0 = dict(np.load(Path(td) / "selftest_n32_seed11.npz"))
        w1 = run_world(tw, tcfg, 11, quiet, td, read_ke=True); z1 = dict(np.load(Path(td) / "selftest_n32_seed11.npz"))
        w2 = run_world(tw, tcfg, 11, quiet, td, read_ke=True)
    c0, c1, c2 = (w["cutoffs"]["3"]["lifts"]["rff"] for w in (w0, w1, w2))
    kept = all(np.array_equal(z0[k], z1[k]) for k in ("Xtr", "S", "S_at", "Xte"))
    scored = all("READ_KE" in c1[str(r)] and c1[str(r)]["READ_KE"]["E"] == c2[str(r)]["READ_KE"]["E"] for r in (2, 4))
    unchanged = all(c0[str(r)][k]["E"] == c1[str(r)][k]["E"] for r in (2, 4) for k in ("READ", "ENERGY", "BALL", "SENS")) and all(c0[str(r)]["RANDOM_E"] == c1[str(r)]["RANDOM_E"] for r in (2, 4))
    check("world path: recheck identical, S_ke added and read back, READ_KE scored, other arms unchanged",
          "S_ke" not in z0 and z1["S_ke"].shape == z1["S"].shape and all(w1["trajectory_recheck"]["identical"].values()) and kept and scored and unchanged
          and "READ_KE" not in c0["2"] and w2.get("trajectory_cache") == "selftest_n32_seed11.npz", f"S_ke {z1['S_ke'].shape}")
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--config"); ap.add_argument("--seed-role", default="probe")
    ap.add_argument("--out", default="out.json"); ap.add_argument("--world", default=None)
    ap.add_argument("--traj-dir", default=None, help="cache the world's trajectories here (seed-deterministic; reused if present)")
    ap.add_argument("--read-ke", action="store_true", help="add the secondary arm READ_KE (the run registration's READ-KE)")
    a = ap.parse_args(argv)
    if a.selftest: return 1 if selftest() else 0
    run(json.load(open(a.config, encoding="utf-8")), a.seed_role, a.out, a.world, a.traj_dir, a.read_ke); return 0


if __name__ == "__main__":
    sys.exit(main())
