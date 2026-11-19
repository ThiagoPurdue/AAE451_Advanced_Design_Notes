"""Figures for Lecture 12, Carpet Plots and Sensitivity Analysis.

One published example: the fighter sizing matrix of Raymer, Aircraft Design: A
Conceptual Approach, 5th ed., AIAA, 2012, Section 19.4. Nine sizing runs at
W_TO/S = 50, 60, 70 lb/ft2 and T_SL/W_TO = 0.9, 1.0, 1.1; each run gives W_TO and
three constraint values: takeoff distance (limit 500 ft), P_s at Mach 0.9, 5 g,
30,000 ft (limit 0 ft/s), and the time to accelerate from Mach 0.9 to 1.5 (limit
50 s). Nothing else is assumed: every curve is the quadratic through three runs,
every crossing is read inside the matrix, and the offset is 6 lb/ft2 per curve.
Every number the lecture quotes is recomputed here and asserted before anything
is drawn; each figure function then measures what it drew.

The aspect-ratio figure is a schematic: shapes only, from scripts/carpet/ar-schematic.json
(see the README beside it).

Run from the book folder:

    python3 -B scripts/make_carpet_figures.py

Set FIG_PREVIEW=<folder> to also write PNG copies for checking.
"""
import json
import os
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.colors import to_rgb
from matplotlib.legend_handler import HandlerBase
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Polygon
from matplotlib.path import Path as MPath
from matplotlib.text import Text

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "notes" / "lecture-12" / "figures"
AR_DATA = HERE / "carpet" / "ar-schematic.json"
PREVIEW = os.environ.get("FIG_PREVIEW")

plt.rcParams.update({
    "svg.fonttype": "none",
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 12,
    "axes.titlesize": 12,
    "axes.labelsize": 12,
    "axes.edgecolor": "#000000",
    "axes.labelcolor": "#000000",
    "xtick.color": "#000000",
    "ytick.color": "#000000",
    "savefig.facecolor": "white",
})
INK, STEEL, GRAY = "#000000", "#555960", "#6F727B"
DUST, BAND = "#EBD99F", "#EBEBEB"
# Okabe-Ito for the data series; the reddish purple of the source, not the house #AA4499
BLUE, VERM, GREEN, SKY, PURPLE = "#0072B2", "#D55E00", "#009E73", "#56B4E9", "#CC79A7"
FS = 11.5                                           # annotation size


# ------------------------------------------------------------------ helpers
def _lum(c):
    rgb = np.array(to_rgb(c))
    lin = np.where(rgb <= 0.03928, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    return float(lin @ [0.2126, 0.7152, 0.0722])


def contrast(a, b="#FFFFFF"):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def shade(c, target=4.6):
    """The color darkened toward black until text in it reaches the target contrast on white."""
    rgb = np.array(to_rgb(c))
    k = 1.0
    while contrast(tuple(rgb * k)) < target:
        k -= 0.01
    return matplotlib.colors.to_hex(tuple(rgb * k))


# label colors: the line color where it reaches 4.5:1 on white, a darker shade where it does not
TXT = {c: (c if contrast(c) >= 4.5 else shade(c)) for c in (BLUE, VERM, GREEN, SKY, PURPLE, INK, STEEL)}
assert TXT[BLUE] == BLUE and TXT[SKY] != SKY and TXT[PURPLE] != PURPLE, "sky blue and reddish purple need a darker shade"


def save(fig, name):
    """Write the SVG (and a PNG preview); every text drawn must reach 4.5:1 on white."""
    for t in fig.findobj(Text):
        if t.get_visible() and t.get_text().strip():
            assert contrast(t.get_color()) >= 4.5, f"{name}: label {t.get_text()!r} in {t.get_color()}"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight", pad_inches=0.1)
    if PREVIEW:
        fig.savefig(Path(PREVIEW) / f"{name}.png", dpi=110, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)
    print("wrote", name)


def clean(ax, grid=False):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if grid:
        ax.grid(True, color="#DDDDDD", lw=0.6)


def close(a, b, tol, what):
    assert abs(a - b) <= tol, f"{what}: {a:.4f} vs {b:.4f}"


def thousands(ax, axis="y"):
    fmt = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(fmt)


def bisect(fun, lo, hi):
    """Root of fun between lo and hi; the bracket must hold one sign change."""
    f_lo = fun(lo)
    assert (f_lo > 0) != (fun(hi) > 0), "bisect: no sign change in the bracket"
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        if (fun(mid) > 0) == (f_lo > 0):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def fmt(x, spec):
    """A number as the lecture prints it: thousands comma, true minus sign."""
    return format(x, spec).replace("-", "−")


# ---------------------------------------------------------------- the nine runs
WSV = np.array([50.0, 60.0, 70.0])                  # W_TO/S, lb/ft2
TWV = np.array([0.9, 1.0, 1.1])                     # T_SL/W_TO
# rows T/W 0.9, 1.0, 1.1; columns W/S 50, 60, 70 (Raymer 2012, Sec. 19.4)
W0 = np.array([[43500, 39000, 36000], [48500, 43700, 41000], [56000, 49000, 45000]], float)
DTO = np.array([[670, 810, 1070], [450, 595, 800], [340, 430, 660]], float)
PS = np.array([[140, -230, -320], [430, 30, -190], [700, 330, 30]], float)
ACC = np.array([[56, 53, 51], [50.5, 47, 45], [46, 42, 39]], float)
RUNS = {"Dto": DTO, "Ps": PS, "Acc": ACC}
LIM = {"Dto": 500.0, "Ps": 0.0, "Acc": 50.0}
CON = ("Dto", "Ps", "Acc")
OFFSET = 6.0                                        # lb/ft2 per T/W curve, for the plot only

# What the lecture prints, as printed. Every entry is compared with a number computed or
# measured on a figure below; none is used to compute anything.
PUB = dict(
    Wk={(0.9, 50): "43.5", (0.9, 60): "39.0", (0.9, 70): "36.0", (1.0, 50): "48.5", (1.0, 60): "43.7",
        (1.0, 70): "41.0", (1.1, 50): "56.0", (1.1, 60): "49.0", (1.1, 70): "45.0"},
    # runs that miss a limit (bold in the matrix table): (T/W, W/S): constraints missed
    bad={(0.9, 50): {"Dto", "Acc"}, (0.9, 60): {"Dto", "Ps", "Acc"}, (0.9, 70): {"Dto", "Ps", "Acc"},
         (1.0, 50): {"Acc"}, (1.0, 60): {"Dto"}, (1.0, 70): {"Dto", "Ps"},
         (1.1, 50): set(), (1.1, 60): set(), (1.1, 70): {"Dto"}},
    feasible_runs=("56,000", "49,000"),
    on_curves={"Dto": ("none", "53.9", "63.8"), "Ps": ("53.0", "61.0", "none"), "Acc": ("none", "51.2", "none")},
    on_lines={"Dto": ("0.972", "1.054", "none"), "Ps": ("none", "0.989", "1.088"), "Acc": ("1.010", "0.948", "0.917")},
    mark_a="53.9", mark_b_tw="0.972", mark_b_w="46,900",
    w_best="46,300", ws_best="56", tw_best="1.017", ps_best="217", acc_best="47.3",
    saved="2,700", best_run="49,000", flat=("53", "60"), swap="52.6",
    offset="6", offset_slope="60",
    dws_b="−481", dtw_b="56,300", s_ws_b="−0.58", s_tw_b="1.24",
)


def lag(xs, x):
    x = np.asarray(x, float)
    return [(x - xs[1]) * (x - xs[2]) / ((xs[0] - xs[1]) * (xs[0] - xs[2])),
            (x - xs[0]) * (x - xs[2]) / ((xs[1] - xs[0]) * (xs[1] - xs[2])),
            (x - xs[0]) * (x - xs[1]) / ((xs[2] - xs[0]) * (xs[2] - xs[1]))]


def surf(M):
    """The biquadratic through the nine runs: a quadratic along every curve and every line of the matrix."""
    def f(ws, tw):
        a, b = lag(WSV, ws), lag(TWV, tw)
        return sum(b[i] * a[j] * M[i][j] for i in range(3) for j in range(3))
    return f


fW = surf(W0)
F = {k: surf(M) for k, M in RUNS.items()}
# violation > 0 where the requirement is not met
VIOL = {"Dto": lambda w, t: F["Dto"](w, t) - LIM["Dto"],
        "Ps": lambda w, t: LIM["Ps"] - F["Ps"](w, t),
        "Acc": lambda w, t: F["Acc"](w, t) - LIM["Acc"]}


def xoff(ws, tw):
    """Abscissa of the carpet plot: W/S plus 6 lb/ft2 per T/W curve above the lowest."""
    return ws + OFFSET * (np.asarray(tw) - TWV[0]) / (TWV[1] - TWV[0])


def roots_in(xs, ys, limit):
    """Where the quadratic through three points meets the limit, inside the three points only."""
    c = np.polyfit(xs, np.asarray(ys, float) - limit, 2)
    return [r.real for r in np.roots(c) if abs(r.imag) < 1e-9 and xs[0] - 1e-9 <= r.real <= xs[-1] + 1e-9]


def floor_tw(k, ws):
    """Lowest T/W that meets constraint k at this W/S: 0.9 if always met, inf if never."""
    v = VIOL[k]
    if v(ws, TWV[0]) <= 0:
        return TWV[0]
    if v(ws, TWV[-1]) > 1e-7:
        return np.inf
    if v(ws, TWV[-1]) >= 0:                         # the crossing sits on the T/W = 1.1 curve
        return TWV[-1]
    return bisect(lambda t: v(ws, t), TWV[0], TWV[-1])


def _compute():
    """Steps 1 to 5 of the lecture on the nine runs; returns everything the figures draw."""
    g = {}
    gw, gt = np.meshgrid(np.linspace(50, 70, 41), np.linspace(0.9, 1.1, 41))
    for k, v in VIOL.items():
        assert np.all(np.diff(v(gw, gt), axis=0) < 0), f"{k} must ease as T/W rises"
    assert np.all(np.diff(fW(gw, gt), axis=0) > 0) and np.all(np.diff(fW(gw, gt), axis=1) < 0), \
        "W_TO rises with T/W and falls with W/S"
    # step 1: which runs meet every limit
    feas = [(i, j) for i in range(3) for j in range(3) if all(VIOL[k](WSV[j], TWV[i]) <= 0 for k in CON)]
    g["feasible_runs"] = feas
    # step 3: crossings on the T/W curves (a W/S) and on the W/S lines (a T/W), inside the matrix
    on_tw, on_ws = {}, {}
    for k, M in RUNS.items():
        on_tw[k], on_ws[k] = [], []
        for i in range(3):
            r = roots_in(WSV, M[i], LIM[k])
            assert len(r) <= 1
            on_tw[k].append(r[0] if r else None)
        for j in range(3):
            r = roots_in(TWV, M[:, j], LIM[k])
            assert len(r) <= 1
            on_ws[k].append(r[0] if r else None)
    g["on_tw"], g["on_ws"] = on_tw, on_ws
    # the constraint lines on constraint-diagram axes, from the left to the right edge of the matrix
    fine = np.linspace(50, 70, 2001)
    lines = {}
    for k in CON:
        pts = [(w, floor_tw(k, w)) for w in fine]
        pts = [(w, t) for w, t in pts if TWV[0] < t <= TWV[-1]]
        lines[k] = tuple(np.array(pts).T)
        marks = [(x, TWV[i]) for i, x in enumerate(on_tw[k]) if x is not None] + \
                [(WSV[j], x) for j, x in enumerate(on_ws[k]) if x is not None]
        for w_, t_ in marks:                        # every crossing lies on the constraint line
            close(floor_tw(k, w_), t_, 2e-3, f"{k} mark on its line")
        g[f"marks_{k}"] = np.array(marks)
    g["lines"] = lines
    # step 5: the feasible region and its lowest point
    need = np.array([max(floor_tw(k, w) for k in CON) for w in fine])
    ok = need <= TWV[-1]
    ws_ok = fine[ok]
    w_low = fW(ws_ok, need[ok])
    i_best = int(np.argmin(w_low))
    g["best"] = (ws_ok[i_best], need[ok][i_best], w_low[i_best])
    g["ws_ok"], g["need_ok"], g["w_low"] = ws_ok, need[ok], w_low
    g["active"] = [k for k in CON if abs(floor_tw(k, ws_ok[i_best]) - need[ok][i_best]) < 1e-6]
    g["ps_never_active"] = all(floor_tw("Ps", w) < max(floor_tw("Dto", w), floor_tw("Acc", w)) for w in ws_ok)
    g["swap"] = bisect(lambda w: floor_tw("Dto", w) - floor_tw("Acc", w), 50, 60)
    # the feasible region inside the matrix: the lower boundary, then back along T/W = 1.1
    g["feas_ws"] = np.concatenate([ws_ok, ws_ok[::-1]])
    g["feas_tw"] = np.concatenate([need[ok], np.full_like(ws_ok, TWV[-1])])
    return g


G = _compute()


def published_checks():
    """Every number the lecture quotes, recomputed from the nine runs."""
    for i, tw in enumerate(TWV):                    # the matrix table: which values miss their limit
        for j, ws in enumerate(WSV):
            missed = {k for k in CON if VIOL[k](ws, tw) > 0}
            assert missed == PUB["bad"][(tw, ws)], (tw, ws, missed)
    best_runs = sorted((f"{W0[i, j]:,.0f}" for i, j in G["feasible_runs"]), reverse=True)
    assert tuple(best_runs) == PUB["feasible_runs"], best_runs
    for k in CON:                                   # the crossings table, "none" where the matrix has none
        got_c = tuple("none" if x is None else f"{x:.1f}" for x in G["on_tw"][k])
        got_l = tuple("none" if x is None else f"{x:.3f}" for x in G["on_ws"][k])
        assert got_c == PUB["on_curves"][k], (k, got_c)
        assert got_l == PUB["on_lines"][k], (k, got_l)
    ws_b, tw_b, w_b = G["best"]
    assert f"{round(w_b, -2):,.0f}" == PUB["w_best"] and f"{ws_b:.0f}" == PUB["ws_best"] and f"{tw_b:.3f}" == PUB["tw_best"]
    assert G["active"] == ["Dto"] and G["ps_never_active"], "takeoff alone sets the lightest point; P_s never active"
    assert all(floor_tw("Dto", w) > floor_tw("Ps", w) for w in np.linspace(50, 70, 401)), "takeoff stricter than P_s"
    assert f"{F['Ps'](ws_b, tw_b):.0f}" == PUB["ps_best"] and f"{F['Acc'](ws_b, tw_b):.1f}" == PUB["acc_best"]
    best_run = min(W0[i, j] for i, j in G["feasible_runs"])
    assert f"{best_run:,.0f}" == PUB["best_run"] and f"{best_run - round(w_b, -2):,.0f}" == PUB["saved"]
    flat = G["ws_ok"][G["w_low"] <= w_b + 200]
    assert (f"{flat[0]:.0f}", f"{flat[-1]:.0f}") == PUB["flat"], (flat[0], flat[-1])
    assert f"{G['swap']:.1f}" == PUB["swap"]
    # sensitivities at the lightest feasible point, on the fit of the nine runs
    h = 0.02                                        # central differences, 2% steps
    dws_b = (fW(ws_b * (1 + h), tw_b) - fW(ws_b * (1 - h), tw_b)) / (2 * h * ws_b)
    dtw_b = (fW(ws_b, tw_b * (1 + h)) - fW(ws_b, tw_b * (1 - h))) / (2 * h * tw_b)
    assert fmt(dws_b, ",.0f") == PUB["dws_b"] and fmt(round(dtw_b, -2), ",.0f") == PUB["dtw_b"], (dws_b, dtw_b)
    assert fmt(ws_b / w_b * dws_b, ".2f") == PUB["s_ws_b"] and fmt(tw_b / w_b * dtw_b, ".2f") == PUB["s_tw_b"]
    # the offset (6 per curve, 60 per unit) is checked on the drawn runs and marks of offset_curves()


published_checks()


# ------------------------------------------------------------- drawing pieces
TW_STYLE = [dict(color=SKY, ls=(0, (4.5, 2.5)), lw=2.2),          # 0.9: sky blue, dashed
            dict(color=BLUE, ls="-", lw=2.2),                     # 1.0: blue, solid
            dict(color=INK, ls=(0, (7, 2.5, 1.5, 2.5)), lw=2.2)]  # 1.1: black, dash-dot
CON_COLOR = {"Dto": VERM, "Ps": PURPLE, "Acc": GREEN}
CON_NAME = {"Dto": "takeoff", "Ps": "$P_s$", "Acc": "acceleration"}
CON_KEY = {"Dto": "takeoff ≤ 500 ft", "Ps": "$P_s$ ≥ 0", "Acc": "acceleration ≤ 50 s"}
D_TICK = 0.011                                      # tick length, in T/W
WSF = np.linspace(50, 70, 81)
TWF = np.linspace(0.9, 1.1, 41)


def _y(space, ws, tw):
    return np.asarray(tw, float) if space == "tw" else fW(ws, tw)


def _x(coord, ws, tw):
    return np.asarray(ws, float) + 0.0 * np.asarray(tw, float) if coord == "ws" else xoff(ws, tw)


def draw_curves(ax, coord, grid_lines=True):
    """The three T/W curves (W_TO against W/S) and the three W/S lines; returns the curves drawn."""
    out, lines = [], []
    if grid_lines:
        for ws in WSV:
            lines += ax.plot(_x(coord, ws, TWF), fW(ws, TWF), color=STEEL, lw=0.9, zorder=2)
    for i, tw in enumerate(TWV):
        out += ax.plot(_x(coord, WSF, tw), fW(WSF, tw), zorder=3, **TW_STYLE[i])
    draw_curves.lines = lines                       # the W/S lines of the last call
    return out


def draw_nodes(ax, coord, size=6.5):
    xs = [_x(coord, WSV[j], TWV[i]) for i in range(3) for j in range(3)]
    ys = [W0[i, j] for i in range(3) for j in range(3)]
    return ax.plot(xs, ys, "o", ms=size, mfc="white", mec=STEEL, mew=1.6, ls="none", zorder=6)[0]


def tick_segments(k, space, coord):
    """Short ticks on the failing side of a constraint line: toward lower T/W, every 2 lb/ft2 of W/S."""
    w, t = G["lines"][k]
    sel = [i for i in range(len(w)) if abs((w[i] - w[0]) / 2.0 - round((w[i] - w[0]) / 2.0)) < 1e-6]
    sel = [i for i in sel if t[i] - D_TICK >= TWV[0] - 0.02]
    return [((float(_x(coord, w[i], t[i])), float(_y(space, w[i], t[i]))),
             (float(_x(coord, w[i], t[i] - D_TICK)), float(_y(space, w[i], t[i] - D_TICK))), w[i], t[i] - D_TICK)
            for i in sel]


def draw_constraints(ax, space, coord, marks=False):
    """The three constraint lines with their ticks; every tick ends on the failing side.

    Returns the drawn lines and, if marks is set, the drawn marks (filled dots), each a dict by constraint."""
    drawn, dots = {}, {}
    for k in ("Ps", "Acc", "Dto"):
        w, t = G["lines"][k]
        col = CON_COLOR[k]
        drawn[k] = ax.plot(_x(coord, w, t), _y(space, w, t), color=col, lw=3.0, zorder=4, solid_capstyle="butt")[0]
        segs = tick_segments(k, space, coord)
        for (p0, p1, w_end, t_end) in segs:
            assert VIOL[k](w_end, t_end) > 0, f"{k}: a tick ends on the passing side"
            ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=col, lw=1.0, zorder=4)
        assert len(segs) >= 4, k
        if marks:
            m = G[f"marks_{k}"]
            dots[k] = ax.plot(_x(coord, m[:, 0], m[:, 1]), _y(space, m[:, 0], m[:, 1]), "o", color=col,
                              mec="white", mew=0.8, ms=8, ls="none", zorder=7)[0]
    return drawn, dots


def draw_feasible(ax, space, coord):
    pw, pt = G["feas_ws"], G["feas_tw"]
    poly = Polygon(np.column_stack([_x(coord, pw, pt), _y(space, pw, pt)]), closed=True, fc=DUST, ec="none", zorder=1)
    ax.add_patch(poly)
    return poly


def draw_best(ax, space, coord):
    ws_b, tw_b, w_b = G["best"]
    return ax.plot(_x(coord, ws_b, tw_b), _y(space, ws_b, tw_b), "D", color=INK, ms=11, mec="white", mew=0.8,
                   zorder=9)[0]


class _TickedLine(HandlerBase):
    """Legend key for a constraint line: the line with short ticks on its failing side."""
    def create_artists(self, legend, orig, xd, yd, width, height, fontsize, trans):
        col, lw = orig.get_color(), orig.get_linewidth()
        y0 = yd + height * 0.62
        arts = [Line2D([xd, xd + width], [y0, y0], color=col, lw=lw, transform=trans)]
        for f in (0.2, 0.5, 0.8):
            arts.append(Line2D([xd + f * width] * 2, [y0, y0 - height * 0.55], color=col, lw=1.0, transform=trans))
        return arts


def constraint_legend(fig_or_ax, feasible=True, ncol=4, fontsize=FS, **kw):
    handles = [Line2D([], [], color=CON_COLOR[k], lw=3.0) for k in CON]
    labels = [CON_KEY[k] for k in CON]
    hmap = {h: _TickedLine() for h in handles}
    handles.append(Line2D([], [], color=STEEL, lw=1.6))
    labels.append("ticks on the failing side")
    hmap[handles[-1]] = _TickedLine()
    if feasible:
        handles.append(Patch(fc=DUST, ec="none"))
        labels.append("feasible")
    return fig_or_ax.legend(handles, labels, handler_map=hmap, frameon=False, fontsize=fontsize, ncol=ncol,
                            handlelength=2.6, columnspacing=1.3, **kw)


def tw_labels(ax, coord, x_pad=0.5, long_hi=True, fs=FS):
    """Direct labels at the right end of the T/W curves (the W/S = 70 run)."""
    out = []
    for i, tw in enumerate(TWV):
        text = f"$T_{{SL}}/W_{{TO}}$ = {tw:.1f}" if (long_hi and i == 2) else f"{tw:.1f}"
        low = coord == "x" and i == 2 and not long_hi        # below its run, clear of the W/S = 70 label
        out.append(ax.text(float(_x(coord, 70.0, tw)) + x_pad, W0[i, 2] - (500 if low else 0), text,
                           color=TXT[TW_STYLE[i]["color"]], fontsize=fs, ha="left", va="top" if low else "center",
                           zorder=8))
    return out


def ws_axis(ax, label=True):
    ax.set_xlim(42, 84)                             # room left of the 50 line for the "acceleration" label
    ax.set_ylim(33000, 58500)
    ax.set_xticks([50, 60, 70])
    if label:
        ax.set_xlabel("$W_{TO}/S$ (lb/ft²)")
    ax.set_ylabel("$W_{TO}$ (lb)")
    thousands(ax)
    clean(ax)


def check_curves(curves, coord):
    """Each drawn T/W curve passes through its three runs and falls as W/S rises."""
    for i, ln in enumerate(curves):
        x, y = ln.get_xdata(), ln.get_ydata()
        assert np.all(np.diff(y) < 0), "W_TO falls as W/S rises"
        for j, ws in enumerate(WSV):
            yy = float(np.interp(float(_x(coord, ws, TWV[i])), x, y))
            assert f"{yy / 1000:.1f}" == PUB["Wk"][(TWV[i], ws)], (TWV[i], ws, yy)


def check_lines_on_curves(ax, drawn, space, coord):
    """The drawn constraint lines pass through every crossing of the table."""
    for k, ln in drawn.items():
        x, y = ln.get_xdata(), ln.get_ydata()
        for w_, t_ in G[f"marks_{k}"]:
            d = np.min(np.hypot((x - _x(coord, w_, t_)) / 20.0,
                                (y - _y(space, w_, t_)) / (0.2 if space == "tw" else 20000.0)))
            assert d < 2e-3, (k, w_, t_, d)


def inside(poly, x, y, ax):
    """Point (data units) inside the drawn polygon, tested in display space."""
    return poly.get_path().transformed(ax.transData).contains_point(ax.transData.transform((x, y)))


# ------------------------------------------------------------- page 1 figures
def question_constraint_axes():
    """The nine runs on constraint-diagram axes, W_TO in 1,000 lb, with the constraint lines."""
    fig, ax = plt.subplots(figsize=(7.6, 5.4))
    poly = draw_feasible(ax, "tw", "ws")
    drawn, _ = draw_constraints(ax, "tw", "ws")
    check_lines_on_curves(ax, drawn, "tw", "ws")
    gw, gt = np.meshgrid(WSV, TWV)
    ax.plot(gw.ravel(), gt.ravel(), "o", color=INK, ms=7, ls="none", zorder=8)
    pos = {(0, 0): (49.4, 0.9, "right", "center"), (1, 0): (49.4, 1.0, "right", "center"),
           (2, 0): (49.4, 1.1, "right", "center"), (0, 1): (60.4, 0.9, "left", "bottom"),
           (1, 1): (59.7, 1.004, "right", "bottom"), (2, 1): (60.4, 1.103, "left", "bottom"),
           (0, 2): (70.6, 0.897, "left", "top"), (1, 2): (70.6, 1.0, "left", "center"),
           (2, 2): (70.6, 1.103, "left", "bottom")}
    labels = {}
    for i in range(3):
        for j in range(3):
            x, y, ha, va = pos[(i, j)]
            ok = (i, j) in G["feasible_runs"]
            labels[(i, j)] = ax.text(x, y, f"{W0[i, j] / 1000:.1f}", fontsize=FS, ha=ha, va=va, zorder=9,
                                     fontweight="bold" if ok else "normal")
    # measured: the labels print the published W_TO, bold exactly on the runs inside the shaded region
    for (i, j), t in labels.items():
        assert t.get_text() == PUB["Wk"][(TWV[i], WSV[j])]
        bold = t.get_fontweight() == "bold"
        assert bold == ((i, j) in G["feasible_runs"])
        if bold:                                    # a feasible run sits on the edge of the region, inside it
            assert inside(poly, WSV[j] + 0.15, TWV[i] - 0.004, ax), (i, j)
    assert sorted(t.get_text() for t in labels.values() if t.get_fontweight() == "bold") == ["49.0", "56.0"]
    for (i, j) in [(i, j) for i in range(3) for j in range(3) if (i, j) not in G["feasible_runs"]]:
        assert not inside(poly, WSV[j], TWV[i], ax), (i, j)
    w, t = G["lines"]["Dto"]
    ax.text(w[-1] + 0.3, t[-1] + 0.006, "takeoff", color=TXT[VERM], fontsize=FS, ha="left", va="bottom")
    w, t = G["lines"]["Ps"]
    ax.text(70.3, t[-1] - 0.004, "$P_s$", color=TXT[PURPLE], fontsize=FS + 1, ha="left", va="top")
    w, t = G["lines"]["Acc"]
    ax.text(70.3, t[-1] + 0.004, CON_NAME["Acc"], color=TXT[GREEN], fontsize=FS, ha="left", va="bottom")
    ax.set_xlim(43, 76)
    ax.set_ylim(0.87, 1.14)
    ax.set_xticks([50, 60, 70])
    ax.set_yticks([0.9, 1.0, 1.1])
    ax.set_xlabel("$W_{TO}/S$ (lb/ft²)")
    ax.set_ylabel("$T_{SL}/W_{TO}$")
    clean(ax)
    constraint_legend(fig, ncol=3, loc="lower center", bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.12, 1, 1))
    save(fig, "question-constraint-axes")


def _carpet(ax, labels=True, fs=FS, marks=False):
    """The finished carpet plot on one axes: offset curves, W/S lines, constraint lines (with their marks if
    marks is set), region, runs, diamond."""
    poly = draw_feasible(ax, "w0", "x")
    curves = draw_curves(ax, "x")
    drawn, dots = draw_constraints(ax, "w0", "x", marks=marks)
    nodes = draw_nodes(ax, "x", size=6)
    best = draw_best(ax, "w0", "x")
    check_curves(curves, "x")
    check_lines_on_curves(ax, drawn, "w0", "x")
    if labels:
        for k, ha, va, dx in (("Dto", "right", "center", -0.4), ("Ps", "right", "top", -0.2), ("Acc", "right", "bottom", -0.9)):
            w, t = G["lines"][k]
            ax.text(float(xoff(w[0], t[0])) + dx - (0.9 if marks else 0.0), float(fW(w[0], t[0])), CON_NAME[k], color=TXT[CON_COLOR[k]],
                    fontsize=fs + (1 if k == "Ps" else 0), ha=ha, va=va, zorder=8)
        for j, ws in enumerate(WSV):
            text = f"$W_{{TO}}/S$ = {ws:.0f}" if j == 0 else f"{ws:.0f}"
            ax.text(float(xoff(ws, 1.1)) + 0.4, W0[2, j] + 400, text, color=STEEL, fontsize=fs, ha="left",
                    va="bottom", zorder=8)
    ax.set_ylim(32500, 58500)
    ax.set_ylabel("$W_{TO}$ (lb)")
    ax.set_yticks(range(35000, 55001, 5000))
    thousands(ax)
    clean(ax)
    ax.spines["bottom"].set_visible(False)        # step 6: no horizontal axis
    ax.set_xticks([])
    # measured: the diamond is the lowest point of the shaded region
    ys = poly.get_xy()[:, 1]
    close(ys.min(), best.get_ydata()[0], 1.0, "the diamond is the lowest point of the feasible region")
    assert f"{round(best.get_ydata()[0], -2):,.0f}" == PUB["w_best"]
    # measured: the runs are drawn at the published weights, and each run sits the printed offset to the
    # right of the run of equal W/S on the curve below
    nx, ny = nodes.get_xdata().reshape(3, 3), nodes.get_ydata().reshape(3, 3)
    for i in range(3):
        for j in range(3):
            assert f"{ny[i, j] / 1000:.1f}" == PUB["Wk"][(TWV[i], WSV[j])]
            if i:
                assert f"{nx[i, j] - nx[i - 1, j]:.0f}" == PUB["offset"], (i, j, nx[i, j] - nx[i - 1, j])
    return poly, curves, drawn, dots, nodes, best


def carpet_plot():
    """The finished carpet plot with its callouts."""
    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    poly, curves, drawn, _, nodes, best = _carpet(ax)
    ws_lines = draw_curves.lines
    lab = tw_labels(ax, "x")
    lab[2].set_va("top")
    lab[2].set_y(W0[2, 2] - 500)
    ws_b, tw_b, w_b = G["best"]
    callouts = [
        ("constant $T_{SL}/W_{TO}$ curve", (85.5, 52600), (78.4, float(fW(66.4, 1.1))), "center", "bottom", curves[2]),
        ("constant $W_{TO}/S$ line", (87.5, 37300), (float(xoff(70, 1.05)), float(fW(70, 1.05))), "center", "top", None),
        ("one sizing run", (51.5, 35300), (float(xoff(60, 0.9)) - 0.5, W0[0, 1] - 120), "center", "top", "node"),
        (f"lightest feasible point:\n{round(w_b, -2):,.0f} lb, {ws_b:.0f} lb/ft²,\n$T_{{SL}}/W_{{TO}}$ = {tw_b:.3f}",
         (43.0, 51400),
         (float(xoff(ws_b, tw_b)) - 0.6, w_b + 250), "left", "bottom", "best"),
    ]
    for text, xy_t, xy, ha, va, target in callouts:
        rel = (1.0, 0.0) if target == "best" else (0.5, 0.5)      # clear of the acceleration label
        ax.annotate(text, xy=xy, xytext=xy_t, fontsize=FS, ha=ha, va=va, zorder=10,
                    arrowprops=dict(arrowstyle="-|>", color=STEEL, lw=1.0, shrinkA=3, shrinkB=2, relpos=rel))
        # measured: each arrow ends on what it names
        if target == "node":
            d = np.min(np.hypot(nodes.get_xdata() - xy[0], (nodes.get_ydata() - xy[1]) / 1000))
            assert d < 1.0, d
        elif target == "best":
            close(xy[0], best.get_xdata()[0], 1.0, "arrow to the diamond, x")
            close(xy[1], best.get_ydata()[0], 600, "arrow to the diamond, y")
        elif target is None:
            x, y = ws_lines[2].get_xdata(), ws_lines[2].get_ydata()
            close(float(np.interp(xy[0], x, y)), xy[1], 150, "arrow on the W/S = 70 line")
        else:
            x, y = target.get_xdata(), target.get_ydata()
            close(float(np.interp(xy[0], x, y)), xy[1], 150, "arrow on the T/W = 1.1 curve")
    lbl = callouts[3][0]
    assert lbl.endswith(f"{PUB['w_best']} lb, {PUB['ws_best']} lb/ft²,\n$T_{{SL}}/W_{{TO}}$ = {PUB['tw_best']}"), lbl
    ax.set_xlim(42, 95)
    constraint_legend(fig, ncol=3, loc="lower center", bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.11, 1, 1))
    save(fig, "carpet-plot")


def sizing_plot():
    """Step 2: W_TO against W/S, one curve per T/W through its three runs, and the three W/S lines."""
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    curves = draw_curves(ax, "ws")
    nodes = draw_nodes(ax, "ws")
    tw_labels(ax, "ws", x_pad=0.6)
    check_curves(curves, "ws")
    # measured: on every W/S line the weight rises with T/W
    ny = nodes.get_ydata().reshape(3, 3)
    assert np.all(np.diff(ny, axis=0) > 0) and np.all(np.diff(ny, axis=1) < 0)
    ws_axis(ax)
    fig.tight_layout()
    save(fig, "sizing-plot")


def cross_plots():
    """Step 3: each constraint against W/S, one curve per T/W; takeoff against T/W, one line per W/S."""
    fig, axs = plt.subplots(2, 2, figsize=(9.6, 7.8))
    fs = 12.5                                       # full column: 9 pt or more at 700 px
    panels = [("Dto", axs[0, 0], (250, 1150), "Takeoff distance (ft)", 500, "limit 500 ft"),
              ("Ps", axs[0, 1], (-420, 800), "$P_s$ (ft/s)", 0, "limit 0 ft/s"),
              ("Acc", axs[1, 0], (37, 58), "Acceleration time (s)", 50, "limit 50 s")]
    wsf = np.linspace(50, 70, 81)
    for k, ax, ylim, ylabel, lim, ltext in panels:
        M = RUNS[k]
        fail_hi = k != "Ps"                         # the failing side: above the limit, below for P_s
        ax.axhspan(lim, ylim[1] if fail_hi else ylim[0], color=BAND, lw=0, zorder=0)
        ax.axhline(lim, color=STEEL, lw=1.2, ls=":", zorder=1)
        if fail_hi:
            ax.text(75.8, lim - 0.015 * (ylim[1] - ylim[0]), ltext, fontsize=fs, ha="right", va="top", color=STEEL)
        else:                                       # P_s: below the line at the left, clear of the curve labels
            ax.text(47.4, lim - 0.05 * (ylim[1] - ylim[0]), ltext, fontsize=fs, ha="left", va="top", color=STEEL)
        fx, fha = {"Dto": (47.4, "left"), "Ps": (55.0, "left"), "Acc": (75.8, "right")}[k]   # clear of the runs
        ax.text(fx, ylim[1] - 0.03 * (ylim[1] - ylim[0]) if fail_hi else ylim[0] + 0.03 * (ylim[1] - ylim[0]),
                "fails", fontsize=fs, ha=fha, va="top" if fail_hi else "bottom", color=STEEL, style="italic")
        for i, tw in enumerate(TWV):
            st = TW_STYLE[i]
            ln = ax.plot(wsf, F[k](wsf, tw), zorder=3, **st)[0]
            ax.plot(WSV, M[i], "o", ms=6.5, mfc="white", mec=st["color"], mew=1.6, ls="none", zorder=4)
            ax.text(70.9, M[i, 2], f"{tw:.1f}", color=TXT[st["color"]], fontsize=fs, ha="left", va="center")
            # measured: the drawn curve passes through the runs
            for j in range(3):
                close(float(np.interp(WSV[j], ln.get_xdata(), ln.get_ydata())), M[i, j], 1e-6, "curve through run")
        xs = [x for x in G["on_tw"][k] if x is not None]
        dots = ax.plot(xs, [lim] * len(xs), "o", color=CON_COLOR[k], mec=INK, mew=0.8, ms=10, ls="none", zorder=6)[0]
        # measured: the filled dots sit where the drawn curves meet the limit, at the table's W/S
        got = tuple("none" if x is None else f"{x:.1f}" for x in G["on_tw"][k])
        assert got == PUB["on_curves"][k]
        for x, i in zip(dots.get_xdata(), [i for i, x in enumerate(G["on_tw"][k]) if x is not None]):
            close(float(F[k](x, TWV[i])), lim, 1e-6, f"{k}: crossing on the {TWV[i]} curve")
        ax.set_xlim(47, 76)
        ax.set_ylim(*ylim)
        ax.set_xticks([50, 60, 70])
        ax.set_xlabel("$W_{TO}/S$ (lb/ft²)")
        ax.set_ylabel(ylabel)
        if k == "Dto":
            thousands(ax)
        clean(ax)
    # takeoff distance against T/W, one line per W/S
    ax = axs[1, 1]
    ax.axhspan(500, 1150, color=BAND, lw=0, zorder=0)
    ax.axhline(500, color=STEEL, lw=1.2, ls=":", zorder=1)
    ax.text(1.158, 1150 - 27, "fails", fontsize=fs, ha="right", va="top", color=STEEL, style="italic")
    ax.text(1.158, 515, "limit 500 ft", fontsize=fs, ha="right", va="bottom", color=STEEL)
    twf = np.linspace(0.9, 1.1, 41)
    ws_style = [dict(ls="-"), dict(ls=(0, (4.5, 2.5))), dict(ls=(0, (7, 2.5, 1.5, 2.5)))]
    for j, ws in enumerate(WSV):
        ln = ax.plot(twf, F["Dto"](ws, twf), color=STEEL, lw=1.8, zorder=3, **ws_style[j])[0]
        ax.plot(TWV, DTO[:, j], "o", ms=6.5, mfc="white", mec=STEEL, mew=1.6, ls="none", zorder=4)
        ax.text(1.106, DTO[2, j], f"{ws:.0f}", color=STEEL, fontsize=fs, ha="left", va="center")
        for i in range(3):
            close(float(np.interp(TWV[i], ln.get_xdata(), ln.get_ydata())), DTO[i, j], 1e-6, "line through run")
    xs = [x for x in G["on_ws"]["Dto"] if x is not None]
    dots = ax.plot(xs, [500] * len(xs), "o", color=VERM, mec=INK, mew=0.8, ms=10, ls="none", zorder=6)[0]
    for x, j in zip(dots.get_xdata(), [j for j, x in enumerate(G["on_ws"]["Dto"]) if x is not None]):
        close(float(F["Dto"](WSV[j], x)), 500, 1e-6, "takeoff crossing on a W/S line")
    assert tuple("none" if x is None else f"{x:.3f}" for x in G["on_ws"]["Dto"]) == PUB["on_lines"]["Dto"]
    ax.set_xlim(0.88, 1.16)
    ax.set_ylim(250, 1150)
    ax.set_xticks([0.9, 1.0, 1.1])
    ax.set_xlabel("$T_{SL}/W_{TO}$")
    ax.set_ylabel("Takeoff distance (ft)")
    thousands(ax)
    clean(ax)
    # one key for all four panels
    h = [Line2D([], [], **TW_STYLE[i]) for i in range(3)] + \
        [Line2D([], [], color=STEEL, lw=1.8, **ws_style[j]) for j in range(3)] + \
        [Line2D([], [], marker="o", color=GRAY, mec=INK, mew=0.8, ms=10, ls="none"), Patch(fc=BAND, ec="none")]
    lab = [f"$T_{{SL}}/W_{{TO}}$ = {t:.1f}" for t in TWV] + [f"$W_{{TO}}/S$ = {w:.0f} lb/ft²" for w in WSV] + \
          ["crossing (filled)", "fails"]
    fig.legend(h, lab, frameon=False, fontsize=fs, ncol=3, loc="lower center", bbox_to_anchor=(0.5, -0.01),
               handlelength=2.8, columnspacing=1.4)
    fig.tight_layout(rect=(0, 0.13, 1, 1), h_pad=1.6, w_pad=2.0)
    save(fig, "cross-plots")


def marked_sizing_plot():
    """Step 4: the crossings marked on the sizing plot, joined into constraint lines, ticked; marks a and b."""
    fig, ax = plt.subplots(figsize=(7.6, 5.6))
    curves = draw_curves(ax, "ws")
    tw_labels(ax, "ws", x_pad=0.6)
    drawn, dots = draw_constraints(ax, "w0", "ws", marks=True)
    check_curves(curves, "ws")
    check_lines_on_curves(ax, drawn, "w0", "ws")
    for k, xy, ha, va in (("Dto", (G["lines"]["Dto"][0][-1] + 0.3, fW(G["lines"]["Dto"][0][-1], 1.1) + 300), "left", "bottom"),
                          ("Ps", (52.8, fW(53.0, 0.9) - 250), "right", "top"),
                          ("Acc", (49.6, fW(50.0, G["on_ws"]["Acc"][0])), "right", "center")):
        ax.text(*xy, CON_NAME[k], color=TXT[CON_COLOR[k]], fontsize=FS + (1 if k == "Ps" else 0), ha=ha, va=va, zorder=8)
    a = (G["on_tw"]["Dto"][1], float(fW(G["on_tw"]["Dto"][1], 1.0)))
    b = (50.0, float(fW(50.0, G["on_ws"]["Dto"][0])))
    ring = ax.plot([a[0], b[0]], [a[1], b[1]], "o", ms=15, mfc="none", mec=INK, mew=1.4, ls="none", zorder=9)[0]
    ax.text(a[0] + 0.2, a[1] + 900, "a", fontsize=FS + 1.5, fontweight="bold", ha="center", va="bottom", zorder=9)
    ax.text(b[0] - 0.9, b[1], "b", fontsize=FS + 1.5, fontweight="bold", ha="right", va="center", zorder=9)
    # measured: a sits on the 1.0 curve at the table's W/S; b on the 50 line at the table's T/W and weight
    rx, ry = ring.get_xdata(), ring.get_ydata()
    assert f"{rx[0]:.1f}" == PUB["mark_a"]
    close(float(np.interp(rx[0], curves[1].get_xdata(), curves[1].get_ydata())), ry[0], 1.0, "a on the 1.0 curve")
    assert rx[1] == 50.0 and f"{round(ry[1], -2):,.0f}" == PUB["mark_b_w"]
    assert f"{G['on_ws']['Dto'][0]:.3f}" == PUB["mark_b_tw"]
    # b lies between the 0.9 and 1.0 runs, and a straight line between them misplaces it by more than 200 lb
    assert W0[0, 0] < ry[1] < W0[1, 0]
    assert abs(np.interp(G["on_ws"]["Dto"][0], TWV[:2], W0[:2, 0]) - ry[1]) > 200
    for k in CON:                                   # measured: four marks drawn per constraint
        assert len(dots[k].get_xdata()) == 4, k
    ws_axis(ax)
    constraint_legend(fig, feasible=False, ncol=2, loc="lower center", bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.12, 1, 1))
    save(fig, "marked-sizing-plot")


def lightest_feasible_point():
    """Step 5: the feasible region shaded and its lowest point."""
    fig, ax = plt.subplots(figsize=(7.6, 5.6))
    poly = draw_feasible(ax, "w0", "ws")
    curves = draw_curves(ax, "ws")
    tw_labels(ax, "ws", x_pad=0.6)
    drawn, _ = draw_constraints(ax, "w0", "ws")
    best = draw_best(ax, "w0", "ws")
    check_curves(curves, "ws")
    check_lines_on_curves(ax, drawn, "w0", "ws")
    for k, xy, ha, va in (("Dto", (G["lines"]["Dto"][0][-1] + 0.3, fW(G["lines"]["Dto"][0][-1], 1.1) + 300), "left", "bottom"),
                          ("Ps", (52.8, fW(53.0, 0.9) - 250), "right", "top"),
                          ("Acc", (49.6, fW(50.0, G["on_ws"]["Acc"][0])), "right", "center")):
        ax.text(*xy, CON_NAME[k], color=TXT[CON_COLOR[k]], fontsize=FS + (1 if k == "Ps" else 0), ha=ha, va=va, zorder=8)
    ws_b, tw_b, w_b = G["best"]
    text = (f"lightest feasible point:\n{round(w_b, -2):,.0f} lb at {ws_b:.0f} lb/ft²,"
            f"\n$T_{{SL}}/W_{{TO}}$ = {tw_b:.3f}")
    ax.annotate(text, xy=(ws_b + 0.35, w_b + 350), xytext=(63.0, 53300), fontsize=FS, ha="left", va="bottom", zorder=10,
                arrowprops=dict(arrowstyle="-|>", color=STEEL, lw=1.0, shrinkA=3, shrinkB=2))
    assert text.split(":\n")[1] == f"{PUB['w_best']} lb at {PUB['ws_best']} lb/ft²,\n$T_{{SL}}/W_{{TO}}$ = {PUB['tw_best']}"
    # measured: the diamond is the lowest point of the shaded region and lies on the takeoff line
    xy = poly.get_xy()
    close(xy[:, 1].min(), best.get_ydata()[0], 1.0, "diamond at the bottom of the region")
    x, y = drawn["Dto"].get_xdata(), drawn["Dto"].get_ydata()
    close(float(np.interp(best.get_xdata()[0], x, y)), best.get_ydata()[0], 2.0, "diamond on the takeoff line")
    # the region: from the left edge of the matrix (50) to the takeoff line on the 1.1 curve
    close(xy[:, 0].min(), 50.0, 1e-9, "region starts at the 50 line")
    close(xy[:, 0].max(), G["lines"]["Dto"][0][-1], 1e-9, "region ends where takeoff meets the 1.1 curve")
    ws_axis(ax)
    constraint_legend(fig, ncol=3, loc="lower center", bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.12, 1, 1))
    save(fig, "lightest-feasible-point")


def offset_curves():
    """Step 6: the T/W curves shifted 6 lb/ft2 per curve (left); the finished carpet plot, no horizontal axis (right)."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 5.2), gridspec_kw=dict(width_ratios=[1, 1]))
    fs = 12.5                                       # full column: 9 pt or more at 700 px
    dotted = {}
    for i in (1, 2):                                # before the shift, dotted
        dotted[i] = a1.plot(WSF, fW(WSF, TWV[i]), color=TW_STYLE[i]["color"], alpha=0.55, lw=1.3, ls=(0, (1, 2)),
                            zorder=2)[0]
    a1.text(50.6, 57900, "dotted: before the shift", color=GRAY, fontsize=fs, ha="left", va="center")
    curves = draw_curves(a1, "x", grid_lines=False)
    nodes = draw_nodes(a1, "x", size=6)
    check_curves(curves, "x")
    arrows = {}
    for i in (1, 2):
        y = W0[i, 1]
        d = float(xoff(60, TWV[i]) - 60)
        arrows[i] = a1.annotate("", xy=(60 + d - 0.5, y), xytext=(60, y),
                                arrowprops=dict(arrowstyle="-|>", color=STEEL, lw=1.0, shrinkA=0, shrinkB=0))
        arrows[i].label = a1.text(60 + d / 2, y + 650, f"+{d:.0f}", fontsize=fs, ha="center", va="bottom", zorder=6,
                                  bbox=dict(boxstyle="square,pad=0.08", fc="white", ec="none"))
    tw_labels(a1, "x", x_pad=0.9, long_hi=False, fs=fs)
    # measured: each shifted curve lies the printed offset per curve to the right of its dotted copy, and the
    # arrows and their labels show the same shift; the 0.9 curve stays at 50 to 70
    for i in (1, 2):
        sx, sy = curves[i].get_xdata(), curves[i].get_ydata()
        ux, uy = dotted[i].get_xdata(), dotted[i].get_ydata()
        assert np.array_equal(sy, uy)
        shift = sx - ux
        close(float(shift.max() - shift.min()), 0.0, 1e-9, "a rigid shift")
        assert f"{shift[0] / i:.0f}" == PUB["offset"], shift[0]
        (x1, _), (x0, _) = arrows[i].xy, arrows[i].xyann
        close(x1 + 0.5 - x0, float(shift[0]), 1e-9, "arrow length")
        assert arrows[i].label.get_text() == f"+{i * int(PUB['offset'])}"
    assert (curves[0].get_xdata()[0], curves[0].get_xdata()[-1]) == (50.0, 70.0)
    a1.set_xlim(43, 92)
    a1.set_ylim(33000, 58500)
    a1.set_xticks([50, 60, 70, 80])
    a1.set_xlabel("$W_{TO}/S$ + offset (lb/ft²)", fontsize=fs)
    a1.set_ylabel("$W_{TO}$ (lb)", fontsize=fs)
    thousands(a1)
    clean(a1)
    poly, curves2, drawn, dots, nodes2, best = _carpet(a2, fs=fs, marks=True)
    tw_labels(a2, "x", x_pad=0.9, long_hi=False, fs=fs)
    a2.set_xlim(36, 92)                             # room for the line labels left of the marks
    a2.set_ylim(33000, 58500)
    a2.set_ylabel("$W_{TO}$ (lb)", fontsize=fs)
    for ax in (a1, a2):
        ax.tick_params(labelsize=fs)
    # measured on the drawn marks of the right panel: four per constraint, each shifted to the abscissa
    # W/S + 60 (T/W - 0.9) of its crossing, and each on the constraint line drawn in the same panel
    for k in CON:
        m = G[f"marks_{k}"]
        x_drawn, y_drawn = dots[k].get_xdata(), dots[k].get_ydata()
        assert len(x_drawn) == 4, k
        close(float(np.max(np.abs(x_drawn - m[:, 0] - float(PUB["offset_slope"]) * (m[:, 1] - TWV[0])))),
              0.0, 1e-9, f"{k}: shift of the drawn marks")
        lx, ly = drawn[k].get_xdata(), drawn[k].get_ydata()
        for xm, ym in zip(x_drawn, y_drawn):
            assert np.min(np.hypot((lx - xm) / 20.0, (ly - ym) / 20000.0)) < 2e-3, (k, xm, ym)
    assert not a2.spines["bottom"].get_visible() and len(a2.get_xticks()) == 0
    constraint_legend(fig, ncol=3, fontsize=fs, loc="lower center", bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.12, 1, 1), w_pad=2.0)
    save(fig, "offset-curves")


# ------------------------------------------------------------- page 2 figure
def aspect_ratio_study():
    """Sizing plots at AR 4, 5, 6 and the lightest feasible W_TO against AR. Schematic: shapes only."""
    d = json.loads(AR_DATA.read_text())
    fig, axs = plt.subplots(2, 2, figsize=(9.6, 6.6))
    lows = {}
    for k, ax in zip("456", (axs[0, 0], axs[0, 1], axs[1, 0])):
        p = d["panels"][k]
        feas = np.array(p["feasible"])
        poly = Polygon(feas, closed=True, fc=DUST, ec="none", zorder=1)
        ax.add_patch(poly)
        for seg in p["matrix_edges"]:
            ax.plot(*np.array(seg).T, color=STEEL, lw=0.9, zorder=2)
        curves = {}
        for i, t in enumerate(("lo", "mid", "hi")):
            st = dict(TW_STYLE[i])
            st["lw"] = 1.8
            curves[t] = np.array(p[f"tw_{t}"])
            ax.plot(*curves[t].T, zorder=3, **st)
        cons = [np.array(c) for c in p["constraints"]]
        for c in cons:
            ax.plot(*c.T, color=INK, lw=2.0, zorder=4)
        for seg in p["ticks"]:
            ax.plot(*np.array(seg).T, color=INK, lw=0.8, zorder=4)
        ax.text(74.5, 60000, f"$AR$ = {k}", fontsize=12.5, ha="right", va="top")
        # measured: the shaded region lies between the 0.9 and 1.1 curves and above every constraint line
        lo = curves["lo"][np.argsort(curves["lo"][:, 0])]
        hi = curves["hi"][np.argsort(curves["hi"][:, 0])]
        assert np.all(feas[:, 1] >= np.interp(feas[:, 0], *lo.T) - 60), k
        assert np.all(feas[:, 1] <= np.interp(feas[:, 0], *hi.T) + 60), k
        for c in cons:
            cs = c[np.argsort(c[:, 0])]
            within = (feas[:, 0] > cs[0, 0]) & (feas[:, 0] < cs[-1, 0])
            assert np.all(feas[within, 1] >= np.interp(feas[within, 0], *cs.T) - 60), k
        # measured: the ticks hang below the constraint line they belong to (the failing side)
        def gap(c, q):                              # distance from a point to a polyline's vertices, scaled
            return float(np.hypot(c[:, 0] - q[0], (c[:, 1] - q[1]) / 1000).min())
        for i, c in enumerate(cons):                # each line: the ticks next to it, and no closer to another
            cs = c[np.argsort(c[:, 0])]
            below = n = 0
            for a, b in (np.array(s) for s in p["ticks"]):
                near = min(gap(c, a), gap(c, b))
                if near > 0.35 or min(min(gap(o, a), gap(o, b)) for j, o in enumerate(cons) if j != i) < near:
                    continue
                off = b if gap(c, a) < gap(c, b) else a       # the end away from the line
                if cs[0, 0] <= off[0] <= cs[-1, 0]:
                    n += 1
                    below += off[1] < np.interp(off[0], *cs.T)
            assert n >= 3 and below / n > 0.9, (k, i, below, n)
        lows[k] = feas[:, 1].min()
        ax.set_xlim(45, 75)
        ax.set_ylim(30000, 61000)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("$W_{TO}/S$")
        ax.set_ylabel("$W_{TO}$")
        clean(ax)
    ax = axs[1, 1]
    curve = np.array(d["lightest"]["curve"])
    marks = np.array(d["lightest"]["marks"])
    ax.plot(*curve.T, color=INK, lw=1.8, zorder=3)
    ax.plot(*marks.T, "x", color=VERM, ms=11, mew=2.4, ls="none", zorder=4)
    # measured: AR 5 is lightest and AR 6 heaviest, in the three sizing panels and in the marks
    assert lows["5"] < lows["4"] < lows["6"], lows
    assert marks[1, 1] < marks[0, 1] < marks[2, 1]
    coef = np.polyfit(marks[:, 0], marks[:, 1], 2)
    close(float(np.max(np.abs(np.polyval(coef, curve[:, 0]) - curve[:, 1]))), 0.0, 1.0, "the curve is the quadratic through the marks")
    ar_min = -coef[1] / (2 * coef[0])
    assert coef[0] > 0 and 4.5 < ar_min < 5.5, ar_min
    ax.set_xlim(3.5, 6.5)
    ax.set_ylim(43500, 49500)
    ax.set_xticks([4, 5, 6])
    ax.set_yticks([])
    ax.set_xlabel("$AR$")
    ax.set_ylabel("lightest feasible $W_{TO}$")
    clean(ax)
    h = [Line2D([], [], **dict(TW_STYLE[i], lw=1.8)) for i in range(3)] + \
        [Line2D([], [], color=INK, lw=2.0), Patch(fc=DUST, ec="none"),
         Line2D([], [], marker="x", color=VERM, mew=2.4, ms=10, ls="none")]
    lab = [f"$T_{{SL}}/W_{{TO}}$ = {t:.1f}" for t in TWV] + \
          ["constraint line, ticks on the failing side", "feasible", "lightest feasible $W_{TO}$"]
    hmap = {h[3]: _TickedLine()}
    fig.legend(h, lab, handler_map=hmap, frameon=False, fontsize=12, ncol=3, loc="lower center",
               bbox_to_anchor=(0.5, -0.01), handlelength=2.6, columnspacing=1.3)
    fig.tight_layout(rect=(0, 0.11, 1, 1), h_pad=1.5, w_pad=2.0)
    save(fig, "aspect-ratio-study")


ALL = [question_constraint_axes, carpet_plot, sizing_plot, cross_plots, marked_sizing_plot, lightest_feasible_point,
       offset_curves, aspect_ratio_study]

if __name__ == "__main__":
    for fn in ALL:
        fn()
