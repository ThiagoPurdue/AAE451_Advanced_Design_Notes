"""Figures for Lecture 10, Stability and Control.

The lecture slides draw every figure natively. The computed figures here use the
slides' invented inputs and assert the point each figure makes before drawing:
the CG loop inside the limits, the scissor lines and the cut, the trim diagram,
the trimmed polar. The Cirrus SR22 envelope uses its published points and the
real-aircraft pitch stiffness the values of Gudmundsson (2022), Table 24-2. The
three report figures (Team Draco 2025, Figures 49 and 52; University of Liege 2025,
Figure 7.1) are redrawn from values read off the report pages. The schematics share
one side view, top view and rear view of a tandem-seat jet trainer. Run from the book folder:

    python3 scripts/make_stability_figures.py

Set FIG_PREVIEW=<folder> to also write PNG copies for checking.
"""
import math
import os
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyBboxPatch, Circle, Rectangle

OUT = Path(__file__).resolve().parents[1] / "notes" / "lecture-10" / "figures"
PREVIEW = os.environ.get("FIG_PREVIEW")
DEG = 180.0 / math.pi

plt.rcParams.update({
    "svg.fonttype": "none", "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"], "font.size": 12,
    "axes.titlesize": 12, "axes.labelsize": 12, "axes.edgecolor": "#000000",
    "axes.labelcolor": "#000000", "xtick.color": "#000000", "ytick.color": "#000000",
    "savefig.facecolor": "white",
})
INK, STEEL, GRAY = "#000000", "#555960", "#6F727B"
DUST, LIGHT, BODY = "#EBD99F", "#F5EFDC", "#D9DCE1"
BLUE, VERM, GREEN, PURPLE = "#0072B2", "#D55E00", "#009E73", "#AA4499"
ARROW = dict(arrowstyle="-|>", lw=1.8)
DIM = dict(arrowstyle="<->", color=STEEL, lw=1.0)


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


def sketch(figsize):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def arrow(ax, p0, p1, color=INK, **kw):
    ax.annotate("", xy=p1, xytext=p0, arrowprops=dict(color=color, **{**ARROW, **kw}))


# ---------------------------------------------------- invented inputs of the slides
X_AC, CLA_W, CLA_T, ETA_H, DEPS = 0.25, 5.0, 4.0, 0.90, 0.35
L_T, SM = 3.0, 0.10
K_TAIL = ETA_H * (1 - DEPS) * CLA_T / CLA_W
CM0_CLEAN, CL_MAX, ALPHA_STALL = -0.05, 1.6, 15.0 / DEG
CM0_FLAP, CL_ROT, CLT_UP, CM_REQ_ROT = -0.20, 1.5, -0.70, 0.15
CM0_LAND, CL_APP = -0.30, 1.2
R_SEL = 0.20


def r_stability(x, sm):
    a = x - X_AC + sm
    return a / (K_TAIL * (L_T - a))


def r_control(x, cm0, cl_w, cl_t, cm_req):
    return (cm0 + cl_w * (x - X_AC) - cm_req) / (cl_t * ETA_H * (L_T - (x - X_AC)))


def r_recovery(x):
    return r_control(x, CM0_CLEAN, CL_MAX, CLA_T * ALPHA_STALL, -CL_MAX * SM + CM0_CLEAN)


def r_rotation(x):
    return r_control(x, CM0_FLAP, CL_ROT, CLT_UP, CM_REQ_ROT)


def r_approach(x):
    return r_control(x, CM0_LAND, CL_APP, CLT_UP, 0.0)


def solve(f, target, lo, hi):
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if (f(lo) - target) * (f(mid) - target) <= 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def cg_limits():
    fwd = max(solve(r_rotation, R_SEL, 0.05, 0.40), solve(r_approach, R_SEL, 0.05, 0.40))
    aft_sm = solve(lambda v: r_stability(v, SM), R_SEL, 0.25, 0.70)
    aft = min(aft_sm, solve(r_recovery, R_SEL, 0.25, 0.70))
    assert fwd < aft and r_recovery(aft_sm) < R_SEL          # the chosen-SM line sets the aft limit
    assert abs(fwd - 0.230) < 0.002 and abs(aft - 0.407) < 0.002
    return fwd, aft


def cg_loop():
    items = {"empty": (0.56, 0.34), "crew": (0.04, -0.60), "payload": (0.18, 0.65), "fuel": (0.22, 0.30)}

    def cg(keys):
        w = sum(items[k][0] for k in keys)
        return sum(items[k][0] * items[k][1] for k in keys) / w, w

    a = [cg(p) for p in (["empty"], ["empty", "crew"], ["empty", "crew", "payload"],
                         ["empty", "crew", "payload", "fuel"])]
    b = [cg(p) for p in (["empty", "crew"], ["empty", "crew", "fuel"], ["empty", "crew", "fuel", "payload"])]
    fwd, aft = cg_limits()
    xs = [p[0] for p in a + b]
    assert fwd + 0.02 < min(xs) and max(xs) < aft - 0.02      # the loop lies inside the limits with margin
    return a, b


# ------------------------------------------------------------------ part 1, the CG
def method_flow():
    fig, ax = plt.subplots(figsize=(10.4, 3.6))
    ax.axis("off")
    steps = [("1 CG table, envelope", "every loading\nthe RFP implies"), ("2 Scissor plot", "$S_t/S$, forward\nand aft limits"),
             ("3 Tail geometry", r"$AR_t$, $\lambda_t$, $\Lambda_t$, $i_t$"), ("4 Trim", r"$\alpha$, $\delta_e$, trim drag" + "\nat every condition"),
             ("5 Vertical tail", r"$V_v$, $C_{n\beta}$," + "\nengine out, crosswind"), ("6 Dihedral", r"$C_{\ell\beta}$ from $\Gamma$," + "\nsweep, wing height"),
             ("7 Control surfaces", "elevator, rudder,\nailerons; the system"), ("8 Check", "vortex lattice;\nthree-view")]
    pos = [(i * 2.6, 2.2) for i in range(4)] + [((3 - i) * 2.6, 0.0) for i in range(4)]
    for (title, sub), (x, y) in zip(steps, pos):
        ax.add_patch(FancyBboxPatch((x, y), 2.25, 1.35, boxstyle="round,pad=0.02,rounding_size=0.08",
                                    fc=DUST if title[0] in "12" else LIGHT, ec=STEEL, lw=1.0))
        ax.text(x + 1.125, y + 1.05, title, ha="center", va="center", fontsize=10.5, fontweight="bold")
        ax.text(x + 1.125, y + 0.48, sub, ha="center", va="center", fontsize=10)
    for i in range(3):
        arrow(ax, (pos[i][0] + 2.27, 2.875), (pos[i + 1][0] - 0.02, 2.875), STEEL, lw=1.2)
        arrow(ax, (pos[4 + i][0] - 0.02, 0.675), (pos[5 + i][0] + 2.27, 0.675), STEEL, lw=1.2)
    arrow(ax, (pos[3][0] + 1.125, 2.18), (pos[4][0] + 1.125, 1.37), STEEL, lw=1.2)
    ax.plot([pos[7][0] - 0.02, -0.45, -0.45], [0.675, 0.675, 2.875], color=STEEL, lw=1.2, ls="--")
    arrow(ax, (-0.45, 2.875), (-0.02, 2.875), STEEL, lw=1.2, ls="--")
    ax.text(-0.62, 1.78, "iterate: layout, masses, polar", rotation=90, ha="center", va="center", fontsize=10)
    ax.set_xlim(-0.9, 10.2)
    ax.set_ylim(-0.1, 3.7)
    save(fig, "method-flow")


def _side_view(ax, x0=0.0, y0=0.0, s=1.0, nose_up=0.0, prop=False, de=0.0, tail=True, wing_y=-0.28, z=2):
    """Side view of a tandem-seat jet trainer, nose to the left, length 10 s. Returns the page
    position of named points. prop=True draws a spinner and propeller disc at the nose (the
    single-engine example of the textbook); de deflects the elevator, trailing edge down positive."""
    T = lambda pts: _tf(pts, x0, y0, s, nose_up)
    fus = [(0.0, 0.0), (0.12, 0.22), (0.6, 0.34)] + FUS_SIDE[2:-2] + [(0.6, -0.30), (0.12, -0.2)] if prop else FUS_SIDE
    if tail:
        fin = [(7.3, 0.52), (8.85, 2.0), (9.4, 2.0), (9.8, 0.34)]
        ax.add_patch(Polygon(T(fin), closed=True, fc=LIGHT, ec=INK, lw=0.9, zorder=z))
    ax.add_patch(Polygon(T(_smooth(fus)), closed=True, fc=FUS_FILL, ec=STEEL, lw=1.2, zorder=z + 0.1))
    ax.add_patch(Polygon(T(_smooth(CANOPY, closed=False)), closed=True, fc=CANOPY_FILL, ec=STEEL, lw=1.0, zorder=z + 0.2))
    ax.plot(*T([(3.55, 0.56), (3.62, 0.94)]).T, color=STEEL, lw=0.9, zorder=z + 0.3)
    if not prop:
        ax.add_patch(Polygon(T([(9.8, 0.26), (10.05, 0.24), (10.05, -0.08), (9.8, -0.1)]), closed=True, fc="#9AA0A8", ec=STEEL, lw=0.8, zorder=z + 0.2))
        ax.add_patch(Polygon(T([(4.25, 0.32), (4.95, 0.32), (5.1, 0.18), (5.1, -0.02), (4.95, -0.12), (4.25, -0.12)]), closed=True,
                             fc="#C3C8CF", ec=STEEL, lw=0.8, zorder=z + 0.2))
    else:
        ax.add_patch(Polygon(T(_smooth([(-0.35, 0.0), (-0.2, 0.12), (0.05, 0.2), (0.05, -0.2), (-0.2, -0.12)])), closed=True,
                             fc="#B8BDC4", ec=STEEL, lw=0.9, zorder=z + 0.3))
        ax.plot(*T([(0.0, -1.15), (0.0, 1.15)]).T, color=STEEL, lw=2.2, solid_capstyle="round", zorder=z + 0.25)
    ax.add_patch(Polygon(T(_naca(3.75, 2.9, wing_y, t=0.11)), closed=True, fc=LIGHT, ec=INK, lw=0.9, zorder=z + 0.4))
    pts = {"nose": T([(0, 0)])[0], "wing_ac": T([(3.75 + 0.25 * 2.9, wing_y + 0.05)])[0], "fin_top": T([(9.2, 1.95)])[0],
           "tail_ac": T([(8.2 + 0.25 * 1.45, 0.14)])[0], "disc_top": T([(0, 1.15)])[0], "tail_end": T([(10.05, 0.1)])[0]}
    if tail:
        ax.add_patch(Polygon(T(_naca(8.2, 1.0, 0.14, t=0.13, m=0)), closed=True, fc=LIGHT, ec=INK, lw=0.9, zorder=z + 0.5))
        hinge = np.array([9.15, 0.14])
        el = _naca(9.15, 0.7, 0.14, t=0.08, m=0)
        th = math.radians(-de)
        el = hinge + (el - hinge) @ np.array([[math.cos(th), math.sin(th)], [-math.sin(th), math.cos(th)]])
        ax.add_patch(Polygon(T(el), closed=True, fc=VERM if de else LIGHT, ec=INK, lw=0.9, zorder=z + 0.6))
        pts["hinge"] = T([hinge])[0]
        pts["el_te"] = T([hinge + 0.7 * np.array([math.cos(math.radians(-de)), math.sin(math.radians(-de))])])[0]
    return pts


def cg_table_sketch():
    """Each item of the weight statement at its own x from a datum ahead of the nose, laid out
    as on a jet trainer: crew forward, fuel at the wing, engine aft."""
    fig, ax = sketch((9.4, 4.4))
    pts = _side_view(ax, 0.0, 0.0, 1.0)
    for shape, name in (([(5.6, 0.42), (7.1, 0.42), (7.1, -0.05), (5.6, -0.05)], "fuel tank"),
                        ([(7.3, 0.36), (9.6, 0.30), (9.6, -0.08), (7.3, -0.14)], "engine")):
        ax.add_patch(Polygon(shape, closed=True, fc="none", ec=STEEL, lw=1.0, ls=(0, (3, 2)), zorder=4))
    datum = -0.9
    ax.plot([datum, datum], [-2.35, 2.2], color=STEEL, lw=1.2)
    ax.text(datum, -2.45, "datum", ha="center", va="top", fontsize=11)
    arrow(ax, (datum, -2.1), (10.9, -2.1), STEEL, lw=1.0, arrowstyle="->")
    ax.text(11.0, -2.1, "$x$", va="center", fontsize=12)
    items = ((3.6, 0.6, "$W_{crew}$", -0.95), (4.6, 0.05, "$W_{fus}$", -1.55), (5.2, -0.3, "$W_{wing}$", -0.95),
             (6.35, 0.2, "$W_{fuel}$", -1.55), (8.4, 0.1, "$W_{eng}$", -0.95), (9.1, 0.18, "$W_{ht}$", -1.55))
    for x, y, name, lvl in items:
        ax.add_patch(Circle((x, y), 0.07, fc=BLUE, ec="white", lw=0.8, zorder=6))
        arrow(ax, (x, y), (x, lvl + 0.08), BLUE, lw=1.4)
        ax.text(x, lvl, name, ha="center", va="top", fontsize=11.5)
    ax.add_patch(Circle((9.3, 1.25), 0.07, fc=BLUE, ec="white", lw=0.8, zorder=6))
    arrow(ax, (9.3, 1.25), (9.3, 0.72), BLUE, lw=1.4)
    ax.text(9.55, 1.3, "$W_{vt}$", ha="left", va="center", fontsize=11.5)
    ax.annotate("", xy=(5.2, 1.75), xytext=(datum, 1.75), arrowprops=DIM)
    ax.plot([5.2, 5.2], [-0.3, 1.75], color=STEEL, lw=0.8, ls=":")
    ax.text((datum + 5.2) / 2, 1.83, "$x_{wing}$", ha="center", va="bottom", fontsize=11.5)
    ax.set_xlim(datum - 0.5, 11.4)
    ax.set_ylim(-2.9, 2.4)
    save(fig, "cg-table-sketch")


def _loop(ax, a, b, labels=True):
    ax.plot(*zip(*a), color=INK, lw=1.8, marker="o", ms=5)
    ax.plot(*zip(*b), color=BLUE, lw=1.8, ls="-.", marker="s", ms=5)
    if labels:
        for (x, w), name, dx, dy in zip(a, "abcd", (0.006, -0.008, 0.006, 0.0), (-0.012, 0.0, -0.012, 0.022)):
            ax.text(x + dx, w + dy, name, ha="left" if dx > 0 else ("right" if dx < 0 else "center"), va="center", fontsize=11)
        ax.text(b[1][0] + 0.006, b[1][1], "e", ha="left", va="center", fontsize=11)


def cg_envelope():
    a, b = cg_loop()
    fwd, aft = cg_limits()
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    for x, name in ((fwd, "forward limit"), (aft, "aft limit")):
        ax.plot([x, x], [0.5, 1.04], color=VERM, lw=1.6, ls="--")
        ax.text(x, 1.05, name, ha="center", va="bottom", fontsize=10.5)
    _loop(ax, a, b)
    ax.set_xlabel(r"CG position $\bar{x}_{cg}$")
    ax.set_ylabel("$W/W_{TO}$")
    ax.set_xlim(0.15, 0.47)
    ax.set_ylim(0.5, 1.10)
    clean(ax)
    fig.tight_layout()
    save(fig, "cg-envelope")


def sr22_envelope():
    fwd, aft = [(137.8, 2100), (139.1, 2700), (142.3, 3400)], [(148.1, 3400), (148.1, 2100)]
    mac = (148.1 - 137.8) / (0.315 - 0.098)
    le = 137.8 - 0.098 * mac
    assert abs(le + 0.125 * mac - 139.1) < 0.2 and abs(le + 0.192 * mac - 142.3) < 0.2   # the published pairs agree
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    ax.add_patch(Polygon(fwd + aft, closed=True, fc=DUST, ec=INK, lw=1.8))
    for (x, w), t, ha in zip(fwd + [(148.1, 2750)], ("9.8% MAC", "12.5%", "19.2%", "31.5% MAC"), ("right", "right", "right", "left")):
        ax.text(x + (0.25 if ha == "left" else -0.25), w, t, ha=ha, va="center", fontsize=10.5)
    ax.text(139.6, 3480, "forward limit", ha="center", va="bottom", fontsize=10.5)
    ax.text(148.1, 3480, "aft limit", ha="center", va="bottom", fontsize=10.5)
    ax.set_xlabel("CG (in aft of the datum)")
    ax.set_ylabel("Weight (lb)")
    ax.set_xlim(134.5, 151.5)
    ax.set_ylim(2000, 3650)
    ax.set_yticks(range(2000, 3601, 400))
    ax.set_yticklabels([f"{t:,}" for t in range(2000, 3601, 400)])
    clean(ax)
    fig.tight_layout()
    save(fig, "sr22-envelope")


# --------------------------------------------------- part 2, longitudinal stability
def cm_components():
    vh, eps0, i_t, dx = 0.80, 0.03, -0.02, 0.10
    comp = {"wing alone": (-0.05, CLA_W * dx), "fuselage alone": (0.02, 0.40), "propulsion alone": (-0.02, 0.20),
            "tail alone": (ETA_H * vh * CLA_T * (eps0 - i_t), -ETA_H * vh * CLA_T * (1 - DEPS))}
    cm0, cma = sum(v[0] for v in comp.values()), sum(v[1] for v in comp.values())
    a_trim = -cm0 / cma * DEG
    assert all(comp[k][1] > 0 for k in list(comp)[:3]) and comp["tail alone"][1] < 0 and cma < 0 and cm0 > 0
    assert 5 < a_trim < 12
    al = np.linspace(-2, 14, 50)
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    for (name, (c0, ca)), color, ls in zip(comp.items(), (BLUE, STEEL, GREEN, VERM), ("--", ":", "-.", "-")):
        ax.plot(al, c0 + ca * al / DEG, color=color, lw=1.8, ls=ls)
        ax.text(14.3, c0 + ca * 14 / DEG, name, fontsize=10.5, va="center")
    ax.plot(al, cm0 + cma * al / DEG, color=INK, lw=2.6)
    ax.text(14.3, cm0 + cma * 14 / DEG, "complete aircraft", fontsize=10.5, va="center", fontweight="bold")
    ax.plot([a_trim], [0], "o", color=INK, ms=7)
    ax.text(a_trim + 0.4, -0.035, r"trim, $\alpha_{trim}$", fontsize=10.5, va="top")
    ax.axhline(0, color=GRAY, lw=0.8)
    ax.set_xlabel(r"Angle of attack $\alpha$ (deg)")
    ax.set_ylabel("$C_{M,cg}$")
    ax.set_xlim(-2, 14)
    ax.set_ylim(-0.4, 0.3)
    clean(ax)
    fig.tight_layout()
    save(fig, "cm-components")


def _airfoil(ax, x0, x1, y, t, **kw):
    xs = np.linspace(0, 1, 40)
    yt = t * (x1 - x0) * 2.2 * (0.2969 * np.sqrt(xs) - 0.126 * xs - 0.3516 * xs ** 2 + 0.2843 * xs ** 3 - 0.1036 * xs ** 4)
    xx = x0 + (x1 - x0) * xs
    ax.add_patch(Polygon(list(zip(xx, y + yt * 1.4)) + list(zip(xx[::-1], y - yt[::-1] * 0.5)), closed=True, **kw))


def moment_about_cg():
    """Wing and tail sections with their lifts, the weight at the CG, and the two section
    moments drawn in the positive, nose-up sense (nose to the left: clockwise)."""
    fig, ax = sketch((9.4, 4.4))
    ax.add_patch(Polygon(_naca(-1.5, 3.0, 0.0, t=0.12, m=0.03), closed=True, fc=LIGHT, ec=INK, lw=1.1, zorder=3))
    ax.add_patch(Polygon(_naca(5.9, 1.3, 0.25, t=0.10, m=0.0), closed=True, fc=LIGHT, ec=INK, lw=1.1, zorder=3))
    ac, cg, tac = (-0.75, 0.06), (-0.2, 0.06), (6.225, 0.25)
    for p in (ac, tac):
        ax.add_patch(Circle(p, 0.06, fc=INK, ec=INK, zorder=5))
    ax.add_patch(Circle(cg, 0.085, fc=VERM, ec="white", lw=0.8, zorder=6))
    arrow(ax, ac, (ac[0], 1.8), BLUE)
    arrow(ax, tac, (tac[0], 1.45), BLUE)
    arrow(ax, cg, (cg[0], -1.25), VERM)
    ax.text(ac[0] + 0.12, 1.6, "$L^{W}$", fontsize=12.5, va="center")
    ax.text(tac[0] + 0.12, 1.3, "$L^{T}$", fontsize=12.5, va="center")
    ax.text(cg[0] + 0.14, -1.1, "$W$", fontsize=12.5, va="center")
    ax.text(cg[0] + 0.08, 0.42, "CG", fontsize=11, ha="left", va="bottom")
    ax.text(ac[0] - 0.1, 0.42, "AC", fontsize=11, ha="right", va="bottom")
    # nose-up positive: clockwise with the nose to the left, drawn below each aerodynamic center
    _arc(ax, ac, 0.55, 320, 220, color=STEEL, lw=1.4)
    ax.text(-1.95, -0.55, "$M_{ac}^{W}$", fontsize=12, ha="center", va="center")
    _arc(ax, tac, 0.42, 320, 220, color=STEEL, lw=1.4)
    ax.text(6.225, -0.45, "$M_{ac}^{T}$", fontsize=12, ha="center", va="center")
    arrow(ax, (-3.9, 0.06), (-2.2, 0.06), STEEL, lw=1.5)
    ax.text(-3.05, 0.2, "$V$", fontsize=12.5, ha="center", va="bottom")
    ax.annotate("", xy=(tac[0], 2.15), xytext=(ac[0], 2.15), arrowprops=DIM)
    ax.text((ac[0] + tac[0]) / 2, 2.25, "$l_t$ (wing AC to tail AC)", ha="center", va="bottom", fontsize=11)
    for x1, y, name in ((ac[0], -1.65, "$x_{ac}$"), (cg[0], -2.2, "$x_{cg}$")):
        ax.annotate("", xy=(x1, y), xytext=(-1.5, y), arrowprops=DIM)
        ax.text((x1 - 1.5) / 2, y - 0.08, name, ha="center", va="top", fontsize=11.5)
        ax.plot([x1, x1], [-1.3 if x1 == cg[0] else -0.2, y], color=STEEL, lw=0.8, ls=":")
    ax.plot([-1.5, -1.5], [-0.05, -2.2], color=STEEL, lw=0.8, ls=":")
    for x, y0 in ((ac[0], 1.8), (tac[0], 1.45)):
        ax.plot([x, x], [y0, 2.15], color=STEEL, lw=0.8, ls=":")
    ax.text(3.0, -1.55, "positive moments: nose up", fontsize=10.5, ha="center", va="center", color=STEEL)
    ax.set_xlim(-4.1, 7.6)
    ax.set_ylim(-2.8, 2.7)
    save(fig, "moment-about-cg")


def static_margin_lines():
    assert abs(0.10 / 0.21 - 0.476) < 0.001
    cl = np.linspace(0, 1, 20)
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    for sm, color, ls in ((0.21, INK, "-"), (0.14, BLUE, "--"), (0.07, GREEN, "-."), (0.0, VERM, ":")):
        ax.plot(cl, 0.10 - sm * cl, color=color, lw=2.0, ls=ls)
        ax.text(1.02, 0.10 - sm, f"$SM$ = {sm:.2f}" if sm else r"$SM$ = 0, CG at $\bar{x}_n$", fontsize=10.5, va="center")
    ax.plot([0.476], [0], "o", color=INK, ms=7)
    ax.text(0.46, -0.012, "$C_{L,trim}$", fontsize=10.5, ha="right", va="top")
    ax.text(0.02, 0.107, "$C_{M0}$", fontsize=10.5, va="bottom")
    ax.axhline(0, color=GRAY, lw=0.8)
    ax.set_xlabel("$C_L$")
    ax.set_ylabel("$C_{M,cg}$")
    ax.set_xlim(0, 1.32)
    ax.set_xticks([0, 0.5, 1.0])
    ax.set_ylim(-0.15, 0.15)
    clean(ax)
    fig.tight_layout()
    save(fig, "static-margin-lines")


def cma_by_class():
    """Values of Gudmundsson (2022), Table 24-2: 22 of its 28 rows (the power-approach rows
    omitted). One label per aircraft, with a thin leader to each of its points; the points of
    one aircraft are not joined (the table gives no values between them)."""
    real = [("BD-5A", 0.27, -0.830), ("Beech 18", 0.23, -1.748), ("Bonanza", 0.23, -0.455), ("727-100", 0.76, -1.500),
            ("727-100", 0.60, -1.672), ("747", 0.30, -1.216), ("747", 0.60, -0.685), ("747", 0.80, -0.630),
            ("Cessna 182", 0.14, -0.900), ("CV-880", 0.60, -0.522), ("CV-880", 0.80, -0.650), ("DHC-6", 0.22, -1.200),
            ("A-4", 0.40, -0.380), ("A-4", 0.80, -0.410), ("F-104", 0.80, -0.901), ("F-104", 2.00, -0.736),
            ("Jetstar", 0.60, -0.663), ("Jetstar", 0.80, -0.717), ("F-4", 0.60, -0.279), ("F-4", 2.00, -0.606),
            ("Navion", 0.16, -0.683), ("Salto", 0.06, -1.206)]
    assert len(real) == 22
    assert all(-1.0 <= c <= -0.6 for n, m, c in real if n in ("Cessna 182", "Navion", "BD-5A", "Jetstar", "F-104"))
    assert -1.7 <= dict((n, c) for n, m, c in real)["Salto"] <= -1.2
    fig, ax = plt.subplots(figsize=(9.2, 5.4))
    ax.axhspan(-1.0, -0.6, color=DUST, lw=0)
    ax.axhspan(-1.7, -1.2, color="#E3E6EA", lw=0)
    ax.text(1.015, (0.8 / 2.05), "general aviation\nand business,\n−0.6 to −1.0", transform=ax.transAxes, fontsize=10, va="center")
    ax.text(1.015, (2.05 - 1.45) / 2.05, "transports,\n−1.2 to −1.7", transform=ax.transAxes, fontsize=10, va="center")
    ax.plot([r[1] for r in real], [r[2] for r in real], "o", color=INK, ms=6, zorder=5)
    # every point carries its aircraft's name: next to the point, or in a stack with a leader where
    # the points crowd at Mach 0.6 and 0.8
    near = {("F-4", 0.6): (0, 10, "center"), ("F-4", 2.0): (0, 10, "center"), ("F-104", 2.0): (0, -11, "center"),
            ("F-104", 0.8): (8, 0, "left"), ("A-4", 0.4): (0, 10, "center"), ("A-4", 0.8): (8, 0, "left"),
            ("727-100", 0.76): (8, 0, "left"), ("727-100", 0.6): (8, 0, "left"), ("747", 0.3): (8, 0, "left"),
            ("DHC-6", 0.22): (-8, 0, "right"), ("Salto", 0.06): (8, 0, "left"), ("Beech 18", 0.23): (0, -11, "center"),
            ("Bonanza", 0.23): (0, 10, "center"), ("Navion", 0.16): (8, 0, "left"), ("Cessna 182", 0.14): (-8, 0, "right"),
            ("BD-5A", 0.27): (8, 0, "left")}
    stack = {("CV-880", 0.6): (0.50, -0.50), ("Jetstar", 0.6): (0.50, -0.615), ("747", 0.6): (0.50, -0.73),
             ("747", 0.8): (0.95, -0.55), ("CV-880", 0.8): (0.95, -0.645), ("Jetstar", 0.8): (0.95, -0.74)}
    assert len(near) + len(stack) == len(real)
    for n, m, c in real:
        if (n, m) in near:
            dx, dy, ha = near[(n, m)]
            ax.annotate(n, xy=(m, c), xytext=(dx, dy), textcoords="offset points", fontsize=10, ha=ha, va="center")
        else:
            lx, ly = stack[(n, m)]
            ha = "right" if lx < m else "left"
            ax.text(lx, ly, n, fontsize=10, ha=ha, va="center")
            ax.plot([lx * (1.02 if ha == "right" else 0.98), m * (0.975 if ha == "right" else 1.025)], [ly, c], color=GRAY, lw=0.7)
    ax.set_xscale("log")
    ax.set_xlim(0.05, 2.6)
    ax.set_xticks([0.1, 0.2, 0.5, 1, 2])
    ax.set_xticklabels(["0.1", "0.2", "0.5", "1", "2"])
    ax.set_ylim(-2.05, 0)
    ax.set_xlabel("Mach number")
    ax.set_ylabel(r"$C_{M\alpha}$ (per rad)")
    clean(ax)
    fig.tight_layout()
    save(fig, "cma-by-class")


def _scissor_lines(ax, x, which=("1", "2", "3", "4", "np")):
    spec = {"1": (r_stability(x, SM), INK, "-", 2.4), "2": (r_recovery(x), STEEL, ":", 2.2),
            "3": (r_rotation(x), BLUE, "-.", 1.8), "4": (r_approach(x), GREEN, "--", 1.8),
            "np": (r_stability(x, 0.0), VERM, (0, (6, 2)), 1.4)}
    for k in which:
        y, color, ls, lw = spec[k]
        ax.plot(x, y, color=color, ls=ls, lw=lw)
    return np.maximum.reduce([spec[k][0] for k in which if k != "np"])


def scissor_plot():
    assert r_stability(0.55, SM) > r_stability(0.35, SM) > 0 and r_rotation(0.15) > r_rotation(0.35) > 0
    assert r_rotation(0.25) > r_approach(0.25) + 0.02 and r_stability(0.45, 0.0) < r_stability(0.45, SM)
    x34 = solve(lambda v: r_rotation(v) - r_approach(v), 0.0, 0.2, 0.6)
    assert abs(x34 - 0.417) < 0.001 and abs(r_rotation(x34) - 0.056) < 0.001     # lines 3 and 4 cross below the cut
    fwd, aft = cg_limits()
    x = np.linspace(0.05, 0.65, 300)
    fig, ax = plt.subplots(figsize=(9.0, 4.9))
    floor = _scissor_lines(ax, x, which=("1", "2", "3", "4"))
    xn = x[x <= 0.52]
    ax.plot(xn, r_stability(xn, 0.0), color=VERM, ls=(0, (6, 2)), lw=1.4)
    ax.fill_between(x, np.minimum(floor, 0.55), 0.55, color=DUST, lw=0, zorder=0)
    ax.plot([fwd, aft], [R_SEL, R_SEL], color=VERM, lw=3.2, marker="o", ms=7, zorder=5)
    ax.text((fwd + aft) / 2, R_SEL + 0.012, "selected $S_t/S$", fontsize=10.5, ha="center", va="bottom", color=INK)
    ax.annotate("forward limit", xy=(fwd, R_SEL + 0.008), xytext=(0.14, 0.43), fontsize=10.5, ha="center",
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    ax.annotate("aft limit", xy=(aft, R_SEL + 0.008), xytext=(0.36, 0.33), fontsize=10.5, ha="center",
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    ax.text(0.5, 0.47, "feasible", fontsize=12, fontweight="bold", ha="center")
    ax.text(0.655, r_stability(0.65, SM), "1  stability,\n    chosen $SM$", fontsize=10.5, va="center")
    ax.text(0.655, r_recovery(0.65), "2  stall recovery", fontsize=10.5, va="center")
    ax.text(0.07, r_rotation(0.07) + 0.03, "3  takeoff rotation", fontsize=10.5, va="bottom")
    ax.text(0.055, 0.18, "4  landing approach", fontsize=10.5, va="top")
    ax.annotate("neutral point,\n$SM$ = 0", xy=(0.47, r_stability(0.47, 0.0)), xytext=(0.53, 0.02), fontsize=10.5,
                va="bottom", arrowprops=dict(arrowstyle="-", color=VERM, lw=0.8))
    ax.set_xlabel(r"CG position $\bar{x}_{cg}$")
    ax.set_ylabel("Tail area ratio $S_t/S$")
    ax.set_xlim(0.05, 0.65)
    ax.set_ylim(0, 0.55)
    clean(ax)
    fig.tight_layout()
    save(fig, "scissor-plot")


def scissor_and_envelope():
    """As the slide: three lines (takeoff rotation, stability at the chosen SM, stall recovery)
    and the cut above; the loading loop below; the two limits dropped through both."""
    a, b = cg_loop()
    fwd, aft = cg_limits()
    x = np.linspace(0.15, 0.5, 200)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(8.0, 6.6), sharex=True, gridspec_kw=dict(height_ratios=(1.1, 1)))
    _scissor_lines(a1, x, which=("3", "1", "2"))
    a1.plot([fwd, aft], [R_SEL, R_SEL], color=VERM, lw=3.2, marker="o", ms=7, zorder=5)
    a1.text((fwd + aft) / 2, R_SEL + 0.012, "cut at the selected $S_t/S$", fontsize=10.5, ha="center", va="bottom")
    a1.text(0.505, r_stability(0.5, SM), "stability,\nchosen $SM$", fontsize=10.5, va="center")
    a1.text(0.505, r_recovery(0.5), "stall\nrecovery", fontsize=10.5, va="center")
    a1.text(0.16, r_rotation(0.16) + 0.025, "takeoff rotation", fontsize=10.5, va="bottom")
    a1.set_ylim(0, 0.45)
    a1.set_ylabel("$S_t/S$")
    _loop(a2, a, b, labels=False)
    a2.text(0.352, 1.02, "MTOW", fontsize=10, ha="left", va="center")
    a2.text(0.345, 0.555, "empty", fontsize=10, ha="left", va="center")
    for ax, top in ((a1, R_SEL), (a2, 1.05)):
        for xl in (fwd, aft):
            ax.plot([xl, xl], [0 if ax is a1 else 0.5, top], color=VERM, lw=1.4, ls="--")
        clean(ax)
    a2.text(fwd - 0.005, 0.53, "forward limit", ha="right", fontsize=10.5)
    a2.text(aft + 0.005, 0.53, "aft limit", ha="left", fontsize=10.5)
    a2.set_ylim(0.5, 1.05)
    a2.set_xlim(0.15, 0.5)
    a2.set_xlabel(r"CG position $\bar{x}_{cg}$")
    a2.set_ylabel("$W/W_{TO}$")
    fig.tight_layout()
    save(fig, "scissor-and-envelope")


# ------------------------------------------------------------------- part 3, trim
def trim_lines():
    """Gudmundsson Example 24-6: C_M = 0.065 - 0.0065 alpha - 0.0215 delta_e, in degrees."""
    al = np.linspace(-5, 22, 20)
    trims = [(0.065 - 0.0215 * de) / 0.0065 for de in (-2, 0, 2)]
    assert abs(trims[1] - 10.0) < 0.01 and abs(trims[0] - 16.6) < 0.05 and abs(trims[2] - 3.4) < 0.05
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    for de, color, ls in ((-2, BLUE, ":"), (0, INK, "-"), (2, VERM, "--")):
        ax.plot(al, 0.065 - 0.0065 * al - 0.0215 * de, color=color, lw=2.0, ls=ls)
        lab = r"$\delta_e$ = 0°" if de == 0 else (r"$\delta_e$ = +2°" if de > 0 else r"$\delta_e$ = −2°")
        ax.text(22.4, 0.065 - 0.0065 * 22 - 0.0215 * de, lab, fontsize=10.5, va="center")
    ax.plot(trims, [0, 0, 0], "o", color=INK, ms=6)
    ax.axhline(0, color=GRAY, lw=0.8)
    ax.set_xlabel(r"Angle of attack $\alpha$ (deg)")
    ax.set_ylabel("$C_M$")
    ax.set_xlim(-5, 27)
    ax.set_xticks([0, 5, 10, 15, 20])
    ax.set_ylim(-0.13, 0.2)
    clean(ax)
    fig.tight_layout()
    save(fig, "trim-lines")


def tau_curve():
    e = np.linspace(0, 0.5, 101)
    thin = (np.arccos(1 - 2 * e) + 2 * np.sqrt(e * (1 - e))) / np.pi
    emp = -4.66 * e ** 4 + 8.79 * e ** 3 - 6.44 * e ** 2 + 2.85 * e + 0.0316
    t30 = -4.66 * 0.3 ** 4 + 8.79 * 0.3 ** 3 - 6.44 * 0.3 ** 2 + 2.85 * 0.3 + 0.0316
    assert abs(t30 - 0.5066) < 0.002 and 0.60 < np.interp(0.3, e, thin) < 0.70      # the empirical curve lies below
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    ax.plot(e, thin, color=INK, lw=2.0, label="thin-airfoil theory")
    keep = e >= 0.025
    ax.plot(e[keep], emp[keep], color=VERM, lw=2.0, ls="--", label="empirical, Gudmundsson Eq. 24-86")
    ax.plot([0.30], [t30], "o", color=VERM, ms=7)
    ax.text(0.315, t30 - 0.03, "0.30, 0.51", fontsize=10.5, va="top")
    ax.set_xlabel(r"Elevator chord ratio $E = c_e/\bar{c}_t$")
    ax.set_ylabel(r"Flap effectiveness $\tau$")
    ax.set_xlim(0, 0.5)
    ax.set_ylim(0, 1.0)
    ax.legend(frameon=False, fontsize=10.5, loc="lower right")
    clean(ax)
    fig.tight_layout()
    save(fig, "tau")


def trim_diagram():
    cl_a, cl_0, cl_de, cm_de, cm_0, limit = 5.0, 0.20, 0.40, -1.00, 0.06, 20.0

    def trim(cl, sm):
        cma = -cl_a * sm
        det = cl_a * cm_de - cl_de * cma
        return (cm_0 * cl_de + cm_de * (cl - cl_0)) / det * DEG, -(cm_0 * cl_a + cma * (cl - cl_0)) / det * DEG

    assert trim(1.8, 0.25)[1] < -limit < trim(1.8, 0.05)[1] < 0       # the forward CG reaches the limit first
    cl = np.linspace(-0.5, 2.0, 100)
    cl_slow = solve(lambda c: trim(c, 0.25)[1], -limit, 0.5, 2.0)
    assert abs(cl_slow - 1.69) < 0.01
    assert abs(trim(-0.5, 0.05)[1] - 5.6) < 0.05                       # the aft-CG elevator line starts at 5.6°
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.6, 4.4))
    for sm, color, ls, name in ((0.25, INK, "-", "forward CG, $SM$ 0.25"), (0.05, VERM, "--", "aft CG, $SM$ 0.05")):
        al, de = np.array([trim(c, sm) for c in cl]).T
        a1.plot(cl, al, color=color, lw=2.0, ls=ls, label=name)
        a2.plot(cl, de, color=color, lw=2.0, ls=ls)
    a2.text(-0.45, trim(-0.5, 0.25)[1] + 1.5, "forward CG", fontsize=10.5, va="bottom")
    a2.text(0.6, trim(0.6, 0.05)[1] + 1.8, "aft CG", fontsize=10.5, va="bottom")
    for y in (limit, -limit):
        a2.axhline(y, color=STEEL, lw=1.8, ls=":")
    a2.text(-0.45, limit + 1.5, "elevator limit, ±20° (invented)", fontsize=10.5, va="bottom")
    a2.plot([cl_slow], [-limit], "o", color=INK, ms=7)
    a2.text(cl_slow - 0.05, -limit - 2, "slowest trimmable", fontsize=10.5, ha="right", va="top")
    a1.set_ylabel(r"$\alpha_{trim}$ (deg)")
    a2.set_ylabel(r"$\delta_{e,trim}$ (deg)")
    for ax in (a1, a2):
        ax.set_xlabel("$C_{L,trim}$")
        ax.set_xlim(-0.5, 2.0)
        ax.set_ylim(-30, 30)
        clean(ax)
    a1.legend(frameon=False, fontsize=10.5, loc="upper left")
    fig.tight_layout()
    save(fig, "trim-diagram")


def thrust_trim():
    """Forces at the CG in flight-path axes, the thrust line z_T above the CG, the propeller
    normal force T_N at x_T ahead of it, and the moment about the CG (nose-up positive)."""
    fig, ax = sketch((9.4, 4.6))
    pts = _side_view(ax, 0.0, -0.05, 1.0, prop=True)
    cg = (4.9, -0.38)
    ax.add_patch(Circle(cg, 0.1, fc=VERM, ec="white", lw=0.8, zorder=8))
    ax.text(cg[0] - 0.2, cg[1] - 0.2, "CG", ha="right", va="top", fontsize=11, zorder=9)
    zt = -0.05
    arrow(ax, (-0.4, zt), (-2.1, zt), BLUE, lw=2.0)
    ax.text(-2.2, zt, "$T$", ha="right", va="center", fontsize=13)
    arrow(ax, (0.0, zt), (0.0, 2.0), BLUE, lw=2.0)
    ax.text(0.0, 2.08, "$T_N$", ha="center", va="bottom", fontsize=13)
    ax.plot([0.1, 10.7], [zt, zt], color=STEEL, lw=0.8, ls=(0, (4, 3)), zorder=9)
    ax.plot([cg[0], 10.7], [cg[1], cg[1]], color=STEEL, lw=0.8, ls=":", zorder=9)
    ax.annotate("", xy=(10.55, zt), xytext=(10.55, cg[1]), arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1.0, mutation_scale=8))
    ax.text(10.7, (zt + cg[1]) / 2, "$z_T$", va="center", fontsize=12)
    ax.annotate("", xy=(cg[0], -1.6), xytext=(0.0, -1.6), arrowprops=DIM)
    ax.text(cg[0] / 2, -1.68, "$x_T$", ha="center", va="top", fontsize=12)
    for x, y0 in ((0.0, -1.15), (cg[0], -0.3)):
        ax.plot([x, x], [y0, -1.6], color=STEEL, lw=0.8, ls=":")
    arrow(ax, cg, (cg[0], 2.2), INK, lw=2.0)
    ax.text(cg[0], 2.28, "$L$", ha="center", va="bottom", fontsize=13)
    arrow(ax, cg, (cg[0], -2.4), INK, lw=2.0)
    ax.text(cg[0] + 0.15, -2.25, "$W$", va="center", fontsize=13)
    arrow(ax, cg, (7.6, cg[1]), VERM, lw=2.0)
    ax.text(7.7, cg[1] - 0.12, "$D$", ha="left", va="top", fontsize=13)
    _arc(ax, cg, 1.1, 125, 50, color=INK, lw=1.5)
    ax.text(cg[0] + 0.95, cg[1] + 1.15, "$M_{cg}$", ha="left", va="center", fontsize=12.5)
    arrow(ax, (-3.6, -1.0), (-2.2, -1.0), STEEL, lw=1.5)
    ax.text(-2.9, -0.87, "$V$", ha="center", va="bottom", fontsize=13)
    ax.set_xlim(-3.8, 11.3)
    ax.set_ylim(-2.7, 2.7)
    save(fig, "thrust-trim")


def trimmed_polar():
    cd0, k, st_s, ar_t, e_t, dx, cmac = 0.025, 1 / (math.pi * 8.0 * 0.80), 0.22, 4.0, 0.80, -0.10, -0.08

    def polar(cl):
        clt = (cmac + cl * dx) / (ETA_H * st_s * L_T)
        clw = cl - ETA_H * st_s * clt
        return cd0 + k * cl ** 2, cd0 + k * clw ** 2 + ETA_H * st_s * clt ** 2 / (math.pi * e_t * ar_t), clt

    assert polar(1.2)[1] > polar(1.2)[0] and polar(1.2)[2] < 0      # a tail download adds drag at high lift
    cl = np.linspace(-0.4, 1.8, 100)
    c, t, _ = np.array([polar(v) for v in cl]).T
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.plot(cl, c, color=VERM, lw=2.0, ls="--")
    ax.plot(cl, t, color=INK, lw=2.0)
    ax.annotate("trimmed", xy=(1.55, polar(1.55)[1]), xytext=(1.05, 0.19), fontsize=10.5, ha="right",
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    ax.annotate("untrimmed, wing only", xy=(1.62, polar(1.62)[0]), xytext=(1.25, 0.075), fontsize=10.5, ha="left",
                arrowprops=dict(arrowstyle="-", color=VERM, lw=0.8))
    ax.set_xlabel("$C_{L,trim}$")
    ax.set_ylabel("$C_D$")
    ax.set_xlim(-0.4, 1.8)
    ax.set_ylim(0, 0.25)
    clean(ax)
    fig.tight_layout()
    save(fig, "trimmed-polar")


# --------------------------------------------- part 4, lateral-directional, controls
def cn_beta():
    b = np.linspace(-18, 18, 10)
    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    ax.plot(b, 0.04 * b, color=INK, lw=2.0)
    ax.plot(b, -0.03 * b, color=VERM, lw=2.0, ls="--")
    ax.text(18.6, 0.72, r"stable, $C_{n\beta} > 0$", fontsize=10.5, va="center")
    ax.text(18.6, -0.54, "unstable", fontsize=10.5, va="center")
    ax.axhline(0, color=INK, lw=0.9)
    ax.axvline(0, color=INK, lw=0.9)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.text(33.5, -0.1, r"$\beta$, wind from the right", fontsize=10.5, ha="right", va="top")
    ax.text(0.6, 0.95, "$C_n$", fontsize=11, va="center")
    ax.set_xlim(-20, 34)
    ax.set_ylim(-1, 1.05)
    save(fig, "cn-beta")


def _top_view(ax, x0=0.0, y0=0.0, s=1.0, nose_up=False, nacelles=False, z=2):
    """Top view of the trainer, nose to the left (or up with nose_up=True), length 10 s.
    Local y is positive toward the right half wing. Returns the page transform."""
    def T(pts):
        P = np.atleast_2d(np.array(pts, float))
        if nose_up:
            return np.column_stack([x0 + s * P[:, 1], y0 - s * P[:, 0]])
        return np.column_stack([x0 + s * P[:, 0], y0 - s * P[:, 1]])
    half = FUS_TOP
    body = half + [(p[0], -p[1]) for p in half[::-1]][1:]
    for sgn in (1, -1):
        ax.add_patch(Polygon(T([(x, sgn * y) for x, y in WING_TOP]), closed=True, fc=LIGHT, ec=INK, lw=0.9, zorder=z))
        ax.add_patch(Polygon(T([(x, sgn * y) for x, y in HT_TOP]), closed=True, fc=LIGHT, ec=INK, lw=0.9, zorder=z))
        if not nacelles:
            ax.add_patch(Polygon(T(_smooth([(3.7, sgn * 0.42), (4.2, sgn * 0.62), (5.6, sgn * 0.6), (6.4, sgn * 0.44)], closed=False)),
                                 closed=True, fc="#DDE0E5", ec=STEEL, lw=0.9, zorder=z + 0.1))
        else:
            ax.add_patch(Polygon(T(_smooth([(4.2, sgn * 1.55), (4.4, sgn * 1.75), (6.6, sgn * 1.78), (7.3, sgn * 1.68),
                                            (7.3, sgn * 1.42), (6.6, sgn * 1.32), (4.4, sgn * 1.35)])), closed=True,
                                 fc="#DDE0E5", ec=STEEL, lw=1.0, zorder=z + 0.3))
    ax.add_patch(Polygon(T(_smooth(body)), closed=True, fc=FUS_FILL, ec=STEEL, lw=1.2, zorder=z + 0.2))
    ax.add_patch(Polygon(T(_smooth([(1.7, 0), (2.4, 0.2), (3.6, 0.24), (4.5, 0.16), (4.8, 0), (4.5, -0.16), (3.6, -0.24), (2.4, -0.2)])),
                         closed=True, fc=CANOPY_FILL, ec=STEEL, lw=0.9, zorder=z + 0.3))
    ax.add_patch(Polygon(T([(7.7, 0.05), (9.9, 0.05), (9.9, -0.05), (7.7, -0.05)]), closed=True, fc=LIGHT, ec=INK, lw=0.9, zorder=z + 0.4))
    return T


def fin_arm():
    fig, ax = sketch((7.8, 5.4))
    T = _top_view(ax)
    wq = 4.1 + 0.25 * 2.75 + (5.75 - 4.1) * 0.42          # wing quarter-chord point at the MAC station (schematic)
    fq = 8.75
    for x, lab in ((wq, r"wing $\bar{c}/4$"), (fq, r"fin $\bar{c}/4$")):
        ax.add_patch(Circle((x, 0), 0.07, fc=INK, ec="white", lw=0.6, zorder=8))
    ax.annotate("", xy=(-0.5, -3.6), xytext=(-0.5, 3.6), arrowprops=DIM)
    ax.text(-0.62, 0.0, "$b$", ha="right", va="center", fontsize=13)
    for s in (1, -1):
        ax.plot([-0.5, 5.75], [s * 3.6, s * 3.6], color=STEEL, lw=0.8, ls=":")
    ax.annotate("", xy=(fq, -4.1), xytext=(wq, -4.1), arrowprops=DIM)
    ax.text((wq + fq) / 2, -4.2, r"$l_v$, wing $\bar{c}/4$ to fin $\bar{c}/4$", ha="center", va="top", fontsize=11.5)
    for x in (wq, fq):
        ax.plot([x, x], [0, -4.1], color=STEEL, lw=0.8, ls=":")
    ax.annotate("fin", xy=(9.3, 0.0), xytext=(10.4, 0.9), fontsize=11, ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    ax.set_xlim(-1.2, 11.2)
    ax.set_ylim(-4.9, 4.0)
    save(fig, "fin-arm")


def dihedral():
    """View from behind, wind from the right (beta > 0). The right half wing, toward the wind,
    lifts more, and the aircraft rolls left half wing down, away from the wind: seen from
    behind that is a counterclockwise arc (240 to 300 degrees, head at 300)."""
    fig, ax = sketch((8.2, 4.4))
    gamma = 7.0
    left, right = _rear_view(ax, gamma)
    g = math.radians(gamma)
    for sgn, L, name in ((-1, 0.85, "$L_L$"), (1, 1.6, "$L_R$")):
        p = (sgn * (0.45 + 2.2 * math.cos(g)), -0.28 + 2.2 * math.sin(g) + 0.05)
        arrow(ax, p, (p[0], p[1] + L), BLUE, lw=2.0)
        ax.text(p[0], p[1] + L + 0.08, name, ha="center", va="bottom", fontsize=13)
    ax.plot([0.45, 4.3], [-0.28, -0.28], color=STEEL, lw=0.8, ls=":")
    _arc(ax, (0.45, -0.28), 3.0, 0, gamma, color=STEEL, lw=1.0, head=False)
    ax.text(4.0, 0.02, r"$\Gamma$", fontsize=13, va="center")
    arrow(ax, (5.4, -1.0), (4.0, -1.0), STEEL, lw=1.6)
    ax.text(5.5, -1.0, r"wind, $\beta > 0$", ha="left", va="center", fontsize=11)
    assert True                                                          # head at 300 deg: right half wing up
    _arc(ax, (0.0, 0.05), 0.95, 240, 300, color=INK, lw=1.6)
    ax.text(0.0, -1.2, "rolls away from the wind:\nleft half wing down", ha="center", va="top", fontsize=11)
    ax.text(-4.2, 1.9, "view from behind", fontsize=10.5, color=STEEL, va="center")
    ax.set_xlim(-4.3, 7.3)
    ax.set_ylim(-2.1, 2.6)
    save(fig, "dihedral")


def engine_out():
    """Top view, nose up, of a twin with the right engine failed."""
    fig, ax = sketch((6.0, 6.6))
    T = _top_view(ax, 0.0, 4.0, 0.85, nose_up=True, nacelles=True)
    live, dead = T([(7.3, -1.55)])[0], T([(7.3, 1.55)])[0]
    cg = T([(5.2, 0.0)])[0]
    fin = T([(8.9, 0.0)])[0]
    ax.add_patch(Circle(cg, 0.1, fc=VERM, ec="white", lw=0.8, zorder=9))
    ax.annotate("CG", xy=cg, xytext=(cg[0] - 0.75, cg[1] - 0.75), fontsize=11, ha="center", va="top", zorder=9,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    nose_l = T([(4.2, -1.55)])[0]
    arrow(ax, nose_l, (nose_l[0], nose_l[1] + 1.5), BLUE, lw=2.2)
    ax.text(nose_l[0], nose_l[1] + 1.58, "$T$", ha="center", va="bottom", fontsize=13)
    arrow(ax, dead, (dead[0], dead[1] - 0.8), VERM, lw=2.2)
    ax.text(dead[0] + 0.15, dead[1] - 0.45, "$D_{dead}$", va="center", fontsize=13)
    ax.text(dead[0] + 0.4, T([(4.2, 1.55)])[0][1] + 0.25, "failed", fontsize=11, va="center")
    ax.annotate("", xy=(fin[0] + 1.3, fin[1]), xytext=fin, zorder=10, arrowprops=dict(color=INK, **{**ARROW, "lw": 2.0}))
    ax.text(fin[0] + 1.4, fin[1], "$Y_v$", va="center", fontsize=13)
    _arc(ax, (cg[0], cg[1] + 2.3), 0.55, 150, 40, color=INK, lw=1.4)
    ax.text(cg[0] + 0.55, cg[1] + 3.0, "yaw", fontsize=11, va="bottom")
    ax.annotate("", xy=(dead[0], 4.6), xytext=(cg[0], 4.6), arrowprops=DIM)
    ax.text((cg[0] + dead[0]) / 2, 4.68, "$y_e$", ha="center", va="bottom", fontsize=12)
    ax.plot([dead[0], dead[0]], [T([(4.2, 1.55)])[0][1], 4.6], color=STEEL, lw=0.8, ls=":")
    ax.plot([cg[0], cg[0]], [4.0, 4.6], color=STEEL, lw=0.8, ls=":")
    ax.annotate("", xy=(-3.4, fin[1]), xytext=(-3.4, cg[1]), arrowprops=DIM)
    ax.text(-3.55, (cg[1] + fin[1]) / 2, "$l_{v,cg}$", ha="right", va="center", fontsize=12)
    for y in (cg[1], fin[1]):
        ax.plot([-3.4, -0.1], [y, y], color=STEEL, lw=0.8, ls=":")
    ax.set_xlim(-4.3, 4.6)
    ax.set_ylim(-4.9, 5.1)
    save(fig, "engine-out")


def control_surfaces():
    """Top view with the ailerons and elevators hatched, the fin in side view with the rudder
    hatched, and a half planform with the aileron between b_1 and b_2."""
    fig, ax = sketch((10.4, 5.0))
    hatch = dict(fc="white", ec=VERM, lw=1.0, hatch="////", zorder=6)
    T = _top_view(ax, 0.0, 0.0, 0.75, nose_up=True)

    def te_strip(le, te, f0, f1, cf):
        (ax0, ay0), (ax1, ay1) = le
        (bx0, by0), (bx1, by1) = te
        p = []
        for f in (f0, f1):
            lx, ly = ax0 + f * (ax1 - ax0), ay0 + f * (ay1 - ay0)
            tx, ty = bx0 + f * (bx1 - bx0), by0 + f * (by1 - by0)
            p.append(((tx - cf * (tx - lx)), ty))
            p.append((tx, ty))
        return [p[0], p[2], p[3], p[1]]
    for s in (1, -1):
        ail = te_strip(((4.1, 0.45), (5.75, 3.6)), ((6.85, 0.45), (6.65, 3.6)), 0.6, 0.95, 0.25)
        ax.add_patch(Polygon(T([(x, s * y) for x, y in ail]), closed=True, **hatch))
        ele = te_strip(((8.35, 0.36), (9.25, 1.55)), ((9.9, 0.30), (9.8, 1.55)), 0.05, 0.95, 0.35)
        ax.add_patch(Polygon(T([(x, s * y) for x, y in ele]), closed=True, **hatch))
    ax.text(*T([(7.4, -3.0)])[0], "aileron", ha="center", va="top", fontsize=11)
    ax.text(*T([(10.6, -1.2)])[0], "elevator", ha="center", va="top", fontsize=11)
    ax.text(0.0, 0.25, "top view", ha="center", va="bottom", fontsize=10.5, color=STEEL)
    # fin in side view, rudder hatched
    fx, fy = 3.6, -7.5
    fin = [(0.0, 0.0), (1.4, 1.9), (2.0, 1.9), (2.3, 0.0)]
    ax.add_patch(Polygon([(fx + x, fy + y) for x, y in fin], closed=True, fc=LIGHT, ec=INK, lw=0.9, zorder=4))
    rud = [(1.75, 0.0), (2.3, 0.0), (2.03, 1.75), (1.62, 1.75)]
    ax.add_patch(Polygon([(fx + x, fy + y) for x, y in rud], closed=True, **hatch))
    ax.plot([fx - 0.3, fx + 2.7], [fy, fy], color=STEEL, lw=1.0)
    ax.text(fx + 1.0, fy + 2.1, "fin, side view", ha="center", va="bottom", fontsize=10.5, color=STEEL)
    ax.text(fx + 2.1, fy - 0.15, "rudder", ha="center", va="top", fontsize=11)
    # half planform with the aileron span, after Gudmundsson Fig. 25-23
    x0, yb = 7.6, -6.9
    hw = [(x0, yb + 4.4), (x0 + 5.6, yb + 3.0), (x0 + 5.6, yb + 2.0), (x0, yb + 1.0)]
    ax.add_patch(Polygon(hw, closed=True, fc=LIGHT, ec=INK, lw=0.9, zorder=4))
    te = lambda x: yb + 1.0 + (x - x0) / 5.6 * 1.0
    le = lambda x: yb + 4.4 - (x - x0) / 5.6 * 1.4
    b1, b2 = x0 + 3.0, x0 + 5.2
    ax.add_patch(Polygon([(b1, te(b1)), (b2, te(b2)), (b2, te(b2) + 0.25 * (le(b2) - te(b2))), (b1, te(b1) + 0.25 * (le(b1) - te(b1)))],
                         closed=True, **hatch))
    ax.plot([x0, x0], [yb - 1.6, yb + 4.9], color=STEEL, lw=0.8, ls="-.")
    ax.text(x0, yb + 5.0, "centerline", ha="center", va="bottom", fontsize=10.5, color=STEEL)
    ax.text((b1 + b2) / 2, te(b2) + 0.75, "aileron", ha="center", va="bottom", fontsize=11)
    for x1, y, name in ((b1, yb + 0.35, "$b_1$"), (b2, yb - 0.35, "$b_2$"), (x0 + 5.6, yb - 1.05, "$b/2$")):
        ax.annotate("", xy=(x1, y), xytext=(x0, y), arrowprops=DIM)
        ax.text((x0 + x1) / 2, y - 0.06, name, ha="center", va="top", fontsize=12)
        ax.plot([x1, x1], [te(x1) if x1 < x0 + 5.6 else yb + 2.0, y], color=STEEL, lw=0.8, ls=":")
    ax.set_xlim(-3.9, 13.8)
    ax.set_ylim(-9.0, 1.0)
    save(fig, "control-surfaces")


def uiuc_scissor():
    """Values read from Team Draco (2025), Figure 52: three straight lines in S_h/S_w against
    the CG in fractions of the MAC, and the operational CG range at the chosen 0.27."""
    lines = {"aft stability limit": ((0.436, 0.0), (0.599, 0.5)), "landing approach": ((0.2, 0.447), (0.656, 0.0)),
             "takeoff rotation": ((0.2, 0.466), (0.5425, 0.0))}

    def x_at(name, r):
        (x0, y0), (x1, y1) = lines[name]
        return x0 + (r - y0) * (x1 - x0) / (y1 - y0)
    r_sel = 0.27
    fwd, aft = x_at("landing approach", r_sel), x_at("aft stability limit", r_sel)
    assert x_at("takeoff rotation", r_sel) < fwd                       # landing sets the forward limit at 0.27
    assert abs(fwd - 0.38) < 0.01 and abs(aft - 0.524) < 0.01           # the report's arrow: about 0.38 to 0.52
    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    xs = np.linspace(0.2, 0.8, 400)
    floor = np.maximum.reduce([np.interp(xs, *zip(*sorted([p0, p1]))) if name != "aft stability limit" else
                               (xs - 0.436) * 0.5 / (0.599 - 0.436) for name, (p0, p1) in lines.items()])
    floor = np.maximum(floor, np.maximum((0.447 - (xs - 0.2) * 0.447 / 0.456), (0.466 - (xs - 0.2) * 0.466 / 0.3425)))
    ax.fill_between(xs, np.minimum(floor, 0.5), 0.5, color=DUST, lw=0, zorder=0)
    ax.text(0.33, 0.44, "feasible", fontsize=12, fontweight="bold", ha="center")
    for (name, (p0, p1)), color, ls in zip(lines.items(), (PURPLE, GREEN, VERM), ("-", "--", "-.")):
        ax.plot(*zip(p0, p1), color=color, ls=ls, lw=2.0)
    ax.annotate("", xy=(aft, r_sel), xytext=(fwd, r_sel), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.6))
    ax.text((fwd + aft) / 2, r_sel + 0.015, "operational CG range", ha="center", va="bottom", fontsize=10.5)
    ax.text(0.61, 0.47, "aft stability\nlimit", fontsize=10.5, va="center")
    ax.text(0.56, 0.14, "landing approach", fontsize=10.5, va="center")
    ax.text(0.235, 0.15, "takeoff rotation", fontsize=10.5, va="center")
    ax.set_xlabel(r"CG position (fraction of the MAC)")
    ax.set_ylabel("$S_h/S_w$")
    ax.set_xlim(0.2, 0.8)
    ax.set_ylim(0, 0.5)
    clean(ax)
    fig.tight_layout()
    save(fig, "uiuc-scissor")


def uiuc_cg_sm():
    """Values read from Team Draco (2025), Figure 49: weight against the CG and the static
    margin, both in % MAC, for the eleven segments of their patrol mission."""
    w = [30610, 30110, 28890, 21300, 20000, 19600, 19240, 18620, 18400, 16920, 16000]
    cg = [38.4, 39.7, 42.9, 46.2, 45.2, 45.6, 46.0, 48.0, 48.3, 50.4, 52.5]
    sm = [3.7, 7.9, 8.1, 5.1, 9.5, -7.5, 5.0, 3.0, 3.0, -3.2, -1.2]
    sup = [3, 5, 6, 9, 10]                                              # supersonic segments (triangles)
    assert all(-10 < v < 10 for v in sm) and cg[-1] - cg[0] > 10       # inside the band; the CG moves aft as fuel burns
    fig, ax = plt.subplots(figsize=(9.0, 4.8))
    ax.axvspan(-10, 10, color=DUST, lw=0, zorder=0)
    for xv in (-10, 10):
        ax.axvline(xv, color=VERM, lw=1.3, ls="--")
    ax.text(0, 32300, "±10% band of\nthat year's RFP", ha="center", va="bottom", fontsize=10.5)
    for vals, color, ls, name, lx in ((cg, BLUE, "-", "CG", 54.0), (sm, VERM, "--", "static margin", 11.0)):
        ax.plot(vals, w, color=color, lw=1.6, ls=ls, zorder=3)
        for i, (v, wi) in enumerate(zip(vals, w), 1):
            ax.plot([v], [wi], "^" if i in sup else "s", color=color, ms=7, zorder=4)
        ax.text(*((47.0, 24500) if name == "CG" else (-9.5, 25500)), name, color=INK, fontsize=11, fontweight="bold",
                va="center", ha="left")
    for v, wi, k in ((cg[0], w[0], "1"), (cg[-1], w[-1], "11"), (sm[0], w[0], "1"), (sm[-1], w[-1], "11")):
        ax.text(v + 1.0, wi, k, fontsize=10, va="center")
    ax.plot([], [], "s", color=STEEL, ms=7, label="subsonic segment")
    ax.plot([], [], "^", color=STEEL, ms=7, label="supersonic segment")
    ax.legend(frameon=False, fontsize=10.5, loc="center", bbox_to_anchor=(0.6, 0.5))
    ax.set_xlabel("Percent of the MAC")
    ax.set_ylabel("Weight (lb)")
    ax.set_xlim(-12, 58)
    ax.set_ylim(15000, 34500)
    ax.set_yticks(range(16000, 32001, 4000))
    ax.set_yticklabels([f"{t:,}" for t in range(16000, 32001, 4000)])
    clean(ax)
    fig.tight_layout()
    save(fig, "uiuc-cg-sm")


def liege_cg():
    """Values read from University of Liege (2025), Figure 7.1 (positions in ft from the nose);
    the CG ends and the aerodynamic centers agree with their Table 16."""
    rows = {"takeoff and landing": dict(ac=53.03, cg=(55.41, 56.22), sm=(55.24, 56.45), lab=("15%", "5%"), y=1.0, c=BLUE),
            "cruise": dict(ac=54.36, cg=(54.49, 56.81), sm=(54.44, 57.11), lab=("32%", "10%"), y=-1.0, c=VERM)}
    assert abs(rows["cruise"]["ac"] - rows["takeoff and landing"]["ac"] - 1.33) < 0.01     # AC 1.3 ft aft with Mach
    fig, ax = plt.subplots(figsize=(9.4, 3.8))
    ax.axis("off")
    ax.annotate("", xy=(59.4, 0), xytext=(52.7, 0), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6))
    for t in range(53, 60):
        ax.plot([t, t], [-0.12, 0.12], color=INK, lw=1.2)
        ax.text(t, -0.2 if t not in (54, 57) else -0.2, f"{t}", ha="center", va="top", fontsize=11)
    ax.text(59.45, 0, "ft from the nose", ha="left", va="center", fontsize=10.5)
    for name, r in rows.items():
        s, c = (1 if r["y"] > 0 else -1), r["c"]
        y_cg, y_sm = s * 1.0, s * 1.55
        ax.plot([r["ac"]], [s * 0.6], "o", color=c, ms=9)
        ax.text(r["ac"] - 0.12, s * 0.6, "AC", color=INK, ha="right", va="center", fontsize=11, fontweight="bold")
        for (x0, x1), y, col, lab in ((r["cg"], y_cg, INK, "CG"), (r["sm"], y_sm, c, "static margin")):
            ax.plot([x0, x1], [y, y], color=col, lw=2.2, ls="-" if col is INK else ("-" if s > 0 else "--"))
            for xe in (x0, x1):
                ax.plot([xe, xe], [y - 0.1, y + 0.1], color=col, lw=2.2)
            ax.text((x0 + x1) / 2, y + s * 0.12, lab, ha="center", va="bottom" if s > 0 else "top", fontsize=11)
        for xe, l in zip(r["sm"], r["lab"]):
            ax.plot([xe, xe], [0, y_sm], color=GRAY, lw=0.9, ls=":")
            ax.text(xe + 0.05, s * 0.32, l, ha="left", va="center", fontsize=10)
        ax.text(52.6, s * 1.3, name, ha="left", va="center", fontsize=11, fontweight="bold")
    ax.set_xlim(52.5, 60.6)
    ax.set_ylim(-2.1, 2.1)
    save(fig, "liege-cg")


def trim_defined():
    """The two controls of trim: the angle of attack alpha between the flight path and the
    reference line, and the elevator deflection delta_e (trailing edge down positive)."""
    fig, ax = sketch((10.0, 5.2))
    a = 9.0
    pts = _side_view(ax, 0.0, 0.0, 1.0, nose_up=a, de=20.0)
    cg = _tf([(5.0, 0.0)], nose_up=a)[0]
    ax.add_patch(Circle(cg, 0.1, fc=VERM, ec="white", lw=0.8, zorder=8))
    lab = _tf([(5.3, 1.45)], nose_up=a)[0]
    ax.annotate("CG", xy=cg, xytext=lab, fontsize=11, ha="center", va="bottom", zorder=9,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    ref0, ref1 = _tf([(-1.4, 0.0), (11.6, 0.0)], nose_up=a)
    ax.plot(*zip(ref0, ref1), color=STEEL, lw=1.0, ls="-.", zorder=1)
    ax.text(ref1[0] + 0.1, ref1[1], "reference line", fontsize=10.5, ha="left", va="center")
    ax.plot([cg[0] - 6.3, cg[0] + 6.3], [cg[1], cg[1]], color=STEEL, lw=1.0, ls=":", zorder=1)
    arrow(ax, (cg[0] - 7.9, cg[1]), (cg[0] - 6.5, cg[1]), INK, lw=1.8)
    ax.text(cg[0] - 7.2, cg[1] + 0.15, "$V$", fontsize=13, ha="center", va="bottom")
    _arc(ax, cg, 5.8, 180 - a, 180, color=INK, lw=1.2, head=False)
    ax.text(cg[0] - 6.0, cg[1] + 0.48, r"$\alpha$", fontsize=13, ha="right", va="center")
    h, te = pts["hinge"], pts["el_te"]
    # the tail enlarged three times, same attitude
    hx, hy, k = cg[0] + 3.2, -3.3, 3.0
    rot = lambda P, deg: np.array([hx, hy]) + (np.array(P) - [hx, hy]) @ np.array(
        [[math.cos(math.radians(-deg)), math.sin(math.radians(-deg))], [-math.sin(math.radians(-deg)), math.cos(math.radians(-deg))]])
    ax.add_patch(Polygon(rot(_naca(hx - 0.95 * k, 0.95 * k, hy, t=0.13, m=0), a), closed=True, fc=LIGHT, ec=INK, lw=1.0, zorder=5))
    ax.add_patch(Polygon(rot(_naca(hx, 0.7 * k, hy, t=0.08, m=0), a + 20.0), closed=True, fc=VERM, ec=INK, lw=1.0, zorder=6))
    ext = rot([(hx, hy), (hx + 0.9 * k, hy)], a)
    ax.plot(*ext.T, color=INK, lw=0.9, ls=(0, (3, 2)), zorder=7)
    _arc(ax, (hx, hy), 1.7, -a, -a - 20.0, color=INK, lw=1.1, head=False)
    ax.text(hx + 1.85, hy - 0.62, r"$\delta_e$", fontsize=13, ha="left", va="center")
    ax.text(hx - 1.4, hy + 0.75, "tail, enlarged", fontsize=10.5, ha="center", va="bottom", color=STEEL)
    ax.text(cg[0] - 4.2, cg[1] - 1.3, "flight path", fontsize=10.5, ha="center", color=STEEL)
    ax.annotate("", xy=(cg[0] - 4.6, cg[1] - 0.03), xytext=(cg[0] - 4.3, cg[1] - 1.05),
                arrowprops=dict(arrowstyle="-", color=STEEL, lw=0.8))
    ax.set_xlim(cg[0] - 8.1, cg[0] + 8.0)
    ax.set_ylim(-4.6, 2.4)
    save(fig, "trim-defined")


def _smooth(pts, n=10, closed=True):
    """Catmull-Rom spline through the points: smooth outlines for the schematics."""
    P = np.array(pts, float)
    P = np.vstack([P[-1], P, P[0], P[1]]) if closed else np.vstack([P[0], P, P[-1]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * (2 * p1 + (p2 - p0) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                              + (3 * p1 - p0 - 3 * p2 + p3) * t ** 3))
    if not closed:
        out.append(P[-2])
    return np.array(out)


def _tf(pts, x0=0.0, y0=0.0, s=1.0, nose_up=0.0):
    """Local side-view coordinates (nose at x = 0, aft positive) to the page: pitch nose up
    by nose_up degrees about the local origin, scale by s, move to (x0, y0)."""
    P = np.atleast_2d(np.array(pts, float))
    a = -math.radians(nose_up)
    c, si = math.cos(a), math.sin(a)
    return np.column_stack([x0 + s * (c * P[:, 0] - si * P[:, 1]), y0 + s * (si * P[:, 0] + c * P[:, 1])])


def _naca(x0, chord, y0=0.0, t=0.12, m=0.02, p=0.4, n=60):
    """NACA four-digit section, leading edge at (x0, y0), chord along +x; closed outline."""
    b = 0.5 * (1 - np.cos(np.linspace(0, np.pi, n)))
    yt = 5 * t * (0.2969 * np.sqrt(b) - 0.1260 * b - 0.3516 * b ** 2 + 0.2843 * b ** 3 - 0.1036 * b ** 4)
    yc = np.where(b < p, m / p ** 2 * (2 * p * b - b ** 2), m / (1 - p) ** 2 * (1 - 2 * p + 2 * p * b - b ** 2)) if m else 0 * b
    up = np.column_stack([x0 + chord * b, y0 + chord * (yc + yt)])
    lo = np.column_stack([x0 + chord * b, y0 + chord * (yc - yt)])
    return np.vstack([up, lo[::-1]])


def _arc(ax, c, r, a0, a1, color=STEEL, lw=1.3, label=None, lpos=None, fs=11.5, head=True):
    """Circular arc from a0 to a1 (degrees, counterclockwise positive) with the head at a1."""
    th = np.radians(np.linspace(a0, a1, 40))
    xs, ys = c[0] + r * np.cos(th), c[1] + r * np.sin(th)
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=10)
    if head:
        ax.annotate("", xy=(xs[-1], ys[-1]), xytext=(xs[-4], ys[-4]),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=14), zorder=10)
    if label:
        ax.text(*lpos, label, fontsize=fs, ha="center", va="center")


FUS_SIDE = [(0.0, 0.02), (0.45, 0.2), (1.2, 0.36), (2.1, 0.47), (3.4, 0.55), (5.6, 0.58), (7.2, 0.52), (8.7, 0.40),
            (9.85, 0.30), (9.95, 0.08), (9.85, -0.12), (8.6, -0.22), (6.6, -0.42), (4.6, -0.50), (2.6, -0.44), (1.3, -0.30),
            (0.5, -0.12)]
CANOPY = [(1.9, 0.46), (2.4, 0.74), (3.2, 0.93), (4.3, 0.95), (5.1, 0.80), (5.6, 0.58)]
FUS_TOP = [(0.0, 0.0), (0.5, 0.16), (1.4, 0.30), (2.6, 0.40), (4.0, 0.45), (7.4, 0.44), (9.0, 0.36), (9.95, 0.28)]
WING_TOP = [(4.1, 0.45), (5.75, 3.6), (6.65, 3.6), (6.85, 0.45)]
HT_TOP = [(8.35, 0.36), (9.25, 1.55), (9.8, 1.55), (9.9, 0.30)]
CANOPY_FILL, FUS_FILL = "#C9D5E1", "#EEF0F3"


def _rear_view(ax, gamma=7.0, wing_y=-0.28, z=2):
    """View from behind: fuselage, canopy, fin, horizontal tail, nozzle, and the two half wings
    raised at the dihedral angle gamma (deg). Returns the outboard tip points (left, right)."""
    g = math.radians(gamma)
    ax.add_patch(Polygon([(-1.45, 0.20), (1.45, 0.20), (1.45, 0.26), (-1.45, 0.26)], closed=True, fc=LIGHT, ec=INK, lw=0.9, zorder=z))
    ax.add_patch(Polygon([(-0.07, 0.4), (-0.04, 2.0), (0.04, 2.0), (0.07, 0.4)], closed=True, fc=LIGHT, ec=INK, lw=0.9, zorder=z))
    tips = []
    for sgn in (1, -1):
        root, span = 0.45, 3.4
        tip = (sgn * (root + span * math.cos(g)), wing_y + span * math.sin(g))
        up = (sgn * root, wing_y + 0.08), (tip[0], tip[1] + 0.03)
        lo = (tip[0], tip[1] - 0.03), (sgn * root, wing_y - 0.08)
        ax.add_patch(Polygon([up[0], up[1], lo[0], lo[1]], closed=True, fc=LIGHT, ec=INK, lw=0.9, zorder=z + 0.1))
        tips.append(tip)
    th = np.linspace(0, 2 * np.pi, 80)
    ax.add_patch(Polygon(np.column_stack([0.55 * np.cos(th), 0.05 + 0.5 * np.sin(th)]), closed=True, fc=FUS_FILL, ec=STEEL, lw=1.2, zorder=z + 0.2))
    ax.add_patch(Polygon(np.column_stack([0.27 * np.cos(th[:41]), 0.48 + 0.33 * np.sin(th[:41])]), closed=True, fc=CANOPY_FILL, ec=STEEL, lw=0.9, zorder=z + 0.1))
    ax.add_patch(Circle((0, 0.02), 0.25, fc="#9AA0A8", ec=STEEL, lw=0.9, zorder=z + 0.3))
    return tips[1], tips[0]


ALL = [method_flow, cg_table_sketch, cg_envelope, sr22_envelope, cm_components, moment_about_cg, static_margin_lines,
       cma_by_class, scissor_plot, uiuc_scissor, uiuc_cg_sm, scissor_and_envelope, trim_defined, trim_lines, tau_curve,
       trim_diagram, thrust_trim, trimmed_polar, cn_beta, fin_arm, dihedral, engine_out, control_surfaces, liege_cg]

if __name__ == "__main__":
    for fn in ALL:
        fn()
