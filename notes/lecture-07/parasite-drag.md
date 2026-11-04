---
title: "Drag, part 1: Parasite drag"
short_title: Parasite drag
---

This is the first part of Lecture 7, *Drag Prediction*. The lecture has three parts: parasite drag, drag due to lift, and the polar. This page covers what the RFP asks of the drag model and the parasite drag build-up. The second part, [](drag-polar.md), covers drag due to lift and the polar. The sources are Gudmundsson (2022), Chapters 8, 9, and 16; Nicolai and Carichner (2010), Chapters 2 and 5; Raymer (2018), Chapter 12; Shevell (1989); and Silva et al. (2021). The figures are redrawn after the figures on the slides and reduced to the point each slide makes.

:::{note} What to take from this lecture
- Parasite drag is built up by component from skin friction, form, interference, and the miscellaneous items.
- Skin friction is most of it, so the wetted area and the transition point decide $C_{D_0}$.
- A build-up is checked on a known aircraft before it is used on your own.
:::

## Requirements the drag model answers

:::{table} What the RFP asks of the drag model. Every value comes from the RFP; T is the threshold, O the objective.
:label: tbl-drag-requirements

| Item | Navy Jet Trainer |
| --- | --- |
| Speed | Mach 0.78 (T), Mach 0.90 (O) at 25,000 ft |
| Climb and maneuver | {term}`Specific excess power` 90 ft/s (T), 125 ft/s (O); sustained +4.0 g (T), +6.0 g (O), at 15,000 ft |
| Range | Ferry 600 nmi; reserves at maximum endurance speed |
| Low speed | {term}`FCLP`: 30 minutes at approach speed in the landing configuration |

:::

:::{admonition} Navy Jet Trainer
:class: navy

The RFP requires the derivation of the lift and drag models, and {term}`drag polars <drag polar>` for the cruise, takeoff, and landing configurations.
:::

## Three types of drag

:::{math}
:label: eq-drag-types
C_D = C_{D_0} + C_{D_i} + C_{D_c}
:::

:::{table} The three types of drag.
:label: tbl-drag-types

| Type | Source | Set by |
| --- | --- | --- |
| {term}`Parasite <parasite drag>`, $C_{D_0}$ | Skin friction, form, interference | Wetted area, shape |
| {term}`Induced <induced drag>`, $C_{D_i}$ | Lift | $AR$, {term}`span efficiency` |
| {term}`Compressibility <compressibility drag>`, $C_{D_c}$ | Mach number | $t/c$, sweep |

:::

:::{figure} figures/polar-types.svg
:label: fig-polar-types
:alt: Lift coefficient against drag coefficient at low speed. A dashed curve without the induced drag has its minimum near a drag coefficient of 0.0125 at a lift coefficient of about 0.27. The solid total curve lies to its right and moves farther away as lift rises. Arrows at a lift coefficient of 0.8 split the total into the minimum drag, a small viscous increment, and a large induced increment.
:width: 75%

How the polar splits at low speed. Schematic, after Nicolai and Carichner (2010), Figure 2.16, which shows the C-141A.
:::

Drag sets the thrust, the fuel, and the cost. One {term}`drag count` is a drag coefficient of 0.0001.

## Parasite drag build-up

:::{math}
:label: eq-buildup
C_{D_0} = \sum_{i}\frac{FF_i\,Q_i\,C_{f_i}\,S_{wet_i}}{S_{ref}} + C_{D_{misc}}
:::

:::{table} The terms of the build-up.
:label: tbl-buildup-terms

| Term | Meaning |
| --- | --- |
| $C_f$ | {term}`Skin friction coefficient` |
| $FF$ | {term}`Form factor`: pressure drag |
| $Q$ | {term}`Interference factor` |
| $S_{wet}$ | {term}`Wetted area` of the component |
| $C_{D_{misc}}$ | Gear, upsweep, leakage, protuberances, cooling |

:::

:::{figure} figures/drag-components.svg
:label: fig-drag-components
:alt: An aircraft drawn in top view as separate pieces with gaps between them: a triangular nose, a rectangular fuselage, two wing panels, and two tail panels. Each piece is labeled with its own area.
:width: 65%

The aircraft split into components, each with its own wetted area. Schematic, after Nicolai and Carichner (2010), Figure 2.18.
:::

Skin friction is 70 to 80% of subsonic $C_{D_0}$ (Nicolai and Carichner 2010, Chapter 2). The {term}`flat-plate area` expresses the same drag as an area: $f = C_{D_0}\,S_{ref}$.

:::{admonition} Navy Jet Trainer
:class: navy

Engine drag is booked in net thrust. Which drag items does your installed engine deck already carry, so that they stay out of this sum?
:::

## Skin friction

:::{figure} figures/skin-friction.svg
:label: fig-skin-friction
:alt: Skin friction coefficient against Reynolds number on logarithmic axes from ten thousand to one billion. The turbulent line falls slowly from about 0.013 to 0.0016. A dashed line for Mach 0.8 lies just below it. The laminar line falls much faster and reaches about 0.0006 at five million. A transition curve leaves the laminar line at a Reynolds number of 500,000 and joins the turbulent line near ten million.
:width: 80%

Skin friction against Reynolds number. Computed from the equations below, with 1700/$Re$ subtracted from the turbulent value for the transition curve; after Nicolai and Carichner (2010), Figure 2.6.
:::

:::{math}
:label: eq-cf
C_f^{\,lam} = \frac{1.328}{\sqrt{Re}}, \qquad C_f^{\,turb} = \frac{0.455}{(\log_{10}Re)^{2.58}}
:::

- $Re = \rho V l/\mu$, with the component length or chord.
- Transition happens near $Re_x = 5\times10^{5}$.
- Fully turbulent flow is the conservative assumption.
- Above Mach 0.3, divide $C_f$ by $(1 + 0.144\,M^{2})^{0.65}$ (Gudmundsson 2022, Eq. 16-44).

## Laminar flow and transition

:::{figure} figures/transition.svg
:label: fig-transition
:alt: Skin friction coefficient against the transition point as a fraction of chord, at a Reynolds number of two million. A fully turbulent line sits at about 0.0039 and a fully laminar line at about 0.0009. The mixed curve from Young's method starts near the turbulent line at the leading edge and falls to the laminar line at the trailing edge.
:width: 75%

Skin friction against the transition point. Computed with Young's method; after Gudmundsson (2022), Figure 16-29.
:::

With transition at $x_{tr}$, Young's method (Gudmundsson 2022, Eqs. 16-69 and 16-70) gives:

:::{math}
:label: eq-young
\frac{x_0}{c} = 36.9\left(\frac{x_{tr}}{c}\right)^{0.625}\left(\frac{1}{Re}\right)^{0.375}, \qquad C_f = \frac{0.074}{Re^{0.2}}\left(1-\frac{x_{tr}-x_0}{c}\right)^{0.8}
:::

- $x_{tr}$ comes from the airfoil data or a stated assumption.
- Rivets, joints, insects, and paint chips move transition forward.

:::{admonition} Navy Jet Trainer
:class: navy

The airfoil choice reaches the aircraft polar through $x_{tr}$. State the value and its source in {term}`ASORT`.
:::

## Wetted area and form factor

:::{table} Wetted area and form factor by component. After Shevell (1989) and Raymer (2018), Chapter 12.
:label: tbl-wetted-form

| Component | Wetted area | Form factor |
| --- | --- | --- |
| Wing, tails, pylons | $2\,(1.02)\,S_{exposed}$ | $1 + Z\,(t/c) + 100\,(t/c)^{4}$ |
| Fuselage | $\pi D\,l\left(1-\dfrac{2}{f}\right)^{2/3}\left(1+\dfrac{1}{f^{2}}\right)$ | $0.9 + \dfrac{5}{f^{1.5}} + \dfrac{f}{400}$ |
| Nacelle, pod | $\pi D\,l$ | $1 + \dfrac{0.35}{l/D}$ |

:::

In the table, $f = l/D$ is the fineness ratio, not the flat-plate area. The sweep and Mach term of the lifting surfaces is:

:::{math}
:label: eq-z
Z = \frac{(2-M^{2})\cos\Lambda_{c/4}}{\sqrt{1-M^{2}\cos^{2}\Lambda_{c/4}}}
:::

- Non-circular fuselage: use $D = \sqrt{4A_{max}/\pi}$.
- Square-sided fuselage: $FF = 1 + 1.30\,(FF_{round} - 1)$.

:::{admonition} Navy Jet Trainer
:class: navy

Measure the wetted areas from your loft once it exists. The formulas are the first pass.
:::

## Interference factors

:::{figure} figures/interference.svg
:label: fig-interference
:alt: A grid of small front and rear views with the interference factor Q under each. Wing on fuselage: high 1.0, mid 1.0, low with fillets 1.0, low with no fillet 1.2. Tail: conventional 1.04 to 1.05, T-tail 1.04 to 1.05, V-tail 1.03, H-tail 1.08. Nacelle on the wing or the fuselage: attached 1.5, within one diameter 1.3, beyond one diameter 1.0.
:width: 90%

Interference factors by arrangement. The nacelle row covers the wing and the fuselage. Values from Raymer (2018), Chapter 12.
:::

Spacing, fillets, and fairings bring $Q$ down to 1.0.

## Miscellaneous drag

:::{table} Leakage and protuberance drag, as a share of $C_{D_0}$. Values from Raymer (2018), Chapter 12.
:label: tbl-leakage

| Aircraft | Share of $C_{D_0}$ |
| --- | ---: |
| Jet transport | 2 to 5% |
| Propeller aircraft, jet fighter | 5 to 10% |

:::

:::{table} Landing gear drag, $D/q$ per unit of frontal area. Values from Raymer (2018), Chapter 12.
:label: tbl-gear-drag

| Item | $D/q$ per frontal area |
| --- | ---: |
| Wheel and tire | 0.25 |
| Wheel and tire, faired | 0.13 |
| Streamlined strut | 0.05 |

:::

From $D/q$ to the drag coefficient, with $(D/q)_i$ the table value times the frontal area:

:::{math}
:label: eq-dq
\Delta C_{D_0} = \frac{\sum_i (D/q)_i}{S_{ref}}
:::

:::{figure} figures/upsweep.svg
:label: fig-upsweep
:alt: Side view of a fuselage with its aft lower surface rising toward the tail. The angle between the aft lower surface and a horizontal dashed line is marked u.
:width: 60%

The aft-fuselage upsweep angle $u$. Schematic.
:::

- Aft-fuselage upsweep: $D/q = 3.83\,u^{2.5}A_{max}$, with $u$ in radians (Raymer 2018, Eq. 12.36). Separation is likely above 15°.
- Cooling air: $D = \dot{m}\,(V_\infty - V_e)$, the momentum lost through the installation (Gudmundsson 2022, Eq. 16-147).

:::{admonition} Navy Jet Trainer
:class: navy

FCLP is flown in the landing configuration for 30 minutes. Which drag items does that segment carry that cruise does not?
:::

## Worked example: Cirrus SR22 build-up

Condition: 313 ft/s at 8,000 ft, Mach 0.288. $S_{ref}$ = 144.9 ft². Fully turbulent flow.

:::{table} The two largest rows of the build-up, from {eq}`eq-buildup`. Wing chord 3.98 ft, $t/c$ 0.15, no sweep; fuselage 22.42 ft long, 4.17 ft in diameter; $Re$ per foot 1.635 million.
:label: tbl-sr22-rows

| Component | $Re$ | $C_f$ | $S_{wet}$ (ft²) | $FF$ | $Q$ | $C_{D_0}$ | $f$ (ft²) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Wing | 6.51 million | 0.00322 | 261.7 | 1.351 | 1.0 | 0.0079 | 1.14 |
| Fuselage | 36.7 million | 0.00246 | 222.8 | 1.314 | 1.0 | 0.0050 | 0.72 |

:::

The wing's wetted area uses $S$ less the part the fuselage covers, about $D$ times the chord.

:::{table} Inputs for the other rows. Tails use {eq}`eq-buildup` with $S_{exposed} = S$; gear uses {numref}`tbl-gear-drag` and {eq}`eq-dq` with the $Q$ shown.
:label: tbl-sr22-inputs

| Item | Inputs | $f$ (ft²) |
| --- | --- | ---: |
| Horizontal tail | $c$ 2.34 ft, $S$ 25.75 ft², $\Lambda$ 5°, $t/c$ 0.10, $Q$ 1.04 | 0.23 |
| Vertical tail | $c$ 3.18 ft, $S$ 15.93 ft², $\Lambda$ 18°, $t/c$ 0.10, $Q$ 1.04 | 0.14 |
| Nose gear | Strut 1.8 ft², faired wheel 0.49 ft², $Q$ 1.2 | 0.18 |
| Main gear | Two legs, each strut 2.12 ft², faired wheel 0.63 ft², $Q$ 1.2 | 0.45 |
| Windscreen | Given | 0.45 |
| Engine cooling | Given | 0.15 |
| Engine installation | Given | 0.06 |
| Leakage and protuberance | 8% of the sum of the components above | 0.27 |

:::

:::{figure} figures/sr22-buildup.svg
:label: fig-sr22-buildup
:alt: Horizontal bars of flat-plate area in square feet, largest first: wing 1.14, fuselage 0.72, main gear 0.45, windscreen 0.45, leakage and protuberance 0.27, horizontal tail 0.23, nose gear 0.18, engine cooling 0.15, vertical tail 0.14, engine installation 0.06.
:width: 80%

The SR22 build-up by component, in flat-plate area. Computed; fully turbulent flow.
:::

Result: $f$ = 3.79 ft² and $C_{D_0}$ = 0.0262. Gudmundsson (2022), Example 16-22, reports 0.0254 from published performance data.

The wing and the fuselage lead. The main gear and the windscreen follow at 0.45 ft² each.

:::{seealso}
Continue with [](drag-polar.md): drag due to lift, the SR22 polar, the polar at high lift, ground effect, compressibility drag, the three polars, and the checks. The references for both parts are at the end of that page.
:::
