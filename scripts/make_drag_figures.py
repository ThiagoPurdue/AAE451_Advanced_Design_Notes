"""Figures for Lecture 7, Drag Prediction.

Each figure is redrawn after the figure on the lecture slide (Gudmundsson 2022,
Chapters 8, 9, and 16; Nicolai and Carichner 2010, Chapters 2 and 5; Silva et
al. 2021), reduced to the point the slide makes and set in the book's typeface.
Curves come from the published equations where they exist: skin friction,
transition, the induced drag factor by lifting-line theory, ground effect, the
compressibility spline, and the SR22 polar. The rest are schematic. Run from
the book folder:

    python3 scripts/make_drag_figures.py

Set FIG_PREVIEW=<folder> to also write PNG copies for checking.
"""
import os
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Arc, PathPatch
from matplotlib.path import Path as MPath

OUT = Path(__file__).resolve().parents[1] / "notes" / "lecture-07" / "figures"
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


def arrow(ax, x0, x1, y, color=STEEL):
    ax.annotate("", xy=(x1, y), xytext=(x0, y), arrowprops=dict(arrowstyle="<->", color=color, lw=1.0))


# ------------------------------------------------------------ part 1, parasite
def polar_types():
    """After Nicolai Fig. 2.16: C_D = C_Dmin + K''(C_L - C_Lmin)^2 + K' C_L^2."""
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    cl = np.linspace(0, 1.0, 200)
    cdmin, clmin, kv, ki = 0.0125, 0.27, 0.02, 0.0407
    visc = cdmin + kv * (cl - clmin) ** 2
    total = visc + ki * cl ** 2
    ax.plot(total, cl, color=INK, lw=2.2, label="total $C_D$")
    ax.plot(visc, cl, color=BLUE, lw=2.0, ls="--", label="without the induced drag")
    y = 0.8
    v = cdmin + kv * (y - clmin) ** 2
    t = v + ki * y ** 2
    arrow(ax, 0, cdmin, y)
    arrow(ax, cdmin, v, y)
    arrow(ax, v, t, y)
    ax.text(cdmin / 2, y + 0.02, "$C_{D_{min}}$", ha="center", va="bottom", fontsize=11, color=STEEL)
    ax.text((cdmin + v) / 2, y + 0.02, "viscous", ha="center", va="bottom", fontsize=10, color=STEEL)
    ax.text((v + t) / 2, y + 0.02, "induced", ha="center", va="bottom", fontsize=11, color=STEEL)
    ax.plot([cdmin], [clmin], "o", color=BLUE, ms=6)
    ax.annotate("", xy=(cdmin, clmin), xytext=(0, clmin), arrowprops=dict(arrowstyle="->", color=STEEL, lw=1.0))
    ax.text(0.0175, clmin, "$C_{L}$ of minimum drag", fontsize=10.5, color=STEEL, va="center")
    ax.set_xlabel("Drag coefficient $C_D$")
    ax.set_ylabel("Lift coefficient $C_L$")
    ax.set_xlim(0, 0.07)
    ax.set_ylim(0, 1.0)
    ax.legend(frameon=False, fontsize=10.5, loc="lower right")
    clean(ax)
    fig.tight_layout()
    save(fig, "polar-types")


def drag_components():
    fig, ax = plt.subplots(figsize=(7.4, 3.3))
    ax.set_aspect("equal")
    ax.axis("off")
    body = dict(fc="#C9DCEE", ec=INK, lw=1.2)
    wing = dict(fc=DUST, ec=INK, lw=1.2)
    ax.add_patch(Polygon([(0, 0), (2.0, 0.55), (2.0, -0.55)], closed=True, fc=LIGHT, ec=INK, lw=1.2))
    ax.add_patch(Polygon([(2.2, 0.6), (7.2, 0.6), (7.2, -0.6), (2.2, -0.6)], closed=True, **body))
    for s in (1, -1):
        ax.add_patch(Polygon([(3.8, s * 0.7), (5.4, s * 0.7), (5.4, s * 2.0), (4.9, s * 2.0)], closed=True, **wing))
        ax.add_patch(Polygon([(6.3, s * 0.7), (7.2, s * 0.7), (7.2, s * 1.4), (6.8, s * 1.4)], closed=True, **wing))
        ax.text(4.85, s * 1.2, "$S_{wing}$", ha="center", va="center", fontsize=11)
        ax.text(6.92, s * 0.98, "$S_{tail}$", ha="center", va="center", fontsize=11)
    ax.text(1.35, 0, "$S_{nose}$", ha="center", va="center", fontsize=11)
    ax.text(4.7, 0, "$S_{fuselage}$", ha="center", va="center", fontsize=11)
    ax.set_xlim(-0.2, 7.5)
    ax.set_ylim(-2.2, 2.2)
    save(fig, "drag-components")


def cf_turb(re, m=0.0):
    return 0.455 / (np.log10(re) ** 2.58 * (1 + 0.144 * m ** 2) ** 0.65)


def cf_lam(re):
    return 1.328 / np.sqrt(re)


def skin_friction():
    fig, ax = plt.subplots(figsize=(7.8, 4.6))
    re = np.logspace(4, 9, 300)
    trans = np.logspace(np.log10(5.26e5), 9, 200)
    lam = np.logspace(4, np.log10(5e6), 200)
    ax.loglog(re, cf_turb(re), color=INK, lw=2.2, label="turbulent")
    ax.loglog(re, cf_turb(re, 0.8), color=BLUE, lw=2.0, ls="--", label="turbulent, Mach 0.8")
    ax.loglog(lam, cf_lam(lam), color=VERM, lw=2.2, ls="-.", label="laminar")
    mix = cf_turb(trans) - 1700 / trans
    ax.loglog(trans, mix, color=GREEN, lw=2.0, ls=":", label="transition, $-1700/Re$")
    ax.axvline(5e5, color=STEEL, lw=0.8)
    ax.text(5.6e5, 1.35e-4, "$Re_x = 5\\times10^{5}$", fontsize=10.5, color=STEEL)
    ax.set_xlabel("Reynolds number $Re$")
    ax.set_ylabel("Skin friction coefficient $C_f$")
    ax.set_xlim(1e4, 1e9)
    ax.set_ylim(1e-4, 2e-2)
    ax.legend(frameon=False, fontsize=10.5, loc="upper right")
    ax.grid(True, which="major", color="#DDDDDD", lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    save(fig, "skin-friction")


def transition():
    """Young's method, Gudmundsson Eqs. 16-69 and 16-70, at Re = 2e6."""
    re = 2e6
    x = np.linspace(0, 1, 200)
    x0 = 36.9 * x ** 0.625 * (1 / re) ** 0.375
    mixed = 0.074 / re ** 0.2 * (1 - (x - x0)) ** 0.8
    assert abs(cf_lam(re) - 0.00094) < 2e-5 and abs(cf_turb(re) - 0.00394) < 2e-5
    assert abs(mixed[-1] - cf_lam(re)) / cf_lam(re) < 0.02, "mixed flow must end near laminar"
    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    ax.plot(x, mixed, color=GREEN, lw=2.2, label="mixed, Young's method")
    ax.axhline(cf_turb(re), color=INK, lw=2.0, ls="--", label="fully turbulent")
    ax.axhline(cf_lam(re), color=VERM, lw=2.0, ls="-.", label="fully laminar")
    ax.set_xlabel("Transition point $x_{tr}/c$")
    ax.set_ylabel("Skin friction coefficient $C_f$")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.005)
    ax.text(0.98, 0.00458, "$Re = 2\\times10^{6}$", ha="right", fontsize=10.5, color=STEEL)
    ax.legend(frameon=False, fontsize=10.5, loc="lower left", bbox_to_anchor=(0.0, 0.24))
    clean(ax)
    fig.tight_layout()
    save(fig, "transition")


def interference():
    fig, axes = plt.subplots(3, 4, figsize=(9.6, 5.6))
    line = dict(color=AGED, lw=3.0, solid_capstyle="butt")
    body = dict(fc=DUST, ec=AGED, lw=1.4)

    def wing(ax, y, fillet=False):
        ax.add_patch(Circle((0, 0), 0.45, **body))
        ax.plot([-1.4, 1.4], [y, y], **line)
        if fillet:
            for s in (1, -1):
                ax.add_patch(Polygon([(s * 0.3, y), (s * 0.8, y), (s * 0.42, y + 0.24)], closed=True, color=AGED))

    def tail(ax, kind):
        ax.add_patch(Circle((0, 0), 0.3, **body))
        if kind == "conv":
            ax.plot([0, 0], [0.28, 1.0], **line)
            ax.plot([-0.9, 0.9], [0.12, 0.12], **line)
        elif kind == "tee":
            ax.plot([0, 0], [0.28, 1.0], **line)
            ax.plot([-0.9, 0.9], [1.0, 1.0], **line)
        elif kind == "vee":
            ax.plot([0, -0.85], [0.25, 0.95], **line)
            ax.plot([0, 0.85], [0.25, 0.95], **line)
        else:
            ax.plot([-0.9, 0.9], [0.12, 0.12], **line)
            ax.plot([-0.9, -0.9], [-0.28, 0.65], **line)
            ax.plot([0.9, 0.9], [-0.28, 0.65], **line)

    def nacelle(ax, gap):
        ax.plot([-1.4, 1.4], [0.95, 0.95], **line)
        ax.add_patch(Circle((0, 0.95 - 0.32 - gap), 0.32, fc=LIGHT, ec=STEEL, lw=1.4))

    rows = [
        ("Wing on\nfuselage", [(lambda a: wing(a, 0.36), "High", "1.0"), (lambda a: wing(a, 0), "Mid", "1.0"),
                               (lambda a: wing(a, -0.36, True), "Low, filleted", "1.0"),
                               (lambda a: wing(a, -0.36), "Low, no fillet", "1.2")]),
        ("Tail", [(lambda a: tail(a, "conv"), "Conventional", "1.04 to 1.05"), (lambda a: tail(a, "tee"), "T-tail", "1.04 to 1.05"),
                  (lambda a: tail(a, "vee"), "V-tail", "1.03"), (lambda a: tail(a, "aitch"), "H-tail", "1.08")]),
        ("Nacelle", [(lambda a: nacelle(a, 0), "Attached", "1.5"), (lambda a: nacelle(a, 0.22), "Within one diameter", "1.3"),
                     (lambda a: nacelle(a, 0.75), "Beyond one diameter", "1.0"), None]),
    ]
    for r, (name, cells) in enumerate(rows):
        for c in range(4):
            ax = axes[r, c]
            ax.set_aspect("equal")
            ax.axis("off")
            ax.set_xlim(-1.5, 1.5)
            ax.set_ylim(-1.15, 1.15)
            if cells[c] is None:
                continue
            draw, lab, q = cells[c]
            draw(ax)
            ax.text(0, -0.82, lab, ha="center", va="center", fontsize=11)
            ax.text(0, -1.22, f"$Q$ = {q}", ha="center", va="center", fontsize=11, fontweight="bold")
        axes[r, 0].text(-1.75, 0.1, name, ha="right", va="center", fontsize=12, fontweight="bold")
    fig.subplots_adjust(left=0.13, right=0.99, top=0.99, bottom=0.03, hspace=0.18, wspace=0.05)
    save(fig, "interference")


def upsweep():
    fig, ax = plt.subplots(figsize=(6.6, 1.9))
    ax.set_aspect("equal")
    ax.axis("off")
    u = np.degrees(np.arctan(0.72 / 2.0))
    verts = [(0, 0.35), (0.25, 0.80), (0.7, 0.95), (1.3, 0.95), (5.6, 0.95), (5.6, 0.72), (3.6, 0), (0.7, 0), (0.35, 0.02), (0.1, 0.15), (0, 0.35)]
    codes = [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4, MPath.LINETO, MPath.LINETO, MPath.LINETO, MPath.LINETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4]
    ax.add_patch(PathPatch(MPath(verts, codes), fc=DUST, ec=AGED, lw=1.6))
    ax.plot([3.6, 6.0], [0, 0], color=STEEL, lw=0.9, ls="--")
    ax.add_patch(Arc((3.6, 0), 3.2, 3.2, theta1=0, theta2=u, color=STEEL, lw=1.0))
    ax.text(5.33, 0.22, "$u$", fontsize=12, color=STEEL, va="center")
    ax.set_xlim(-0.1, 6.2)
    ax.set_ylim(-0.1, 1.05)
    save(fig, "upsweep")


SR22_F = [("Wing", 1.14), ("Fuselage", 0.72), ("Main gear", 0.45), ("Windscreen", 0.45), ("Leakage and protuberance", 0.27),
          ("Horizontal tail", 0.23), ("Nose gear", 0.18), ("Engine cooling", 0.15), ("Vertical tail", 0.14), ("Engine installation", 0.06)]
SR22_S, SR22_W, SR22_Q, SR22_AR = 144.9, 2750.0, 91.6, 10.0  # AR as in Gudmundsson, Example 9-4


def sr22_buildup():
    f = sum(v for _, v in SR22_F)
    assert abs(f - 3.79) < 1e-9 and abs(f / SR22_S - 0.0262) < 5e-5
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    y = np.arange(len(SR22_F))
    v = [b for _, b in SR22_F]
    ax.barh(y, v, color=AGED, height=0.62)
    for yi, vi in zip(y, v):
        ax.text(vi + 0.015, yi, f"{vi:.2f}", va="center", fontsize=11)
    ax.set_yticks(y)
    ax.set_yticklabels([n for n, _ in SR22_F])
    ax.invert_yaxis()
    ax.set_xlim(0, 1.3)
    ax.set_xlabel("Flat-plate area $f$ (ft²)")
    ax.tick_params(axis="y", length=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    save(fig, "sr22-buildup")


# -------------------------------------------------------- part 2, lift and polar
def lifting_line_delta(ar, lam, n=30):
    """Induced drag factor of an unswept, untwisted wing, lifting-line theory."""
    th = (np.arange(1, n + 1) - 0.5) * np.pi / (2 * n)
    odd = 2 * np.arange(n) + 1
    cr_b = 2 / (ar * (1 + lam))
    c_b = cr_b * (1 - (1 - lam) * np.abs(np.cos(th)))
    mu = 2 * np.pi * c_b / 4
    A = np.array([[np.sin(k * t) * (np.sin(t) + k * m) for k in odd] for t, m in zip(th, mu)])
    a = np.linalg.solve(A, mu * np.sin(th))
    return float(np.sum(odd[1:] * (a[1:] / a[0]) ** 2))


def induced_factor():
    lam = np.linspace(0.02, 1.0, 60)
    # read from Gudmundsson Figure 9-75 at taper 1
    assert abs(lifting_line_delta(4, 1.0) - 0.028) < 0.006
    assert abs(lifting_line_delta(8, 1.0) - 0.068) < 0.008
    fig, ax = plt.subplots(figsize=(7.8, 4.4))
    styles = [(4, "-", INK), (8, "--", BLUE), (12, "-.", VERM), (16, ":", GREEN)]
    for ar, ls, c in styles:
        d = [lifting_line_delta(ar, x) for x in lam]
        ax.plot(lam, d, ls=ls, color=c, lw=2.2, label=f"$AR$ = {ar}")
    ax.set_xlabel(r"Taper ratio $\lambda$")
    ax.set_ylabel(r"Induced drag factor $\delta$")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.22)
    ax.legend(frameon=False, fontsize=10.5, loc="upper center")
    clean(ax)
    fig.tight_layout()
    save(fig, "induced-factor")


def sr22_polar():
    cd0 = sum(v for _, v in SR22_F) / SR22_S
    e = 1.78 * (1 - 0.045 * SR22_AR ** 0.68) - 0.64
    k = 1 / (np.pi * SR22_AR * e)
    cl_c = SR22_W / (SR22_Q * SR22_S)
    cd_c = cd0 + k * cl_c ** 2
    cl_b = np.sqrt(cd0 / k)
    ldmax = 1 / (2 * np.sqrt(cd0 * k))
    assert abs(e - 0.757) < 0.001 and abs(k - 0.0421) < 1e-4 and abs(cl_c - 0.207) < 1e-3
    assert abs(cd_c - 0.0280) < 1e-4 and abs(cd_c * SR22_Q * SR22_S - 371) < 0.5
    assert abs(cl_c / cd_c - 7.4) < 0.05 and abs(cl_b - 0.79) < 0.01 and abs(ldmax - 15.1) < 0.05
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    cl = np.linspace(0, 1.25, 200)
    ax.plot(cd0 + k * cl ** 2, cl, color=INK, lw=2.2)
    x = np.array([0, 2 * cd0 + 0.034])
    ax.plot(x, ldmax * x, color=AGED, lw=1.5, ls="--")
    ax.plot([cd_c], [cl_c], "o", color=AGED, ms=8)
    ax.plot([2 * cd0], [cl_b], "o", color=AGED, ms=8)
    ax.text(cd_c + 0.0025, cl_c - 0.02, "cruise at 313 ft/s, $L/D$ = 7.4", fontsize=11, color=STEEL, va="center")
    ax.text(2 * cd0 + 0.003, cl_b - 0.05, f"$(L/D)_{{max}}$ = {ldmax:.1f}", fontsize=11, color=STEEL, va="center")
    ax.set_xlabel("Drag coefficient $C_D$")
    ax.set_ylabel("Lift coefficient $C_L$")
    ax.set_xlim(0, 0.09)
    ax.set_ylim(0, 1.3)
    clean(ax)
    fig.tight_layout()
    save(fig, "sr22-polar")


def polar_break():
    """After Nicolai Fig. 2.17, with K = 0.169."""
    cd0, k, clb = 0.024, 0.169, 0.5
    cl = np.linspace(0, 0.84, 200)
    par = cd0 + k * cl ** 2
    act = par + 0.67 * np.clip(cl - clb, 0, None) ** 2
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.plot(act, cl, color=INK, lw=2.2, label="with separation")
    ax.plot(par, cl, color=BLUE, lw=2.0, ls="--", label="parabolic")
    y = 0.75
    px, ax_ = cd0 + k * y ** 2, cd0 + k * y ** 2 + 0.67 * (y - clb) ** 2
    arrow(ax, px, ax_, y)
    ax.text(0.14, 0.71, "separation adds drag", ha="left", va="top", fontsize=10.5, color=STEEL)
    xb = cd0 + k * clb ** 2
    ax.annotate("", xy=(0, clb), xytext=(xb, clb), arrowprops=dict(arrowstyle="->", color=STEEL, lw=1.0))
    ax.text(xb / 2, clb + 0.015, "break $C_L$", ha="center", va="bottom", fontsize=11, color=STEEL)
    ax.set_xlabel("Drag coefficient $C_D$")
    ax.set_ylabel("Lift coefficient $C_L$")
    ax.set_xlim(0, 0.24)
    ax.set_ylim(0, 1.0)
    ax.legend(frameon=False, fontsize=10.5, loc="lower right")
    clean(ax)
    fig.tight_layout()
    save(fig, "polar-break")


def ground_effect():
    hb = np.linspace(0.005, 1.5, 400)
    phi_d = 33 * hb ** 1.5 / (1 + 33 * hb ** 1.5)
    assert abs(33 * 0.5 ** 1.5 / (1 + 33 * 0.5 ** 1.5) - 0.921) < 0.002
    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    ax.plot(hb, phi_d, color=INK, lw=2.2, label=r"$\Phi_D$, Hoerner")
    ax.plot([0, 0.5], [1.05, 1.05], color=BLUE, lw=2.2, ls="--", label=r"$\Phi_L$")
    ax.plot([0.5, 1.5], [1.0, 1.0], color=BLUE, lw=2.2, ls="--")
    ax.set_xlabel("Height above the ground $h/b$")
    ax.set_ylabel(r"Ground influence coefficient $\Phi$")
    ax.set_xlim(0, 1.5)
    ax.set_ylim(0, 1.2)
    ax.legend(frameon=False, fontsize=10.5, loc="lower right")
    clean(ax)
    fig.tight_layout()
    save(fig, "ground-effect")


def spline(m, mcrit, mmaxd, dcd):
    a = np.arctanh(1 - 0.0002 / dcd)
    A = 2 * a / (mmaxd - mcrit)
    B = -a - A * mcrit
    return dcd / 2 * (1 + np.tanh(A * m + B))


def compressibility():
    # the wing rows of Gudmundsson Table 16-9, with invented M_crit values
    wings = [("straight", 0.70, 1.10, 0.055, "-", INK), (r"$\Lambda_{c/4}$ = 34°", 0.76, 1.25, 0.030, "--", BLUE),
             (r"$\Lambda_{c/4}$ = 45°", 0.82, 1.65, 0.020, "-.", VERM)]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2))
    for lab, mc, mm, dc, ls, c in wings:
        m = np.linspace(0.4, mm, 400)
        a1.plot(m, spline(m, mc, mm, dc), ls=ls, color=c, lw=2.2, label=lab)
        a1.plot([mm], [dc], "o", color=c, ms=6)
        a2.plot(m, spline(m, mc, mm, dc), ls=ls, color=c, lw=2.2)
        a2.plot([mc], [spline(mc, mc, mm, dc)], "o", color=c, ms=6)
    a1.set_xlim(0.4, 1.8)
    a1.set_ylim(0, 0.06)
    a1.set_ylabel("Compressibility drag $C_{D_c}$")
    a1.set_xlabel("Mach number")
    a1.legend(frameon=False, fontsize=10.5, loc="upper right")
    a2.set_xlim(0.6, 1.0)
    a2.set_ylim(0, 0.004)
    a2.set_xlabel("Mach number")
    a2.set_ylabel("Compressibility drag $C_{D_c}$")
    a2.set_title("The start of the rise; the dots mark $M_{crit}$", fontsize=11)
    clean(a1)
    clean(a2)
    fig.tight_layout()
    save(fig, "compressibility")


def flap_polar():
    """Section polar, flap up and down, after Gudmundsson Fig. 8-59."""
    up = np.linspace(-1.1, 1.55, 300)
    dn = np.linspace(-0.8, 1.85, 300)
    cd_up = 0.004 + np.where(up < 0.05, 0.036 * np.abs(up - 0.05) ** 2.4, 0.0218 * np.abs(up - 0.05) ** 3.76)
    cd_dn = 0.016 + 0.0247 * np.abs(dn - 0.40) ** 3.24
    fig, ax = plt.subplots(figsize=(7.8, 4.6))
    ax.plot(up, cd_up, color=BLUE, lw=2.2, label="flap up")
    ax.plot(dn, cd_dn, color=VERM, lw=2.2, ls="--", label="flap down")
    ax.plot([0.97], [0.020], "o", color=STEEL, ms=6)
    ax.annotate("crossover", xy=(0.97, 0.020), xytext=(1.14, 0.009), fontsize=10.5, color=STEEL,
                arrowprops=dict(arrowstyle="-", color=STEEL, lw=0.8), va="center")
    ax.text(0.40, 0.0185, "higher $C_{d_{min}}$", ha="center", va="bottom", fontsize=10.5, color=VERM)
    ax.set_xlabel("Section lift coefficient $C_l$")
    ax.set_ylabel("Section drag coefficient $C_d$")
    ax.set_xlim(-1.25, 2.0)
    ax.set_ylim(0, 0.11)
    ax.legend(frameon=False, fontsize=10.5, loc="upper center")
    clean(ax)
    fig.tight_layout()
    save(fig, "flap-polar")


def ldmax_vs_ar():
    """Subsonic lines read from Nicolai Fig. 5.3."""
    lines = [(10, 21.97, 22.57), (8, 18.44, 19.04), (6, 15.61, 16.21), (4, 12.46, 13.06), (3, 10.58, 11.19), (2, 8.83, 9.44)]
    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    for ar, y0, y1 in lines:
        ax.plot([0.10, 0.91], [y0, y1], color=BLUE, lw=2.0)
        ax.text(0.93, y1, f"$AR$ = {ar}", va="center", fontsize=10.5, color=BLUE)
    for name, m, ld, ha, dy in (("U-2S", 0.71, 24.6, "right", 0.0), ("L-1011", 0.83, 17.3, "right", 0.0), ("F-16C", 0.83, 11.45, "right", -1.2)):
        ax.plot([m], [ld], "o", color=INK, ms=7)
        ax.text(m - 0.025, ld + dy, name, ha=ha, va="center", fontsize=10.5)
    ax.set_xlabel("Mach number")
    ax.set_ylabel("$(L/D)_{max}$")
    ax.set_xlim(0, 1.1)
    ax.set_ylim(0, 28)
    clean(ax)
    fig.tight_layout()
    save(fig, "ldmax-vs-ar")


def solver_compare():
    """Silva et al. (2021): end points from Table 1, C_D between them read from Fig. 17b."""
    alpha = np.arange(0, 6)
    cl_ends = {"MDO code": (0.0628, 0.5752), "XFLR5": (0.0533, 0.5692), "OpenVSP": (0.0595, 0.5692)}
    cd = {"MDO code": [0.0067, 0.0073, 0.0086, 0.0104, 0.0128, 0.0158],
          "XFLR5": [0.0081, 0.0079, 0.0084, 0.0097, 0.0115, 0.0140],
          "OpenVSP": [0.0071, 0.0074, 0.0082, 0.0095, 0.0113, 0.0134]}
    assert abs(max(v[-1] for v in cd.values()) / min(v[-1] for v in cd.values()) - 1.18) < 0.005
    assert abs(0.5752 / 0.5692 - 1) < 0.011
    styles = {"MDO code": ("-", INK), "XFLR5": ("--", BLUE), "OpenVSP": ("-.", VERM)}
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.9))
    for k, (ls, c) in styles.items():
        a1.plot([0, 5], cl_ends[k], ls=ls, color=c, lw=2.0, label=k)
        a2.plot(alpha, cd[k], ls=ls, color=c, lw=2.0, label=k)
    a1.set_ylabel("$C_L$")
    a2.set_ylabel("$C_D$")
    a1.set_ylim(0, 0.65)
    a2.set_ylim(0.006, 0.016)
    for a in (a1, a2):
        a.set_xlabel(r"Angle of attack $\alpha$ (deg)")
        a.set_xlim(0, 5)
        a.legend(frameon=False, fontsize=10.5, loc="upper left")
        clean(a)
    fig.tight_layout()
    save(fig, "solver-compare")


ALL = [polar_types, drag_components, skin_friction, transition, interference, upsweep, sr22_buildup,
       induced_factor, sr22_polar, polar_break, ground_effect, compressibility, flap_polar, ldmax_vs_ar, solver_compare]

if __name__ == "__main__":
    for fn in ALL:
        fn()
