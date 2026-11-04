"""Figures for Lecture 6, High-Lift Systems.

Each figure is redrawn after the figure on the lecture slide (Gudmundsson
2022, Chapters 8, 10, 16, 18, and 23), reduced to the point the slide makes
and set in the book's typeface. Device sketches and lift curves are
schematic; the SR22 bars and the partition planform carry the published
example values. Run from the book folder:

    python3 scripts/make_highlift_figures.py

Set FIG_PREVIEW=<folder> to also write PNG copies for checking.
"""
import os
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Arc

OUT = Path(__file__).resolve().parents[1] / "notes" / "lecture-06" / "figures"
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
BLUE, VERM, GREEN, SKY = "#0072B2", "#D55E00", "#009E73", "#56B4E9"


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


def lift_curve(a, a0, a_stall, clmax, post=0.04, slope=0.1):
    x = np.clip(a - a0, 0, None)
    k = slope / clmax
    pre = clmax * np.tanh(k * x)
    cl_stall = clmax * np.tanh(k * (a_stall - a0))
    pre = pre * clmax / cl_stall
    pre = np.where(a < a0, slope * (a - a0), pre)
    post_curve = clmax - post * (a - a_stall) - 0.01 * (a - a_stall) ** 2
    return np.where(a <= a_stall, pre, post_curve)


# ------------------------------------------------------------ airfoil pieces
def naca4(m, p, t, n=160):
    x = 0.5 * (1 - np.cos(np.linspace(0, np.pi, n)))
    yt = 5 * t * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x ** 2 + 0.2843 * x ** 3 - 0.1015 * x ** 4)
    if p > 0:
        yc = np.where(x < p, m / p ** 2 * (2 * p * x - x ** 2), m / (1 - p) ** 2 * (1 - 2 * p + 2 * p * x - x ** 2))
        dyc = np.where(x < p, 2 * m / p ** 2 * (p - x), 2 * m / (1 - p) ** 2 * (p - x))
    else:
        yc, dyc = 0 * x, 0 * x
    th = np.arctan(dyc)
    return x - yt * np.sin(th), yc + yt * np.cos(th), x + yt * np.sin(th), yc - yt * np.cos(th)


XU, YU, XL, YL = naca4(0.02, 0.4, 0.14)


def piece(x0, x1):
    """Closed polygon of the airfoil between chordwise stations x0 and x1."""
    mu = (XU >= x0) & (XU <= x1)
    ml = (XL >= x0) & (XL <= x1)
    xs = np.concatenate([[x0], XU[mu], [x1], XL[ml][::-1], [x0]])
    ys = np.concatenate([[np.interp(x0, XU, YU)], YU[mu], [np.interp(x1, XU, YU)], YL[ml][::-1], [np.interp(x0, XL, YL)]])
    # close the cut faces with straight lines through the interpolated points
    return np.column_stack([xs, ys])


def rotate(pts, pivot, deg):
    th = np.radians(deg)
    R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    return (pts - pivot) @ R.T + pivot


def shrouded(x_cut, x_lip, t=0.012):
    """Main body cut at x_cut whose upper skin runs on to x_lip as a thin shroud lip."""
    mu = (XU >= 0) & (XU <= x_lip)
    ml = (XL >= 0) & (XL <= x_cut)
    y_lip, y_cut = np.interp(x_lip, XU, YU), np.interp(x_cut, XU, YU)
    xs = np.concatenate([XU[mu], [x_lip, x_lip, x_cut], XL[ml][::-1]])
    ys = np.concatenate([YU[mu], [y_lip, y_lip - t, y_cut - t], YL[ml][::-1]])
    return np.column_stack([xs, ys])


def draw_device(ax, kind):
    ax.set_aspect("equal")
    ax.axis("off")
    main_face = dict(fc=LIGHT, ec=INK, lw=1.3)
    flap_face = dict(fc=DUST, ec=INK, lw=1.3)
    if kind == "plain":
        ax.add_patch(Polygon(piece(0, 0.7), closed=True, **main_face))
        h = np.array([0.7, np.interp(0.7, XU, YU) - 0.5 * (np.interp(0.7, XU, YU) - np.interp(0.7, XL, YL))])
        ax.add_patch(Polygon(rotate(piece(0.7, 1.0), h, -30), closed=True, **flap_face))
        ax.plot(*h, "o", color=INK, ms=3)
    elif kind == "split":
        ax.add_patch(Polygon(piece(0, 1.0), closed=True, **main_face))
        h = np.array([0.7, np.interp(0.7, XL, YL)])
        plate = np.array([[0.7, h[1]], [1.0, np.interp(1.0, XL, YL)], [1.0, np.interp(1.0, XL, YL) - 0.012], [0.7, h[1] - 0.012]])
        ax.add_patch(Polygon(rotate(plate, h, -45), closed=True, **flap_face))
        ax.plot(*h, "o", color=INK, ms=3)
    elif kind == "single":
        # the flap nose sits just below and behind the shroud lip, leaving a narrow slot
        ax.add_patch(Polygon(shrouded(0.72, 0.84), closed=True, **main_face))
        f = piece(0.72, 1.0) + np.array([0.06, -0.05])
        ax.add_patch(Polygon(rotate(f, f[0], -35), closed=True, **flap_face))
    elif kind == "double":
        ax.add_patch(Polygon(shrouded(0.72, 0.80), closed=True, **main_face))
        v = piece(0.72, 0.85) + np.array([0.04, -0.04])
        v = rotate(v, v[0], -18)
        ax.add_patch(Polygon(v, closed=True, **flap_face))
        f = piece(0.85, 1.0) + np.array([0.085, -0.10])
        ax.add_patch(Polygon(rotate(f, f[0], -50), closed=True, **flap_face))
    elif kind == "fowler":
        # the flap runs aft on tracks: its nose clears the shroud lip, so the chord grows
        ax.add_patch(Polygon(shrouded(0.72, 0.85), closed=True, **main_face))
        f = piece(0.72, 1.0) + np.array([0.13, -0.055])
        ax.add_patch(Polygon(rotate(f, f[0], -30), closed=True, **flap_face))
    elif kind == "droop":
        ax.add_patch(Polygon(piece(0.15, 1.0), closed=True, **main_face))
        h = np.array([0.15, 0.5 * (np.interp(0.15, XU, YU) + np.interp(0.15, XL, YL))])
        ax.add_patch(Polygon(rotate(piece(0, 0.15), h, -22), closed=True, **flap_face))
        ax.plot(*h, "o", color=INK, ms=3)
    elif kind == "slot":
        ax.add_patch(Polygon(piece(0.14, 1.0), closed=True, **main_face))
        ax.add_patch(Polygon(piece(0, 0.11) + np.array([-0.025, -0.012]), closed=True, **flap_face))
    elif kind == "kruger":
        # hinged at the leading edge, swung forward to stand ahead of and below the nose
        ax.add_patch(Polygon(piece(0, 1.0), closed=True, **main_face))
        h = np.array([0.02, np.interp(0.02, XL, YL)])
        plate = np.array([[0.02, h[1]], [0.02 - 0.17, h[1]], [0.02 - 0.17, h[1] - 0.012], [0.02, h[1] - 0.012]])
        ax.add_patch(Polygon(rotate(plate, h, 35), closed=True, **flap_face))
        ax.plot(*h, "o", color=INK, ms=3)
    elif kind == "slat":
        ax.add_patch(Polygon(piece(0.15, 1.0), closed=True, **main_face))
        s = piece(0, 0.14) + np.array([-0.08, -0.05])
        ax.add_patch(Polygon(rotate(s, s[0], -12), closed=True, **flap_face))
    ax.set_xlim(-0.25, 1.25)
    ax.set_ylim(-0.33, 0.2)


def trailing_edge_devices():
    fig, axes = plt.subplots(1, 5, figsize=(12, 2.6))
    names = [("plain", "Plain", "+0.66 at 45°"), ("split", "Split", "+0.89 at 60°"),
             ("single", "Single-slotted", "+1.32 at 40°"), ("double", "Double-slotted", "+1.40 at 55° to 60°"),
             ("fowler", "Fowler", "+2.24 at 40°")]
    for ax, (k, n, inc) in zip(axes, names):
        draw_device(ax, k)
        ax.set_title(n, fontsize=12)
        ax.text(0.5, -0.3, inc, ha="center", va="top", fontsize=11, color=STEEL)
    fig.tight_layout()
    save(fig, "trailing-edge-devices")


def leading_edge_devices():
    fig, axes = plt.subplots(1, 4, figsize=(11, 2.6))
    names = [("droop", "Droop nose", "+0.58, stall +7.8°"), ("slot", "Fixed slot", "+0.45, stall +9.0°"),
             ("kruger", "Krüger flap", "+0.30, stall +5.0°"), ("slat", "Slat", "+0.84, stall +11.0°")]
    for ax, (k, n, inc) in zip(axes, names):
        draw_device(ax, k)
        ax.set_title(n, fontsize=12)
        ax.text(0.5, -0.3, inc, ha="center", va="top", fontsize=11, color=STEEL)
    fig.tight_layout()
    save(fig, "leading-edge-devices")


# ------------------------------------------------------------ lift curves
def flap_lift_curve():
    fig, ax = plt.subplots(figsize=(8, 4.6))
    a = np.linspace(-14, 28, 500)
    curves = [("clean", -2, 15, 1.5, "-", INK), ("trailing-edge flap", -10, 11, 2.3, "--", VERM),
              ("slat", -2, 24, 2.1, ":", BLUE), ("flap and slat", -10, 20, 2.9, "-.", GREEN)]
    for lab, a0, ast, clmax, ls, c in curves:
        ax.plot(a, lift_curve(a, a0, ast, clmax, post=0.05), ls=ls, color=c, lw=2.2, label=lab)
    ax.axhline(0, color=STEEL, lw=0.7)
    ax.axvline(0, color=STEEL, lw=0.7)
    # labels in the open corners: the curves run through the lower half of the plot
    ax.text(-13.5, 3.15, "a flap shifts the curve up and left:\nhigher $C_{l_{max}}$, lower $\\alpha_{stall}$", fontsize=10.5, color=VERM, va="bottom")
    ax.text(15.0, 3.15, "a slat extends the curve:\nhigher $C_{l_{max}}$ and $\\alpha_{stall}$", fontsize=10.5, color=BLUE, va="bottom")
    ax.set_xlabel(r"Angle of attack $\alpha$ (deg)")
    ax.set_ylabel("Section lift coefficient $C_l$")
    ax.set_xlim(-14, 28)
    ax.set_ylim(-1.0, 3.8)
    ax.legend(frameon=False, fontsize=10, loc="upper left", bbox_to_anchor=(-14, 2.6), bbox_transform=ax.transData)
    clean(ax)
    fig.tight_layout()
    save(fig, "flap-lift-curve")


def slot_lift_curve():
    fig, ax = plt.subplots(figsize=(7, 4.2))
    # Clark Y with and without a slot, after Gudmundsson Fig. 8-61: stall 12° -> 18°, peak 1.38 -> 1.96
    a = np.linspace(-6, 28, 500)
    ax.plot(a, lift_curve(a, -3, 12, 1.38, post=0.05), color=INK, lw=2.2, label="clean airfoil")
    ax.plot(a, lift_curve(a, -3, 18, 1.96, post=0.05), color=BLUE, lw=2.2, ls="--", label="with a fixed slot")
    ax.axhline(0, color=STEEL, lw=0.7)
    ax.text(10.0, 2.12, "the slot delays the stall\nby about 6 degrees", fontsize=10.5, color=BLUE, va="bottom")
    ax.set_xlabel(r"Angle of attack $\alpha$ (deg)")
    ax.set_ylabel("$C_l$")
    ax.set_xlim(-6, 28)
    ax.set_ylim(-0.5, 2.6)
    ax.legend(frameon=False, fontsize=10, loc="upper left")
    clean(ax)
    fig.tight_layout()
    save(fig, "slot-lift-curve")


def increment_vs_deflection():
    fig, ax = plt.subplots(figsize=(8, 4.4))
    # smooth monotone curves through the Table 10-4 values (plain and split c_f/c = 0.2,
    # single-slotted and Fowler c_f/c = 0.3), each drawn over the deflections the table covers
    try:
        from scipy.interpolate import PchipInterpolator as _pchip
    except ImportError:  # piecewise linear if scipy is missing
        _pchip = lambda x, y: (lambda xx: np.interp(xx, x, y))
    table = (("plain", "-", INK, [(0, 0), (15, 0.24), (30, 0.48), (45, 0.66)]),
             ("split", "--", STEEL, [(0, 0), (15, 0.35), (30, 0.62), (45, 0.82), (60, 0.89)]),
             ("single-slotted", "-.", BLUE, [(0, 0), (30, 1.10), (40, 1.32), (50, 1.37)]),
             ("Fowler", ":", VERM, [(0, 0), (20, 1.61), (30, 1.99), (40, 2.24)]))
    for lab, ls, c, pts in table:
        x, y = np.array(pts).T
        d = np.linspace(0, x[-1], 200)
        ax.plot(d, _pchip(x, y)(d), ls=ls, color=c, lw=2.2, label=lab)
        ax.plot(x[1:], y[1:], "o", color=c, ms=6)
    ax.axvspan(10, 20, color=DUST, alpha=0.6, lw=0)
    ax.text(15, 2.45, "takeoff\n10° to 20°", ha="center", fontsize=10, color=AGED)
    ax.text(1.5, 1.5, "plain flap: the flow separates\nabove about 15°", fontsize=10, color=STEEL, va="bottom")
    ax.set_xlabel("Flap deflection (deg)")
    ax.set_ylabel(r"Section increment $\Delta C_{l_{max}}$")
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 2.8)
    ax.legend(frameon=False, fontsize=10, loc="upper left")
    clean(ax)
    fig.tight_layout()
    save(fig, "increment-vs-deflection")


def flap_drag():
    fig, ax = plt.subplots(figsize=(7, 4.0))
    for lab, v30, v50, ls, c in (("plain or split", 0.050, 0.100, "-", INK), ("slotted", 0.020, 0.050, "--", BLUE), ("Fowler", 0.032, 0.083, "-.", VERM)):
        ax.plot([30, 50], [v30, v50], ls=ls, color=c, lw=2.2, marker="o", ms=7, label=lab)
    ax.set_xlabel("Flap deflection (deg)")
    ax.set_ylabel(r"$\Delta C_D$ of the flap")
    ax.set_xlim(25, 55)
    ax.set_ylim(0, 0.11)
    ax.set_xticks([30, 40, 50])
    ax.legend(frameon=False, fontsize=10, loc="upper left")
    ax.text(54, 0.004, "flap span 60%, chord 25%", fontsize=10, color=STEEL, ha="right")
    clean(ax)
    fig.tight_layout()
    save(fig, "flap-drag")


# ------------------------------------------------------------ wing
def partial_span_flaps():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.6), gridspec_kw=dict(width_ratios=[1.1, 1]))
    a1.set_aspect("equal")
    a1.axis("off")
    lam, cr = 0.6, 1.6
    xs = np.array([0, 1, 1, 0])
    ys = np.array([0, -0.15, -0.15 - lam * cr, -cr])
    a1.add_patch(Polygon(np.column_stack([xs * 4, ys]), closed=True, fc=LIGHT, ec=INK, lw=1.4))
    for s0, s1, c, lab in ((0.12, 0.62, GOLD, "flap"), (0.65, 0.95, "#C9CED6", "aileron")):
        xx = np.array([s0, s1, s1, s0]) * 4
        top = -0.15 * np.array([s0, s1]) - 0.75 * (cr - (cr - lam * cr) * np.array([s0, s1]))
        bot = -0.15 * np.array([s0, s1]) - (cr - (cr - lam * cr) * np.array([s0, s1]))
        a1.add_patch(Polygon(np.column_stack([xx, [top[0], top[1], bot[1], bot[0]]]), closed=True, fc=c, ec=INK, lw=1.0))
        a1.text((s0 + s1) / 2 * 4, (top.mean() + bot.mean()) / 2, lab, ha="center", va="center", fontsize=11)
    a1.plot([0, 0], [0.15, -cr - 0.15], color=STEEL, lw=0.8, ls=":")
    a1.text(0.05, 0.1, "root", fontsize=10, color=STEEL)
    a1.text(3.95, 0.1, "tip", fontsize=10, color=STEEL, ha="right")
    a1.set_title("Flaps inboard, ailerons outboard", fontsize=11)
    a1.set_xlim(-0.1, 4.1)
    a1.set_ylim(-cr - 0.3, 0.4)
    eta = np.linspace(0, 1, 300)
    base = 1.0 - 0.35 * eta ** 3
    ramp = 1 / (1 + np.exp(-(eta - 0.12) / 0.02)) - 1 / (1 + np.exp(-(eta - 0.62) / 0.02))
    a2.plot(eta, base, color=INK, lw=2.0, label="flaps up")
    a2.plot(eta, base + 0.72 * ramp, color=VERM, lw=2.0, ls="--", label="flaps down")  # stays under the section maximum
    a2.axhline(1.75, color=STEEL, lw=0.8, ls=":")
    a2.text(0.98, 1.78, "section $C_{l_{max}}$, flapped", fontsize=9.5, color=STEEL, ha="right")
    a2.text(0.66, 1.2, "the flapped part reaches\nits maximum first", fontsize=10, color=VERM)
    a2.set_xlabel("Spanwise station $2y/b$")
    a2.set_ylabel("Section $C_l$")
    a2.set_xlim(0, 1)
    a2.set_ylim(0, 2.2)
    a2.legend(frameon=False, fontsize=10, loc="lower left")
    clean(a2)
    fig.tight_layout()
    save(fig, "partial-span-flaps")


def wing_partition():
    """The SR22 half wing split into the four segments of Gudmundsson's
    Example 10-3: stations and areas from the slide's table."""
    fig, ax = plt.subplots(figsize=(9, 3.4))
    ax.set_aspect("equal")
    ax.axis("off")
    b2, S, lam = 19.15, 144.9, 0.5
    cr = 2 * S / (2 * b2 * (1 + lam))
    ct = lam * cr
    chord = lambda y: cr - (cr - ct) * y / b2
    ys = [0, 3.0, 11.75, 16.42, 19.15]
    names = ["I, root", "II, flap", "III, aileron", "IV, tip"]
    areas = [14.88, 36.49, 15.27, 7.57]
    colors = [LIGHT, GOLD, "#C9CED6", LIGHT]
    for y0, y1, n, A, c in zip(ys[:-1], ys[1:], names, areas, colors):
        poly = np.array([[y0, 0], [y1, 0], [y1, -chord(y1)], [y0, -chord(y0)]])
        ax.add_patch(Polygon(poly, closed=True, fc=c, ec=INK, lw=1.2))
        ax.text((y0 + y1) / 2, -chord((y0 + y1) / 2) / 2, f"{n}\n{A} ft²", ha="center", va="center", fontsize=10)
    for y in ys:
        ax.plot([y, y], [0.15, 0.45], color=STEEL, lw=0.8)
        ax.text(y, 0.5, f"{y:g}", ha="center", va="bottom", fontsize=10, color=STEEL)
    ax.text(b2 / 2, 1.05, "spanwise station, ft", ha="center", fontsize=10, color=STEEL)
    ax.plot([0, 0], [-cr - 0.3, 0.1], color=STEEL, lw=0.8, ls=":")
    ax.text(0.2, -cr - 0.25, "root", fontsize=10, color=STEEL, va="top")
    ax.set_xlim(-0.6, b2 + 0.6)
    ax.set_ylim(-cr - 0.9, 1.6)
    fig.tight_layout()
    save(fig, "wing-partition")


def fclp_approach():
    fig, ax = plt.subplots(figsize=(9, 4.0))
    ax.set_aspect("equal")
    ax.axis("off")
    P = np.array([1.2, 2.3])
    A = np.array([7.52, 0.0])
    B = np.array([4.14, 0.0])
    ax.plot([0, 8.8], [0, 0], color=STEEL, lw=1.2)
    ax.plot([P[0], A[0]], [P[1], A[1]], color=AGED, lw=1.8)
    ax.plot([P[0], B[0]], [P[1], B[1]], color=STEEL, lw=1.0)
    body = np.radians(12)
    ax.plot([P[0] - 0.9 * np.cos(body), P[0] + 1.3 * np.cos(body)], [P[1] - 0.9 * np.sin(body), P[1] + 1.3 * np.sin(body)], color=INK, lw=3)
    ax.plot([P[0], P[0] + 3.0 * np.cos(body)], [P[1], P[1] + 3.0 * np.sin(body)], color=GRAY, lw=0.8, ls="--")
    ax.plot(*P, "o", color=INK, ms=5)
    gam = np.degrees(np.arctan2(P[1] - A[1], A[0] - P[0]))   # drawn flight-path angle
    sight = np.degrees(np.arctan2(P[1] - B[1], B[0] - P[0]))
    ax.add_patch(Arc(P, 3.4, 3.4, theta1=-gam, theta2=12, color=STEEL, lw=0.9))
    ax.add_patch(Arc(P, 5.6, 5.6, theta1=-sight, theta2=12, color=STEEL, lw=0.9))
    ax.add_patch(Arc(A, 3.0, 3.0, theta1=180 - gam, theta2=180, color=STEEL, lw=0.9))
    ax.text(P[0] + 1.9, P[1] - 0.25, r"$\alpha_{pa}$", fontsize=12, color=STEEL)
    ax.text(P[0] + 3.0, P[1] - 1.1, "view over the nose", fontsize=11, color=STEEL)
    ax.text(P[0] + 0.3, P[1] + 0.35, "body axis", fontsize=11, color=STEEL)
    ax.text(A[0] - 1.75, 0.35, r"$\gamma$ = 3.5°", fontsize=11, color=STEEL, ha="right")
    ax.text(P[0] + 2.2, P[1] - 0.95 - 0.0, "", fontsize=10)
    ax.text(3.6, 1.55, "flight path", fontsize=11, color=AGED, rotation=-gam)
    ax.plot(*B, "o", color=STEEL, ms=5)
    ax.plot(*A, "o", color=AGED, ms=5)
    ax.text(B[0], -0.15, "stern", ha="center", va="top", fontsize=11, color=STEEL)
    ax.text(A[0], -0.15, "aim point", ha="center", va="top", fontsize=11, color=STEEL)
    ax.text(0.0, -0.15, "not to scale", ha="left", va="top", fontsize=9, color=GRAY)
    ax.set_xlim(-0.2, 8.9)
    ax.set_ylim(-0.6, 3.4)
    save(fig, "fclp-approach")


# ------------------------------------------------------------ field length
def takeoff_segments():
    fig, ax = plt.subplots(figsize=(11, 3.4))
    ax.axis("off")
    ax.plot([0, 10.6], [0, 0], color=STEEL, lw=1.4)
    sg, srot, R, gam = 5.8, 0.7, 9.0, np.radians(9)
    x0 = sg + srot
    th = np.linspace(0, gam, 40)
    xt, yt = x0 + R * np.sin(th), R * (1 - np.cos(th))
    xc = np.linspace(xt[-1], xt[-1] + 2.2, 20)
    yc = yt[-1] + np.tan(gam) * (xc - xt[-1])
    ax.plot([0, sg], [0, 0], color=AGED, lw=3.5)
    ax.plot([sg, x0], [0, 0], color=DUST, lw=3.5)
    ax.plot(xt, yt, color=STEEL, lw=2.6)
    ax.plot(xc, yc, color=GRAY, lw=2.6)
    hobs = yc[-1]
    ax.plot([xc[-1], xc[-1]], [0, hobs], color=INK, lw=1.4)
    ax.text(xc[-1] + 0.08, hobs / 2, "50 ft\nobstacle", fontsize=10, color=INK, va="center")
    for x, lab in ((0, "brake\nrelease"), (sg, "$V_R$"), (x0, "$V_{LOF}$"), (xc[-1], "$V_2$")):
        ax.plot([x, x], [-0.08, 0.08], color=STEEL, lw=0.9)
        ax.text(x, -0.14, lab, ha="center", va="top", fontsize=10, color=STEEL)
    for xa, xb, lab, y in ((0, sg, "ground run $S_G$", 0.62), (sg, x0, "rotation\n$S_{ROT}$", 0.62), (x0, xt[-1], "transition $S_{TR}$\nradius $R$", 1.05), (xt[-1], xc[-1], "climb $S_C$", 1.05)):
        ax.annotate("", xy=(xb, y), xytext=(xa, y), arrowprops=dict(arrowstyle="<->", color=STEEL, lw=0.9))
        ax.text((xa + xb) / 2, y + 0.06, lab, ha="center", va="bottom", fontsize=10, color=STEEL)
    ax.text(xt[-1] - 0.9, yt[-1] + 0.02, "$h_{TR}$", fontsize=10, color=STEEL)
    ax.set_xlim(-0.4, 11.4)
    ax.set_ylim(-0.75, 1.75)
    save(fig, "takeoff-segments")


def landing_segments():
    fig, ax = plt.subplots(figsize=(11, 3.4))
    ax.axis("off")
    ax.plot([0, 10.6], [0, 0], color=STEEL, lw=1.4)
    gam = np.radians(10)
    R = 14.0
    hobs = 0.9
    hF = R * (1 - np.cos(gam))
    sF = R * np.sin(gam)
    sA = (hobs - hF) / np.tan(gam)
    xA0 = 0.3
    xF0 = xA0 + sA
    xTD = xF0 + sF
    sFR, sBR = 0.8, 3.2
    ax.plot([xA0, xA0], [0, hobs], color=INK, lw=1.4)
    ax.text(xA0 - 0.08, hobs / 2, "50 ft\nobstacle", fontsize=10, color=INK, va="center", ha="right")
    ax.plot([xA0, xF0], [hobs, hF], color=GRAY, lw=2.6)
    th = np.linspace(gam, 0, 40)
    ax.plot(xF0 + R * (np.sin(gam) - np.sin(th)), R * (1 - np.cos(th)), color=STEEL, lw=2.6)
    ax.plot([xTD, xTD + sFR], [0, 0], color=DUST, lw=3.5)
    ax.plot([xTD + sFR, xTD + sFR + sBR], [0, 0], color=AGED, lw=3.5)
    for x, lab in ((xA0, "$V_{app}$"), (xTD, "$V_{TD}$"), (xTD + sFR, "brakes on"), (xTD + sFR + sBR, "stop")):
        ax.plot([x, x], [-0.08, 0.08], color=STEEL, lw=0.9)
        ax.text(x, -0.14, lab, ha="center", va="top", fontsize=10, color=STEEL)
    for xa, xb, lab, y in ((xA0, xF0, "approach $S_A$ at $\\gamma_{app}$", 1.15), (xF0, xTD, "flare $S_F$", 0.62), (xTD, xTD + sFR, "free roll $S_{FR}$", 0.36), (xTD + sFR, xTD + sFR + sBR, "braking $S_{BR}$", 0.36)):
        ax.annotate("", xy=(xb, y), xytext=(xa, y), arrowprops=dict(arrowstyle="<->", color=STEEL, lw=0.9))
        ax.text((xa + xb) / 2, y + 0.06, lab, ha="center", va="bottom", fontsize=10, color=STEEL)
    ax.plot([xF0, xF0], [0, hF], color=STEEL, lw=0.8, ls=":")
    ax.text(xF0 - 0.08, hF / 2, "$h_F$", fontsize=10, color=STEEL, ha="right", va="center")
    ax.set_xlim(-0.9, 11.4)
    ax.set_ylim(-0.75, 1.7)
    save(fig, "landing-segments")


def sr22_field_lengths():
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.axis("off")
    rows = [("Takeoff", [(963, AGED, "ground run 963"), (119, DUST, "rotation 119"), (406, STEEL, "transition 406"), (104, "#9D9795", "climb 104")], "1,592 ft", "handbook 1,594"),
            ("Landing", [(914, STEEL, "approach 914"), (79, "#9D9795", "flare 79"), (110, DUST, "free roll 110"), (1019, AGED, "braking 1,019")], "2,122 ft", "handbook 2,344")]
    for i, (name, segs, total, hb) in enumerate(rows):
        y = 1.2 - i
        x = 0
        ax.text(-60, y, name, ha="right", va="center", fontsize=12, fontweight="bold")
        for j, (w, c, lab) in enumerate(segs):
            ax.barh(y, w, left=x, height=0.42, color=c, edgecolor="white", linewidth=1.2)
            yl = y + 0.33 if (w > 300) else (y - 0.34 if j % 2 else y + 0.33)
            ax.text(x + w / 2, yl, lab, ha="center", va="center", fontsize=9.5, color=STEEL)
            x += w
        ax.text(x + 40, y + 0.08, total, va="center", fontsize=11, fontweight="bold")
        ax.text(x + 40, y - 0.14, hb, va="center", fontsize=10, color=STEEL)
    ax.barh(-0.75, 70, left=0, height=0.18, color=AGED); ax.barh(-0.75, 70, left=80, height=0.18, color=DUST)
    ax.text(170, -0.75, "on the ground", va="center", fontsize=10, color=STEEL)
    ax.barh(-0.75, 70, left=900, height=0.18, color=STEEL); ax.barh(-0.75, 70, left=980, height=0.18, color="#9D9795")
    ax.text(1070, -0.75, "in the air", va="center", fontsize=10, color=STEEL)
    ax.text(2600, -0.75, "distances in ft", va="center", fontsize=10, color=STEEL, ha="right")
    ax.set_xlim(-500, 2650)
    ax.set_ylim(-1.0, 1.7)
    save(fig, "sr22-field-lengths")


ALL = [trailing_edge_devices, leading_edge_devices, flap_lift_curve, slot_lift_curve, increment_vs_deflection,
       flap_drag, partial_span_flaps, wing_partition, fclp_approach, takeoff_segments, landing_segments,
       sr22_field_lengths]

if __name__ == "__main__":
    for fn in ALL:
        fn()
