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
:alt: Three airfoil outlines side by side with their camber lines dashed. NACA 0012, symmetric and 12 percent thick, has a straight camber line. NACA 2412 has a gently arched camber line with its peak at 40 percent of the chord. NACA 23012 has its camber concentrated near the leading edge, at 15 percent of the chord.
:width: 100%

Three NACA airfoils computed from the published shape equations. The 4-digit and 5-digit numbers encode camber and thickness; the 6-series and the newer laminar and supercritical families are defined by their pressure distributions and have no simple formula. Gudmundsson (2022), Figure 8-39, shows the measured lift curves and polars of five such airfoils from NACA Report 824.
:::

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
:alt: Two schematic plots. Left, section lift coefficient against angle of attack: a straight line through the zero-lift angle, marked, with its linear range and slope labeled, bending over to the maximum lift coefficient at the stall angle, marked, then falling. Right, section lift coefficient against drag coefficient: a polar with its minimum drag marked at a lift coefficient of about 0.3 and a shaded band labeled drag bucket, the low-drag range, around it.
:width: 100%

What to read from an airfoil's lift curve and drag polar. Schematic, after Gudmundsson (2022), Figure 8-5, which shows the measured NACA 4415 data from NACA Report 824.
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
:alt: Left, lift coefficient against angle of attack for a cambered airfoil, solid, and a symmetric airfoil, dashed. The cambered curve is shifted up and to the left, crosses zero lift at a negative angle, marked alpha ZL, and reaches a higher maximum lift coefficient. Right, the drag polars: the cambered airfoil's polar is shifted to a higher lift coefficient, so its low-drag range sits at a positive lift coefficient.
:width: 100%

The effect of camber on the lift curve and the drag polar. Schematic, after Gudmundsson (2022), Figure 8-54; trends from Table 8-4.
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

Candidates must be credible at the maximum operating Mach number of the RFP. Which published data sets reach it?
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

Decide whether "basic maneuvers" include stalls. Stall class is a selection criterion either way.
:::

## Compressibility

:::{figure} figures/mach-effects.svg
:label: fig-mach-effects
:alt: Left, lift coefficient against angle of attack at Mach 0.2, 0.6, 0.7, and 0.8: the slope steepens with Mach number, and at 0.7 and 0.8 the curves peak lower and earlier. Right, section drag coefficient against Mach number: flat at the incompressible level, then rising steeply. A dashed vertical line marks the critical Mach number at the start of the rise; a marker shows the Boeing definition of drag divergence, where the drag is 0.002 above the incompressible level, and a second marker further along shows the Douglas definition, where the slope reaches 0.10 per unit Mach.
:width: 100%

Mach number effects on the lift curve and the drag coefficient, with the critical and drag divergence Mach numbers. Schematic, after Gudmundsson (2022), Figure 8-67.
:::

- $M_{crit}$, the {term}`critical Mach number`: the first sonic point on the airfoil.
- $M_{dd}$, the {term}`drag divergence Mach number`. Boeing: $C_d$ 0.002 above the incompressible level. Douglas: $dC_d/dM = 0.10$.
- The Korn relation for an airfoil (Gudmundsson 2022, Eq. 8-67):

:::{math}
:label: eq-korn-section
M_{dd} = \kappa - \frac{t}{c} - 0.1\,C_l, \qquad \kappa = 0.87 \text{ conventional}, \ 0.95 \text{ supercritical}
:::

- To raise $M_{crit}$: lower $t/c$, sweep, lower $AR$. A supercritical airfoil raises $M_{dd}$ only.

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
:alt: Two columns. Left, a conventional airfoil at Mach 0.72 with a strong shock on the upper surface and separated flow behind it; below it, the pressure coefficient along the chord, upper surface solid and lower surface dashed, with a sharp jump at the shock near mid-chord. Right, a supercritical airfoil at Mach 0.80, flatter on top, with a weak shock far aft; below it, a flat pressure plateau on the upper surface, a small step at the shock, and aft loading from the lower surface near the trailing edge.
:width: 90%

A conventional and a supercritical airfoil at the same lift coefficient. Schematic, after Nicolai and Carichner (2010), Figure 2.22.
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
:alt: Two schematic plots comparing candidate A, solid, and candidate B, dashed. Left, the drag polars with horizontal dotted lines at the cruise and climb lift coefficients: candidate A has the lower drag at both. Right, the lift curves: candidate B reaches the higher maximum lift coefficient and stalls more sharply.
:width: 100%

How two candidates are compared: at the lift coefficients you fly on the polar, and at $C_{l_{max}}$ on the lift curve. Schematic; Gudmundsson (2022), Figure 8-74, shows the comparison with measured data for NACA 23015 and 65$_2$-415.
:::

:::{admonition} Navy Jet Trainer
:class: navy

A04: at least three candidates with published data, every curve cited. Select one and justify the choice.
:::

### The comparison table

:::{table} Comparison table for three candidate airfoils A, B, and C. Score 1 for the best on a row, 0 for the worst, and prorate the others. After Gudmundsson (2022), Table 8-13.
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
