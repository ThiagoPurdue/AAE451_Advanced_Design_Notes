"""The illustrative figures of the Navy Jet Trainer brief A09, redrawn as SVG from the
brief's own script (Assignments/A09/scripts/make_a09_figures.py): the carpet plot and the
ranked sensitivity bars. Same invented data on invented scales, generic labels
("Constraint A", "Input A"). Each figure asserts its point before it is written, as the
brief script does. The STOL carpet of the brief script is not part of the book.

The carpet samples are computed, not drawn by hand: an invented smooth takeoff weight
W(u, v) over the two design variables (u = wing loading, v = thrust-to-weight ratio, both
scaled so that the matrix runs from -1 to +1), invented constraint functions g(u, v) >= 0
on the passing side, the nine runs at the matrix nodes, the constraint lines g = 0 and
the feasible region all mapped through the same carpet transformation (abscissa =
u + offset * v, ordinate = W). The lightest feasible point is solved for, then checked
against the shaded region.

Every text is set at 13 pt, at the SVG's natural size. The assert in save() checks the font
size set for each text (>= 11 pt), not the drawn size: mathtext subscripts are drawn at about
70% of it, and the page scales the SVG to its column width. (The brief's script checks
>= 11 pt at its printed width on the PNG; the SVG has no printed width.)

The SVG output is reproducible: a fixed svg.hashsalt for the clip and hatch ids, and no date
in the metadata, so a rerun writes identical files.

Run from the book folder:  python3 scripts/make_a09_figures.py
"""
from pathlib import Path

import contourpy
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.text as mtext
from matplotlib.patches import Patch

OUT = Path(__file__).resolve().parents[1] / "notes" / "assignments" / "figures"
BLACK, ORANGE, SKY, GREEN, BLUE, VERM, PURPLE = (
    "#000000", "#E69F00", "#56B4E9", "#009E73", "#0072B2", "#D55E00", "#CC79A7")
GREY, FILL = "#6e6e6e", "#EBD9A6"      # grey 5.1:1 on white, blue 5.2:1: labels pass
FS = 13                                # every text of both figures, >= 11 pt
plt.rcParams.update({"svg.fonttype": "none", "font.family": "sans-serif",
                     "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
                     "font.size": FS, "legend.fontsize": FS, "axes.labelsize": FS,
                     "xtick.labelsize": FS, "ytick.labelsize": FS,
                     "savefig.facecolor": "white",
                     "svg.hashsalt": "a09"})     # fixed ids: reruns write identical SVGs

# line styles: grid curves and constraint lines each have their own
CURVE_STYLE = {"low": (BLUE, (0, (1.2, 1.6)), 1.8),
               "center": (BLUE, "-", 1.4),
               "high": (BLACK, (0, (5, 1.6, 1.2, 1.6)), 1.4)}
CONSTRAINT_STYLE = {"A": (VERM, "-"), "B": (GREEN, (0, (6, 2.2))),
                    "C": (PURPLE, (0, (6, 1.6, 1.4, 1.6, 1.4, 1.6)))}
LEVELS = ("low", "center", "high")
NODES = (-1.0, 0.0, 1.0)


def save(fig, name):
    # the font size set for each text, not the drawn size of mathtext subscripts
    sizes = [t.get_fontsize() for t in fig.findobj(mtext.Text)
             if t.get_visible() and t.get_text().strip()]
    assert min(sizes) >= 11, (f"{name}: font size set below 11 pt "
                              "(set size checked, not the drawn size of subscripts)")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight", pad_inches=0.1,
                metadata={"Date": None})
    plt.close(fig)
    print("wrote", name)


def grad(f, u, v, h=1e-6):
    return np.array([f(u + h, v) - f(u - h, v), f(u, v + h) - f(u, v - h)]) / (2 * h)


def lightest_point(cons, active):
    """The crossing of the two active constraint lines, g_i = g_j = 0 (Newton, numerical
    Jacobian). a09_carpet then checks that it is the lowest feasible point."""
    x = np.array([0.0, 0.0])
    f = lambda p: np.array([cons[active[0]](*p), cons[active[1]](*p)])
    for _ in range(50):
        J = np.empty((2, 2))
        for k in range(2):
            d = np.zeros(2)
            d[k] = 1e-7
            J[:, k] = (f(x + d) - f(x - d)) / 2e-7
        x = x - np.linalg.solve(J, f(x))
    assert np.abs(f(x)).max() < 1e-10
    return x


# --------------------------------------------------------------- A09 Navy carpet plot
def a09_carpet():
    """v = thrust-to-weight ratio: W rises with it and falls with wing loading.
    Constraints A and B are active; C bounds the region at high wing loading."""
    W = lambda u, v: 1.0 - 0.10 * u + 0.22 * v + 0.035 * u ** 2 + 0.03 * v ** 2 - 0.02 * u * v
    cons = {"A": lambda u, v: 0.35 - 0.75 * u + 0.70 * v - 0.08 * u ** 2,
            "B": lambda u, v: v + 0.30 + 0.25 * u,
            "C": lambda u, v: 0.60 - u + 0.15 * v}
    active, offset, toward = ("A", "B"), 0.6, +1
    curve_sym = r"$T_{SL}/W_{TO}$"
    curve_order = {-1.0: "low", 0.0: "center", 1.0: "high"}
    labels = {"xlim": (-2.6, 1.66), "ylim": (0.645, 1.47),
              "curve": {"low": (8, 4), "center": (8, 0), "high": (8, 0)},
              "line": {"low": (-1, 12, -9, "right", "top"),
                       "center": (-1, 12, -9, "right", "top"),
                       "high": (-1, 0, -9, "center", "top")},
              "cons": {"A": (1.47, 1.07, "left"), "B": (0.73, 0.83, "left"),
                       "C": (1.58, 1.117, "left", 0.75)},
              "feasible": (-0.25, 1.2),
              "diamond": ((-1.55, 1.30), "center"),
              "run": ((-1.1, 1.43), "right", (-1, 1))}

    X = lambda u, v: u + offset * v
    n = 401
    s = np.linspace(-1, 1, n)
    U, V = np.meshgrid(s, s)
    WW, XX = W(U, V), X(U, V)
    G = {k: g(U, V) for k, g in cons.items()}
    GMIN = np.minimum.reduce(list(G.values()))

    # the grid is open: no two curves overlap in the carpet coordinates
    for v1, v2 in zip(NODES[:-1], NODES[1:]):
        lo, hi = (v1, v2) if W(0, v2) > W(0, v1) else (v2, v1)
        xs = np.linspace(-3, 3, 600)
        u_lo, u_hi = xs - offset * lo, xs - offset * hi
        both = (abs(u_lo) <= 1) & (abs(u_hi) <= 1)
        assert np.all(W(u_hi[both], hi) > W(u_lo[both], lo)), "curves overlap"

    # the lightest feasible point
    pu, pv = lightest_point(cons, active)
    w_star = W(pu, pv)
    feas = GMIN >= 0
    w_region = WW[feas].min()
    assert all(g(pu, pv) > -1e-9 for g in cons.values()), "diamond is not feasible"
    assert abs(pu) < 1 and abs(pv) < 1, "diamond is on the edge of the matrix"
    assert w_star <= w_region + 1e-9, "a shaded point lies below the diamond"
    assert w_region - w_star < 2e-3, "the diamond is not the lowest point of the region"
    assert all(abs(cons[k](pu, pv)) < 1e-9 for k in active), "diamond is not on the lines"
    runs = [(a, b) for a in NODES for b in NODES]
    gap = min(np.hypot(pu - a, pv - b) for a, b in runs)
    assert gap > 0.25, "the diamond sits on a run"
    # the region lies toward the stated side of the second variable
    assert np.sign(V[feas].mean()) == toward, "feasible region on the wrong side"
    # every constraint line crosses the matrix and bounds the region somewhere
    for k, g in G.items():
        assert g.min() < 0 < g.max(), f"Constraint {k} does not cross the matrix"
        on_edge = feas & (abs(g) < 4e-3) & (abs(GMIN - g) < 1e-12)
        assert on_edge.any(), f"Constraint {k} does not bound the feasible region"

    fig = plt.figure(figsize=(5.4, 4.3))
    ax = fig.add_axes([0.11, 0.04, 0.64, 0.92])
    ax.set_xlim(*labels["xlim"])
    ax.set_ylim(*labels["ylim"])

    ax.contourf(XX, WW, GMIN, levels=[0, 10], colors=[FILL], zorder=0)
    # lines of constant wing loading
    for u in NODES:
        vv = np.linspace(-1, 1, 100)
        ax.plot(X(u, vv), W(u, vv), color=GREY, lw=1.0, zorder=2)
    # curves of constant T/W
    for v in NODES:
        col, ls, lw = CURVE_STYLE[curve_order[v]]
        uu = np.linspace(-1, 1, 200)
        ax.plot(X(uu, v), W(uu, v), color=col, ls=ls, lw=lw, zorder=3)
    # constraint lines, from the zero contour of g on the (u, v) mesh
    fig.canvas.draw()
    to_disp, to_data = ax.transData, ax.transData.inverted()
    pt = fig.dpi / 72.0
    for k, g in cons.items():
        col, ls = CONSTRAINT_STYLE[k]
        for seg in contourpy.contour_generator(U, V, G[k]).lines(0):
            cu, cv = seg[:, 0], seg[:, 1]
            ax.plot(X(cu, cv), W(cu, cv), color=col, ls=ls, lw=2.4, zorder=4,
                    solid_capstyle="butt", dash_capstyle="butt")
            # ticks on the failing side, every 8 pt along the line, 5 pt long
            d = to_disp.transform(np.column_stack([X(cu, cv), W(cu, cv)]))
            arc = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(d, axis=0).T))])
            for a in np.arange(4 * pt, arc[-1] - 2 * pt, 8 * pt):
                u0, v0 = np.interp(a, arc, cu), np.interp(a, arc, cv)
                n_g = grad(g, u0, v0)
                u1, v1 = np.array([u0, v0]) - 1e-3 * n_g / np.linalg.norm(n_g)
                assert g(u1, v1) < 0, "tick on the passing side"
                p0 = to_disp.transform([X(u0, v0), W(u0, v0)])
                p1 = to_disp.transform([X(u1, v1), W(u1, v1)])
                t = (p1 - p0) / np.linalg.norm(p1 - p0)
                q = to_data.transform([p0, p0 + 5 * pt * t])
                ax.plot(q[:, 0], q[:, 1], color=col, lw=1.3, zorder=4, solid_capstyle="butt")
    # runs and the lightest feasible point
    for a, b in runs:
        ax.plot(X(a, b), W(a, b), "o", ms=6.5, mfc="white", mec=BLACK, mew=1.3, zorder=6)
    ax.plot(X(pu, pv), w_star, "D", ms=10, color=BLACK, zorder=7)

    # direct labels: blue (5.2:1) and grey (5.1:1) on white pass 4.5:1
    for v in NODES:
        word = curve_order[v]
        dx, dy = labels["curve"][word]
        ax.annotate(f"{curve_sym} {word}", (X(1, v), W(1, v)), xytext=(dx, dy),
                    textcoords="offset points", color=CURVE_STYLE[word][0],
                    ha="left", va="center")
    for u, word in zip(NODES, LEVELS):
        end, dx, dy, ha, va = labels["line"][word]
        ax.annotate(rf"$W_{{TO}}/S$ {word}", (X(u, end), W(u, end)), xytext=(dx, dy),
                    textcoords="offset points", color=GREY, ha=ha, va=va)
    for k, g in cons.items():
        x, y, ha, *leader = labels["cons"][k]
        # black text: the line colors are below 4.5:1 on white; the label sits at the
        # line's end and the line has its own style
        if not leader:
            ax.text(x, y, f"Constraint {k}", ha=ha, va="center", fontweight="bold")
            continue
        # a line whose end is not clear of the grid: the label sits on its failing side
        # with a short leader to the point of the line at v = leader[0]
        lv = leader[0]
        a, b = -1.0, 1.0
        assert g(a, lv) * g(b, lv) < 0, f"Constraint {k} leader point is off the matrix"
        for _ in range(60):
            m = 0.5 * (a + b)
            a, b = (m, b) if g(a, lv) * g(m, lv) > 0 else (a, m)
        lu = 0.5 * (a + b)
        assert g(lu + 0.05, lv) < 0, f"Constraint {k} label is not on the failing side"
        ax.annotate(f"Constraint {k}", (X(lu, lv), W(lu, lv)), xytext=(x, y), ha=ha,
                    va="center", fontweight="bold",
                    arrowprops=dict(arrowstyle="-", color=BLACK, lw=1.0, shrinkA=3,
                                    shrinkB=0), zorder=8)
    fx, fy = labels["feasible"]
    ax.text(fx, fy, "feasible", ha="center", va="center")
    arrow = dict(arrowstyle="-|>", mutation_scale=11, color=BLACK, lw=1.0, shrinkA=2)
    (tx, ty), ha = labels["diamond"]
    ax.annotate("lightest\nfeasible point", (X(pu, pv), w_star), xytext=(tx, ty),
                ha=ha, va="center", arrowprops=dict(arrow, shrinkB=8, relpos=(0.7, 0)),
                zorder=8)
    (rx, ry), ha, (ru, rv) = labels["run"]
    ax.annotate("one run", (X(ru, rv), W(ru, rv)), xytext=(rx, ry), ha=ha, va="center",
                arrowprops=dict(arrow, shrinkB=6), zorder=8)

    # no horizontal axis; the vertical axis has no numbers
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)
    ax.set_ylabel(r"$W_{TO}$ (invented scale)")
    ax.plot(0, 1, "^k", ms=6, transform=ax.transAxes, clip_on=False)
    save(fig, "a09-carpet")


# ----------------------------------------------------------- A09 sensitivity ranking
def a09_sensitivity():
    """Invented sensitivities, named so that the ranked order is not the name order."""
    s = {"Input A": 0.45, "Input B": -1.10, "Input C": 1.40,
         "Input D": 0.15, "Input E": -0.60, "Input F": 0.30}
    ranked = sorted(s, key=lambda k: abs(s[k]), reverse=True)
    mags = [abs(s[k]) for k in ranked]
    assert all(a > b for a, b in zip(mags[:-1], mags[1:])), "ranking has ties"
    assert ranked != sorted(s), "ranked order equals name order; the sort shows nothing"
    fig, ax = plt.subplots(figsize=(5.0, 3.5))
    y = np.arange(len(ranked))[::-1]              # largest on top
    for yi, k in zip(y, ranked):
        pos = s[k] > 0
        ax.barh(yi, s[k], height=0.62, color=BLUE if pos else ORANGE,
                hatch="///" if pos else "...", edgecolor=BLACK, lw=0.8)
    ax.axvline(0, color=BLACK, lw=1.6)
    ax.set_yticks(y, ranked)
    ax.set_xticks([])                            # no numbers: the zero line is the mark
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-0.6, len(ranked) - 0.4)
    ax.set_xlabel(r"$s_x$ (invented scale)")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(handles=[Patch(facecolor=BLUE, edgecolor=BLACK, hatch="///", label="positive"),
                       Patch(facecolor=ORANGE, edgecolor=BLACK, hatch="...", label="negative")],
              loc="lower left", frameon=False, handlelength=1.6)
    # the bars are drawn in the ranked order, largest |s_x| at the top (the figure's point)
    bars = sorted(ax.patches[:len(ranked)], key=lambda p: -p.get_y())
    assert [abs(p.get_width()) for p in bars] == mags
    shown = [t.get_text() for t in
             sorted(ax.get_yticklabels(), key=lambda t: -t.get_position()[1])]
    assert shown == ranked, "labels not in ranked order"
    save(fig, "a09-sensitivity")


if __name__ == "__main__":
    a09_carpet()
    a09_sensitivity()
