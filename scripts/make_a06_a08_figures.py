"""The illustrative figures of the Navy Jet Trainer briefs A06, A07 and A08, redrawn
as SVG from the briefs' own scripts (Assignments/A0N/scripts/make_a0N_figures.py).
Invented data on invented scales, generic labels. Each figure asserts its point
before it is written, as the brief scripts do.

Run from the book folder:  python3 scripts/make_a06_a08_figures.py
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / "notes" / "assignments" / "figures"
BLACK, ORANGE, SKY, GREEN, BLUE, VERM, PURPLE = (
    "#000000", "#E69F00", "#56B4E9", "#009E73", "#0072B2", "#D55E00", "#CC79A7")
GRID = dict(color="#dddddd", lw=0.6)
plt.rcParams.update({"svg.fonttype": "none", "font.family": "sans-serif",
                     "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
                     "font.size": 12, "legend.fontsize": 10.5,
                     "xtick.labelsize": 11, "ytick.labelsize": 11,
                     "savefig.facecolor": "white"})


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)
    print("wrote", name)


# ------------------------------------------------------------------- A06 Mach sweep
def a06_ps_sweep():
    mach = np.linspace(0.35, 0.90, 300)

    def tw_required(ws):
        q = mach ** 2
        return 0.9 * q / ws + 0.035 * ws / q + 0.30 / mach + 6.0 * np.clip(mach - 0.78, 0, None) ** 2

    lines = [("Low wing loading", 0.7, SKY, "-"),
             ("Middle wing loading", 1.0, BLUE, "--"),
             ("High wing loading", 1.3, VERM, "-.")]
    ref = tw_required(1.0)[0]
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    mins = []
    for lab, ws, c, ls in lines:
        y = tw_required(ws) / ref
        mins.append(mach[np.argmin(y)])
        ax.plot(mach, y, color=c, ls=ls, lw=2.2, label=lab)
    # the dependence on Mach differs with wing loading; no minimum is marked, since
    # which speed or band applies is the team's reading (brief review 2026-10-22)
    assert len({round(m, 2) for m in mins}) == 3
    ax.set_xlabel("Mach number at the specific excess power condition")
    ax.set_ylabel("Thrust-to-weight ratio required (invented scale)")
    ax.set_xlim(0.35, 0.90)
    ax.grid(**GRID)
    ax.legend(loc="upper center", frameon=False)
    save(fig, "a06-ps-sweep")


# ------------------------------------------------------------ A06 constraint diagram
def a06_diagram():
    curves = [("Requirement A, threshold", 0.12, 0.45, BLUE, "-"),
              ("Requirement A, objective", 0.16, 0.62, BLUE, "--"),
              ("Requirement B, threshold", 0.22, 0.20, ORANGE, "-"),
              ("Requirement B, objective", 0.30, 0.26, ORANGE, "--")]
    line_k = ("Requirement C", 0.80)
    vlim = ("Requirement D", 1.05)
    px, py = 0.55, 0.82
    db = [(0.42, 1.25), (0.75, 1.02), (0.95, 1.18), (1.10, 0.92)]
    x = np.linspace(0.2, 1.3, 500)
    thr = [c for c in curves if "objective" not in c[0]]
    env_thr = np.max([c[1] / x + c[2] * x for c in thr] + [line_k[1] * x], axis=0)
    env_all = np.max([c[1] / x + c[2] * x for c in curves] + [line_k[1] * x], axis=0)
    ymax = 1.6
    left = x <= vlim[1]
    req = {c[0]: c[1] / px + c[2] * px for c in curves}
    req[line_k[0]] = line_k[1] * px
    top = max(req, key=req.get)
    assert px < vlim[1] and py > max(req.values())
    assert top in {c[0] for c in curves}, "nearest boundary must be a curve"
    assert np.interp(px, x, env_all) > np.interp(px, x, env_thr)

    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    ax.fill_between(x[left], env_thr[left], ymax, color="#e8e8e8", zorder=0,
                    label="Feasible, threshold set")
    ax.fill_between(x[left], env_all[left], ymax, facecolor="none", hatch="///",
                    edgecolor="#9a9a9a", lw=0, zorder=0, label="Feasible, objective set")
    for label, a, b, c, ls in curves:
        ax.plot(x, a / x + b * x, color=c, ls=ls, lw=2.2, label=label)
    ax.plot(x, line_k[1] * x, color=GREEN, ls="-.", lw=2.2, label=line_k[0])
    ax.axvline(vlim[1], color=BLACK, ls=":", lw=2.4, label=vlim[0])
    ax.plot(*zip(*db), "o", mfc="white", mec=BLACK, ms=8, mew=1.6, label="Database aircraft")
    ax.plot(px, py, "D", color=VERM, mec=BLACK, ms=10, zorder=6, label="Design point")
    ax.annotate("", xy=(px, req[top]), xytext=(px, py),
                arrowprops=dict(arrowstyle="<->", color=BLACK, lw=1.4))
    ax.annotate("", xy=(vlim[1], py), xytext=(px, py),
                arrowprops=dict(arrowstyle="<->", color=BLACK, lw=1.4))
    ax.text(px - 0.015, (py + req[top]) / 2, "margin", ha="right", va="center",
            fontsize=11, bbox=dict(fc="white", ec="none", pad=1))
    ax.text((px + vlim[1]) / 2, py + 0.04, "margin", ha="center", va="bottom", fontsize=11,
            bbox=dict(fc="white", ec="none", pad=1))
    ax.set_xlim(0.2, 1.3)
    ax.set_ylim(0, ymax)
    ax.set_xlabel(r"Wing loading $W_{TO}/S$, $S$ = reference wing area (invented scale)")
    ax.set_ylabel(r"Thrust-to-weight ratio $T_{SL}/W_{TO}$ (invented scale)")
    ax.grid(**GRID)
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False)
    save(fig, "a06-diagram")


# ------------------------------------------------------------------ A07 CG envelope
def a07_cg_envelope():
    fwd, aft = 0.16, 0.36
    cases = [("case A", 0.62, 0.21), ("case B", 0.66, 0.25), ("case C", 0.70, 0.30),
             ("case D", 0.74, 0.33), ("case E", 0.78, 0.335)]
    fuel, tank = 0.22, 0.26
    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    ax.axvline(fwd, color=VERM, lw=1.6, ls="--")
    ax.axvline(aft, color=VERM, lw=1.6, ls="-.")
    ax.text(fwd - 0.006, 0.54, "forward limit", color=VERM, rotation=90, va="bottom", ha="right")
    ax.text(aft + 0.006, 0.54, "aft limit", color=VERM, rotation=90, va="bottom", ha="left")
    xs = []
    for i, (lab, w0, x0) in enumerate(cases):
        wf = np.linspace(0, fuel, 30)
        w = w0 + wf
        x = (w0 * x0 + wf * tank) / w
        ax.plot(x, w, color=BLUE, lw=1.4, ls=["-", "--", "-.", ":", "-"][i])
        ax.plot(x0, w0, "o", mfc="white", mec=BLACK, ms=7)
        ax.plot(x[-1], w[-1], "s", mfc=BLACK, mec=BLACK, ms=5)
        if lab == "case E":
            # no room between case D's line and the aft limit: label outside, with a leader
            ax.annotate(lab, xy=(x0 + 0.003, w0), xytext=(0.372, w0), va="center", fontsize=11,
                        arrowprops=dict(arrowstyle="-", color=BLACK, lw=0.8))
        else:
            ax.text(x0, w0 - 0.014, lab, ha="center", va="top", fontsize=11)
        xs.extend(x)
    assert min(xs) > fwd and max(xs) < aft, "a loading case leaves the envelope"
    ax.plot([], [], "o", mfc="white", mec=BLACK, label="loading case, zero fuel")
    ax.plot([], [], "s", mfc=BLACK, mec=BLACK, label="same case, full fuel")
    ax.plot([], [], color=BLUE, lw=1.4, label="CG travel as fuel burns")
    ax.set_xlim(0.10, 0.42)
    ax.set_ylim(0.52, 1.10)
    ax.set_xlabel("CG position, fraction of the mean aerodynamic chord (invented scale)")
    ax.set_ylabel("Aircraft weight (invented scale)")
    ax.grid(**GRID)
    # opaque, so the forward-limit line does not run through the legend text
    ax.legend(loc="upper left", frameon=True, framealpha=1, edgecolor="none")
    save(fig, "a07-cg-envelope")


# ------------------------------------------------------------------ A07 scissor plot
def a07_scissor():
    x_ac, l_t, eta_h, sm, k = 0.25, 3.0, 0.9, 0.10, 0.30
    cl_max, cl_r, cl_app = 1.6, 1.5, 1.2
    clt_up, clt_dn = 0.5, -0.7
    cm0_clean, cm0_to, cm0_ldg = -0.05, -0.12, -0.20
    x = np.linspace(0.05, 0.65, 600)

    def line1(sm_):
        a = x - x_ac + sm_
        return a / (k * (l_t - a))

    def control(cl, clt, cm0, cm_req):
        return (cm0 + cl * (x - x_ac) - cm_req) / (eta_h * clt * (l_t - (x - x_ac)))

    l1, l0 = line1(sm), line1(0.0)
    l2 = control(cl_max, clt_up, cm0_clean, -0.16)
    l3 = control(cl_r, clt_dn, cm0_to, 0.15)
    l4 = control(cl_app, clt_dn, cm0_ldg, 0.0)
    aft_env, fwd_env = np.maximum(l1, l2), np.maximum(l3, l4)
    sel = 0.24

    def crossing(y, rising):
        idx = np.where(np.diff(np.sign(y - sel)) != 0)[0]
        assert len(idx) >= 1
        return x[idx[0] if rising else idx[-1]]

    x_aft, x_fwd = crossing(aft_env, True), crossing(fwd_env, False)
    assert x_fwd < x_aft
    i_aft = np.argmin(abs(x - x_aft))
    assert l1[i_aft] >= l2[i_aft], "line 1 must govern the aft limit"
    rng = (x_fwd + 0.03, x_aft - 0.03)
    assert rng[0] > x_fwd and rng[1] < x_aft, "the loading range must fit"

    fig, ax = plt.subplots(figsize=(6.8, 4.6))
    ax.fill_between(x, np.maximum(aft_env, fwd_env), 0.6, color="#eeeeee", label="feasible region")
    ax.plot(x, l3, color=ORANGE, lw=1.8, ls="-", label="line 3: takeoff rotation")
    ax.plot(x, l4, color=GREEN, lw=1.8, ls="--", label="line 4: landing approach")
    ax.plot(x, l1, color=BLUE, lw=1.8, ls="-", label="line 1: stability, chosen $SM$")
    ax.plot(x, l2, color=PURPLE, lw=1.8, ls="-.", label="line 2: stall recovery")
    ax.plot(x, l0, color=BLACK, lw=1.2, ls=":", label="neutral point, $SM$ = 0")
    ax.axhline(sel, color=VERM, lw=1.6, label="selected $S_t/S$")
    ax.plot([x_fwd, x_aft], [sel, sel], "|", color=VERM, ms=14, mew=2)
    ax.annotate("", xy=(rng[0], sel + 0.035), xytext=(rng[1], sel + 0.035),
                arrowprops=dict(arrowstyle="<->", color=BLACK, lw=1.2))
    ax.text((rng[0] + rng[1]) / 2, sel + 0.05, "loading range, Deliverable 1",
            ha="center", va="bottom", fontsize=11)
    ax.annotate("forward limit", xy=(x_fwd, sel), xytext=(0.16, 0.44), color=VERM,
                ha="center", fontsize=11, arrowprops=dict(arrowstyle="->", color=VERM, lw=1.1))
    ax.annotate("aft limit", xy=(x_aft, sel), xytext=(0.42, 0.44), color=VERM,
                ha="center", fontsize=11, arrowprops=dict(arrowstyle="->", color=VERM, lw=1.1))
    ax.set_xlim(0.05, 0.65)
    ax.set_ylim(0, 0.6)
    ax.set_xlabel("CG position, fraction of the mean aerodynamic chord (invented scale)")
    ax.set_ylabel("Tail area ratio $S_t/S$ (invented scale)")
    ax.grid(**GRID)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), frameon=False, ncol=3,
              fontsize=10.5, columnspacing=1.4, handlelength=2.2)
    save(fig, "a07-scissor")


# ---------------------------------------------------------------- A08 flight envelope
def a08_envelope():
    def ps(m, h):
        return (1.0 - h ** 1.6) - 2.6 * (m - (0.45 + 0.15 * h)) ** 2

    def stall_f(h):
        return 0.18 + 0.32 * h ** 1.3

    def vmax_f(h):
        return np.minimum(0.62 + 0.32 * h, 0.88)

    def root(f, lo, hi):
        f_lo = f(lo)
        assert (f_lo > 0) != (f(hi) > 0)
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if (f(mid) > 0) == (f_lo > 0):
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    M, H = np.linspace(0.1, 1.0, 400), np.linspace(0.0, 1.0, 400)
    MM, HH = np.meshgrid(M, H)
    inside = (MM >= stall_f(H)[:, None]) & (MM <= vmax_f(H)[:, None])
    PS = np.where(inside, ps(MM, HH), np.nan)
    h_j = root(lambda h: ps(stall_f(h), h), 0.3, 1.0)
    h_t = root(lambda h: ps(vmax_f(h), h), 0.3, 1.0)
    m_top = np.linspace(stall_f(h_j), float(vmax_f(h_t)), 200)
    h_top = np.array([root(lambda h, m=m: ps(m, h), 0.3, 1.0) for m in m_top])
    h_top[0], h_top[-1] = h_j, h_t
    h_dn, h_up = np.linspace(h_j, 0.0, 120), np.linspace(0.0, h_t, 120)
    edge_m = np.concatenate([stall_f(h_dn), vmax_f(h_up)])
    edge_h = np.concatenate([h_dn, h_up])
    # one closed boundary: the black path and the P_s = 0 line share both corners
    assert abs(edge_m[0] - m_top[0]) < 1e-9 and abs(edge_h[0] - h_top[0]) < 1e-9
    assert abs(edge_m[-1] - m_top[-1]) < 1e-9 and abs(edge_h[-1] - h_top[-1]) < 1e-9
    assert abs(ps(m_top, h_top)).max() < 1e-6

    fig, ax = plt.subplots(figsize=(6.8, 4.5))
    ax.contour(MM, HH, PS, levels=[0.25, 0.5, 0.75], colors=[BLUE], linewidths=[0.9],
               linestyles=[":"])
    ax.plot(m_top, h_top, color=BLUE, lw=2.6, solid_capstyle="round", zorder=4)
    ax.plot(edge_m, edge_h, color=BLACK, lw=1.8, solid_joinstyle="miter",
            solid_capstyle="projecting", clip_on=False, zorder=5)
    ax.text(0.27, 0.62, "stall", ha="right", fontsize=11)
    ax.text(0.89, 0.30, "maximum\nspeed", ha="left", fontsize=11)
    ax.text(0.52, 0.90, "$P_s$ = 0", color=BLUE, ha="center", fontsize=11)
    ax.text(0.47, 0.20, "$P_s$ contours", color=BLUE, ha="center", fontsize=11)
    conds = [("Condition 1", 0.40, 0.55, (0.02, -0.02, "left", "top")),
             ("Condition 2", 0.60, 0.35, (-0.02, -0.02, "right", "top")),
             ("Condition 3", 0.75, 0.70, (-0.02, 0.03, "right", "bottom"))]
    for lab, m, h, (dx, dy, ha, va) in conds:
        ax.plot(m, h, "D", color=VERM, ms=7)
        ax.text(m + dx, h + dy, lab, color=VERM, fontsize=11, ha=ha, va=va)
        i, j = np.argmin(abs(H - h)), np.argmin(abs(M - m))
        assert np.isfinite(PS[i, j]) and PS[i, j] > 0, lab
    ax.set_xlabel("Mach number (invented scale)")
    ax.set_ylabel("Pressure altitude (invented scale)")
    ax.set_xlim(0.1, 1.05)
    ax.set_ylim(0, 1.08)
    ax.grid(**GRID)
    save(fig, "a08-envelope")


if __name__ == "__main__":
    a06_ps_sweep()
    a06_diagram()
    a07_cg_envelope()
    a07_scissor()
    a08_envelope()
