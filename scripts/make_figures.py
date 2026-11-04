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
    "design-mission-profile": "lecture-02",
    "empty-weight-trends": "lecture-02",
    "trend-honesty": "assignments",
    "pugh-controlled-convergence": "lecture-04",
    "pugh-matrix-runs": "lecture-04",
    "training-flight-profile": "lecture-02",
    "wing-planform": "lecture-05",
    "naca-families": "lecture-05",
    "section-data-schematic": "lecture-05",
    "stall-classes": "lecture-05",
    "drag-divergence": "lecture-05",
    "wing-height": "lecture-05",
    "aspect-ratio-effects": "lecture-05",
    "taper-lift-distribution": "lecture-05",
    "sweep-components": "lecture-05",
    "korn-sweep": "lecture-05",
    "pitch-up-boundary": "lecture-05",
    "wing-incidence": "lecture-05",
    "lift-curve-slope": "lecture-05",
    "stall-speed": "lecture-05",
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


# ---------------------------------------------------------------------------
def design_mission_profile():
    """Design mission with numbered points 0 to 4 (sizing lecture, slide 8)."""
    fig, ax = plt.subplots(figsize=(9, 3.4))
    pts = [(0, 0), (0.5, 0), (1.9, 1.0), (6.9, 1.4), (6.9, 0)]
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=AGED, lw=3, solid_capstyle="round")
    ax.plot(xs, ys, "o", color="#555960", ms=7)
    for (x, y), lab, dy in zip(pts, "01234", (-0.17, -0.17, 0.14, 0.14, -0.17)):
        ax.text(x, y + dy, lab, ha="center", va="center", fontsize=13, color="#555960")
    ax.text(0.25, -0.42, "Warm-up, taxi, takeoff", ha="center", va="center", fontsize=13,
            color=AGED)
    ax.text(0.95, 0.55, "Climb", ha="right", va="center", fontsize=13, color=AGED)
    ax.text(4.4, 1.33, "Cruise-climb", ha="center", va="bottom", fontsize=13, color=AGED)
    ax.text(7.1, 0.7, "No-range\ndescent", ha="left", va="center", fontsize=13, color=AGED,
            linespacing=1.2)
    ax.annotate("", xy=(6.9, -0.65), xytext=(0.5, -0.65),
                arrowprops=dict(arrowstyle="<->", color="#555960", lw=1.2))
    ax.text(3.7, -0.65, "still air range", ha="center", va="center", fontsize=13,
            color="#555960", bbox=dict(fc="white", ec="none", pad=2))
    ax.set_xlim(-0.6, 8.4)
    ax.set_ylim(-0.95, 1.75)
    ax.axis("off")
    save(fig, "design-mission-profile")


# ---------------------------------------------------------------------------
def empty_weight_trends():
    """Empty-weight trend lines from Nicolai Table 5.1, with the F9F-5 point
    (Nicolai Table I.5a) used in the lecture's check of the regression."""
    fig, ax = plt.subplots(figsize=(8, 6))
    w = np.logspace(3, 5, 100)
    ax.plot(w, 0.747 * w ** 0.993, color="#0072B2", lw=2.2, ls="-",
            label="Military jet trainer, $W_e = 0.747\,W_{TO}^{\,0.993}$")
    ax.plot(w, 0.911 * w ** 0.947, color="#D55E00", lw=2.2, ls="--",
            label="Multipurpose fighter and light civil, $W_e = 0.911\,W_{TO}^{\,0.947}$")
    ax.plot([17500], [10223], "s", color=INK, ms=9, label="Grumman F9F-5 (17,500 lb, 10,223 lb)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e3, 1e5)
    ax.set_ylim(5e2, 1e5)
    ax.set_xlabel("Takeoff gross weight, $W_{TO}$ (lb)", fontsize=13)
    ax.set_ylabel("Empty weight, $W_e$ (lb)", fontsize=13)
    ax.grid(True, which="both", color="#CCCCCC", lw=0.6)
    ax.legend(fontsize=11, loc="upper left")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    # the lecture's check: the trainer line over-predicts the F9F-5 by 19 percent
    assert abs(0.747 * 17500 ** 0.993 / 10223 - 1.19) < 0.01
    assert abs(0.911 * 17500 ** 0.947 / 10223 - 0.93) < 0.01
    save(fig, "empty-weight-trends")


# ---------------------------------------------------------------------------
def trend_honesty():
    """Sample figure from the A02 brief (Deliverable 3): a least-squares line
    appears whether or not the data supports one. Invented data, same seed as
    the brief's figure. Left panel one aircraft class, right panel mixed classes."""
    rng = np.random.default_rng(42)
    x1 = np.sort(rng.uniform(10, 70, 9))                  # gross weight, 1000 lb
    y1 = 0.68 - 0.0025 * x1 + rng.normal(0, 0.006, x1.size)
    x2 = np.sort(rng.uniform(10, 70, 9))
    y2 = rng.normal(0.55, 0.055, x2.size)

    def fit_r2(x, y):
        b, a = np.polyfit(x, y, 1)
        yhat = a + b * x
        return a, b, 1 - np.sum((y - yhat) ** 2) / np.sum((y - y.mean()) ** 2)

    a1, b1, r2_1 = fit_r2(x1, y1)
    a2, b2, r2_2 = fit_r2(x2, y2)
    print(f"trend-honesty: left R^2 = {r2_1:.3f}, right R^2 = {r2_2:.3f}")
    # the point of the figure; refuse to write a version that does not show it
    assert r2_1 > 0.85, f"left panel shows no real trend (R^2={r2_1:.3f})"
    assert r2_2 < 0.30, f"right panel shows a trend (R^2={r2_2:.3f})"

    fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.6), sharey=True, sharex=True)
    for ax, x, y, a, b, r2, title in (
        (axes[0], x1, y1, a1, b1, r2_1, "One aircraft class"),
        (axes[1], x2, y2, a2, b2, r2_2, "Mixed classes"),
    ):
        xf = np.linspace(8, 72, 50)
        ax.plot(x, y, "o", color="#0072B2", ms=7, zorder=3)
        ax.plot(xf, a + b * xf, "--", color="#D55E00", lw=2, zorder=2)
        ax.set_title(title)
        ax.set_xlabel("Takeoff gross weight (1000 lb)")
        ax.text(0.04, 0.07, f"$R^2$ = {r2:.2f}", transform=ax.transAxes)
        ax.grid(True, lw=0.4, alpha=0.5)
    axes[0].set_ylabel("Empty-weight fraction (–)")
    fig.tight_layout()
    save(fig, "trend-honesty")


# ---------------------------------------------------------------------------
STEEL = "#555960"


def pugh_controlled_convergence():
    """Controlled convergence, after the diagram in Pugh (1991) reproduced on
    the concept-selection lecture's source slide: the set of concepts narrows
    at each convergence step and widens at each generation step, until one
    concept is left."""
    fig, ax = plt.subplots(figsize=(7.8, 9.4))
    ax.set_xlim(-6.5, 5.0)
    ax.set_ylim(-0.9, 11.2)
    ax.axis("off")
    # (y, half-width) of the funnel at each level, top to bottom
    levels = [(9.0, 3.6), (7.6, 1.9), (7.0, 2.5), (5.4, 1.5), (4.8, 1.9),
              (3.2, 1.0), (2.6, 1.3), (1.2, 0.6), (0.8, 0.8), (0.0, 0.0)]

    def edge(y):
        """Half-width of the funnel at height y, by linear interpolation."""
        for (y0, w0), (y1, w1) in zip(levels[:-1], levels[1:]):
            if y1 <= y <= y0:
                return w1 + (w0 - w1) * (y - y1) / (y0 - y1)
        return 0.0
    for sign in (-1, 1):
        for (y0, w0), (y1, w1) in zip(levels[:-1], levels[1:]):
            ax.annotate("", xy=(sign * w1, y1), xytext=(sign * w0, y0),
                        arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4,
                                        mutation_scale=12, shrinkA=0, shrinkB=0))
    # the specification feeds concept generation, which spreads the first set
    ax.annotate("", xy=(0, 9.9), xytext=(0, 10.75),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4, mutation_scale=12))
    ax.text(0, 10.85, "Specification (PDS)", ha="center", va="bottom", fontsize=12)
    ax.text(0, 9.75, "Concept generation", ha="center", va="top", fontsize=12)
    ax.annotate("", xy=(-3.6, 9.0), xytext=(0, 9.0),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2, mutation_scale=12))
    ax.annotate("", xy=(3.6, 9.0), xytext=(0, 9.0),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2, mutation_scale=12))
    ax.text(0, 8.9, "Initial number of\nconcepts, from the PDS", ha="center", va="top",
            fontsize=11, bbox=dict(fc="white", ec="none", pad=1.5))
    centre = [(7.6, "Initial number reduced"), (7.0, "New ones added"),
              (5.4, "Further reduction (FR)"), (4.8, "Further addition (FA)"),
              (3.2, "FR"), (2.6, "FA"), (1.2, "FR"), (0.8, "FA")]
    for y, s in centre:
        ax.text(0, y, s, ha="center", va="center", fontsize=11,
                bbox=dict(fc="white", ec="none", pad=1.0))
    ax.text(0, -0.25, "Concept selected", ha="center", va="top", fontsize=12)
    # what is applied at each step, on the left
    side = [(8.3, "Apply controlled\nconvergence (CC)"), (7.3, "Apply concept\ngeneration (CG)"),
            (6.2, "CC"), (5.1, "CG"), (4.0, "CC"), (2.9, "CG"), (1.9, "CC"), (1.0, "CG"), (0.45, "CC")]
    for y, s in side:
        ax.annotate(s, xy=(-edge(y), y), xytext=(-6.4, y), ha="left", va="center", fontsize=11,
                    color=STEEL,
                    arrowprops=dict(arrowstyle="-|>", color=STEEL, lw=1.0, mutation_scale=10,
                                    shrinkA=4, shrinkB=2))
    save(fig, "pugh-controlled-convergence")


def pugh_matrix_runs():
    """The sketch on the lecture slide: the number of concepts over successive
    matrix runs. Eliminations dominate; hybrids add columns briefly."""
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    ax.set_xlim(-0.25, 5.1)
    ax.set_ylim(-0.7, 3.35)
    ax.axis("off")
    for xy in ((4.7, 0), (0, 2.95)):
        ax.annotate("", xy=xy, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=STEEL, lw=1.3, mutation_scale=12))
    ax.text(4.7, -0.12, "matrix runs", ha="right", va="top", fontsize=12, color=STEEL)
    ax.text(0.1, 3.0, "concepts", ha="left", va="bottom", fontsize=12, color=STEEL)
    ax.plot([0.3, 1.2, 1.5, 2.4, 2.7, 3.6, 4.2], [2.5, 1.5, 1.75, 0.95, 1.15, 0.55, 0.45],
            color=AGED, lw=2.8, solid_capstyle="round", solid_joinstyle="round")
    ax.text(1.45, 1.85, "added hybrids", ha="left", va="bottom", fontsize=12, color=AGED)
    ax.text(3.55, 0.95, "winner emerges", ha="left", va="bottom", fontsize=12, color=AGED)
    save(fig, "pugh-matrix-runs")


def training_flight_profile():
    """The training flight as drawn on the design-missions slide: the ten
    RFP segments with the conditions the RFP states written on the profile."""
    GRAY = "#6F727B"
    fig, ax = plt.subplots(figsize=(11.5, 3.9))
    ax.set_xlim(-1.3, 14.2)
    ax.set_ylim(-1.15, 3.0)
    ax.axis("off")
    for y, s in ((1.0, "10,000 ft"), (2.0, "20,000 ft")):
        ax.plot([0, 13.3], [y, y], ls="--", color=GRAY, lw=0.9)
        ax.text(-0.15, y, s, ha="right", va="center", color=GRAY, fontsize=11)
    ax.annotate("", xy=(13.7, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=STEEL, lw=1.3, mutation_scale=12))
    xs = [0, 1.2, 2.6, 4.6, 5.4, 7.4, 8.2, 10.2, 11.0, 11.2, 11.45, 11.7, 11.95, 12.2, 12.45, 12.7]
    ys = [0, 0, 2, 2, 1, 1, 2, 2, 0, 0, 0.3, 0, 0.3, 0, 0.3, 0]
    ax.plot(xs, ys, color=AGED, lw=3, solid_joinstyle="round", solid_capstyle="round")
    ax.text(0.6, -0.12, "Segments 1 and 2: 15 min idle,\n1 min takeoff thrust",
            ha="center", va="top", color=STEEL, fontsize=11)
    ax.text(3.6, 2.12, "Segments 3 and 4: climb at 250 KCAS, cruise to 50 nmi",
            ha="center", va="bottom", color=STEEL, fontsize=11)
    ax.text(5.55, 1.42, "Segment 5: descent, idle", ha="left", va="bottom", color=STEEL, fontsize=11)
    ax.text(6.4, 0.88, "Segment 6: 30 min at military thrust, M 0.60",
            ha="center", va="top", color=STEEL, fontsize=11)
    ax.text(9.2, 2.12, "Segments 7 and 8: climb, return", ha="center", va="bottom",
            color=STEEL, fontsize=11)
    ax.text(11.15, 0.72, "Segment 9: descent, idle", ha="left", va="bottom", color=STEEL, fontsize=11)
    ax.text(11.95, -0.12, "Segment 10: FCLP, 30 min at approach\nspeed, landing configuration",
            ha="center", va="top", color=STEEL, fontsize=11)
    ax.text(11.3, 1.75, "Reserve: 30 min at\nmaximum endurance", ha="left", va="center",
            color=AGED, fontsize=11)
    save(fig, "training-flight-profile")


# ---------------------------------------------------------------------------
# Lecture 5, Aerodynamics: Airfoil and Wing. The deck shows figures cropped
# from Gudmundsson (2022) and Nicolai and Carichner (2010) for classroom use.
# The book cannot reproduce those, so each figure here is either computed from
# the equation the slide gives, drawn from public-domain NACA geometry, or a
# labeled schematic with invented curves, and its caption says which.
BLUE, VERM, GREEN = "#0072B2", "#D55E00", "#009E73"


def _clean_axes(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(True, color="#DDDDDD", lw=0.6)


def wing_planform():
    """Planform nomenclature: span, root and tip chords, leading-edge sweep,
    the mean geometric chord and its spanwise station."""
    AR, lam, sweep = 6.0, 0.4, np.radians(25)
    S = 1.0
    b = np.sqrt(AR * S)
    cr = 2 * S / (b * (1 + lam))
    ct = lam * cr
    cmgc = 2 / 3 * cr * (1 + lam + lam ** 2) / (1 + lam)
    ymgc = b / 6 * (1 + 2 * lam) / (1 + lam)
    xmgc = ymgc * np.tan(sweep)
    fig, ax = plt.subplots(figsize=(9, 4.6))
    ax.set_aspect("equal")
    ax.axis("off")
    half = b / 2
    xle_t = half * np.tan(sweep)
    for sgn in (-1, 1):
        xs = [0, sgn * half, sgn * half, 0]
        ys = [0, -xle_t, -xle_t - ct, -cr]
        ax.plot(xs + [xs[0]], ys + [ys[0]], color=INK, lw=1.8)
        # quarter-chord line
        ax.plot([0, sgn * half], [-cr / 4, -xle_t - ct / 4], color=AGED, lw=1.2, ls="--")
    # mean geometric chord at y_MGC
    xle_m = ymgc * np.tan(sweep)
    ax.plot([ymgc, ymgc], [-xle_m, -xle_m - cmgc], color=VERM, lw=2.4)
    ax.text(ymgc + 0.03, -xle_m - cmgc / 2, "$c_{MGC}$", color=VERM, va="center", fontsize=12)
    # span
    ax.annotate("", xy=(half, 0.16), xytext=(-half, 0.16),
                arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1.1))
    ax.text(0, 0.19, "$b$", ha="center", va="bottom", fontsize=13, color=STEEL)
    # root and tip chords
    ax.annotate("", xy=(-0.06, 0), xytext=(-0.06, -cr),
                arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1.1))
    ax.text(-0.09, -cr / 2, "$c_r$", ha="right", va="center", fontsize=13, color=STEEL)
    ax.annotate("", xy=(half + 0.06, -xle_t), xytext=(half + 0.06, -xle_t - ct),
                arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1.1))
    ax.text(half + 0.09, -xle_t - ct / 2, "$c_t$", ha="left", va="center", fontsize=13, color=STEEL)
    # y_MGC and x_MGC
    ax.annotate("", xy=(ymgc, -cr - 0.12), xytext=(0, -cr - 0.12),
                arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1.1))
    ax.text(ymgc / 2, -cr - 0.15, "$y_{MGC}$", ha="center", va="top", fontsize=12, color=STEEL)
    ax.annotate("", xy=(ymgc + 0.25, 0), xytext=(ymgc + 0.25, -xle_m),
                arrowprops=dict(arrowstyle="<->", color=STEEL, lw=1.1))
    ax.text(ymgc + 0.28, -xle_m / 2, "$x_{MGC}$", ha="left", va="center", fontsize=12, color=STEEL)
    # leading-edge sweep angle
    ax.plot([0, 0.55 * half], [0, 0], color=STEEL, lw=0.8, ls=":")
    ang = np.linspace(0, -sweep, 20)
    ax.plot(0.42 * half * np.cos(ang), 0.42 * half * np.sin(ang), color=STEEL, lw=0.9)
    ax.text(0.46 * half, -0.07, r"$\Lambda_{LE}$", fontsize=12, color=STEEL, va="top")
    ax.text(-half * 0.55, -cr - 0.2, "dashed: quarter-chord line", color=AGED,
            fontsize=11, ha="center", va="top")
    ax.text(0, -cr - 0.42, "$S$ is the whole planform area, both halves, to the centerline",
            ha="center", va="top", fontsize=11, color=STEEL)
    ax.set_xlim(-half - 0.3, half + 0.55)
    ax.set_ylim(-cr - 0.6, 0.35)
    save(fig, "wing-planform")


def _naca4(m, p, t, n=200):
    x = 0.5 * (1 - np.cos(np.linspace(0, np.pi, n)))
    yt = 5 * t * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x ** 2 + 0.2843 * x ** 3 - 0.1015 * x ** 4)
    yc = np.where(x < p, m / p ** 2 * (2 * p * x - x ** 2), m / (1 - p) ** 2 * (1 - 2 * p + 2 * p * x - x ** 2)) if p > 0 else 0 * x
    dyc = np.where(x < p, 2 * m / p ** 2 * (p - x), 2 * m / (1 - p) ** 2 * (p - x)) if p > 0 else 0 * x
    th = np.arctan(dyc)
    return x, yc, x - yt * np.sin(th), yc + yt * np.cos(th), x + yt * np.sin(th), yc - yt * np.cos(th)


def _naca5_230(t, n=200):
    # NACA 230xx mean line: m = 0.2025, k1 = 15.957
    x = 0.5 * (1 - np.cos(np.linspace(0, np.pi, n)))
    m, k1 = 0.2025, 15.957
    yc = np.where(x < m, k1 / 6 * (x ** 3 - 3 * m * x ** 2 + m ** 2 * (3 - m) * x), k1 * m ** 3 / 6 * (1 - x))
    dyc = np.where(x < m, k1 / 6 * (3 * x ** 2 - 6 * m * x + m ** 2 * (3 - m)), -k1 * m ** 3 / 6)
    yt = 5 * t * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x ** 2 + 0.2843 * x ** 3 - 0.1015 * x ** 4)
    th = np.arctan(dyc)
    return x, yc, x - yt * np.sin(th), yc + yt * np.cos(th), x + yt * np.sin(th), yc - yt * np.cos(th)


def naca_families():
    """Three NACA sections computed from the published equations: a symmetric
    four-digit section, a cambered four-digit section and a five-digit section."""
    fig, axes = plt.subplots(1, 3, figsize=(11, 2.9))
    items = [(_naca4(0.0, 0.0, 0.12), "NACA 0012: symmetric, 12% thick"),
             (_naca4(0.02, 0.4, 0.12), "NACA 2412: 2% camber at 40% chord"),
             (_naca5_230(0.12), "NACA 23012: camber forward, at 15% chord")]
    for ax, ((x, yc, xu, yu, xl, yl), title) in zip(axes, items):
        ax.fill(np.concatenate([xu, xl[::-1]]), np.concatenate([yu, yl[::-1]]), color=LIGHT, ec=INK, lw=1.6)
        ax.plot(x, yc, color=VERM, lw=1.3, ls="--")
        ax.plot([0, 1], [0, 0], color=STEEL, lw=0.6, ls=":")
        ax.set_aspect("equal")
        ax.set_xlim(-0.03, 1.03)
        ax.set_ylim(-0.17, 0.2)
        ax.axis("off")
        ax.set_title(title, fontsize=11)
    axes[0].text(0.5, -0.15, "dashed: camber line", ha="center", va="top", fontsize=10, color=VERM)
    fig.tight_layout()
    save(fig, "naca-families")


def section_data_schematic():
    """What to read off a section's lift curve and drag polar. Invented smooth
    curves; only the labeled features matter."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))
    a = np.linspace(-6, 20, 300)
    a0, slope, amax = -2.0, 0.105, 15.0
    cl_lin = slope * (a - a0)
    cl = np.where(a < 10, cl_lin, cl_lin - 0.012 * (a - 10) ** 2)
    cl = np.where(a > amax, cl[np.argmin(np.abs(a - amax))] - 0.08 * (a - amax), cl)
    clmax = cl.max()
    ax1.plot(a, cl, color=BLUE, lw=2.2)
    ax1.plot([a0 - 1, 8], [slope * (-1), slope * (8 - a0)], color=STEEL, lw=0.9, ls="--")
    ax1.axhline(0, color=STEEL, lw=0.7)
    ax1.axvline(0, color=STEEL, lw=0.7)
    ax1.plot([a0], [0], "o", color=VERM, ms=7)
    ax1.text(a0 - 0.4, -0.2, r"$\alpha_{ZL}$", color=VERM, ha="right", fontsize=12)
    ax1.plot([amax], [clmax], "o", color=VERM, ms=7)
    ax1.text(amax - 0.6, clmax + 0.08, r"$C_{l_{max}}$ at $\alpha_{stall}$", color=VERM, ha="right", fontsize=12)
    ax1.text(5.5, slope * (5.5 - a0) - 0.32, r"slope $C_{l_\alpha}$", color=STEEL, fontsize=12)
    ax1.set_xlabel(r"Angle of attack $\alpha$ (deg)")
    ax1.set_ylabel("Section lift coefficient $C_l$")
    ax1.set_xlim(-6, 20)
    ax1.set_ylim(-0.6, 2.0)
    _clean_axes(ax1)
    cl2 = np.linspace(-0.4, 1.6, 300)
    cd = 0.006 + 0.004 * np.clip(np.abs(cl2 - 0.3) - 0.3, 0, None) ** 1.2 * 6 + 0.011 * (cl2 - 0.3) ** 2
    ax2.plot(cd, cl2, color=BLUE, lw=2.2)
    ax2.axvspan(0.0055, 0.0075, ymin=(0.0 + 0.4) / 2.0, ymax=(0.6 + 0.4) / 2.0, color=DUST, alpha=0.7)
    ax2.text(0.0125, 0.3, "low-drag range\n(the drag bucket)", color=AGED, fontsize=11, va="center")
    ax2.annotate("", xy=(0.0068, 0.3), xytext=(0.0122, 0.3), arrowprops=dict(arrowstyle="-|>", color=AGED, lw=1))
    ax2.plot([0.006], [0.3], "o", color=VERM, ms=7)
    ax2.text(0.0045, 0.3, r"$C_{d_{min}}$", color=VERM, ha="right", va="center", fontsize=12)
    ax2.set_xlabel("Section drag coefficient $C_d$")
    ax2.set_ylabel("Section lift coefficient $C_l$")
    ax2.set_xlim(0, 0.03)
    ax2.set_ylim(-0.4, 1.6)
    _clean_axes(ax2)
    fig.tight_layout()
    save(fig, "section-data-schematic")


def stall_classes():
    """The three stall classes as schematic lift curves: gentle trailing-edge
    stall, a sharper stall, and the abrupt leading-edge stall."""
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.4), sharey=True)
    a = np.linspace(-2, 22, 400)
    titles = ["Class A: trailing-edge stall", "Class B: between A and C", "Class C: leading-edge stall"]
    for i, (ax, t) in enumerate(zip(axes, titles)):
        lin = 0.1 * (a + 2)
        if i == 0:
            cl = np.where(a < 9, lin, lin - 0.011 * (a - 9) ** 2)
            cl = np.where(a > 16, cl[np.argmin(np.abs(a - 16))] - 0.03 * (a - 16), cl)
        elif i == 1:
            cl = np.where(a < 12, lin, lin - 0.02 * (a - 12) ** 2)
            cl = np.where(a > 15, cl[np.argmin(np.abs(a - 15))] - 0.09 * (a - 15), cl)
        else:
            cl = np.where(a < 14, lin, lin[np.argmin(np.abs(a - 14))] - 0.6 - 0.02 * (a - 14))
        cl = cl * 1.5 / cl.max()
        ax.plot(a, cl, color=BLUE, lw=2.2)
        ax.set_title(t, fontsize=11)
        ax.set_xlabel(r"$\alpha$ (deg)")
        ax.set_xlim(-2, 22)
        ax.set_ylim(0, 2.0)
        _clean_axes(ax)
    axes[0].set_ylabel("$C_l$")
    axes[0].text(10, 0.35, "separation grows forward\nfrom the trailing edge", fontsize=10, color=STEEL)
    axes[2].text(3, 0.35, "a leading-edge bubble bursts;\nsharp drop after the peak", fontsize=10, color=STEEL)
    fig.tight_layout()
    save(fig, "stall-classes")


def drag_divergence():
    """Section drag against Mach number, schematic, with the critical Mach
    number and the two definitions of drag divergence the slide gives."""
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    M = np.linspace(0.3, 0.95, 400)
    cd0 = 0.008
    cd = cd0 + 0.0 * M + np.where(M > 0.70, 0.9 * (M - 0.70) ** 3, 0) + np.where(M > 0.6, 0.004 * (M - 0.6) ** 2, 0)
    ax.plot(M, cd, color=BLUE, lw=2.4)
    ax.axhline(cd0, color=STEEL, lw=0.8, ls=":")
    ax.text(0.31, cd0 + 0.0003, "incompressible level", fontsize=10, color=STEEL, va="bottom")
    mcrit = 0.78
    ax.axvline(mcrit, color=STEEL, lw=0.8, ls="--")
    ax.text(mcrit - 0.005, 0.0265, "$M_{crit}$: first sonic point", rotation=90, va="top", ha="right", fontsize=10, color=STEEL)
    # Boeing definition: cd exceeds cd0 by 0.002
    mb = M[np.argmax(cd >= cd0 + 0.002)]
    ax.plot([mb], [cd0 + 0.002], "o", color=VERM, ms=7)
    ax.annotate("Boeing: $C_d$ 0.002 above\nthe incompressible level", xy=(mb, cd0 + 0.002), xytext=(0.42, 0.016),
                fontsize=10, color=VERM, arrowprops=dict(arrowstyle="-|>", color=VERM, lw=1))
    # Douglas definition: slope 0.10
    dcd = np.gradient(cd, M)
    md = M[np.argmax(dcd >= 0.10)]
    ax.plot([md], [cd[np.argmax(dcd >= 0.10)]], "s", color=GREEN, ms=7)
    ax.annotate("Douglas: $dC_d/dM = 0.10$", xy=(md, cd[np.argmax(dcd >= 0.10)]), xytext=(0.46, 0.0225),
                fontsize=10, color=GREEN, arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1))
    ax.set_xlabel("Mach number $M$")
    ax.set_ylabel("Section drag coefficient $C_d$")
    ax.set_xlim(0.3, 0.95)
    ax.set_ylim(0.005, 0.03)
    _clean_axes(ax)
    fig.tight_layout()
    save(fig, "drag-divergence")


def wing_height():
    """Front views of a high wing and a low wing with the wing height h."""
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


def _cla(AR, sweep_half_deg=0.0, M=0.0, kappa=1.0):
    beta = np.sqrt(1 - M ** 2)
    t = np.tan(np.radians(sweep_half_deg))
    return 2 * np.pi * AR / (2 + np.sqrt((AR * beta / kappa) ** 2 * (1 + t ** 2 / beta ** 2) + 4))


def aspect_ratio_effects():
    """Lift curve and drag polar of a wing at three aspect ratios, computed
    from the lift-curve-slope equation and the induced-drag term with invented
    section values."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.3))
    styles = [(4, "-", BLUE), (8, "--", VERM), (16, ":", GREEN)]
    a = np.linspace(0, 14, 100)
    cl = np.linspace(0, 1.4, 100)
    e, cd0 = 0.85, 0.02
    for AR, ls, c in styles:
        cla = _cla(AR)
        ax1.plot(a, cla * np.radians(a), ls=ls, color=c, lw=2.2, label=f"AR = {AR}")
        ax2.plot(cd0 + cl ** 2 / (np.pi * e * AR), cl, ls=ls, color=c, lw=2.2, label=f"AR = {AR}")
    ax1.set_xlabel(r"Angle of attack $\alpha$ (deg)")
    ax1.set_ylabel("Wing lift coefficient $C_L$")
    ax1.set_title("Lift curve: slope falls with lower AR", fontsize=11)
    ax1.legend(fontsize=10, frameon=False)
    ax2.set_xlabel("Wing drag coefficient $C_D$")
    ax2.set_ylabel("Wing lift coefficient $C_L$")
    ax2.set_title("Drag polar: induced drag rises with lower AR", fontsize=11)
    ax2.legend(fontsize=10, frameon=False, loc="lower right")
    ax1.set_xlim(0, 14)
    ax1.set_ylim(0, 1.4)
    ax2.set_xlim(0, 0.2)
    ax2.set_ylim(0, 1.4)
    _clean_axes(ax1)
    _clean_axes(ax2)
    fig.tight_layout()
    save(fig, "aspect-ratio-effects")


def taper_lift_distribution():
    """Spanwise lift distribution of straight tapered wings by Schrenk's
    approximation, for three taper ratios, against the elliptical distribution."""
    fig, ax = plt.subplots(figsize=(8, 4.3))
    eta = np.linspace(0, 1, 200)
    ell = np.sqrt(1 - eta ** 2)
    for lam, ls, c in ((1.0, "-", BLUE), (0.5, "--", VERM), (0.3, ":", GREEN)):
        chord = (1 - (1 - lam) * eta) / ((1 + lam) / 2)      # chord / mean chord
        ell_n = 4 / np.pi * ell                               # elliptical, same area
        schrenk = 0.5 * (chord + ell_n)
        ax.plot(eta, schrenk, ls=ls, color=c, lw=2.2, label=f"$\\lambda$ = {lam}")
    ax.plot(eta, 4 / np.pi * ell, color=STEEL, lw=1.2, label="elliptical")
    ax.set_xlabel(r"Spanwise station $2y/b$")
    ax.set_ylabel("Local lift per unit span, normalized")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.6)
    ax.legend(fontsize=10, frameon=False)
    ax.text(0.02, 0.08, "Schrenk's approximation: the mean of the planform chord\nand the elliptical distribution of the same area",
            fontsize=10, color=STEEL)
    _clean_axes(ax)
    fig.tight_layout()
    save(fig, "taper-lift-distribution")


def sweep_components():
    """A swept wing panel and the free-stream velocity resolved along and
    normal to the sweep line."""
    fig, ax = plt.subplots(figsize=(8, 5.2))
    ax.set_aspect("equal")
    ax.axis("off")
    sweep = np.radians(35)
    L = 5.0                                   # leading-edge length of the panel
    tip = np.array([L * np.cos(sweep), -L * np.sin(sweep)])
    cr, ct = 1.7, 0.9
    panel = np.array([[0, 0], tip, tip - [0, ct], [0, -cr]])
    ax.fill(panel[:, 0], panel[:, 1], color=LIGHT, ec=INK, lw=1.5)
    # the sweep line, drawn at mid-chord
    A, B = np.array([0, -cr / 2]), tip - [0, ct / 2]
    ax.plot([A[0], B[0]], [A[1], B[1]], color=AGED, lw=1.4, ls="--")
    ax.text(B[0] + 0.1, B[1], "sweep line", color=AGED, fontsize=11, va="center")
    # unit vectors along the sweep line and normal to it
    s = (B - A) / np.linalg.norm(B - A)
    n = np.array([-s[1], s[0]])               # normal, pointing up and to the right
    P = A + 0.5 * (B - A)                     # point on the sweep line
    V = 1.8
    Vvec = np.array([0.0, -V])                # free stream, flight direction, chordwise
    tail = P - Vvec
    ax.annotate("", xy=P, xytext=tail, arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.2, shrinkA=0, shrinkB=0))
    ax.text(tail[0] + 0.12, tail[1] - 0.1, r"$V_\infty$", fontsize=13, va="top")
    vn = (Vvec @ n) * n                       # component normal to the sweep line
    vs = (Vvec @ s) * s                       # component along the sweep line
    ax.annotate("", xy=tail + vn, xytext=tail, arrowprops=dict(arrowstyle="-|>", color=VERM, lw=2, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=tail + vn + vs, xytext=tail + vn, arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2, shrinkA=0, shrinkB=0))
    mid_n = tail + 0.5 * vn
    ax.text(mid_n[0] - 0.3, mid_n[1] + 0.45, r"$V_\infty\cos\Lambda$, sets the pressures", color=VERM, fontsize=11,
            ha="right", va="bottom")
    mid_s = tail + vn + 0.5 * vs
    ax.text(mid_s[0] - 0.15, mid_s[1] - 0.15, r"$V_\infty\sin\Lambda$", color=GREEN, fontsize=11, ha="right", va="top")
    # the sweep angle, measured at the sweep line itself
    sw_line = np.arctan2(-s[1], s[0])
    ax.plot([A[0], A[0] + 1.8], [A[1], A[1]], color=INK, lw=0.8, ls=":")
    ang = np.linspace(0, -sw_line, 20)
    ax.plot(A[0] + 1.3 * np.cos(ang), A[1] + 1.3 * np.sin(ang), color=INK, lw=0.9)
    ax.text(A[0] + 1.42, A[1] - 0.3, r"$\Lambda$", fontsize=13, color=INK)
    ax.set_xlim(-2.4, 6.0)
    ax.set_ylim(-4.2, 2.2)
    save(fig, "sweep-components")


def korn_sweep():
    """Drag-divergence Mach number of a wing from the Korn relation against
    sweep, for three thickness ratios, at an example lift coefficient."""
    fig, ax = plt.subplots(figsize=(8, 4.3))
    lam = np.radians(np.linspace(0, 45, 200))
    CL = 0.3
    for tc, ls, c in ((0.08, "-", BLUE), (0.10, "--", VERM), (0.12, ":", GREEN)):
        mdd = 0.87 / np.cos(lam) - tc / np.cos(lam) ** 2 - CL / (10 * np.cos(lam) ** 3)
        mdd = np.where(mdd <= 1.0, mdd, np.nan)
        ax.plot(np.degrees(lam), mdd, ls=ls, color=c, lw=2.2, label=f"$t/c$ = {tc:.2f}, conventional")
    mdd_sc = 0.95 / np.cos(lam) - 0.10 / np.cos(lam) ** 2 - CL / (10 * np.cos(lam) ** 3)
    mdd_sc = np.where(mdd_sc <= 1.0, mdd_sc, np.nan)
    ax.plot(np.degrees(lam), mdd_sc, color=AGED, lw=2.2, label="$t/c$ = 0.10, supercritical")
    ax.set_xlabel(r"Sweep of the mid-chord line $\Lambda$ (deg)")
    ax.set_ylabel("$M_{DD}$")
    ax.set_xlim(0, 45)
    ax.set_ylim(0.6, 1.0)
    ax.legend(fontsize=10, frameon=False, loc="upper left")
    ax.text(44, 0.62, "Korn relation at $C_L$ = 0.3; $\\kappa$ = 0.87 conventional, 0.95 supercritical",
            fontsize=10, color=STEEL, ha="right")
    _clean_axes(ax)
    fig.tight_layout()
    save(fig, "korn-sweep")


def pitch_up_boundary():
    """The pitch-up boundary of swept wings: the limiting aspect ratio against
    quarter-chord sweep for three taper ratios, from the equation on the slide."""
    fig, ax = plt.subplots(figsize=(8, 4.3))
    sw = np.linspace(0, 60, 200)
    for lam, ls, c in ((1.0, "-", BLUE), (0.5, "--", VERM), (0.3, ":", GREEN)):
        ax.plot(sw, 17.714 * (2 - lam) * np.exp(-0.04267 * sw), ls=ls, color=c, lw=2.2, label=f"$\\lambda$ = {lam}")
    ax.text(5, 2.0, "Region I: nose drops at stall", fontsize=11, color=STEEL)
    ax.text(32, 12.5, "Region II: nose rises at stall", fontsize=11, color=STEEL)
    ax.set_xlabel(r"Quarter-chord sweep $\Lambda_{c/4}$ (deg)")
    ax.set_ylabel("Limiting aspect ratio $AR_{lim}$")
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 32)
    ax.legend(fontsize=10, frameon=False)
    _clean_axes(ax)
    fig.tight_layout()
    save(fig, "pitch-up-boundary")


def wing_incidence():
    """Side view: the fuselage reference line, the wing chord at the incidence
    angle, and the free stream at the angle of attack."""
    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.set_aspect("equal")
    ax.axis("off")
    # fuselage as a rounded bar
    ax.add_patch(FancyBboxPatch((-3.2, -0.45), 6.4, 0.9, boxstyle="round,pad=0,rounding_size=0.45",
                                fc=LIGHT, ec=INK, lw=1.4))
    ax.plot([-3.8, 3.8], [0, 0], color=STEEL, lw=0.9, ls="--")
    ax.text(3.85, 0, "fuselage reference line", fontsize=11, color=STEEL, va="center")
    iw = np.radians(3)
    c = 2.2
    x0 = -0.4
    ax.plot([x0 - c / 2 * np.cos(iw), x0 + c / 2 * np.cos(iw)], [0.0 + c / 2 * np.sin(iw), 0.0 - c / 2 * np.sin(iw)],
            color=AGED, lw=3.5)
    ax.text(x0 + 0.1, 0.55, "wing chord line", color=AGED, fontsize=11)
    ax.text(x0 + c / 2 + 0.15, -0.12, "$i_W$", color=AGED, fontsize=12, va="top")
    # free stream
    al = np.radians(5)
    ax.annotate("", xy=(-3.5, 0.75), xytext=(-5.3, 0.75 + 1.8 * np.tan(al)),
                arrowprops=dict(arrowstyle="-|>", color=VERM, lw=2))
    ax.plot([-5.3, -3.5], [0.75 + 1.8 * np.tan(al)] * 2, color=STEEL, lw=0.8, ls=":")
    ax.text(-5.3, 1.05, r"$V_\infty$ at angle of attack $\alpha$", color=VERM, fontsize=11)
    ax.set_xlim(-5.6, 6.6)
    ax.set_ylim(-1.0, 1.7)
    save(fig, "wing-incidence")


def lift_curve_slope():
    """Wing lift-curve slope against aspect ratio for three mid-chord sweeps,
    computed from the equation on the slide at M = 0 and kappa = 1."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    AR = np.linspace(0.5, 16, 200)
    ax.axhline(2 * np.pi, color=STEEL, lw=0.9)
    ax.text(15.8, 2 * np.pi + 0.08, "section, $2\\pi$", ha="right", va="bottom", fontsize=11, color=STEEL)
    for sw, ls, c in ((0, "-", INK), (30, "--", AGED), (45, ":", STEEL)):
        ax.plot(AR, _cla(AR, sw), ls=ls, color=c, lw=2.2, label=f"$\\Lambda_{{c/2}}$ = {sw}°")
    ax.set_xlabel("Aspect ratio")
    ax.set_ylabel(r"$C_{L_\alpha}$, per rad")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 7)
    ax.set_xticks([0, 4, 8, 12, 16])
    ax.legend(fontsize=10, frameon=False, loc="lower right")
    _clean_axes(ax)
    fig.tight_layout()
    save(fig, "lift-curve-slope")


def stall_speed():
    """Stall speed against wing loading at sea level for four values of the
    maximum lift coefficient, from the stall-speed equation."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ws = np.linspace(5, 120, 300)
    rho = 0.002377
    for clmax, ls, c in ((1.2, "-", BLUE), (1.6, "--", VERM), (2.0, "-.", GREEN), (2.4, ":", AGED)):
        vs = np.sqrt(2 * ws / (rho * clmax)) / 1.6878
        ax.plot(ws, vs, ls=ls, color=c, lw=2.2, label=f"$C_{{L_{{max}}}}$ = {clmax}")
    ax.set_xlabel("Wing loading $W/S$ (lb/ft²)")
    ax.set_ylabel("Stall speed $V_S$ (KEAS)")
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 200)
    ax.legend(fontsize=10, frameon=False, loc="upper left")
    ax.text(118, 8, "sea level, standard day", fontsize=10, color=STEEL, ha="right")
    _clean_axes(ax)
    fig.tight_layout()
    save(fig, "stall-speed")


if __name__ == "__main__":
    design_phases()
    design_process_flow()
    design_funnel()
    narrowbody_production()
    system_levels()
    combat_mission_profile()
    navy_training_mission()
    navy_ferry_mission()
    design_mission_profile()
    empty_weight_trends()
    trend_honesty()
    pugh_controlled_convergence()
    pugh_matrix_runs()
    training_flight_profile()
    for fn in (wing_planform, naca_families, section_data_schematic, stall_classes, drag_divergence,
               wing_height, aspect_ratio_effects, taper_lift_distribution, sweep_components, korn_sweep,
               pitch_up_boundary, wing_incidence, lift_curve_slope, stall_speed):
        fn()
