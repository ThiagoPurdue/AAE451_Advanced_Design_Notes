---
title: "Constraint analysis, part 2: The trainer boundaries and the design point"
short_title: The trainer boundaries and the design point
---

This is the second part of Lecture 9, *Constraint Analysis and the Design Point*. It writes each RFP requirement as a boundary with the equations of [](constraint-method.md): the maximum operating speed, the specific excess power, the sustained load factor, and the field lengths. It then compares the threshold and the objective, shows how to select the design point, and closes the loop with the sizing code. The figures are redrawn after the figures on the slides.

:::{note} What to take from this lecture
- The trainer's point requirements set the thrust at altitude. Each has a threshold boundary and an objective boundary.
- The RFP states no speed for the specific excess power and the sustained load factor. The team chooses the speed and states its source.
- The design point is chosen inside the feasible region with stated margins, and the sizing code is run again at that point.
:::

## The RFP requirements as boundaries

:::{table} The RFP requirements as cases. Threshold value first, objective second.
:label: tbl-trainer-conditions

| RFP requirement | Case | Weight | $n$ | $P_s$ (ft/s) | $\alpha$ and $q$ at |
| --- | --- | --- | ---: | ---: | --- |
| Mach 0.78 and 0.90 at 25,000 ft | Maximum speed | MTOW less 50% fuel | 1 | 0 | Mach 0.78 and Mach 0.90 |
| $P_s$ 90 and 125 ft/s at 15,000 ft | Climb, acceleration | MTOW less 50% fuel | 1 | 90 and 125 | A speed the RFP does not state |
| +4.0 g and +6.0 g at 15,000 ft | Sustained turn | MTOW less 50% fuel | 4 and 6 | 0 | A speed the RFP does not state |
| Takeoff distance 5,000 ft; critical field length 6,000 ft | Takeoff; critical field length | MTOW | 1 | none | 5,000 ft density altitude |
| Landing distance 5,000 ft | Landing | MLW | 1 | none | 5,000 ft density altitude |

:::

$\beta$ follows from the weight: MTOW less 50% fuel from your A03 mission analysis, 1.0 at takeoff, and MLW over MTOW at landing. The MLW is your team's definition; see [Lecture 2](../lecture-02/design-missions.md). State the rating at each condition. The equations of this page write $W/S$ for $W_{TO}/S$.

:::{admonition} Navy Jet Trainer
:class: navy

The RFP requires the standard atmosphere. How do you convert the 5,000 ft {term}`density altitude` to the pressure altitude and the temperature that the engine deck uses?
:::

## Maximum operating speed at 25,000 ft

The maximum operating speed is the cruise case of [part 1](constraint-method.md), with the compressibility drag added to the parasite term:

:::{math}
:label: eq-max-mach-boundary
\frac{T_{SL}}{W_{TO}} = \frac{\beta}{\alpha}\left[\frac{q\,(C_{D_0} + C_{D_c})}{\beta\,W/S} + \frac{K_1\beta}{q}\frac{W}{S}\right]
:::

$C_{D_c}$ is the compressibility drag at the Mach number of the condition, from the drag-rise curve of [Lecture 7](../lecture-07/drag-polar.md). Check it at Mach 0.90, where it is large. $\alpha$ differs between Mach 0.78 and Mach 0.90; see [Lecture 8](../lecture-08/engine-models.md). $q$ is large at 25,000 ft. The parasite term dominates, and the boundary falls as the wing loading rises over the range of the cohort.

The threshold and the objective give two boundaries. Their gap at your wing loading is the thrust that the objective costs.

This boundary moves with:

- The thickness ratio and the sweep, through $C_{D_c}$; see [Lecture 5](../lecture-05/wing-geometry-and-lift.md).
- The engine class, through $\alpha$ against Mach number.
- The weight at MTOW less 50% fuel, through $\beta^{2}$ in the induced term.

:::{admonition} Navy Jet Trainer
:class: navy

How much thrust does the objective, Mach 0.90, cost over the threshold, Mach 0.78, at your wing loading?
:::

## Specific excess power at 15,000 ft

With $n = 1$ and the required $P_s$, the master equation gives

:::{math}
:label: eq-ps-boundary
\frac{T_{SL}}{W_{TO}} = \frac{\beta}{\alpha}\left[\frac{q\,C_{D_0}}{\beta\,W/S} + \frac{K_1\beta}{q}\frac{W}{S} + \frac{P_s}{V}\right]
:::

$P_s$ is 90 ft/s (T) or 125 ft/s (O), at 15,000 ft and MTOW less 50% fuel. The RFP states no speed, and the thrust required depends on the speed through $q$, $\alpha$, and $P_s/V$. Vary the Mach number at 15,000 ft, and plot the required $T_{SL}/W_{TO}$ against Mach number, one line for each wing loading.

The requirement can be read in two ways:

- At one stated speed. The requirement then gives one boundary.
- Over a band of speeds. The boundary is then the highest required $T_{SL}/W_{TO}$ in the band.

Record the reading, the speed or the band, and the source in ASORT. MIL-STD-3013 defines the conditions for $P_s$, and the RFP refers to it. These notes use the 2003 issue; confirm against revision B.

:::{admonition} Navy Jet Trainer
:class: navy

The specific excess power and the sustained load factor set the thrust class of the trainer; see [Lecture 2](../lecture-02/design-missions.md). Plot both at the threshold and at the objective. Which reading gives the higher boundary?
:::

## Sustained load factor at 15,000 ft

The sustained turn is the cruise form with the induced term multiplied by $n^{2}$:

:::{math}
:label: eq-turn-boundary
\frac{T_{SL}}{W_{TO}} = \frac{\beta}{\alpha}\left[\frac{q\,C_{D_0}}{\beta\,W/S} + \frac{K_1 n^{2}\beta}{q}\frac{W}{S}\right], \qquad n = 4.0 \ \text{or}\ 6.0
:::

At 6 g the induced term is 2.25 times its value at 4 g. The turn uses $C_L = n\beta\,(W/S)/q$, and this $C_L$ must stay below the usable $C_{L_{max}}$ at the Mach number of the turn. Where $C_L$ reaches that limit, the turn is limited by lift, and the limit is a vertical boundary at that wing loading.

This boundary moves with (Mattingly et al. 2002, Case 3):

- The aspect ratio and the span efficiency, through $K_1$.
- The weight at MTOW less 50% fuel, through $\beta^{2}$.
- The speed chosen for the turn, through $q$.

:::{admonition} Navy Jet Trainer
:class: navy

Compare the thrust required for +4.0 g and for +6.0 g. Is either turn limited by lift at your wing loading?
:::

## Field lengths at 5,000 ft density altitude

The takeoff distance and the critical field length give boundaries in $T_{SL}/W_{TO}$. The landing distance gives a limit on $W_{TO}/S$.

**Takeoff distance, 5,000 ft at MTOW.** The ground run gives the takeoff boundary of [part 1](constraint-method.md), {eq}`eq-takeoff-boundary`. If the MIL-STD-3013B distance you use runs to the obstacle, add the rotation, the transition, and the climb. Use $\alpha$ at the takeoff condition and $C_{L_{max}}$ in the takeoff configuration.

**Critical field length, 6,000 ft.** The aircraft accelerates to the engine-failure speed, then stops or continues. Which distance governs depends on the number of engines. The stop is the braking roll of Mattingly et al. (2002), Case 7.

**Landing distance, 5,000 ft at MLW.** The braking roll gives the landing boundary of part 1, {eq}`eq-landing-boundary`, a vertical line. If the distance you use starts at the obstacle, add the air distance at your approach speed. [Lecture 6](../lecture-06/high-lift-wing-and-field.md) covers the reference speeds and the {term}`FCLP` approach.

**Density ratio.** $\sigma$ is 0.862 at 5,000 ft density altitude. It enters the slope of the takeoff boundary and the stall speed. The thrust lapse needs the pressure and the temperature; in the standard atmosphere they are those of 5,000 ft.

:::{admonition} Navy Jet Trainer
:class: navy

The RFP says "takeoff distance" and "landing distance." Which MIL-STD-3013B distance do you use for each? Which method gives the critical field length with your number of engines?
:::

## Example: a fighter constraint diagram

:::{figure} figures/fighter-diagram.svg
:label: fig-fighter-diagram
:alt: Thrust-to-weight ratio against wing loading, on an invented scale, with eight boundaries. Maximum speed, dash, turn, acceleration, and ceiling are curves with a minimum. One-engine climb is a horizontal line. Takeoff is a line through the origin. Landing is a vertical line. The feasible region is shaded. It lies above the acceleration curve at low wing loading, above the turn curve in the middle, above the takeoff line at high wing loading, and left of the landing line. The ceiling, maximum speed, dash, and one-engine climb boundaries lie below the region. Three cohort aircraft are marked inside it.
:width: 90%

A constraint diagram of a fighter, with one boundary for each of eight requirements. Schematic with invented values.
:::

In {numref}`fig-fighter-diagram`, acceleration, turn, takeoff, and landing close the region. Ceiling, maximum speed, dash, and one-engine climb have margin. The cohort aircraft on the same axes check the inputs.

## Threshold and objective

The maximum operating speed, the specific excess power, and the sustained load factor each carry two values, and each gives two boundaries. The objective values shrink the region. The difference in $T_{SL}/W_{TO}$ at the design point is the added thrust, and a larger engine costs weight and money; see the thrust sizing and the scaling in [Lecture 8](../lecture-08/engine-models.md). The design point may meet the objective of one requirement and the threshold of another. State which, and why.

Report the trade in four items:

1. The feasible region at the threshold and at the objective, on one diagram.
2. The design point under each.
3. The engine, the weight, and the cost that each implies, from the sizing code.
4. The objective values met at the design point.

:::{admonition} Navy Jet Trainer
:class: navy

Which objective does your team give up first, and what does that save?
:::

## Choosing the design point

:::{prf:definition} Design point
:label: def-design-point

The {term}`design point` is the wing loading $W_{TO}/S$ and the thrust-to-weight ratio $T_{SL}/W_{TO}$ selected for the aircraft, inside the feasible region.
:::

:::{figure} figures/design-point.svg
:label: fig-design-point
:alt: Thrust-to-weight ratio against wing loading, on an invented scale. The boundaries are maximum speed, acceleration, turn, takeoff, and a vertical landing line. The feasible region is shaded above the turn curve and the takeoff line and left of the landing line. A design point is marked inside the region. One arrow, labeled margin, runs from the point down to the turn curve. A second arrow, labeled margin, runs from the point right to the landing line.
:width: 85%

The design point and its margins to the active boundaries. Schematic with invented values, after Mattingly et al. (2002), Figure 2.E3, a fighter.
:::

The lowest $T_{SL}/W_{TO}$ gives the smallest engine, and the highest $W_{TO}/S$ gives the smallest wing. The landing boundary usually sets the highest wing loading. The margin to the active boundaries covers the uncertainty in $C_{D_0}$, $C_{L_{max}}$, and $\alpha$. In {numref}`fig-design-point`, landing, takeoff, and turn close the region near the design point. The source is Mattingly et al. (2002), Section 2.4.2.

:::{admonition} Navy Jet Trainer
:class: navy

State the design point, the active boundaries, and the margin to each. Which input has an uncertainty larger than the margin?
:::

## Rubber engine and fixed engine

With a {term}`rubber engine`:

- The thrust is $T_{SL} = (T_{SL}/W_{TO})\,W_{TO}$ at the design point. The weight and the size scale from the reference engine with the relations of [Lecture 8](../lecture-08/engine-models.md).
- The design point can be anywhere inside the region.
- The report states the reference engine and the scale factor.

With a {term}`fixed engine`:

- $T_{SL}$ is the published value of the A05 engine. As $W_{TO}$ changes in the sizing loop, the available $T_{SL}/W_{TO}$ changes.
- The available $T_{SL}/W_{TO}$ must exceed the highest boundary at the design wing loading. If it does not, the options are a larger wing, less weight, or another engine.

:::{admonition} Navy Jet Trainer
:class: navy

With a fixed engine, how far is your available $T_{SL}/W_{TO}$ above the highest boundary?
:::

## Closing the loop with the sizing code

1. Enter $W_{TO}/S$ and $T_{SL}/W_{TO}$ in ASORT.
2. Run the sizing code again. It returns $S$, $T_{SL}$, the weights, and a new $\beta$ for each condition.
3. Redraw the boundaries with the new $\beta$, the A04 geometry at the new $S$, and the A05 deck at the new thrust.
4. Repeat until the design point and the weights no longer change.
5. Record the active boundaries and the margin to each.

For the sensitivity, change one input at a time: $C_{D_0}$, $K_1$, $C_{L_{max}}$, $\alpha$, and $\beta$. Report which boundary moves and how far. Refine first the input whose uncertainty exceeds the margin.

The design point sets:

- The wing area and the A04 geometry.
- The engine thrust and the A05 selection.
- The starting point of the performance analysis and of the carpet plots.

The source is Mattingly et al. (2002), Section 2.4.2.

:::{seealso}
Continue with [](constraint-examples.md): the Cessna 162 and the T-45C worked through, and the work for the week. The references for the three parts are at the end of that page.
:::
