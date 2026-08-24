"""Grade QUANTUMREP-family.json against the sealed XPROTO-QUANTUM bars.

    python quantum_check.py [QUANTUMREP-family.json]          # grade (shakedown ok on aer)
    python quantum_check.py --seal [QUANTUMREP-family.json]   # seal: REFUSES unless real hardware

Bars (committed in PREREG-XPROTO-QUANTUM.md before the graded run):
  B1  min naive_fc      >= 0.25   aggregate device cert false-clears per-circuit
  B2  max aware_fc      <= 0.10   footprint-aware cert holds
  B3  aware_fc <= naive_fc/2      per seed (dominance)
Manipulation checks (any fail => VOID):
  MC1 device_certified True       the device passes its aggregate benchmark
  MC2 good-fp success >= target   the device works for good footprints
  MC3 non-degenerate              n>=30 footprints and naive_fc<1 (a real mix)
"""
import json
import sys

B1_NAIVE_MIN = 0.25
B2_AWARE_MAX = 0.10
MC3_MIN_N = 30


def grade(path="QUANTUMREP-family.json", seal=False):
    rec = json.load(open(path))
    if seal and rec.get("mode") != "hardware":
        print(f"REFUSE-TO-SEAL: mode '{rec.get('mode')}' is model validation, not "
              "evidence (hand-constructed device). The sealed rung requires real IBM "
              "hardware per PREREG-XPROTO-QUANTUM.md. Grade the shakedown without --seal.")
        return False
    cells = rec["cells"]
    naive = [c["naive_fc"] for c in cells]
    aware = [c["aware_fc"] for c in cells]

    b1 = min(naive) >= B1_NAIVE_MIN
    b2 = max(aware) <= B2_AWARE_MAX
    b3 = all(a <= n / 2 for a, n in zip(aware, naive))
    mc1 = all(c["device_certified"] for c in cells)
    mc2 = all(c["good_footprint_success_rate"] >= c["target_success"] for c in cells)
    mc3 = all(c["n_footprints"] >= MC3_MIN_N and c["naive_fc"] < 1.0 for c in cells)

    print(f"XPROTO-QUANTUM  ({rec.get('mode','?')})  n_seeds={len(cells)}")
    for c in cells:
        print(f"  seed {c['seed']}: naive_fc={c['naive_fc']:.3f} aware_fc={c['aware_fc']:.3f} "
              f"| agg_fid={c['aggregate_fidelity']} good-fp={c['good_footprint_success_rate']:.3f}")
    checks = [
        ("B1 min naive_fc>=0.25", b1, f"min={min(naive):.3f}"),
        ("B2 max aware_fc<=0.10", b2, f"max={max(aware):.3f}"),
        ("B3 aware<=naive/2", b3, "per-seed"),
        ("MC1 device certified", mc1, ""),
        ("MC2 good-fp success>=target", mc2, ""),
        ("MC3 non-degenerate", mc3, ""),
    ]
    ok = True
    for name, val, extra in checks:
        print(f"  [{'PASS' if val else 'FAIL'}] {name} {extra}")
        ok = ok and val
    mc_ok = mc1 and mc2 and mc3
    verdict = "PASS" if ok else ("VOID" if not mc_ok else "FAIL")
    print(f"VERDICT: {verdict}")
    return ok


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--seal"]
    seal = "--seal" in sys.argv[1:]
    sys.exit(0 if grade(*args, seal=seal) else 1)
