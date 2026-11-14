---
title: "Stability and control, part 1: The method and the center of gravity"
short_title: The method and the center of gravity
---

This is the first part of Lecture 10, *Stability and Control*. The lecture has four parts: the method and the center of gravity (CG), longitudinal static stability and the horizontal tail, trim, and lateral-directional stability with the control surfaces. This page covers what the RFP asks, the eight steps of the method, and step 1, the CG table and the {term}`CG envelope`. The second part is [](longitudinal-stability.md), the third [](trim.md), and the fourth [](lateral-and-controls.md). The sources are Gudmundsson (2022), Chapters 11, 24, and 25; Nelson (1998), Chapter 2; Raymer (2018), Chapters 4 and 6; and Torenbeek (1982), Section 9.5. The figures are redrawn after the figures on the slides.

:::{note} What to take from this lecture
- The stability and control method has eight steps. They iterate with the layout, the weights, and the polar.
- The CG table gives the CG of every loading case the RFP implies. The CG envelope shows them against the forward and aft limits.
- The CG limits and the tail area depend on each other. The first two steps take two passes.
:::

## What the RFP asks

:::{table} What the RFP asks of the stability and control analysis.
:label: tbl-sc-requirements

| Item | Navy Jet Trainer |
| --- | --- |
| Analysis | Climb, cruise, maneuvering, and low-speed operations: takeoff and landing |
| Deliverables | Criteria for horizontal and vertical tail sizing; longitudinal static stability and trim analysis; longitudinal and lateral-directional dynamic stability analysis |
| Flight control system | The architecture and the major components shall be specified |
| Data items | A dimensioned three-view with the location of the neutral point, the tail moment arms, and a table of the aircraft areas; the control surface sizes; the CG envelope |
| Center of gravity | The CG for all loading cases; a weight statement that includes the minimum and maximum crew weights and single-pilot operations |
| Standard | MIL-HDBK-516C, whose Section 6.1 (flying qualities) applies MIL-STD-1797; the configuration may be statically stable or unstable |

:::

This lecture's method covers every item except the dynamic stability analysis.

## Methodology

The method has eight steps, and step 8 returns to step 1: the steps iterate with the layout, the weights, and the polar ({numref}`fig-sc-method`).

:::{figure} figures/method-flow.svg
:label: fig-sc-method
:alt: A flow of eight steps in two rows. Top row, left to right. Step 1, CG table and envelope: every loading the RFP implies. Step 2, scissor plot: the tail area ratio and the forward and aft limits. Step 3, tail geometry: aspect ratio, taper, sweep, and incidence. Step 4, trim: angle of attack, elevator deflection, and trim drag at every condition. Bottom row, right to left. Step 5, vertical tail: volume coefficient, yaw stiffness, engine out, and crosswind. Step 6, dihedral: from the dihedral angle, sweep, and wing height. Step 7, control surfaces: elevator, rudder, ailerons, and the system. Step 8, check: vortex lattice and three-view. A dashed arrow returns from step 8 to step 1, labeled iterate: layout, weights, polar.
:width: 100%

The eight steps of the method. Schematic.
:::

The inputs are the A04 loft, the high-lift increments, the thrust line, and the weight statement. The loft gives $S$, $AR$, $\bar c$, $x_{LEMAC}$, $x_{ac}$, and $C_{M,ac}^{W}$. Steps 1 and 2 depend on each other: the CG envelope needs the CG limits, and the CG limits need the loading cases. Plan two passes.

:::{admonition} Navy Jet Trainer
:class: navy

A tail sized here changes the CG, the polar, and the weights. Which of your A04 to A06 results change with it?
:::

## Symbols

:::{table} Symbols of this lecture. Superscripts $W$, $T$, and $V$ mark coefficients of the wing with the body, the horizontal tail, and the fin. Subscripts $t$ and $v$ mark the geometry of the tail and the fin.
:label: tbl-sc-symbols

| Symbol | Meaning |
| --- | --- |
| $\bar c$; $\bar x = x/\bar c$ | {term}`Mean geometric chord`, the $c_{MGC}$ of [Lecture 5](../lecture-05/wing-geometry-and-lift.md); a position in chords from its leading edge |
| $x_{ac}$, $x_{cg}$, $x_n$ | Wing aerodynamic center, taken for the wing with the body; CG; {term}`neutral point` |
| $SM = \bar x_n - \bar x_{cg}$ | {term}`Static margin` |
| $l_t$, $l_v$ | Distance from the wing aerodynamic center to the tail aerodynamic center, and to the aerodynamic center of the fin. Some books measure from the CG |
| $V_H = S_t l_t/(S\bar c)$, $V_v = S_v l_v/(S b)$ | {term}`Volume coefficients <tail volume coefficient>` of the tail and the fin |
| $\eta_H = q_t/q$; $\varepsilon$, $\varepsilon_0$; $i_t$ | Dynamic-pressure ratio at the tail; downwash and its value at $\alpha = 0$; tail incidence |
| $\alpha_t = \alpha + i_t - \varepsilon$ | Angle of attack of the tail |
| $\delta_e$, $\delta_r$, $\delta_a$; $\tau$; $E = c_e/\bar c_t$ | Deflections of the elevator, the rudder, and the ailerons; flap effectiveness; elevator chord ratio |
| $\bar c_t$, $\bar c_v$ | Mean chords of the horizontal tail and the fin; $\bar c_t$ is not the tip chord $c_t$ of [Lecture 5](../lecture-05/wing-geometry-and-lift.md) |
| $c_e$, $c_{rud}$ | Chords of the elevator and the rudder |
| $\eta_v$; $l_{v,cg}$ | Dynamic-pressure ratio at the fin; arm from the CG to the fin aerodynamic center, used for moments about the CG |
| $\beta$; $C_n$; $C_\ell$ | Sideslip angle; yawing moment; rolling moment. $C_\ell$ is never a lift coefficient |

:::

A nose-up pitching moment is positive. $\beta$ is positive with the wind from the right. $\delta_e$ is positive with the trailing edge down. In this lecture $\alpha$ is the angle of attack, $\beta$ the sideslip, $\sigma$ the sidewash angle, and $\mu$ the mass parameter of the trim page. They are not the thrust lapse, the weight fraction, the density ratio, and the friction coefficient of [Lecture 9](../lecture-09/constraint-method.md).

## Step 1: the CG table

:::{figure} figures/cg-table-sketch.svg
:label: fig-cg-table
:alt: Side view of a tandem-seat jet trainer, nose to the left, with a vertical datum line ahead of the nose and an x axis running aft. Downward arrows mark seven weights, each at its own position along the axis, from front to back: crew in the cockpit, fuselage, wing, fuel in a tank just aft of the wing root, engine in the aft fuselage, horizontal tail, and fin. Dashed outlines show the fuel tank and the engine. A dimension from the datum to the wing weight is labeled x wing.
:width: 75%

Each item of the weight statement acts at its own position aft of the datum. Schematic.
:::

With $W_i$ the weight of item $i$ and $x_i$ its position aft of the datum, the CG is the weighted mean of the positions. The second relation gives it in chords from the leading edge of $\bar c$, at $x_{LEMAC}$:

:::{math}
:label: eq-cg
x_{cg} = \frac{\sum_i x_i W_i}{\sum_i W_i}, \qquad \bar x_{cg} = \frac{x_{cg} - x_{LEMAC}}{\bar c}
:::

- Enter every item of the weight statement at its centroid, from the CAD model.
- Give the crew, the payload, and the fuel their own rows. They move the CG.
- Put the datum ahead of the nose. Take $x_{LEMAC}$ from the loft.
- Before a weight build-up exists, take approximate locations from Raymer (2018), Table 15.2.
- The CG table is the weight statement with an $x$ column added.

### The CG table of a winning report

{numref}`tbl-uiuc-cg` is the CG table of the report that won the AIAA 2024-25 undergraduate competition. The published reports and handbooks quoted in this lecture call the mean geometric chord the MAC, and their values are kept in % MAC.

:::{table} The CG table of the University of Illinois 2025 undergraduate report, its 27 rows grouped here. The CG is at 37.9% MAC at MTOW and at 52.5% MAC empty. Team Draco (2025), Table 22; totals from their Table 24.
:label: tbl-uiuc-cg

| Component | $W_i$ (lb) | $x_i$ (in) | Source of the weight |
| --- | ---: | ---: | --- |
| Fuel, nine tanks | 14,490 | 331 | CAD |
| Wing | 1,980 | 360 | CAD |
| Fuselage and radome | 3,738 | 378 | CAD |
| Horizontal tail | 513 | 565 | CAD |
| Vertical tail | 283 | 520 | CAD |
| Engine and starter | 3,882 | 540 | Manufacturer's data |
| Missiles, two AIM-120 | 654 | 275 | RFP |
| Launchers, two | 154 | 275 | Manufacturer's data |
| Avionics and radar | 1,825 | 123 | RFP, Raymer |
| Landing gear | 1,140 | 280 | Nicolai |
| Systems, six rows | 2,375 | 313 | Nicolai, Raymer |
| **MTOW** | **31,034** | **353.1** | Sum of the rows |
| **Empty weight** | **15,890** | **376.7** | Without the fuel and the two missiles |

:::

The datum is at the nose. The locations come from the CAD model, and the source of each weight has its own column. The report's 27 rows sum to 353.1 in at MTOW and 376.7 in empty; the grouped rows here give 353.3 in and 376.9 in, because their positions are rounded to the inch. The empty weight keeps the missile launchers. Adding the items one at a time (their Table 23), the report places the CG at 42% MAC with the wing alone, 101% with the engine added, and 37.9% at MTOW.

The University of Liège 2025 graduate report gives the same table (their Table 15), with 21 rows in lb and ft from the nose. It places the zero-fuel weight of 46,169 lb at 56.68 ft and the MTOW of 91,238 lb at 54.73 ft. Build your table the same way: one row per item, with the source of every weight.

## Step 1: the CG envelope

The CG envelope plots the weight against the CG position ({numref}`fig-cg-envelope`). The loading loop is the path that joins the loading cases. The CG limits are the forward limit and the aft limit.

:::{figure} figures/cg-envelope.svg
:label: fig-cg-envelope
:alt: Weight over maximum takeoff weight against CG position in chords, with invented values. A solid path joins four loading cases, each given as CG position and weight ratio: a, empty, 0.34 and 0.56; b, with crew, 0.28 and 0.60; c, with payload, 0.36 and 0.78; d, maximum takeoff weight, 0.35 and 1.00. A dash-dot path goes from b to e, fuel loaded before payload, at 0.28 and 0.82, and on to d. Two vertical dashed lines mark the forward limit at 0.23 and the aft limit at 0.41. The whole loop lies between them.
:width: 80%

The CG envelope: the loading loop inside the forward and aft limits, with the loading cases a empty, b crew, c payload, d MTOW, and e fuel before payload. Computed from invented weights and arms.
:::

Plot one point for each loading case: empty, crew, payload, and fuel, in every order the RFP allows, with the fuel burning down. The forward limit comes from the nose-up control at rotation and on approach. The aft limit comes from the minimum static margin and the stall recovery. Both come from step 2. The loading loop must lie inside the CG limits with margin. An engine behind the crew moves the empty CG aft, and the crew moves it forward. Check both ends of the loop.

:::{admonition} Navy Jet Trainer
:class: navy

The RFP gives pilots of 103 lb to 205 lb nude weight, plus 35 lb of flight suit, equipment, and survival kit for each, and asks for a weight statement that covers single-pilot operations. Which loading cases does that imply?
:::

### A published CG envelope

:::{figure} figures/sr22.jpg
:label: fig-sr22-photo
:alt: A Cirrus SR22 on final approach against a blue sky, gear fixed and down, above a line of trees.
:width: 55%

Cirrus SR22. Photo by The Bushranger, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Cirrus_SR22_on_final_at_Apalachicola_Regional_Airport.jpg).
:::

:::{figure} figures/sr22-envelope.svg
:label: fig-sr22-envelope
:alt: Weight in pounds against CG position in inches aft of the datum for the Cirrus SR22. The allowed region is a shaded polygon. The forward limit passes through three points: 137.8 inches, 9.8% MAC, at 2,100 pounds; 139.1 inches, 12.5%, at 2,700 pounds; and 142.3 inches, 19.2%, at 3,400 pounds. The aft limit is a vertical line at 148.1 inches, 31.5% MAC, at every weight.
:width: 75%

The CG envelope of the Cirrus SR22. Values from the Cirrus SR22 Pilot's Operating Handbook, Figure 2-4.
:::

The forward limit moves aft as the weight rises. Gudmundsson (2022), Section 6.7.2, gives two causes for such a slope: the structural limit of the nose landing gear, and the elevator limit at takeoff rotation. His Figure 6-28 draws the elevator limit as a sloped line. The aft limit is one line: the static margin does not depend on the weight. At the maximum weight the CG range runs from 19.2% to 31.5% MAC.

:::{admonition} Navy Jet Trainer
:class: navy

The CG envelope the RFP asks for is this plot, with your limits from step 2. Does every loading case of your CG table lie inside it?
:::

:::{seealso}
Continue with [](longitudinal-stability.md): the pitching moment, the neutral point and the static margin, the scissor plot, and the tail geometry. The references for the four parts are at the end of [](lateral-and-controls.md).
:::
