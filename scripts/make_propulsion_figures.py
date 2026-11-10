"""Figures for Lecture 8, Propulsion Selection and Integration.

Each figure is redrawn after the figure on the lecture slide (Gudmundsson 2022,
Chapters 7 and 14; Nicolai and Carichner 2010, Appendix J; Team Draco 2025),
reduced to the point the slide makes and set in the book's typeface. The thrust
lapse and the inlet recovery are computed from the published relations and
checked against known values. The FJ44-3E deck uses the tabulated values. The
operational map, the efficiency curves, the fuel-flow chart, the engine trade,
the mission points, and the separation limits are read from the source figures.
The engine sections and the inlet streamtube are schematic. Run from the
book folder:

    python3 scripts/make_propulsion_figures.py

Set FIG_PREVIEW=<folder> to also write PNG copies for checking.
"""
import os
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, PathPatch
from matplotlib.path import Path as MPath

OUT = Path(__file__).resolve().parents[1] / "notes" / "lecture-08" / "figures"
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
COLD, WARM, HOT = "#C9DCEE", "#F6D2A8", "#EFA58B"


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight", pad_inches=0.1)
    if PREVIEW:
        fig.savefig(Path(PREVIEW) / f"{name}.png", dpi=110, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)
    print("wrote", name)


def clean(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(True, color="#DDDDDD", lw=0.6)


def smooth(points, n=200):
    """A smooth, shape-preserving curve through points read from a source figure."""
    from scipy.interpolate import PchipInterpolator
    x, y = np.array(points, dtype=float).T
    xs = np.linspace(x[0], x[-1], n)
    return xs, PchipInterpolator(x, y)(xs)


# ------------------------------------------------------------ part 1, selection
def _side(points, n=120):
    """Mach number along one side of an outline, as a smooth function of altitude."""
    from scipy.interpolate import PchipInterpolator
    h, m = np.array(points, dtype=float).T
    hs = np.linspace(h[0], h[-1], n)
    return PchipInterpolator(h, m)(hs), hs


def operational_map():
    """Outlines through points read from Gudmundsson Fig. 7-1: (altitude in 1,000 ft, Mach number)."""
    biz_right = [(0, 0.73), (5, 0.77), (10, 0.81), (15, 0.84), (20, 0.87), (25, 0.90)]
    classes = [
        ("Light sport, normally aspirated pistons", VERM, "-",
         [(0, 0.05), (4, 0.08), (8, 0.15), (10, 0.23)], [(0, 0.19), (4, 0.21), (8, 0.24), (10, 0.23)]),
        ("Single pistons, normally aspirated", BLUE, "--",
         [(0, 0.07), (5, 0.10), (10, 0.17), (14, 0.27), (16, 0.36)], [(0, 0.29), (5, 0.32), (10, 0.35), (14, 0.375), (16, 0.36)]),
        ("Turbo-normalized pistons, singles and twins", GREEN, "-.",
         [(0, 0.10), (5, 0.14), (10, 0.17), (15, 0.21), (20, 0.28), (23, 0.36), (25, 0.45)],
         [(0, 0.37), (5, 0.40), (10, 0.42), (15, 0.45), (20, 0.47), (23, 0.475), (25, 0.45)]),
        ("Single turboprops", SKY, "-",
         [(0, 0.08), (5, 0.11), (15, 0.19), (20, 0.25), (25, 0.33), (30, 0.48), (31.2, 0.55)],
         [(0, 0.43), (5, 0.45), (10, 0.47), (15, 0.50), (20, 0.54), (25, 0.56), (30, 0.58), (31.2, 0.55)]),
        ("Twin turboprops, commuters", INK, "--",
         [(0, 0.13), (5, 0.16), (15, 0.23), (20, 0.28), (30, 0.41), (35, 0.51), (40, 0.66), (42, 0.77)],
         [(0, 0.60), (5, 0.62), (10, 0.64), (15, 0.67), (20, 0.70), (25, 0.73), (30, 0.76), (35, 0.78), (40, 0.80),
          (42, 0.77)]),
        ("High-bypass turbofans, airliners", "#B8860B", "-.",
         [(0, 0.19), (5, 0.21), (15, 0.28), (20, 0.34), (25, 0.40), (30, 0.49), (35, 0.59), (40, 0.75), (42, 0.88)],
         biz_right + [(30, 0.91), (35, 0.92), (40, 0.92), (42, 0.88)]),
        ("High-bypass turbofans, business jets", PURPLE, "-",
         [(0, 0.18), (5, 0.20), (10, 0.23), (15, 0.26), (20, 0.30), (25, 0.35), (30, 0.41), (35, 0.48), (40, 0.57),
          (45, 0.68), (50, 0.84), (51.5, 0.93)],
         biz_right + [(30, 0.92), (35, 0.94), (40, 0.96), (45, 0.97), (50, 0.97), (51.5, 0.93)]),
    ]
    at25 = {}
    fig, ax = plt.subplots(figsize=(9.6, 5.2))
    label_y = [3.5, 9, 14.5, 20, 25.5, 36, 45]
    for (name, color, ls, left, right), ly in zip(classes, label_y):
        lm, lh = _side(left)
        rm, rh = _side(right)
        assert np.all(np.interp(lh, rh, rm) >= lm - 1e-9)        # the outline does not cross itself
        ax.plot(np.r_[lm, rm[::-1]], np.r_[lh, rh[::-1]], color=color, lw=1.9, ls=ls)
        ya = min(ly, 0.9 * rh[-1])
        ax.annotate(name, xy=(np.interp(ya, rh, rm), ya), xytext=(1.12, ly), fontsize=10.5, va="center", color=INK,
                    arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8, shrinkB=1))
        if rh[-1] >= 25:
            at25[name] = float(np.interp(25, rh, rm))
    # the source's high-speed limits at 25,000 ft, where the RFP states its maximum operating speed
    assert abs(at25["High-bypass turbofans, business jets"] - 0.90) < 0.005
    assert abs(at25["High-bypass turbofans, airliners"] - 0.90) < 0.005
    assert abs(at25["Twin turboprops, commuters"] - 0.73) < 0.005
    lm, lh = smooth([(0.27, 0), (0.4, 12), (0.6, 27), (0.8, 39), (1.0, 48), (1.25, 55), (1.5, 60)])
    rm, rh = smooth([(1.08, 0), (1.3, 10), (1.6, 19), (2.0, 29)])
    ax.plot(lm, lh, color=STEEL, lw=1.6, ls=":")
    ax.plot(rm, rh, color=STEEL, lw=1.6, ls=":")
    ax.text(1.42, 53.5, "Fighters: low-bypass turbofans or turbojets,\nwith afterburner, between the dotted lines",
            fontsize=10.5, color=INK, va="center")
    ax.set_xlabel("Mach number")
    ax.set_ylabel("Altitude (1,000 ft)")
    ax.set_xlim(0, 2.0)
    ax.set_ylim(0, 60)
    ax.set_xticks(np.arange(0, 2.01, 0.25))
    clean(ax)
    fig.tight_layout()
    save(fig, "operational-map")


def propulsive_efficiency():
    """After Gudmundsson Fig. 7-2: propulsive efficiency against Mach number by class."""
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    curves = [
        ("Constant-speed\npropeller", [(0, 0), (0.05, 0.38), (0.10, 0.62), (0.15, 0.75), (0.20, 0.81), (0.27, 0.84),
                                      (0.35, 0.845), (0.42, 0.835), (0.50, 0.79), (0.58, 0.68)], BLUE, "--",
         (0.20, 0.93), "center"),
        ("Turboprop", [(0, 0), (0.05, 0.25), (0.10, 0.45), (0.2, 0.69), (0.3, 0.80), (0.4, 0.84), (0.5, 0.845),
                       (0.6, 0.835), (0.68, 0.80), (0.74, 0.73)], GREEN, "-.", (0.52, 0.90), "center"),
        ("High-bypass turbofan", [(0, 0), (0.1, 0.21), (0.2, 0.37), (0.3, 0.49), (0.4, 0.59), (0.5, 0.67),
                                  (0.6, 0.73), (0.8, 0.81), (0.98, 0.85)], INK, "-", (0.90, 0.925), "center"),
        ("Low-bypass turbofan", [(0, 0), (0.2, 0.27), (0.4, 0.47), (0.6, 0.60), (0.8, 0.70), (1.0, 0.77),
                                 (1.28, 0.845)], PURPLE, "--", (1.38, 0.925), "center"),
        ("Turbojet", [(0, 0), (0.2, 0.23), (0.4, 0.40), (0.6, 0.53), (0.8, 0.63), (1.0, 0.71), (1.5, 0.86),
                      (2.0, 0.94)], STEEL, "-.", (1.86, 0.985), "center"),
    ]
    for name, pts, color, ls, (tx, ty), ha in curves:
        x, y = smooth(pts)
        ax.plot(x, y, color=color, lw=2.0, ls=ls)
        ax.text(tx, ty, name, fontsize=10.5, color=INK, ha=ha, va="center")
    ax.plot([0.95, 0.95], [0.856, 0.898], color=GRAY, lw=0.8)
    ax.plot([1.25, 1.25], [0.846, 0.898], color=GRAY, lw=0.8)
    ax.set_xlabel("Mach number")
    ax.set_ylabel(r"Propulsive efficiency $\eta_{prop}$")
    ax.set_xlim(0, 2.0)
    ax.set_ylim(0, 1.05)
    clean(ax)
    fig.tight_layout()
    save(fig, "propulsive-efficiency")


def _core(ax, y0, x0=0.0):
    """Compressor, burner, turbine, and nozzle of a gas generator centered on y0."""
    ax.add_patch(Polygon([(x0 + 2.0, y0 + 0.95), (x0 + 4.2, y0 + 0.55), (x0 + 4.2, y0 - 0.55), (x0 + 2.0, y0 - 0.95)],
                         closed=True, fc=COLD, ec=INK, lw=1.0))
    for xb in np.linspace(x0 + 2.35, x0 + 3.85, 5):
        t = (xb - x0 - 2.0) / 2.2
        hb = 0.95 - 0.40 * t
        ax.plot([xb, xb], [y0 - hb, y0 + hb], color=STEEL, lw=0.8)
    ax.add_patch(Polygon([(x0 + 4.2, y0 + 0.55), (x0 + 4.8, y0 + 0.85), (x0 + 4.8, y0 - 0.85), (x0 + 4.2, y0 - 0.55)],
                         closed=True, fc=LIGHT, ec=INK, lw=1.0))
    ax.add_patch(Rectangle((x0 + 4.8, y0 - 0.85), 1.7, 1.7, fc=WARM, ec=INK, lw=1.0))
    ax.add_patch(Rectangle((x0 + 6.5, y0 - 0.95), 0.4, 1.9, fc=HOT, ec=INK, lw=1.0))
    ax.add_patch(Polygon([(x0 + 6.9, y0 + 0.95), (x0 + 9.0, y0 + 0.60), (x0 + 9.0, y0 - 0.60), (x0 + 6.9, y0 - 0.95)],
                         closed=True, fc="#FBE9D7", ec="none"))
    ax.text(x0 + 3.1, y0, "compressor", ha="center", va="center", fontsize=10,
            bbox=dict(fc=COLD, ec="none", pad=1.0))
    ax.text(x0 + 5.65, y0, "burner", ha="center", va="center", fontsize=10)
    ax.text(x0 + 6.7, y0 - 1.2, "turbine", ha="center", va="top", fontsize=10)
    ax.text(x0 + 8.0, y0, "nozzle", ha="center", va="center", fontsize=10)


def _flow(ax, x0, x1, y, color, lw=1.6):
    ax.annotate("", xy=(x1, y), xytext=(x0, y), arrowprops=dict(arrowstyle="-|>", color=color, lw=lw))


def turbojet_turbofan():
    """After Gudmundsson Figs. 7-30 and 7-33: one stream, and a core stream with a bypass stream."""
    fig, ax = plt.subplots(figsize=(9.2, 6.6))
    ax.set_aspect("equal")
    ax.axis("off")
    # turbojet, centered on y = 5.2
    y = 5.2
    for s in (1, -1):
        ax.plot([1.0, 1.3, 6.9, 9.0], [y + s * 1.15, y + s * 1.05, y + s * 1.05, y + s * 0.62], color=INK, lw=2.4,
                solid_capstyle="round")
    _core(ax, y)
    _flow(ax, -0.4, 1.0, y, BLUE)
    _flow(ax, 9.1, 10.5, y, VERM)
    ax.text(-0.5, y + 0.45, r"ṁ at $V_\infty$", ha="left", va="bottom", fontsize=11)
    ax.text(10.6, y + 0.45, r"ṁ at $V_e$", ha="right", va="bottom", fontsize=11)
    ax.text(-0.5, y + 1.75, "Turbojet", fontsize=12.5, fontweight="bold", va="center")
    # turbofan, centered on y = 0
    y = 0.0
    for s in (1, -1):
        ax.plot([1.0, 1.3, 4.6], [y + s * 2.2, y + s * 2.05, y + s * 2.05], color=INK, lw=2.4, solid_capstyle="round")
        ax.plot([2.0, 6.9, 9.0], [y + s * 1.05, y + s * 1.05, y + s * 0.62], color=INK, lw=2.4, solid_capstyle="round")
        ax.add_patch(Rectangle((2.0, y + s * 1.6 - 0.45), 2.6, 0.9, fc="#E3EEF8", ec="none"))
        _flow(ax, 2.2, 5.6, y + s * 1.55, SKY)
    ax.add_patch(Rectangle((1.55, y - 2.0), 0.4, 4.0, fc=COLD, ec=INK, lw=1.0))
    ax.text(1.75, y + 2.3, "fan", ha="center", va="bottom", fontsize=10)
    _core(ax, y)
    _flow(ax, -0.4, 1.0, y + 1.0, BLUE)
    _flow(ax, -0.4, 1.0, y - 1.0, BLUE)
    _flow(ax, 9.1, 10.5, y, VERM)
    ax.text(5.8, y + 1.55, r"bypass air, ṁ$_{bypass}$", ha="left", va="center", fontsize=11)
    ax.text(10.6, y - 1.15, r"core air, ṁ$_{core}$", ha="right", va="top", fontsize=11)
    ax.text(-0.5, y + 1.4, r"ṁ$_i$", ha="left", va="bottom", fontsize=11)
    ax.text(-0.5, y + 2.75, "Turbofan", fontsize=12.5, fontweight="bold", va="center")
    ax.set_xlim(-0.7, 10.8)
    ax.set_ylim(-2.6, 7.3)
    save(fig, "turbojet-turbofan")


# --------------------------------------------------------- part 2, engine models
G = 1.4
TR = 1.07


def isa(h_ft):
    """Temperature and pressure ratios of the International Standard Atmosphere."""
    if h_ft <= 36089:
        theta = 1 - 6.87535e-6 * h_ft
        return theta, theta ** 5.2561
    return 0.751865, 0.223361 * np.exp(-(h_ft - 36089) / 20806)


def lapse(m, h_ft, kind):
    """Mattingly et al. (2002), as printed in Gudmundsson (2022), Eqs. 14-77 to 14-80."""
    theta, delta = isa(h_ft)
    ram = 1 + 0.5 * (G - 1) * m ** 2
    theta0, delta0 = theta * ram, delta * ram ** (G / (G - 1))
    over = np.maximum(theta0 - TR, 0)
    if kind == "low":      # military (dry), referred to the military sea-level static thrust
        return delta0 * (1 - 3.8 * over / theta0)
    return delta0 * (1 - 0.49 * np.sqrt(m) - 3 * over / (1.5 + m))


def turbofan_lapse():
    assert abs(lapse(0.6, 0, "low") - 1.266) < 0.002 and abs(lapse(0.9, 0, "low") - 1.182) < 0.002
    assert abs(lapse(0.9, 15000, "low") - 0.955) < 0.002 and abs(lapse(0.9, 25000, "low") - 0.628) < 0.002
    assert abs(lapse(0.3, 0, "high") - 0.779) < 0.002 and abs(lapse(0.9, 0, "high") - 0.711) < 0.002
    assert abs(lapse(0.9, 25000, "high") - 0.336) < 0.002 and abs(lapse(0.0, 35000, "high") - 0.235) < 0.002
    m = np.linspace(0, 0.9, 181)
    alts = [(0, "sea level", INK, "-"), (15000, "15,000 ft", BLUE, "--"), (25000, "25,000 ft", VERM, "-."),
            (35000, "35,000 ft", STEEL, ":")]
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.3), sharey=True)
    for ax, kind, title in zip(axes, ("low", "high"), ("Low bypass ratio, military (dry)", "High bypass ratio")):
        for h, name, color, ls in alts:
            y = lapse(m, h, kind)
            ax.plot(m, y, color=color, lw=2.0, ls=ls)
            ax.text(0.915, y[-1], name, fontsize=10.5, va="center", color=INK)
        ax.set_title(title)
        ax.set_xlabel("Mach number")
        ax.set_xlim(0, 1.13)
        ax.set_xticks([0, 0.3, 0.6, 0.9])
        ax.set_ylim(0, 1.4)
        clean(ax)
    axes[0].set_ylabel("$F/F_{SL}$")
    fig.tight_layout()
    save(fig, "turbofan-lapse")


def fj44_deck():
    """Nicolai and Carichner (2010), Table J.2b: FJ44-3E installed in a pod."""
    thrust = [
        ("sea level", [(0, 2254), (0.2, 1862), (0.3, 1671), (0.35, 1581)], INK, "-", "o"),
        ("10,000 ft", [(0, 2023), (0.2, 1751), (0.3, 1641), (0.4, 1549)], BLUE, "--", "s"),
        ("20,000 ft", [(0.2, 1376), (0.3, 1304), (0.4, 1255), (0.5, 1224)], VERM, "-.", "^"),
        ("30,000 ft", [(0.3, 948), (0.4, 924), (0.5, 914), (0.6, 914)], GREEN, "-", "D"),
        ("40,000 ft", [(0.3, 603), (0.4, 598), (0.5, 605), (0.6, 610)], STEEL, ":", "v"),
    ]
    part = [(1255, 0.67), (969, 0.67), (607, 0.728), (312, 0.956), (170, 1.24), (80, 1.91)]
    assert max(c for _, c in part) / min(c for _, c in part) > 2.8     # the point of the right panel
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 4.3))
    for name, pts, color, ls, mk in thrust:
        x, y = zip(*pts)
        a1.plot(x, y, color=color, lw=1.8, ls=ls, marker=mk, ms=5)
        if name == "sea level":
            a1.text(0.03, 2330, name, fontsize=10.5, va="center")
        else:
            a1.text(x[-1] + 0.02, y[-1], name, fontsize=10.5, va="center")
    a1.set_title("Highest tabulated throttle setting")
    a1.set_xlabel("Mach number")
    a1.set_ylabel("Installed net thrust (lb)")
    a1.set_xlim(0, 0.85)
    a1.set_xticks([0, 0.2, 0.4, 0.6])
    a1.set_ylim(0, 2500)
    x, y = zip(*part)
    a2.plot(x, y, color=INK, lw=1.8, marker="o", ms=5)
    a2.set_title("Part throttle at 20,000 ft, Mach 0.4")
    a2.set_xlabel("Installed net thrust (lb)")
    a2.set_ylabel("TSFC (1/h)")
    a2.set_xlim(0, 1400)
    a2.set_ylim(0, 2.0)
    for a in (a1, a2):
        clean(a)
    fig.tight_layout()
    save(fig, "fj44-deck")


def tfe731_fuel_flow():
    """Values read from Nicolai and Carichner (2010), Fig. J.5a: TFE731-1069 at sea level."""
    lines = [
        (0.0, [(190, 245), (600, 405), (1000, 570), (1400, 740), (2000, 1010), (2400, 1245), (2980, 1550)]),
        (0.2, [(130, 245), (500, 470), (1000, 700), (1500, 960), (2000, 1235), (2700, 1635)]),
        (0.3, [(100, 240), (500, 520), (1000, 800), (1500, 1080), (2000, 1380), (2480, 1660)]),
        (0.4, [(80, 235), (500, 560), (1000, 880), (1500, 1190), (2000, 1500), (2300, 1680)]),
        (0.5, [(480, 600), (1000, 960), (1500, 1290), (2130, 1700)]),
        (0.6, [(370, 595), (1000, 1050), (1500, 1400), (1990, 1730)]),
        (0.7, [(540, 800), (1000, 1130), (1270, 1320), (1870, 1760)]),
    ]
    fig, ax = plt.subplots(figsize=(7.2, 5.6))
    ends = []
    for mach, pts in lines:
        x, y = smooth(pts)
        ax.plot(x, y, color=BLUE, lw=1.7)
        ends.append(pts[-1])
    ex, ey = zip(*ends)
    ax.plot(ex, ey, color=INK, lw=1.6, ls="--")
    cx, cy = smooth([(1400, 1415), (1650, 1350), (1900, 1310), (2150, 1285), (2350, 1245)])
    ax.plot(cx, cy, color=INK, lw=1.6, ls="--")
    for (mach, _), (x, y) in zip(lines, ends):
        ax.text(x - 10, y + 22, f"{mach:.1f}", fontsize=10, ha="center", va="bottom")
    ax.text(1620, 1845, "Mach", fontsize=10, ha="center", va="bottom")
    ax.text(2500, 1740, "maximum continuous", fontsize=10.5, ha="left", va="bottom")
    ax.text(1960, 1205, "best cruise", fontsize=10.5, ha="left", va="top")
    ax.annotate("idle", xy=(150, 245), xytext=(420, 150), fontsize=10.5, va="center",
                arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8))
    ax.set_xlabel("Installed net thrust (lb)")
    ax.set_ylabel("Fuel flow (lb/h)")
    ax.set_xlim(0, 3400)
    ax.set_ylim(0, 2000)
    clean(ax)
    fig.tight_layout()
    save(fig, "tfe731-fuel-flow")


DRACO_PW229_35K = [(800, 2.0), (1000, 1.68), (1500, 1.27), (2000, 1.07), (2500, 0.97), (3000, 0.925), (3500, 0.90),
                   (4200, 0.888), (5000, 0.90), (5500, 0.94), (6080, 0.995)]


def engine_trade():
    """Values read from Team Draco (2025), Fig. 28: two candidates at 35,000 ft, Mach 0.8."""
    ge = [(600, 2.0), (1000, 1.37), (1500, 1.05), (2000, 0.91), (2500, 0.84), (3000, 0.805), (3500, 0.795),
          (4000, 0.80), (5000, 0.85), (5950, 0.945)]
    xg, yg = smooth(ge)
    xp, yp = smooth(DRACO_PW229_35K)
    lo, hi = 1960, 2860
    ratio = np.interp(lo, xg, yg) / np.interp(lo, xp, yp)
    assert 0.83 < ratio < 0.87                      # the report's 15% lower fuel flow
    assert xg[np.argmin(yg)] > hi and xp[np.argmin(yp)] > hi   # the loiter range is left of both minima
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ax.axvspan(lo, hi, color=DUST, alpha=0.7, lw=0)
    ax.plot(xp, yp, color=BLUE, lw=2.0, ls="--", label="F100-PW-229")
    ax.plot(xg, yg, color=VERM, lw=2.0, label="F110-GE-132")
    ax.text((lo + hi) / 2, 1.9, "loiter\nthrust range", ha="center", va="top", fontsize=10.5)
    ax.set_xlabel("Thrust (lbf)")
    ax.set_ylabel("TSFC (1/h)")
    ax.set_xlim(0, 6500)
    ax.set_ylim(0, 2.0)
    ax.legend(frameon=False, fontsize=10.5, loc="lower right")
    clean(ax)
    fig.tight_layout()
    save(fig, "engine-trade")


def deck_mission_points():
    """Values read from Team Draco (2025), Fig. 31: F100-PW-229, no afterburner, Mach 0.8."""
    curves = [
        ("10,000 ft", [(3100, 2.0), (3500, 1.85), (4000, 1.65), (5000, 1.45), (6000, 1.29), (7000, 1.19), (8000, 1.12),
                       (9000, 1.07), (10000, 1.03), (11000, 1.01), (12000, 1.003), (13250, 1.008)], INK, "-"),
        ("20,000 ft", [(1950, 2.0), (2500, 1.60), (3000, 1.38), (4000, 1.17), (5000, 1.06), (6000, 1.01), (7000, 0.975),
                       (8000, 0.96), (9000, 0.965), (10100, 0.988)], BLUE, "--"),
        ("35,000 ft", DRACO_PW229_35K, VERM, "-"),
        ("50,000 ft", [(380, 2.0), (500, 1.55), (800, 1.15), (1000, 1.03), (1500, 0.92), (2000, 0.885), (2300, 0.89),
                       (2700, 0.94), (3000, 1.0)], GREEN, "-."),
    ]
    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    for name, pts, color, ls in curves:
        x, y = smooth(pts)
        ax.plot(x, y, color=color, lw=2.0, ls=ls)
        dy = {"20,000 ft": -0.055, "35,000 ft": -0.095}.get(name, 0.0)
        ax.text(x[-1] + 150, y[-1] + dy, name, fontsize=10.5, va="center")
    x35, y35 = smooth(DRACO_PW229_35K)
    loiter = [(1960, float(np.interp(1960, x35, y35))), (2860, float(np.interp(2860, x35, y35)))]
    assert abs(loiter[0][1] - 1.08) < 0.03 and abs(loiter[1][1] - 0.935) < 0.03   # the points lie on the curve
    lx, ly = zip(*loiter)
    ax.plot(lx, ly, "o", color=INK, ms=8, mfc="white", mew=2.0, zorder=5, label="loiter, start and end")
    ax.legend(frameon=False, fontsize=10.5, loc="upper right")
    ax.set_xlabel("Thrust (lbf)")
    ax.set_ylabel("TSFC (1/h)")
    ax.set_xlim(0, 15500)
    ax.set_ylim(0.8, 2.0)
    clean(ax)
    fig.tight_layout()
    save(fig, "deck-mission-points")


# ----------------------------------------------------------- part 3, integration
def _nacelle(ax, y0):
    """An inlet lip and duct in section, with the fan face."""
    for s in (1, -1):
        ax.add_patch(Polygon([(0, y0 + s * 0.90), (0.35, y0 + s * 1.22), (1.6, y0 + s * 1.45), (4.2, y0 + s * 1.45),
                              (4.2, y0 + s * 1.12), (1.6, y0 + s * 1.12), (0.5, y0 + s * 0.98)],
                             closed=True, fc="#E6E6E6", ec=INK, lw=1.2))
    ax.add_patch(Rectangle((2.7, y0 - 1.10), 0.22, 2.2, fc=COLD, ec=INK, lw=1.0))
    ax.text(2.81, y0 - 1.62, "fan", ha="center", va="top", fontsize=10)


def inlet_streamtube():
    """After Gudmundsson Fig. 7-38: the captured streamtube at rest and at cruise."""
    fig, ax = plt.subplots(figsize=(7.4, 8.8))
    ax.set_aspect("equal")
    ax.axis("off")
    t = np.linspace(0, 1, 60)
    # at rest: air is drawn in from all around the lip
    y0 = 6.9
    _nacelle(ax, y0)
    for a in (0.0, 0.42, 0.82):
        for s in ((1, -1) if a else (1,)):
            x = -4.6 + 4.6 * t
            y = y0 + s * (a * 0.9 + a * 2.2 * (1 - t) ** 2.2)
            ax.plot(x, y, color=BLUE, lw=1.3)
            ax.annotate("", xy=(0.9, y0 + s * a * 0.9), xytext=(0.0, y0 + s * a * 0.9),
                        arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.3))
    for s in (1, -1):
        verts = [(2.2, y0 + s * 2.9), (-1.9, y0 + s * 3.1), (-1.5, y0 + s * 0.86), (0.0, y0 + s * 0.86)]
        ax.add_patch(PathPatch(MPath(verts, [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4]),
                               fc="none", ec=BLUE, lw=1.3))
    ax.text(-4.6, y0 + 3.9, "At rest", fontsize=12.5, fontweight="bold", va="center")
    ax.text(-4.6, y0 + 3.3, "The streamtube is wider than the lip.", fontsize=11, va="center")
    # at cruise: the streamtube is narrower than the lip
    y0 = 0.0
    _nacelle(ax, y0)
    for a in (0.0, 0.42, 0.82):
        for s in ((1, -1) if a else (1,)):
            x = -4.6 + 4.6 * t
            y = y0 + s * a * (0.62 + 0.28 * t ** 2.5)
            ax.plot(x, y, color=BLUE, lw=1.3)
            ax.annotate("", xy=(0.9, y0 + s * a * 0.9), xytext=(0.0, y0 + s * a * 0.9),
                        arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.3))
    for s in (1, -1):
        ax.plot(-4.6 + 4.6 * t, y0 + s * (0.62 + 0.28 * t ** 2.5), color=STEEL, lw=1.2, ls="--")
    ax.annotate("", xy=(-4.25, y0 + 0.62), xytext=(-4.25, y0 - 0.62),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.0))
    ax.text(-4.1, y0 + 0.95, r"demand capture area $A_{\infty E}$", fontsize=11, va="center")
    ax.annotate("", xy=(0.0, y0 + 0.90), xytext=(0.0, y0 - 0.90), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.0))
    ax.text(-0.15, y0 + 1.75, "lip area", fontsize=11, ha="center", va="center")
    ax.text(-4.6, y0 + 3.2, "At cruise", fontsize=12.5, fontweight="bold", va="center")
    ax.text(-4.6, y0 + 2.6, "The streamtube is narrower than the lip.", fontsize=11, va="center")
    ax.set_xlim(-4.8, 4.4)
    ax.set_ylim(-2.3, 11.1)
    save(fig, "inlet-streamtube")


def diffuser():
    """After Gudmundsson Figs. 7-39 and 7-40: diffuser geometry and the separation limits."""
    lo = [(0.4, 40), (0.5, 36), (1, 26.5), (1.5, 22), (2, 19), (3, 15.5), (4, 13.2), (5, 11.7), (6, 10.5)]
    hi = [(0.45, 40), (0.5, 38.5), (1, 29), (1.5, 25), (2, 22.3), (3, 19), (4, 16.8), (5, 15.2), (6, 14)]
    assert min(y for _, y in lo) > 10          # ten degrees stays below the lower limit over the range drawn
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.8, 4.3), gridspec_kw=dict(width_ratios=[1, 1.15]))
    a1.set_aspect("equal")
    a1.axis("off")
    for s in (1, -1):
        a1.add_patch(Polygon([(0, s * 0.80), (0.3, s * 1.10), (1.5, s * 1.42), (4.4, s * 1.42), (4.4, s * 1.18),
                              (3.0, s * 1.18), (0.45, s * 0.86)], closed=True, fc="#E6E6E6", ec=INK, lw=1.2))
        a1.plot([-1.6, 0.0], [s * 0.60, s * 0.80], color=GRAY, lw=0.9, ls=":")
    a1.add_patch(Rectangle((3.0, -1.16), 0.22, 2.32, fc=COLD, ec=INK, lw=1.0))
    a1.annotate("", xy=(0.25, 0.80), xytext=(0.25, -0.80), arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.1))
    a1.text(0.4, 0.0, "$D_t$", fontsize=12, va="center")
    a1.annotate("", xy=(2.7, 1.16), xytext=(2.7, -1.16), arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.1))
    a1.text(2.25, 0.0, "$D_f$", fontsize=12, va="center")
    a1.annotate("", xy=(3.0, 1.85), xytext=(0.0, 1.85), arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.1))
    a1.plot([0, 0], [1.0, 1.95], color=GRAY, lw=0.8)
    a1.plot([3.0, 3.0], [1.5, 1.95], color=GRAY, lw=0.8)
    a1.text(1.5, 2.0, "$L$", fontsize=12, ha="center", va="bottom")
    a1.annotate("", xy=(-1.45, 0.62), xytext=(-1.45, -0.62),
                arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.1, connectionstyle="arc3,rad=0.25"))
    a1.text(-1.95, 0.0, r"$\theta$", fontsize=13, ha="center", va="center")
    a1.text(3.11, -1.65, "compressor\nface", fontsize=10, ha="center", va="top")
    a1.text(0.0, -1.65, "throat", fontsize=10, ha="center", va="top")
    a1.set_xlim(-2.3, 4.6)
    a1.set_ylim(-2.5, 2.5)
    xl, yl = smooth(lo)
    xh, yh = smooth(hi)
    a2.plot(xh, yh, color=INK, lw=2.0, ls="--", label="upper limit")
    a2.plot(xl, yl, color=INK, lw=2.0, label="lower limit")
    a2.axhline(10, color=VERM, lw=1.6, ls="-.")
    a2.text(0.15, 8.6, r"$\theta$ = 10°", color=INK, fontsize=10.5, va="top")
    a2.text(3.6, 30, "full separation", fontsize=10.5, ha="center")
    a2.text(3.5, 16.0, "transitory separation", fontsize=10, ha="center", va="center", rotation=-12.5,
            rotation_mode="anchor")
    a2.text(1.4, 4.5, "no separation", fontsize=10.5, ha="center")
    a2.set_xlabel("Diffuser length over throat diameter")
    a2.set_ylabel(r"Included angle $\theta$ (deg)")
    a2.set_xlim(0, 6)
    a2.set_ylim(0, 40)
    a2.legend(frameon=False, fontsize=10.5, loc="upper right")
    clean(a2)
    fig.tight_layout()
    save(fig, "diffuser")


def normal_shock(m):
    """Total pressure ratio across a normal shock; 1 below Mach 1."""
    m = np.maximum(m, 1.0)
    a = ((G + 1) * m ** 2 / ((G - 1) * m ** 2 + 2)) ** (G / (G - 1))
    b = ((G + 1) / (2 * G * m ** 2 - (G - 1))) ** (1 / (G - 1))
    return a * b


def mil_e_5008b(m):
    return 1 - 0.075 * np.maximum(m - 1.0, 0) ** 1.35


def inlet_recovery():
    assert abs(normal_shock(2.0) - 0.7209) < 0.0005 and abs(mil_e_5008b(2.0) - 0.925) < 0.0005
    assert normal_shock(0.9) == 1.0 and mil_e_5008b(0.9) == 1.0     # no shock loss below Mach 1
    m = np.linspace(0, 2.0, 401)
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    ax.plot(m, mil_e_5008b(m), color=BLUE, lw=2.0, ls="--", label="MIL-E-5008B")
    ax.plot(m, normal_shock(m), color=INK, lw=2.0, label="one normal shock (pitot inlet)")
    ax.axvline(1.0, color=GRAY, lw=0.9, ls=":")
    ax.text(0.5, 0.965, "subsonic: no shock loss", fontsize=10.5, ha="center", va="center")
    ax.set_xlabel("Flight Mach number")
    ax.set_ylabel("Pressure recovery from shocks")
    ax.set_xlim(0, 2.0)
    ax.set_ylim(0.70, 1.02)
    ax.legend(frameon=False, fontsize=10.5, loc="lower left")
    clean(ax)
    fig.tight_layout()
    save(fig, "inlet-recovery")


ALL = [operational_map, propulsive_efficiency, turbojet_turbofan, turbofan_lapse, fj44_deck, tfe731_fuel_flow,
       engine_trade, deck_mission_points, inlet_streamtube, diffuser, inlet_recovery]

if __name__ == "__main__":
    for fn in ALL:
        fn()
