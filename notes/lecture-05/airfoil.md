---
title: "Aerodynamics, part 1: The airfoil"
short_title: The airfoil
---

This is the first part of Lecture 5, *Aerodynamics: Airfoil and Wing*: from the requirement to the airfoil, the planform, and the lift model. The lecture has four parts: the requirements, the airfoil, the wing geometry, and the lift model. This page covers the first two: what the RFP asks of the wing, and how an airfoil is read and chosen, the families, the airfoil data, the Reynolds and Mach effects, the stall classes, and the comparison that ends in a selection. The second part, [](wing-geometry-and-lift.md), covers the planform and the lift model. The sources are Gudmundsson (2022), Chapters 8, 9, and 16, and Nicolai and Carichner (2010), Chapter 2. The figures are redrawn after the figures on the slides and reduced to the point each slide makes; the captions name the source figure.

:::{note} What to take from this lecture
- Every wing choice traces to a requirement: speed, field length, maneuver, or low speed.
- Airfoil data come from published curves, not from a model.
- The Reynolds number and the Mach number decide which data apply.
- The airfoil is chosen by a comparison on traced criteria, with the runner-up recorded.
:::

## Requirements that size the wing

:::{table} What the RFP asks of the wing. Every value comes from the RFP; T is the threshold, O the objective.
:label: tbl-wing-requirements

| Requirement | Navy Jet Trainer |
| --- | --- |
| Speed | Mach 0.78 (T), Mach 0.90 (O) at 25,000 ft |
| Field | Takeoff 5,000 ft and landing 5,000 ft, at 5,000 ft density altitude |
| Maneuver and climb | Sustained +4.0 g (T), +6.0 g (O) at 15,000 ft; specific excess power 90 ft/s (T), 125 ft/s (O) at 15,000 ft |
| Low speed | FCLP approach; full view over the nose on a 3.5° glide slope |

:::

:::{admonition} Navy Jet Trainer
:class: navy

The proposal must contain the wing planform, the airfoil selection, and the derivation of the lift model. Which requirement in {numref}`tbl-wing-requirements` do you expect to drive each one?
:::

## Lift has a price

::::{grid} 1 2 4 4

:::{card}
:header: Lift costs
Drag and a nose-down pitching moment.
:::

:::{card}
:header: The wing design affects
Stall speed. Takeoff and landing distance. Maximum speed. Range and endurance. Maneuver.
:::

:::{card}
:header: To determine
$S$, $AR$, $\lambda$, $\Lambda$, twist, incidence, height on the fuselage, the airfoil, and $t/c$.
:::

:::{card}
:header: In later lectures
Flaps: high lift. Dihedral: lateral stability. Ailerons: control sizing.
:::

::::

:::{figure} figures/wing-airfoil-nomenclature.svg
:label: fig-wing-nomenclature
:alt: Left, a swept and tapered wing planform in top view with the datum line, the span b, the root chord, the tip chord, the leading-edge sweep angle, a dashed quarter-chord line, and the mean geometric chord drawn as a thick bar at its spanwise station y MGC, set back by x MGC. Right, an airfoil with its chord line, dashed mean camber line, the maximum thickness and the maximum camber marked by arrows, and the leading edge, trailing edge, upper surface, and lower surface labeled.
:width: 100%

Wing and airfoil nomenclature. After Nicolai and Carichner (2010), Figure 2.1.
:::

:::{admonition} Navy Jet Trainer
:class: navy

A04: each choice is traced to a requirement and entered in {term}`ASORT`.
:::

## Airfoil families

:::{figure} figures/naca-families.svg
:label: fig-naca-families
:alt: Six airfoil outlines in two rows with their mean camber lines dashed. Top row: NACA 0012, symmetric and 12 percent thick, with a straight mean camber line; NACA 2412, with a gently arched one that peaks at 40 percent of the chord; NACA 23012, with its camber concentrated near the leading edge, at 15 percent of the chord. Bottom row: NACA 65 2-415, a 6-series airfoil, thickest at 40 percent of the chord, with a thin cusped rear; NASA NLF(1)-0416, a laminar airfoil 16 percent thick, concave under the trailing edge; NASA SC(2)-0714, a supercritical airfoil with a blunt nose, a nearly flat upper surface, aft camber, and a blunt trailing edge.
:width: 100%

Six airfoils, at least one from each family in {numref}`tbl-airfoil-families`. The NACA 0012, 2412, and 23012 are computed from the published shape equations. The NACA 65$_2$-415 (NACA Report 824), the NASA NLF(1)-0416 (NASA TP-1861), and the NASA SC(2)-0714 (NASA TP-2969) are drawn from their published coordinates, as listed in the UIUC Airfoil Coordinates Database.
:::

- The 4-digit and 5-digit numbers encode camber and thickness.
- The 6-series and the newer laminar and supercritical families are defined by their pressure distributions and have no simple formula.
- Gudmundsson (2022), Figure 8-39, shows the measured lift curves and polars of five such airfoils.

:::{table} Airfoil families and what each trades. After Gudmundsson (2022), Tables 8-7 and 8-12, and Nicolai and Carichner (2010).
:label: tbl-airfoil-families

| Family | Strength | Weakness |
| --- | --- | --- |
| NACA 4-digit | Benign stall; tolerates roughness | Low $C_{l_{max}}$, high $C_{d_{min}}$ |
| NACA 5-digit | High $C_{l_{max}}$, low $C_{d_{min}}$ and low $\lvert C_m \rvert$ | Abrupt stall |
| NACA 6-series | Drag bucket when the surface is smooth | Surface sensitive; high $\lvert C_m \rvert$ |
| Laminar (NLF) | Lowest drag inside the bucket | Needs a smooth composite skin |
| Supercritical | Higher $M_{dd}$ at the same $t/c$ | Aft camber: nose-down $C_m$ |

:::

:::{admonition} Navy Jet Trainer
:class: navy

A04 accepts only cited, published data. Start with NACA Report 824 and Gudmundsson (2022), Table 8-10. A polar a model produced is not data.
:::

## Reading airfoil data

:::{figure} figures/section-data.svg
:label: fig-section-data
:alt: Two plots of measured data for the NACA 65 2-415. Left, section lift coefficient against angle of attack: a straight line through the zero-lift angle, marked at about minus 2.6 degrees, with its linear range and slope labeled. The curve bends over to the maximum lift coefficient, marked at about 1.6 near 18 degrees, the stall angle, then falls to about 1.1 at 23 degrees. Right, section lift coefficient against drag coefficient: the drag stays near 0.0043 for lift coefficients from 0.1 to 0.65, a shaded band labeled drag bucket, the low-drag range, with the minimum drag marked inside it. Above the band the drag rises to about 0.02 at a lift coefficient of 1.4.
:width: 100%

What to read from an airfoil's lift curve and drag polar. NACA 65$_2$-415 (NACA Report 824); values read from Gudmundsson (2022), Figure 8-74. His Figure 8-5 marks the same quantities on the NACA 4415.
:::

Read from the curves:

- $C_{l_\alpha}$ and $\alpha_{ZL}$.
- $C_{l_{max}}$, $\alpha_{stall}$, and the shape of the stall.
- $C_{d_{min}}$ and the $C_l$ where it occurs.
- $C_m$ about $c/4$.
- The test Reynolds number, Mach number, and surface condition.

:::{admonition} Navy Jet Trainer
:class: navy

A04 Deliverable 1: the lift curve and polar of the selected airfoil, from published data, with the design point marked.
:::

## Camber and thickness

:::{figure} figures/camber-effect.svg
:label: fig-camber
:alt: Left, lift coefficient against angle of attack for the cambered NACA 64 1-412, solid, and the symmetric NACA 64 1-012, dashed, with markers at the tabulated values. The cambered curve is shifted up and to the left: it crosses zero lift at minus 2.6 degrees, marked alpha ZL, against 0 degrees, and reaches a maximum lift coefficient of 1.67 against 1.44, both at 15 degrees. Right, the drag polars with markers at lift coefficients of 0, 0.4, and 0.8. The symmetric airfoil has its drag bucket around zero lift; the cambered airfoil has it around 0.4. Drag coefficients, symmetric then cambered: 0.0042 and 0.0058 at zero lift, 0.0062 and 0.0046 at 0.4, 0.0081 and 0.0076 at 0.8.
:width: 100%

The effect of camber on the lift curve and the drag polar: the NACA 64$_1$-012 and the NACA 64$_1$-412, the same thickness without and with camber. Markers: values from Gudmundsson (2022), Table 8-9 (NACA Report 824, Reynolds number about 9 million). Lines: smooth curves through them, after his Figure 8-54 and Table 8-4.
:::

::::{grid} 1 1 2 2

:::{card}
:header: More camber
- Higher $C_{l_{max}}$.
- The drag bucket moves to higher $C_l$.
- Cost: more nose-down $C_m$ and trim drag.
:::

:::{card}
:header: More thickness
- A deeper spar, so a lighter wing.
- More fuel volume.
- $C_{l_{max}}$ peaks for $t/c$ of 0.09 to 0.15.
- Costs: higher $C_{d_{min}}$, lower $M_{crit}$.
:::

::::

## Reynolds number

:::{figure} figures/reynolds-effect.svg
:label: fig-reynolds
:alt: Left, lift coefficient against angle of attack at three Reynolds numbers, Re 1 less than Re 2 less than Re 3: the same slope in the linear range, with the maximum lift coefficient and the stall angle increasing with Reynolds number. Right, the drag polars: the minimum drag coefficient falls as the Reynolds number rises.
:width: 100%

The effect of Reynolds number on the lift curve and the drag polar. Schematic, after Gudmundsson (2022), Figure 8-55.
:::

- Higher {term}`Reynolds number`: higher $C_{l_{max}}$ and $\alpha_{stall}$, lower $C_{d_{min}}$. $C_{l_\alpha}$ does not change.
- $Re = \rho V c_{MGC} / \mu$, on the mean geometric chord.
- Use data at your $Re$: stall, climb, cruise.

:::{admonition} Navy Jet Trainer
:class: navy

Candidates must be credible at your Reynolds numbers and at the maximum operating Mach number of the RFP. Which published data sets reach them?
:::

## Stall behavior

:::{figure} figures/stall-classes.svg
:label: fig-stall-classes
:alt: Three schematic lift curves with the same peak. Class A, trailing-edge stall, rounds over gently past its peak. Class B, between A and C, peaks and falls at a moderate rate. Class C, leading-edge stall, rises to a peak and drops suddenly.
:width: 100%

The three stall classes. Schematic, after Gudmundsson (2022), Figure 8-72.
:::

Class A: separation grows forward from the trailing edge. Class C: a leading-edge separation bubble bursts. Class B lies between them.

:::{admonition} Navy Jet Trainer
:class: navy

Decide whether "basic maneuvers" include stalls. Either way, find the stall class of each candidate.
:::

## Compressibility

:::{figure} figures/mach-effects.svg
:label: fig-mach-effects
:alt: Left, lift coefficient against angle of attack at Mach 0.2, 0.6, 0.7, and 0.8: from 0.2 to 0.7 the slope steepens and the stall comes earlier at about the same maximum lift coefficient; at Mach 0.8 the curve is a shallower line through zero lift near 0 degrees. Right, section drag coefficient against Mach number: flat at the incompressible level of 0.006, then rising steeply. A dashed line at Mach 0.60 marks where the wave drag starts, labeled the M crit of the Korn relation. A marker at Mach 0.70 shows the Boeing definition of drag divergence, 0.002 above the incompressible level; a second marker at Mach 0.71 shows the Douglas definition, a slope of 0.10 per unit Mach.
:width: 100%

Mach number effects on the lift curve and the drag coefficient, with the critical and drag divergence Mach numbers. Schematic, after Gudmundsson (2022), Figure 8-67. The drag rise is drawn for a conventional airfoil with $t/c$ = 0.12 at $C_l$ = 0.4: {eq}`eq-korn-section` gives $M_{dd}$ = 0.71, and the wave drag starts 0.108 below it.
:::

- $M_{crit}$, the {term}`critical Mach number`: the first sonic point on the airfoil. Airfoil data list it: 0.70 for the NACA 64$_1$-412 (Gudmundsson 2022, Table 8-9).
- Drag-rise models use the same symbol for the Mach number at which the wave drag starts, 0.108 below $M_{dd}$ in the Korn relation of [part 2](wing-geometry-and-lift.md). {numref}`fig-mach-effects` marks that value.
- $M_{dd}$, the {term}`drag divergence Mach number`. Boeing: $C_d$ 0.002 above the incompressible level. Douglas: $dC_d/dM = 0.10$.
- The Korn relation for an airfoil (Gudmundsson 2022, Eq. 8-67):

:::{math}
:label: eq-korn-section
M_{dd} = \kappa - \frac{t}{c} - 0.1\,C_l, \qquad \kappa = 0.87 \text{ conventional}, \ 0.95 \text{ supercritical}
:::

- To raise $M_{crit}$: lower $t/c$, sweep, lower $AR$. A supercritical airfoil raises $M_{dd}$ by weakening the shock.

:::{admonition} Navy Jet Trainer
:class: navy

Mach 0.78 (T) and Mach 0.90 (O) at 25,000 ft. Thickness, sweep, and airfoil are one decision.
:::

## Transonic flow and the supercritical airfoil

:::{figure} figures/transonic-flow.svg
:label: fig-transonic
:alt: Three sketches of an airfoil in a flow from the left. At Mach 0.72 a dot marks the first point where the local Mach number reaches 1. At Mach 0.82 a shaded supersonic region on the upper surface ends in a normal shock, with separated flow drawn behind it. At Mach 1.05 a curved bow wave stands ahead of the leading edge and two shocks trail from the trailing edge.
:width: 100%

Transonic flow over an airfoil as the Mach number rises. Schematic, after Nicolai and Carichner (2010), Figure 2.19.
:::

:::{figure} figures/supercritical-airfoil.svg
:label: fig-supercritical
:alt: Left, the conventional NACA 64A410 at Mach 0.72: a supersonic region on the upper surface ends in a strong shock at mid-chord, with separated flow behind it. Below, the pressure coefficient, upper surface solid, lower dashed: the upper surface reaches about minus 1.25, past the sonic value of minus 0.70, and jumps to about minus 0.3 at the shock. Right, the supercritical NASA SC(2)-0710 at Mach 0.80, flatter on top: a longer, lower supersonic region ends in a weak shock near 72 percent of the chord. Below, the upper surface holds a plateau near minus 0.75, past the sonic value of minus 0.43, with a small step at the shock; the lower surface rises to about plus 0.45 near 85 percent, the aft loading.
:width: 90%

A conventional airfoil (NACA 64A410) and a supercritical airfoil (NASA SC(2)-0710), both with $t/c$ = 0.10, at the same lift coefficient. Outlines from the published coordinates (NACA Report 903 and NASA TP-2969, as listed in the UIUC Airfoil Coordinates Database). Flow and pressure distributions schematic, after Nicolai and Carichner (2010), Figure 2.22; the sonic pressure coefficient is computed for each Mach number.
:::

- A flatter upper surface gives a weaker shock and less separation.
- Aft camber recovers the lift and adds nose-down $C_m$.
- At the same $t/c$, a higher $M_{dd}$. At the same $M_{dd}$, a thicker and lighter wing.

## Design lift coefficient and the drag bucket

:::{figure} figures/drag-bucket.svg
:label: fig-drag-bucket
:alt: Three schematic drag polars, drag coefficient against lift coefficient, each with the cruise and climb lift coefficients marked by dashed vertical lines. Left, undesirable: no drag bucket and a high minimum drag at a high lift coefficient. Center, desirable: a wide flat bucket with the cruise and climb lift coefficients inside it. Right, undesirable: a narrow bucket with both lift coefficients outside it.
:width: 100%

Where the cruise and climb lift coefficients should sit on the polar. Schematic, after Gudmundsson (2022), Figure 8-71.
:::

:::{math}
:label: eq-design-cl
C_{L_C} = \frac{2W}{\rho V_C^{2} S} \qquad \text{at the start and at the end of cruise}
:::

Keep cruise and climb $C_l$ inside the drag bucket.

:::{admonition} Navy Jet Trainer
:class: navy

$W/S$ is the ASORT value. The design $C_L$ is provisional until the constraint diagram fixes the design point.
:::

## Airfoil selection

:::{table} Selection criteria and the requirement each one traces to.
:label: tbl-airfoil-criteria

| Criterion | Traces to |
| --- | --- |
| Design $C_l$ in the drag bucket | Cruise, climb |
| $C_{l_{max}}$, stall class | Stall and approach speed |
| $C_m$ | Trim drag, tail load |
| $t/c$ | Spar depth, fuel volume |
| $M_{dd}$, $Re$ range | Speed envelope |
| Surface sensitivity | Contamination, icing |

:::

:::{figure} figures/airfoil-comparison.svg
:label: fig-airfoil-comparison
:alt: Two plots comparing measured data for the NACA 65 2-415, solid, and the NACA 23015, dashed. Left, the drag polars with dotted lines at example cruise and climb lift coefficients of 0.3 and 0.7. At cruise, inside the drag bucket of the NACA 65 2-415, its drag coefficient is about 0.0043 against 0.0065 for the NACA 23015. At climb, the upper edge of the bucket, about 0.0054 against 0.0073. Above a lift coefficient of about 0.8 the NACA 23015 has the lower drag. Right, the lift curves: the NACA 23015 reaches the higher maximum lift coefficient, 1.69 against 1.62, then drops to 1.1 within 2 degrees; the NACA 65 2-415 rounds over and falls gradually.
:width: 100%

How two candidates are compared: at the lift coefficients you fly on the polar, and at $C_{l_{max}}$ on the lift curve. NACA 65$_2$-415 and NACA 23015 (NACA Report 824); values read from Gudmundsson (2022), Figure 8-74. The cruise and climb lift coefficients, 0.3 and 0.7, are examples.
:::

:::{admonition} Navy Jet Trainer
:class: navy

A04: at least three candidates with published data, every curve cited. Select one and justify the choice.
:::

### The comparison table

:::{table} Comparison table for three candidate airfoils A, B, and C. Score 1 for the best on a row, 0 for the worst, and interpolate linearly for the others. After Gudmundsson (2022), Table 8-13.
:label: tbl-airfoil-comparison

| Group | Parameter | Best is | A | B | C |
| --- | --- | --- | :---: | :---: | :---: |
| Stall | $C_{l_{max}}$ at the stall Reynolds number | highest | | | |
| Stall | Stall class | A | | | |
| Cruise | $C_{d_{min}}$ | lowest | | | |
| Cruise | $C_l$ at $C_{d_{min}}$ | near the cruise $C_l$ | | | |
| Cruise | $\lvert C_m \rvert$ at cruise | lowest | | | |
| Cruise | Sensitive to surface quality | no | | | |
| Climb | Climb and cruise $C_l$ inside the drag bucket | yes | | | |
| High speed | $M_{dd}$ at the design $C_l$ | highest | | | |
| General | Thickness ratio | highest | | | |

:::

:::{admonition} Navy Jet Trainer
:class: navy

A04: the rows and their weights are your criteria. Trace each one to a requirement.
:::

:::{seealso}
Continue with [](wing-geometry-and-lift.md): the planform, wing volume and height, aspect ratio, taper, sweep, twist, incidence, and the lift model. The references for both parts are at the end of that page.
:::
