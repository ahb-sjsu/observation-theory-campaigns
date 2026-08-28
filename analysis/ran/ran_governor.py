"""governor.ran -- reference RAN freshness governor (the O-RAN rApp core).

Observe certificate + witness streams; measure the per-(certificate, consumer)
false-clear rate and the refresh floor (from the certificate's coherence time);
emit a GovernanceDecision + a calibrated, witnessed certificate. The RAN
generalization of governor.sealed / governor.detector.

The governance logic encodes the sealed cells' lessons:
  * refresh at the floor: if a certificate is vacuous and its report period
    exceeds the coherence floor, refresh faster -- down to the floor. (The
    proportional floor model this uses rests on a superseded exploration; see
    the K_FLOOR note below. The governance direction is unaffected, but the
    floor value is heuristic, not measured.)
  * mechanism, not parameter (URLLC / NTN): if it is already at the floor and
    still vacuous, refreshing cannot close the loop (deep-fade- or delay-limited)
    -- switch mechanism (diversity for a link certificate; route elsewhere for a
    serving/beam certificate).
  * certify against the witness, per consumer (the reliability target is the
    read operator): the same certificate is certified for a lax consumer and
    vacuous for a strict one.

Self-contained (numpy + stdlib). This is a reference/skeleton, not a production
xApp; the E2SM-KPM ingest and E2SM-RC actuation are the integration surface.
"""
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass

import numpy as np

# SUPERSEDED PROVENANCE (annotated 2026-08-27). K_FLOOR came from the
# exploration in analysis/csi/csi_sweep.py, which was never sealed and which
# measured its floors at a relaxed 0.15 BLER threshold while reporting against
# a 0.10 target. The sealed recompute XPROTO-CSI-SWEEP2 (2026-08-27) finds no
# proportional law at the true budget: the admissible period is 4-6 TTI at
# 10 Hz Doppler, 2-3 at 25 Hz, and 1 TTI at 50 Hz and above.
# The value is retained UNCHANGED as an explicit heuristic so this reference
# implementation keeps working, and because replacing the proportional model
# with the measured per-Doppler floors is a design decision, not a provenance
# fix. It is NOT a measured constant. Do not cite it as one.
K_FLOOR = 0.177          # heuristic slope (floor = K * T_coh); see note above
LINK_CERTS = {"cqi", "csi", "pmi", "ri"}          # fixable by diversity
SERVING_CERTS = {"beam", "rsrp"}                   # fixable by re-routing


@dataclass(frozen=True)
class Consumer:
    name: str
    target: float        # reliability budget: max tolerable false-clear rate


@dataclass
class GovernanceDecision:
    cert: str
    consumer: str
    false_clear: float
    target: float
    vacuous: bool
    refresh_floor_slots: float
    report_period_slots: int
    recommend_report_period: int
    mechanism: str        # "ok" | "refresh_faster" | "add_diversity" | "route_elsewhere"
    certified: bool       # the calibrated certificate clears for this consumer


class FalseClearMeter:
    """Rolling fraction of witnessed failures (NACKs)."""
    def __init__(self, window: int = 500):
        self._w = deque(maxlen=window)

    def observe(self, witness_ok: bool):
        self._w.append(0 if witness_ok else 1)

    @property
    def rate(self) -> float:
        return sum(self._w) / len(self._w) if self._w else 0.0


class RefreshFloorEstimator:
    """Coherence time of the certificate value stream -> refresh floor."""
    def __init__(self, window: int = 512):
        self._v = deque(maxlen=window)

    def observe(self, value: float):
        self._v.append(float(value))

    def coherence_slots(self) -> float:
        x = np.array(self._v, float)
        if len(x) < 32:
            return float("nan")
        x = x - x.mean()
        var = float(np.dot(x, x))
        if var <= 0:
            return float("nan")
        for lag in range(1, len(x) // 2):
            if np.dot(x[:-lag], x[lag:]) / var < np.exp(-1):   # 1/e crossing
                return float(lag)
        return float(len(x) // 2)

    def floor_slots(self) -> float:
        tc = self.coherence_slots()
        return K_FLOOR * tc if tc == tc else float("nan")


class RanGovernor:
    """observe -> measure -> govern -> certify, per (certificate, consumer)."""
    def __init__(self, window: int = 500):
        self._meter: dict = defaultdict(lambda: FalseClearMeter(window))
        self._floor: dict = defaultdict(RefreshFloorEstimator)
        self._consumers: dict = {}

    def register(self, consumer: Consumer):
        self._consumers[consumer.name] = consumer

    def observe(self, cert: str, consumer: str, value: float, witness_ok: bool):
        self._meter[(cert, consumer)].observe(witness_ok)
        self._floor[cert].observe(value)

    def govern(self, cert: str, consumer: str, report_period_slots: int) -> GovernanceDecision:
        c = self._consumers[consumer]
        fc = self._meter[(cert, consumer)].rate
        floor = self._floor[cert].floor_slots()
        vacuous = fc > c.target
        rp = report_period_slots
        mech = "ok"
        if vacuous:
            if floor == floor and report_period_slots > floor:
                rp = max(int(round(floor)), 1); mech = "refresh_faster"
            else:                                   # already at the floor -> mechanism
                mech = "add_diversity" if cert in LINK_CERTS else \
                    ("route_elsewhere" if cert in SERVING_CERTS else "add_diversity")
        return GovernanceDecision(
            cert=cert, consumer=consumer, false_clear=round(fc, 4), target=c.target,
            vacuous=vacuous, refresh_floor_slots=round(floor, 2) if floor == floor else float("nan"),
            report_period_slots=report_period_slots, recommend_report_period=rp,
            mechanism=mech, certified=not vacuous)
