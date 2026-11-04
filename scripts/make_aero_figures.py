"""Figures for Lecture 5, Aerodynamics: Airfoil and Wing.

Each figure is redrawn after the figure on the lecture slide (Gudmundsson 2022;
Nicolai and Carichner 2010), reduced to the point the slide makes and set in
the book's typeface. Where the slide gives an equation the curve is computed
from it; the rest are schematics with invented, smooth curves, and the captions
say which. Run from the book folder:

    python3 scripts/make_aero_figures.py

Set FIG_PREVIEW=<folder> to also write PNG copies for checking.
"""
import os
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Ellipse

OUT = Path(__file__).resolve().parents[1] / "notes" / "lecture-05" / "figures"
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


# ------------------------------------------------------------ airfoil shapes
def naca4(m, p, t, n=200):
    x = 0.5 * (1 - np.cos(np.linspace(0, np.pi, n)))
    yt = 5 * t * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x ** 2 + 0.2843 * x ** 3 - 0.1015 * x ** 4)
    if p > 0:
        yc = np.where(x < p, m / p ** 2 * (2 * p * x - x ** 2), m / (1 - p) ** 2 * (1 - 2 * p + 2 * p * x - x ** 2))
        dyc = np.where(x < p, 2 * m / p ** 2 * (p - x), 2 * m / (1 - p) ** 2 * (p - x))
    else:
        yc, dyc = 0 * x, 0 * x
    th = np.arctan(dyc)
    return x, yc, x - yt * np.sin(th), yc + yt * np.cos(th), x + yt * np.sin(th), yc - yt * np.cos(th)


def naca230(t, n=200):
    x = 0.5 * (1 - np.cos(np.linspace(0, np.pi, n)))
    m, k1 = 0.2025, 15.957
    yc = np.where(x < m, k1 / 6 * (x ** 3 - 3 * m * x ** 2 + m ** 2 * (3 - m) * x), k1 * m ** 3 / 6 * (1 - x))
    dyc = np.where(x < m, k1 / 6 * (3 * x ** 2 - 6 * m * x + m ** 2 * (3 - m)), -k1 * m ** 3 / 6)
    yt = 5 * t * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x ** 2 + 0.2843 * x ** 3 - 0.1015 * x ** 4)
    th = np.arctan(dyc)
    return x, yc, x - yt * np.sin(th), yc + yt * np.cos(th), x + yt * np.sin(th), yc - yt * np.cos(th)


def outline(shape):
    x, yc, xu, yu, xl, yl = shape
    return np.concatenate([xu, xl[::-1]]), np.concatenate([yu, yl[::-1]])


def lift_curve(a, a0, a_stall, clmax, post=0.04, slope=0.1):
    """A schematic lift curve: linear from the zero-lift angle, rounding to a
    peak at the stall angle, then a drop."""
    x = np.clip(a - a0, 0, None)
    k = slope / clmax
    pre = clmax * np.tanh(k * x) + 0.08 * np.clip(x, 0, None) * np.exp(-((a - a0) / 6) ** 2) * 0
    pre = np.where(a < a0, slope * (a - a0), pre)
    cl_stall = clmax * np.tanh(k * (a_stall - a0))
    scale = clmax / cl_stall
    pre = pre * scale
    pre = np.where(a < a0, slope * (a - a0), pre)
    post_curve = clmax - post * (a - a_stall) ** 1.0 - 0.01 * (a - a_stall) ** 2
    return np.where(a <= a_stall, pre, post_curve)


# ------------------------------------------------------------ nomenclature
def draw_planform(ax, AR=6.0, lam=0.4, sweep_deg=25, annotate=True):
    S = 1.0
    sweep = np.radians(sweep_deg)
    b = np.sqrt(AR * S)
    cr = 2 * S / (b * (1 + lam))
    ct = lam * cr
    cmgc = 2 / 3 * cr * (1 + lam + lam ** 2) / (1 + lam)
    ymgc = b / 6 * (1 + 2 * lam) / (1 + lam)
    half = b / 2
    xle_t = half * np.tan(sweep)
    ax.set_aspect("equal")
    ax.axis("off")
    for sgn in (-1, 1):
        xs = [0, sgn * half, sgn * half, 0]
        ys = [0, -xle_t, -xle_t - ct, -cr]
        ax.plot(xs + [xs[0]], ys + [ys[0]], color=INK, lw=1.8)
        ax.plot([0, sgn * half], [-cr / 4, -xle_t - ct / 4], color=AGED, lw=1.2, ls="--")
    ax.plot([-half - 0.15, half + 0.15], [0, 0], color=STEEL, lw=0.8, ls=":")
    ax.text(-half - 0.15, 0.03, "datum", fontsize=10, color=STEEL, va="bottom")
    if not annotate:
        return
    xle_m = ymgc * np.tan(sweep)
    ax.plot([ymgc, ymgc], [-xle_m, -xle_m - cmgc], color=VERM, lw=2.6)
    ax.text(ymgc + 0.04, -xle_m - cmgc / 2, "$c_{MGC}$", color=VERM, va="center", fontsize=12)
    ax.annotate("", xy=(half, 0.2), xytext=(-half, 0.2), arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1.1))
    ax.text(0, 0.23, "$b$", ha="center", va="bottom", fontsize=13, color=STEEL)
    ax.annotate("", xy=(-0.07, 0), xytext=(-0.07, -cr), arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1.1))
    ax.text(-0.1, -cr / 2, "$c_r$", ha="right", va="center", fontsize=13, color=STEEL)
    ax.annotate("", xy=(half + 0.07, -xle_t), xytext=(half + 0.07, -xle_t - ct), arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1.1))
    ax.text(half + 0.1, -xle_t - ct / 2, "$c_t$", ha="left", va="center", fontsize=13, color=STEEL)
    ax.annotate("", xy=(ymgc, -cr - 0.12), xytext=(0, -cr - 0.12), arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1.1))
    ax.text(ymgc / 2, -cr - 0.15, "$y_{MGC}$", ha="center", va="top", fontsize=12, color=STEEL)
    ax.annotate("", xy=(ymgc + 0.25, 0), xytext=(ymgc + 0.25, -xle_m), arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1.1))
    ax.text(ymgc + 0.28, -xle_m / 2, "$x_{MGC}$", ha="left", va="center", fontsize=12, color=STEEL)
    ang = np.linspace(0, -sweep, 20)
    ax.plot(0.42 * half * np.cos(ang), 0.42 * half * np.sin(ang), color=STEEL, lw=0.9)
    ax.text(0.46 * half, -0.06, r"$\Lambda_{LE}$", fontsize=12, color=STEEL, va="top")
    ax.text(-half * 0.55, -cr - 0.2, "dashed: quarter-chord line", color=AGED, fontsize=10, ha="center", va="top")
    ax.set_xlim(-half - 0.3, half + 0.6)
    ax.set_ylim(-cr - 0.5, 0.4)


def draw_airfoil_nomenclature(ax):
    x, yc, xu, yu, xl, yl = naca4(0.04, 0.4, 0.15)
    ax.fill(*outline((x, yc, xu, yu, xl, yl)), color=LIGHT, ec=INK, lw=1.6)
    ax.plot([0, 1], [0, 0], color=STEEL, lw=0.9, ls="--")
    ax.plot(x, yc, color=VERM, lw=1.2, ls="--")
    ax.set_aspect("equal")
    ax.axis("off")
    # maximum thickness at 0.3 c, maximum camber at 0.4 c
    i = np.argmax(yu - np.interp(xu, xl, yl))
    xt = 0.30
    yt_u, yt_l = np.interp(xt, xu, yu), np.interp(xt, xl, yl)
    ax.annotate("", xy=(xt, yt_u), xytext=(xt, yt_l), arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.2))
    ax.text(xt + 0.02, yt_u + 0.02, "maximum thickness $t$", color=BLUE, fontsize=10, va="bottom")
    xm = 0.40
    ax.annotate("", xy=(xm, np.interp(xm, x, yc)), xytext=(xm, 0), arrowprops=dict(arrowstyle="<->", color=VERM, lw=1.2))
    ax.text(0.06, -0.085, "maximum camber", color=VERM, fontsize=10, va="top")
    ax.text(0.66, 0.085, "upper surface", fontsize=10, color=STEEL, rotation=-8)
    ax.text(0.64, -0.095, "lower surface", fontsize=10, color=STEEL, rotation=6)
    ax.text(0.5, 0.012, "chord line", fontsize=10, color=STEEL, va="bottom")
    ax.text(0.16, np.interp(0.16, x, yc) + 0.012, "mean camber line", fontsize=10, color=VERM, va="bottom", rotation=12)
    ax.annotate("leading edge", xy=(0, 0), xytext=(-0.02, -0.14), fontsize=10, color=STEEL, ha="left",
                arrowprops=dict(arrowstyle="-|>", color=STEEL, lw=0.9))
    ax.annotate("trailing edge", xy=(1, 0), xytext=(0.82, -0.14), fontsize=10, color=STEEL,
                arrowprops=dict(arrowstyle="-|>", color=STEEL, lw=0.9))
    ax.annotate("", xy=(1, -0.2), xytext=(0, -0.2), arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1.1))
    ax.text(0.5, -0.215, "chord $c$", ha="center", va="top", fontsize=11, color=STEEL)
    ax.set_xlim(-0.08, 1.08)
    ax.set_ylim(-0.3, 0.22)


def wing_airfoil_nomenclature():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.6), gridspec_kw=dict(width_ratios=[1.15, 1]))
    draw_planform(a1)
    a1.set_title("Wing planform", fontsize=12)
    draw_airfoil_nomenclature(a2)
    a2.set_title("Airfoil", fontsize=12)
    fig.tight_layout()
    save(fig, "wing-airfoil-nomenclature")


def wing_planform():
    fig, ax = plt.subplots(figsize=(8.5, 4.4))
    draw_planform(ax)
    ax.text(0, -ax.get_ylim()[0] * 0 + ax.get_ylim()[0] + 0.12, "$S$ is the whole planform area, both halves, to the centerline",
            ha="center", va="bottom", fontsize=11, color=STEEL)
    save(fig, "wing-planform")


def naca_families():
    fig, axes = plt.subplots(1, 3, figsize=(11, 2.9))
    items = [(naca4(0.0, 0.0, 0.12), "NACA 0012: symmetric, 12% thick"),
             (naca4(0.02, 0.4, 0.12), "NACA 2412: 2% camber at 40% chord"),
             (naca230(0.12), "NACA 23012: camber forward, at 15% chord")]
    for ax, (shape, title) in zip(axes, items):
        ax.fill(*outline(shape), color=LIGHT, ec=INK, lw=1.6)
        ax.plot(shape[0], shape[1], color=VERM, lw=1.3, ls="--")
        ax.plot([0, 1], [0, 0], color=STEEL, lw=0.6, ls=":")
        ax.set_aspect("equal")
        ax.set_xlim(-0.03, 1.03)
        ax.set_ylim(-0.17, 0.2)
        ax.axis("off")
        ax.set_title(title, fontsize=11)
    axes[0].text(0.5, -0.15, "dashed: camber line", ha="center", va="top", fontsize=10, color=VERM)
    fig.tight_layout()
    save(fig, "naca-families")


# ------------------------------------------------------------ section data
def section_data():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))
    a = np.linspace(-8, 20, 400)
    a0, amax, clmax = -2.0, 15.0, 1.5
    cl = lift_curve(a, a0, amax, clmax)
    ax1.plot(a, cl, color=BLUE, lw=2.2)
    ax1.plot([a0 - 2, 8], [-0.2, 0.1 * (8 - a0)], color=STEEL, lw=0.9, ls="--")
    ax1.axhline(0, color=STEEL, lw=0.7)
    ax1.axvline(0, color=STEEL, lw=0.7)
    ax1.plot([a0], [0], "o", color=VERM, ms=7)
    ax1.text(a0 - 0.5, -0.22, r"$\alpha_{ZL}$", color=VERM, ha="right", fontsize=12)
    ax1.plot([amax], [clmax], "o", color=VERM, ms=7)
    ax1.annotate(r"$C_{l_{max}}$ at $\alpha_{stall}$", xy=(amax, clmax), xytext=(5, 1.78), color=VERM, fontsize=12,
                 arrowprops=dict(arrowstyle="-|>", color=VERM, lw=1))
    ax1.text(4.0, 0.25, "linear range,\nslope $C_{l_\\alpha}$", color=STEEL, fontsize=11)
    ax1.set_xlabel(r"Angle of attack $\alpha$ (deg)")
    ax1.set_ylabel("Section lift coefficient $C_l$")
    ax1.set_xlim(-8, 20)
    ax1.set_ylim(-0.8, 2.0)
    clean(ax1)
    cl2 = np.linspace(-0.4, 1.6, 300)
    cd = 0.006 + 0.004 * np.clip(np.abs(cl2 - 0.3) - 0.3, 0, None) ** 1.2 * 6 + 0.011 * (cl2 - 0.3) ** 2
    ax2.plot(cd, cl2, color=BLUE, lw=2.2)
    ax2.axhspan(0.0, 0.6, xmin=0.02, xmax=0.25, color=DUST, alpha=0.7)
    ax2.text(0.0125, 0.3, "drag bucket:\nthe low-drag range", color=AGED, fontsize=11, va="center")
    ax2.plot([0.006], [0.3], "o", color=VERM, ms=7)
    ax2.annotate(r"$C_{d_{min}}$, and the $C_l$ where it occurs", xy=(0.006, 0.3), xytext=(0.009, -0.25), color=VERM, fontsize=11,
                 arrowprops=dict(arrowstyle="-|>", color=VERM, lw=1))
    ax2.set_xlabel("Section drag coefficient $C_d$")
    ax2.set_ylabel("Section lift coefficient $C_l$")
    ax2.set_xlim(0, 0.03)
    ax2.set_ylim(-0.4, 1.6)
    clean(ax2)
    fig.tight_layout()
    save(fig, "section-data")


def camber_effect():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    a = np.linspace(-10, 20, 400)
    for a0, amax, clmax, c, ls, lab in ((-4, 15, 1.6, BLUE, "-", "cambered"), (0, 14, 1.3, STEEL, "--", "symmetric")):
        ax1.plot(a, lift_curve(a, a0, amax, clmax), color=c, lw=2.2, ls=ls, label=lab)
    ax1.axhline(0, color=STEEL, lw=0.7)
    ax1.axvline(0, color=STEEL, lw=0.7)
    ax1.plot([-4], [0], "o", color=VERM, ms=6)
    ax1.text(-4.3, -0.2, r"$\alpha_{ZL}$", color=VERM, ha="right", fontsize=11)
    ax1.text(5, 1.75, "camber raises $C_{l_{max}}$\nand moves the curve left", fontsize=11, color=STEEL)
    ax1.set_xlabel(r"$\alpha$ (deg)")
    ax1.set_ylabel("$C_l$")
    ax1.set_xlim(-10, 20)
    ax1.set_ylim(-1.0, 2.1)
    ax1.legend(frameon=False, fontsize=10, loc="lower right")
    clean(ax1)
    cl = np.linspace(-0.8, 1.5, 300)
    for cl0, c, ls, lab in ((0.4, BLUE, "-", "cambered"), (0.0, STEEL, "--", "symmetric")):
        cd = 0.0065 + 0.012 * (cl - cl0) ** 2
        ax2.plot(cd, cl, color=c, lw=2.2, ls=ls, label=lab)
    ax2.text(0.013, 0.75, "the low-drag range moves\nto a higher $C_l$", fontsize=11, color=STEEL)
    ax2.set_xlabel("$C_d$")
    ax2.set_ylabel("$C_l$")
    ax2.set_xlim(0, 0.03)
    ax2.set_ylim(-1.0, 1.6)
    ax2.legend(frameon=False, fontsize=10, loc="lower right")
    clean(ax2)
    fig.tight_layout()
    save(fig, "camber-effect")


def reynolds_effect():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    a = np.linspace(-6, 22, 400)
    sets = ((12, 1.25, 0.0105, ":", "$Re_1$"), (14, 1.42, 0.0085, "--", "$Re_2$"), (16, 1.58, 0.0065, "-", "$Re_3$"))
    for amax, clmax, cdmin, ls, lab in sets:
        ax1.plot(a, lift_curve(a, -2, amax, clmax), color=BLUE, lw=2.0, ls=ls, label=lab)
    ax1.text(1, 1.8, "$Re_1 < Re_2 < Re_3$: same slope,\nhigher $C_{l_{max}}$ and $\\alpha_{stall}$", fontsize=11, color=STEEL)
    ax1.axhline(0, color=STEEL, lw=0.7)
    ax1.set_xlabel(r"$\alpha$ (deg)")
    ax1.set_ylabel("$C_l$")
    ax1.set_xlim(-6, 22)
    ax1.set_ylim(-0.5, 2.1)
    ax1.legend(frameon=False, fontsize=10, loc="lower right")
    clean(ax1)
    cl = np.linspace(-0.4, 1.5, 300)
    for amax, clmax, cdmin, ls, lab in sets:
        ax2.plot(cdmin + 0.011 * (cl - 0.3) ** 2, cl, color=BLUE, lw=2.0, ls=ls, label=lab)
    ax2.text(0.015, 0.2, "lower $C_{d_{min}}$\nat higher $Re$", fontsize=11, color=STEEL)
    ax2.set_xlabel("$C_d$")
    ax2.set_ylabel("$C_l$")
    ax2.set_xlim(0, 0.03)
    ax2.set_ylim(-0.5, 1.6)
    ax2.legend(frameon=False, fontsize=10, loc="lower right")
    clean(ax2)
    fig.tight_layout()
    save(fig, "reynolds-effect")


def stall_classes():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.6), sharey=True)
    a = np.linspace(-2, 22, 400)
    specs = [("Class A: trailing-edge stall", lambda: lift_curve(a, -2, 14, 1.5, post=0.03)),
             ("Class B: between A and C", lambda: lift_curve(a, -2, 14, 1.5, post=0.09)),
             ("Class C: leading-edge stall", lambda: np.where(a < 14, 0.1 * (a + 2) * 1.5 / 1.6, 0.9 - 0.02 * (a - 14)))]
    notes = ["separation grows forward\nfrom the trailing edge", "", "a leading-edge bubble bursts:\nsharp drop after the peak"]
    for ax, (t, f), n in zip(axes, specs, notes):
        ax.plot(a, f(), color=BLUE, lw=2.2)
        ax.set_title(t, fontsize=11)
        ax.set_xlabel(r"$\alpha$ (deg)")
        ax.set_xlim(-2, 22)
        ax.set_ylim(0, 2.0)
        if n:
            ax.text(1, 0.25, n, fontsize=10, color=STEEL)
        clean(ax)
    axes[0].set_ylabel("$C_l$")
    fig.tight_layout()
    save(fig, "stall-classes")


def mach_effects():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))
    a = np.linspace(-4, 20, 400)
    for M, amax, clmax, ls, c in ((0.2, 15, 1.5, "-", BLUE), (0.6, 14, 1.55, "--", BLUE), (0.7, 11, 1.2, "-.", VERM), (0.8, 9, 0.9, ":", VERM)):
        beta = np.sqrt(1 - M ** 2)
        ax1.plot(a, lift_curve(a, -2, amax, clmax, slope=0.1 / beta, post=0.05), color=c, lw=2.0, ls=ls, label=f"$M$ = {M}")
    ax1.text(-3.5, 1.8, "compressibility steepens the slope;\nabove $M_{crit}$ the curve changes shape", fontsize=11, color=STEEL)
    ax1.axhline(0, color=STEEL, lw=0.7)
    ax1.set_xlabel(r"$\alpha$ (deg)")
    ax1.set_ylabel("$C_l$")
    ax1.set_xlim(-4, 20)
    ax1.set_ylim(-0.3, 2.1)
    ax1.legend(frameon=False, fontsize=10, loc="lower right")
    clean(ax1)
    M = np.linspace(0.3, 0.95, 400)
    cd0 = 0.008
    cd = cd0 + np.where(M > 0.70, 0.9 * (M - 0.70) ** 3, 0) + np.where(M > 0.6, 0.004 * (M - 0.6) ** 2, 0)
    ax2.plot(M, cd, color=BLUE, lw=2.4)
    ax2.axhline(cd0, color=STEEL, lw=0.8, ls=":")
    ax2.text(0.31, cd0 + 0.0003, "incompressible level", fontsize=10, color=STEEL, va="bottom")
    mcrit = 0.78
    ax2.axvline(mcrit, color=STEEL, lw=0.8, ls="--")
    ax2.text(mcrit - 0.005, 0.0265, "$M_{crit}$: first sonic point", rotation=90, va="top", ha="right", fontsize=10, color=STEEL)
    mb = M[np.argmax(cd >= cd0 + 0.002)]
    ax2.plot([mb], [cd0 + 0.002], "o", color=VERM, ms=7)
    ax2.annotate("Boeing: $C_d$ 0.002 above\nthe incompressible level", xy=(mb, cd0 + 0.002), xytext=(0.40, 0.016),
                 fontsize=10, color=VERM, arrowprops=dict(arrowstyle="-|>", color=VERM, lw=1))
    dcd = np.gradient(cd, M)
    i = np.argmax(dcd >= 0.10)
    ax2.plot([M[i]], [cd[i]], "s", color=GREEN, ms=7)
    ax2.annotate("Douglas: $dC_d/dM = 0.10$", xy=(M[i], cd[i]), xytext=(0.44, 0.0225),
                 fontsize=10, color=GREEN, arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1))
    ax2.set_xlabel("Mach number $M$")
    ax2.set_ylabel("$C_d$")
    ax2.set_xlim(0.3, 0.95)
    ax2.set_ylim(0.005, 0.03)
    clean(ax2)
    fig.tight_layout()
    save(fig, "mach-effects")


def transonic_sketch():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.0))
    shape = naca4(0.02, 0.4, 0.14)
    ox, oy = outline(shape)
    titles = ["$M$ = 0.72: the first sonic point", "$M$ = 0.82: a supersonic region\nends in a normal shock",
              "$M$ = 1.05: bow wave ahead,\nshocks at the trailing edge"]
    for k, (ax, t) in enumerate(zip(axes, titles)):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.fill(ox, oy, color=LIGHT, ec=INK, lw=1.4)
        ax.annotate("", xy=(-0.12, 0.0), xytext=(-0.32, 0.0), arrowprops=dict(arrowstyle="-|>", color=STEEL, lw=1.4))
        ax.set_title(t, fontsize=11)
        if k == 0:
            ax.plot([0.28], [np.interp(0.28, shape[2], shape[3])], "o", color=VERM, ms=7)
            ax.text(0.33, 0.16, "local $M$ = 1", color=VERM, fontsize=10)
        if k == 1:
            xs = np.linspace(0.12, 0.55, 60)
            top = np.interp(xs, shape[2], shape[3]) + 0.16 * np.sin(np.pi * (xs - 0.12) / 0.43)
            ax.fill_between(xs, np.interp(xs, shape[2], shape[3]), top, color=SKY, alpha=0.45, lw=0)
            ax.plot([0.55, 0.55], [np.interp(0.55, shape[2], shape[3]), 0.26], color=INK, lw=2.2)
            ax.text(0.57, 0.22, "shock", fontsize=10)
            ax.text(0.14, 0.2, "supersonic", fontsize=10, color=BLUE)
            xs2 = np.linspace(0.55, 1.1, 30)
            ax.plot(xs2, np.interp(0.55, shape[2], shape[3]) + 0.02 * (xs2 - 0.55) + 0.01 * np.sin(30 * xs2), color=STEEL, lw=0.9, ls="--")
            ax.text(0.7, 0.12, "separation", fontsize=10, color=STEEL)
        if k == 2:
            th = np.linspace(-1.2, 1.2, 60)
            ax.plot(-0.07 + 0.25 * (np.cosh(th) - 1), 0.28 * np.sinh(th) * 0.9, color=INK, lw=2.2)
            ax.text(-0.3, 0.25, "bow wave", fontsize=10)
            for sgn in (1, -1):
                ax.plot([1.0, 1.22], [0, sgn * 0.22], color=INK, lw=2.0)
            ax.text(1.02, 0.25, "shock", fontsize=10)
        ax.set_xlim(-0.4, 1.35)
        ax.set_ylim(-0.32, 0.36)
    fig.tight_layout()
    save(fig, "transonic-flow")


def supercritical_sketch():
    fig, axes = plt.subplots(2, 2, figsize=(10, 5.2), gridspec_kw=dict(height_ratios=[1, 1.15]))
    x = 0.5 * (1 - np.cos(np.linspace(0, np.pi, 200)))
    yt = 5 * 0.12 * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x ** 2 + 0.2843 * x ** 3 - 0.1015 * x ** 4)
    conv = naca4(0.02, 0.4, 0.12)
    cx, cy = outline(conv)
    # supercritical: flat upper surface, aft camber on the lower surface
    yu = np.minimum(yt * 1.05, 0.062) * (1 - 0.35 * x ** 3)
    yl = -yt * 0.85 + 0.09 * x ** 3 * (1 - x) * 4
    sx, sy = np.concatenate([x, x[::-1]]), np.concatenate([yu, yl[::-1]])
    for ax, (px, py), title, xs_shock, sep in ((axes[0, 0], (cx, cy), "Conventional airfoil, $M$ = 0.72", 0.5, True),
                                              (axes[0, 1], (sx, sy), "Supercritical airfoil, $M$ = 0.80", 0.72, False)):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.fill(px, py, color=LIGHT, ec=INK, lw=1.4)
        ytop = np.interp(xs_shock, px[:200], py[:200])
        ax.plot([xs_shock, xs_shock], [ytop, ytop + (0.22 if sep else 0.12)], color=INK, lw=2.4 if sep else 1.4)
        ax.text(xs_shock + 0.02, ytop + (0.2 if sep else 0.1), "strong shock" if sep else "weak shock", fontsize=10)
        if sep:
            xs2 = np.linspace(xs_shock, 1.05, 30)
            ax.plot(xs2, ytop + 0.03 * (xs2 - xs_shock) + 0.01 * np.sin(40 * xs2), color=STEEL, lw=0.9, ls="--")
            ax.text(0.62, 0.17, "separated flow", fontsize=10, color=STEEL)
        ax.set_title(title, fontsize=11)
        ax.set_xlim(-0.05, 1.1)
        ax.set_ylim(-0.2, 0.32)
    # pressure distributions, schematic: Cp plotted upward negative
    xp = np.linspace(0, 1, 300)
    cpu_conv = -np.where(xp < 0.5, 1.1 + 0.3 * np.sqrt(xp), 1.4 - 1.1 * np.clip((xp - 0.5) / 0.08, 0, 1) - 0.3 * np.clip((xp - 0.58) / 0.42, 0, 1))
    cpl_conv = -0.2 - 0.2 * np.sqrt(xp) + 0.5 * xp ** 2
    cpu_sc = -np.where(xp < 0.72, 0.85 + 0.0 * xp, 0.85 - 0.35 * np.clip((xp - 0.72) / 0.06, 0, 1) - 0.5 * np.clip((xp - 0.78) / 0.22, 0, 1))
    cpl_sc = -0.1 - 0.3 * np.sqrt(xp) + 0.9 * xp ** 2.2
    for ax, cpu, cpl in ((axes[1, 0], cpu_conv, cpl_conv), (axes[1, 1], cpu_sc, cpl_sc)):
        ax.plot(xp, cpu, color=BLUE, lw=2.0, label="upper surface")
        ax.plot(xp, cpl, color=VERM, lw=2.0, ls="--", label="lower surface")
        ax.axhline(-0.8, color=STEEL, lw=0.8, ls=":")
        ax.text(0.01, -0.83, "$C_p$ for $M$ = 1 locally", fontsize=9, color=STEEL, va="top")
        ax.invert_yaxis()
        ax.set_xlabel("$x/c$")
        ax.set_ylabel("$C_p$")
        ax.set_xlim(0, 1)
        ax.set_ylim(1.1, -1.6)
        ax.legend(frameon=False, fontsize=9, loc="lower right")
        clean(ax)
    axes[1, 1].text(0.35, -1.45, "flat plateau, then aft loading", fontsize=10, color=STEEL)
    fig.tight_layout()
    save(fig, "supercritical-airfoil")


def drag_bucket_trio():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.4), sharey=True)
    cl = np.linspace(-0.4, 1.3, 400)
    specs = [("Undesirable: no bucket,\nhigh $C_{d_{min}}$ at a high $C_l$", 0.012 + 0.03 * (cl - 0.6) ** 2),
             ("Desirable: wide bucket,\ncruise and climb inside", 0.006 + 0.03 * np.clip(np.abs(cl - 0.4) - 0.32, 0, None) ** 2),
             ("Undesirable: narrow bucket,\ncruise and climb outside", 0.006 + 0.03 * np.clip(np.abs(cl - 0.45) - 0.06, 0, None) ** 2)]
    for ax, (t, cd) in zip(axes, specs):
        ax.plot(cl, cd, color=BLUE, lw=2.2)
        for v, lab in ((0.25, "$C_{l,cruise}$"), (0.65, "$C_{l,climb}$")):
            ax.axvline(v, color=VERM, lw=1.0, ls="--")
            ax.text(v, 0.0305, lab, color=VERM, fontsize=10, ha="center", va="top")
        ax.set_title(t, fontsize=10.5)
        ax.set_xlabel("$C_l$")
        ax.set_xlim(-0.4, 1.3)
        ax.set_ylim(0, 0.032)
        clean(ax)
    axes[0].set_ylabel("$C_d$")
    fig.tight_layout()
    save(fig, "drag-bucket")


def airfoil_comparison():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    cl = np.linspace(-0.4, 1.6, 300)
    cdA = 0.0055 + 0.03 * np.clip(np.abs(cl - 0.35) - 0.25, 0, None) ** 2 + 0.004 * (cl - 0.35) ** 2
    cdB = 0.0085 + 0.012 * (cl - 0.3) ** 2
    ax1.plot(cdA, cl, color=BLUE, lw=2.2, label="candidate A")
    ax1.plot(cdB, cl, color=VERM, lw=2.2, ls="--", label="candidate B")
    for v, lab in ((0.3, "cruise $C_l$"), (0.8, "climb $C_l$")):
        ax1.axhline(v, color=STEEL, lw=0.9, ls=":")
        ax1.text(0.0295, v + 0.03, lab, color=STEEL, fontsize=10, ha="right")
    ax1.text(0.012, -0.25, "read $C_d$ where you fly:\nat the cruise and climb $C_l$", fontsize=11, color=STEEL)
    ax1.set_xlabel("$C_d$")
    ax1.set_ylabel("$C_l$")
    ax1.set_xlim(0, 0.03)
    ax1.set_ylim(-0.4, 1.7)
    ax1.legend(frameon=False, fontsize=10, loc="upper left")
    clean(ax1)
    a = np.linspace(-6, 20, 400)
    ax2.plot(a, lift_curve(a, -2.5, 15, 1.5), color=BLUE, lw=2.2, label="candidate A")
    ax2.plot(a, lift_curve(a, -1.5, 16, 1.7, post=0.08), color=VERM, lw=2.2, ls="--", label="candidate B")
    ax2.axhline(0, color=STEEL, lw=0.7)
    ax2.text(-5, 1.85, "compare $C_{l_{max}}$ and the stall shape", fontsize=11, color=STEEL)
    ax2.set_xlabel(r"$\alpha$ (deg)")
    ax2.set_ylabel("$C_l$")
    ax2.set_xlim(-6, 20)
    ax2.set_ylim(-0.6, 2.1)
    ax2.legend(frameon=False, fontsize=10, loc="lower right")
    clean(ax2)
    fig.tight_layout()
    save(fig, "airfoil-comparison")


# ------------------------------------------------------------ wing geometry
def wing_volume_sketch():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.4), gridspec_kw=dict(width_ratios=[1, 1.5]))
    # left: a wing segment in plan
    a1.set_aspect("equal")
    a1.axis("off")
    c1, c2, dy = 1.6, 1.1, 1.4
    seg = Polygon([[0, 0], [dy, 0.15], [dy, 0.15 - c2], [0, -c1]], closed=True, fc=DUST, ec=INK, lw=1.4)
    a1.add_patch(seg)
    for sgn, x0, w in ((1, -0.9, 0.9), (1, dy, 0.9)):
        pass
    a1.plot([-0.9, 0], [0, 0], color=STEEL, lw=1.0)
    a1.plot([-0.9, 0], [-c1 - 0.0, -c1 + (0.0)], color=STEEL, lw=1.0)
    a1.plot([dy, dy + 0.9], [0.15, 0.15 + 0.1], color=STEEL, lw=1.0)
    a1.plot([dy, dy + 0.9], [0.15 - c2, 0.15 - c2 - 0.03], color=STEEL, lw=1.0)
    a1.annotate("", xy=(-0.2, 0), xytext=(-0.2, -c1), arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1.1))
    a1.text(-0.28, -c1 / 2, "$c_1$", ha="right", va="center", fontsize=12, color=STEEL)
    a1.annotate("", xy=(dy + 0.2, 0.15), xytext=(dy + 0.2, 0.15 - c2), arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1.1))
    a1.text(dy + 0.28, 0.15 - c2 / 2, "$c_2$", ha="left", va="center", fontsize=12, color=STEEL)
    a1.annotate("", xy=(dy, 0.45), xytext=(0, 0.45), arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1.1))
    a1.text(dy / 2, 0.5, r"$\Delta y$", ha="center", va="bottom", fontsize=12, color=STEEL)
    a1.text(dy / 2, -c1 * 0.55, "the volume\nbetween two stations", ha="center", va="center", fontsize=10, color=STEEL)
    a1.set_xlim(-1.1, dy + 1.1)
    a1.set_ylim(-c1 - 0.3, 0.9)
    # right: the airfoil area as a parabola plus a triangle
    a2.set_aspect("equal")
    a2.axis("off")
    k = 0.30
    shape = naca4(0.0, 0.0, 0.15)
    x, yc, xu, yu, xl, yl = shape
    a2.fill(*outline(shape), color=LIGHT, ec=INK, lw=1.5)
    mask = xu <= k
    a2.fill_between(xu[mask], yl[mask] if False else -yu[mask], yu[mask], color=DUST, alpha=0.9, lw=0)
    a2.plot([k, k], [-np.interp(k, xu, yu), np.interp(k, xu, yu)], color=INK, lw=1.2)
    a2.text(k / 2, 0.0, "$A_1$\nparabola", ha="center", va="center", fontsize=10)
    a2.text(k + (1 - k) / 2.2, 0.0, "$A_2$\ntriangle", ha="center", va="center", fontsize=10)
    a2.annotate("", xy=(k, 0.13), xytext=(0, 0.13), arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1.0))
    a2.text(k / 2, 0.14, "$k\\,c$", ha="center", va="bottom", fontsize=11, color=STEEL)
    a2.annotate("", xy=(1, 0.13), xytext=(k, 0.13), arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1.0))
    a2.text((1 + k) / 2, 0.14, "$(1-k)\\,c$", ha="center", va="bottom", fontsize=11, color=STEEL)
    a2.annotate("", xy=(k - 0.0, np.interp(k, xu, yu)), xytext=(k, -np.interp(k, xu, yu)),
                arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.1))
    a2.text(k + 0.015, 0.085, "$t$", color=BLUE, fontsize=12)
    a2.annotate("", xy=(1, -0.14), xytext=(0, -0.14), arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1.0))
    a2.text(0.5, -0.15, "$c$", ha="center", va="top", fontsize=12, color=STEEL)
    a2.set_xlim(-0.03, 1.03)
    a2.set_ylim(-0.24, 0.24)
    fig.tight_layout()
    save(fig, "wing-volume")


def cla(AR, sweep_half_deg=0.0, M=0.0, kappa=1.0):
    beta = np.sqrt(1 - M ** 2)
    t = np.tan(np.radians(sweep_half_deg))
    return 2 * np.pi * AR / (2 + np.sqrt((AR * beta / kappa) ** 2 * (1 + t ** 2 / beta ** 2) + 4))


def aspect_ratio_effects():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.3))
    a = np.linspace(0, 14, 100)
    cl = np.linspace(0, 1.4, 100)
    e, cd0 = 0.85, 0.02
    for AR, ls, c in ((4, "-", BLUE), (8, "--", VERM), (16, ":", GREEN)):
        ax1.plot(a, cla(AR) * np.radians(a), ls=ls, color=c, lw=2.2, label=f"AR = {AR}")
        ax2.plot(cd0 + cl ** 2 / (np.pi * e * AR), cl, ls=ls, color=c, lw=2.2, label=f"AR = {AR}")
    ax1.set_xlabel(r"Angle of attack $\alpha$ (deg)")
    ax1.set_ylabel("Wing lift coefficient $C_L$")
    ax1.set_title("Lift curve: the slope falls with lower AR", fontsize=11)
    ax1.legend(fontsize=10, frameon=False)
    ax2.set_xlabel("Wing drag coefficient $C_D$")
    ax2.set_ylabel("Wing lift coefficient $C_L$")
    ax2.set_title("Drag polar: induced drag rises with lower AR", fontsize=11)
    ax2.legend(fontsize=10, frameon=False, loc="lower right")
    ax1.set_xlim(0, 14)
    ax1.set_ylim(0, 1.4)
    ax2.set_xlim(0, 0.2)
    ax2.set_ylim(0, 1.4)
    clean(ax1)
    clean(ax2)
    fig.tight_layout()
    save(fig, "aspect-ratio-effects")


def schrenk(eta, lam):
    chord = (1 - (1 - lam) * eta) / ((1 + lam) / 2)        # chord / mean chord
    ell = 4 / np.pi * np.sqrt(np.clip(1 - eta ** 2, 0, None))
    return chord, 0.5 * (chord + ell)


def taper_lift_distribution():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.3))
    eta = np.linspace(0, 1, 300)
    for lam, ls, c in ((1.0, "-", BLUE), (0.6, "--", VERM), (0.2, ":", GREEN)):
        chord, L = schrenk(eta, lam)
        ax1.plot(eta, L / chord, ls=ls, color=c, lw=2.2, label=f"$\\lambda$ = {lam}")
        ax2.plot(eta, L, ls=ls, color=c, lw=2.2, label=f"$\\lambda$ = {lam}")
    ax1.text(0.02, 0.1, "tip loaded ($\\lambda$ = 0.2): the tip stalls first\nroot loaded ($\\lambda$ = 1): the root stalls first", fontsize=10, color=STEEL)
    ax1.set_xlabel("Spanwise station $2y/b$")
    ax1.set_ylabel("Section lift coefficient, wing $C_L$ = 1")
    ax1.set_title("Section lift coefficient", fontsize=11)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1.5)
    ax1.legend(frameon=False, fontsize=10, loc="lower left", bbox_to_anchor=(0.0, 0.18))
    clean(ax1)
    ax2.text(0.02, 0.1, "root loading raises the\nbending moment at the root", fontsize=10, color=STEEL)
    ax2.set_xlabel("Spanwise station $2y/b$")
    ax2.set_ylabel("Lift per unit span, normalized")
    ax2.set_title("Lift per unit span", fontsize=11)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1.6)
    ax2.legend(frameon=False, fontsize=10, loc="lower left", bbox_to_anchor=(0.0, 0.18))
    clean(ax2)
    fig.text(0.5, -0.01, "Schrenk's approximation: the mean of the planform chord and the elliptical distribution of the same area. Computed.",
             ha="center", fontsize=10, color=STEEL)
    fig.tight_layout()
    save(fig, "taper-lift-distribution")


def draw_sweep_components(ax):
    ax.set_aspect("equal")
    ax.axis("off")
    sweep = np.radians(35)
    L = 5.0
    tip = np.array([L * np.cos(sweep), -L * np.sin(sweep)])
    cr, ct = 1.7, 0.9
    panel = np.array([[0, 0], tip, tip - [0, ct], [0, -cr]])
    ax.fill(panel[:, 0], panel[:, 1], color=LIGHT, ec=INK, lw=1.5)
    A, B = np.array([0, -cr / 2]), tip - [0, ct / 2]
    ax.plot([A[0], B[0]], [A[1], B[1]], color=AGED, lw=1.4, ls="--")
    ax.text(B[0] + 0.1, B[1], "sweep line", color=AGED, fontsize=11, va="center")
    s = (B - A) / np.linalg.norm(B - A)
    n = np.array([-s[1], s[0]])
    P = A + 0.5 * (B - A)
    V = 1.8
    Vvec = np.array([0.0, -V])
    tail = P - Vvec
    ax.annotate("", xy=P, xytext=tail, arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.2, shrinkA=0, shrinkB=0))
    ax.text(tail[0] + 0.12, tail[1] - 0.1, r"$V_\infty$", fontsize=13, va="top")
    vn = (Vvec @ n) * n
    vs = (Vvec @ s) * s
    ax.annotate("", xy=tail + vn, xytext=tail, arrowprops=dict(arrowstyle="-|>", color=VERM, lw=2, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=tail + vn + vs, xytext=tail + vn, arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2, shrinkA=0, shrinkB=0))
    mid_n = tail + 0.5 * vn
    ax.text(mid_n[0] - 0.3, mid_n[1] + 0.45, r"$V_\infty\cos\Lambda$ sets the pressures", color=VERM, fontsize=11, ha="right", va="bottom")
    mid_s = tail + vn + 0.5 * vs
    ax.text(mid_s[0] - 0.15, mid_s[1] - 0.15, r"$V_\infty\sin\Lambda$", color=GREEN, fontsize=11, ha="right", va="top")
    sw_line = np.arctan2(-s[1], s[0])
    ax.plot([A[0], A[0] + 1.8], [A[1], A[1]], color=INK, lw=0.8, ls=":")
    ang = np.linspace(0, -sw_line, 20)
    ax.plot(A[0] + 1.3 * np.cos(ang), A[1] + 1.3 * np.sin(ang), color=INK, lw=0.9)
    ax.text(A[0] + 1.42, A[1] - 0.3, r"$\Lambda$", fontsize=13, color=INK)
    ax.set_xlim(-2.6, 6.2)
    ax.set_ylim(-4.2, 2.2)


def sweepback_effects():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.6), gridspec_kw=dict(width_ratios=[1.15, 1]))
    draw_sweep_components(a1)
    M = np.linspace(0.3, 3.0, 500)
    for sw, Mp, amp, w, ls, c in ((0, 1.02, 1.0, 0.07, "-", BLUE), (30, 1.17, 0.72, 0.11, "--", VERM),
                                  (45, 1.42, 0.5, 0.2, "-.", GREEN), (60, 1.95, 0.32, 0.4, ":", AGED)):
        rise = amp * np.exp(-((M - Mp) / w) ** 2) + amp * 0.35 / (1 + np.exp(-(M - Mp) / (0.6 * w + 0.05))) * np.exp(-0.25 * (M - Mp).clip(0))
        a2.plot(M, 0.1 + rise, ls=ls, color=c, lw=2.0, label=f"$\\Lambda$ = {sw}°")
    a2.set_xlabel("Mach number $M$")
    a2.set_ylabel("$C_{D_0}$, schematic")
    a2.set_title("Sweep delays the drag rise and lowers its peak", fontsize=11)
    a2.set_xlim(0.3, 3.0)
    a2.set_ylim(0, 1.3)
    a2.set_yticks([])
    a2.legend(frameon=False, fontsize=10)
    clean(a2)
    fig.tight_layout()
    save(fig, "sweepback")


def korn_sweep():
    fig, ax = plt.subplots(figsize=(8, 4.3))
    lam = np.radians(np.linspace(0, 45, 200))
    CL = 0.3
    for tc, ls, c in ((0.08, "-", BLUE), (0.10, "--", VERM), (0.12, ":", GREEN)):
        mdd = 0.87 / np.cos(lam) - tc / np.cos(lam) ** 2 - CL / (10 * np.cos(lam) ** 3)
        ax.plot(np.degrees(lam), np.where(mdd <= 1.0, mdd, np.nan), ls=ls, color=c, lw=2.2, label=f"$t/c$ = {tc:.2f}, conventional")
    mdd_sc = 0.95 / np.cos(lam) - 0.10 / np.cos(lam) ** 2 - CL / (10 * np.cos(lam) ** 3)
    ax.plot(np.degrees(lam), np.where(mdd_sc <= 1.0, mdd_sc, np.nan), color=AGED, lw=2.2, label="$t/c$ = 0.10, supercritical")
    ax.set_xlabel(r"Sweep of the mid-chord line $\Lambda$ (deg)")
    ax.set_ylabel("$M_{DD}$")
    ax.set_xlim(0, 45)
    ax.set_ylim(0.6, 1.0)
    ax.legend(fontsize=10, frameon=False, loc="upper left")
    ax.text(44, 0.62, "Korn relation at $C_L$ = 0.3; $\\kappa$ = 0.87 conventional, 0.95 supercritical", fontsize=10, color=STEEL, ha="right")
    clean(ax)
    fig.tight_layout()
    save(fig, "korn-sweep")


def pitch_up_boundary():
    fig, ax = plt.subplots(figsize=(8, 4.3))
    sw = np.linspace(0, 60, 200)
    for lam, ls, c in ((1.0, "-", BLUE), (0.5, "--", VERM), (0.3, ":", GREEN)):
        ax.plot(sw, 17.714 * (2 - lam) * np.exp(-0.04267 * sw), ls=ls, color=c, lw=2.2, label=f"$\\lambda$ = {lam}")
    ax.text(3, 1.6, "Region I: the nose drops at stall", fontsize=11, color=STEEL)
    ax.text(30, 13.5, "Region II: the nose rises at stall", fontsize=11, color=STEEL)
    ax.set_xlabel(r"Quarter-chord sweep $\Lambda_{c/4}$ (deg)")
    ax.set_ylabel("Limiting aspect ratio $AR_{lim}$")
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 20)
    ax.legend(fontsize=10, frameon=False)
    clean(ax)
    fig.tight_layout()
    save(fig, "pitch-up-boundary")


def stall_progression():
    fig, axes = plt.subplots(2, 4, figsize=(11, 4.6), gridspec_kw=dict(height_ratios=[1, 1.1]))
    eta = np.linspace(0, 1, 200)
    chord_r, L_r = schrenk(eta, 1.0)
    chord_t, L_t = schrenk(eta, 0.4)
    dists = [("Rectangular", L_r / chord_r), ("Elliptical", np.ones_like(eta)), ("Tapered", L_t / chord_t),
             ("Swept", 0.92 + 0.35 * eta ** 2)]
    for ax, (name, d) in zip(axes[0], dists):
        ax.plot(eta, d, color=BLUE, lw=2.2)
        ax.set_title(name, fontsize=11)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.5)
        ax.set_xticks([0, 0.5, 1])
        ax.set_yticks([])
        clean(ax)
    axes[0, 0].set_ylabel("section $C_l$")
    for ax in axes[0, 1:]:
        ax.set_yticklabels([])
    # planforms with the stall region shaded
    specs = [("rect", 0.0, 1.0, 0, (0.0, 0.3)), ("ellipse", 0.0, 1.0, 0, (0.0, 1.0)),
             ("taper", 0.0, 0.4, 0, (0.65, 1.0)), ("swept", 0.0, 0.55, 35, (0.65, 1.0))]
    for ax, (kind, _, lam, sweep, (s0, s1)) in zip(axes[1], specs):
        ax.set_aspect("equal")
        ax.axis("off")
        if kind == "ellipse":
            ax.add_patch(Ellipse((0, 0), 2.0, 0.55, fc=LIGHT, ec=INK, lw=1.4))
            ax.set_xlim(-0.05, 1.1)
            ax.set_ylim(-0.4, 0.4)
            ax.fill_between(np.linspace(0, 1, 100), -0.275 * np.sqrt(1 - np.linspace(0, 1, 100) ** 2) * 0.35,
                            0.275 * np.sqrt(1 - np.linspace(0, 1, 100) ** 2) * 0.35, color=VERM, alpha=0.35, lw=0)
        else:
            cr = 0.6
            ct = lam * cr
            sw = np.tan(np.radians(sweep))
            pts = np.array([[0, cr / 2], [1, cr / 2 - sw], [1, cr / 2 - sw - ct], [0, -cr / 2]])
            ax.add_patch(Polygon(pts, closed=True, fc=LIGHT, ec=INK, lw=1.4))
            xs = np.linspace(s0, s1, 50)
            top = cr / 2 - sw * xs
            bot = cr / 2 - sw * xs - (cr - (cr - ct) * xs)
            ax.fill_between(xs, bot, top, color=VERM, alpha=0.35, lw=0)
            ax.set_xlim(-0.05, 1.1)
            ax.set_ylim(-0.9, 0.5)
        ax.plot([0, 0], [-0.45, 0.45], color=STEEL, lw=0.8, ls=":")
    axes[1, 0].text(0.0, -0.75, "root stalls first", fontsize=10, color=VERM)
    axes[1, 1].text(0.0, -0.37, "whole span at once", fontsize=10, color=VERM)
    axes[1, 2].text(0.0, -0.75, "tip stalls first", fontsize=10, color=VERM)
    axes[1, 3].text(0.0, -0.85, "tip stalls first", fontsize=10, color=VERM)
    fig.text(0.5, 0.0, "Top: where the section lift coefficient peaks. Bottom: the half wing, root at the left, with the region that stalls first shaded.",
             ha="center", fontsize=10, color=STEEL)
    fig.tight_layout()
    save(fig, "stall-progression")


def wing_incidence():
    fig, axes = plt.subplots(3, 1, figsize=(8, 6.0))
    alpha = 4.0
    cases = [("Too large an incidence: the fuselage flies nose down, high fuselage drag", -4.0),
             ("Too small an incidence: the fuselage flies nose up, high fuselage drag", 5.0),
             ("Correct incidence: the fuselage follows the flight path, least drag", 0.0)]
    for ax, (title, theta) in zip(axes, cases):
        ax.set_aspect("equal")
        ax.axis("off")
        th = np.radians(theta)
        # fuselage as a rotated rounded bar
        L, H = 6.0, 0.9
        box = FancyBboxPatch((-L / 2, -H / 2), L, H, boxstyle="round,pad=0,rounding_size=0.45", fc=LIGHT, ec=INK, lw=1.4,
                             transform=matplotlib.transforms.Affine2D().rotate(th) + ax.transData)
        ax.add_patch(box)
        # wing chord at the cruise angle of attack, fixed to the flight path
        c = 2.0
        xw = -0.4
        aw = np.radians(alpha)
        ax.plot([xw - c / 2 * np.cos(aw), xw + c / 2 * np.cos(aw)], [-c / 2 * np.sin(aw), c / 2 * np.sin(aw)], color=AGED, lw=4, solid_capstyle="round")
        ax.annotate("", xy=(-3.6, 1.0), xytext=(-5.4, 1.0), arrowprops=dict(arrowstyle="-|>", color=VERM, lw=2))
        ax.text(-5.4, 1.15, "flight path", color=VERM, fontsize=10)
        ax.set_title(title, fontsize=10.5, loc="left")
        ax.set_xlim(-5.6, 4.0)
        ax.set_ylim(-1.3, 1.5)
    axes[2].text(1.6, -1.15, "wing chord at the cruise angle of attack", color=AGED, fontsize=10)
    fig.tight_layout()
    save(fig, "wing-incidence")


def critical_section():
    fig, ax = plt.subplots(figsize=(8, 4.3))
    eta = np.linspace(0, 1, 300)
    chord, L = schrenk(eta, 0.5)
    f = L / chord                       # section C_l for wing C_L = 1
    ax.axhspan(1.35, 1.45, color=DUST, alpha=0.8, lw=0)
    ax.text(0.02, 1.47, "section $C_{l_{max}}$ band", fontsize=10, color=AGED)
    CL3 = 1.42 / f.max()
    for CL, ls, lab in ((0.72 * CL3, ":", r"$\alpha_1$"), (0.86 * CL3, "--", r"$\alpha_2$"), (CL3, "-", r"$\alpha_3$: the stall")):
        ax.plot(eta, CL * f, color=BLUE, lw=2.0, ls=ls, label=lab)
    top = CL3 * f
    i = np.argmax(top >= 1.40)
    ax.plot([eta[i]], [top[i]], "o", color=VERM, ms=8)
    ax.annotate("critical section: the first\nto reach its $C_{l_{max}}$", xy=(eta[i], top[i]), xytext=(0.52, 0.6), fontsize=11, color=VERM,
                arrowprops=dict(arrowstyle="-|>", color=VERM, lw=1))
    ax.set_xlabel("Spanwise station $2y/b$")
    ax.set_ylabel("Section lift coefficient $C_l$")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.7)
    ax.text(0.02, 0.1, "raise the angle of attack until one section reaches its $C_{l_{max}}$", fontsize=10, color=STEEL)
    ax.legend(frameon=False, fontsize=10, loc="lower left", bbox_to_anchor=(0.0, 0.14))
    clean(ax)
    fig.tight_layout()
    save(fig, "critical-section")


def lift_curve_slope():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    AR = np.linspace(0.5, 16, 200)
    ax.axhline(2 * np.pi, color=STEEL, lw=0.9)
    ax.text(15.8, 2 * np.pi + 0.08, "airfoil, $2\\pi$", ha="right", va="bottom", fontsize=11, color=STEEL)
    for sw, ls, c in ((0, "-", INK), (30, "--", AGED), (45, ":", STEEL)):
        ax.plot(AR, cla(AR, sw), ls=ls, color=c, lw=2.2, label=f"$\\Lambda_{{c/2}}$ = {sw}°")
    ax.set_xlabel("Aspect ratio")
    ax.set_ylabel(r"$C_{L_\alpha}$, per rad")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 7)
    ax.set_xticks([0, 4, 8, 12, 16])
    ax.legend(fontsize=10, frameon=False, loc="lower right")
    clean(ax)
    fig.tight_layout()
    save(fig, "lift-curve-slope")


def stall_speed():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ws = np.linspace(5, 120, 300)
    rho = 0.002377
    for clmax, ls, c in ((1.2, "-", BLUE), (1.6, "--", VERM), (2.0, "-.", GREEN), (2.4, ":", AGED)):
        ax.plot(ws, np.sqrt(2 * ws / (rho * clmax)) / 1.6878, ls=ls, color=c, lw=2.2, label=f"$C_{{L_{{max}}}}$ = {clmax}")
    ax.axhline(61, color=STEEL, lw=1.0, ls="--")
    ax.text(118, 63, "61 kt: former Part 23 single-engine limit", fontsize=10, color=STEEL, ha="right")
    ax.axhline(45, color=STEEL, lw=1.0, ls=":")
    ax.text(118, 47, "45 kt: light-sport limit", fontsize=10, color=STEEL, ha="right")
    ax.set_xlabel("Wing loading $W/S$ (lb/ft²)")
    ax.set_ylabel("Stall speed $V_S$ (KEAS)")
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 200)
    ax.legend(fontsize=10, frameon=False, loc="upper left")
    ax.text(118, 8, "sea level, standard day", fontsize=10, color=STEEL, ha="right")
    clean(ax)
    fig.tight_layout()
    save(fig, "stall-speed")


def wing_height():
    fig, axes = plt.subplots(1, 2, figsize=(8, 2.8))
    for ax, hw, title in zip(axes, (0.36, -0.36), ("High wing", "Low wing")):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.plot([-2.1, 2.1], [-0.95, -0.95], color=STEEL, lw=1.2)
        ax.add_patch(plt.Circle((0, 0), 0.45, fc=DUST, ec=AGED, lw=1.5))
        ax.plot([-1.7, 1.7], [hw, hw], color=AGED, lw=4)
        ax.plot([-0.06, -0.02, 0.06, 0.06], [0.44, 1.0, 1.0, 0.44], color=AGED, lw=1.5)
        ax.annotate("", xy=(1.95, hw), xytext=(1.95, -0.95), arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1))
        ax.text(2.05, (hw - 0.95) / 2, "$h$", fontsize=12, color=STEEL, va="center")
        ax.set_xlim(-2.3, 2.5)
        ax.set_ylim(-1.1, 1.2)
        ax.set_title(title, fontsize=12)
    fig.tight_layout()
    save(fig, "wing-height")


ALL = [wing_airfoil_nomenclature, wing_planform, naca_families, section_data, camber_effect, reynolds_effect,
       stall_classes, mach_effects, transonic_sketch, supercritical_sketch, drag_bucket_trio, airfoil_comparison,
       wing_volume_sketch, aspect_ratio_effects, taper_lift_distribution, sweepback_effects, korn_sweep,
       pitch_up_boundary, stall_progression, wing_incidence, critical_section, lift_curve_slope, stall_speed,
       wing_height]

if __name__ == "__main__":
    for fn in ALL:
        fn()
