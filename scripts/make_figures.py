"""Figures for the AAE 490/590 lecture notes book.

Run from the book folder:  python3 scripts/make_figures.py
Writes SVG files to the figures folder of each chapter (notes/<chapter>/figures/). Text stays as text in the SVG
(svg.fonttype = none) so it scales and can be selected.

Every diagram is redrawn for the book. Sources are named in the captions
in the Markdown files; the data in the bar chart are the values printed on
the lecture slide.
"""
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon

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
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "font.size": 13,
    "axes.edgecolor": "#000000",
    "axes.labelcolor": "#000000",
    "xtick.color": "#000000",
    "ytick.color": "#000000",
    "savefig.facecolor": "white",
})

# Purdue palette. Text is always black or white on these fills.
GOLD = "#CFB991"      # Boilermaker gold
DUST = "#EBD99F"
LIGHT = "#F5EFDC"
AGED = "#8E6F3E"      # aged gold, lines
STEEL = "#555960"
GRAY = "#D9D9D9"
BLUE = "#0072B2"      # Okabe-Ito blue
INK = "#000000"


def save(fig, name):
    out = NOTES / FOLDER.get(name, DEFAULT_FOLDER) / "figures"
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{name}.svg", bbox_inches="tight", pad_inches=0.15)
    if PREVIEW:
        fig.savefig(Path(PREVIEW) / f"{name}.png", dpi=80, bbox_inches="tight",
                    pad_inches=0.15)
    plt.close(fig)
    print("wrote", name)


def canvas(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text, fill=LIGHT, size=12, bold=False, edge=AGED):
    """Box centered at (x, y)."""
    p = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                       boxstyle="round,pad=0.25,rounding_size=0.8",
                       fc=fill, ec=edge, lw=1.6)
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", fontsize=size,
            fontweight="bold" if bold else "normal", color=INK,
            linespacing=1.25)


def diamond(ax, x, y, w, h, text, size=12):
    ax.add_patch(Polygon([(x - w / 2, y), (x, y + h / 2), (x + w / 2, y),
                          (x, y - h / 2)], closed=True, fc=GOLD, ec=AGED,
                         lw=1.6))
    ax.text(x, y, text, ha="center", va="center", fontsize=size,
            fontweight="bold", color=INK)


def arrow(ax, p, q, style="-|>", ls="-", color=INK, rad=0.0, lw=1.6):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=16,
                                 lw=lw, ls=ls, color=color,
                                 connectionstyle=f"arc3,rad={rad}",
                                 shrinkA=0, shrinkB=0))


# ---------------------------------------------------------------------------
def design_phases():
    """Phases 0 to 5 of an aircraft program, after Venson."""
    fig, ax = canvas(11, 2.6, 113, 26)
    names = ["Feasibility\nstudy", "Conceptual\ndesign", "Preliminary\ndesign",
             "Detail\ndesign", "Entry into\nservice and\nproduction",
             "Operation\nand\nphase-out"]
    w, tip, y0, y1 = 17.0, 4.0, 3.0, 23.0
    for i, name in enumerate(names):
        x = 1 + i * (w + 1.0)
        pts = [(x, y0), (x + w, y0), (x + w + tip, (y0 + y1) / 2), (x + w, y1),
               (x, y1)]
        if i > 0:
            pts.append((x + tip, (y0 + y1) / 2))
        ax.add_patch(Polygon(pts, closed=True, fc=GRAY if i == 0 else DUST,
                             ec=AGED, lw=1.6))
        cx = x + w / 2 + (tip / 2 if i > 0 else 0)
        ax.text(cx, 16.5, name, ha="center", va="center", fontsize=12.5,
                linespacing=1.15)
        ax.text(cx, 6.3, f"Phase {i}", ha="center", va="center",
                fontsize=12.5, fontweight="bold")
    save(fig, "design-phases")


# ---------------------------------------------------------------------------
def design_process_flow():
    """Conceptual design flow, simplified after Nicolai and Carichner."""
    fig, ax = canvas(11, 9.6, 100, 88)
    W, H = 19, 8.5
    xs = [12, 37, 62, 87]
    r1, r2, r3, r4, r5 = 72, 56, 40, 24, 8

    # Row 1, left to right
    box(ax, xs[0], r1, W, H, "Customer", fill=GOLD, bold=True)
    box(ax, xs[1], r1, W, H, "Mission\nrequirements")
    box(ax, xs[2], r1, W, H, "Concept of\noperations")
    box(ax, xs[3], r1, W, H + 1.5, "Design guidelines\nradius, payload,\naltitude, signature",
        size=11.5)
    for a, b in zip(xs[:-1], xs[1:]):
        arrow(ax, (a + W / 2 + 0.4, r1), (b - W / 2 - 0.4, r1))
    # inputs to the design guidelines
    box(ax, 76, 85, 36, 6.5,
        "Inputs: system approach, technology,\nmeasures of merit, selection criteria",
        fill="white", size=11)
    arrow(ax, (87, 81.4), (87, r1 + (H + 1.5) / 2 + 0.4))
    box(ax, 37, 85, 30, 6.5, "Evaluate and negotiate\nrequirements with the customer",
        fill="white", size=11)
    arrow(ax, (37, 81.4), (37, r1 + H / 2 + 0.4))

    # Row 2, right to left
    box(ax, xs[3], r2, W, H, "Configuration\nsketches")
    box(ax, xs[2], r2, W, H, "Concepts\n1 to n")
    box(ax, xs[1], r2, W, H, "Initial\nsizing")
    box(ax, xs[0], r2, W, H, "Select\nconfiguration")
    arrow(ax, (87, r1 - (H + 1.5) / 2 - 0.4), (87, r2 + H / 2 + 0.4))
    for a, b in zip(xs[::-1][:-1], xs[::-1][1:]):
        arrow(ax, (a - W / 2 - 0.4, r2), (b + W / 2 + 0.4, r2))

    # Row 3, left to right
    box(ax, xs[0], r3, W, H + 2, "Functional inputs\naero, propulsion,\nweights, structure",
        size=11.5)
    box(ax, xs[1], r3, W, H + 2, "Design trades\nW/S, T/W,\nAR, sweep", size=11.5)
    box(ax, xs[2], r3, W, H, "Select preferred\nconfiguration")
    box(ax, xs[3], r3, W, H, "Baseline\ndesign", fill=GOLD, bold=True)
    arrow(ax, (12, r2 - H / 2 - 0.4), (12, r3 + (H + 2) / 2 + 0.4))
    for a, b in zip(xs[:-1], xs[1:]):
        arrow(ax, (a + W / 2 + 0.4, r3), (b - W / 2 - 0.4, r3))

    # Row 4, right to left
    box(ax, xs[3], r4, W, H + 2, "Mission trades\nradius, payload,\nspeed, time", size=11.5)
    box(ax, xs[2], r4, W, H + 2, "Technology trades\nTSFC, engine T/W,\nempty weight, L/D",
        size=11.5)
    diamond(ax, xs[1], r4, 17, 11, "Satisfied?")
    box(ax, xs[0], r4, W, H + 2, "Share trade\nresults with\nthe customer")
    arrow(ax, (87, r3 - H / 2 - 0.4), (87, r4 + (H + 2) / 2 + 0.4))
    arrow(ax, (xs[3] - W / 2 - 0.4, r4), (xs[2] + W / 2 + 0.4, r4))
    arrow(ax, (xs[2] - W / 2 - 0.4, r4), (xs[1] + 8.5 + 0.2, r4))
    arrow(ax, (xs[1] - 8.5 - 0.2, r4), (xs[0] + W / 2 + 0.4, r4))
    ax.text(26.5, r4 + 1.6, "Yes", fontsize=11.5, ha="center", fontweight="bold")
    # No branch: iterate from initial sizing through connector A
    def connector(x, y):
        ax.add_patch(matplotlib.patches.Circle((x, y), 1.7, fc="white", ec=AGED,
                                               lw=1.6))
        ax.text(x, y, "A", ha="center", va="center", fontsize=11.5,
                fontweight="bold")
    connector(37, 32.4)
    arrow(ax, (37, r4 + 5.5 + 0.2), (37, 30.6))
    ax.text(35.6, 30.2, "No", fontsize=11.5, ha="right", va="center",
            fontweight="bold")
    connector(31, 48.6)
    arrow(ax, (31, 50.4), (31, r2 - H / 2 - 0.4))
    # risk assessment
    box(ax, 62, 32.3, 17, 3.6, "Risk assessment", fill="white", size=11)
    arrow(ax, (53.2, 31.4), (41.4, 26.6))

    # Row 5, left to right
    diamond(ax, xs[0], r5, 19, 11, "Requirements\nchange?", size=11)
    box(ax, 52, r5, 34, H + 3,
        "Point design\nOML, arrangement, performance,\nsubsystems, risk, cost, TRL 3 to 4",
        size=11)
    arrow(ax, (12, r4 - (H + 2) / 2 - 0.4), (12, r5 + 5.5 + 0.2))
    arrow(ax, (xs[0] + 9.5 + 0.2, r5), (52 - 17 - 0.6, r5))
    ax.text(25, r5 + 1.6, "No", fontsize=11.5, fontweight="bold")
    box(ax, 87, r5, W, H, "Preliminary\ndesign", fill=GOLD, bold=True)
    arrow(ax, (69.6, r5), (87 - W / 2 - 0.4, r5))
    # Yes branch: back to design guidelines
    arrow(ax, (12, r5 - 5.5 - 0.2), (12, -3.2))
    ax.text(12, -5.6, "Yes: return to design guidelines", fontsize=11, ha="left",
            va="center", bbox=dict(fc="white", ec="none", pad=0.5))
    ax.set_ylim(-8, 89)
    save(fig, "design-process-flow")


# ---------------------------------------------------------------------------
def design_funnel():
    """Conceptual, preliminary and detail design, after Raymer."""
    fig, ax = canvas(9.5, 8.2, 100, 86)
    stages = [
        ("Conceptual design",
         "What requirements drive the design?\nWhat should it look like? Weight? Cost?\n"
         "What trade-offs should be considered?\nWhat technologies should be used?\n"
         "Do these requirements give a viable and salable aircraft?"),
        ("Preliminary design",
         "Freeze the configuration\nDevelop lofting (surface definition)\n"
         "Develop the test and analytical database\nDesign major items\n"
         "Develop the cost estimate"),
        ("Detail design",
         "Design the actual pieces to be built\nDesign tooling and fabrication process\n"
         "Test major items: structure, landing gear\n"
         "Finalize weight and performance estimates"),
    ]
    tops = [74, 49, 24]
    hgt = 23
    for (title, body), top in zip(stages, tops):
        ax.add_patch(Polygon([(6, top), (94, top), (84, top - hgt), (16, top - hgt)],
                             closed=True, fc=DUST, ec=AGED, lw=1.6))
        ax.text(50, top - 3.2, title, ha="center", va="center", fontsize=13.5,
                fontweight="bold")
        ax.text(50, top - 13.3, body, ha="center", va="center", fontsize=11.5,
                linespacing=1.3)
    ax.text(50, 81.5, "Requirements", ha="center", va="center", fontsize=13,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.45", fc=GOLD, ec=AGED, lw=1.6))
    arrow(ax, (50, 78.6), (50, 74.4))
    ax.text(50, -5.5, "Fabrication", ha="center", va="center", fontsize=13,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.45", fc=GOLD, ec=AGED, lw=1.6))
    arrow(ax, (50, 0.8), (50, -2.6))
    ax.set_ylim(-9, 86)
    save(fig, "design-funnel")


# ---------------------------------------------------------------------------
def narrowbody_production():
    """Narrow-body production counts, values as printed on the lecture slide."""
    data = [
        ("Airbus A318/A319/A320/A321", 16000),
        ("Boeing 737 family", 10500),
        ("Bombardier CRJ family", 1945),
        ("Embraer E-Jets (first generation)", 1500),
        ("McDonnell Douglas MD-80/90", 1191),
        ("COMAC C919", 305),
        ("Fokker 100", 283),
        ("Bombardier CSeries (A220)", 220),
        ("Sukhoi Superjet 100", 200),
        ("Embraer E-Jets E2 (second generation)", 200),
        ("Fokker 70", 47),
        ("Mitsubishi SpaceJet", 0),
    ]
    names = [d[0] for d in data][::-1]
    vals = [d[1] for d in data][::-1]
    fig, ax = plt.subplots(figsize=(9.5, 6.2))
    bars = ax.barh(names, vals, color=BLUE, edgecolor=INK, lw=0.6)
    for b, v in zip(bars, vals):
        ax.text(b.get_width() + 150, b.get_y() + b.get_height() / 2, f"{v:,}",
                va="center", fontsize=12)
    ax.set_xlabel("Number of aircraft produced")
    ax.set_xlim(0, 18500)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
        lambda x, _: f"{int(x):,}"))
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#BBBBBB", lw=0.6)
    ax.set_axisbelow(True)
    assert vals[-1] == max(vals) and vals[0] == 0
    save(fig, "narrowbody-production")


# ---------------------------------------------------------------------------
def system_levels():
    """Five levels of an aircraft system, after Sadraey."""
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
         "Fittings, fasteners, blades, screws, nuts, ribs, spars,\n"
         "frames, stiffeners, skin, shafts, pipes, propellers"),
    ]
    fig, ax = canvas(10.5, 6.4, 100, 62)
    fills = [GOLD, DUST, LIGHT, LIGHT, "white"]
    for i, ((lv, name, ex), fc) in enumerate(zip(levels, fills)):
        y = 54 - i * 12
        indent = i * 2.5
        ax.add_patch(FancyBboxPatch((1 + indent, y - 4.8), 27 - indent, 9.6,
                                    boxstyle="round,pad=0.2,rounding_size=0.8",
                                    fc=fc, ec=AGED, lw=1.6))
        ax.text(14.5 + indent / 2, y + 1.9, lv, ha="center", va="center",
                fontsize=12.5, fontweight="bold")
        ax.text(14.5 + indent / 2, y - 2.0, name, ha="center", va="center",
                fontsize=12.5)
        ax.text(32, y, ex, ha="left", va="center", fontsize=12, linespacing=1.3)
        if i < 4:
            arrow(ax, (6 + indent, y - 5.0), (6 + indent, y - 7.1), lw=1.4)
    save(fig, "system-levels")


# ---------------------------------------------------------------------------
def goaero_conops():
    """Purdue GoAERO team CONOPS diagram, redrawn with readable contrast."""
    fig, ax = canvas(11, 7.4, 110, 74)
    box(ax, 55, 34, 18, 12, "Operating\nzone", fill=GOLD, size=13.5, bold=True)
    nodes = {
        "vehicle": (55, 64, "Competition vehicle",
                    "Semi-autonomous aircraft that carries\none passenger or a medium payload"),
        "gps": (10, 64, "GPS", "Accurate\npositioning data"),
        "areas": (95, 46, "Areas of operation",
                  "Fly to and from objects of interest\nwith autonomous recognition,\n"
                  "adapting to diverse conditions"),
        "obst": (14, 30, "Obstacles",
                 "The vehicle navigates complex\nobstacle environments using\n"
                 "onboard sensors"),
        "trans": (52, 8, "Transportation",
                  "Ground transport brings the vehicle\nand the ground station to the\n"
                  "area of operation"),
        "ground": (95, 14, "Ground station",
                   "Command and control center\nfor the operator to fly\nthe vehicle"),
    }
    for key, (x, y, title, body) in nodes.items():
        ax.text(x, y + 3.2, title, ha="center", va="bottom", fontsize=13,
                fontweight="bold")
        ax.text(x, y + 2.6, body, ha="center", va="top", fontsize=11.5,
                linespacing=1.25)
    # flight paths (solid)
    arrow(ax, (58, 40.5), (58, 56.0), lw=2.2)                  # zone -> vehicle
    arrow(ax, (72, 62.5), (84, 52.5), lw=2.2, rad=-0.15)       # vehicle -> areas
    arrow(ax, (82, 36.5), (64.6, 34), lw=2.2, rad=-0.15)       # areas -> zone
    arrow(ax, (45.4, 33), (29, 30), lw=2.2, rad=0.1)           # zone -> obstacles
    arrow(ax, (14, 23.0), (45.4, 30), lw=2.2, rad=0.25)        # obstacles -> zone
    arrow(ax, (52, 14.2), (52, 27.6), lw=2.2)                  # transport -> zone
    # data links (dashed)
    arrow(ax, (19, 68.2), (40, 68.2), ls="--", color=BLUE, lw=2.0, style="-")
    arrow(ax, (88, 20.5), (66, 56.5), ls="--", color=BLUE, lw=2.0, style="-",
          rad=0.1)
    ax.text(29.5, 69.2, "data link", ha="center", fontsize=11, color=INK)
    ax.text(76.5, 27.5, "data link", ha="center", fontsize=11, color=INK)
    save(fig, "goaero-conops")


# ---------------------------------------------------------------------------
def combat_mission_profile():
    """Generic combat mission profile with eight phases, after Raymer."""
    fig, ax = plt.subplots(figsize=(10, 5.4))
    x = [0, 3, 18, 40, 42, 47, 52, 66, 86, 87, 87.5, 95, 96]
    y = [0, 2, 70, 73, 60, 60, 37, 80, 82, 25, 25, 0, 0]
    ax.fill_between(x, y, color=LIGHT)
    ax.plot(x, y, color=INK, lw=2.2)
    labels = [(9, 18, "1"), (12, 42, "2"), (29, 77, "3"), (43, 66, "4"),
              (49.5, 46, "5"), (76, 86, "6"), (91, 31, "7"), (93, 8, "8")]
    for lx, ly, t in labels:
        ax.text(lx, ly, t, ha="center", va="center", fontsize=13,
                fontweight="bold",
                bbox=dict(boxstyle="circle,pad=0.25", fc="white", ec=AGED))
    ax.set_xlabel("Distance (not to scale)")
    ax.set_ylabel("Altitude (not to scale)")
    ax.set_xticks([0, 96], ["origin", "origin"])
    ax.set_yticks([])
    ax.set_xlim(-1, 100)
    ax.set_ylim(0, 95)
    ax.spines[["top", "right"]].set_visible(False)
    save(fig, "combat-mission-profile")


# ---------------------------------------------------------------------------
def navy_training_mission():
    """Training flight from the Navy Jet Trainer RFP (schematic, distance not to scale)."""
    fig, ax = plt.subplots(figsize=(10, 4.6))
    x = [0, 4, 7, 21, 37, 41, 53, 57, 71, 85, 89]
    y = [0, 0, 0, 20000, 20000, 10000, 10000, 20000, 20000, 0, 0]
    ax.plot(x, y, color=INK, lw=2.2)
    seg = [(2, 0, "1"), (5.5, 0, "2"), (14, 10000, "3"), (29, 20000, "4"),
           (39, 15000, "5"), (47, 10000, "6"), (55, 15000, "7"), (64, 20000, "8"),
           (78, 10000, "9"), (87, 0, "10")]
    for sx, sy, t in seg:
        ax.text(sx, sy, t, ha="center", va="center", fontsize=12, fontweight="bold",
                bbox=dict(boxstyle="circle,pad=0.25", fc="white", ec=AGED))
    for xa, xb in ((7, 41), (53, 85)):
        ax.annotate("", xy=(xb, -4200), xytext=(xa, -4200),
                    arrowprops=dict(arrowstyle="<|-|>", color=BLUE, lw=1.6))
        ax.text((xa + xb) / 2, -4200, "50 nm", ha="center", va="center",
                fontsize=12, bbox=dict(fc="white", ec="none", pad=1.5))
    ax.set_yticks([0, 10000, 20000], ["0 ft", "10,000 ft", "20,000 ft"])
    ax.set_xticks([])
    ax.set_xlabel("Distance (not to scale)")
    ax.set_ylabel("Altitude")
    ax.set_ylim(-6500, 23500)
    ax.set_xlim(-1, 91)
    ax.grid(axis="y", color="#BBBBBB", lw=0.6)
    ax.spines[["top", "right"]].set_visible(False)
    save(fig, "navy-training-mission")


def navy_ferry_mission():
    """Ferry flight from the Navy Jet Trainer RFP (schematic)."""
    fig, ax = plt.subplots(figsize=(10, 4.2))
    x = [0, 4, 7, 22, 72, 87, 91]
    y = [0, 0, 0, 1, 1, 0, 0]
    ax.plot(x, y, color=INK, lw=2.2)
    seg = [(2, 0, "1"), (5.5, 0, "2"), (14.5, 0.5, "3"), (47, 1, "4"),
           (79.5, 0.5, "5"), (89, 0, "6")]
    for sx, sy, t in seg:
        ax.text(sx, sy, t, ha="center", va="center", fontsize=12, fontweight="bold",
                bbox=dict(boxstyle="circle,pad=0.25", fc="white", ec=AGED))
    ax.annotate("", xy=(87, -0.22), xytext=(7, -0.22),
                arrowprops=dict(arrowstyle="<|-|>", color=BLUE, lw=1.6))
    ax.text(47, -0.22, "600 nm, segments 3 to 5", ha="center", va="center",
            fontsize=12, bbox=dict(fc="white", ec="none", pad=1.5))
    ax.set_yticks([0, 1], ["0 ft", "Cruise altitude\n(team choice)"])
    ax.set_xticks([])
    ax.set_xlabel("Distance (not to scale)")
    ax.set_ylabel("Altitude")
    ax.set_ylim(-0.38, 1.18)
    ax.set_xlim(-1, 93)
    ax.spines[["top", "right"]].set_visible(False)
    save(fig, "navy-ferry-mission")


if __name__ == "__main__":
    design_phases()
    design_process_flow()
    design_funnel()
    narrowbody_production()
    system_levels()
    goaero_conops()
    combat_mission_profile()
    navy_training_mission()
    navy_ferry_mission()
