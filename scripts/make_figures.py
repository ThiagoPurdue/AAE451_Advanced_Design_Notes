"""Figures for the AAE 451 Advanced Aircraft Design lecture notes book.

Run from the book folder:  python3 scripts/make_figures.py
Writes SVG files to the figures folder of each chapter (notes/<chapter>/figures/).
Text stays as text in the SVG (svg.fonttype = none) so it scales and can be
selected. Set FIG_PREVIEW=<folder> to also write PNG copies for checking.

Each figure is a vector redraw of the figure on the lecture slide or in the
RFP, named in its caption, kept as close to the source as the redraw allows.
Colors follow the sources, except where a source color would not meet the
contrast needed on a white page. The GoAERO concept of operations is not
drawn here: it is a draw.io file next to the figures, exported to SVG.
"""
import os
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon,
                                Rectangle, RegularPolygon)

NOTES = Path(__file__).resolve().parents[1] / "notes"
# Each figure goes to the figures folder of the chapter that uses it.
FOLDER = {
    "navy-training-mission": "navy-rfp",
    "navy-ferry-mission": "navy-rfp",
}
DEFAULT_FOLDER = "lecture-01"
PREVIEW = os.environ.get("FIG_PREVIEW")  # optional PNG copies for checking

plt.rcParams.update({
    "svg.fonttype": "none",
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 12,
    "axes.edgecolor": "#000000",
    "axes.labelcolor": "#000000",
    "xtick.color": "#000000",
    "ytick.color": "#000000",
    "savefig.facecolor": "white",
})

INK = "#000000"
# Purdue palette, used only for the figure that has no source drawing.
GOLD, DUST, LIGHT, AGED = "#CFB991", "#EBD99F", "#F5EFDC", "#8E6F3E"


def save(fig, name):
    out = NOTES / FOLDER.get(name, DEFAULT_FOLDER) / "figures"
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{name}.svg", bbox_inches="tight", pad_inches=0.1)
    if PREVIEW:
        fig.savefig(Path(PREVIEW) / f"{name}.png", dpi=110, bbox_inches="tight",
                    pad_inches=0.1)
    plt.close(fig)
    print("wrote", name)


def pixel_canvas(w, h):
    """Axes whose data units are pixels of the source image, y downwards."""
    fig = plt.figure(figsize=(w / 100, h / 100))
    ax = fig.add_axes([0, 0, 1, 1])   # fills the figure, so insets can use the same units
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.axis("off")
    return fig, ax


# ---------------------------------------------------------------------------
def design_phases():
    """Phases 0 to 5 of an aircraft program, after Venson (lecture slide 2)."""
    fig, ax = plt.subplots(figsize=(11, 2.4))
    ax.set_xlim(0, 113)
    ax.set_ylim(0, 24)
    ax.axis("off")
    names = ["feasibility\nstudy", "conceptual\ndesign", "preliminary\ndesign",
             "detailed\ndesign", "entry into\nservice &\nproduction",
             "operating\n& phase out"]
    w, tip, y0, y1 = 17.0, 4.0, 0.5, 23.5
    for i, name in enumerate(names):
        x = 1 + i * (w + 0.9)
        pts = [(x, y0), (x + w, y0), (x + w + tip, (y0 + y1) / 2), (x + w, y1), (x, y1)]
        if i > 0:
            pts.append((x + tip, (y0 + y1) / 2))
        ax.add_patch(Polygon(pts, closed=True, fc="#A6A6A6" if i == 0 else "#4FA3DD",
                             ec="white", lw=2.5))
        cx = x + w / 2 + (tip / 2 if i > 0 else 0)
        ax.text(cx, 13.5, name, ha="center", va="center", fontsize=12.5,
                fontweight="bold", linespacing=1.15)
        ax.text(cx, 3.6, f"Phase {i}", ha="center", va="center", fontsize=12,
                fontweight="bold")
    save(fig, "design-phases")


# ---------------------------------------------------------------------------
def design_process_flow():
    """The conceptual design process, after Nicolai and Carichner (slide 3).

    Drawn in the pixel coordinates of the source figure (1187 by 907) so the
    arrangement matches it box for box.
    """
    W, H = 1187, 907
    fig, ax = pixel_canvas(W, H)
    NB = "#1F5FA8"   # outline blue
    FB = "#4F86C6"   # filled boxes
    LB = "#9DB9D9"   # wide arrows

    def box(x0, y0, x1, y1, title, items=(), filled=False, ts=11, isz=9.5):
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=FB if filled else "white",
                               ec=NB, lw=2.2, zorder=3))
        tc = "white" if filled else INK
        if items:
            ax.text((x0 + x1) / 2, y0 + 7, title, ha="center", va="top", fontsize=ts,
                    fontweight="bold", color=tc, linespacing=1.1, zorder=4)
            n = title.count("\n") + 1
            ax.text(x0 + 9, y0 + 9 + n * ts * 1.55, "\n".join(items), ha="left",
                    va="top", fontsize=isz, color=tc, linespacing=1.22, zorder=4)
        else:
            ax.text((x0 + x1) / 2, (y0 + y1) / 2, title, ha="center", va="center",
                    fontsize=ts, fontweight="bold", color=tc, linespacing=1.1, zorder=4)

    def arrow(pts, thick=False, head=True):
        c = LB if thick else NB
        lw = 9 if thick else 2
        if len(pts) > 2:
            xs, ys = zip(*pts[:-1])
            ax.plot(xs, ys, color=c, lw=lw, solid_joinstyle="miter",
                    solid_capstyle="projecting", zorder=1)
        p, q = pts[-2], pts[-1]
        if not head:
            ax.plot([p[0], q[0]], [p[1], q[1]], color=c, lw=lw,
                    solid_capstyle="projecting", zorder=1)
            return
        if thick:
            style = "simple,head_length=1.6,head_width=2.6,tail_width=1.0"
            ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=9,
                                         color=c, lw=0, zorder=1, shrinkA=0, shrinkB=0))
        else:
            ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>,head_length=0.7,head_width=0.35",
                                         mutation_scale=12, color=c, lw=2, zorder=2,
                                         shrinkA=0, shrinkB=0))

    def ellipse(cx, cy, text):
        ax.add_patch(Ellipse((cx, cy), 42, 46, fc="white", ec=NB, lw=2.2, zorder=3))
        ax.text(cx, cy, text, ha="center", va="center", fontsize=10.5, fontweight="bold",
                zorder=4)

    def diamond(cx, cy, hw, hh, text):
        ax.add_patch(Polygon([(cx - hw, cy), (cx, cy - hh), (cx + hw, cy), (cx, cy + hh)],
                             closed=True, fc="white", ec=NB, lw=2.2, zorder=3))
        ax.text(cx, cy, text, ha="center", va="center", fontsize=10.5, fontweight="bold",
                linespacing=1.05, zorder=4)

    def inset(x0, y0, x1, y1):
        a = fig.add_axes([x0 / W, 1 - y1 / H, (x1 - x0) / W, (y1 - y0) / H])
        a.set_xticks([])
        a.set_yticks([])
        for s in a.spines.values():
            s.set_edgecolor("#888888")
        a.set_facecolor("#F2F2F2")
        return a

    # --- left column: customer to concept of operations
    box(15, 83, 130, 125, "Customer")
    box(15, 155, 130, 215, "Mission\nReqs")
    box(15, 245, 130, 305, "Concept\nof Ops")
    arrow([(72, 125), (72, 155)])
    arrow([(72, 215), (72, 245)])

    # --- requirements negotiation, GO, design guidelines
    box(188, 8, 315, 60, "Evaluate\nReq/ConOps")
    box(188, 80, 340, 135, "Negotiate\nwith Customer", filled=True)
    arrow([(250, 60), (250, 80)], head=False)
    arrow([(188, 108), (155, 108), (155, 268)], thick=True)
    arrow([(130, 275), (178, 275)], thick=True)
    star = []
    for k in range(24):
        r = 36 if k % 2 == 0 else 24
        a = np.pi / 12 * k
        star.append((225 + r * np.cos(a), 180 + r * np.sin(a)))
    ax.add_patch(Polygon(star, closed=True, fc="#C9D9EE", ec=NB, lw=1.8, zorder=3))
    ax.text(225, 180, "GO", ha="center", va="center", fontsize=12, fontweight="bold",
            zorder=4)
    box(323, 150, 425, 210, "Selection\nCriteria")
    arrow([(323, 180), (280, 180), (280, 225)])
    box(178, 225, 288, 370, "Design\nGuidelines",
        ["Radius", "Payload", "Altitude", "Signature", "etc."])
    box(325, 240, 450, 305, "Configuration\nSketches")
    arrow([(288, 272), (325, 272)], thick=True)
    arrow([(450, 272), (490, 272)], thick=True)

    # --- concept stack
    for k in (2, 1, 0):
        d = 10 * k
        ax.add_patch(Rectangle((490 + d, 200 - d), 130, 110, fc="white", ec="#555555",
                               lw=2.2, zorder=3 + (2 - k) * 0.1))
    ax.text(497, 207, "Concept No. 1", ha="left", va="top", fontsize=10.5,
            fontweight="bold", fontstyle="italic", zorder=4)
    planform = [(612, 262), (575, 254), (562, 236), (549, 236), (557, 254), (538, 254),
                (531, 258), (538, 266), (557, 270), (549, 288), (562, 288), (575, 270)]
    ax.add_patch(Polygon(planform, closed=True, fc="#BBBBBB", ec="#444444", lw=1.2,
                         zorder=4))
    ax.plot([503, 530], [252, 252], color="#444444", lw=1.5, zorder=4)
    ax.plot([516, 516], [240, 252], color="#444444", lw=1.5, zorder=4)
    arrow([(590, 312), (590, 393)], thick=True)
    arrow([(515, 312), (515, 348)])
    box(460, 348, 550, 410, "Initial\nSizing")
    ax.add_patch(RegularPolygon((590, 425), 6, radius=30, orientation=np.pi / 6,
                                fc="#8FB3DB", ec=NB, lw=2.2, zorder=3))
    ax.text(590, 425, "A", ha="center", va="center", fontsize=12, fontweight="bold",
            zorder=4)
    arrow([(505, 410), (505, 470)])
    box(443, 470, 565, 530, "Select\nConfiguration")
    arrow([(505, 530), (505, 580)])
    box(443, 580, 565, 725, "Functional\nInputs",
        ["Aero", "Propulsion", "Weights", "Mat'l Structure", "Signature"])

    # --- inputs to the design guidelines
    box(12, 350, 140, 520, "System\nApproach",
        ["Tactics", "Support Aircraft", "ECM", "Subsystems", "etc."])
    box(315, 350, 425, 470, "Technology", ["Materials", "Stealth", "Propulsion", "etc."])
    box(158, 465, 300, 605, "Measures\nof Merit",
        ["Life Cycle Cost (LCC)", "Takeoff Weight", "Targets Killed/LCC", "etc."])
    arrow([(140, 430), (200, 372)])
    arrow([(315, 400), (266, 372)])
    arrow([(232, 465), (232, 372)])
    arrow([(158, 575), (75, 575), (75, 685)])

    # --- design trades and the baseline
    box(183, 640, 330, 690, "Design Trades", filled=True)
    arrow([(443, 665), (330, 665)])
    a = inset(183, 695, 330, 795)
    a.set_xlim(0, 1)
    a.set_ylim(0, 1)
    a.text(0.03, 0.5, "MoM", ha="left", va="center", fontsize=8.5, fontweight="bold")
    a.plot([0.2, 0.2], [0.08, 0.92], color=INK, lw=2.5)
    for x0, lab in ((0.30, "W/S"), (0.60, "T/W")):
        for j in range(3):
            xs = np.linspace(x0 + 0.05 * j, x0 + 0.05 * j + 0.17, 20)
            a.plot(xs, 0.25 + 0.14 * j + 0.5 * (xs - x0 - 0.05 * j) ** 2 * 4, color=NB,
                   lw=0.8)
            a.plot([x0 + 0.06 * j, x0 + 0.06 * j + 0.1], [0.22, 0.6], color=NB, lw=0.8)
        a.text(x0 + 0.08, 0.72, lab, fontsize=6.5, rotation=40, color=INK)
    ax.text(336, 712, "W/S\nT/W\nAR\nSweep\netc.", ha="left", va="top", fontsize=9.5,
            linespacing=1.2)
    arrow([(183, 725), (145, 725)])
    box(10, 685, 145, 765, "Select\nPreferred\nConfiguration")
    arrow([(75, 765), (75, 820)])
    box(15, 820, 140, 885, "Baseline\nDesign")
    arrow([(140, 855), (655, 855), (655, 60), (683, 60)], thick=True)
    arrow([(590, 455), (590, 745), (380, 745)], thick=True)

    # --- trades loop, right side
    box(683, 30, 783, 90, "Mission\nTrades", filled=True)
    ax.text(792, 6, "Radius\nPayload\nSpeed\nBox Size\nHover\nTime\netc.", ha="left",
            va="top", fontsize=9.5, linespacing=1.2)
    ax.text(858, 52, "MoM", ha="center", va="center", fontsize=8.5, fontweight="bold")
    a = inset(870, 15, 1050, 90)
    a.set_xlim(-10, 10)
    a.set_ylim(-1.1, 1.1)
    a.plot([-10, -10], [-1.1, 1.1], color=INK, lw=2.5)
    a.axhline(0, color=INK, lw=1)
    for k, lab in ((0.09, "Payload"), (0.06, "Speed"), (0.03, "Radius")):
        a.plot([-10, 10], [-10 * k, 10 * k], color=NB, lw=0.8)
        a.text(9.8, 10 * k, lab, fontsize=5.5, ha="right", va="bottom", rotation=12)
    for t in (-10, -5, 0, 5, 10):
        a.text(t, -1.05, f"{t:+d}" if t else "0", fontsize=5.5, ha="center", va="bottom")
    arrow([(1050, 52), (1075, 52), (1075, 250)], thick=True)

    box(1015, 250, 1130, 315, "Technology\nTrades", filled=True)
    ax.text(966, 388, "MoM", ha="center", va="center", fontsize=9, fontweight="bold")
    a = inset(990, 320, 1155, 455)
    a.set_xlim(-10, 10)
    a.set_ylim(-1.1, 1.1)
    a.plot([-10, -10], [-1.1, 1.1], color=INK, lw=2.5)
    a.axhline(0, color=INK, lw=1)
    for k, lab, dx in ((-0.09, "TSFC", -1), (-0.06, "Weight", -1), (0.07, "L/D", 1)):
        a.plot([-9, 9], [-9 * k, 9 * k], color=NB, lw=0.8)
        a.text(9.5 * dx, 9 * k * dx, lab, fontsize=5.5, ha="center", va="bottom")
    for t in (-10, -5, 0, 5, 10):
        a.text(t, -1.05, f"{t:+d}" if t else "0", fontsize=5.5, ha="center", va="bottom")
    ax.text(1085, 460, "TSFC\nEngine T/W\nEmpty Weight\n$C_D$\nL/D\n$C_{L\\,max}$\netc.",
            ha="left", va="top", fontsize=9.5, linespacing=1.2)
    arrow([(1072, 455), (1072, 585), (1006, 585)], thick=True)

    diamond(966, 585, 40, 46, "Happy\n??")
    box(1058, 705, 1165, 765, "Risk\nAssessment")
    arrow([(1058, 735), (1030, 735), (1030, 625)], thick=True)
    ellipse(966, 480, "No")
    arrow([(966, 539), (966, 503)])
    box(923, 250, 1003, 310, "Iterate\nDesign\n(back to A)", ts=10)
    arrow([(966, 457), (966, 310)])
    ellipse(966, 680, "Yes")
    arrow([(966, 631), (966, 657)])
    box(795, 540, 923, 625, "Share\nTrade Results\nwith Customer", filled=True)
    arrow([(945, 680), (859, 680), (859, 625)])
    arrow([(859, 540), (859, 425)])
    diamond(859, 375, 42, 50, "Req\nChange\n??")
    ellipse(813, 280, "No")
    arrow([(817, 375), (813, 303)])
    box(681, 250, 748, 310, "Point\nDesign")
    arrow([(792, 280), (748, 280)])
    ellipse(859, 185, "Yes")
    arrow([(859, 325), (859, 208)])
    box(928, 158, 1001, 215, "Back\nto GO")
    arrow([(880, 185), (928, 185)])
    ax.text(681, 325, "OML\nGen Arrangement\nPerformance\nSubsystems\nRisk Analysis\n"
            "Req Analysis\nSys Engr Results\nManagement Plan\nRM&S\nLCC Analysis\n"
            "System Specs\nTest Planning\nTRL = 3-4", ha="left", va="top", fontsize=9.5,
            linespacing=1.2)
    arrow([(695, 310), (695, 772), (783, 772)], thick=True)
    ax.add_patch(FancyBboxPatch((783, 720), 175, 105, boxstyle="round,pad=0,rounding_size=22",
                                fc=FB, ec=NB, lw=2.2, zorder=3))
    ax.text(870, 772, "Preliminary\nDesign", ha="center", va="center", fontsize=14,
            fontweight="bold", color="white", zorder=4)
    ax.text(1170, 890, "MoM = Measure of Merit", ha="right", va="center", fontsize=10,
            fontstyle="italic")
    save(fig, "design-process-flow")


# ---------------------------------------------------------------------------
def design_funnel():
    """Conceptual, preliminary and detail design, after Raymer (slide 4)."""
    fig, ax = plt.subplots(figsize=(8.6, 8.2))
    ax.set_xlim(0, 100)
    ax.set_ylim(100, 0)
    ax.axis("off")
    OR, TT = "#C55A11", "#A04F00"
    stages = [
        ("Conceptual Design",
         ["What requirements drive the design?", "What should it look like? Weight? Cost?",
          "What tradeoffs should be considered?", "What technologies should be used?",
          "Do these requirements produce a viable &", "salable plane?"]),
        ("Preliminary Design",
         ["Freeze the configuration", "Develop lofting (surface definition)",
          "Develop test and analytical database", "Design major items",
          "Develop actual cost estimate (statistical)", "(“You bet your company”)"]),
        ("Detail Design",
         ["Design actual pieces to be built", "Design tooling and fabrication process",
          "Test major items - structure, landing gear, …",
          "Finalize weight and performance estimates",
          "(NOW you learn the real numbers!)"]),
    ]
    x0, x1, xm, dip = 30, 94, 62, 4.5
    tops = [3, 33.5, 64]
    hts = [26, 26, 23]
    for (title, lines), top, h in zip(stages, tops, hts):
        bot = top + h
        ax.plot([x0, x0, x1, x1], [bot, top, top, bot], color=OR, lw=1.8)
        ax.plot([x0 - 4, xm, x1 + 4], [bot, bot + dip, bot], color=OR, lw=1.8)
        ax.text(xm, top + 2.2, title, ha="center", va="top", color=TT, fontsize=13.5,
                fontweight="bold")
        ax.text(xm, top + 6.3, "\n".join(lines), ha="center", va="top", fontsize=11.5,
                linespacing=1.33)
    ax.add_patch(Polygon([(2, 7), (22, 7), (22, 3.5), (30, 11), (22, 18.5), (22, 15),
                          (2, 15)], closed=True, fc="white", ec=OR, lw=1.8))
    ax.text(12, 11, "Requirements", ha="center", va="center", fontsize=12.5)
    ax.add_patch(Rectangle((44, 92.5), 36, 6, fc="white", ec=OR, lw=1.8))
    ax.text(62, 95.5, "Fabrication", ha="center", va="center", fontsize=12.5)
    save(fig, "design-funnel")


# ---------------------------------------------------------------------------
def narrowbody_production():
    """Narrow-body production, values and order as on the lecture slide (slide 7)."""
    data = [
        ("McDonnell Douglas MD-80/90", 1191),
        ("COMAC C919", 305),
        ("Mitsubishi SpaceJet", 0),
        ("Bombardier CSeries (A220)", 220),
        ("Sukhoi Superjet 100", 200),
        ("Embraer E-Jets E2 (Second Generation)", 200),
        ("Bombardier CRJ Family", 1945),
        ("Embraer E-Jets (First Generation)", 1500),
        ("Fokker 100", 283),
        ("Fokker 70", 47),
        ("737 Family", 10500),
        ("Airbus A318/A319/A320/A321", 16000),
    ]
    names = [d[0] for d in data][::-1]
    vals = [d[1] for d in data][::-1]
    fig, ax = plt.subplots(figsize=(10, 7))
    bars = ax.barh(names, vals, color="#87CEEB", edgecolor="#2F6F8F", lw=0.6, height=0.72)
    for b, v in zip(bars, vals):
        ax.text(b.get_width() + 150, b.get_y() + b.get_height() / 2, f"{v}", va="center",
                fontsize=12)
    ax.set_title("Narrow Body Aircraft Production", fontsize=15, pad=12)
    ax.set_xlabel("Number of Aircraft Produced", fontsize=13)
    ax.set_xlim(0, 17500)
    ax.set_xticks(range(0, 17501, 2000))
    ax.set_xticklabels([])
    ax.tick_params(axis="y", length=5, labelsize=12)
    ax.grid(axis="x", color="#999999", lw=0.8, ls="--")
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    assert vals[0] == 16000 and dict(data)["Mitsubishi SpaceJet"] == 0
    save(fig, "narrowbody-production")


# ---------------------------------------------------------------------------
def system_levels():
    """Five levels of an aircraft system, after Sadraey (slide 9, text only)."""
    levels = [
        ("Level 1", "System of systems",
         "Air transportation or defense system: aircraft, missiles,\n"
         "satellites, ground stations, airports, air traffic management"),
        ("Level 2", "System",
         "The aircraft and related systems: operators, trainers,\n"
         "manufacturing plants, maintenance shops"),
        ("Level 3", "Subsystem",
         "Flight control, hydraulic, electric, avionics, powerplant,\n"
         "fuel, air conditioning, structure"),
        ("Level 4", "Component",
         "Wing, fuselage, tail, landing gear, radar, pumps, nacelles,\n"
         "control surfaces, auxiliary power unit"),
        ("Level 5", "Part",
         "Fittings, fasteners, blades, propellers, screws, nuts, ribs,\n"
         "spars, frames, stiffeners, skin, shafts, pipes"),
    ]
    fig, ax = plt.subplots(figsize=(10.5, 6.4))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 62)
    ax.axis("off")
    fills = [GOLD, DUST, LIGHT, LIGHT, "white"]
    for i, ((lv, name, ex), fc) in enumerate(zip(levels, fills)):
        y = 54 - i * 12
        indent = i * 2.5
        ax.add_patch(FancyBboxPatch((1 + indent, y - 4.8), 27 - indent, 9.6,
                                    boxstyle="round,pad=0.2,rounding_size=0.8",
                                    fc=fc, ec=AGED, lw=1.6))
        ax.text(14.5 + indent / 2, y + 1.9, lv, ha="center", va="center", fontsize=12.5,
                fontweight="bold")
        ax.text(14.5 + indent / 2, y - 2.0, name, ha="center", va="center", fontsize=12.5)
        ax.text(32, y, ex, ha="left", va="center", fontsize=12, linespacing=1.3)
        if i < 4:
            ax.add_patch(FancyArrowPatch((6 + indent, y - 5.0), (6 + indent, y - 7.1),
                                         arrowstyle="-|>", mutation_scale=16, lw=1.4,
                                         color=INK, shrinkA=0, shrinkB=0))
    save(fig, "system-levels")


# ---------------------------------------------------------------------------
def combat_mission_profile():
    """Generic combat mission profile with eight phases, after Raymer (slide 17)."""
    fig, ax = plt.subplots(figsize=(10, 6.2))
    takeoff_x = np.linspace(0, 6, 12)
    takeoff_y = 12 * (takeoff_x / 6) ** 2.2
    x = list(takeoff_x) + [18, 40, 41.5, 48, 53, 66, 86, 87, 87.5, 95, 96]
    y = list(takeoff_y) + [70, 73, 61, 61, 37, 80, 82, 25, 25, 0, 0]
    ax.fill_between(x, y, color="#AFC6E2")
    ax.plot(x, y, color=INK, lw=2.4)
    t = np.linspace(0, 0.94, 400)
    ax.plot(48 + 5 * t + 1.8 * np.cos(2 * np.pi * 4 * t),
            61 - 24 * t + 3.5 * np.sin(2 * np.pi * 4 * t), color=INK, lw=1.8)
    ax.add_patch(Ellipse((87.6, 25), 6.5, 4.5, fc="none", ec=INK, lw=1.8))
    labels = [(10.5, 4, "Phase 1"), (19.5, 38, "Phase 2"), (29, 77, "Phase 3"),
              (46.5, 66.5, "Phase 4"), (39.5, 47, "Phase 5"), (76, 86, "Phase 6"),
              (93.5, 31, "Phase 7"), (97, 10, "Phase 8")]
    for lx, ly, s in labels:
        ax.text(lx, ly, s, ha="center", va="center", fontsize=13, fontweight="bold",
                fontstyle="italic")
    legend = ["Engine start and takeoff", "Accelerate and climb to cruise speed/alt",
              "Cruise to destination", "Accelerate to high speed dash", "Combat",
              "Cruise back to origin", "Loiter", "Land, taxi, engine shutdown"]
    for i, s in enumerate(legend):
        yy = 27 - 3.2 * i
        ax.text(46, yy, f"Phase {i + 1}", fontsize=8.5, fontstyle="italic", va="center")
        ax.text(53, yy, s, fontsize=8.5, fontstyle="italic", va="center")
    ax.set_xlabel("Distance", fontsize=14, fontweight="bold")
    ax.set_ylabel("Altitude", fontsize=14, fontweight="bold")
    ax.set_xticks([0, 96], ["origin", "origin"])
    ax.tick_params(axis="x", labelsize=11)
    for lab in ax.get_xticklabels():
        lab.set_fontstyle("italic")
    ax.set_yticks([])
    ax.set_xlim(-0.5, 103)
    ax.set_ylim(0, 95)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_linewidth(2)
    save(fig, "combat-mission-profile")


# ---------------------------------------------------------------------------
def navy_training_mission():
    """Training flight from the Navy Jet Trainer RFP (RFP page 2)."""
    fig, ax = plt.subplots(figsize=(10, 4.6))
    x = [0, 4, 7, 21, 37, 41, 53, 57, 71, 85, 89]
    y = [0, 0, 0, 20000, 20000, 10000, 10000, 20000, 20000, 0, 0]
    ax.plot(x, y, color=INK, lw=1.8)
    seg = [(2, 1400, "1"), (5.5, 1400, "2"), (12.5, 10000, "3"), (29, 21300, "4"),
           (40.5, 15500, "5"), (47, 11300, "6"), (54, 15500, "7"), (64, 21300, "8"),
           (79.5, 10000, "9"), (88, 1400, "10")]
    for sx, sy, s in seg:
        ax.text(sx, sy, s, ha="center", va="center", fontsize=12)
    for xa, xb in ((7, 41), (53, 85)):
        ax.annotate("", xy=(xb, -4200), xytext=(xa, -4200),
                    arrowprops=dict(arrowstyle="<|-|>", color="#4472C4", lw=1.6))
        ax.text((xa + xb) / 2, -4200, "50 nm", ha="center", va="center", fontsize=12,
                bbox=dict(fc="white", ec="#BBBBBB", pad=3))
    ax.set_yticks([0, 10000, 20000], ["0 ft", "10,000 ft", "20,000 ft"])
    ax.set_xticks([])
    ax.set_xlabel("Distance (not to scale)")
    ax.set_ylabel("Altitude")
    ax.set_ylim(-6500, 23500)
    ax.set_xlim(-1, 91)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_linewidth(2)
    save(fig, "navy-training-mission")


def navy_ferry_mission():
    """Ferry flight from the Navy Jet Trainer RFP (RFP page 3)."""
    fig, ax = plt.subplots(figsize=(10, 4.2))
    x = [0, 4, 7, 22, 72, 87, 91]
    y = [0, 0, 0, 1, 1, 0, 0]
    ax.plot(x, y, color=INK, lw=1.8)
    seg = [(2, 0.07, "1"), (5.5, 0.07, "2"), (13, 0.5, "3"), (47, 1.07, "4"),
           (81, 0.5, "5"), (89, 0.07, "6")]
    for sx, sy, s in seg:
        ax.text(sx, sy, s, ha="center", va="center", fontsize=12)
    ax.annotate("", xy=(87, -0.22), xytext=(7, -0.22),
                arrowprops=dict(arrowstyle="<|-|>", color="#4472C4", lw=1.6))
    ax.text(47, -0.22, "600 nm, segments 3 to 5", ha="center", va="center", fontsize=12,
            bbox=dict(fc="white", ec="#BBBBBB", pad=3))
    ax.set_yticks([0, 1], ["0 ft", "Cruise altitude\n(team choice)"])
    ax.set_xticks([])
    ax.set_xlabel("Distance (not to scale)")
    ax.set_ylabel("Altitude")
    ax.set_ylim(-0.38, 1.2)
    ax.set_xlim(-1, 93)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_linewidth(2)
    save(fig, "navy-ferry-mission")


if __name__ == "__main__":
    design_phases()
    design_process_flow()
    design_funnel()
    narrowbody_production()
    system_levels()
    combat_mission_profile()
    navy_training_mission()
    navy_ferry_mission()
