"""The three illustrative figures of the A05 brief that apply to the Navy Jet
Trainer, redrawn as SVG from the brief's own script (Assignments/A05/scripts/
make_a05_figures.py). Invented data: invented engines, normalized axes. Each
figure asserts its point before it is written.

Run from the book folder:  python3 scripts/make_a05_figures.py
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / "notes" / "assignments" / "figures"
BLACK, ORANGE, SKY, GREEN, BLUE, VERM = "#000000", "#E69F00", "#56B4E9", "#009E73", "#0072B2", "#D55E00"
STYLES = ["-", "--", "-.", ":"]
GRID = dict(color="#dddddd", lw=0.6)
plt.rcParams.update({"svg.fonttype": "none", "font.family": "sans-serif",
                     "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
                     "font.size": 12, "savefig.facecolor": "white"})


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)
    print("wrote", name)


def tsfc_curve(x, xmax, cmin, bucket=0.8, k=0.55):
    """Normalized TSFC bucket: minimum cmin at bucket*xmax, rising at low thrust."""
    xb = bucket * xmax
    return cmin * (1 + k * (xb / x - 1) ** 2 + 0.25 * np.clip(x / xb - 1, 0, None) ** 2)


def candidate_trade():
    x = np.linspace(0.12, 1.0, 300)
    yA = tsfc_curve(x, 1.00, 0.92)
    yB = tsfc_curve(x, 0.62, 1.00)
    mB = x <= 0.62
    band1, band2 = (0.30, 0.42), (0.70, 0.80)
    in1 = (x >= band1[0]) & (x <= band1[1])
    assert np.all(yB[in1] < yA[in1]) and band2[0] > 0.62 and abs(yB[mB].min() - 1.0) < 0.01
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.axvspan(*band1, color="#e6e6e6")
    ax.axvspan(*band2, color="#e6e6e6")
    ax.text(np.mean(band1), 1.72, "condition 1", ha="center")
    ax.text(np.mean(band2), 1.72, "condition 2", ha="center")
    ax.plot(x, yA, color=BLUE, ls="-", lw=2.2, label="Candidate A")
    ax.plot(x[mB], yB[mB], color=ORANGE, ls="--", lw=2.2, label="Candidate B")
    ax.plot([0.62], [yB[mB][-1]], "|", color=ORANGE, ms=14, mew=2.5)
    ax.plot([1.0], [yA[-1]], "|", color=BLUE, ms=14, mew=2.5)
    ax.set_xlabel("Thrust / sea-level static thrust of candidate A")
    ax.set_ylabel("TSFC / minimum TSFC of candidate B")
    ax.set_ylim(0.85, 1.8)
    ax.set_xlim(0.1, 1.02)
    ax.grid(**GRID)
    ax.legend(loc="upper center", frameon=False)
    fig.tight_layout()
    save(fig, "a05-candidate-trade")


def deck_segments():
    alts = [("Sea level", 1.00, 1.12), ("Low altitude", 0.70, 1.06),
            ("Mid altitude", 0.45, 1.02), ("Cruise altitude", 0.32, 1.00)]
    colors = [ORANGE, SKY, GREEN, BLUE]
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    curves = {}
    for (name, xmax, cmin), c, ls in zip(alts, colors, STYLES):
        xx = np.linspace(0.18 * xmax, xmax, 200)
        curves[name] = (xmax, cmin)
        ax.plot(xx, tsfc_curve(xx, xmax, cmin), color=c, ls=ls, lw=2.2, label=name)
        ax.plot([xmax], [tsfc_curve(xmax, xmax, cmin)], "|", color=c, ms=14, mew=2.5)
    for label, alt, xr, m, off in [("Cruise", "Cruise altitude", 0.24, "o", (-10, -20)),
                                   ("Reserve", "Cruise altitude", 0.14, "s", (-62, 6)),
                                   ("Approach", "Sea level", 0.45, "^", (10, 6))]:
        xmax, cmin = curves[alt]
        ax.plot(xr, tsfc_curve(xr, xmax, cmin), m, color=VERM, ms=9, mec=BLACK, zorder=5)
        ax.annotate(label, (xr, tsfc_curve(xr, xmax, cmin)), textcoords="offset points", xytext=off)
    xmax, cmin = curves["Mid altitude"]
    ax.plot(xmax, tsfc_curve(xmax, xmax, cmin), "D", color=VERM, ms=9, mec=BLACK, zorder=5)
    ax.annotate("Segment at a\nnamed rating", (xmax, tsfc_curve(xmax, xmax, cmin)),
                textcoords="offset points", xytext=(8, 10))
    xmax, cmin = curves["Sea level"]
    xq = 0.78
    yq = tsfc_curve(xq, xmax, cmin)
    ax.plot(xq, yq, "*", color=VERM, ms=13, mec=BLACK, zorder=5)
    ax.annotate("Performance\nrequirement", (xq, yq), textcoords="offset points", xytext=(-62, 16))
    ax.annotate("", xy=(xmax, yq - 0.07), xytext=(xq, yq - 0.07),
                arrowprops=dict(arrowstyle="<->", color=BLACK, lw=1.4))
    ax.text((xq + xmax) / 2, yq - 0.10, "margin", ha="center", va="top", fontsize=11)
    assert xq < xmax
    ax.set_xlabel("Installed thrust / sea-level static thrust")
    ax.set_ylabel("TSFC / minimum TSFC")
    ax.set_ylim(0.75, 2.0)
    ax.set_xlim(0, 1.05)
    ax.grid(**GRID)
    ax.legend(loc="upper right", frameon=False)
    fig.tight_layout()
    save(fig, "a05-deck-segments")


def model_check():
    def lapse(M, sigma, a):
        return sigma * (1 - a * M ** 1.5)

    rng = np.random.default_rng(7)
    M = np.linspace(0, 0.9, 200)
    Mp = np.array([0.0, 0.15, 0.3, 0.45, 0.6])
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.axvspan(0.6, 0.92, color="#eeeeee")
    ax.text(0.76, 1.02, "beyond the published points:\nstate the relations used", ha="center", va="top")
    for (name, sig, a), c, ls, mk in zip(
            [("Sea level", 1.00, 0.28), ("Mid altitude", 0.62, 0.22), ("Cruise altitude", 0.38, 0.18)],
            [ORANGE, GREEN, BLUE], STYLES, ["o", "s", "^"]):
        ax.plot(M, lapse(M, sig, a), color=c, ls=ls, lw=2.0, label=f"Relation, {name.lower()}")
        pub = lapse(Mp, sig, a) * (1 + rng.normal(0, 0.02, Mp.size))
        assert np.abs(pub / lapse(Mp, sig, a) - 1).max() < 0.06
        ax.plot(Mp, pub, mk, color=c, mec=BLACK, ms=7, ls="none")
    ax.plot([], [], "o", color="white", mec=BLACK, label="Published points")
    ax.set_xlabel("Mach number")
    ax.set_ylabel("Thrust / sea-level static thrust")
    ax.set_xlim(0, 0.92)
    ax.set_ylim(0, 1.05)
    ax.grid(**GRID)
    ax.legend(loc="lower left", frameon=False, fontsize=10.5)
    fig.tight_layout()
    save(fig, "a05-model-check")


if __name__ == "__main__":
    candidate_trade()
    deck_segments()
    model_check()
