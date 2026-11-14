"""Figures for Lecture 9, Constraint Analysis and the Design Point.

The lecture slides draw every figure natively, so each one here is drawn from
the same definition: the schematic diagrams use the slides' invented curves and
say "invented scale" on their axes; the energy-height chart is computed; the
Cessna 162 diagram recomputes Gudmundsson (2022), Example 3-1, and the T-45C
diagram recomputes the lecture's worked example. Both worked examples assert
the published or lecture values before anything is drawn. Run from the book
folder:

    python3 scripts/make_constraint_figures.py

Set FIG_PREVIEW=<folder> to also write PNG copies for checking.
"""
import os
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyBboxPatch

OUT = Path(__file__).resolve().parents[1] / "notes" / "lecture-09" / "figures"
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
GOLD, DUST, LIGHT, AGED = "#CFB991", "#EBD99F", "#F5EFDC", "#8E6F3E"
BLUE, VERM, GREEN, SKY, PURPLE = "#0072B2", "#D55E00", "#009E73", "#56B4E9", "#AA4499"
WS_INV = "Wing loading $W_{TO}/S$ (invented scale)"
TW_INV = "Thrust-to-weight ratio $T_{SL}/W_{TO}$ (invented scale)"


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight", pad_inches=0.1)
    if PREVIEW:
        fig.savefig(Path(PREVIEW) / f"{name}.png", dpi=110, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)
    print("wrote", name)


def clean(ax, grid=True):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if grid:
        ax.grid(True, color="#DDDDDD", lw=0.6)


def invented_axes(ax, ymax=1.0):
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, ymax)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel(WS_INV)
    ax.set_ylabel(TW_INV)
    clean(ax, grid=False)


# ------------------------------------------------------------ part 1, the method
def design_space():
    """After Mattingly et al. Fig. 2.1: two requirements bound the region."""
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    x = np.linspace(0.12, 1.0, 200)
    a = 0.06 / x + 0.30 * x
    inside = x <= 0.74
    ax.fill_between(x[inside], a[inside], 1.0, color=DUST, lw=0)
    ax.plot(x, a, color=INK, lw=2.2)
    ax.plot([0.74, 0.74], [0, 1.0], color=BLUE, lw=2.2, ls="--")
    ax.text(0.985, 0.40, "requirement A", ha="right", va="bottom", fontsize=11)
    ax.text(0.755, 0.94, "requirement B", ha="left", va="center", fontsize=11)
    ax.text(0.40, 0.80, "feasible region", ha="center", va="center", fontsize=12, fontweight="bold")
    ax.text(0.45, 0.12, "A not met", ha="center", va="center", fontsize=11, color=STEEL)
    ax.text(0.88, 0.62, "B not met", ha="center", va="center", fontsize=11, color=STEEL)
    ax.plot([0.58], [0.52], "D", color=VERM, ms=8)
    ax.text(0.555, 0.52, "design point", ha="right", va="center", fontsize=11)
    invented_axes(ax)
    fig.tight_layout()
    save(fig, "design-space")


def energy_height():
    """Lines of constant energy height, h = z_e - V^2/2g. After Mattingly et al. Fig. 2.5."""
    g = 32.17
    assert abs((20000 + 1134 ** 2 / (2 * g)) - 39987) < 10      # the marked state lies near z_e = 40,000 ft
    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    v = np.linspace(0, 1500, 300)
    for ze in (10000, 20000, 30000, 40000, 50000):
        h = ze - v ** 2 / (2 * g)
        ax.plot(v[h >= 0], h[h >= 0], color=GRAY, lw=1.2)
        ax.text(150, ze - 150 ** 2 / (2 * g) + 700, f"$z_e$ = {ze:,} ft", fontsize=10, color=STEEL, rotation=-4)
    p = (1134, 20000)
    ax.plot(*p, "o", color=INK, ms=7, zorder=5)
    kw = dict(arrowstyle="-|>", lw=1.8)
    ax.annotate("", xy=(1134, 31000), xytext=p, arrowprops=dict(color=BLUE, **kw))
    ax.annotate("", xy=(1400, 20000), xytext=p, arrowprops=dict(color=BLUE, **kw))
    ax.annotate("", xy=(700, 32385), xytext=p, arrowprops=dict(color=VERM, ls="--", **kw))
    ax.text(1150, 24000, "climb", fontsize=10.5, va="center")
    ax.text(1270, 18300, "accelerate", fontsize=10.5, ha="center", va="center")
    ax.annotate("trade speed for altitude,\n$P_s$ = 0", xy=(917, 26200), xytext=(1090, 43500), fontsize=10.5,
                ha="center", va="center", arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8, shrinkB=3))
    ax.set_xlabel("True airspeed $V$ (ft/s)")
    ax.set_ylabel("Altitude $h$ (ft)")
    ax.set_xlim(0, 1500)
    ax.set_ylim(0, 52000)
    ax.set_yticks(range(0, 50001, 10000))
    ax.set_yticklabels([f"{t:,}" for t in range(0, 50001, 10000)])
    clean(ax)
    fig.tight_layout()
    save(fig, "energy-height")


def path_forces():
    """Forces on an aircraft climbing along a path inclined by gamma."""
    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    ax.set_aspect("equal")
    ax.axis("off")
    gam = np.radians(20)
    c, s = np.cos(gam), np.sin(gam)

    def rot(pts):
        return [(x * c - y * s, x * s + y * c) for x, y in pts]

    ax.plot([-3.2, 3.6], [0, 0], color=GRAY, lw=1.0, ls="--")
    ax.plot([-3.0 * c, 3.6 * c], [-3.0 * s, 3.6 * s], color=GRAY, lw=1.0, ls="--")
    ang = np.linspace(0, gam, 20)
    ax.plot(1.9 * np.cos(ang), 1.9 * np.sin(ang), color=STEEL, lw=1.0)
    ax.text(2.25, 0.38, r"$\gamma$", fontsize=13, ha="center", va="center")
    ax.text(3.65, -0.05, "horizontal", fontsize=10, va="top", ha="right", color=STEEL)
    ax.text(3.6 * c + 0.05, 3.6 * s, "flight path", fontsize=10, va="center", color=STEEL)
    # the trainer side view of Lecture 10, mirrored to fly to the right, CG at the origin, pitched up by gamma
    import make_stability_figures as msf
    from matplotlib.transforms import Affine2D
    n_p, n_l = len(ax.patches), len(ax.lines)
    msf._side_view(ax, z=2.2)
    tr = Affine2D().translate(-5.0, 0.0).scale(-0.30, 0.30).rotate(gam) + ax.transData
    for art in ax.patches[n_p:] + ax.lines[n_l:]:
        art.set_transform(tr)
    kw = dict(arrowstyle="-|>", lw=2.0)

    def force(vec, label, color, off):
        (x, y), = rot([vec])
        ax.annotate("", xy=(x, y), xytext=(0, 0), arrowprops=dict(color=color, **kw))
        ax.text(x + off[0], y + off[1], label, fontsize=13, ha="center", va="center")

    force((2.6, 0), "$T$", BLUE, (0.05, 0.28))
    force((-1.9, 0), "$D$", VERM, (-0.1, 0.3))
    force((0, 2.0), "$L$", INK, (-0.05, 0.25))
    w = 2.2
    ax.annotate("", xy=(0, -w), xytext=(0, 0), arrowprops=dict(color=INK, **kw))
    ax.text(-0.28, -w + 0.1, "$W$", fontsize=13, ha="center", va="center")
    corner = (w * c * s, -w * c * c)                    # W cos(gamma) normal to the path, then W sin(gamma) along it
    ax.plot([0, corner[0], 0], [0, corner[1], -w], color=STEEL, lw=1.2, ls=":")
    ax.text(corner[0] / 2 + 0.2, corner[1] / 2, r"$W\cos\gamma$", fontsize=11.5, ha="left", va="center")
    ax.text(corner[0] / 2 + 0.15, (corner[1] - w) / 2 - 0.22, r"$W\sin\gamma$", fontsize=11.5, ha="left", va="top")
    (vx0, vy0), (vx1, vy1) = rot([(1.2, 0.8), (2.3, 0.8)])
    ax.annotate("", xy=(vx1, vy1), xytext=(vx0, vy0), arrowprops=dict(arrowstyle="->", color=STEEL, lw=1.2, ls="--"))
    ax.text(vx1 + 0.2, vy1 + 0.1, "$V$", fontsize=12, ha="center", va="center")
    ax.set_xlim(-3.4, 4.6)
    ax.set_ylim(-2.8, 2.6)
    save(fig, "path-forces")


def equation_flow():
    """One condition in, one boundary out."""
    fig, ax = plt.subplots(figsize=(8.6, 3.5))
    ax.axis("off")
    inputs = [("engine deck", r"$\alpha$"), ("mission weight", r"$\beta$"),
              ("RFP condition", "$q$, $n$, $P_s$, $V$"), ("drag polar", "$K_1$, $K_2$, $C_{D_0}$, $C_{D_R}$")]
    for i, (name, sym) in enumerate(inputs):
        y = 3.3 - i * 1.0
        ax.add_patch(FancyBboxPatch((0.1, y - 0.36), 3.2, 0.72, boxstyle="round,pad=0.02,rounding_size=0.08",
                                    fc=LIGHT, ec=STEEL, lw=1.0))
        ax.text(1.7, y + 0.14, name, ha="center", va="center", fontsize=10.5)
        ax.text(1.7, y - 0.17, sym, ha="center", va="center", fontsize=10.5)
        ax.annotate("", xy=(4.2, y), xytext=(3.35, y), arrowprops=dict(arrowstyle="-|>", color=STEEL, lw=1.2))
    ax.add_patch(FancyBboxPatch((4.25, -0.06), 2.5, 3.72, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=DUST, ec=INK, lw=1.2))
    ax.text(5.5, 1.8, "master equation\n\n$T_{SL}/W_{TO}$\nat each $W_{TO}/S$", ha="center", va="center", fontsize=11)
    ax.annotate("", xy=(7.75, 1.8), xytext=(6.8, 1.8), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4))
    x = np.linspace(0.18, 1.0, 60)
    ax.plot([7.9, 7.9, 10.3], [3.3, 0.5, 0.5], color=INK, lw=1.0)
    ax.plot(7.9 + 2.3 * x, 0.5 + 2.6 * (0.09 / x + 0.45 * x), color=BLUE, lw=2.0)
    ax.text(9.1, 0.18, "$W_{TO}/S$", ha="center", va="center", fontsize=10.5)
    ax.text(9.1, 3.55, "one boundary", ha="center", va="center", fontsize=10.5)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(-0.2, 3.9)
    save(fig, "equation-flow")


def diagram_shape():
    """The shape each kind of boundary takes; invented values."""
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    x = np.linspace(0.1, 1.0, 300)
    cruise, turn, takeoff = 0.06 / x + 0.22 * x, 0.06 / x + 0.55 * x, 0.9 * x
    upper = np.maximum.reduce([cruise, turn, takeoff, np.full_like(x, 0.32)])
    inside = (x >= 0.15) & (x <= 0.72)
    ax.fill_between(x[inside], upper[inside], 1.0, color=DUST, lw=0)
    ax.plot(x, cruise, color=INK, lw=2.0)
    ax.plot(x, turn, color=VERM, lw=2.0, ls="--")
    ax.plot(x, takeoff, color=BLUE, lw=2.0, ls="-.")
    ax.plot(x, np.full_like(x, 0.32), color=STEEL, lw=1.8, ls=":")
    ax.plot([0.72, 0.72], [0, 1.0], color=GREEN, lw=2.0)
    ax.plot([0.85, 0.85], [0, 1.0], color=PURPLE, lw=2.0, ls="--")
    for y, name in ((0.275, "cruise"), (0.61, "turn"), (0.905, "takeoff"), (0.36, "climb gradient")):
        ax.text(1.01, y, name, fontsize=11, va="center", clip_on=False)
    ax.text(0.70, 0.06, "landing", fontsize=11, rotation=90, ha="right", va="bottom")
    ax.text(0.83, 0.06, "stall", fontsize=11, rotation=90, ha="right", va="bottom")
    ax.text(0.42, 0.82, "feasible region", fontsize=12, fontweight="bold", ha="center", va="center")
    invented_axes(ax)
    fig.tight_layout()
    save(fig, "diagram-shape")


# ------------------------------------------------- part 2, the trainer boundaries
def fighter_diagram():
    """A fighter constraint diagram with eight boundaries; invented values, shapes only."""
    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    x = np.linspace(0.1, 1.0, 300)
    turn, accel, takeoff = 0.05 / x + 0.70 * x, 0.09 / x + 0.30 * x, 0.85 * x
    upper = np.maximum.reduce([turn, accel, takeoff])
    inside = (x >= 0.12) & (x <= 0.75)
    ax.fill_between(x[inside], upper[inside], 1.2, color=DUST, lw=0)
    lines = [
        ("maximum speed", 0.04 / x + 0.15 * x, INK, "-"),
        ("dash", 0.05 / x + 0.30 * x, INK, "--"),
        ("turn", turn, VERM, "-"),
        ("acceleration", accel, VERM, "--"),
        ("ceiling", 0.03 / x + 0.12 * x, STEEL, "-."),
        ("one-engine climb", np.full_like(x, 0.22), STEEL, ":"),
        ("takeoff", takeoff, BLUE, "-"),
    ]
    for name, y, color, ls in lines:
        ax.plot(x, y, color=color, lw=1.9, ls=ls, label=name)
    ax.plot([0.75, 0.75], [0, 1.2], color=BLUE, lw=1.9, ls="--", label="landing")
    ax.plot([0.40, 0.50, 0.58], [0.62, 0.72, 0.84], "o", color=INK, mfc="white", ms=7, mew=1.6, label="cohort aircraft")
    ax.text(0.30, 1.07, "feasible region", fontsize=12, fontweight="bold", ha="center", va="center")
    invented_axes(ax, ymax=1.2)
    ax.legend(frameon=False, fontsize=10.5, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.12))
    fig.tight_layout()
    save(fig, "fighter-diagram")


def design_point():
    """After Mattingly et al. Fig. 2.E3: the design point and its margins; invented values."""
    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    x = np.linspace(0.1, 1.0, 300)
    turn, accel, takeoff = 0.07 / x + 0.75 * x, 0.08 / x + 0.35 * x, 0.95 * x
    upper = np.maximum.reduce([turn, accel, takeoff])
    inside = (x >= 0.12) & (x <= 0.74)
    ax.fill_between(x[inside], upper[inside], 1.2, color=DUST, lw=0)
    ax.plot(x, 0.04 / x + 0.20 * x, color=INK, lw=1.9)
    ax.plot(x, accel, color=VERM, lw=1.9, ls="--")
    ax.plot(x, turn, color=VERM, lw=1.9)
    ax.plot(x, takeoff, color=BLUE, lw=1.9, ls="-.")
    ax.plot([0.74, 0.74], [0, 1.2], color=GREEN, lw=1.9)
    for y, name in ((0.24, "maximum speed"), (0.43, "acceleration"), (0.80, "turn"), (0.97, "takeoff")):
        ax.text(1.01, y, name, fontsize=11, va="center", clip_on=False)
    ax.text(0.72, 0.05, "landing", fontsize=11, rotation=90, ha="right", va="bottom")
    ax.text(0.30, 1.10, "feasible region", fontsize=12, fontweight="bold", ha="center", va="center")
    dp = (0.50, 0.88)
    below = float(np.interp(dp[0], x, upper))
    assert dp[1] > below and dp[0] < 0.74                   # the point is inside the region
    kw = dict(arrowstyle="<->", color=STEEL, lw=1.3)
    ax.annotate("", xy=(dp[0], below), xytext=dp, arrowprops=kw)
    ax.annotate("", xy=(0.74, dp[1]), xytext=dp, arrowprops=kw)
    ax.plot(*dp, "D", color=VERM, ms=8, zorder=5)
    ax.text(dp[0] - 0.02, dp[1] + 0.035, "design point", fontsize=11, ha="right", va="bottom")
    ax.text(dp[0] - 0.015, (dp[1] + below) / 2, "margin", fontsize=10.5, ha="right", va="center", color=STEEL)
    ax.text((dp[0] + 0.74) / 2, dp[1] + 0.03, "margin", fontsize=10.5, ha="center", va="bottom", color=STEEL)
    invented_axes(ax, ymax=1.2)
    fig.tight_layout()
    save(fig, "design-point")


# ---------------------------------------------------- part 3, the worked examples
RHO_SL, G, KT = 0.002378, 32.174, 1.688
C162 = dict(W0=1320.0, k=0.04909, CDmin=0.0333, CLmaxTO=1.756, mu=0.04, CLTO=0.5, CDTO=0.038, sG=640.0,
            VV=880 / 60.0, rho8=0.001869, V3=108 * KT, n=1.155, sig17=0.6292,
            eta_to=0.60, eta_cl=0.65, eta_cr=0.75, ws_land=11.37)   # 0.60 at V_LOF, 0.65 climb and ceiling, 0.75 cruise


def gagg_ferrar(sigma):
    return 1.132 * sigma - 0.132


def c162_constraints(ws):
    """T/W and sea-level power (hp) of each Cessna 162 boundary: Gudmundsson (2022), Example 3-1."""
    c = C162
    sig8 = c["rho8"] / RHO_SL
    q3 = 0.5 * c["rho8"] * c["V3"] ** 2
    tw_to = 1.21 / (G * RHO_SL * c["CLmaxTO"]) * ws / c["sG"] + 0.605 / c["CLmaxTO"] * (c["CDTO"] - c["mu"] * c["CLTO"]) + c["mu"]
    vy = (43.591 + 2.2452 * ws) * KT
    q2 = 0.5 * RHO_SL * vy ** 2
    tw_cl = c["VV"] / vy + q2 * c["CDmin"] / ws + c["k"] * ws / q2
    tw_turn = q3 * (c["CDmin"] / ws + c["k"] * (c["n"] / q3) ** 2 * ws)
    tw_cr = q3 * c["CDmin"] / ws + c["k"] * ws / q3
    vyt = vy / np.sqrt(c["sig17"])
    tw_ce = 1.667 / vyt + q2 * c["CDmin"] / ws + c["k"] * ws / q2
    vlof = 1.1 * np.sqrt(2 * ws / (RHO_SL * c["CLmaxTO"]))
    hp = lambda tw, v, eta, sigma=1.0: tw * c["W0"] * v / (eta * 550) / (gagg_ferrar(sigma) if sigma < 1 else 1.0)
    tw = dict(takeoff=tw_to, climb=tw_cl, turn=tw_turn, cruise=tw_cr, ceiling=tw_ce)
    p = dict(takeoff=hp(tw_to, vlof, c["eta_to"]), climb=hp(tw_cl, vy, c["eta_cl"]),
             turn=hp(tw_turn, c["V3"], c["eta_cr"], sig8), cruise=hp(tw_cr, c["V3"], c["eta_cr"], sig8),
             ceiling=hp(tw_ce, vyt, c["eta_cl"], c["sig17"]))
    return tw, p


def c162_checks():
    tw, p = c162_constraints(10.0)
    book = dict(takeoff=0.1869, climb=0.2140, turn=0.1245, cruise=0.1192, ceiling=0.0943)
    for k, v in book.items():
        assert abs(tw[k] - v) < 5e-4, (k, tw[k])
    assert abs(p["cruise"] - 92) < 1.0
    # takeoff and ceiling power as read from the book's Figure 3-2 (0.60 at V_LOF; 0.65 at the ceiling)
    assert abs(c162_constraints(4.0)[1]["takeoff"] - 19.7) < 0.3 and abs(c162_constraints(16.0)[1]["takeoff"] - 104.5) < 0.5
    assert abs(c162_constraints(13.0)[1]["ceiling"] - 92) < 2.0
    ws = np.linspace(4, C162["ws_land"], 400)
    pmax = np.array([max(c162_constraints(w)[1].values()) for w in ws])
    j = int(np.argmin(pmax))
    assert abs(ws[j] - 11.2) < 0.1 and abs(pmax[j] - 89.4) < 0.5
    tw_land = max(c162_constraints(C162["ws_land"])[0].values())
    assert abs(tw_land - 0.208) < 0.002
    return ws[j], pmax[j]


C162_STYLE = [("takeoff", BLUE, "-."), ("climb", VERM, "-"), ("turn", INK, "-"), ("cruise", INK, "--"),
              ("ceiling", STEEL, ":")]


def c162_diagram():
    """Cessna 162 in thrust-to-weight ratio and in sea-level power; after Gudmundsson Fig. 3-2.

    The ceiling boundary follows Eq. 3-11 with V_Y changing with the wing loading. The book's figure
    holds the dynamic pressure fixed for that curve, so the two agree at W/S = 10 and differ away from it.
    """
    ws_dp, p_dp = c162_checks()
    ws = np.linspace(4, 30, 200)
    tw, p = c162_constraints(ws)
    env = ws <= C162["ws_land"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.8, 4.9))
    for ax, data, top in ((a1, tw, 0.5), (a2, p, 250)):
        upper = np.maximum.reduce(list(data.values()))
        ax.fill_between(ws[env], upper[env], top, color=DUST, lw=0)
        for name, color, ls in C162_STYLE:
            ax.plot(ws, data[name], color=color, lw=1.9, ls=ls, label=name)
        ax.plot([C162["ws_land"]] * 2, [0, top], color=GREEN, lw=1.9, label="landing boundary")
        ax.set_xlim(0, 30)
        ax.set_ylim(0, top)
        ax.set_xlabel("$W/S$ (lb/ft²)")
        clean(ax)
    tw_land = max(c162_constraints(C162["ws_land"])[0].values())
    a1.plot([C162["ws_land"]], [tw_land], "D", color=VERM, ms=7, zorder=5)
    a1.annotate(f"lowest $T/W$: {tw_land:.3f} at {C162['ws_land']}", xy=(C162["ws_land"], tw_land), xytext=(13.0, 0.43),
                fontsize=10.5, arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8))
    a2.plot([ws_dp], [p_dp], "D", color=VERM, ms=7, zorder=5)
    a2.annotate(f"lowest $P_{{SL}}$: {p_dp:.1f} hp at {ws_dp:.1f}", xy=(ws_dp, p_dp), xytext=(13.0, 215),
                fontsize=10.5, arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8))
    a1.text(7.2, 0.445, "feasible", fontsize=11, fontweight="bold", ha="center")
    a2.text(7.2, 222, "feasible", fontsize=11, fontweight="bold", ha="center")
    a1.set_ylabel("$T/W$")
    a2.set_ylabel("$P_{SL}$ (hp)")
    h, l = a1.get_legend_handles_labels()
    fig.legend(h, l, frameon=False, fontsize=10.5, ncol=6, loc="lower center", bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, "c162-diagram")


def c162_design_point():
    """The design point and the maximum lift coefficient it needs; after Gudmundsson Fig. 3-3."""
    ws_dp, p_dp = c162_checks()
    q45 = 0.5 * RHO_SL * (45 * KT) ** 2
    q61 = 0.5 * RHO_SL * (61 * KT) ** 2
    cl_dp = ws_dp / q45
    assert abs(q45 - 6.86) < 0.01 and abs(q61 - 12.61) < 0.02 and abs(cl_dp - 1.63) < 0.01
    ws = np.linspace(4, 30, 200)
    _, p = c162_constraints(ws)
    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    for name, color, ls in C162_STYLE:
        ax.plot(ws, p[name], color=color, lw=1.9, ls=ls, label=name)
    ax.plot([C162["ws_land"]] * 2, [0, 250], color=GREEN, lw=1.9, label="landing boundary")
    ax2 = ax.twinx()
    w = np.linspace(0, 30, 50)
    ax2.plot(w, w / q45, color=PURPLE, lw=1.6, ls=(0, (1, 1.5)))
    ax2.plot(w, w / q61, color=PURPLE, lw=1.6, ls=(0, (4, 2, 1, 2)))
    ax2.text(17.6, 2.42, "$V_S$ = 45 KCAS", fontsize=10.5, ha="left", va="center")
    ax2.text(23.2, 2.12, "$V_S$ = 61 KCAS", fontsize=10.5, ha="right", va="center")
    ax2.annotate("", xy=(ws_dp, cl_dp), xytext=(ws_dp, p_dp / 100), arrowprops=dict(arrowstyle="-|>", color=STEEL, lw=1.2))
    ax2.annotate("", xy=(30, cl_dp), xytext=(ws_dp, cl_dp), arrowprops=dict(arrowstyle="-|>", color=STEEL, lw=1.2))
    ax2.text(15.4, cl_dp - 0.04, f"$C_{{L_{{max}}}}$ = {cl_dp:.2f}", fontsize=10.5, ha="center", va="top")
    ax.plot([ws_dp], [p_dp], "D", color=VERM, ms=8, zorder=6)
    ax.annotate("design point", xy=(ws_dp, p_dp), xytext=(21.5, 28), fontsize=10.5, ha="center", va="center",
                arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8, shrinkB=5), zorder=7)
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 250)
    ax2.set_ylim(0, 2.5)
    ax.set_xlabel("$W/S$ (lb/ft²)")
    ax.set_ylabel("$P_{SL}$ (hp)")
    ax2.set_ylabel("$C_{L_{max}}$ at the stall speed")
    ax.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)
    ax.grid(True, color="#DDDDDD", lw=0.6)
    ax.legend(frameon=False, fontsize=10.5, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.14))
    fig.tight_layout()
    save(fig, "c162-design-point")


def isa(h_ft):
    """theta, delta, sigma, speed of sound (ft/s) in the troposphere and the lower stratosphere."""
    if h_ft <= 36089:
        t = 518.67 - 0.0035662 * h_ft
        theta = t / 518.67
        delta = theta ** 5.2559
    else:
        t = 389.97
        theta = t / 518.67
        delta = 0.22336 * np.exp(-(h_ft - 36089) / 20806)
    return theta, delta, delta / theta, 49.02 * np.sqrt(t)


def lapse_low_bpr(h_ft, mach, tr=1.07):
    """F/F_SL of a low-bypass turbofan at military thrust: the relation of Lecture 8."""
    theta, delta, _, _ = isa(h_ft)
    th0 = theta * (1 + 0.2 * mach ** 2)
    d0 = delta * (1 + 0.2 * mach ** 2) ** 3.5
    return d0 * (1.0 if th0 <= tr else 1 - 3.8 * (th0 - tr) / th0)


T45 = dict(W_TO=14500.0, W_L=13360.0, S=190.1, b=30.83, F_SL=5527.0, fuel=2893.0, Vmax_kt=543.0, h_Vmax=8000.0,
           RoC_fpm=8000.0, ceiling=42500.0, s_TO50=3610.0, s_L50=3310.0, VS_half=99.0, VS_full=94.0, W_VS=11500.0,
           V_app_full=116.0)
T45E = dict(CD0=0.020, dCDc=0.015, e=0.80, V_climb_kcas=300.0, M_ceiling=0.70, f_ground=0.70, glide_deg=3.5,
            t_FR=1.0, muB=0.40, k_TO=1.10)


def t45_boundaries(ws):
    p, e = T45, T45E
    ar = p["b"] ** 2 / p["S"]
    k1 = 1 / (np.pi * ar * e["e"])
    beta = (p["W_TO"] - 0.5 * p["fuel"]) / p["W_TO"]
    beta_l = p["W_L"] / p["W_TO"]
    qs = lambda v_kt: 0.5 * RHO_SL * (v_kt * KT) ** 2
    clmax_to = (p["W_VS"] / p["S"]) / qs(p["VS_half"])
    clmax_l = (p["W_VS"] / p["S"]) / qs(p["VS_full"])
    k_td = p["V_app_full"] / p["VS_full"]

    def level(h, v, cd0, ps=0.0):
        _, _, sig, a = isa(h)
        q = 0.5 * RHO_SL * sig * v ** 2
        alpha = lapse_low_bpr(h, v / a)
        return (beta / alpha) * (q * cd0 / (beta * ws) + k1 * beta * ws / q + ps / v)

    vmax = level(p["h_Vmax"], p["Vmax_kt"] * KT, e["CD0"] + e["dCDc"])
    climb = level(0.0, e["V_climb_kcas"] * KT, e["CD0"], ps=p["RoC_fpm"] / 60)
    ceiling = level(p["ceiling"], e["M_ceiling"] * isa(p["ceiling"])[3], e["CD0"], ps=100 / 60)
    s_g = e["f_ground"] * p["s_TO50"]
    takeoff = e["k_TO"] ** 2 * ws / (lapse_low_bpr(0.0, 0.1) * RHO_SL * G * s_g * clmax_to)
    s_air = 50.0 / np.tan(np.radians(e["glide_deg"]))
    ws_land = 80.0
    for _ in range(30):
        v_td = k_td * np.sqrt(2 * beta_l * ws_land / (RHO_SL * clmax_l))
        s_b = p["s_L50"] - s_air - e["t_FR"] * v_td
        ws_land = RHO_SL * G * e["muB"] * clmax_l * s_b / (beta_l * k_td ** 2)
    info = dict(AR=ar, K1=k1, beta=beta, beta_L=beta_l, CLmax_TO=clmax_to, CLmax_L=clmax_l, k_TD=k_td, s_G=s_g)
    return dict(vmax=vmax, climb=climb, ceiling=ceiling, takeoff=takeoff), ws_land, info


def t45_diagram():
    """The lecture's worked example: T-45C boundaries from published and estimated inputs."""
    ws_real, tw_real = T45["W_TO"] / T45["S"], T45["F_SL"] / T45["W_TO"]
    at, ws_land, info = t45_boundaries(ws_real)
    printed = dict(ceiling=0.328, vmax=0.320, climb=0.289, takeoff=0.260)
    for k, v in printed.items():
        assert abs(at[k] - v) < 0.001, (k, at[k])
    assert abs(tw_real / at["ceiling"] - 1.16) < 0.005        # the T-45C lies 16% above its highest boundary
    assert abs(ws_land - 99.3) < 0.5 and abs(ws_real - 76.3) < 0.05 and abs(tw_real - 0.381) < 0.001
    assert abs(info["AR"] - 5.0) < 0.01 and abs(info["K1"] - 0.080) < 0.001 and abs(info["beta"] - 0.90) < 0.002
    assert abs(info["CLmax_TO"] - 1.82) < 0.01 and abs(info["CLmax_L"] - 2.02) < 0.01 and abs(info["k_TD"] - 1.23) < 0.005
    ws = np.linspace(30, 120, 181)
    b, _, _ = t45_boundaries(ws)
    upper = np.maximum.reduce(list(b.values()))
    env = ws <= ws_land
    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    ax.fill_between(ws[env], upper[env], 0.8, color=DUST, lw=0)
    style = [("vmax", "maximum speed, 543 kt at 8,000 ft", INK, "-"), ("climb", "climb, 8,000 ft/min", VERM, "--"),
             ("ceiling", "ceiling, 42,500 ft", STEEL, "-."), ("takeoff", "takeoff, 3,610 ft", BLUE, "-")]
    for key, name, color, ls in style:
        ax.plot(ws, b[key], color=color, lw=1.9, ls=ls, label=name)
    ax.plot([ws_land, ws_land], [0, 0.8], color=GREEN, lw=1.9, ls=":", label="landing, 3,310 ft")
    ax.plot([ws_real], [tw_real], "D", color=VERM, ms=8, zorder=5, label="T-45C: 76.3 lb/ft² and 0.38")
    ax.text(55, 0.69, "feasible", fontsize=12, fontweight="bold", ha="center", va="center")
    ax.set_xlabel("$W_{TO}/S$ (lb/ft²)")
    ax.set_ylabel("$T_{SL}/W_{TO}$")
    ax.set_xlim(30, 120)
    ax.set_ylim(0, 0.8)
    ax.set_xticks([30, 45, 60, 75, 90, 105, 120])
    clean(ax)
    ax.legend(frameon=False, fontsize=10.5, ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.14))
    fig.tight_layout()
    save(fig, "t45-diagram")


ALL = [design_space, energy_height, path_forces, equation_flow, diagram_shape, fighter_diagram, design_point,
       c162_diagram, c162_design_point, t45_diagram]

if __name__ == "__main__":
    for fn in ALL:
        fn()
