---
title: "Constraint analysis, part 1: The master equation"
short_title: The master equation
---

This is the first part of Lecture 9, *Constraint Analysis and the Design Point*. The lecture has three parts: the method, the trainer boundaries and the design point, and two worked examples. This page derives the master equation and the boundaries it gives. The second part, [](trainer-boundaries.md), writes each RFP requirement as a boundary and shows how to select the design point. The third part, [](constraint-examples.md), works the Cessna 162 and the T-45C. The sources are Mattingly et al. (2002), Chapter 2; Gudmundsson (2022), Chapter 3; and MIL-STD-3013. The figures are redrawn after the figures on the slides.

:::{note} What to take from this lecture
- Every point requirement is a boundary in {term}`wing loading` and {term}`thrust-to-weight ratio`.
- One equation gives the boundaries in flight. The field lengths and the stall speed give the rest.
- The boundaries use the same inputs as the sizing code.
:::

## Requirements that become boundaries

:::{table} The RFP requirements that become boundaries. Every value comes from the RFP; T is the threshold, O the objective.
:label: tbl-constraint-requirements

| Item | Navy Jet Trainer |
| --- | --- |
| Speed | Maximum operating speed Mach 0.78 (T), Mach 0.90 (O) at 25,000 ft, at {term}`MTOW` less 50% fuel |
| Climb and maneuver | {term}`Specific excess power` 90 ft/s (T), 125 ft/s (O); sustained load factor +4.0 g (T), +6.0 g (O); both at 15,000 ft, at MTOW less 50% fuel |
| Field | Takeoff distance 5,000 ft and {term}`critical field length` 6,000 ft at MTOW; landing distance 5,000 ft at {term}`MLW`; all at 5,000 ft {term}`density altitude` |

:::

Each row gives boundaries on the diagram. The range and the endurance of the design missions are not on the diagram; they set the fuel in the mission analysis. A03 to A05 used provisional values of the wing loading and the thrust-to-weight ratio. Your team now selects them.

:::{admonition} Navy Jet Trainer
:class: navy

A requirement with a threshold and an objective gives two boundaries. How far apart are the two at your wing loading?
:::

## The constraint diagram

:::{prf:definition} Constraint diagram
:label: def-constraint-diagram

A {term}`constraint diagram` plots the thrust-to-weight ratio $T_{SL}/W_{TO}$ against the wing loading $W_{TO}/S$. $T_{SL}$ is the sea-level static thrust. $W_{TO}$ is the maximum takeoff weight, the MTOW of the RFP and $W_0$ in [Lecture 2](../lecture-02/weight-estimation.md). Each requirement value gives one boundary: a minimum $T_{SL}/W_{TO}$ or a maximum $W_{TO}/S$.
:::

:::{figure} figures/design-space.svg
:label: fig-design-space
:alt: Thrust-to-weight ratio against wing loading, on an invented scale. Requirement A is a curve that falls steeply at low wing loading, reaches a minimum, and rises slowly. Requirement B is a vertical line at a high wing loading. The region above the curve and left of the line is shaded and marked feasible region. Below the curve, requirement A is not met. Right of the line, requirement B is not met. A design point is marked inside the shaded region.
:width: 75%

Two boundaries close the feasible region. Schematic with invented values, after Mattingly et al. (2002), Figure 2.1.
:::

In {numref}`fig-design-space` two boundaries close the {term}`feasible region`, the part of the diagram that meets every requirement. Mattingly et al. call it the solution space. The boundaries that close the region are the {term}`active boundaries <active boundary>`. The {term}`design point` is chosen inside the region on weight, cost, and margin.

## The master equation

The {term}`master equation` follows from the energy of the aircraft in nine steps (Mattingly et al. 2002, Section 2.2). The symbols are Mattingly's.

### Steps 1 and 2: energy height

The potential energy $Wh$ plus the kinetic energy $\tfrac{1}{2}(W/g)V^{2}$, divided by the weight, is the {term}`energy height`:

:::{math}
:label: eq-energy-height
z_e = h + \frac{V^{2}}{2g}
:::

It is the altitude the aircraft would reach if all its kinetic energy became altitude. Its rate of change is

:::{math}
:label: eq-energy-rate
\frac{dz_e}{dt} = \frac{dh}{dt} + \frac{V}{g}\frac{dV}{dt}
:::

:::{figure} figures/energy-height.svg
:label: fig-energy-height
:alt: Altitude against true airspeed with five curves of constant energy height, from 10,000 to 50,000 feet. Each curve starts at its energy height at zero speed and falls as speed rises. An aircraft is marked at 1,134 feet per second and 20,000 feet, on the 40,000 foot curve. A vertical arrow shows a climb and a horizontal arrow an acceleration; both cross to higher curves. A dashed arrow runs along the 40,000 foot curve toward lower speed and higher altitude: speed traded for altitude at constant energy height.
:width: 80%

Lines of constant energy height, $h = z_e - V^{2}/2g$. Computed; after Mattingly et al. (2002), Figure 2.5.
:::

Climbing and accelerating cross the lines. Moving along one line trades speed for altitude.

### Steps 3 and 4: forces on the path

:::{figure} figures/path-forces.svg
:label: fig-path-forces
:alt: A jet trainer climbing to the right on a flight path inclined at the angle gamma above the horizontal. Thrust T acts forward along the path, drag D backward along the path, lift L normal to the path, and weight W straight down. Dotted lines split the weight into W cosine gamma normal to the path and W sine gamma along it. The velocity V points along the path.
:width: 65%

The forces on an aircraft that climbs along a path inclined at $\gamma$. Schematic.
:::

Step 3 is Newton's law along the path, with the mass $W/g$:

:::{math}
:label: eq-newton-path
T - D - W\sin\gamma = \frac{W}{g}\frac{dV}{dt}
:::

Step 4 multiplies by $V$ and divides by $W$. With $V\sin\gamma = dh/dt$, the right side becomes {eq}`eq-energy-rate`:

:::{math}
:label: eq-specific-excess-power
\frac{(T - D)\,V}{W} = \frac{dh}{dt} + \frac{V}{g}\frac{dV}{dt} = \frac{dz_e}{dt} \equiv P_s
:::

$P_s$ is the {term}`specific excess power`, the excess power per unit weight, in ft/s. With $P_s > 0$ the aircraft climbs or accelerates. With $P_s = 0$ it cruises or holds a sustained turn. Lift does no work along the path. It enters through the drag in step 8. The equations are Mattingly et al. (2002), Eqs. 2.1a, 2.2a, and 2.2b.

:::{admonition} Navy Jet Trainer
:class: navy

The RFP's 90 ft/s (T) and 125 ft/s (O) at 15,000 ft are values of $P_s$. Does the RFP state the speed for them?
:::

### Steps 5 to 9: the boundary

5. Solve {eq}`eq-specific-excess-power` for the thrust: $T/W = D/W + P_s/V$.
6. Write $T = \alpha\,T_{SL}$ and $W = \beta\,W_{TO}$. Then $T_{SL}/W_{TO} = (\beta/\alpha)\,[D/W + P_s/V]$.
7. At the load factor $n$ and the dynamic pressure $q$, the lift is $L = nW = qC_LS$. Then $C_L = n\beta\,(W_{TO}/S)/q$.
8. With the drag polar $C_D = K_1C_L^{2} + K_2C_L + C_{D_0} + C_{D_R}$, the drag is $D/W = qC_D/[\beta\,(W_{TO}/S)]$.
9. Put step 7 into step 8, and step 8 into step 6.

:::{math}
:label: eq-master
\frac{T_{SL}}{W_{TO}} = \frac{\beta}{\alpha}\left\{\frac{q}{\beta\,(W_{TO}/S)}\left[K_1\left(\frac{n\beta}{q}\frac{W_{TO}}{S}\right)^{2} + K_2\left(\frac{n\beta}{q}\frac{W_{TO}}{S}\right) + C_{D_0} + C_{D_R}\right] + \frac{P_s}{V}\right\}
:::

This is the master equation (Mattingly et al. 2002, Eqs. 2.3 to 2.11).

- $\alpha$ is the installed {term}`thrust lapse` at the condition, $T/T_{SL}$ in [Lecture 8](../lecture-08/engine-models.md). $T_{SL}/W_{TO}$ is the $(T/W)_{TO}$ of that lecture.
- $\beta = W/W_{TO}$ is the weight at the condition as a fraction of the takeoff weight.
- $C_{D_R}$ is the drag coefficient of the landing gear, the flaps, and the stores.
- The polar of [Lecture 7](../lecture-07/drag-polar.md) with $C_{L_{minD}}$ = 0 has $K_1 = K$ and $K_2 = 0$.

:::{figure} figures/equation-flow.svg
:label: fig-equation-flow
:alt: A flow diagram. Four inputs on the left feed the master equation in the middle. The engine deck gives alpha. The mission weight gives beta. The RFP condition gives q, n, specific excess power, and V. The drag polar gives K1, K2, CD0, and CDR. The master equation returns the thrust-to-weight ratio at each wing loading. On the right, the result is one boundary, a curve against wing loading.
:width: 85%

One condition gives one boundary. Schematic.
:::

## Where each term comes from

:::{table} The inputs of the master equation and the rule for each.
:label: tbl-constraint-terms

| Term | Source in this course | Rule |
| --- | --- | --- |
| $C_{D_0}$, $K_1$ | [Lecture 7](../lecture-07/parasite-drag.md); the polar of each configuration, A04 Deliverable 5 | Clean for cruise and maneuver; gear and flaps through $C_{D_R}$; compressibility drag at Mach 0.78 and Mach 0.90 |
| $\alpha$ | [Lecture 8](../lecture-08/engine-models.md); the installed {term}`engine deck` of A05 | Installed, at the altitude, speed, day, and {term}`rating` of the condition |
| $\beta$ | [Lecture 2](../lecture-02/design-missions.md); the mission analysis of A03; the weight the RFP states for the condition | MTOW less 50% fuel for the point requirements; 1.0 at takeoff; MLW over MTOW at landing |
| $C_{L_{max}}$ | [Lecture 6](../lecture-06/high-lift-wing-and-field.md); A04 Deliverable 3 | The takeoff and landing configurations |
| $AR$, $e$ | [Lecture 5](../lecture-05/wing-geometry-and-lift.md); A04 | The same values as the sizing code |

:::

:::{admonition} Navy Jet Trainer
:class: navy

Take every term from {term}`ASORT`. Are the values in your constraint code the values the sizing code uses?
:::

## The cases

Each condition sets $P_s$, $n$, the altitude, and the speed. The master equation then reduces to one of these forms, written here with $K_2 = 0$, $C_{D_R} = 0$, and $W/S$ for $W_{TO}/S$.

:::{table} The cases of the master equation. Mattingly et al. (2002), Cases 1 to 4, 8, and 9; Gudmundsson (2022), Eqs. 3-2, 3-7, 3-10, and 3-11.
:label: tbl-constraint-cases

| Condition | Set | $T_{SL}/W_{TO}$ reduces to | Shape |
| --- | --- | --- | --- |
| Cruise, maximum speed | $P_s = 0$, $n = 1$ | $\dfrac{\beta}{\alpha}\left[\dfrac{q\,C_{D_0}}{\beta\,W/S} + \dfrac{K_1\beta}{q}\dfrac{W}{S}\right]$ | A curve with its minimum at $\dfrac{W}{S} = \dfrac{q}{\beta}\sqrt{\dfrac{C_{D_0}}{K_1}}$ |
| Climb at constant speed | $P_s = dh/dt$, $n = 1$ | The cruise form plus $\dfrac{\beta}{\alpha}\dfrac{1}{V}\dfrac{dh}{dt}$ | The curve, shifted up |
| Sustained turn | $P_s = 0$, $n > 1$ | The cruise form with $K_1 n^{2}$ | The curve, steeper on the right |
| Acceleration | $P_s = \dfrac{V}{g}\dfrac{\Delta V}{\Delta t}$, $n = 1$ | The cruise form plus $\dfrac{\beta}{\alpha}\dfrac{1}{g}\dfrac{\Delta V}{\Delta t}$ | The curve, shifted up |
| Takeoff climb gradient | $\gamma$ at $C_L = C_{L_{max}}/k_{TO}^{2}$ | $\dfrac{\beta}{\alpha}\left[\sin\gamma + \dfrac{C_D}{C_L}\right]$ | A horizontal line |

:::

The minimum of the cruise curve lies at the wing loading that puts the aircraft at the $C_L$ of best $L/D$ at that $q$ (Gudmundsson 2022, Eq. 3-8). The service ceiling is the climb form at 100 ft/min and the density of the ceiling. Each condition has its own $q$, $\alpha$, and $\beta$. The next section defines $k_{TO}$.

:::{iframe} ../quickcheck/boundary-point.html
:label: qc-boundary-point
:width: 100%

Quick check: one point on a cruise boundary and on a turn boundary, from {numref}`tbl-constraint-cases`. Shuffle gives new values; the solution shows the steps.
:::

## Field and stall boundaries

The takeoff ground run $s_G$, $S_G$ in [Lecture 6](../lecture-06/high-lift-wing-and-field.md), gives a line through the origin when the thrust is much larger than the drag and the rolling friction (Mattingly et al. 2002, Case 5):

:::{math}
:label: eq-takeoff-boundary
\frac{T_{SL}}{W_{TO}} = \frac{\beta^{2}\,k_{TO}^{2}}{\alpha\,\rho\,g\,s_G\,C_{L_{max}}}\;\frac{W_{TO}}{S}
:::

The line is steeper at a higher weight. It is flatter at a higher density, a longer ground run, and a higher $C_{L_{max}}$.

The braking roll $s_B$, $S_{BR}$ in [Lecture 6](../lecture-06/high-lift-wing-and-field.md), gives a vertical line that does not depend on the thrust. This form has no reverse thrust and a constant deceleration $\mu_B\,g$:

:::{math}
:label: eq-landing-boundary
\frac{W_{TO}}{S} \le \frac{\rho\,g\,\mu_B\,C_{L_{max}}\,s_B}{\beta\,k_{TD}^{2}}
:::

A required stall speed $V_S$ at the weight $\beta\,W_{TO}$ gives a vertical line for each configuration:

:::{math}
:label: eq-stall-boundary
\frac{W_{TO}}{S} \le \frac{\rho\,V_S^{2}\,C_{L_{max}}}{2\,\beta}
:::

- $k_{TO} = V_{LOF}/V_S$ is the liftoff speed over the stall speed in the takeoff configuration.
- $k_{TD} = V_{TD}/V_S$ is the touchdown speed over the stall speed in the landing configuration.
- $\mu_B$ is the braking friction coefficient.

Both speed factors compare calibrated airspeeds at the same weight. The 2003 issue of MIL-STD-3013 gives 1.10 for each; see the reference speeds of [Lecture 6](../lecture-06/high-lift-wing-and-field.md), and confirm them against revision B. For a similar aircraft, the flight manual gives the liftoff speed, the touchdown speed, and the stall speed. Their ratios are $k_{TO}$ and $k_{TD}$. The T-45C example of [part 3](constraint-examples.md) takes $k_{TD}$ this way.

The sources are MIL-STD-3013 (2003), Sections 3.2 and 3.8; Gudmundsson (2022), Eqs. 3-1, 3-13, and 3-18; and Mattingly et al. (2002), Cases 5 to 7.

## Normalizing to sea-level static

Every boundary is drawn in $T_{SL}$ and $W_{TO}$, whatever its condition:

- Divide the thrust at the condition by $\alpha$ at that altitude, Mach number, and rating. The result is $T_{SL}$.
- Divide the weight at the condition by $\beta$. The result is $W_{TO}$.
- Use the density of the condition. The field requirements are at 5,000 ft density altitude.
- A lower density lowers $\alpha$ and moves the landing and stall boundaries to the left. It steepens the takeoff line through $\rho$ in {eq}`eq-takeoff-boundary`.

:::{admonition} Navy Jet Trainer
:class: navy

The RFP requires the International Standard Atmosphere for all calculations. Which rating does each of your conditions use, and how does MIL-STD-3013B define it?
:::

## The shape of the diagram

:::{figure} figures/diagram-shape.svg
:label: fig-diagram-shape
:alt: Thrust-to-weight ratio against wing loading, on an invented scale, with six boundaries. Cruise and turn are curves with a minimum; the turn curve lies above the cruise curve and rises faster to the right. Takeoff is a straight line through the origin. The climb gradient is a horizontal line. Landing and stall are vertical lines, landing to the left of stall. The feasible region is shaded: above the turn curve at low wing loading, above the takeoff line at higher wing loading, and left of the landing line.
:width: 85%

The shape of each kind of boundary. Schematic with invented values.
:::

- Cruise and turn are curves with a minimum.
- Takeoff is a line through the origin.
- Landing and stall are vertical lines. The thrust does not move them. They move with $C_{L_{max}}$, $\beta$, and the density, and the landing line also with $k_{TD}$ and $\mu_B$.
- The climb gradient is a horizontal line.

The feasible region is above the highest boundary and left of the leftmost vertical one.

## Reading the diagram

The requirements of the active boundaries are the driving requirements. The other boundaries have more margin. A driving requirement that your team derived can be renegotiated: state what relaxing it gains. For a requirement trade, change one requirement, such as the field length, and report how far its boundary moves. Plot the A02 cohort on the same axes.

Check five things before you trust a boundary:

1. The $AR$, the sweep, and $e$ are those of the sizing code.
2. $\alpha$ comes from the installed deck at the condition.
3. $\beta$ is the weight the RFP states for that condition.
4. $C_{L_{max}}$ is that of the configuration flown.
5. The day is the day the RFP states.

Record the altitude, the atmosphere, and the weight with each boundary.

:::{admonition} Navy Jet Trainer
:class: navy

The RFP asks for design or cost trade studies between the threshold and the objective requirements. Which boundary does each trade move, and how far?
:::

:::{seealso}
Continue with [](trainer-boundaries.md): the trainer's boundaries, the threshold and the objective, and the choice of the design point. The references for the three parts are at the end of [](constraint-examples.md).
:::
