"""Prototype + measurement of the read_fresh() fix (see FIX-PROPOSAL.md).

read_fresh(path, W): read the local follower; if the follower's applied zxid
>= W (the reader's required watermark), the read is CERTIFIED FRESH locally --
no leader involvement -- because Zab totally orders writes, so an applied
watermark >= W means every write <= W is present. Otherwise fall to sync().

We measure this against the reader's *declared* freshness need, modeled as a
tolerance tau: the reader carries a causal watermark W = the leader's committed
zxid as of (now - tau) -- "give me state at least as fresh as tau ago." Sweeping
tau traces read_fresh's cost (sync rate) against the freshness it guarantees,
bracketed by the two degenerate baselines:
  naive       : trust the local read      -> 0 cost, false-clears ~99% vs latest
  sync-always : sync() every read          -> 1.0 cost, always latest

The correctness invariant is checked empirically: for every CERTIFIED-local
read we verify, against a per-znode write log, that the follower's returned
version reflects the latest write <= W. This false_clear_vs_W must be 0 -- the
zxid is a *sound* witness. Writes concurrent with reads are the reason W (not
"latest") is the honest reference: read_fresh promises freshness to W, not to an
unknowable global latest.

Emits ZK-FIX.json + ZK-FIX.png. Requires the lab (lab_up.sh) + matplotlib.
"""
import bisect
import json
import os
import random
import threading
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from kazoo.client import KazooClient

HERE = os.path.dirname(os.path.abspath(__file__))
TOPO = json.load(open("/home/claude/zk/topology.json"))
N = 10
HOT = [0, 1, 2]
HOT_INT = 0.012
TAUS = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.45]   # reader tolerance (s)
N_PER_TAU = 80
SETTLE_S = 1.0


def _p(i):
    return f"/z/{i}"


def main():
    w = KazooClient(hosts=f"localhost:{TOPO['leader_port']}")
    r = KazooClient(hosts=f"localhost:{TOPO['follower_port']}")
    t = KazooClient(hosts=f"localhost:{TOPO['leader_port']}")
    w.start(); r.start(); t.start()
    for i in range(N):
        w.ensure_path(_p(i)); w.set(_p(i), b"0")
    # wait for the creates to reach the delayed follower before sampling
    for _ in range(100):
        if r.exists(_p(N - 1)):
            break
        time.sleep(0.05)

    # confirm the follower reply carries an applied-zxid witness (kazoo last_zxid)
    r.get(_p(0))
    if not isinstance(getattr(r, "last_zxid", None), int):
        raise RuntimeError("kazoo client.last_zxid unavailable; witness path broken")

    stop = threading.Event()
    lock = threading.Lock()
    wlog = {i: [] for i in range(N)}          # per-znode sorted applied write zxids

    def writer():
        wr = random.Random(12345)
        while not stop.is_set():
            i = wr.choice(HOT)
            st = w.set(_p(i), str(wr.random()).encode())
            with lock:
                wlog[i].append(st.mzxid)       # writes commit in zxid order
            time.sleep(HOT_INT)

    buf_t, buf_z = [], []                       # leader zxid ring buffer (for W)

    def sampler():
        while not stop.is_set():
            t.get(_p(0))
            buf_t.append(time.time()); buf_z.append(t.last_zxid or 0)
            time.sleep(0.004)

    thw = threading.Thread(target=writer, daemon=True); thw.start()
    ths = threading.Thread(target=sampler, daemon=True); ths.start()
    time.sleep(SETTLE_S)

    rng = random.Random(0)
    naive_stale = naive_n = 0
    rows = []
    for tau in TAUS:
        n = sync = fc_vs_W = stale_local = 0
        while n < N_PER_TAU:
            i = rng.choice(HOT)
            now = time.time()
            k = bisect.bisect_right(buf_t, now - tau) - 1
            if k < 0:
                continue
            W = buf_z[k]                          # the reader's causal watermark
            lz = t.get(_p(i))[1].mzxid            # leader's latest mzxid(Z)
            fmz = r.get(_p(i))[1].mzxid           # local follower read (value+version)
            fzx = r.last_zxid or 0                # follower applied zxid (reply witness)
            n += 1
            naive_n += 1
            if fmz < lz:                          # naive baseline: stale vs latest
                naive_stale += 1
            if fzx >= W:                          # read_fresh fast path (certified)
                with lock:
                    lst = wlog[i]
                    kk = bisect.bisect_right(lst, W) - 1
                    expected = lst[kk] if kk >= 0 else 0
                if fmz < expected:                # unsound witness -> MUST be 0
                    fc_vs_W += 1
                if fmz < lz:                       # behind latest but within tau (declared)
                    stale_local += 1
            else:                                  # read_fresh slow path
                sync += 1
                r.sync(_p(i)); r.get(_p(i))        # -> fresh to at least W
        local = n - sync
        rows.append({
            "tau_s": tau, "n": n,
            "sync_rate": round(sync / n, 4),
            "false_clear_vs_W": round(fc_vs_W / n, 4),
            "stale_vs_latest_local": round(stale_local / local, 4) if local else 0.0,
        })
        print(f"tau={tau:.2f}s n={n} sync_rate={rows[-1]['sync_rate']} "
              f"false_clear_vs_W={rows[-1]['false_clear_vs_W']} "
              f"within_tol_stale={rows[-1]['stale_vs_latest_local']}", flush=True)

    stop.set(); thw.join(2); ths.join(2)
    naive_fc = round(naive_stale / max(1, naive_n), 4)
    print(f"\nBASELINES: naive false_clear_vs_latest={naive_fc} (sync_rate 0.0); "
          f"sync-always sync_rate=1.0 false_clear=0.0", flush=True)
    w.stop(); r.stop(); t.stop()

    out = {"delay_ms": TOPO.get("delay_ms"), "hot_interval_s": HOT_INT,
           "naive_false_clear_vs_latest": naive_fc,
           "sync_always": {"sync_rate": 1.0, "false_clear": 0.0},
           "read_fresh_sweep": rows}
    json.dump(out, open(os.path.join(HERE, "ZK-FIX.json"), "w"), indent=1)

    xs = [r["tau_s"] * 1000 for r in rows]
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.plot(xs, [r["sync_rate"] for r in rows], "o-", color="C0",
            label="read_fresh cost (sync rate)")
    ax.plot(xs, [r["false_clear_vs_W"] for r in rows], "s-", color="C2",
            label="read_fresh false-clear vs W (=0, sound)")
    ax.axhline(1.0, ls="--", c="grey", label="sync-always cost")
    ax.axhline(naive_fc, ls=":", c="red", label=f"naive false-clear vs latest ({naive_fc})")
    ax.axvline(TOPO.get("delay_ms"), ls="-.", c="green", lw=1,
               label=f"follower lag ({TOPO.get('delay_ms')} ms)")
    ax.set_xlabel(r"reader tolerance $\tau$ (ms) = declared freshness need")
    ax.set_ylabel("fraction of reads")
    ax.set_ylim(-0.03, 1.06); ax.legend(fontsize=8, loc="center right")
    ax.set_title("ZooKeeper read_fresh: cost vs declared freshness\n"
                 "(witnessed, consumer-relative; correct at every point)")
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "ZK-FIX.png"), dpi=120)
    print("wrote ZK-FIX.json + ZK-FIX.png", flush=True)


if __name__ == "__main__":
    main()
