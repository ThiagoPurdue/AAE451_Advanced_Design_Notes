"""Figures for Lecture 11, Performance.

The lecture slides draw every figure natively. The computed figures here use two
published examples and recompute each curve from the published inputs, asserting
the numbers the figure exists to show before anything is drawn:

  - Learjet 45, Gudmundsson (2022), Table 17-8: S 311.6 ft2, simplified polar
    C_D0 0.0200, K 0.05236 (his Examples 19-4, 20-5, 20-6, 20-8), C_Lmax 1.527
    flaps up; thrust from the Mattingly low-bypass model of his Sec. 14.3.4,
    Eqs. 14-66 to 14-78, throttle ratio 1.072, 2 x 3,500 lbf. Ground run of his
    Example 18-5.
  - Air-to-Air Fighter of Mattingly, Heiser and Pratt (2002), Chapter 2, for
    the maneuver V-n diagram.

Neither is the Navy trainer. The schematics (free-body diagrams, the takeoff
run, the loop) reuse the tandem-seat jet trainer drawing of Lecture 10
(make_stability_figures.py) and assert the direction of every force they draw.
Run from the book folder:

    python3 scripts/make_performance_figures.py

Set FIG_PREVIEW=<folder> to also write PNG copies for checking.
"""
import math
import os
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.patches import Polygon, FancyBboxPatch, Circle, Rectangle
from matplotlib.transforms import Affine2D

import make_stability_figures as msf        # the shared trainer drawing

OUT = Path(__file__).resolve().parents[1] / "notes" / "lecture-11" / "figures"
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
ARROW = dict(arrowstyle="-|>", lw=2.0)


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


def sketch(figsize):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def close(a, b, tol, what):
    assert abs(a - b) <= tol, f"{what}: {a:.4f} vs {b:.4f}"


def thousands(ax, axis="y"):
    fmt = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(fmt)


def bisect(fun, lo, hi):
    """Root of fun between lo and hi; the bracket must hold one sign change."""
    f_lo = fun(lo)
    assert (f_lo > 0) != (fun(hi) > 0), "bisect: no sign change in the bracket"
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if (fun(mid) > 0) == (f_lo > 0):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def contour_segments(X, Y, Z, level):
    """The paths of one contour level, computed on a throwaway figure."""
    fig, ax = plt.subplots()
    cs = ax.contour(X, Y, Z, levels=[level])
    segs = [s for s in cs.allsegs[0] if len(s) > 2]
    plt.close(fig)
    return segs


# ------------------------------------------------------------------ the models
G, KT, RHO0 = 32.174, 1.6878, 0.002378          # ft/s2, ft/s per knot, slug/ft3
T0R, P0 = 518.67, 2116.22                       # sea-level temperature (deg R) and pressure (lbf/ft2)


def isa(h, dT=0.0):
    """Standard atmosphere at the pressure altitude h (ft), to 65,617 ft; dT is the temperature
    offset in deg R. Returns temperature, pressure, density and the speed of sound (ft/s)."""
    h = np.asarray(h, dtype=float)
    hc = np.minimum(h, 36089.0)
    t_std = T0R - 0.00356616 * hc
    p = P0 * (t_std / T0R) ** 5.2559 * np.exp(-np.maximum(h - 36089.0, 0) / 20806.0)
    t = t_std + dT
    return t, p, p / (1716.5 * t), np.sqrt(1.4 * 1716.5 * t)


# Learjet 45: Gudmundsson (2022), Table 17-8
S, K, CD0, CLMAX = 311.6, 0.05236, 0.0200, 1.527
FSL, TR = 7000.0, 1.072


def thrust(h, mach, rating="mil", dT=0.0):
    """Mattingly low-bypass turbofan, Gudmundsson Eqs. 14-75 (maximum) and 14-77 (military), lbf."""
    t, p, _, _ = isa(h, dT)
    th0 = t / T0R * (1 + 0.2 * mach ** 2)
    de0 = p / P0 * (1 + 0.2 * mach ** 2) ** 3.5
    f, c = (0.6, 3.8) if rating == "mil" else (1.0, 3.5)
    return f * FSL * de0 * np.where(th0 <= TR, 1.0, 1 - c * (th0 - TR) / th0)


def drag(V, rho, W, n=1.0):
    q = 0.5 * rho * V ** 2
    return q * S * CD0 + K * (n * W) ** 2 / (q * S)


def v_md(W, rho):
    return np.sqrt(2 * W / (rho * S) * np.sqrt(K / CD0))


def mach_from_kcas(kcas, h):
    """Compressible: impact pressure from the calibrated airspeed, then the Mach number at altitude."""
    qc = P0 * ((1 + 0.2 * (kcas / 661.48) ** 2) ** 3.5 - 1)
    p = isa(h)[1]
    return float(np.sqrt(5 * ((qc / p + 1) ** (2 / 7) - 1)))


def published_checks():
    """The model reproduces the published answers of Gudmundsson's examples."""
    close(float(thrust(0.0, 250 * KT / isa(0)[3])), 4635, 3, "military thrust at 250 KCAS, Ex. 19-1")
    close(1 / np.sqrt(4 * K * CD0), 15.45, 0.01, "(L/D)max, Ex. 19-4")
    close(np.sqrt(CD0 / K), 0.6180, 0.0005, "C_L of (L/D)max, Ex. 20-5")
    close(2 * 20000 * np.sqrt(K * CD0), 1294, 1, "minimum thrust, Ex. 20-6")
    close(0.75 * (1 / (3 * K * CD0 ** 3)) ** 0.25, 22.40, 0.01, "max range ratio, Ex. 20-8")
    close(v_md(20000, 0.0008897), 483.2, 0.5, "V_TRmin, Ex. 20-6")


published_checks()


# ------------------------------------------------------- the trainer drawing
def _trainer_side(ax, x, y, s, pitch=0.0, right=True, gear=False, z=2.0):
    """The Lecture 10 side view with its CG (mid length, on the axis) at (x, y), length 10 s,
    flying to the right (or left) and pitched nose up by pitch degrees."""
    n_p, n_l = len(ax.patches), len(ax.lines)
    if gear:        # wheels down for the runway: both touch the ground 1.22 s below the axis
        for xg, yc, r in ((1.55, -1.02, 0.20), (5.7, -0.98, 0.24)):
            ax.plot([xg, xg], [-0.3, yc], color=STEEL, lw=1.0, zorder=z - 0.1)
            ax.add_patch(Circle((xg, yc), r, fc=STEEL, ec=INK, lw=0.5, zorder=z + 0.7))
    msf._side_view(ax, z=z)
    tr = (Affine2D().translate(-5.0, 0.0).scale(-s if right else s, s)
          .rotate_deg(pitch if right else -pitch).translate(x, y) + ax.transData)
    for art in ax.patches[n_p:] + ax.lines[n_l:]:
        art.set_transform(tr)


def _trainer_rear(ax, x, y, s, bank=0.0, z=2.0):
    """The Lecture 10 view from behind, centered at (x, y), banked right wing down by bank degrees."""
    n_p, n_l = len(ax.patches), len(ax.lines)
    msf._rear_view(ax, gamma=4.0, z=z)
    tr = Affine2D().scale(s, s).rotate_deg(-bank).translate(x, y) + ax.transData
    for art in ax.patches[n_p:] + ax.lines[n_l:]:
        art.set_transform(tr)


def _force(ax, tip, label, color, off, origin=(0.0, 0.0), fs=13):
    tip = np.asarray(tip, float) + np.asarray(origin, float)
    ax.annotate("", xy=tuple(tip), xytext=origin, arrowprops=dict(color=color, **ARROW), zorder=6)
    ax.text(tip[0] + off[0], tip[1] + off[1], label, fontsize=fs, ha="center", va="center", zorder=7)


def _arc(ax, r, a0, a1, c=(0.0, 0.0), color=STEEL, lw=1.1):
    th = np.radians(np.linspace(a0, a1, 40))
    ax.plot(c[0] + r * np.cos(th), c[1] + r * np.sin(th), color=color, lw=lw, zorder=5)


# ------------------------------------------------ page 1, level flight and range
def sizing_check_flow():
    """Inputs, point performance, mission, field, envelopes, compare, back to sizing."""
    fig, ax = plt.subplots(figsize=(10.4, 3.5))
    ax.axis("off")
    w, hgt, gap, y1, y0 = 2.3, 1.3, 0.5, 1.95, 0.0
    wide = 3.7
    x = [i * (w + gap) for i in range(4)]
    boxes = [("Inputs", "polars, engine deck,\nweights, $S$", x[0], y1, w, True),
             ("Point performance", "speeds, climb,\n$P_s$, turns", x[1], y1, w, False),
             ("Mission", "segment by segment,\nfuel", x[2], y1, w, False),
             ("Field", "takeoff, critical field,\nlanding", x[3], y1, w, False),
             ("Envelopes", "flight envelope,\nV-n diagram", x[3], y0, w, False),
             ("Compare", "with every requirement:\nmargin or shortfall", x[3] - gap - wide, y0, wide, True),
             ("Back to sizing", "ASORT,\nconstraint diagram", x[3] - 2 * gap - wide - w, y0, w, False)]
    for title, sub, bx, by, bw, gold in boxes:
        ax.add_patch(FancyBboxPatch((bx, by), bw, hgt, boxstyle="round,pad=0.02,rounding_size=0.08",
                                    fc=DUST if gold else LIGHT, ec=STEEL, lw=1.0))
        ax.text(bx + bw / 2, by + 1.0, title, ha="center", va="center", fontsize=10.5, fontweight="bold")
        ax.text(bx + bw / 2, by + 0.45, sub, ha="center", va="center", fontsize=10)
    arrows = []
    for i in range(3):                                      # along the top row, left to right
        arrows.append(((boxes[i][2] + w + 0.03, y1 + hgt / 2), (boxes[i + 1][2] - 0.03, y1 + hgt / 2)))
    arrows.append(((x[3] + w / 2, y1 - 0.03), (x[3] + w / 2, y0 + hgt + 0.03)))     # Field down to Envelopes
    for i in (4, 5):                                        # along the bottom row, right to left
        arrows.append(((boxes[i][2] - 0.03, y0 + hgt / 2), (boxes[i + 1][2] + boxes[i + 1][4] + 0.03, y0 + hgt / 2)))
    for p0, p1 in arrows:
        ax.annotate("", xy=p1, xytext=p0, arrowprops=dict(arrowstyle="-|>", color=STEEL, lw=1.2))

    def inside(p, b):                                       # which box an arrow end touches
        return b[2] - 0.05 <= p[0] <= b[2] + b[4] + 0.05 and b[3] - 0.05 <= p[1] <= b[3] + hgt + 0.05
    chain = [(next(i for i, b in enumerate(boxes) if inside(p0, b)), next(i for i, b in enumerate(boxes) if inside(p1, b)))
             for p0, p1 in arrows]
    assert chain == [(i, i + 1) for i in range(6)], chain   # one path through the seven boxes, in order
    ax.set_xlim(-0.2, x[3] + w + 0.2)
    ax.set_ylim(-0.15, y1 + hgt + 0.15)
    save(fig, "sizing-check-flow")


def _free_body(name, gamma, eps, T, W, xlim, ylim, path_label, figsize=(7.4, 4.9)):
    """Point-mass forces in the vertical plane, drawn in steady flight: the flight path at gamma to
    the horizon (deg, negative in a descent), thrust at eps above the path, lift normal to the path,
    drag along it, weight down. The trainer lies along the flight path, as in Lecture 9."""
    g, e = math.radians(gamma), math.radians(eps)
    t = np.array([math.cos(g), math.sin(g)])                # along the flight path
    n = np.array([-t[1], t[0]])                             # normal to it, up
    D = T * math.cos(e) - W * math.sin(g)                   # the steady equations give the two lengths
    L = W * math.cos(g) - T * math.sin(e)
    u_t = np.array([math.cos(g + e), math.sin(g + e)])      # along the thrust
    tips = {"T": T * u_t, "D": -D * t, "L": L * n, "W": np.array([0.0, -W])}
    # every drawn force is checked for direction, and the four close the polygon of steady flight
    length = {k: float(np.linalg.norm(v)) for k, v in tips.items()}
    assert abs(tips["L"] @ t) < 1e-9 and tips["L"] @ n > 0, "lift normal to the path, upward"
    assert abs(tips["D"] @ n) < 1e-9 and tips["D"] @ t < 0, "drag along the path, aft"
    assert tips["W"][0] == 0 and tips["W"][1] < 0, "weight straight down"
    close(math.degrees(math.atan2(t[0] * tips["T"][1] - t[1] * tips["T"][0], tips["T"] @ t)), eps, 1e-9,
          "thrust above the path by epsilon")
    close(math.degrees(math.atan2(t[1], t[0])), gamma, 1e-9, "flight path above the horizon by gamma")
    close(float(np.linalg.norm(sum(tips.values()))), 0.0, 1e-9, "the drawn forces balance")
    close(length["T"] * math.cos(e) - length["D"] - length["W"] * math.sin(g), 0.0, 1e-9, "along the path")
    close(length["T"] * math.sin(e) + length["L"] - length["W"] * math.cos(g), 0.0, 1e-9, "normal to the path")

    fig, ax = sketch(figsize)
    if gamma:
        ax.plot([xlim[0] + 0.2, 4.75], [0, 0], color=GRAY, lw=1.0, ls="--")
        ax.text(4.75, 0.1 if gamma < 0 else -0.1, "horizon", fontsize=10, color=STEEL, ha="right",
                va="bottom" if gamma < 0 else "top")
    r_path = 3.3
    ax.plot([-3.2 * t[0], r_path * t[0]], [-3.2 * t[1], r_path * t[1]], color=STEEL, lw=1.0, ls="--")
    ax.annotate("", xy=tuple(4.5 * t), xytext=tuple(r_path * t), arrowprops=dict(arrowstyle="-|>", color=STEEL, lw=1.4))
    ax.text(*(4.72 * t), "$V$", fontsize=13, ha="center", va="center")
    ax.text(*(-3.2 * t - 0.14 * n), path_label, fontsize=10, color=STEEL, ha="left", va="top", rotation=gamma,
            rotation_mode="anchor")
    _trainer_side(ax, 0.0, 0.0, 0.34, pitch=gamma)
    off = {"T": 0.26 * u_t + 0.06 * n, "D": 0.27 * n + 0.1 * t, "L": -0.27 * t - 0.05 * n, "W": np.array([-0.3, 0.1])}
    if eps == 0:
        off["T"] = 0.3 * n - 0.15 * t
    for key, color in (("T", VERM), ("D", INK), ("L", BLUE), ("W", GREEN)):
        _force(ax, tips[key], f"${key}$", color, off[key])
    ax.plot(0, 0, "o", color=INK, ms=5, zorder=8)
    if eps:
        _arc(ax, 2.15, gamma, gamma + eps)
        mid = math.radians(gamma + eps / 2)
        ax.text(2.45 * math.cos(mid), 2.45 * math.sin(mid), r"$\varepsilon$", fontsize=13, ha="center", va="center")
    if gamma:
        _arc(ax, 3.75, 0, gamma)
        mid = math.radians(gamma / 2)
        ax.text(4.08 * math.cos(mid), 4.08 * math.sin(mid), r"$\gamma$" if gamma > 0 else r"$\gamma_d$", fontsize=13,
                ha="center", va="center")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    save(fig, name)


def eom_cruise():
    """Level flight: L and W vertical, D aft, T at epsilon above the flight path."""
    _free_body("eom-cruise", 0.0, 16.0, 2.7, 2.4, (-3.5, 5.0), (-2.8, 2.2), "flight path, horizontal")


def eom_climb():
    """Climb: the flight path above the horizon by gamma."""
    _free_body("eom-climb", 18.0, 16.0, 3.0, 2.6, (-3.5, 5.0), (-3.0, 2.8), "flight path")


def eom_descent():
    """Descent: the flight path below the horizon by gamma_d; thrust along the path."""
    _free_body("eom-descent", -16.0, 0.0, 2.2, 2.2, (-3.5, 5.0), (-2.7, 2.8), "flight path")


def eom_maneuver():
    """Level turn seen from behind, and pull-up seen from the side."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 4.8))
    for ax in (a1, a2):
        ax.set_aspect("equal")
        ax.axis("off")
    # level turn: banked right wing down by phi, the center of the turn to the right
    phi, W = 35.0, 2.0
    p = math.radians(phi)
    L = W / math.cos(p)
    tip_l, tip_w = L * np.array([math.sin(p), math.cos(p)]), np.array([0.0, -W])
    center_dir = 1.0                                        # +x: toward the low wing
    close(tip_l[1] + tip_w[1], 0.0, 1e-9, "L cos(phi) = W: no vertical acceleration in the level turn")
    assert (tip_l + tip_w)[0] * center_dir > 0, "the horizontal part of the lift points to the center"
    close(math.degrees(math.atan2(tip_l[0], tip_l[1])), phi, 1e-9, "lift tilted from the vertical by the bank angle")
    a1.plot([-2.9, 3.3], [0, 0], color=GRAY, lw=1.0, ls="--")
    a1.plot([0, 0], [0, 2.9], color=STEEL, lw=1.0, ls=":")
    _trainer_rear(a1, 0.0, 0.0, 0.62, bank=phi)
    _force(a1, tip_l, "$L$", BLUE, (0.22, 0.12))
    _force(a1, tip_w, "$W$", GREEN, (-0.3, 0.1))
    _arc(a1, 1.75, 90 - phi, 90)
    a1.text(2.0 * math.sin(p / 2), 2.0 * math.cos(p / 2), r"$\phi$", fontsize=13, ha="center", va="center")
    a1.annotate("", xy=(3.3, -1.7), xytext=(0.9, -1.7), arrowprops=dict(arrowstyle="-|>", color=STEEL, lw=1.3))
    a1.text(2.1, -1.88, "radius $r$ to the center\nof the turn", fontsize=10.5, ha="center", va="top")
    a1.text(0.0, -3.1, "level turn, seen from behind", fontsize=11, ha="center", va="center")
    a1.set_xlim(-3.1, 3.6)
    a1.set_ylim(-3.3, 3.1)
    # pull-up: wings level at the bottom of the arc, the center above
    R, Wp, Lp, Tp = 3.6, 1.1, 2.2, 2.0
    forces = {"L": np.array([0.0, Lp]), "W": np.array([0.0, -Wp]), "T": np.array([Tp, 0.0]), "D": np.array([-Tp, 0.0])}
    net = sum(forces.values())
    center = np.array([0.0, R])
    assert abs(net[0]) < 1e-9 and net[1] * center[1] > 0, "L - W points to the center of the arc"
    assert Lp / Wp > 1, "load factor above 1 in the pull-up"
    th = np.radians(np.linspace(222, 318, 80))
    a2.plot(center[0] + R * np.cos(th), center[1] + R * np.sin(th), color=STEEL, lw=1.1, ls="--", zorder=1)
    a2.plot(*center, "o", color=STEEL, ms=5)
    a2.text(center[0] - 0.15, center[1] + 0.02, "center of the arc", fontsize=10.5, ha="right", va="center")
    end = center + R * np.array([math.cos(math.radians(310)), math.sin(math.radians(310))])
    a2.plot([center[0], end[0]], [center[1], end[1]], color=STEEL, lw=1.0)
    a2.text((center[0] + end[0]) / 2 + 0.2, (center[1] + end[1]) / 2 + 0.12, "$r$", fontsize=13, ha="center", va="center")
    _trainer_side(a2, 0.0, 0.0, 0.26)
    _force(a2, forces["L"], "$L$", BLUE, (-0.25, -0.1))
    _force(a2, forces["W"], "$W$", GREEN, (-0.3, 0.1))
    _force(a2, forces["T"], "$T$", VERM, (-0.05, -0.3))
    _force(a2, forces["D"], "$D$", INK, (0.05, -0.3))
    a2.plot(0, 0, "o", color=INK, ms=5, zorder=8)
    a2.text(0.0, -2.0, "pull-up, seen from the side", fontsize=11, ha="center", va="center")
    a2.set_xlim(-3.3, 3.4)
    a2.set_ylim(-2.2, 4.2)
    fig.tight_layout()
    save(fig, "eom-maneuver")


LEVELS = [(0.0, "sea level", BLUE, "-"), (15000.0, "15,000 ft", GREEN, "--"), (30000.0, "30,000 ft", VERM, "-.")]


def drag_power():
    """Learjet 45 at 20,000 lb: drag and power required at three altitudes."""
    W = 20000.0
    kt = np.linspace(120, 560, 881)
    V = kt * KT
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.4, 4.5))
    pmin = {}
    for h, name, color, ls in LEVELS:
        rho = float(isa(h)[2])
        D = drag(V, rho, W)
        P = D * V / 550
        i, j = int(np.argmin(D)), int(np.argmin(P))
        vm = v_md(W, rho) / KT
        close(D[i], 1294, 1, f"minimum drag at {h:.0f} ft")
        close(kt[i], vm, 0.5, "the drag curve bottoms at V_md")
        close(kt[j], vm / 3 ** 0.25, 0.5, "the power curve bottoms at V_md / 3^(1/4)")
        pmin[h] = P[j]
        a1.plot(kt, D, color=color, lw=2.0, ls=ls, label=name)
        a2.plot(kt, P, color=color, lw=2.0, ls=ls, label=name)
        a1.plot(kt[i], D[i], "o", color=INK, ms=6, zorder=5)
        a2.plot(kt[j], P[j], "o", color=INK, ms=6, zorder=5)
    close(pmin[0.0], 610, 1, "minimum power at sea level, hp")
    close(pmin[30000.0], 998, 1, "minimum power at 30,000 ft, hp")
    assert pmin[0.0] < pmin[15000.0] < pmin[30000.0], "minimum power rises with altitude"
    a1.annotate("$D_{min}$ = 1,294 lbf\nat every altitude", xy=(235, 1294), xytext=(300, 420), fontsize=10.5, ha="center",
                va="center", arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8, shrinkB=4))
    a2.annotate(f"{pmin[0.0]:,.0f} hp", xy=(kt[0] + 13, pmin[0.0]), xytext=(175, 180), fontsize=10.5, ha="center", va="center",
                arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8, shrinkB=4))
    a2.annotate(f"{pmin[30000.0]:,.0f} hp", xy=(v_md(W, float(isa(30000)[2])) / KT / 3 ** 0.25, pmin[30000.0]), xytext=(300, 330),
                fontsize=10.5, ha="center", va="center", arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8, shrinkB=4))
    for ax, top, lab in ((a1, 6000, "Drag $D$ (lbf)"), (a2, 5000, "Power required $P_{req}$ (hp)")):
        ax.set_xlim(120, 560)
        ax.set_ylim(0, top)
        ax.set_xlabel("True airspeed (KTAS)")
        ax.set_ylabel(lab)
        thousands(ax)
        clean(ax)
    a1.legend(frameon=False, fontsize=10.5, loc="upper center")
    fig.tight_layout()
    save(fig, "drag-power")


def _level_speeds_30k():
    """V_S, V_min, V_md, V_BR and V_H (KTAS) and the Mach number of V_H: 20,000 lb, 30,000 ft, military thrust."""
    W, h = 20000.0, 30000.0
    _, _, rho, a = isa(h)
    kt = np.linspace(140, 560, 841)
    V = kt * KT
    D, T = drag(V, rho, W), thrust(h, V / a)
    diff = T - D
    idx = np.where(np.diff(np.sign(diff)) != 0)[0]
    cross = [kt[i] + (kt[i + 1] - kt[i]) * diff[i] / (diff[i] - diff[i + 1]) for i in idx]
    assert len(cross) == 2, "thrust meets drag twice"
    vs = np.sqrt(2 * W / (rho * S * CLMAX)) / KT
    vm = kt[int(np.argmin(D))]
    close(vm, v_md(W, rho) / KT, 0.5, "the drag curve bottoms at V_md")
    speeds = dict(VS=float(vs), Vmin=cross[0], Vmd=float(v_md(W, rho) / KT), VBR=float(v_md(W, rho) / KT * 3 ** 0.25), VH=cross[1])
    return kt, D, T, speeds, cross[1] * KT / float(a)


def level_speeds():
    """Drag and military thrust at 30,000 ft with the five level-flight speeds."""
    kt, D, T, v, mach_h = _level_speeds_30k()
    for key, book in (("VS", 182), ("Vmin", 236), ("Vmd", 286), ("VBR", 377), ("VH", 441)):
        close(v[key], book, 0.5, f"{key} at 30,000 ft, KTAS")
    close(mach_h, 0.75, 0.005, "Mach number of V_H")
    assert v["VS"] < v["Vmin"] < v["Vmd"] < v["VBR"] < v["VH"], "V_min is thrust limited, above V_S"
    fig, ax = plt.subplots(figsize=(8.4, 4.7))
    ax.plot(kt, D, color=INK, lw=2.2)
    ax.plot(kt, T, color=BLUE, lw=2.2, ls="--")
    ax.text(552, float(np.interp(552, kt, D)) + 130, "drag", fontsize=11, ha="right", va="bottom")
    ax.text(556, float(np.interp(540, kt, T)) - 190, "military thrust", fontsize=11, ha="right", va="top")
    for key, sym in (("VS", "$V_S$"), ("Vmin", "$V_{min}$"), ("Vmd", "$V_{md}$"), ("VBR", "$V_{BR}$"), ("VH", "$V_H$")):
        ax.plot([v[key]] * 2, [0, 3300], color=GRAY, lw=1.0, ls=":")
        ax.text(v[key], 3360, f"{sym}\n{v[key]:.0f}", fontsize=11, ha="center", va="bottom", linespacing=1.25)
    for key in ("Vmin", "VH"):
        ax.plot(v[key], float(np.interp(v[key], kt, D)), "o", color=INK, ms=6, zorder=5)
    ax.set_xlim(140, 560)
    ax.set_ylim(0, 4000)
    ax.set_yticks(range(0, 3001, 1000))
    ax.set_xlabel("True airspeed (KTAS)")
    ax.set_ylabel("Force (lbf)")
    thousands(ax)
    clean(ax)
    fig.tight_layout()
    save(fig, "level-speeds")


def range_endurance():
    """L/D and V L/D as fractions of their maxima: the endurance and range speeds of a jet."""
    W = 20000.0
    rho = float(isa(30000.0)[2])
    kt = np.linspace(160, 560, 801)
    V = kt * KT
    CL = W / (0.5 * rho * V ** 2 * S)
    LD = CL / (CD0 + K * CL ** 2)
    VLD = V * LD
    i, j = int(np.argmax(LD)), int(np.argmax(VLD))
    close(kt[i], 286, 0.5, "L/D peaks at V_md, KTAS")
    close(kt[j], 377, 0.5, "V L/D peaks at V_BR, KTAS")
    close(kt[j] / kt[i], 3 ** 0.25, 0.005, "V_BR = 1.316 V_md")
    close(LD[j] / LD[i], 0.866, 0.0005, "L/D at V_BR as a fraction of the maximum")
    close(LD[i], 15.45, 0.01, "(L/D)max")
    fig, ax = plt.subplots(figsize=(8.0, 4.7))
    ax.plot(kt, LD / LD[i], color=BLUE, lw=2.2)
    ax.plot(kt, VLD / VLD[j], color=VERM, lw=2.2, ls="--")
    ax.text(505, 0.50, "$L/D$: endurance", fontsize=11, ha="right", va="center")
    ax.text(548, 0.97, "$V\\,L/D$: range", fontsize=11, ha="right", va="bottom")
    for x, sym in ((kt[i], "$V_{md}$"), (kt[j], "$V_{BR}$")):
        ax.plot([x, x], [0.25, 1.0], color=GRAY, lw=1.0, ls=":")
        ax.text(x + 5, 0.275, sym, fontsize=11, ha="left", va="bottom")
    ax.plot(kt[i], 1.0, "o", color=INK, ms=6, zorder=5)
    ax.plot(kt[j], 1.0, "o", color=INK, ms=6, zorder=5)
    ax.plot(kt[j], LD[j] / LD[i], "o", color=INK, mfc="white", ms=6, mew=1.4, zorder=5)
    ax.annotate(f"{LD[j] / LD[i]:.3f}", xy=(kt[j], LD[j] / LD[i]), xytext=(kt[j] + 38, 0.73), fontsize=10.5, ha="center",
                va="center", arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8, shrinkB=4))
    ax.set_xlim(160, 560)
    ax.set_ylim(0.25, 1.1)
    ax.set_xlabel("True airspeed (KTAS)")
    ax.set_ylabel("Fraction of the maximum")
    clean(ax)
    fig.tight_layout()
    save(fig, "range-endurance")


# -------------------------------------------- page 2, climb and field performance
def climb_learjet():
    """Rate of climb and climb angle at sea level: thrust held constant, and the military rating."""
    W = 20000.0
    _, _, rho, a = isa(0.0)
    rho, a = float(rho), float(a)
    ws, T0 = W / S, 4635.0
    tw = T0 / W
    vy = np.sqrt(tw * ws / (3 * RHO0 * CD0) * (1 + np.sqrt(1 + 3 * 4 * K * CD0 / tw ** 2)))
    close(vy, 469.1, 0.5, "V_Y, Ex. 19-4")
    gopt = np.degrees(np.arcsin(tw - np.sqrt(4 * CD0 * K)))
    close(gopt, 9.62, 0.01, "gamma_opt, Ex. 19-7")
    close(np.sqrt(2 / RHO0 * ws * np.sqrt(K / CD0) * np.cos(np.radians(gopt))), 293.5, 0.3, "V_X, Ex. 19-7")
    kc = np.linspace(110, 380, 541)
    V = kc * KT
    out, curves = {}, {}
    for key, T in (("c", np.full_like(V, T0)), ("l", thrust(0.0, V / a))):
        sg = (T - drag(V, rho, W)) / W
        for _ in range(3):                                  # lift = W cos(gamma), Gudmundsson Eq. 19-6
            sg = (T - drag(V, rho, W, np.sqrt(1 - sg ** 2))) / W
        roc, gam = V * sg * 60, np.degrees(np.arcsin(sg))
        out[key] = (kc[np.argmax(gam)], gam.max(), kc[np.argmax(roc)], roc.max())
        curves[key] = (roc, gam)
    for key, book in (("c", (174, 9.7, 278, 3874)), ("l", (192, 9.1, 326, 4180))):
        close(out[key][0], book[0], 0.5, "V_X, KCAS")
        close(out[key][1], book[1], 0.05, "best climb angle, deg")
        close(out[key][2], book[2], 0.5, "V_Y, KCAS")
        close(out[key][3], book[3], 1.0, "best rate of climb, ft/min")
    close(out["c"][2], vy / KT, 1, "V_Y of the curve against the closed form, Ex. 19-4")
    close(out["l"][3] / out["c"][3], 1.08, 0.005, "the rate rises 8% with the military rating")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.6, 4.6))
    style = (("c", "$T$ held at 4,635 lbf", BLUE, "-"), ("l", "military rating, Mattingly model", VERM, "--"))
    for key, name, color, ls in style:
        a1.plot(kc, curves[key][0], color=color, lw=2.0, ls=ls, label=name)
        a2.plot(kc, curves[key][1], color=color, lw=2.0, ls=ls, label=name)
        a1.plot(out[key][2], out[key][3], "o", color=color, mec=INK, mew=0.8, ms=7, zorder=5)
        a2.plot(out[key][0], out[key][1], "s", color=color, mec=INK, mew=0.8, ms=7, zorder=5)
    a1.annotate(f"$V_Y$ {out['c'][2]:.0f} KCAS\n{out['c'][3]:,.0f} ft/min", xy=(out["c"][2], out["c"][3]), xytext=(232, 2500),
                fontsize=10.5, ha="center", va="center", arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8, shrinkB=5))
    a1.annotate(f"$V_Y$ {out['l'][2]:.0f} KCAS\n{out['l'][3]:,.0f} ft/min", xy=(out["l"][2], out["l"][3]), xytext=(326, 5150),
                fontsize=10.5, ha="center", va="center", arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8, shrinkB=5))
    a2.annotate(f"$V_X$ {out['c'][0]:.0f} KCAS, {out['c'][1]:.1f}°", xy=(out["c"][0], out["c"][1]), xytext=(190, 11.1),
                fontsize=10.5, ha="center", va="center", arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8, shrinkB=5))
    a2.annotate(f"$V_X$ {out['l'][0]:.0f} KCAS, {out['l'][1]:.1f}°", xy=(out["l"][0], out["l"][1]), xytext=(215, 7.0),
                fontsize=10.5, ha="center", va="center", arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8, shrinkB=5))
    for ax, top, lab in ((a1, 6000, "Rate of climb (ft/min)"), (a2, 12, "Climb angle $\\gamma$ (deg)")):
        ax.set_xlim(110, 380)
        ax.set_ylim(0, top)
        ax.set_xlabel("Calibrated airspeed at sea level (KCAS)")
        ax.set_ylabel(lab)
        clean(ax)
    thousands(a1)
    h, l = a1.get_legend_handles_labels()
    fig.legend(h, l, frameon=False, fontsize=10.5, ncol=2, loc="lower center", bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, "climb-learjet")


def takeoff_speeds():
    """The takeoff run and the speeds along it; after Gudmundsson (2022), Figure 18-4."""
    s = 0.15                                                # trainer length 1.5
    y_g = 1.22 * s                                          # height of the axis with the wheels on the runway
    x_lof, x_2, theta, rad = 7.2, 9.8, math.radians(17.0), 4.2
    marks = [(0.4, "$V$ = 0"), (3.7, "$V_S$"), (4.5, "$V_{MC}$"), (5.5, "$V_1$"), (6.1, "$V_R$"), (6.7, "$V_{MU}$"),
             (x_lof, "$V_{LOF}$"), (x_2, "$V_2$")]

    def path(x):                                            # the axis of the aircraft: runway, arc, straight climb
        x = np.asarray(x, float)
        x_t = x_lof + rad * math.sin(theta)
        arc = y_g + rad - np.sqrt(np.clip(rad ** 2 - (x - x_lof) ** 2, 0, None))
        line = y_g + rad * (1 - math.cos(theta)) + (x - x_t) * math.tan(theta)
        return np.where(x <= x_lof, y_g, np.where(x <= x_t, arc, line))

    xs = [m[0] for m in marks]
    assert xs == sorted(xs) and len(set(xs)) == len(xs), "the speeds follow one another along the run"
    assert all(float(path(x)) == y_g for x in xs[:-1]) and float(path(x_lof + 0.05)) > y_g, "airborne after V_LOF"
    pitch_2 = math.degrees(theta) + 4.0                     # deck angle in the climb: path angle plus angle of attack
    c2, s2 = math.cos(math.radians(pitch_2)), math.sin(math.radians(pitch_2))
    wheel = np.array([x_2, float(path(x_2))]) + s * np.array([-0.7 * c2 + 1.22 * s2, -0.7 * s2 - 1.22 * c2])
    h_obst = float(wheel[1])                                # the main wheels clear the obstacle height at V_2
    assert 0.3 < h_obst < float(path(x_2))
    fig, ax = sketch((10.6, 3.3))
    ax.add_patch(Rectangle((-0.45, -0.3), 11.35, 0.3, fc=DUST, ec="none"))
    ax.plot([-0.45, 10.9], [0, 0], color=INK, lw=1.4)
    xx = np.linspace(0.4, 10.75, 300)
    ax.plot(xx, path(xx), color=BLUE, lw=1.6, ls="--", zorder=1)
    _trainer_side(ax, 0.4 + 0.7 * s, y_g, s, gear=True)     # main wheels on the brake-release mark
    _trainer_side(ax, 6.85, y_g + 0.045, s, pitch=7.0, gear=True)
    _trainer_side(ax, x_2, float(path(x_2)), s, pitch=pitch_2, gear=True)
    for x, lab in marks:
        ax.plot([x, x], [-0.04, -0.42], color=STEEL, lw=1.0)
        ax.text(x, -0.48, lab, fontsize=11.5, ha="center", va="top")
    ax.text(0.4, -0.86, "brake release", fontsize=10, ha="center", va="top", color=STEEL)
    ax.text(6.1, -0.86, "rotation", fontsize=10, ha="center", va="top", color=STEEL)
    ax.text(x_lof, -0.86, "liftoff", fontsize=10, ha="center", va="top", color=STEEL)
    ax.text(x_2, -0.86, "obstacle height", fontsize=10, ha="center", va="top", color=STEEL)
    xd = 10.72
    ax.plot([wheel[0] + 0.06, xd + 0.1], [h_obst, h_obst], color=STEEL, lw=0.8, ls=":")
    ax.annotate("", xy=(xd, h_obst), xytext=(xd, 0), arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1.0))
    ax.text(xd + 0.1, h_obst / 2, "$h_{obst}$", fontsize=11.5, ha="left", va="center")
    ax.set_xlim(-0.55, 11.5)
    ax.set_ylim(-1.15, 1.75)
    save(fig, "takeoff-speeds")


EX185 = dict(W=21500.0, CLTO=0.90, CDTO=0.045, CLmax=1.65, T=7000.0, mu=0.02, VR=206.7)


def ground_run():
    """Gudmundsson (2022), Example 18-5: the ground run integrated and with the average acceleration."""
    e = EX185
    W, T, mu, vr = e["W"], e["T"], e["mu"], e["VR"]         # V_R as printed and carried; the inputs give 206.3 ft/s
    close(1.556 * np.sqrt(W / (RHO0 * S * e["CLmax"])), vr, 0.5, "V_R, Ex. 18-5")
    acc = lambda v: G / W * (T - 0.5 * RHO0 * v ** 2 * S * e["CDTO"] - mu * (W - 0.5 * RHO0 * v ** 2 * S * e["CLTO"]))
    a_avg = acc(vr / np.sqrt(2))
    close(a_avg, 9.511, 0.005, "average acceleration, Ex. 18-5")
    sg = vr ** 2 / (2 * a_avg)
    close(sg, 2246, 2, "S_G with the average acceleration, Ex. 18-5")
    dt, v, s, t = 0.25, 0.0, 0.0, 0.0
    vv, ss, tt = [0.0], [0.0], [0.0]
    while v < vr:
        a = acc(v)
        s += v * dt + 0.5 * a * dt ** 2
        v += a * dt
        t += dt
        vv.append(v)
        ss.append(s)
        tt.append(t)
    sg_num = float(np.interp(vr, vv, ss))
    t_num = float(np.interp(vr, vv, tt))
    close(sg_num, 2246, 1, "S_G integrated, ft")
    close(t_num, 21.5, 0.05, "time to V_R, s")
    close(t, 21.5, 1e-9, "the first step at or above V_R")
    close(sg_num / sg, 1.0, 0.001, "the two methods agree at constant thrust")
    close(vr / KT, 122, 0.5, "V_R, KCAS")
    fig, ax = plt.subplots(figsize=(8.2, 4.5))
    sa = np.linspace(0, sg, 80)
    keep = np.array(ss) <= sg_num
    ax.plot(np.append(np.array(ss)[keep], sg_num), np.append(np.array(vv)[keep], vr) / KT, color=BLUE, lw=3.2,
            label=f"integrated: {sg_num:,.0f} ft, {t_num:.1f} s")
    ax.plot(sa, np.sqrt(2 * a_avg * sa) / KT, color=VERM, lw=1.6, ls="--", label=f"average acceleration: {sg:,.0f} ft")
    ax.plot([0, 2500], [vr / KT] * 2, color=GRAY, lw=1.0, ls=":")
    ax.text(60, vr / KT + 2.5, f"$V_R$ = {vr / KT:.0f} KCAS", fontsize=11, ha="left", va="bottom")
    ax.plot(sg_num, vr / KT, "o", color=INK, ms=6, zorder=5)
    ax.set_xlim(0, 2500)
    ax.set_ylim(0, 140)
    ax.set_xlabel("Ground distance (ft)")
    ax.set_ylabel("Calibrated airspeed (KCAS)")
    thousands(ax, "x")
    clean(ax)
    ax.legend(frameon=False, fontsize=10.5, loc="lower right")
    fig.tight_layout()
    save(fig, "ground-run")


def balanced_field():
    """Airspeed against distance: all engines, continue with an engine out, stop. After
    Gudmundsson (2022), Figures 18-16 and 18-17. Each branch is a constant acceleration, so the
    square of the speed is a straight line in distance; invented scale."""
    s_lof, s_fail, s_bfl, v2 = 0.80, 0.42, 1.00, 1.10       # distance in balanced field lengths, speed in V_LOF
    x_all = s_lof * np.linspace(0, 1, 200) ** 2             # dense near brake release, where the curve is steep
    v_all = np.sqrt(x_all / s_lof)
    v1 = math.sqrt(s_fail / s_lof)
    x_br = s_bfl - (s_bfl - s_fail) * np.linspace(1, 0, 200) ** 2      # dense near the stop
    v_go = np.sqrt(v1 ** 2 + (v2 ** 2 - v1 ** 2) * (x_br - s_fail) / (s_bfl - s_fail))
    v_stop = np.sqrt(np.clip(v1 ** 2 * (1 - (x_br - s_fail) / (s_bfl - s_fail)), 0, None))
    close(float(np.interp(s_fail, x_all, v_all)), v_go[0], 1e-3, "the continue branch starts on the all-engines curve")
    close(v_go[0], v_stop[0], 1e-12, "the two branches start at the same point")
    close(v_go[-1], v2, 1e-9, "continue: V_2 reached at the balanced field length")
    close(v_stop[-1], 0.0, 1e-9, "stop: at rest at the balanced field length")
    assert x_br[-1] == s_bfl and np.all(np.diff(v_go) > 0) and np.all(np.diff(v_stop) < 0)
    slope_all = np.gradient(v_all ** 2, x_all)[100]
    slope_go = np.gradient(v_go ** 2, x_br)[100]
    assert 0 < slope_go < slope_all, "with an engine out the aircraft accelerates more slowly"
    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    ax.plot(x_all, v_all, color=BLUE, lw=2.4)
    ax.plot(x_br, v_go, color=VERM, lw=2.2, ls="--")
    ax.plot(x_br, v_stop, color=GREEN, lw=2.2, ls="-.")
    ax.plot([0, 1.06], [v2, v2], color=GRAY, lw=1.0, ls=":")
    ax.plot([s_bfl, s_bfl], [0, v2], color=GRAY, lw=1.0, ls=":")
    ax.plot(s_fail, v1, "o", color=INK, ms=7, zorder=5)
    ax.text(s_fail - 0.02, v1 + 0.04, "engine fails at $V_{EF}$,\ndecision at $V_1$", fontsize=10.5, ha="right", va="bottom")
    ax.text(0.60, 0.91, "all engines", fontsize=10.5, ha="right", va="bottom")
    ax.text(0.75, 0.86, "continue, engine out", fontsize=10.5, ha="left", va="top")
    ax.text(0.60, 0.33, "stop, brakes", fontsize=10.5, ha="right", va="center")
    ax.add_patch(Rectangle((0, -0.2), s_bfl, 0.08, fc=DUST, ec=STEEL, lw=0.8, clip_on=False))
    ax.text(s_bfl / 2, -0.16, "runway", fontsize=10, ha="center", va="center", clip_on=False)
    ax.annotate("", xy=(s_bfl, -0.29), xytext=(0, -0.29), arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1.0),
                annotation_clip=False)
    ax.text(s_bfl / 2, -0.32, "balanced field length: both branches end here", fontsize=10.5, ha="center", va="top",
            clip_on=False)
    ax.set_xlim(0, 1.1)
    ax.set_ylim(0, 1.25)
    ax.set_xticks([])
    ax.set_yticks([v1, 1.0, v2])
    ax.set_yticklabels(["$V_1$", "$V_{LOF}$", "$V_2$"])
    ax.plot([0, s_fail], [v1, v1], color=GRAY, lw=1.0, ls=":")
    ax.plot([0, s_lof], [1.0, 1.0], color=GRAY, lw=1.0, ls=":")
    ax.text(1.1, -0.025, "distance $S$", fontsize=11, ha="right", va="top", clip_on=False)
    ax.set_ylabel("Airspeed")
    clean(ax, grid=False)
    fig.tight_layout()
    save(fig, "balanced-field")


def sg_numeric(W, h, dTC=0.0, mu=0.02, CLTO=0.90, CDTO=0.045, CLM=1.65):
    """Ground run to V_R = 1.1 V_S (ft), integrated, at the maximum rating of the Mattingly model.
    dTC is the ISA temperature offset in deg C (isa() and thrust() take deg R)."""
    dT = 1.8 * dTC
    _, _, rho, a = isa(h, dT)
    vr = 1.556 * np.sqrt(W / (rho * S * CLM))
    dt, v, s = 0.1, 0.0, 0.0
    while True:
        q = 0.5 * rho * v ** 2
        acc = G / W * (thrust(h, v / a, "max", dT) - q * S * CDTO - mu * (W - q * S * CLTO))
        if v + acc * dt >= vr:
            tau = (vr - v) / acc
            return float(s + v * tau + 0.5 * acc * tau ** 2)
        s += v * dt + 0.5 * acc * dt ** 2
        v += acc * dt


def takeoff_altitude_weight():
    """Ground run against pressure altitude: three temperatures, three weights."""
    hs = np.linspace(0, 10000, 21)
    temp = {dT: np.array([sg_numeric(21500, h, dT) for h in hs]) for dT in (-20, 0, 20)}
    wts = {W: np.array([sg_numeric(W, h) for h in hs]) for W in (18000, 20000, 21500)}
    close(temp[0][0], 2209, 1, "ground run at sea level, ISA, 21,500 lb")
    close(temp[0][-1], 4530, 1, "ground run at 10,000 ft, ISA, 21,500 lb")
    close(temp[0][-1] / temp[0][0], 2.05, 0.05, "sea level to 10,000 ft")
    close(temp[20][-1] / temp[0][-1] * 100 - 100, 7, 0.5, "ISA plus 20 C at 10,000 ft, percent")
    assert np.all(temp[20] > temp[0]) and np.all(temp[0] > temp[-20]), "hotter is longer at every altitude"
    assert np.all(wts[21500] > wts[20000]) and np.all(wts[20000] > wts[18000]), "heavier is longer at every altitude"
    w_exp = np.log(wts[21500][0] / wts[18000][0]) / np.log(21500 / 18000)
    close(w_exp, 2.1, 0.05, "weight exponent of the ground run at sea level")
    close(float(np.max(np.abs(wts[21500] - temp[0]))), 0.0, 1e-9, "the two panels share the 21,500 lb ISA line")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.6, 4.6), sharey=True)
    a1.plot(temp[-20], hs, color=BLUE, lw=2.0, ls="-.", label="ISA − 20 °C")
    a1.plot(temp[0], hs, color=INK, lw=2.2, label="ISA")
    a1.plot(temp[20], hs, color=VERM, lw=2.0, ls="--", label="ISA + 20 °C")
    a1.plot([temp[0][0], temp[0][-1]], [0, 10000], "o", color=INK, ms=6, zorder=5, clip_on=False)
    a1.text(1150, 9900, f"ISA: {temp[0][0]:,.0f} ft at sea level,\n{temp[0][-1]:,.0f} ft at 10,000 ft", fontsize=10.5, ha="left",
            va="top", linespacing=1.3)
    a2.plot(wts[18000], hs, color=GREEN, lw=2.0, ls="-.", label="18,000 lb")
    a2.plot(wts[20000], hs, color=BLUE, lw=2.0, ls="--", label="20,000 lb")
    a2.plot(wts[21500], hs, color=INK, lw=2.2, label="21,500 lb")
    a2.text(1150, 9900, f"$S_G \\propto W^{{{w_exp:.1f}}}$ at sea level", fontsize=10.5, ha="left", va="top")
    a1.set_title("Temperature, 21,500 lb", fontweight="bold")
    a2.set_title("Weight, ISA", fontweight="bold")
    a1.set_ylabel("Pressure altitude (ft)")
    for ax in (a1, a2):
        ax.set_xlim(1000, 5500)
        ax.set_ylim(0, 10500)
        ax.set_xticks(range(1000, 5001, 1000))
        ax.set_yticks(range(0, 10001, 2000))
        ax.set_xlabel("Ground run $S_G$ (ft)")
        thousands(ax, "x")
        clean(ax)
        ax.legend(frameon=False, fontsize=10.5, loc="lower right")
    thousands(a1)
    fig.tight_layout()
    save(fig, "takeoff-altitude-weight")


# ------------------------------------------------------- page 3, maneuver and V-n
def turn_rate_chart():
    """Turn rate against Mach number at 15,000 ft: stall, n_max, V_MO, the sustained line, P_s."""
    W, h, nmax = 20000.0, 15000.0, 3.5
    _, _, rho, a = isa(h)
    rho, a = float(rho), float(a)
    mlim = mach_from_kcas(330.0, h)                         # V_MO 330 KIAS (M_MO 0.81 above 26,756 ft): published limits
    close(mlim, 0.65, 0.005, "330 KCAS at 15,000 ft")
    close(mach_from_kcas(330.0, 26756), 0.81, 0.005, "V_MO meets M_MO at 26,756 ft")
    M = np.linspace(0.12, mlim, 531)
    V = M * a
    q = 0.5 * rho * V ** 2
    om = lambda n, v: np.degrees(G * np.sqrt(np.clip(n ** 2 - 1, 0, None)) / v)
    n_env = np.minimum(q * CLMAX / (W / S), nmax)
    T = thrust(h, M, "max")
    n_sus = np.sqrt(np.clip(q / (K * W / S) * (T / W - q * CD0 / (W / S)), 0, None))
    fly = n_env >= 1
    ok = (n_sus <= n_env + 1e-9) & (n_sus >= 1)
    om_env, om_sus = om(n_env, V), om(n_sus, V)
    i_c = int(np.argmax(np.where(fly, om_env, 0)))
    vstar = np.sqrt(2 * nmax * W / (rho * S * CLMAX))
    close(M[i_c], vstar / a, 0.002, "the boundary peaks at the corner speed")
    close(M[i_c], 0.42, 0.005, "corner Mach number")
    close(om_env[i_c], 13.9, 0.05, "turn rate at the corner, deg/s")
    close(np.degrees(np.arccos(1 / nmax)), 73.4, 0.05, "bank angle at 3.5 g, Ex. 20-10")
    i_s = int(np.argmax(np.where(ok, om_sus, 0)))
    close(om_sus[i_s], 10.8, 0.05, "best sustained turn rate, deg/s")
    close(M[i_s], 0.44, 0.005, "Mach number of the best sustained turn rate")
    MM, NN = np.meshgrid(M, np.linspace(1.0, nmax, 300))
    VV = MM * a
    PS = VV * (thrust(h, MM, "max") - drag(VV, rho, W, NN)) / W
    lim = np.minimum(0.5 * rho * VV ** 2 * CLMAX / (W / S), nmax)
    PS = np.where(NN <= lim, PS, np.nan)
    OM = om(NN, VV)
    assert np.nanmax(PS) > 75 and np.nanmin(PS) < -25
    # P_s on the sustained line is zero, and negative above it at the corner
    close(float(V[i_s] * (T[i_s] - drag(V[i_s], rho, W, n_sus[i_s])) / W), 0.0, 1e-6, "P_s = 0 on the sustained line")
    assert V[i_c] * (T[i_c] - drag(V[i_c], rho, W, nmax)) / W < -25, "the corner loses energy"
    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    for lev in (-25, 25, 75):
        for seg in contour_segments(MM, OM, PS, lev):
            ax.plot(seg[:, 0], seg[:, 1], color=GRAY, lw=1.2, ls="--")
    m_s1 = np.sqrt(2 * W / (rho * S * CLMAX)) / a           # 1 g stall: the boundary starts on the axis
    assert M[fly][0] - m_s1 < M[1] - M[0]
    ax.plot(np.concatenate(([m_s1], M[fly])), np.concatenate(([0.0], om_env[fly])), color=INK, lw=2.6)
    ax.plot([mlim, mlim], [0, om_env[-1]], color=INK, lw=2.6)
    ax.plot(M[ok], om_sus[ok], color=BLUE, lw=2.6)
    ax.plot(M[i_c], om_env[i_c], "o", color=VERM, mec=INK, mew=0.8, ms=9, zorder=6)
    ax.plot(M[i_s], om_sus[i_s], "o", color=BLUE, mec=INK, mew=0.8, ms=7, zorder=6)
    ax.text(M[i_c] + 0.012, om_env[i_c] + 0.35, f"corner: Mach {M[i_c]:.2f}, {om_env[i_c]:.1f} deg/s", fontsize=10.5,
            ha="left", va="bottom")
    ax.text(0.565, 10.9, "$n_{max}$ = 3.5", fontsize=10.5, ha="left", va="bottom")
    ax.text(0.29, 9.0, "stall", fontsize=10.5, ha="right", va="center")
    ax.text(mlim + 0.008, 4.6, f"$V_{{MO}}$, Mach {mlim:.2f}", fontsize=10.5, ha="left", va="center", rotation=90)
    ax.text(M[i_s] + 0.005, om_sus[i_s] - 0.3, f"sustained, $P_s$ = 0\nbest: {om_sus[i_s]:.1f} deg/s at Mach {M[i_s]:.2f}",
            fontsize=10.5, ha="center", va="top", linespacing=1.25)
    box = dict(fc="white", ec="none", pad=1.2)
    ax.text(0.30, 6.35, "$P_s$ = 25 ft/s", fontsize=10, color=STEEL, ha="center", va="center", bbox=box)
    ax.text(0.55, 3.45, "75 ft/s", fontsize=10, color=STEEL, ha="center", va="center", bbox=box)
    ax.text(0.382, 12.75, "−25 ft/s", fontsize=10, color=STEEL, ha="right", va="center")
    ax.set_xlim(0.12, 0.72)
    ax.set_ylim(0, 16)
    ax.set_xlabel("Mach number")
    ax.set_ylabel("Turn rate $\\omega$ (deg/s)")
    clean(ax)
    fig.tight_layout()
    save(fig, "turn-rate-chart")


def flight_envelope():
    """The 1 g flight envelope: stall, V_MO and M_MO, and the contours of P_s."""
    W = 20000.0
    M = np.linspace(0.1, 0.85, 301)
    hs = np.linspace(0, 60000, 301)
    MM, HH = np.meshgrid(M, hs)
    _, _, rho, a = isa(HH)
    V = MM * a
    PS = V * (thrust(HH, MM, "max") - drag(V, rho, W)) / W
    PS = np.where(0.5 * rho * V ** 2 * CLMAX * S < W, np.nan, PS)
    mlim_h = np.array([min(mach_from_kcas(330.0, h), 0.81) for h in hs])     # V_MO 330 KIAS, M_MO 0.81: published limits
    PS = np.where(MM > mlim_h[:, None] + 1e-9, np.nan, PS)
    assert np.nanmax(PS[0]) > 150 and np.all(~(PS[-1] > 0)), "the 1 g envelope closes below 60,000 ft"

    def ps1(h, mach):
        _, _, rho_, a_ = isa(h)
        return float(mach * a_ * (thrust(h, mach, "max") - drag(mach * a_, rho_, W)) / W)

    def m_stall(h):
        _, _, rho_, a_ = isa(h)
        return float(np.sqrt(2 * W / (rho_ * S * CLMAX)) / a_)

    m_lim = lambda h: min(mach_from_kcas(330.0, h), 0.81)

    def ps_best(h):                                         # the highest P_s inside the envelope at one altitude
        ms = np.linspace(m_stall(h), m_lim(h), 400)
        return max(ps1(h, m) for m in ms)

    for edge in (m_stall, m_lim):                           # P_s changes sign once along each side
        sg = np.sign([ps1(h, edge(h)) for h in hs])
        assert sg[0] > 0 and sg[-1] < 0 and np.count_nonzero(np.diff(sg)) == 1
    h_j = bisect(lambda h: ps1(h, m_stall(h)), 0.0, 60000.0)                 # the stall line meets P_s = 0
    h_t = bisect(lambda h: ps1(h, m_lim(h)), 0.0, 60000.0)                   # P_s = 0 meets the speed limit
    h_k = bisect(lambda h: mach_from_kcas(330.0, h) - 0.81, 0.0, 60000.0)    # V_MO = M_MO
    assert h_k < h_t and m_lim(h_t) == 0.81, "the ceiling ends on the M_MO line"
    close(h_k, 26756, 30, "altitude where V_MO meets M_MO, ft")
    h_abs = bisect(ps_best, 40000.0, 60000.0)
    h_srv = bisect(lambda h: ps_best(h) - 100 / 60, 40000.0, 60000.0)
    close(h_abs, h_t, 1.0, "the absolute ceiling is reached at M_MO")
    close(h_abs, 49000, 500, "absolute ceiling, ft")
    close(h_srv, 48000, 500, "service ceiling (100 ft/min), ft")
    assert h_srv < h_abs
    m_j = m_stall(h_j)
    segs = contour_segments(MM, HH, PS, 0)
    assert len(segs) == 1, "one P_s = 0 line inside the envelope"
    top = segs[0] if segs[0][0, 0] > segs[0][-1, 0] else segs[0][::-1]      # from the speed limit to the stall line
    top = top[(top[:, 0] < 0.81 - 1e-9) & (top[:, 0] > m_j + 1e-9)]
    close(float(top[0, 1]), h_t, 100.0, "ceiling contour at the speed limit")
    close(float(top[-1, 1]), h_j, 400.0, "ceiling contour at the stall line")
    top = np.vstack([[0.81, h_t], top, [m_j, h_j]])
    assert np.all(np.diff(top[:, 0]) < 0), "ceiling single valued in Mach"
    h_dn = np.linspace(h_j, 0.0, 80)
    h_up = np.unique(np.concatenate([np.linspace(0.0, h_k, 60), [h_k, h_t]]))
    edge_m = np.concatenate([[m_stall(h) for h in h_dn], [m_lim(h) for h in h_up]])
    edge_h = np.concatenate([h_dn, h_up]) / 1000
    fig, ax = plt.subplots(figsize=(8.6, 5.4))
    for lev in (50, 100, 150):
        for seg in contour_segments(MM, HH, PS, lev):
            ax.plot(seg[:, 0], seg[:, 1] / 1000, color=BLUE, lw=1.2)
    ax.plot(top[:, 0], top[:, 1] / 1000, color=BLUE, lw=2.8)
    ax.plot(edge_m, edge_h, color=INK, lw=2.4, solid_capstyle="projecting")
    box = dict(fc="white", ec="none", pad=1.2)
    ax.text(0.235, 27, "stall, 1 g", fontsize=10.5, ha="right", va="center")
    ax.text(0.56, h_abs / 1000 + 1.4, f"$P_s$ = 0: absolute ceiling {round(h_abs, -3):,.0f} ft\n"
            f"service ceiling ($P_s$ = 100 ft/min) {round(h_srv, -3):,.0f} ft", fontsize=10.5, ha="center", va="bottom",
            linespacing=1.3)
    ax.text(0.55, 24.9, "$P_s$ = 50 ft/s", fontsize=10, ha="center", va="center", bbox=box)
    ax.text(0.55, 12.4, "100 ft/s", fontsize=10, ha="center", va="center", bbox=box)
    ax.text(0.425, 3.0, "150 ft/s", fontsize=10, ha="center", va="center", bbox=box)
    ax.text(0.715, 14, "$V_{MO}$\n330 KIAS", fontsize=10.5, ha="left", va="center")
    ax.text(0.817, 38, "$M_{MO}$\n0.81", fontsize=10.5, ha="left", va="center")
    ax.set_xlim(0.1, 0.9)
    ax.set_ylim(0, 58)
    ax.set_xlabel("Mach number")
    ax.set_ylabel("Pressure altitude (1,000 ft)")
    clean(ax)
    fig.tight_layout()
    save(fig, "flight-envelope")


def loop_forces():
    """A loop seen from the side: lift and weight at the bottom (pull-up) and at the top (inverted)."""
    R, W = 2.6, 0.75
    fc = 1.35                                               # the same centripetal force drawn at both points
    bottom, top = np.array([0.0, -R]), np.array([0.0, R])
    f_bot = {"L": np.array([0.0, fc + W]), "W": np.array([0.0, -W])}
    f_top = {"L": np.array([0.0, -(fc - W)]), "W": np.array([0.0, -W])}
    for point, f, rule in ((bottom, f_bot, "L - W"), (top, f_top, "L + W")):
        net = f["L"] + f["W"]
        to_center = -point / np.linalg.norm(point)
        close(float(net @ to_center), fc, 1e-9, f"{rule} is the centripetal force")
        assert f["L"] @ to_center > 0, "lift points to the center of the loop"
    assert f_bot["W"] @ (-bottom) < 0 < f_top["W"] @ (-top), "weight opposes the lift at the bottom and adds to it at the top"
    close(np.linalg.norm(f_bot["L"]) - W, np.linalg.norm(f_top["L"]) + W, 1e-9, "L - W at the bottom equals L + W at the top")
    fig, ax = sketch((8.6, 6.2))
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(R * np.cos(th), R * np.sin(th), color=STEEL, lw=1.1, ls="--", zorder=1)
    ax.plot(0, 0, "o", color=STEEL, ms=5)
    a_r = math.radians(200)
    ax.plot([0, R * math.cos(a_r)], [0, R * math.sin(a_r)], color=STEEL, lw=1.0)
    ax.text(0.5 * R * math.cos(a_r), 0.5 * R * math.sin(a_r) + 0.22, "$r$", fontsize=13, ha="center", va="center")
    for ang in (-35.0, 145.0):                              # direction of flight along the loop, counterclockwise
        p = R * np.array([math.cos(math.radians(ang)), math.sin(math.radians(ang))])
        d = np.array([-math.sin(math.radians(ang)), math.cos(math.radians(ang))])
        ax.annotate("", xy=tuple(p + 0.22 * d), xytext=tuple(p - 0.22 * d),
                    arrowprops=dict(arrowstyle="-|>", color=STEEL, lw=1.2, mutation_scale=16))
    _trainer_side(ax, *bottom, 0.2)                         # upright, flying to the right
    _trainer_side(ax, *top, 0.2, pitch=180.0)               # inverted, flying to the left, canopy toward the center
    _force(ax, f_bot["L"], "$L$", BLUE, (-0.25, -0.12), origin=tuple(bottom))
    _force(ax, f_bot["W"], "$W$", GREEN, (-0.28, 0.12), origin=tuple(bottom))
    _force(ax, f_top["L"], "$L$", BLUE, (-0.25, 0.12), origin=(top[0] - 0.22, top[1]))
    _force(ax, f_top["W"], "$W$", GREEN, (0.3, 0.12), origin=(top[0] + 0.22, top[1]))
    for p in (bottom, top):
        ax.plot(*p, "o", color=INK, ms=5, zorder=8)
    ax.text(1.5, R + 0.05, r"inverted at the top:  $L + W = \dfrac{W}{g}\,\dfrac{V^2}{r}$", fontsize=11.5, ha="left", va="center")
    ax.text(1.5, -R - 0.05, r"pull-up at the bottom:  $L - W = \dfrac{W}{g}\,\dfrac{V^2}{r}$", fontsize=11.5, ha="left", va="center")
    ax.set_xlim(-3.3, 6.5)
    ax.set_ylim(-R - 1.0, R + 0.8)
    save(fig, "loop-forces")


# Air-to-Air Fighter (AAF) of Mattingly, Heiser and Pratt (2002), Chapter 2: T_SL/W_TO 1.25 and
# W_TO/S 64 lbf/ft2 (Sec. 2.4.2); C_D = K1 C_L^2 + C_D0, C_Lmax 2.0 (Fig. 2.E1a); C_D0 0.016 and
# K1 0.18 at Mach 0.9 and 30,000 ft (combat turn 2), held constant; low-bypass mixed-flow turbofan
# at maximum power, TR 1.07, Eq. (2.54a); combat at beta = 0.78, 30,000 ft. Limit load factor 7.33:
# the USAF fighter value of Nicolai and Carichner (2010), Example 5.1, assumed (Mattingly gives none).
AAF = dict(TW=1.25, WS=64.0, CD0=0.016, K1=0.18, CLmax=2.0, TR=1.07, beta=0.78, h=30000.0, nmax=7.33)


def aaf_alpha(h, mach):
    """Thrust lapse at maximum power (afterburning), Mattingly Eq. (2.54a)."""
    t, p, _, _ = isa(h)
    th0 = t / T0R * (1 + 0.2 * mach ** 2)
    de0 = p / P0 * (1 + 0.2 * mach ** 2) ** 3.5
    return de0 * np.where(th0 <= AAF["TR"], 1.0, 1 - 3.5 * (th0 - AAF["TR"]) / th0)


def maneuver_vn():
    """Load factor against Mach number at 30,000 ft for the AAF: stall, n_max, the Mach 0.9 edge,
    and the lines of constant P_s through five load factors at Mach 0.9."""
    f = AAF
    h, beta, nmax, mmax, m0 = f["h"], f["beta"], f["nmax"], 0.9, 0.9
    a = float(isa(h)[3])
    p_h = float(isa(h)[1])
    ws = beta * f["WS"]                                     # wing loading in combat
    qf = lambda M: 0.7 * p_h * M ** 2

    def ps(n, M):                                           # Mattingly Eq. (2.E4)
        q = qf(M)
        return M * a * (aaf_alpha(h, M) / beta * f["TW"] - f["K1"] * n ** 2 * ws / q - f["CD0"] * q / ws)

    # published checks: Mattingly's combat turn 2 (Mach 0.9, 30,000 ft, 5 g)
    close(float(aaf_alpha(h, 0.9)), 0.5033, 0.002, "alpha_wet at Mach 0.9, 30,000 ft")
    close(float(aaf_alpha(h, 1.6)), 0.7829, 0.003, "alpha_wet at Mach 1.6, 30,000 ft")
    close(qf(0.9), 357.0, 1.0, "q at Mach 0.9, 30,000 ft")
    tw5 = lambda w: beta / aaf_alpha(h, 0.9) * (f["K1"] * 25 * beta * w / qf(0.9) + f["CD0"] * qf(0.9) / (beta * w))
    close(float(tw5(60.0)), 1.10, 0.01, "5 g turn T/W at W/S 60")
    close(float(tw5(80.0)), 1.36, 0.01, "5 g turn T/W at W/S 80")
    n_stall = lambda Mx: qf(Mx) * f["CLmax"] / ws
    ms1 = float(np.sqrt(ws / f["CLmax"] / (0.7 * p_h)))             # 1 g stall
    mstar = float(np.sqrt(nmax * ws / f["CLmax"] / (0.7 * p_h)))    # corner
    M = np.linspace(ms1, mmax, 801)
    n_top = np.minimum(n_stall(M), nmax)                    # stall line, then n_max
    i_c = int(np.argmax(n_top >= nmax - 1e-12))             # first point on the n_max line
    close(M[i_c], mstar, 0.001, "the stall line reaches n_max at the corner")
    close(mstar, 0.64, 0.005, "corner Mach number")
    close(n_top[0], 1.0, 1e-9, "the boundary starts at the 1 g stall")
    q0, v0 = qf(m0), m0 * a
    n_sus = float(np.sqrt((aaf_alpha(h, m0) / beta * f["TW"] - f["CD0"] * q0 / ws) * q0 / (f["K1"] * ws)))
    close(float(ps(n_sus, m0)), 0.0, 1e-6, "P_s = 0 at the sustained load factor")
    assert q0 * f["CLmax"] / ws > nmax, "n_max reachable at Mach 0.9"
    rows = [1.0, 2.0, 4.0, n_sus, nmax]
    book = [(1.00, 596, 0.0), (2.00, 528, 60.0), (4.00, 257, 75.5), (5.23, 0, 79.0), (7.33, -595, 82.2)]

    def n2_at(lev, Mx):                                     # load factor squared at a given P_s
        q = qf(Mx)
        return (aaf_alpha(h, Mx) / beta * f["TW"] - f["CD0"] * q / ws - lev / (Mx * a)) * q / (f["K1"] * ws)

    def contour(lev):
        """The line of one P_s inside the boundary, ending at Mach 0.9."""
        n2 = n2_at(lev, M)
        nc = np.sqrt(np.clip(n2, 0.0, None))
        ok = (n2 >= 0) & (nc <= n_top * (1 + 1e-9))
        assert ok[-1], f"P_s {lev:.0f} line reaches Mach {mmax}"
        i0 = len(M) - 1
        while i0 > 0 and ok[i0 - 1]:
            i0 -= 1
        assert not ok[:i0].any(), f"P_s {lev:.0f} line in one piece"
        Mc, ncc = M[i0:], nc[i0:]
        if i0 > 0:                                          # exact left end: on the axis or on the stall line
            if n2[i0 - 1] < 0:
                mx = bisect(lambda Mx: n2_at(lev, Mx), M[i0 - 1], M[i0])
                Mc, ncc = np.concatenate(([mx], Mc)), np.concatenate(([0.0], ncc))
            else:
                assert M[i0 - 1] <= mstar, f"P_s {lev:.0f} line leaves through the stall line"
                mx = bisect(lambda Mx: n2_at(lev, Mx) - n_stall(Mx) ** 2, M[i0 - 1], M[i0])
                Mc, ncc = np.concatenate(([mx], Mc)), np.concatenate(([n_stall(mx)], ncc))
        return Mc, ncc

    lines, table = [], []
    for n, (n_b, ps_b, bank_b) in zip(rows, book):
        lev = float(ps(n, m0))
        Mc, ncc = contour(lev)
        close(float(ncc[-1]), n, 1e-6, "the P_s line ends on its load factor at Mach 0.9")
        k = len(Mc) // 2
        close(float(ps(ncc[k], Mc[k])), lev, 1e-6, "P_s constant along the line")
        bank = float(np.degrees(np.arccos(1 / n)))
        close(n, n_b, 0.005, "load factor")
        close(lev, ps_b, 0.5, "P_s at Mach 0.9, ft/s")
        close(bank, bank_b, 0.05, "bank angle of the level turn, deg")
        lines.append((Mc, ncc))
        table.append((n, lev, bank))
    nv = np.sqrt(np.clip(n2_at(0.0, M), 0, None))
    assert nv.max() < nmax, "the sustained load factor stays below n_max to Mach 0.9"
    fig, ax = plt.subplots(figsize=(9.0, 5.4))
    ax.plot([ms1, mmax], [1, 1], color=GRAY, lw=0.9, ls=":")
    for k, (Mc, ncc) in enumerate(lines):
        if k == 3:
            ax.plot(Mc, ncc, color=BLUE, lw=2.6, zorder=3)
        else:
            ax.plot(Mc, ncc, color=GRAY, lw=1.2, ls="--", zorder=2)
    ax.plot([mmax, mmax], [0, nmax], color=GRAY, lw=1.6, ls=":", zorder=3)
    m_st = np.linspace(ms1, mstar, 200)
    ax.plot(np.concatenate(([ms1], m_st, [mmax])), np.concatenate(([0.0], n_stall(m_st), [nmax])), color=INK, lw=2.6, zorder=4)
    ax.plot(mstar, nmax, "o", color=VERM, mec=INK, mew=0.8, ms=9, zorder=6)
    ax.plot([m0] * 5, rows, "D", color="white", mec=INK, mew=1.3, ms=7, zorder=6, clip_on=False)
    ax.text(mstar - 0.015, nmax + 0.12, f"corner, Mach {mstar:.2f}", fontsize=10.5, ha="right", va="bottom")
    ax.text(0.78, nmax + 0.12, "$n_{max}$ = 7.33", fontsize=10.5, ha="center", va="bottom")
    ax.text(0.405, 3.7, "stall, $C_{L_{max}}$ = 2.0", fontsize=10.5, ha="right", va="center")
    ax.text(0.60, float(np.sqrt(n2_at(0.0, 0.62))) + 0.25, "$P_s$ = 0", fontsize=10.5, ha="right", va="bottom")
    ax.text(0.965, 8.05, "bank", fontsize=10.5, ha="left", va="center", clip_on=False)
    ax.text(1.115, 8.05, "$P_s$ (ft/s)", fontsize=10.5, ha="right", va="center", clip_on=False)
    for n, lev, bank in table:
        whole = abs(bank - round(bank)) < 1e-6
        ax.text(0.965, n, f"{bank:.0f}°" if whole else f"{bank:.1f}°", fontsize=10.5, ha="left", va="center", clip_on=False)
        ax.text(1.115, n, f"{lev:.0f}".replace("-", "−") if abs(lev) > 0.5 else "0", fontsize=10.5, ha="right", va="center",
                clip_on=False)
    ax.set_xlim(0.15, 0.95)
    ax.set_ylim(0, 8.4)
    ax.set_xticks([0.2, 0.4, 0.6, 0.8, 0.9])
    ax.set_xlabel("Mach number at 30,000 ft")
    ax.set_ylabel("Load factor $n$")
    clean(ax)
    fig.tight_layout()
    fig.subplots_adjust(right=0.80)
    save(fig, "maneuver-vn")


ALL = [sizing_check_flow, eom_cruise, eom_climb, eom_descent, eom_maneuver, drag_power, level_speeds, range_endurance,
       climb_learjet, takeoff_speeds, ground_run, balanced_field, takeoff_altitude_weight, turn_rate_chart, flight_envelope,
       loop_forces, maneuver_vn]

if __name__ == "__main__":
    for fn in ALL:
        fn()
