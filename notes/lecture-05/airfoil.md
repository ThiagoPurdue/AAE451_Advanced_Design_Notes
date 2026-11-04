---
title: "Aerodynamics, part 1: The airfoil"
short_title: The airfoil
---

This is the first part of Lecture 5, *Aerodynamics: Airfoil and Wing*. It covers what the RFP asks of the wing and how an airfoil is read and chosen: the families, the airfoil data, the Reynolds and Mach effects, the stall classes, and the comparison that ends in a selection. The second part, [](wing-geometry-and-lift.md), covers the planform and the lift model. The lecture follows Gudmundsson (2022), Chapters 8 and 9 and Section 16.3.3, and Nicolai and Carichner (2010), Chapter 2.

:::{note} What to take from this lecture
- Every wing choice traces to a requirement: speed, field length, maneuver, or low speed.
- Airfoil data come from published curves. An AI tool does not produce them.
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

:::{figure} figures/wing-planform.svg
:label: fig-wing-planform
:alt: Top view of a tapered, swept wing. Arrows mark the span b across both halves, the root chord at the centerline, the tip chord at the right tip, the leading-edge sweep angle at the root, and on the right half the mean geometric chord drawn as a thick bar at the spanwise station y MGC, with its leading edge set back by x MGC. A dashed line runs along the quarter chord.
:width: 90%

Wing planform nomenclature. The quantities the lecture uses: span $b$, root and tip chords $c_r$ and $c_t$, leading-edge sweep $\Lambda_{LE}$, and the {term}`mean geometric chord` $c_{MGC}$ at its station $y_{MGC}$. Drawn with example values, $AR$ = 6, $\lambda$ = 0.4, $\Lambda_{LE}$ = 25°.
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

Three NACA airfoils computed from the published shape equations. The 4-digit and 5-digit numbers encode camber and thickness; the 6-series and the newer laminar and supercritical families are defined by their pressure distributions and have no simple formula.
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

A04 accepts only cited, published data. Start with NACA Report 824 and Gudmundsson (2022), Table 8-10. A polar produced by an AI tool is not data.
:::

## Reading airfoil data

:::{figure} figures/section-data-schematic.svg
:label: fig-section-data
:alt: Two schematic plots. Left, section lift coefficient against angle of attack: a straight line through the zero-lift angle, marked, with its slope labeled, bending over to a maximum lift coefficient at the stall angle, marked, then falling. Right, section lift coefficient against drag coefficient: a polar with its minimum drag marked at a lift coefficient of about 0.3 and a shaded band labeled low-drag range, the drag bucket, around it.
:width: 100%

What to read from an airfoil's lift curve and drag polar. Schematic curves; the labels are what matter.
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

Trends from Gudmundsson (2022), Table 8-4.

## Reynolds number

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
:alt: Three schematic lift curves. Class A rounds over gently past its peak. Class B peaks sharply and falls at a moderate rate. Class C rises to a peak and drops suddenly.
:width: 100%

The three stall classes as schematic lift curves. Class A: separation grows forward from the trailing edge. Class C: a leading-edge separation bubble bursts. Class B lies between them. After Gudmundsson (2022), Figure 8-72.
:::

:::{admonition} Navy Jet Trainer
:class: navy

Decide whether "basic maneuvers" include stalls. Stall class is a selection criterion either way.
:::

## Compressibility

:::{figure} figures/drag-divergence.svg
:label: fig-drag-divergence
:alt: Section drag coefficient against Mach number, schematic. The curve is flat at the incompressible level, then rises steeply above about Mach 0.75. A dashed vertical line marks the critical Mach number. A marker on the curve shows the Boeing definition of drag divergence, where the drag is 0.002 above the incompressible level, and a second marker further along shows the Douglas definition, where the slope reaches 0.10 per unit Mach.
:width: 75%

Drag rise with Mach number, schematic, with the two common definitions of the {term}`drag divergence Mach number`.
:::

- $M_{crit}$, the {term}`critical Mach number`: the first sonic point on the airfoil.
- $M_{dd}$: drag divergence. Boeing: $C_d$ 0.002 above the incompressible level. Douglas: $dC_d/dM = 0.10$.
- The Korn relation for an airfoil:

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

- A flatter upper surface gives a weaker shock and less separation.
- Aft camber recovers the lift and adds nose-down $C_m$.
- At the same $t/c$, a higher $M_{dd}$. At the same $M_{dd}$, a thicker and lighter wing.

Nicolai and Carichner (2010), Figures 2.19 and 2.22, show the flow over a conventional and a supercritical airfoil through the transonic range.

## Design lift coefficient and the drag bucket

:::{math}
:label: eq-design-cl
C_{L_C} = \frac{2W}{\rho V_C^{2} S} \qquad \text{at the start and at the end of cruise}
:::

Keep cruise and climb $C_l$ inside the drag bucket of {numref}`fig-section-data`.

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
Continue with [](wing-geometry-and-lift.md): the planform, wing volume and height, aspect ratio, taper, sweep, twist, incidence, and the lift model.
:::
