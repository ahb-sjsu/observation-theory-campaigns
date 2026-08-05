#!/usr/bin/env python3
"""Shared exact machinery for EG-2 through EG-4 on the
causal-determinism substrate.

The substrate is the one that passed the EG-1b gate, a deterministic
radius-one cellular automaton on a ring, with additive rules so that
every hidden spacetime cell is a GF(2)-linear functional of the
generator set (the i.i.d. uniform initial row, plus any declared
noise bits). Every ensemble marginal on a window of spacetime cells
is then uniform on the image subspace of a boolean matrix, and every
entropy, relative entropy, and equality-of-distribution question is
exact subspace arithmetic:

  H(window)                = rank(M_W) bits,
  distributions equal      iff the two image subspaces coincide,
  D(mat || vac) finite     iff im(mat) is contained in im(vac),
                           and then D = rank_vac - rank_mat bits,
  D infinite               iff the deformed support leaves the vacuum
                           support (the EG-0 support-floor semantics).

Vacuum dynamics is rule 90. A matter source is a declared set of
defect cells that use rule 150 instead, a rule substitution containing
no function of distance and no potential, so the EG-2
reverse-engineering audit is structural. Noise, where declared, is a
fresh generator XORed into a stated cell at a stated step.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from eg1b_mechanism import gf2_rank  # noqa: E402


def evolve_generators(n_ring: int, n_steps: int,
                      defect_cells: frozenset[int] = frozenset(),
                      noise_events: tuple[tuple[int, int], ...] = ()):
    """Return the list G[t] of boolean generator matrices, one per
    time 0..n_steps. G[t][j] expresses ring cell j at time t over the
    generator basis: n_ring initial bits followed by one bit per
    noise event. Vacuum rule 90; defect cells use rule 150; a noise
    event (t, j) XORs a fresh generator into cell j at time t."""
    n_noise = len(noise_events)
    ncols = n_ring + n_noise
    gen = np.zeros((n_ring, ncols), dtype=bool)
    gen[:, :n_ring] = np.eye(n_ring, dtype=bool)
    noise_index = {ev: n_ring + k for k, ev in enumerate(noise_events)}
    for j in range(n_ring):
        if (0, j) in noise_index:
            gen[j, noise_index[(0, j)]] = True
    history = [gen.copy()]
    defect = np.zeros(n_ring, dtype=bool)
    for c in defect_cells:
        defect[c % n_ring] = True
    for t in range(1, n_steps + 1):
        nxt = np.roll(gen, 1, axis=0) ^ np.roll(gen, -1, axis=0)
        nxt[defect] ^= gen[defect]
        for j in range(n_ring):
            if (t, j) in noise_index:
                nxt[j, noise_index[(t, j)]] ^= True
        gen = nxt
        history.append(gen.copy())
    return history


def window_matrix(history, cells):
    """Boolean matrix whose rows are the generator expressions of the
    listed spacetime cells (t, j)."""
    return np.stack([history[t][j % history[0].shape[0]]
                     for t, j in cells], axis=0)


def pad_columns(a: np.ndarray, ncols: int) -> np.ndarray:
    if a.shape[1] == ncols:
        return a
    out = np.zeros((a.shape[0], ncols), dtype=bool)
    out[:, :a.shape[1]] = a
    return out


def image_relation(m_mat: np.ndarray, m_vac: np.ndarray):
    """Classify the deformed window marginal against the vacuum one.

    The distribution of the window cells y = M u for uniform u is
    uniform on the span of the COLUMNS of M read as vectors in
    F2^|W|, so the comparison works on transposes. Returns one of
    ("equal", 0.0), ("nested", D bits), ("escaped", inf)."""
    ncols = max(m_mat.shape[1], m_vac.shape[1])
    a = pad_columns(m_mat, ncols).T.copy()
    b = pad_columns(m_vac, ncols).T.copy()
    ra = gf2_rank(a)
    rb = gf2_rank(b)
    r_join = gf2_rank(np.concatenate([a, b], axis=0))
    if r_join == ra == rb:
        return "equal", 0.0
    if r_join == rb:
        return "nested", float(rb - ra)
    return "escaped", float("inf")


def marginal_entropy_bits(m: np.ndarray) -> int:
    """H(window) in bits for the uniform-generator ensemble."""
    return gf2_rank(m.T.copy())
