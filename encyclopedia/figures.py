"""Draw one schematic per entry, in the book's figure style.

    python encyclopedia/figures.py

Writes encyclopedia/figures/<id>.svg for every entry in entries.toml. Each figure is a
schematic of the entry's core idea, drawn from a small library of templates with the same
palette, marks, and type as the book's figures (svgfig.py mirrors the book's
tools/svgfig.py). The accent colour follows the entry's kind. No figure carries a measured
number; the numbers live in the entry's measurement rows.
"""
import math
import os
import sys
import tomllib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgfig import Canvas, Axes, INK, INK2, INK3, GRID, SERIES, SURFACE, CRITICAL, GOOD  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)
W, H = 720, 300
ACCENT = {"concept": SERIES[0], "instrument": SERIES[2], "result": SERIES[1], "correction": CRITICAL, "reference": SERIES[6]}
PALE = "#dfe9f6"


def canvas():
    return Canvas(W, H, "")


def note(c, s, y=H - 14):
    c.text(16, y, s, 11.5, "start", INK2, italic=True)


def rng(seed):
    """A tiny deterministic generator so figures are reproducible without numpy."""
    x = seed * 2654435761 % 2 ** 32

    def nxt():
        nonlocal x
        x = (1103515245 * x + 12345) % 2 ** 31
        return x / 2 ** 31
    return nxt


def gauss(r):
    u1, u2 = max(r(), 1e-9), r()
    return math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)


# ================================================================ templates
def t_angle(c, acc, a="x", b="y", deg=40, proj=False, residual=False, note_=""):
    ox, oy = 250, 235
    la, lb = 260, 200
    c.line(ox - 30, oy, ox + 300, oy, GRID, 1)
    c.line(ox, oy + 20, ox, oy - 210, GRID, 1)
    ang = math.radians(deg)
    bx, by = ox + lb * math.cos(ang), oy - lb * math.sin(ang)
    c.arrow(ox, oy, ox + la, oy, INK, 2)
    c.arrow(ox, oy, bx, by, acc, 2)
    c.text(ox + la + 8, oy + 4, a, 13, "start", INK)
    c.text(bx + 8, by, b, 13, "start", INK)
    pts = [(ox + 60 * math.cos(t), oy - 60 * math.sin(t)) for t in [i * ang / 20 for i in range(21)]]
    c.polyline(pts, INK2, 1.5)
    c.text(ox + 78 * math.cos(ang / 2), oy - 78 * math.sin(ang / 2) + 4, "θ", 12, "middle", INK2, italic=True)
    if proj:
        px = ox + lb * math.cos(ang)
        c.line(bx, by, px, oy, INK3, 1.5, dash="4 4")
        c.hrect(ox, oy - 4, px - ox, 8, acc, opacity=0.35)
        c.text((ox + px) / 2, oy + 20, "projection of " + b + " on " + a, 11, "middle", INK2)
        if residual:
            c.text(px + 8, (by + oy) / 2, "residual, orthogonal", 11, "start", INK2)
    if note_:
        note(c, note_)


def t_venn(c, acc, a="A", b="B", nested=False, disjoint=False, note_="", third=None):
    cx, cy = 300, 150
    if nested:
        c.ellipse(cx, cy, 150, 100, 0, INK, "none", 2)
        c.ellipse(cx - 40, cy + 10, 70, 50, 0, acc, acc, 2, 0.15)
        c.text(cx + 60, cy - 60, a, 13, "middle", INK)
        c.text(cx - 40, cy + 14, b, 13, "middle", INK)
    elif disjoint:
        c.ellipse(cx - 110, cy, 90, 70, 0, INK, "none", 2)
        c.ellipse(cx + 110, cy, 90, 70, 0, acc, acc, 2, 0.15)
        c.text(cx - 110, cy + 4, a, 13, "middle", INK)
        c.text(cx + 110, cy + 4, b, 13, "middle", INK)
    else:
        c.ellipse(cx - 55, cy, 110, 80, 0, INK, "none", 2)
        c.ellipse(cx + 55, cy, 110, 80, 0, acc, acc, 2, 0.15)
        c.text(cx - 120, cy + 4, a, 13, "middle", INK)
        c.text(cx + 120, cy + 4, b, 13, "middle", INK)
        c.text(cx, cy + 4, a + " ∩ " + b, 12, "middle", INK)
    if third:
        c.text(cx, cy + 118, third, 11.5, "middle", INK2)
    if note_:
        note(c, note_)


def t_matrix(c, acc, n=6, pattern="diag", note_="", label=None):
    s = 30
    x0, y0 = 260, 40
    for i in range(n):
        for j in range(n):
            if pattern == "diag":
                v = 1.0 if i == j else 0.08
            elif pattern == "symmetric":
                v = 0.25 + 0.6 * abs(math.sin(0.9 * (i + 1) * (j + 1)))
            elif pattern == "outer":
                v = ((n - i) / n) * ((n - j) / n)
            elif pattern == "lowrank":
                v = 0.9 if (i < 2 or j < 2) else 0.12
            elif pattern == "kernel":
                v = 0.9 if (i < 3 and j < 3) else 0.06
            elif pattern == "block":
                v = 0.85 if (i // 3 == j // 3) else 0.05
            elif pattern == "band":
                v = 0.9 if abs(i - j) <= 1 else 0.06
            else:
                v = 0.5
            c.add(f'<rect x="{x0 + j * s}" y="{y0 + i * s}" width="{s - 2}" height="{s - 2}" rx="3" fill="{acc}" fill-opacity="{0.08 + 0.85 * v:.2f}"/>')
    if label:
        c.text(x0 + n * s / 2, y0 + n * s + 22, label, 11.5, "middle", INK2)
    if note_:
        note(c, note_)


def t_ellipses(c, acc, deg=15, same=True, circle=False, note_="", second=True, labels=("first code", "second code")):
    cx, cy, s = 240, 155, 85
    c.line(cx - 170, cy, cx + 170, cy, GRID, 1)
    c.line(cx, cy - 120, cx, cy + 120, GRID, 1)
    if circle:
        c.ellipse(cx, cy, s, s, 0, acc, acc, 2, 0.12)
    else:
        c.ellipse(cx, cy, s * math.sqrt(0.3), s * math.sqrt(1.7), 0, SERIES[0], SERIES[0], 2, 0.10, title=labels[0])
        if second:
            c.ellipse(cx, cy, s * math.sqrt(1.7), s * math.sqrt(0.3), 0, SERIES[1], SERIES[1], 2, 0.10, title=labels[1])
    ang = math.radians(deg)
    ux, uy = math.cos(ang), -math.sin(ang)
    c.arrow(cx, cy, cx + 150 * ux, cy + 150 * uy, INK, 2)
    c.text(cx + 160 * ux + 4, cy + 160 * uy, "reader", 12, "start", INK)
    if not circle:
        c.add(f'<rect x="470" y="60" width="12" height="12" rx="3" fill="{SERIES[0]}"/>')
        c.text(488, 70, labels[0], 11.5, "start", INK2)
        if second:
            c.add(f'<rect x="470" y="82" width="12" height="12" rx="3" fill="{SERIES[1]}"/>')
            c.text(488, 92, labels[1], 11.5, "start", INK2)
        if same:
            c.text(470, 116, "same trace", 11.5, "start", INK2, italic=True)
    if note_:
        note(c, note_)


def t_spectrum(c, acc, vals=None, kept=None, water=None, note_="", ylabel="eigenvalue", xlabel="direction"):
    vals = vals or [1.0, 0.62, 0.38, 0.22, 0.12, 0.07, 0.04, 0.02]
    ax = Axes(c, 90, 30, 560, 200, (0, len(vals)), (0, max(vals) * 1.1), (), (), xlabel, ylabel)
    bw = 560 / len(vals) * 0.6
    for i, v in enumerate(vals):
        col = acc if (kept is None or i < kept) else INK3
        x = ax.X(i + 0.5) - bw / 2
        c.rect(x, ax.Y(v), bw, ax.Y(0) - ax.Y(v), col)
    if water is not None:
        y = ax.Y(water)
        c.line(ax.x0, y, ax.x0 + ax.w, y, SERIES[1], 2, dash="6 4")
        c.text(ax.x0 + ax.w - 4, y - 6, "water level", 11, "end", INK2)
    if kept is not None:
        c.line(ax.X(kept), ax.y0, ax.X(kept), ax.y0 + ax.h, INK2, 1.5, dash="4 4")
        c.text(ax.X(kept) + 6, ax.y0 + 14, "kept | dropped", 11, "start", INK2)
    if note_:
        note(c, note_)


def _nodes(seed, n, cx=300, cy=150, rx=200, ry=105):
    r = rng(seed)
    return [(cx + (2 * r() - 1) * rx, cy + (2 * r() - 1) * ry) for _ in range(n)]


def t_graph(c, acc, kind="hub", note_="", n=14):
    if kind == "ring":
        pts = [(300 + 110 * math.cos(2 * math.pi * i / 10), 150 + 110 * math.sin(2 * math.pi * i / 10)) for i in range(10)]
        for i in range(10):
            a, b = pts[i], pts[(i + 1) % 10]
            c.line(a[0], a[1], b[0], b[1], INK3, 1.5)
        for p in pts:
            c.dot(p[0], p[1], acc, 5)
        c.line(300, 150, pts[2][0], pts[2][1], INK2, 1.5, dash="4 4")
        c.text(300, 155, "·", 12, "middle", INK)
        c.text(470, 60, "angle kept, radius is degree noise", 11.5, "start", INK2)
    else:
        pts = _nodes(7, n)
        hub = (300, 150)
        for i, p in enumerate(pts):
            for q in pts[i + 1:]:
                if math.hypot(p[0] - q[0], p[1] - q[1]) < 95:
                    c.line(p[0], p[1], q[0], q[1], GRID, 1.5)
        if kind == "hub":
            for p in pts:
                if math.hypot(p[0] - hub[0], p[1] - hub[1]) < 190:
                    c.line(hub[0], hub[1], p[0], p[1], acc, 1.2, opacity=0.6)
        if kind == "path":
            path = sorted(pts, key=lambda p: p[0])[:6]
            c.polyline(path, acc, 2.5)
            c.text(path[0][0] - 8, path[0][1] - 10, "i", 12, "end", INK)
            c.text(path[-1][0] + 8, path[-1][1] - 10, "j", 12, "start", INK)
        if kind == "knn":
            for p in pts:
                near = sorted(pts, key=lambda q: math.hypot(p[0] - q[0], p[1] - q[1]))[1:3]
                for q in near:
                    c.line(p[0], p[1], q[0], q[1], acc, 1.5, opacity=0.7)
        for p in pts:
            c.dot(p[0], p[1], INK2, 4)
        if kind == "hub":
            c.dot(hub[0], hub[1], acc, 8, title="hub")
            c.text(hub[0] + 14, hub[1] - 10, "hub", 12, "start", INK)
        if kind == "antihub":
            far = (600, 60)
            c.dot(far[0], far[1], acc, 6)
            c.text(far[0] - 12, far[1] + 4, "anti-hub, never retrieved", 11.5, "end", INK)
    if note_:
        note(c, note_)


def t_histogram(c, acc, shape="poisson", ceiling=None, threshold=None, note_="", xlabel="count", right_tail=True):
    if shape == "poisson":
        vals = [2, 7, 13, 17, 16, 12, 8, 5, 3, 2, 1, 1, 0, 0, 0, 0, 3, 0, 5]
    elif shape == "skew":
        vals = [20, 17, 13, 10, 8, 6, 5, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1]
    else:
        vals = [1, 2, 4, 7, 11, 15, 17, 16, 13, 9, 6, 3, 2, 1, 1, 0, 0, 0, 0]
    ax = Axes(c, 80, 30, 570, 200, (0, len(vals)), (0, max(vals) * 1.15), (), (), xlabel, "rows")
    bw = 570 / len(vals) * 0.7
    for i, v in enumerate(vals):
        col = acc
        if threshold is not None and i >= threshold:
            col = CRITICAL
        if ceiling is not None and i >= ceiling and v > 0:
            col = CRITICAL
        c.rect(ax.X(i + 0.5) - bw / 2, ax.Y(v), bw, ax.Y(0) - ax.Y(v), col)
    if ceiling is not None:
        c.line(ax.X(ceiling), ax.y0, ax.X(ceiling), ax.y0 + ax.h, INK, 1.5, dash="5 4")
        c.text(ax.X(ceiling) + 6, ax.y0 + 14, "ceiling", 11.5, "start", INK2)
    if threshold is not None:
        c.line(ax.X(threshold), ax.y0, ax.X(threshold), ax.y0 + ax.h, INK, 1.5, dash="5 4")
        c.text(ax.X(threshold) + 6, ax.y0 + 14, "threshold", 11.5, "start", INK2)
    if note_:
        note(c, note_)


def t_roc(c, acc, point=None, youden=False, calibration=False, note_="", second=None):
    ax = Axes(c, 110, 30, 300, 215, (0, 1), (0, 1), [0, 0.5, 1], [0, 0.5, 1],
              "true fraction" if calibration else "false positive rate", "positive fraction" if calibration else "true positive rate")
    c.line(ax.X(0), ax.Y(0), ax.X(1), ax.Y(1), INK3, 1.5, dash="5 4")
    if calibration:
        pts = [(x, x + 0.18 * math.sin(math.pi * x)) for x in [i / 10 for i in range(11)]]
        c.polyline([(ax.X(x), ax.Y(min(1, y))) for x, y in pts], acc, 2.5)
        for x, y in pts[1:-1:2]:
            c.dot(ax.X(x), ax.Y(min(1, y)), acc, 4)
        c.text(430, 80, "bins above the diagonal", 11.5, "start", INK2)
        c.text(430, 98, "score below the observed rate", 11.5, "start", INK2)
    else:
        pts = [(x, x ** 0.35) for x in [i / 40 for i in range(41)]]
        c.polyline([(ax.X(x), ax.Y(y)) for x, y in pts], acc, 2.5)
        if second:
            pts2 = [(x, x ** 0.7) for x in [i / 40 for i in range(41)]]
            c.polyline([(ax.X(x), ax.Y(y)) for x, y in pts2], SERIES[1], 2.5)
            c.text(430, 120, second, 11.5, "start", INK2)
        if point:
            c.dot(ax.X(point[0]), ax.Y(point[1]), INK, 5)
            c.text(ax.X(point[0]) + 10, ax.Y(point[1]) + 4, "operating point", 11.5, "start", INK)
        if youden:
            x = 0.15
            c.line(ax.X(x), ax.Y(x), ax.X(x), ax.Y(x ** 0.35), SERIES[1], 2.5)
            c.text(ax.X(x) + 8, ax.Y((x + x ** 0.35) / 2), "Youden index, TPR − FPR", 11.5, "start", INK2)
        c.text(430, 80, "area under the curve, AUROC", 11.5, "start", INK2)
        c.text(430, 98, "chance is the diagonal", 11.5, "start", INK2)
    if note_:
        note(c, note_)


def t_sigmoid(c, acc, note_="", threshold=True):
    ax = Axes(c, 90, 30, 540, 210, (-6, 6), (0, 1), [-6, -3, 0, 3, 6], [0, 0.5, 1], "weighted sum", "score")
    pts = [(z, 1 / (1 + math.exp(-z))) for z in [i / 5 - 6 for i in range(61)]]
    c.polyline([(ax.X(z), ax.Y(y)) for z, y in pts], acc, 2.5)
    if threshold:
        c.line(ax.X(-6), ax.Y(0.5), ax.X(6), ax.Y(0.5), INK3, 1.5, dash="5 4")
        c.line(ax.X(0), ax.Y(0), ax.X(0), ax.Y(1), INK3, 1.5, dash="5 4")
        c.text(ax.X(0) + 8, ax.Y(0.93), "decision boundary at zero", 11.5, "start", INK2)
    if note_:
        note(c, note_)


def t_parabola(c, acc, note_="", secant=True, tangent=True):
    ax = Axes(c, 90, 30, 540, 210, (-2, 2), (0, 4.4), [-2, -1, 0, 1, 2], (), "x", "C(x)")
    pts = [(x, x * x) for x in [i / 20 - 2 for i in range(81)]]
    c.polyline([(ax.X(x), ax.Y(y)) for x, y in pts], acc, 2.5)
    x0, h = 0.8, 0.6
    if secant:
        c.line(ax.X(x0 - h), ax.Y((x0 - h) ** 2), ax.X(x0 + h), ax.Y((x0 + h) ** 2), SERIES[1], 2)
        c.dot(ax.X(x0 - h), ax.Y((x0 - h) ** 2), SERIES[1], 4)
        c.dot(ax.X(x0 + h), ax.Y((x0 + h) ** 2), SERIES[1], 4)
        c.text(ax.X(x0 + h) + 8, ax.Y((x0 + h) ** 2), "central difference", 11.5, "start", INK2)
    if tangent:
        m = 2 * x0
        c.line(ax.X(x0 - 1), ax.Y(x0 * x0 - m), ax.X(x0 + 0.9), ax.Y(x0 * x0 + 0.9 * m), INK, 1.5, dash="5 4")
        c.text(ax.X(x0 - 1) - 6, ax.Y(x0 * x0 - m) + 4, "tangent, the derivative", 11.5, "end", INK2)
    c.dot(ax.X(x0), ax.Y(x0 * x0), INK, 4)
    if note_:
        note(c, note_)


def t_cliff(c, acc, note_="", xlabel="probe directions over dimension, k/d", ylabel="recovery"):
    ax = Axes(c, 100, 30, 540, 210, (0, 2), (0, 1.05), [0, 0.5, 1, 1.5, 2], [0, 0.5, 1], xlabel, ylabel)
    pts = [(x, 0.05 + 0.1 * x) for x in [i / 20 for i in range(20)]] + [(1, 0.15), (1, 1.0)] + [(x, 1.0) for x in [1 + i / 20 for i in range(1, 21)]]
    c.polyline([(ax.X(x), ax.Y(y)) for x, y in pts], acc, 2.5)
    c.line(ax.X(1), ax.y0, ax.X(1), ax.y0 + ax.h, INK3, 1.5, dash="5 4")
    c.text(ax.X(1) + 8, ax.y0 + 14, "cliff at k = d", 11.5, "start", INK2)
    if note_:
        note(c, note_)


def t_loglog(c, acc, note_="", slope_label="slope d/2"):
    ax = Axes(c, 100, 30, 540, 210, (1, 100), (1, 100), [1, 10, 100], [1, 10, 100], "eigenvalue, log", "count below it, log", True, True)
    pts = [(x, x ** 0.75 * 1.3) for x in [1.2 ** i for i in range(26)] if x <= 100]
    c.polyline([(ax.X(x), ax.Y(min(y, 100))) for x, y in pts], acc, 2.5)
    c.text(ax.X(30), ax.Y(12), slope_label, 12, "start", INK2, italic=True)
    if note_:
        note(c, note_)


def t_timeline(c, acc, events=(), stale_from=None, note_="", floor=None, repeat=None):
    y = 150
    c.line(60, y, 660, y, INK, 2)
    c.arrow(640, y, 664, y, INK, 2)
    c.text(664, y + 22, "time", 11.5, "end", INK2)
    if stale_from is not None:
        c.add(f'<rect x="{stale_from}" y="{y - 40}" width="{660 - stale_from}" height="80" fill="{CRITICAL}" fill-opacity="0.10"/>')
        c.text(stale_from + 8, y - 26, "stale for this reader", 11.5, "start", CRITICAL)
    for x, label, col in events:
        c.line(x, y - 22, x, y + 22, col, 2.5)
        c.text(x, y + 40, label, 11.5, "middle", INK)
    if floor:
        a, b = floor
        c.line(a, y - 60, b, y - 60, acc, 2)
        c.line(a, y - 66, a, y - 54, acc, 2)
        c.line(b, y - 66, b, y - 54, acc, 2)
        c.text((a + b) / 2, y - 70, "refresh floor", 11.5, "middle", INK2)
    if repeat:
        for x in repeat:
            c.line(x, y - 14, x, y + 14, acc, 2)
    if note_:
        note(c, note_)


def t_blocks(c, acc, n=10, highlight=(), labels=None, note_="", rows=1, caption=None, dim=()):
    w = min(56, 600 // n)
    x0 = 360 - n * w / 2
    for r in range(rows):
        y0 = 110 + r * 60 - (rows - 1) * 30
        for i in range(n):
            col = acc if i in highlight else ("#f3f2ee" if i not in dim else GRID)
            stroke = acc if i in highlight else INK3
            c.add(f'<rect x="{x0 + i * w + 2}" y="{y0}" width="{w - 4}" height="44" rx="5" fill="{col}" fill-opacity="{0.35 if i in highlight else 1}" stroke="{stroke}" stroke-width="1.2"/>')
            if labels and r == 0 and i < len(labels):
                c.text(x0 + i * w + w / 2, y0 + 27, labels[i], 11, "middle", INK)
    if caption:
        c.text(360, 220, caption, 11.5, "middle", INK2)
    if note_:
        note(c, note_)


def t_chain(c, acc, stages, collapse=None, note_="", nojac=None):
    n = len(stages)
    w, gap = 110, 30
    x0 = 360 - (n * w + (n - 1) * gap) / 2
    y = 110
    for i, s in enumerate(stages):
        x = x0 + i * (w + gap)
        c.box(x, y, w, 50, s, fill="#f3f2ee", stroke=(acc if i == collapse else INK3))
        if i < n - 1:
            c.arrow(x + w, y + 25, x + w + gap - 2, y + 25, INK2, 1.5)
    if collapse is not None:
        x = x0 + collapse * (w + gap)
        c.line(x - 40, y - 30, x + 10, y + 2, acc, 1.5)
        c.line(x - 40, y + 80, x + 10, y + 48, acc, 1.5)
        c.text(x - 46, y - 30, "two inputs", 11, "end", INK2)
        c.text(x - 46, y + 84, "one output", 11, "end", INK2)
        c.text(x + w / 2, y + 74, "identified here, for every stage after", 11, "middle", acc)
    if nojac is not None:
        x = x0 + nojac * (w + gap)
        c.text(x + w / 2, y - 12, "no Jacobian", 11, "middle", INK2, italic=True)
    if note_:
        note(c, note_)


def t_barnull(c, acc, bar=0.55, null_mu=0.3, real_mu=0.72, vacuous=False, note_="", labels=("null", "system")):
    ax = Axes(c, 80, 30, 570, 200, (0, 1), (0, 1.1), [0, 0.5, 1], (), "statistic", "")
    def bell(mu, s):
        return [(x, math.exp(-((x - mu) ** 2) / (2 * s * s))) for x in [i / 100 for i in range(101)]]
    c.polyline([(ax.X(x), ax.Y(y)) for x, y in bell(null_mu, 0.09)], INK3, 2.5)
    c.text(ax.X(null_mu), ax.Y(1.05), labels[0], 11.5, "middle", INK2)
    c.polyline([(ax.X(x), ax.Y(y)) for x, y in bell(real_mu, 0.09)], acc, 2.5)
    c.text(ax.X(real_mu), ax.Y(1.05), labels[1], 11.5, "middle", INK2)
    col = CRITICAL if vacuous else INK
    c.line(ax.X(bar), ax.y0, ax.X(bar), ax.y0 + ax.h, col, 2, dash="6 4")
    c.text(ax.X(bar) + 6, ax.y0 + 14, "bar, vacuous" if vacuous else "bar", 11.5, "start", col)
    if note_:
        note(c, note_)


def t_scatter(c, acc, kind="clusters", note_=""):
    r = rng(11)
    ax = Axes(c, 90, 30, 540, 210, (0, 10), (0, 10), (), (), "", "")
    if kind in ("clusters", "kmeans", "silhouette", "sse"):
        centres = [(2.5, 3), (7, 7), (7.5, 2.5)]
        for k, (cx, cy) in enumerate(centres):
            for _ in range(18):
                x, y = cx + 0.8 * gauss(r), cy + 0.8 * gauss(r)
                c.dot(ax.X(x), ax.Y(y), [SERIES[0], SERIES[2], SERIES[3]][k], 3.5)
            if kind in ("kmeans", "sse"):
                c.dot(ax.X(cx), ax.Y(cy), INK, 6, title="centre")
        if kind == "sse":
            cx, cy = centres[0]
            for _ in range(6):
                x, y = cx + 0.9 * gauss(r), cy + 0.9 * gauss(r)
                c.line(ax.X(x), ax.Y(y), ax.X(cx), ax.Y(cy), INK2, 1)
        c.text(500, 60, "centres at the means" if kind in ("kmeans", "sse") else "three groups", 11.5, "start", INK2)
    elif kind in ("boundary", "margin"):
        for _ in range(30):
            x, y = 3 + 1.4 * gauss(r), 6.5 + 1.4 * gauss(r)
            c.dot(ax.X(x), ax.Y(y), SERIES[0], 3.5)
            x, y = 7 + 1.4 * gauss(r), 3.5 + 1.4 * gauss(r)
            c.dot(ax.X(x), ax.Y(y), SERIES[1], 3.5)
        c.line(ax.X(1), ax.Y(1.5), ax.X(9), ax.Y(9), INK, 2)
        if kind == "margin":
            c.line(ax.X(0.4), ax.Y(2.5), ax.X(8.4), ax.Y(10), INK3, 1.5, dash="5 4")
            c.line(ax.X(1.6), ax.Y(0.5), ax.X(9.6), ax.Y(8), INK3, 1.5, dash="5 4")
            c.text(ax.X(8.6), ax.Y(9.6), "margin", 11.5, "start", INK2)
        c.text(ax.X(8.2), ax.Y(8.9), "boundary", 11.5, "start", INK)
    elif kind == "outlier":
        for _ in range(60):
            x, y = 4 + 1.2 * gauss(r), 5 + 1.2 * gauss(r)
            c.dot(ax.X(x), ax.Y(y), INK2, 3.5)
        c.dot(ax.X(9), ax.Y(8.5), CRITICAL, 5, title="outlier")
        c.text(ax.X(9), ax.Y(8.5) - 12, "outlier", 11.5, "middle", CRITICAL)
        c.ellipse(ax.X(4), ax.Y(5), 75, 75, 0, acc, "none", 1.5)
    elif kind == "tree":
        for _ in range(40):
            x, y = 10 * r(), 10 * r()
            col = SERIES[0] if (x < 5 and y > 4) or (x >= 5 and y > 7) else SERIES[1]
            c.dot(ax.X(x), ax.Y(y), col, 3.5)
        c.line(ax.X(5), ax.Y(0), ax.X(5), ax.Y(10), INK, 2)
        c.line(ax.X(0), ax.Y(4), ax.X(5), ax.Y(4), INK, 2)
        c.line(ax.X(5), ax.Y(7), ax.X(10), ax.Y(7), INK, 2)
        c.text(ax.X(5) + 6, ax.Y(9.6), "axis-aligned splits", 11.5, "start", INK2)
    elif kind == "dbscan":
        for _ in range(45):
            x, y = 3.5 + 0.9 * gauss(r), 5 + 0.9 * gauss(r)
            c.dot(ax.X(x), ax.Y(y), acc, 3.5)
        for _ in range(8):
            c.dot(ax.X(10 * r()), ax.Y(10 * r()), INK3, 3.5, title="noise")
        c.ellipse(ax.X(3.5), ax.Y(5), 22, 22, 0, INK, "none", 1.5, title="radius")
        c.text(ax.X(3.5) + 26, ax.Y(5), "core point, enough neighbours in radius", 11.5, "start", INK2)
        c.text(ax.X(8.5), ax.Y(9), "noise", 11.5, "middle", INK3)
    elif kind == "density":
        for _ in range(50):
            x, y = 3 + 0.7 * gauss(r), 5 + 0.7 * gauss(r)
            c.dot(ax.X(x), ax.Y(y), acc, 3.5)
        for _ in range(12):
            x, y = 7.5 + 1.8 * gauss(r), 5 + 1.8 * gauss(r)
            c.dot(ax.X(x), ax.Y(y), INK2, 3.5)
        c.text(ax.X(3), ax.Y(8.5), "dense", 11.5, "middle", INK2)
        c.text(ax.X(7.5), ax.Y(9.2), "sparse", 11.5, "middle", INK2)
    elif kind == "rank":
        pts = [(1 + i * 0.9, 1 + i * 0.9 + 1.5 * gauss(r)) for i in range(10)]
        for x, y in pts:
            c.dot(ax.X(x), ax.Y(max(0.3, min(9.7, y))), acc, 4)
        c.text(ax.X(1), ax.Y(9.3), "rank of one score against rank of another", 11.5, "start", INK2)
    if note_:
        note(c, note_)


def t_dendrogram(c, acc, note_=""):
    leaves = [120 + i * 60 for i in range(9)]
    y0 = 240
    for x in leaves:
        c.dot(x, y0, INK2, 4)
    merges = [((0, 1), 200), ((2, 3), 210), ((5, 6), 190), ((7, 8), 205), (("a", "b"), 150), (("c", "d"), 140), ((4, "c"), 120), (("e", "f"), 80), (("g", "h"), 50)]
    pos = {i: (leaves[i], y0) for i in range(9)}
    names = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
    for k, ((u, v), h) in enumerate(merges):
        (xu, yu), (xv, yv) = pos[u], pos[v]
        c.line(xu, yu, xu, h, acc, 2)
        c.line(xv, yv, xv, h, acc, 2)
        c.line(xu, h, xv, h, acc, 2)
        pos[names[k]] = ((xu + xv) / 2, h)
    c.text(40, 60, "merge height never decreases", 11.5, "start", INK2, rotate=-90)
    if note_:
        note(c, note_)


def t_bars(c, acc, labels, vals, highlight=None, note_="", ylabel="", bar=None, colors=None):
    ax = Axes(c, 90, 30, 560, 200, (0, len(vals)), (0, max(vals) * 1.15), (), (), "", ylabel)
    bw = 560 / len(vals) * 0.55
    for i, (l, v) in enumerate(zip(labels, vals)):
        col = colors[i] if colors else (acc if (highlight is None or i == highlight) else INK3)
        c.rect(ax.X(i + 0.5) - bw / 2, ax.Y(v), bw, ax.Y(0) - ax.Y(v), col)
        c.text(ax.X(i + 0.5), ax.y0 + ax.h + 16, l, 11, "middle", INK2)
    if bar is not None:
        c.line(ax.x0, ax.Y(bar), ax.x0 + ax.w, ax.Y(bar), INK, 1.5, dash="6 4")
        c.text(ax.x0 + ax.w - 4, ax.Y(bar) - 6, "bar", 11.5, "end", INK2)
    if note_:
        note(c, note_)


def t_folds(c, acc, k=5, test=2, leak=False, note_="", label="fold"):
    w = 100
    x0 = 360 - k * w / 2
    for i in range(k):
        col = acc if i == test else "#f3f2ee"
        c.add(f'<rect x="{x0 + i * w + 3}" y="100" width="{w - 6}" height="60" rx="6" fill="{col}" fill-opacity="{0.35 if i == test else 1}" stroke="{INK3}" stroke-width="1.2"/>')
        c.text(x0 + i * w + w / 2, 135, "test" if i == test else "train", 12, "middle", INK)
    c.text(360, 190, f"every row is tested once across the {k} {label}s", 11.5, "middle", INK2)
    if leak:
        c.arrow(x0 + test * w + w / 2, 100, x0 + w / 2, 70, CRITICAL, 2)
        c.text(x0 + w, 62, "a transform fit on all rows reads the test fold", 11.5, "start", CRITICAL)
    if note_:
        note(c, note_)


def t_seal(c, acc, note_="", changed=False, chain=True):
    for i in range(3):
        x = 120 + i * 190
        c.box(x, 90, 130, 70, ["prediction", "measurement", "verdict"][i], sub=["sealed", "run", "reported"][i])
        col = CRITICAL if (changed and i == 0) else acc
        c.add(f'<rect x="{x + 20}" y="170" width="90" height="22" rx="4" fill="{col}" fill-opacity="0.2" stroke="{col}"/>')
        c.text(x + 65, 185, ["3f2a…", "9c1e…", "b7d0…"][i], 11, "middle", INK)
        if i < 2 and chain:
            c.arrow(x + 130, 125, x + 190 - 4, 125, INK2, 1.5)
    c.text(360, 230, "each file's digest is recorded before the next step, and a changed digest proves a changed file", 11.5, "middle", INK2)
    if note_:
        note(c, note_)


def t_rotation(c, acc, note_=""):
    cx, cy, R = 240, 150, 100
    c.ellipse(cx, cy, R, R, 0, GRID, "none", 1.5)
    for ang, col, lab in [(20, INK, "query at m"), (75, acc, "key at n")]:
        a = math.radians(ang)
        c.arrow(cx, cy, cx + R * math.cos(a), cy - R * math.sin(a), col, 2)
        c.text(cx + (R + 14) * math.cos(a), cy - (R + 14) * math.sin(a), lab, 11.5, "start", INK)
    pts = [(cx + 45 * math.cos(math.radians(t)), cy - 45 * math.sin(math.radians(t))) for t in range(20, 76, 3)]
    c.polyline(pts, INK2, 1.5)
    c.text(cx + 60, cy - 40, "θ(n − m)", 12, "start", INK2, italic=True)
    c.text(430, 120, "the score reads the difference of positions", 11.5, "start", INK2)
    c.text(430, 140, "shifting both by the same amount changes nothing", 11.5, "start", INK2)
    if note_:
        note(c, note_)


def t_attention(c, acc, note_=""):
    keys = [0.1, 0.25, 0.9, 0.35, 0.05, 0.6, 0.15, 0.2]
    tot = sum(math.exp(3 * k) for k in keys)
    x0 = 130
    c.text(x0 - 10, 80, "query", 12, "end", INK)
    c.add(f'<rect x="{x0}" y="66" width="40" height="22" rx="4" fill="{INK}" fill-opacity="0.8"/>')
    for i, k in enumerate(keys):
        x = x0 + 60 + i * 60
        c.add(f'<rect x="{x}" y="66" width="44" height="22" rx="4" fill="{acc}" fill-opacity="{0.15 + 0.8 * k:.2f}"/>')
        c.text(x + 22, 60, f"key {i + 1}", 10.5, "middle", INK2)
        w = math.exp(3 * k) / tot
        c.rect(x + 8, 220 - 120 * w, 28, 120 * w, acc)
    c.line(x0 + 60, 220, x0 + 60 + 8 * 60, 220, GRID, 1)
    c.text(x0 - 10, 160, "softmax weights, sum to one", 11.5, "end", INK2)
    if note_:
        note(c, note_)


def t_lorenz(c, acc, note_=""):
    ax = Axes(c, 110, 30, 300, 215, (0, 1), (0, 1), [0, 0.5, 1], [0, 0.5, 1], "share of rows", "share of retrievals")
    c.line(ax.X(0), ax.Y(0), ax.X(1), ax.Y(1), INK3, 1.5, dash="5 4")
    pts = [(x, x ** 2.6) for x in [i / 40 for i in range(41)]]
    c.polyline([(ax.X(x), ax.Y(y)) for x, y in pts], acc, 2.5)
    c.text(430, 80, "equal shares is the diagonal", 11.5, "start", INK2)
    c.text(430, 98, "the index is the largest vertical gap", 11.5, "start", INK2)
    if note_:
        note(c, note_)


def t_intervals(c, acc, kind="ci", note_=""):
    ax = Axes(c, 110, 30, 540, 200, (0, 1), (0, 5), [0, 0.5, 1], (), "estimate", "")
    r = rng(5)
    if kind == "paired":
        for i in range(4):
            y = 4 - i
            a, b = 0.35 + 0.1 * gauss(r) * 0.5, 0.55 + 0.1 * gauss(r) * 0.5
            c.line(ax.X(a), ax.Y(y), ax.X(b), ax.Y(y), INK3, 2)
            c.dot(ax.X(a), ax.Y(y), INK2, 4.5)
            c.dot(ax.X(b), ax.Y(y), acc, 4.5)
        c.text(ax.X(0.62), ax.Y(4), "same rows, two arms", 11.5, "start", INK2)
    elif kind == "se":
        for i, n in enumerate([4, 16, 64, 256]):
            y = 4 - i
            hw = 0.4 / math.sqrt(n) * 2
            c.line(ax.X(0.5 - hw), ax.Y(y), ax.X(0.5 + hw), ax.Y(y), acc, 2.5)
            c.dot(ax.X(0.5), ax.Y(y), acc, 4)
            c.text(ax.X(0.02), ax.Y(y) + 4, f"n = {n}", 11.5, "start", INK2)
        c.text(ax.X(0.62), ax.Y(4), "the interval shrinks as one over root n", 11.5, "start", INK2)
    else:
        for i in range(4):
            y = 4 - i
            m = 0.5 + 0.12 * gauss(r)
            hw = 0.12 + 0.05 * r()
            c.line(ax.X(m - hw), ax.Y(y), ax.X(m + hw), ax.Y(y), acc, 2.5)
            c.dot(ax.X(m), ax.Y(y), acc, 4)
        c.text(ax.X(0.02), ax.Y(0.5), "resamples of the same rows", 11.5, "start", INK2)
    if note_:
        note(c, note_)


def t_ladder(c, acc, note_="", pairs=True):
    levels = [0, 0.38, 0.38, 1.38, 1.38, 2.62, 2.62, 3.62] if pairs else [0, 0.5, 1.1, 1.7, 2.6, 3.1, 3.7]
    ax = Axes(c, 200, 30, 320, 210, (0, 1), (-0.2, 4), (), (), "", "eigenvalue")
    for i, v in enumerate(levels):
        off = 0 if not pairs else (-0.05 if i % 2 == 1 and i > 0 else 0.05)
        c.line(ax.X(0.2 + off), ax.Y(v), ax.X(0.8 + off), ax.Y(v), acc, 2.5)
    c.text(ax.X(0.86), ax.Y(0.38) + 4, "a pair, one multiplet", 11.5, "start", INK2)
    c.text(ax.X(0.86), ax.Y(0) + 4, "the constant mode", 11.5, "start", INK2)
    if note_:
        note(c, note_)


def t_manifold(c, acc, kind="geodesic", note_=""):
    if kind == "geodesic":
        pts = [(80 + i * 8, 200 - 90 * math.sin(math.pi * i / 70)) for i in range(71)]
        c.polyline(pts, INK, 2.5)
        c.polyline(pts[10:61], acc, 3)
        c.line(pts[10][0], pts[10][1], pts[60][0], pts[60][1], INK3, 1.5, dash="5 4")
        c.dot(pts[10][0], pts[10][1], INK, 4)
        c.dot(pts[60][0], pts[60][1], INK, 4)
        c.text(360, 240, "the chord cuts through the space, the geodesic follows the surface", 11.5, "middle", INK2)
    elif kind == "band":
        c.line(80, 220, 640, 80, acc, 2.5)
        c.line(80, 250, 640, 140, INK3, 1.5, dash="5 4")
        c.line(80, 190, 640, 20, INK3, 1.5, dash="5 4")
        c.text(360, 270, "every distance lands between the two lines, a factor each way", 11.5, "middle", INK2)
    elif kind == "concentration":
        ax = Axes(c, 100, 30, 540, 210, (1, 500), (0, 1), [1, 10, 100], [0, 0.5, 1], "dimension, log", "relative contrast", True)
        pts = [(d, 1 / math.sqrt(d) * 1.0) for d in [1.3 ** i for i in range(24)] if d <= 500]
        c.polyline([(ax.X(d), ax.Y(min(1, y))) for d, y in pts], acc, 2.5)
        c.text(ax.X(40), ax.Y(0.5), "nearest and farthest converge", 11.5, "start", INK2)
    elif kind == "circle":
        c.ellipse(300, 150, 100, 100, 0, acc, "none", 2.5)
        c.line(180, 150, 420, 150, GRID, 1)
        c.line(300, 40, 300, 260, GRID, 1)
        c.text(440, 120, "one-dimensional, two coordinates", 11.5, "start", INK2)
        c.text(440, 140, "locally a line, globally not a line", 11.5, "start", INK2)
    if note_:
        note(c, note_)


def t_strata(c, acc, vals=None, bar=0.9, note_="", kind="min", labels=None):
    vals = vals or [0.95, 0.93, 0.97, 0.66, 0.94, 0.92, 0.96]
    labels = labels or [f"s{i + 1}" for i in range(len(vals))]
    ax = Axes(c, 90, 30, 560, 200, (0, len(vals)), (0, 1.1), (), [0, 0.5, 1], "stratum", "score")
    bw = 560 / len(vals) * 0.55
    mn = min(range(len(vals)), key=lambda i: vals[i])
    for i, v in enumerate(vals):
        col = CRITICAL if (kind == "min" and i == mn) else acc
        c.rect(ax.X(i + 0.5) - bw / 2, ax.Y(v), bw, ax.Y(0) - ax.Y(v), col)
        c.text(ax.X(i + 0.5), ax.y0 + ax.h + 16, labels[i], 11, "middle", INK2)
    c.line(ax.x0, ax.Y(bar), ax.x0 + ax.w, ax.Y(bar), INK, 1.5, dash="6 4")
    c.text(ax.x0 + ax.w - 4, ax.Y(bar) - 6, "bar", 11.5, "end", INK2)
    mean = sum(vals) / len(vals)
    c.line(ax.x0, ax.Y(mean), ax.x0 + ax.w, ax.Y(mean), INK3, 1.5)
    c.text(ax.x0 + 4, ax.Y(mean) - 6, "mean passes, the minimum fails", 11.5, "start", INK2)
    if note_:
        note(c, note_)


def t_triple(c, acc, highlight="consumer", note_=""):
    boxes = {"consumer": (90, 110, "consumer", "the computation"), "metric": (300, 110, "output metric", "what a mistake costs"), "budget": (510, 110, "budget", "what can be spent")}
    for k, (x, y, l, s) in boxes.items():
        c.box(x, y, 150, 60, l, sub=s, stroke=(acc if k == highlight else INK3))
    c.arrow(240, 140, 298, 140, INK2, 1.5)
    c.arrow(450, 140, 508, 140, INK2, 1.5)
    c.text(360, 215, "the read operator is what the triple induces, and its kernel is the nuisance", 11.5, "middle", INK2)
    if note_:
        note(c, note_)


def t_table(c, acc, note_="", rows=(("chapter 4 section 4.2", "0.41 to 0.005, twelve of twelve", "repo/file.md:40-70")), highlight=0):
    x0, y0 = 60, 70
    cols = [150, 260, 200]
    heads = ["where", "numbers", "source, file and lines"]
    x = x0
    for w, h in zip(cols, heads):
        c.text(x + 6, y0 - 8, h, 11, "start", INK2, "600")
        x += w
    c.line(x0, y0, x0 + sum(cols), y0, INK3, 1)
    for i, row in enumerate(rows):
        y = y0 + 26 + i * 32
        x = x0
        for j, (w, cell) in enumerate(zip(cols, row)):
            col = acc if (i == highlight and j == 2) else INK
            c.text(x + 6, y, cell, 11, "start", col)
            x += w
        c.line(x0, y + 10, x0 + sum(cols), y + 10, GRID, 1)
    c.text(360, 250, "every number names the file and lines it came from, at a commit", 11.5, "middle", INK2)
    if note_:
        note(c, note_)


def t_bits(c, acc, note_="", nats=False):
    for b in range(1, 5):
        x = 100 + (b - 1) * 150
        n = 2 ** b
        for i in range(n):
            y = 60 + i * (160 / n)
            c.add(f'<rect x="{x}" y="{y}" width="80" height="{160 / n - 3}" rx="3" fill="{acc}" fill-opacity="{0.15 + 0.6 * i / n:.2f}"/>')
        c.text(x + 40, 245, f"{b} bit{'s' if b > 1 else ''}, {n} levels", 11.5, "middle", INK2)
    if nats:
        c.text(360, 275, "one nat is 1.4427 bits, the natural logarithm's unit", 11.5, "middle", INK2)
    if note_:
        note(c, note_)


def t_quotient(c, acc, note_="", classes=3):
    r = rng(3)
    for i in range(24):
        x, y = 70 + 200 * r(), 60 + 180 * r()
        k = int(y // 60) % classes
        c.dot(x, y, [SERIES[0], SERIES[2], SERIES[3]][k], 4)
    c.arrow(300, 150, 400, 150, INK2, 2)
    c.text(350, 138, "reader", 11.5, "middle", INK2)
    for k in range(classes):
        y = 80 + k * 60
        c.add(f'<rect x="440" y="{y}" width="200" height="40" rx="6" fill="{[SERIES[0], SERIES[2], SERIES[3]][k]}" fill-opacity="0.2" stroke="{INK3}"/>')
        c.text(540, y + 25, f"class {k + 1}, rows the reader cannot tell apart", 11, "middle", INK)
    if note_:
        note(c, note_)


def t_kl(c, acc, note_="", labels=("p", "q")):
    ax = Axes(c, 90, 30, 540, 210, (0, 10), (0, 0.5), (), (), "", "density")
    def bell(mu, s):
        return [(x, 0.45 * math.exp(-((x - mu) ** 2) / (2 * s * s))) for x in [i / 10 for i in range(101)]]
    c.polyline([(ax.X(x), ax.Y(y)) for x, y in bell(4, 1.1)], acc, 2.5)
    c.polyline([(ax.X(x), ax.Y(y)) for x, y in bell(6, 1.6)], SERIES[1], 2.5)
    c.text(ax.X(4), ax.Y(0.47), labels[0], 12, "middle", INK2, italic=True)
    c.text(ax.X(6.3), ax.Y(0.31), labels[1], 12, "middle", INK2, italic=True)
    if note_:
        note(c, note_)


def t_stepcurve(c, acc, note_="", kind="early"):
    ax = Axes(c, 90, 30, 540, 210, (0, 100), (0, 1), [0, 50, 100], [0, 0.5, 1], "rounds" if kind == "early" else "threshold", "held-out score" if kind == "early" else "positives called")
    if kind == "early":
        pts = [(t, 0.9 - 0.6 * math.exp(-t / 18) - 0.004 * max(0, t - 45)) for t in range(0, 101, 2)]
        c.polyline([(ax.X(t), ax.Y(y)) for t, y in pts], acc, 2.5)
        c.line(ax.X(45), ax.y0, ax.X(45), ax.y0 + ax.h, INK3, 1.5, dash="5 4")
        c.text(ax.X(45) + 6, ax.y0 + 14, "stop here, chosen on the held-out fold", 11.5, "start", INK2)
    else:
        pts = [(t, 1 - t / 100) for t in range(0, 101, 5)]
        c.polyline([(ax.X(t), ax.Y(y)) for t, y in pts], acc, 2.5)
        c.text(ax.X(50), ax.Y(0.6), "a higher threshold calls fewer rows", 11.5, "start", INK2)
    if note_:
        note(c, note_)


# ================================================================ mapping
# id -> (template, kwargs, caption)
M = {}


def m(eid, tpl, cap, **kw):
    M[eid] = (tpl, kw, cap)


m("abstention", t_strata, "A verdict per group, with the group too thin to score reported as an abstention rather than dropped.", vals=[0.95, 0.93, 0.97, 0.0, 0.94, 0.92], labels=["g1", "g2", "g3", "thin", "g5", "g6"])
m("aggregation", t_strata, "An aggregate over strata passes a bar that one stratum fails.")
m("alignment", t_ellipses, "The overlap between the consumer's read direction and the data's covariance.", second=False)
m("allocation", t_spectrum, "Bits go to the directions above the water level and none to those below it.", water=0.18)
m("anisotropic", t_ellipses, "Unequal variances across directions, so a reader at an angle sees a different variance from another.", same=False)
m("anti-arm", t_ellipses, "The control that puts the error on the read direction, confirmed worst.", labels=("read direction", "anti arm"))
m("anti-hub", t_graph, "A row that no query reaches.", kind="antihub")
m("anti-hub-recall", t_strata, "Recall on the rarely retrieved rows, taken as the minimum over strata.")
m("anti-monotonicity", t_venn, "Support cannot rise as an itemset grows, so a superset of an infrequent itemset is pruned.", a="itemset", b="superset", nested=True)
m("apriori", t_venn, "Every superset of an infrequent itemset is infrequent.", a="infrequent", b="all its supersets", nested=True)
m("attention", t_attention, "A query against every key, and a softmax that turns the scores into weights.")
m("attribute-type", t_blocks, "The four scales and the transformations each permits, nested from ratio to nominal.", n=4, labels=["ratio", "interval", "ordinal", "nominal"], highlight=(0,), caption="rescale ⊂ affine ⊂ increasing ⊂ injective")
m("attribution", t_bars, "A share of one prediction per feature, and the averaged squared gradient that estimates the read operator.", labels=["x1", "x2", "x3", "x4", "x5"], vals=[0.42, 0.28, 0.05, 0.18, 0.07])
m("audit", t_seal, "A reader who did not produce the number checks it against the sealed record.")
m("auroc", t_roc, "The area under the curve is the chance that a random positive outscores a random negative.")
m("bag-of-words", t_quotient, "Documents with the same counts are the same document to the reader, whatever the order.", classes=3)
m("bagging", t_intervals, "Resamples of the same rows, each fit and then averaged.", kind="bootstrap")
m("balanced-accuracy", t_strata, "The mean of the per-class recalls, so a large class cannot hide a small one.", vals=[0.9, 0.55, 0.85], labels=["class A", "class B", "class C"], bar=0.75, kind="none")
m("bar", t_barnull, "A bar discriminates when the null fails it and the system passes it.")
m("baseline", t_barnull, "The simplest scorer the claim must beat, under the same protocol.", labels=("baseline", "system"))
m("bi-lipschitz", t_manifold, "Every distance stretched or shrunk by at most a fixed factor.", kind="band")
m("bit", t_bits, "Each bit doubles the levels and halves the step.")
m("blind-probe", t_cliff, "Recovery of the read operator against the probe's budget, with a cliff at k equal to d.")
m("block-error-rate", t_timeline, "Blocks a receiver cannot decode, as a fraction of those sent in a window.", events=[(150, "sent", INK3), (250, "sent", INK3), (350, "lost", CRITICAL), (450, "sent", INK3), (550, "lost", CRITICAL)])
m("boosting", t_bars, "Rows the last scorer got wrong are reweighted so that its error becomes one half.", labels=["right", "right", "wrong", "right", "wrong", "right"], vals=[0.6, 0.6, 1.6, 0.6, 1.6, 0.6], colors=[INK3, INK3, SERIES[1], INK3, SERIES[1], INK3], ylabel="weight")
m("bootstrap", t_intervals, "Resampling the rows with replacement to see how far the estimate moves.", kind="bootstrap")
m("budget", t_triple, "The third element of the observer, what the consumer can spend.", highlight="budget")
m("budget-cliff", t_cliff, "Recovery jumps at k equal to d and does not soften below it.")
m("cache", t_blocks, "Recently used entries kept so they need not be fetched again.", n=10, highlight=(1, 2, 3, 6), caption="the footprint is the entries this reader reads")
m("calibration", t_roc, "Score bins against the fraction of positives in each.", calibration=True)
m("capacity", t_spectrum, "The distinctions a model class can draw, the model-side half of the budget.", kept=3)
m("certificate", t_timeline, "A claim about a read at a time, and a witness that checks it later.", events=[(180, "certificate issued", SERIES[2]), (460, "witness reads", SERIES[0])], stale_from=360)
m("challenge-set", t_venn, "A collection on which a benchmark-passing shortcut fails, outside the benchmark.", a="benchmark", b="challenge set", disjoint=True)
m("chance-level", t_barnull, "The score a null scorer reaches, which a bar must clear.", labels=("chance", "system"))
m("chunk", t_chain, "A document goes to pieces at a stage that has no Jacobian.", stages=["document", "chunks", "vectors", "candidates"], nojac=1)
m("classifier", t_sigmoid, "A score per row and a threshold that turns it into a decision.")
m("codebook", t_blocks, "The small set of values a quantizer replaces each number with.", n=8, highlight=(3,), labels=["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"], caption="each number rounds to its nearest code")
m("coherence-time", t_timeline, "How long a quantity stays what it was.", events=[(150, "read", SERIES[2])], floor=(150, 330))
m("cold-warm", t_blocks, "Before the cache holds anything useful, and after.", n=10, highlight=(0, 1, 2, 3, 4), rows=2, caption="cold above, warm below")
m("commit-hash", t_seal, "A fingerprint of a snapshot and its history, proving content and not time.")
m("commute-time", t_graph, "Steps there and back for a random walk, whose scaling by the volume is the resistance.", kind="path")
m("concentrated", t_spectrum, "A few eigenvalues carry most of the total.", vals=[1.0, 0.12, 0.06, 0.03, 0.02, 0.01, 0.01, 0.01])
m("confidence", t_venn, "The fraction of transactions with the antecedent that also hold the consequent.", a="antecedent", b="consequent")
m("confidence-interval", t_intervals, "A range the estimate falls in with a stated frequency over repetitions.", kind="ci")
m("confound", t_ellipses, "A variable that moves both arms of a comparison.", same=False)
m("consumer", t_triple, "The computation that reads the vector, the first element of the observer.", highlight="consumer")
m("contraction", t_bars, "Several axes reduced to one verdict by a formula a person can read.", labels=["a1", "a2", "a3", "a4", "a5", "a6"], vals=[0.9, 0.2, 0.15, 0.1, 0.1, 0.05])
m("contrastive-objective", t_scatter, "Pairs declared similar pulled together, others pushed apart.", kind="clusters")
m("control", t_barnull, "An arm that should show no effect, run beside the one that should.", vacuous=False)
m("correction", t_seal, "An erratum kept beside the original, itself sealed.", changed=True)
m("correlation", t_angle, "The cosine of two centred columns.", a="x − mean", b="y − mean", deg=35)
m("cosine", t_angle, "The dot product over the two lengths, the cosine of the angle between the vectors.", a="x", b="y", deg=40)
m("coupling-null", t_graph, "Hubs that appear because the queries were drawn from the corpus.", kind="hub")
m("covariance-matrix", t_matrix, "Variances on the diagonal and covariances off it, symmetric and positive semidefinite.", pattern="symmetric", label="Σ")
m("coverage", t_venn, "The fraction of decisions the certificate cleared.", a="decisions", b="cleared", nested=True)
m("cross-corpus-gate", t_barnull, "An encoder votes only if its AUROC on a corpus it never saw clears the margin over a bag-of-words null.", labels=("bag-of-words null", "encoder"))
m("cross-support-ratio", t_venn, "The support of the rarer item over the support of the commoner one.", a="common item", b="rare item")
m("cross-validation", t_folds, "Folds tested once each, sharing training data.")
m("curvature", t_parabola, "The second derivative, which the finite difference does not read and which sets the linear model's error.")
m("dbscan", t_scatter, "Core points by neighbour count within a radius, clusters by reachability, the rest noise.", kind="dbscan")
m("decision-boundary", t_scatter, "Where the score crosses the threshold.", kind="boundary")
m("decision-tree", t_scatter, "Axis-aligned splits, flat within each leaf.", kind="tree")
m("declaration", t_seal, "What the study will count, drop, or treat as a failure, sealed before the run.")
m("degree", t_graph, "The number of edges at a node.", kind="knn")
m("density", t_scatter, "The local crowding of rows, the coordinate the geodesic reader discards.", kind="density")
m("deployment-mismatch", t_ellipses, "The harness reads a direction the deployed consumer never sees.", same=False, labels=("harness reads", "deployment reads"))
m("detector", t_scatter, "A scorer that calls a row an outlier, of four families.", kind="outlier")
m("direction-only-quantizer", t_angle, "The length stored exactly and the direction rounded.", a="length", b="direction", deg=30)
m("discretization", t_quotient, "Values in one cell become one label.", classes=3)
m("disparate-impact-ratio", t_strata, "The positive rate of one group over another's.", vals=[0.62, 0.48, 0.6], labels=["group A", "group B", "group C"], bar=0.8, kind="none")
m("distance-concentration", t_manifold, "Nearest and farthest converge as the dimension grows.", kind="concentration")
m("distortion", t_ellipses, "The error a code costs a reader, which two readers rank differently.", same=True)
m("dot-product", t_angle, "The sum of the products of matching coordinates.", a="x", b="y", deg=40, proj=True)
m("drift", t_timeline, "The read operator moving over time, so an old certificate no longer describes the reader.", events=[(150, "measured", SERIES[2]), (500, "re-measured", SERIES[1])], stale_from=380)
m("early-stopping", t_stepcurve, "Halting a boosting run when a held-out score stops improving.", kind="early")
m("effective-rank", t_spectrum, "The number of directions a spectrum really uses, with no cutoff to choose.")
m("eigenvalue-eigenvector", t_ellipses, "The directions a symmetric matrix stretches along, and by how much.", second=False)
m("embedding", t_chain, "A row mapped to a vector by an encoder whose quotient is learned.", stages=["input", "encoder", "vector", "consumer"])
m("encoder", t_chain, "A model that maps an input to an embedding.", stages=["input", "encoder", "embedding"])
m("ensemble", t_intervals, "An average of several scorers, between its members.", kind="bootstrap")
m("equalized-odds", t_strata, "Equal true and false positive rates across groups.", vals=[0.9, 0.88, 0.7], labels=["group A", "group B", "group C"], bar=0.85, kind="none")
m("escalation", t_timeline, "A verdict handed up when the certificate cannot clear it.", events=[(150, "cleared", SERIES[2]), (330, "cleared", SERIES[2]), (520, "escalated", CRITICAL)])
m("euclidean-distance", t_angle, "The length of the difference of two vectors.", a="x", b="y", deg=40)
m("eviction", t_blocks, "Choosing what to drop when the cache is full.", n=10, highlight=(7,), dim=(7,), caption="the evicted entry is read next")
m("expected-calibration-error", t_roc, "The bin-weighted gap between the mean score and the fraction of positives.", calibration=True)
m("explained-variance", t_spectrum, "The fraction of the spectrum the kept components carry.", kept=3)
m("f1", t_roc, "The harmonic mean of precision and recall at a threshold.", point=(0.15, 0.55))
m("false-clear-rate", t_timeline, "How often a clearance was wrong, conditional on clearing.", events=[(150, "cleared", SERIES[2]), (300, "cleared", SERIES[2]), (450, "cleared, witness disagrees", CRITICAL)], stale_from=400)
m("fine-tuning", t_scatter, "Continuing to train an encoder so that its quotient changes.", kind="clusters")
m("finite-difference", t_parabola, "A derivative from two evaluations a step apart.")
m("flip", t_ellipses, "At matched bits, the code that reconstructs worse can serve the consumer better.")
m("floor-ceiling", t_histogram, "A lower bound a quantity cannot fall below, an upper bound it cannot exceed.", ceiling=12, shape="poisson")
m("footprint", t_blocks, "The set of entries a reader reads.", n=10, highlight=(2, 3, 4), caption="what the reader reads decides how warm and how stale it is")
m("formula-search", t_scatter, "A search over short formulas scored by optimal thresholded F1.", kind="boundary")
m("freshness", t_timeline, "Whether a read is still what the quantity is.", events=[(150, "written", SERIES[2]), (420, "read", SERIES[0])], stale_from=330)
m("gate", t_barnull, "A bar a build must pass before it proceeds.")
m("gaussian", t_ellipses, "The normal distribution, isotropic when every direction is the same.", circle=True)
m("geodesic-distance", t_manifold, "The shortest path along the surface.", kind="geodesic")
m("graph", t_graph, "Nodes and the edges that join pairs of them.", kind="knn")
m("harness", t_folds, "The evaluation reads folds, samples, and seeds, and what it reads it can leak.", leak=False)
m("hash", t_seal, "A fixed-length fingerprint that changes whenever the file does.")
m("head", t_attention, "One attention head, a query against every key.")
m("hessian", t_matrix, "Second derivatives, with the interactions off the diagonal.", pattern="band", label="diagonal for naive Bayes")
m("hierarchical-clustering", t_dendrogram, "The closest pair merged at each step, with heights that never decrease.")
m("hub", t_graph, "A row retrieved far more often than chance allows.", kind="hub")
m("hubness", t_histogram, "The count distribution's tail above the Poisson ceiling.", ceiling=12, shape="poisson")
m("identity-reader", t_ellipses, "The reader that weighs every direction equally.", circle=True)
m("importance", t_bars, "How much a classifier reads each feature, counting splits for a tree.", labels=["x1", "x2", "x3", "x4", "x5", "x6"], vals=[0.35, 0.3, 0.02, 0.2, 0.1, 0.03])
m("imputation", t_blocks, "A value written into a missing cell that the consumer will read.", n=8, highlight=(2, 5), caption="filled with the mean, which keeps the mean and shrinks the variance")
m("intrinsic-dimension", t_loglog, "The dimension read from the slope of the eigenvalue count.")
m("inverted-file", t_blocks, "The vectors partitioned into cells, and a query that probes a few.", n=8, highlight=(2, 3), caption="probe depth two of eight cells")
m("isotropic", t_ellipses, "Every direction has the same variance.", circle=True)
m("itemset", t_venn, "A set of items, with the transactions that contain it as its support.", a="transactions", b="itemset", nested=True)
m("jaccard", t_venn, "Intersection over union.", a="A", b="B", third="|A ∩ B| / |A ∪ B|")
m("jacobian", t_matrix, "The partial derivatives of a vector-valued consumer.", pattern="dense", label="rows are outputs, columns inputs")
m("k-means", t_scatter, "Centres at the means, rows assigned to the nearest.", kind="kmeans")
m("kendall-correlation", t_scatter, "Concordant pairs less discordant pairs over all pairs.", kind="rank")
m("kernel", t_matrix, "The directions a matrix sends to zero, the nuisance for the read operator.", pattern="kernel", label="the unread block")
m("kl-divergence", t_kl, "How many extra bits coding with q costs when the truth is p.")
m("kv-cache", t_blocks, "One key and one value per token per head, kept for the next token.", n=12, highlight=(9, 10, 11), caption="a window keeps the last tokens")
m("lag", t_timeline, "How far a replica trails the primary.", events=[(200, "primary write", SERIES[2]), (420, "replica catches up", SERIES[0])], stale_from=200)
m("landauers-principle", t_bits, "Erasing a bit costs at least kT ln 2 of energy.")
m("language-model", t_attention, "A model that reads tokens and outputs a probability for the next one.")
m("laplacian", t_matrix, "Degrees on the diagonal, minus the adjacency off it.", pattern="band", label="D − A")
m("latent-semantic-analysis", t_spectrum, "The top singular components of the term-document matrix.", kept=2)
m("leakage", t_folds, "A transform fit on all rows reads the test fold.", leak=True)
m("ledger-class", t_seal, "Proved, demonstrated, replicated, predicted, exploratory, refuted, missed, or void.")
m("lift", t_venn, "Confidence over the base rate of the consequent.", a="antecedent", b="consequent")
m("linear-classifier", t_scatter, "A weighted sum, whose boundary is a hyperplane.", kind="margin")
m("logistic-regression", t_sigmoid, "The sigmoid of a weighted sum, above one half on one side of the hyperplane.")
m("mahalanobis-distance", t_ellipses, "Euclidean distance after whitening.", second=False)
m("manifold", t_manifold, "Locally like flat space, and not globally low-dimensional in the coordinates.", kind="circle")
m("margin", t_scatter, "The distance from the boundary to the nearest rows.", kind="margin")
m("matched-bits", t_bits, "Two codes are compared only at the same bit count.")
m("metric", t_angle, "A rule for the distance between two rows or two outputs.", a="x", b="y", deg=50)
m("min-over-strata", t_strata, "The worst stratum is the verdict.")
m("monotone-invariance", t_roc, "Optimal thresholded F1 survives any strictly monotone transform, AUROC only an increasing one.", second="the reversed score")
m("multiple-comparisons", t_histogram, "Many tests, and the best reported.", shape="normal", threshold=14)
m("multiplet", t_ladder, "Eigenvalues that come in equal groups.")
m("nadeau-and-bengio-correction", t_intervals, "The variance of a cross-validated difference inflated for the folds' shared training data.", kind="se")
m("naive-bayes", t_matrix, "One-dimensional likelihoods multiplied, so the score is additive and the Hessian diagonal.", pattern="diag", label="no interaction terms")
m("nat", t_bits, "Information in the natural logarithm's unit.", nats=True)
m("nearest-neighbour", t_graph, "The row at minimal distance from a query.", kind="knn")
m("neighbourhood-graph", t_graph, "Each row joined to its k nearest rows.", kind="knn")
m("nuisance", t_ellipses, "The directions the consumer never reads, the kernel of its read operator.", second=False)
m("null-model", t_barnull, "What the statistic looks like when the claimed effect is absent.")
m("observer", t_triple, "A consumer, an output metric, and a budget.", highlight="consumer")
m("operating-point", t_roc, "The row at which a consumer is read, or the threshold at which a classifier is scored.", point=(0.2, 0.62))
m("orthogonal", t_angle, "Dot product zero.", a="u", b="v", deg=90)
m("outer-product", t_matrix, "The entry in row i and column j is the product of the i-th and j-th coordinates.", pattern="outer", label="rank one")
m("outlier", t_scatter, "A row the reader cannot place.", kind="outlier")
m("output-metric", t_triple, "What a mistake costs, the second element of the observer.", highlight="metric")
m("p-value", t_histogram, "The fraction of the null distribution at least as extreme as the observation.", shape="normal", threshold=13)
m("paired", t_intervals, "The same rows or seeds in both arms.", kind="paired")
m("paraphrase-class", t_quotient, "Texts the encoder cannot tell apart.", classes=3)
m("per-channel-quantizer", t_blocks, "A step per coordinate.", n=8, highlight=(0, 2, 4, 6), caption="each channel has its own step")
m("percentile", t_histogram, "The value below which a given fraction of the rows fall.", shape="skew", threshold=15)
m("perplexity", t_bars, "Two to the power of the average bits per token.", labels=["t1", "t2", "t3", "t4", "t5", "t6"], vals=[2.1, 3.4, 1.2, 4.0, 2.8, 1.6], ylabel="bits per token")
m("planted", t_ellipses, "A case whose answer is known before the instrument reads it.", second=False)
m("poisson-ceiling", t_histogram, "The count chance allows.", ceiling=12, shape="poisson")
m("posited-versus-measured", t_seal, "A claim written down before, and a number read after.")
m("positive-semidefinite", t_matrix, "Every quadratic form nonnegative.", pattern="symmetric", label="xᵀAx ≥ 0")
m("precision-recall", t_roc, "Of the rows called positive, how many are, and of the positives, how many are called.", point=(0.15, 0.55))
m("preregistration", t_seal, "The claim, bar, null, and budget written before the measurement.")
m("principal-component-analysis", t_spectrum, "Projection onto the top eigenvectors, the identity reader's code.", kept=2)
m("product-quantization", t_blocks, "A vector split into pieces, each with its own codebook.", n=8, highlight=(0, 1, 4, 5), caption="four sub-vectors, four codebooks")
m("projection", t_angle, "The component of one vector along another.", a="u", b="x", deg=40, proj=True, residual=True)
m("quantization", t_bits, "Replacing each number with one of a small set of values.")
m("query-key-value", t_attention, "The query scores each key, and the weights mix the values.")
m("query-set", t_graph, "The rows a benchmark asks about, which decide the hubs.", kind="hub")
m("quotient", t_quotient, "What the reader cannot tell apart.", classes=3)
m("random-forest", t_scatter, "Trees on bootstrap samples with random features at each split, averaged.", kind="tree")
m("rank", t_matrix, "The dimension of the column space.", pattern="lowrank", label="rank two")
m("rank-certificate", t_intervals, "A bound on which neighbour rankings the compression preserved.", kind="ci")
m("rank-faithful", t_scatter, "Compressed distances that keep the exact ranking.", kind="rank")
m("read-direction", t_ellipses, "A direction the consumer is sensitive to.", second=False)
m("read-distortion", t_ellipses, "The error a code costs a reader, weighted by what it reads.")
m("read-operator", t_matrix, "The averaged outer product of the sensitivity with itself.", pattern="lowrank", label="P_C = E[g gᵀ]")
m("read-subspace", t_ellipses, "The directions the consumer reads.", second=False)
m("recall-at-k", t_blocks, "Of the k true neighbours, how many the k returned contain.", n=10, highlight=(0, 1, 2, 4, 5, 6, 8), caption="seven of ten returned are true neighbours")
m("recognizer", t_ladder, "The spectrum read against a finite list of templates, and a refusal when none matches.")
m("reconstruction-error", t_angle, "The squared length of the difference between a row and its approximation.", a="approximation", b="row", deg=25, proj=True, residual=True)
m("refresh-floor", t_timeline, "The shortest renewal that keeps a certificate within its error.", events=[(150, "refresh", SERIES[2]), (330, "refresh", SERIES[2]), (510, "refresh", SERIES[2])], floor=(150, 330))
m("refresh-interval", t_timeline, "The longest renewal period that keeps a certificate within its error.", events=[(150, "refresh", SERIES[2]), (450, "refresh", SERIES[2])], floor=(150, 450))
m("refusal", t_strata, "A number the instrument declines to report, counted as a verdict.", vals=[0.95, 0.93, 0.0, 0.94], labels=["g1", "g2", "refused", "g4"])
m("registered", t_seal, "Written into a sealed file before the measurement.")
m("reliability-weight", t_roc, "Twice the held-out AUROC minus one, or zero.")
m("replica", t_timeline, "A copy of a database on another machine, trailing the primary.", events=[(200, "primary", SERIES[2]), (420, "replica", SERIES[0])], stale_from=200)
m("rerank", t_blocks, "A second scorer reorders the candidate list and cannot add to it.", n=10, highlight=(0, 1, 2, 3, 4, 5), caption="recall is at most the candidate coverage")
m("residualization", t_angle, "The least-squares multiple of one column removed from another.", a="x", b="y", deg=40, proj=True, residual=True)
m("retrieval-augmented-pipeline", t_chain, "Chunker, encoder, index, and generator, each reading the one before.", stages=["chunker", "encoder", "index", "generator"], collapse=0)
m("robin-hood-index", t_lorenz, "The share of retrievals that would have to move to equalize the rows.")
m("roc-curve", t_roc, "True positive rate against false positive rate as the threshold sweeps.", youden=True)
m("rotary-position-embedding", t_rotation, "A rotation by position, under which a head reads relative position only.")
m("rouge", t_venn, "The overlap of the generated text's n-grams with the reference's.", a="reference", b="generated")
m("safe-pruning", t_venn, "A branch dropped without loss because a bound says nothing in it can win.", a="search space", b="pruned", nested=True)
m("sampling", t_intervals, "Which rows to read, and the standard error of the mean of those read.", kind="se")
m("score", t_sigmoid, "A number per row that a threshold turns into a decision.")
m("sealed", t_seal, "Committed with its hash recorded before the measurement.")
m("seed", t_intervals, "The number that fixes a run's pseudo-randomness.", kind="paired")
m("sensitivity", t_parabola, "The gradient of the consumer at a row.", secant=False)
m("session-deck", t_table, "The course's lecture deck, cited by line range.", rows=(("session 3", "the four failure modes", "session-outlines.md:38"), ("session 6", "formula or black box", "session-outlines.md:117-136")), highlight=0)
m("shard", t_blocks, "A partition searched separately, with the answers merged.", n=8, highlight=(0, 1, 2, 3, 4, 5, 6, 7), caption="each shard returns its top k, and the global top k lies in the union")
m("silhouette", t_scatter, "Distance to the nearest other cluster against distance within its own.", kind="silhouette")
m("simpsons-paradox", t_strata, "Every group shows one sign and the aggregate shows the other.", vals=[0.3, 0.35, 0.28], labels=["g1", "g2", "g3"], bar=0.5, kind="none")
m("skewness", t_histogram, "The mean cubed deviation, zero for a symmetric column.", shape="skew")
m("softmax", t_attention, "Exponentials normalized to sum to one.")
m("sources-table", t_table, "For every number, the file and lines it came from.")
m("spearman-correlation", t_scatter, "Pearson's correlation of the ranks.", kind="rank")
m("spectral-clustering", t_graph, "Clustering the row-normalized spectral embedding.", kind="ring")
m("spectral-embedding", t_graph, "A node's values in the low eigenvectors of the Laplacian.", kind="ring")
m("spectrum", t_spectrum, "The eigenvalues of a matrix.")
m("split", t_folds, "The rows a model is fit on and the rows it is scored on.", k=4, test=3)
m("standard-error", t_intervals, "The spread of an estimate over repetitions, falling as one over root n.", kind="se")
m("standardization", t_ellipses, "Each column centred and divided by its spread.", circle=True)
m("stratification", t_strata, "Rows scored in strata, so the minimum can be reported.")
m("sum-of-squared-errors", t_scatter, "The squared distance to the cluster centre, summed.", kind="sse")
m("support", t_venn, "The fraction of transactions that contain the itemset.", a="transactions", b="contain the itemset", nested=True)
m("surrogate", t_ellipses, "A quadratic stand-in for the consumer's output metric.")
m("sweep", t_stepcurve, "A measurement run across a range of one parameter.", kind="sweep")
m("teacher-forcing", t_chain, "The reference token fed in at each step, so an error cannot compound.", stages=["reference", "model", "next token"])
m("template-match", t_ladder, "The spectrum's ratios against a stored template.")
m("tf-idf", t_bars, "Term frequency scaled down by how many documents carry the term.", labels=["the", "of", "spectrum", "kernel", "reader"], vals=[0.02, 0.03, 0.6, 0.45, 0.3], ylabel="weight")
m("threshold", t_sigmoid, "The value that turns a score into a decision.")
m("token", t_blocks, "A piece of text, roughly a word, the unit a language model reads.", n=8, labels=["the", "read", "er", "does", "not", "see", "this", "."], highlight=(1, 2), caption="two tokens for one word")
m("trace", t_matrix, "The sum of the diagonal, the total variance for a covariance.", pattern="diag", label="tr Σ")
m("transaction", t_venn, "One row of a market-basket table.", a="items", b="one basket", nested=True)
m("transmission-time-interval", t_timeline, "The one-millisecond slot a tower schedules in.", events=[(150, "slot", INK3), (250, "slot", INK3), (350, "slot", INK3), (450, "slot", INK3), (550, "slot", INK3)], repeat=[200, 300, 400, 500])
m("truncation", t_spectrum, "The first k components kept and the rest dropped.", kept=3)
m("vacuity-threshold", t_barnull, "The statistic below which the certificate says nothing.", vacuous=True)
m("validity-index", t_scatter, "A score for a clustering without labels.", kind="silhouette")
m("variance", t_histogram, "The mean squared deviation from the mean.", shape="normal")
m("verdict", t_strata, "Pass, fail, or abstain, taken as the worst group.")
m("water-filling", t_spectrum, "Directions below the water get no bits.", water=0.18)
m("weyls-law", t_loglog, "The eigenvalue count grows like the value to half the dimension.")
m("whitening", t_ellipses, "Rescaling so that the covariance becomes the identity.", circle=True)
m("witness", t_timeline, "An independent measurement of whether the certificate's claim was true.", events=[(180, "certificate", SERIES[2]), (460, "witness", SERIES[0])])
m("youden-f1-bound", t_roc, "The Youden index bounds the best F1, for every score.", youden=True)
m("youden-index", t_roc, "True positive rate minus false positive rate at a threshold.", youden=True)


# ================================================================ driver
def main():
    entries = tomllib.load(open(os.path.join(ROOT, "entries.toml"), "rb"))["entry"]
    missing = [e["id"] for e in entries if e["id"] not in M]
    if missing:
        print("no figure mapping for", missing)
        sys.exit(1)
    captions = {}
    for e in entries:
        tpl, kw, cap = M[e["id"]]
        c = canvas()
        tpl(c, ACCENT.get(e["kind"], INK), **kw)
        c.save(os.path.join(FIG, e["id"] + ".svg"), caption=cap)
        captions[e["id"]] = cap
    with open(os.path.join(FIG, "captions.toml"), "w", encoding="utf-8", newline="\n") as f:
        for k, v in sorted(captions.items()):
            f.write(f'{k} = "{v.replace(chr(34), chr(39))}"\n')
    print("drew", len(entries), "figures")


if __name__ == "__main__":
    main()
