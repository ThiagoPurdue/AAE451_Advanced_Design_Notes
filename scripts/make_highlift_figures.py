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


import make_aero_figures as _aero          # the airfoil equations and the lift-curve shape of Lecture 5

lift_curve = _aero.lift_curve


# ------------------------------------------------------------ airfoil pieces
# Every device is cut from one contour, the NACA 23012 of the NACA slotted-flap reports, computed
# from the 5-digit equations. Chord fractions, deflections and gaps are in the ranges of
# Gudmundsson (2022), Chapter 10, and each sketch asserts its own.
_S = _aero.naca230(0.12, n=400)
XU, YU, XL, YL = _S[2], _S[3], _S[4], _S[5]
_I0 = int(np.argmin(XU))                     # the upper surface doubles back by 0.001 c at the nose
up = lambda x: np.interp(x, XU[_I0:], YU[_I0:])
lo = lambda x: np.interp(x, XL, YL)


def surf(x0, x1, upper=True, n=80):
    """Points of the upper or lower surface from station x0 to x1 (either order)."""
    x = np.linspace(x0, x1, n)
    return np.column_stack([x, up(x) if upper else lo(x)])


def nose_contour(xl, xu_):
    """The contour around the leading edge, from the lower surface at xl to the upper surface at xu_."""
    low = np.column_stack([XL, YL])[XL <= xl][::-1]
    upp = np.column_stack([XU, YU])[_I0:][XU[_I0:] <= xu_]
    return np.vstack([[xl, lo(xl)], low, np.column_stack([XU, YU])[:_I0][::-1][-1:], upp, [xu_, up(xu_)]])


def move(pts, pivot, deg, shift=(0.0, 0.0)):
    """Rotate about the pivot (counterclockwise positive), then translate."""
    th = np.radians(deg)
    R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    return (np.asarray(pts) - pivot) @ R.T + pivot + np.asarray(shift)


def gap_between(a, b):
    """Smallest distance between two outlines (dense point sets), in chords."""
    a, b = _dense(a), _dense(b)
    return float(np.sqrt(((a[:, None, :] - b[None, :, :]) ** 2).sum(-1)).min())


def _dense(p, n=6):
    p = np.asarray(p)
    t = np.linspace(0, 1, n, endpoint=False)[:, None]
    return np.vstack([p[i] + t * (p[i + 1] - p[i]) for i in range(len(p) - 1)] + [p[-1:]])


def slotted_flap(x0, x_lip, lip=0.006, clear=0.008, nose_dx=0.04):
    """A slotted flap of chord 1 - x0 with a rounded nose, stowed under a shroud that ends at
    x_lip, and the main body with the cove the flap nose fits in. Returns (main, flap)."""
    xs = np.linspace(x0, x_lip, 50)
    y_le = lo(x0) + 0.40 * (up(x0) - lo(x0))
    m = (up(x_lip + 0.005) - up(x_lip - 0.005)) / 0.01
    u = (x_lip - xs) / (x_lip - x0)
    top = y_le + (up(x_lip) - y_le) * np.sqrt(1 - u ** 2) + m * (xs - x_lip) * (1 - u)
    xb = np.linspace(x0, x0 + nose_dx, 25)
    v = (xb - x0) / nose_dx
    bot = y_le - (y_le - lo(x0 + nose_dx)) * np.sqrt(1 - (1 - v) ** 2)
    flap = np.vstack([np.column_stack([xs, top]), surf(x_lip, 1.0), surf(1.0, x0 + nose_dx, upper=False), np.column_stack([xb, bot])[::-1]])
    cove = np.column_stack([xs - clear, top - 0.5 * clear])[::-1]
    cove[:, 1] = np.minimum(cove[:, 1], up(x_lip) - lip)
    main = np.vstack([nose_contour(x0 - clear, x_lip), [x_lip, up(x_lip) - lip], cove, [x0 - clear, lo(x0 - clear)]])
    return main, flap


def hinge_of(stowed, deployed):
    """The fixed point of the rigid motion that takes the stowed flap to the deployed one: the
    hinge a simple flap bracket would need. Returns (point, rotation in degrees)."""
    a0, a1, b0, b1 = stowed[0], stowed[len(stowed) // 2], deployed[0], deployed[len(deployed) // 2]
    th = np.arctan2(*(b1 - b0)[::-1]) - np.arctan2(*(a1 - a0)[::-1])
    R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    return np.linalg.solve(np.eye(2) - R, b0 - R @ a0), float(np.degrees(th))


def nose_split(x_up, x_low, bulge=0.05):
    """Cut the nose off along a curve from the upper surface at x_up to the lower surface at
    x_low that bulges forward: the fixed leading edge of the main body behind a slat. Returns
    (main, slat), stowed, the slat's concave back resting on the main body's nose."""
    U, Lw = np.array([x_up, up(x_up)]), np.array([x_low, lo(x_low)])
    tu = np.array([0.01, up(x_up + 0.005) - up(x_up - 0.005)])
    tl = np.array([0.01, lo(x_low + 0.005) - lo(x_low - 0.005)])
    P1, P2 = U - bulge * 1.6 * tu / np.linalg.norm(tu), Lw - bulge * tl / np.linalg.norm(tl)
    t = np.linspace(0, 1, 60)[:, None]
    cut = (1 - t) ** 3 * U + 3 * (1 - t) ** 2 * t * P1 + 3 * (1 - t) * t ** 2 * P2 + t ** 3 * Lw      # upper to lower
    slat = np.vstack([nose_contour(x_low, x_up), cut[1:-1]])
    main = np.vstack([cut[::-1], surf(x_up, 1.0), surf(1.0, x_low, upper=False)])
    return main, slat


def swing(pts, pivot):
    """Length and direction (degrees, counterclockwise from +x) of a hinged part as drawn: the
    vector from the pivot to its farthest point."""
    v = np.asarray(pts) - pivot
    far = v[np.argmax((v ** 2).sum(1))]
    return float(np.hypot(*far)), float(np.degrees(np.arctan2(far[1], far[0])))


def draw_device(ax, kind):
    ax.set_aspect("equal")
    ax.axis("off")
    main_face = dict(fc=LIGHT, ec=INK, lw=1.2, joinstyle="round")
    flap_face = dict(fc=DUST, ec=INK, lw=1.2, joinstyle="round")
    add = lambda pts, face: ax.add_patch(Polygon(pts, closed=True, **face))
    pin = lambda p: ax.plot(*p, "o", color=INK, ms=3.5, zorder=7)
    if kind == "plain":
        # 20% chord, hinged on the mean line; the flap nose is an arc about the hinge, sealed in the cove
        xh, d = 0.80, 45.0
        h = np.array([xh, 0.5 * (up(xh) + lo(xh))])
        r = 0.5 * (up(xh) - lo(xh))
        th = np.radians(np.linspace(90, 270, 30))
        arc = h + r * np.column_stack([np.cos(th), np.sin(th)])
        flap = np.vstack([arc[::-1], surf(xh, 1.0, upper=False), surf(1.0, xh)])
        add(np.vstack([nose_contour(xh - 0.2 * r, xh - 0.2 * r), (arc + [0.004, 0])[::-1][3:-3]]), main_face)
        out = move(flap, h, -d)
        add(out, flap_face)
        pin(h)
        (c0, a0), (c1, a1) = swing(flap, h), swing(out, h)                   # the flap stowed and as drawn
        assert abs(c1 - 0.20) < 0.005 and abs((a0 - a1) - 45.0) < 0.5        # 20% chord, 45 deg down
    elif kind == "split":
        # 20% chord plate on the lower surface; the upper surface does not move
        xh, d = 0.80, 60.0
        add(np.vstack([nose_contour(1.0, 1.0)]), main_face)
        h = np.array([xh, lo(xh)])
        plate = np.vstack([surf(xh, 1.0, upper=False, n=12), surf(1.0, xh, upper=False, n=12) - [0, 0.010]])
        out = move(plate, h, -d)
        add(out, flap_face)
        pin(h)
        (c0, a0), (c1, a1) = swing(plate, h), swing(out, h)
        assert abs(c1 - 0.20) < 0.005 and abs((a0 - a1) - 60.0) < 0.5        # 20% chord plate, 60 deg down
    elif kind in ("single", "fowler"):
        # 30% chord flap; the single-slotted flap swings on a bracket below the wing, the Fowler
        # flap runs aft on tracks until its nose is under the end of the shroud
        x0, d = 0.70, 40.0
        x_lip, nose_at = (0.84, (-0.012, -0.030)) if kind == "single" else (0.92, (-0.012, -0.030))
        main, flap = slotted_flap(x0, x_lip)
        le = flap[0]
        out = move(flap, le, -d, np.array([x_lip, up(x_lip)]) + nose_at - le)
        add(main, main_face)
        add(out, flap_face)
        g = gap_between(main, out)
        hinge, turned = hinge_of(flap, out)
        assert abs(turned + d) < 0.5 and 0.015 < g < 0.035, (kind, g)       # slot gap of 1.5% to 3.5% chord
        if kind == "single":
            assert 0.6 < hinge[0] < 0.9 and lo(hinge[0]) - 0.20 < hinge[1] < lo(hinge[0]) - 0.03, hinge   # a bracket below the wing
            ax.plot([0.66, hinge[0]], [lo(0.66), hinge[1]], color=INK, lw=1.0)
            ax.plot([hinge[0], out[len(out) // 2 + 30][0]], [hinge[1], out[len(out) // 2 + 30][1]], color=INK, lw=1.0)
            pin(hinge)
            assert 1.05 < out[:, 0].max() < 1.10                             # the chord grows by 5 to 10%
        else:
            assert out[:, 0].max() > 1.12                                    # the chord grows by more than 12%
    elif kind == "double":
        # fixed vane and flap that move together: the vane at about 30 deg, the flap at 55 deg
        x0, x_lip, dv, df = 0.70, 0.82, 30.0, 55.0
        main, flap = slotted_flap(x0, x_lip)
        # the vane is a separate small cambered section of 9% chord, not cut from the 23012; with the
        # flap of 21% chord behind it, the two stow in the 30% of the chord aft of the cut
        cv, cf = 0.09, 0.21
        s = _aero.naca4(0.08, 0.4, 0.18, n=60)
        vane = cv * np.column_stack([np.r_[s[2], s[4][::-1]], np.r_[s[3], s[5][::-1]]])
        vane = move(vane, (0, 0), -dv, np.array([x_lip, up(x_lip)]) + (-0.035, -0.034))
        aft = flap * [cf / 0.30, cf / 0.30] + [1 - cf, 0.0]
        assert abs(np.ptp(aft[:, 0]) - cf) < 1e-6 and np.ptp(aft[:, 0]) + cv <= (1 - x0) + 1e-9   # they fit the wing
        le = aft[0]
        vte = vane[np.argmax(vane[:, 0])]
        aft = move(aft, le, -df, vte + (-0.012, -0.024) - le)
        add(main, main_face)
        add(vane, flap_face)
        add(aft, flap_face)
        g1, g2 = gap_between(main, vane), gap_between(vane, aft)
        assert 0.012 < g1 < 0.035 and 0.010 < g2 < 0.035, (g1, g2)
    elif kind == "droop":
        # 15% chord nose hinged near the lower surface, drooped 25 deg; the upper skin slides on a knuckle
        xh, d = 0.15, 25.0
        h = np.array([xh, lo(xh) + 0.25 * (up(xh) - lo(xh))])
        r = up(xh) - h[1]
        th = np.radians(np.linspace(90, 90 + d, 12))
        knuckle = h + r * np.column_stack([np.cos(th), np.sin(th)])
        add(np.vstack([knuckle[::-1], surf(xh, 1.0), surf(1.0, xh, upper=False), [h]]), main_face)
        nose = np.vstack([nose_contour(xh, xh), [h]])
        out = move(nose, h, d)
        add(out, flap_face)
        pin(h)
        (c0, a0), (c1, a1) = swing(nose, h), swing(out, h)
        assert abs((a1 - a0) % 360 - 25.0) < 0.5 and abs(xh - nose[:, 0].min() - 0.15) < 0.002   # 15% chord nose, drooped 25 deg
    elif kind in ("slot", "slat"):
        # slot: a 15% chord nose piece fixed 2% chord ahead of the main body
        # slat: a 16% chord nose piece moved forward and down and turned 25 deg nose down
        x_up, x_low, bulge, d, shift = (0.15, 0.06, 0.025, 0.0, (-0.045, 0.0)) if kind == "slot" else (0.16, 0.08, 0.03, 25.0, (-0.075, -0.02))
        main, slat = nose_split(x_up, x_low, bulge)
        out = move(slat, np.array([x_up, up(x_up)]), d, shift)
        add(main, main_face)
        add(out, flap_face)
        g = gap_between(main, out)
        assert (0.015 < g < 0.025) if kind == "slot" else (0.012 < g < 0.035 and d <= 30), (kind, g)
        assert abs(np.ptp(slat[:, 0]) - x_up) < 0.003                         # nose piece of 15% (slot) or 16% (slat) chord
    elif kind == "kruger":
        # a panel of 10% chord from the lower surface, swung 125 deg forward about a hinge at the
        # nose, with a bullnose of radius 0.167 of its chord; no gap to the leading edge
        cs, d, xh = 0.10, 125.0, 0.012
        h = np.array([xh, lo(xh)])
        add(nose_contour(1.0, 1.0), main_face)
        rb = 0.167 * cs
        th = np.radians(np.linspace(-90, 90, 20))
        bull = np.array([cs - rb, 0.0]) + rb * np.column_stack([np.cos(th), np.sin(th)])
        panel = np.vstack([[0, -0.006], [cs - rb, -0.006], bull * [1, 0.6] + [0, -0.006 * 0], [cs - rb, 0.006], [0, 0.006]])
        out = move(panel + h, h, -d)
        add(out, flap_face)
        pin(h)
        c1, a1 = swing(out, h)                                               # the panel as drawn
        assert 0.07 <= c1 <= 0.105 and 110 <= -a1 <= 140, (c1, a1)           # chord and swing from the stowed position
    # show the half of the airfoil that carries the device, with a break line where the rest is cut off
    lead = kind in ("droop", "slot", "slat", "kruger")
    xa, xb = (-0.16, 0.50) if lead else (0.46, 1.24)
    xc = xb - 0.03 if lead else xa + 0.03
    zz = np.linspace(lo(xc), up(xc), 7)
    ax.plot(xc + 0.012 * np.array([0, 1, -1, 1, -1, 1, 0]), zz, color=STEEL, lw=0.9, zorder=6)
    ax.add_patch(Polygon([(xc, -0.5), (xc, 0.5), (xc + (0.2 if lead else -0.2), 0.5), (xc + (0.2 if lead else -0.2), -0.5)],
                         closed=True, fc="white", ec="none", zorder=5.5))
    ax.set_xlim(xa, xb)
    ax.set_ylim(*((-0.20, 0.13) if lead else (-0.31, 0.12)))


def trailing_edge_devices():
    fig, axes = plt.subplots(1, 5, figsize=(12, 2.3))
    names = [("plain", "Plain", "+0.66 at 45°"), ("split", "Split", "+0.89 at 60°"),
             ("single", "Single-slotted", "+1.32 at 40°"), ("double", "Double-slotted", "+1.40 at 55° to 60°"),
             ("fowler", "Fowler", "+2.24 at 40°")]
    for ax, (k, n, inc) in zip(axes, names):
        draw_device(ax, k)
        ax.set_title(n, fontsize=12)
        ax.text(0.5, -0.02, inc, ha="center", va="top", fontsize=11, color=STEEL, transform=ax.transAxes)
    fig.tight_layout()
    save(fig, "trailing-edge-devices")


def leading_edge_devices():
    fig, axes = plt.subplots(1, 4, figsize=(11, 2.3))
    names = [("droop", "Droop nose", "+0.58, stall +7.8°"), ("slot", "Fixed slot", "+0.45, stall +9.0°"),
             ("kruger", "Krüger flap", "+0.30, stall +5.0°"), ("slat", "Slat", "+0.84, stall +11.0°")]
    for ax, (k, n, inc) in zip(axes, names):
        draw_device(ax, k)
        ax.set_title(n, fontsize=12)
        ax.text(0.5, -0.02, inc, ha="center", va="top", fontsize=11, color=STEEL, transform=ax.transAxes)
    fig.tight_layout()
    save(fig, "leading-edge-devices")


# ------------------------------------------------------------ lift curves
def flap_lift_curve():
    fig, ax = plt.subplots(figsize=(8, 4.6))
    a = np.linspace(-16, 28, 600)
    # schematic: a flap moves the zero-lift angle and raises the peak; a slat extends the clean curve
    curves = [("clean", -2, 15, 1.5, "-", INK), ("trailing-edge flap", -12, 12, 2.3, "--", VERM),
              ("slat", -2, 24, 2.1, ":", BLUE), ("flap and slat", -12, 21, 2.9, "-.", GREEN)]
    drawn = []
    for lab, a0, ast, clmax, ls, c in curves:
        show = a <= ast + 5
        cl = lift_curve(a, a0, ast, clmax, drop=0.4, width=4.0)
        drawn.append((a[np.argmax(cl)], cl.max()))                           # stall angle and peak as drawn
        ax.plot(a[show], cl[show], ls=ls, color=c, lw=2.2, label=lab)
    (s0, c0), (s1, c1), (s2, c2), (s3, c3) = drawn
    assert c1 > c0 and s1 < s0 and c2 > c0 and s2 > s0 and c3 > max(c1, c2) and s1 < s3 < s2
    ax.axhline(0, color=STEEL, lw=0.7)
    ax.axvline(0, color=STEEL, lw=0.7)
    # labels in the open corners: the curves run through the lower half of the plot
    ax.text(-15.5, 3.15, "a flap shifts the curve up and left:\nhigher $C_{l_{max}}$, lower $\\alpha_{stall}$", fontsize=10.5, color=VERM, va="bottom")
    ax.text(13.0, 3.15, "a slat extends the curve:\nhigher $C_{l_{max}}$ and $\\alpha_{stall}$", fontsize=10.5, color=BLUE, va="bottom")
    ax.set_xlabel(r"Angle of attack $\alpha$ (deg)")
    ax.set_ylabel("Section lift coefficient $C_l$")
    ax.set_xlim(-16, 28)
    ax.set_ylim(-1.0, 3.8)
    ax.legend(frameon=False, fontsize=10, loc="lower right")
    clean(ax)
    fig.tight_layout()
    save(fig, "flap-lift-curve")


def slot_lift_curve():
    """The Clark Y with and without a fixed slot, Re = 0.63e6 (NACA Report 407), read from the
    plotted curves of Gudmundsson (2022), Figure 10-9."""
    import json
    data = json.loads((_aero.AIRFOILS / "gudmundsson-fig-10-9.json").read_text())
    plain, slot = np.array(data["plain"]), np.array(data["slot"])
    ip, js = int(np.argmax(plain[:, 1])), int(np.argmax(slot[:, 1]))
    # the values printed on the source figure, and the increments of its Table 10-2
    assert abs(plain[ip, 1] - 1.297) < 0.02 and abs(slot[js, 1] - 1.751) < 0.02
    assert abs((slot[js, 1] - plain[ip, 1]) - 0.45) < 0.02 and abs((slot[js, 0] - plain[ip, 0]) - 9.0) < 1.0
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(plain[:, 0], plain[:, 1], color=INK, lw=2.2, label="Clark Y")
    ax.plot(slot[:, 0], slot[:, 1], color=BLUE, lw=2.2, ls="--", label="Clark Y with a fixed slot")
    ax.axhline(0, color=STEEL, lw=0.7)
    ax.annotate("", xy=(slot[js, 0], 0.55), xytext=(plain[ip, 0], 0.55), arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.1))
    for x, y in ((plain[ip, 0], plain[ip, 1]), (slot[js, 0], slot[js, 1])):
        ax.plot([x, x], [0.5, y], color=STEEL, lw=0.8, ls=":")
    ax.text(0.5 * (plain[ip, 0] + slot[js, 0]), 0.5, "the slot delays the\nstall by 9 degrees", fontsize=10.5, color=BLUE, va="top", ha="center")
    ax.text(27.5, -0.3, "$Re$ = 0.63 × 10$^6$, NACA Report 407", fontsize=10, color=STEEL, ha="right")
    ax.set_xlabel(r"Angle of attack $\alpha$ (deg)")
    ax.set_ylabel("$C_l$")
    ax.set_xlim(-6, 28)
    ax.set_ylim(-0.5, 2.2)
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
