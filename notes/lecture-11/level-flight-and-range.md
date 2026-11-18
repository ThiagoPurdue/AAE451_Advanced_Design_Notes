---
title: "Performance, part 1: Level flight, range, and endurance"
short_title: Level flight and range
---

This is the first part of Lecture 11, *Performance Assessment*. The lecture has three parts: level flight and range, climb and field performance, and maneuver and the V-n diagram. This page states what the RFP asks, writes the equations of motion, and covers the level-flight speeds, range and endurance, and the segment table. The second part is [](climb-and-field.md) and the third is [](maneuver-and-vn.md).

The worked numbers come from published examples: the Learjet 45 of Gudmundsson (2022), Chapters 17 to 23, and the Air-to-Air Fighter of Mattingly et al. (2002). No number on these pages is computed for the Navy Jet Trainer.

:::{note} What to take from this lecture
- Performance is the check on the sizing: every RFP requirement is computed at its own weight, altitude, and day, with the polar, the engine deck, and the weights of the sizing code.
- Three optimum lift coefficients give the speeds for minimum drag, minimum power, and best range; the Breguet equations give range and endurance.
- Field lengths come from integrating the ground run. Specific excess power comes from the energy equation, and the maneuver V-n diagram from specific excess power at each load factor.
- Each result is reported with its margin. A shortfall goes back to the sizing loop.
:::

## What the RFP asks

:::{table} The performance the RFP asks for. Every value comes from the RFP; T is the threshold, O the objective.
:label: tbl-perf-requirements

| Item | Navy Jet Trainer |
| --- | --- |
| Point performance | Maximum operating speed Mach 0.78 (T), Mach 0.90 (O) at 25,000 ft; {term}`specific excess power` 90 ft/s (T), 125 ft/s (O) and sustained load factor +4.0 g (T), +6.0 g (O) at 15,000 ft; all at {term}`MTOW` less 50% fuel |
| Field | Takeoff distance 5,000 ft at MTOW; {term}`critical field length` 6,000 ft; landing distance 5,000 ft at {term}`MLW`; all at 5,000 ft {term}`density altitude`; full-stop {term}`FCLP` |
| Missions | The training flight and the 600 nmi ferry flight, on internal fuel; reserves of 30 and 45 minutes at maximum endurance speed |
| Data | {term}`Flight envelope` and V-n diagram; maximum dive speed; a segment table for each mission; field lengths at MTOW and MLW |

:::

:::{admonition} Navy Jet Trainer
:class: navy

Check every row with the drag polar and the engine deck of the sizing code. Which rows did the constraint diagram already check, and at which weight?
:::

## The check on the sizing

:::{figure} figures/sizing-check-flow.svg
:label: fig-sizing-check-flow
:alt: A flow of seven boxes in two rows. Top row, left to right. Inputs: polars, engine deck, weights, and the wing area S. Point performance: speeds, climb, specific excess power, and turns. Mission: segment by segment, fuel. Field: takeoff, critical field, and landing. An arrow runs down from Field to the bottom row, which reads right to left. Envelopes: flight envelope and V-n diagram. Compare with every requirement: margin or shortfall. Back to sizing: ASORT and the constraint diagram. The Inputs and Compare boxes are shaded.
:width: 100%

The performance check on the sizing, from the inputs to the comparison with the requirements. Schematic.
:::

- Use the same drag polar, the same engine deck, and the same weights as the sizing code. A different model hides sizing errors.
- The constraint diagram used one point per requirement. Here each requirement is computed at its own weight, altitude, and day.
- A shortfall goes back to the sizing loop. A large margin is excess weight.

:::{admonition} Navy Jet Trainer
:class: navy

Report each result with its margin against the RFP value. Which requirement has the smallest margin?
:::

## Speeds and symbols

:::{table} Symbols of the performance lecture.
:label: tbl-perf-symbols

| Symbol | Meaning | Part |
| --- | --- | --- |
| $V$, $V_E = V\sqrt{\sigma}$ | True and equivalent airspeed, in KTAS and KEAS; KCAS and KIAS are the calibrated and indicated airspeeds | 1 to 3 |
| $q = \tfrac{1}{2}\rho V^2$, $\rho$, $\sigma = \rho/\rho_0$ | Dynamic pressure, air density, and density ratio | 1 to 3 |
| $W$, $S$, $b$, $h$, $g$ | Weight, wing area, wing span, altitude, and acceleration of gravity | 1 to 3 |
| $T$, $D$, $L$, $P_{req} = D\,V$ | Thrust, drag, lift, and power required | 1 to 3 |
| $C_{D_0}$, $K = 1/(\pi\,AR\,e)$ | The polar $C_D = C_{D_0} + K\,C_L^2$ of [Lecture 7](../lecture-07/drag-polar.md) | 1, 2 |
| $V_S$, $V_{min}$, $V_H$ | Stall speed; lowest and highest speed in level flight with the thrust available | 1 |
| $V_{md}$, $V_{mp}$, $V_{BR}$ | Speeds of minimum drag, minimum power, and best range of a jet | 1 |
| $R$, $E$, $C$ | Range, endurance, and thrust specific fuel consumption | 1 |
| $\gamma$, $V_v$, $V_X$, $V_Y$ | Climb angle, rate of climb, speed for the best angle, and speed for the best rate | 1, 2 |
| $\varepsilon = \alpha + \phi_T$, $\gamma_d$ | Angle of the thrust line to the flight path, with $\phi_T$ the incidence of the thrust line; descent angle | 1, 2 |
| $\mu$, $\mu_B$, $S_G$ | Rolling and braking friction coefficients; ground run | 2 |
| $V_{S1}$, $V_{EF}$, $V_1$, $V_R$, $V_{MU}$, $V_{LOF}$, $V_2$ | Stall speed in the takeoff configuration, engine-failure speed, and the takeoff speeds | 2 |
| $V_{mc}$, $y_e$, $D_{dead}$, $b$, $C_{n\delta_r}$, $\delta_{r,max}$ | Minimum control speed, engine arm from the centerline, drag of the failed engine, span, rudder yaw power, and the rudder limit, as in [Lecture 10](../lecture-10/lateral-and-controls.md) | 2 |
| $z_e$, $P_s$ | {term}`Energy height` and specific excess power, as in [Lecture 9](../lecture-09/constraint-method.md) | 3 |
| $n$, $\omega$, $r$, $\phi$ | {term}`Load factor`, turn rate, radius of the turn or of the flight path, and bank angle | 1, 3 |
| $V_{MO}$, $M_{MO}$ | Maximum operating speed and Mach number | 3 |
| $n_{max}$, $n_{sus}$, $V^*$ | Limit and sustained load factors; {term}`corner speed` | 3 |

:::

Units are feet, pounds, and seconds, with speeds in knots where stated. In this lecture $\alpha$ is the angle of attack. The thrust lapse $\alpha$ and the weight fraction $\beta$ of Lecture 9 are not used, except where the Air-to-Air Fighter example of part 3 quotes its $\beta$.

Four symbols have another meaning earlier in the book. In [Lecture 10](../lecture-10/lateral-and-controls.md), $V_H$ and $V_v$ are the tail volume coefficients and $\varepsilon$ is the downwash angle. In [Lecture 6](../lecture-06/high-lift-wing-and-field.md), $V_{BR}$ is the speed at brake application.

## Equations of motion

The aircraft is a point mass at the CG, of mass $W/g$. Each case sums the forces along the flight path and normal to it. $\varepsilon = \alpha + \phi_T$ is the angle of the thrust line to the flight path.

### Cruise

:::{figure} figures/eom-cruise.svg
:label: fig-eom-cruise
:alt: A jet trainer in level flight to the right, with four forces drawn from its center of gravity. Lift L points straight up and weight W straight down. Drag D points aft along the horizontal flight path. Thrust T points forward and is tilted up from the flight path by the angle epsilon. The velocity V points forward along the flight path. The lift arrow is shorter than the weight arrow, because the tilted thrust carries part of the weight.
:width: 65%

Forces in level flight. Schematic, drawn in steady flight; notation of Gudmundsson (2022), Section 17.1.2.
:::

:::{math}
:label: eq-perf-cruise
\frac{W}{g}\frac{dV}{dt} = T\cos\varepsilon - D, \qquad 0 = T\sin\varepsilon + L - W
:::

In steady cruise with small $\varepsilon$, $T = D$ and $L = W$. The distance flown and the fuel burned follow from

:::{math}
:label: eq-perf-cruise-rates
\frac{dx}{dt} = V, \qquad \frac{dW}{dt} = -C\,T
:::

The sources are Gudmundsson (2022), Eq. 17-1 and Eqs. 20-1 to 20-3.

### Climb

:::{figure} figures/eom-climb.svg
:label: fig-eom-climb
:alt: A jet trainer climbing to the right along a flight path inclined above the horizon by the angle gamma. Lift L is normal to the flight path, drag D points aft along it, and weight W points straight down. Thrust T points forward and is tilted up from the flight path by the angle epsilon. The velocity V points along the flight path. A dashed horizontal line marks the horizon.
:width: 65%

Forces in a climb. The flight path lies above the horizon by the climb angle $\gamma$. Schematic, drawn in steady flight; notation of Gudmundsson (2022), Section 17.1.2.
:::

:::{math}
:label: eq-perf-climb
\begin{aligned}
\frac{W}{g}\frac{dV}{dt} &= T\cos\varepsilon - D - W\sin\gamma, \qquad \frac{dh}{dt} = V\sin\gamma\\
\frac{W}{g}\,V\frac{d\gamma}{dt} &= T\sin\varepsilon + L - W\cos\gamma
\end{aligned}
:::

In a steady climb with small $\varepsilon$:

:::{math}
:label: eq-steady-climb
\sin\gamma = \frac{T - D}{W}, \qquad L = W\cos\gamma
:::

When the speed changes along the climb, with small $\varepsilon$, the first equation of {eq}`eq-perf-climb` times $V/W$ gives the specific excess power of [part 3](maneuver-and-vn.md):

:::{math}
:label: eq-perf-ps-climb
\frac{V\,(T - D)}{W} = \frac{dh}{dt} + \frac{V}{g}\frac{dV}{dt}
:::

The sources are Gudmundsson (2022), Eq. 17-1 and Section 19.2.1.

### Descent

:::{figure} figures/eom-descent.svg
:label: fig-eom-descent
:alt: A jet trainer descending to the right along a flight path inclined below the horizon by the descent angle, gamma with the subscript d. Lift L is normal to the flight path, drag D points aft along it, and weight W points straight down. Thrust T points forward along the flight path, with no tilt, and is shorter than the drag. The velocity V points down the flight path. A dashed horizontal line marks the horizon.
:width: 65%

Forces in a descent. The flight path lies below the horizon by the descent angle $\gamma_d$, and the thrust is drawn along the flight path. Schematic, drawn in steady flight; notation of Gudmundsson (2022), Section 17.1.2.
:::

With the thrust along the flight path, $\varepsilon = 0$, and a constant descent angle $\gamma_d = -\gamma$:

:::{math}
:label: eq-perf-descent
\frac{W}{g}\frac{dV}{dt} = T - D + W\sin\gamma_d, \qquad 0 = L - W\cos\gamma_d, \qquad \frac{dh}{dt} = -V\sin\gamma_d
:::

In a steady descent:

:::{math}
:label: eq-steady-descent
\sin\gamma_d = \frac{D - T}{W}, \qquad L = W\cos\gamma_d
:::

In a glide, $T = 0$ and $\tan\gamma_d = D/L = 1/(L/D)$. The glide is flattest at $(L/D)_{max}$, at the speed $V_{md}$.

The sources are Gudmundsson (2022), Eq. 17-1 and Eqs. 22-1 to 22-5, 22-9, 22-10, 22-16, and 22-17.

### Maneuver

:::{figure} figures/eom-maneuver.svg
:label: fig-eom-maneuver
:alt: Two sketches. Left, a level turn seen from behind. The trainer is banked to the right by the angle phi, measured between the vertical and the lift. Lift L points up and to the right, normal to the wing, and weight W points straight down. An arrow to the right shows the radius r to the center of the turn. The vertical part of the lift equals the weight. Right, a pull-up seen from the side. The trainer is at the bottom of a circular arc whose center lies above it at the radius r. Lift L points up toward the center and is twice as long as the weight W, which points down. Thrust T points forward and drag D aft.
:width: 100%

Forces in a level turn at the bank angle $\phi$ and in a pull-up at the bottom of an arc of radius $r$. Schematic; notation of Gudmundsson (2022), Sections 17.1.2 and 20.4.
:::

In a level turn at the bank angle $\phi$ and the radius $r$, with small $\varepsilon$, the forces are summed vertically and toward the center of the turn:

:::{math}
:label: eq-perf-turn
\begin{aligned}
L\cos\phi &= W, \qquad L\sin\phi = \frac{W}{g}\frac{V^2}{r}\\
n &= \frac{L}{W} = \frac{1}{\cos\phi}, \qquad \omega = \frac{V}{r} = \frac{g\sqrt{n^2-1}}{V}
\end{aligned}
:::

In a pull-up with the wings level, at the bottom of the arc:

:::{math}
:label: eq-perf-pullup
L - W = \frac{W}{g}\frac{V^2}{r}, \qquad n = 1 + \frac{V^2}{g\,r}
:::

Along the flight path, with the drag computed at $L = nW$:

:::{math}
:label: eq-perf-maneuver-path
\frac{W}{g}\frac{dV}{dt} = T - D
:::

The sources are Gudmundsson (2022), Eq. 17-2 and Eqs. 20-61 to 20-63, 20-65, and 20-74.

:::{admonition} Navy Jet Trainer
:class: navy

The RFP gives a condition for each case: Mach 0.78 (T) and Mach 0.90 (O) at 25,000 ft; climbs at 250 KCAS and descents at idle thrust in the training flight; a sustained load factor of +4.0 g (T) and +6.0 g (O) at 15,000 ft. Which equation applies to each?
:::

## Drag and power required

With the parabolic polar and $L = W$, the drag and the power required in level flight are

:::{math}
:label: eq-drag-power
D = q\,S\,C_{D_0} + \frac{K\,W^2}{q\,S}, \qquad P_{req} = D\,V
:::

:::{figure} figures/drag-power.svg
:label: fig-drag-power
:alt: Two panels against true airspeed from 120 to 560 knots, each with curves for sea level, 15,000 feet, and 30,000 feet. Left, drag. Each curve falls to the same minimum, 1,294 pounds, and rises again. The minimum lies at 175 knots at sea level, 221 knots at 15,000 feet, and 286 knots at 30,000 feet. The sea-level curve leaves the top of the panel, 6,000 pounds, near 530 knots; at 560 knots the 30,000-foot curve is at 2,645. Right, power required. The minimum is 610 horsepower at 133 knots at sea level, 769 horsepower at 168 knots at 15,000 feet, and 998 horsepower at 218 knots at 30,000 feet.
:width: 100%

Drag and power required of the Learjet 45, a published example, at 20,000 lb and three altitudes: $S$ = 311.6 ft², $C_{D_0}$ = 0.0200, $K$ = 0.05236. The dots mark minimum drag and minimum power. Computed; inputs from Gudmundsson (2022), Table 17-8 and Example 20-6.
:::

- The minimum drag is $D_{min} = 2W\sqrt{K\,C_{D_0}} = W/(L/D)_{max}$. It is the same at every altitude: 1,294 lb for the Learjet 45 at 20,000 lb.
- The minimum-drag speed rises with altitude: $V_{md} \propto 1/\sqrt{\sigma}$.
- The minimum power rises as $1/\sqrt{\sigma}$: 610 hp at sea level and 998 hp at 30,000 ft.

:::{admonition} Navy Jet Trainer
:class: navy

These curves come from the polar of [Lecture 7](../lecture-07/drag-polar.md). Which of your three polars applies at each RFP condition?
:::

## Thrust available and limiting speeds

:::{math}
:label: eq-level-speeds
V_S = \sqrt{\frac{2W}{\rho\,S\,C_{L_{max}}}}, \qquad
V^2 = \frac{T \pm \sqrt{T^2 - 4\,C_{D_0}\,K\,W^2}}{\rho\,S\,C_{D_0}}
:::

The two roots of the second equation are $V_H$ and $V_{min}$, the speeds at which the thrust equals the drag.

:::{figure} figures/level-speeds.svg
:label: fig-level-speeds
:alt: Drag and military thrust against true airspeed from 140 to 560 knots. The drag curve falls from 2,860 pounds to a minimum of 1,294 at 286 knots and rises to 2,640. The thrust line rises steadily from 1,300 to 2,230 pounds and crosses the drag curve twice. Five vertical lines mark the speeds. The stall speed, V S, is at 182 knots. The minimum level speed, V min, is at 236 knots, the first crossing. The minimum drag speed, V m d, is at 286 knots. The best range speed, V B R, is at 377 knots. The maximum level speed, V H, is at 441 knots, the second crossing.
:width: 85%

Thrust available and the level-flight speeds of the Learjet 45, a published example, at 20,000 lb and 30,000 ft, flaps up, military thrust. $V_H$ is Mach 0.75; the polar has no compressibility drag, so the real $V_H$ is lower. Computed; inputs from Gudmundsson (2022), Table 17-8, with the Mattingly thrust model of his Eq. 14-77.
:::

- Level flight needs $T \ge D$ and $V \ge V_S$.
- At altitude $V_{min}$ can be limited by the thrust: 236 KTAS here, against 182 KTAS for $V_S$.
- The thrust varies with Mach number. Solve $T(V) = D(V)$ numerically with the engine deck.

In the Learjet 45 example the military thrust is $0.6\,F_{SL}\,\delta_0$ and the maximum thrust is $F_{SL}\,\delta_0$, with $F_{SL}$ = 7,000 lb (Gudmundsson 2022, Eqs. 14-77 and 14-75, Examples 19-1 and 18-5). {eq}`eq-lapse-low` of [Lecture 8](../lecture-08/engine-models.md) is normalized by the military static thrust and has no factor 0.6. The flight envelope and the turn-rate chart of [part 3](maneuver-and-vn.md) use the maximum thrust, so they reach a higher speed than $V_H$ here.

:::{admonition} Navy Jet Trainer
:class: navy

Mach 0.78 (T) and Mach 0.90 (O) at 25,000 ft are points where $T = D$, with the compressibility drag of [Lecture 7](../lecture-07/drag-polar.md) included. Which rating do you use there?
:::

## Level-flight speeds

:::{table} The level-flight speeds. The values are for the Learjet 45 of {numref}`fig-level-speeds`: 20,000 lb, 30,000 ft, military thrust, flaps up, $C_{L_{max}}$ = 1.527. $V_{md}$ and $V_{BR}$ follow from {numref}`tbl-optimum-cl`. After Gudmundsson (2022), Eqs. 20-24, 20-26, 20-29, 20-39, and 20-58.
:label: tbl-level-speeds

| Speed | Definition | Relation | KTAS |
| --- | --- | --- | ---: |
| $V_S$ | Stall. Level flight at $C_{L_{max}}$ and 1 g; one value per configuration | $\sqrt{2W/(\rho\,S\,C_{L_{max}})}$ | 182 |
| $V_{min}$ | Minimum level speed. The low-speed point where $T = D$, or $V_S$ if that is higher; one value per rating | Lower root of {eq}`eq-level-speeds`; not below $V_S$ | 236 |
| $V_{md}$ | Minimum drag. $D_{min}$ and $(L/D)_{max}$: the parasite drag equals the drag due to lift | $\sqrt{2W/(\rho\,S)}\,(K/C_{D_0})^{1/4}$ | 286 |
| $V_{BR}$ | Best range of a jet. The maximum of $V\,L/D$, that is, of $\sqrt{C_L}/C_D$, at constant $C$ | $3^{1/4}\,V_{md} = 1.316\,V_{md}$ | 377 |
| $V_H$ | Maximum level speed. The high-speed point where $T = D$; one value per rating | Upper root of {eq}`eq-level-speeds` | 441 |

:::

:::{admonition} Navy Jet Trainer
:class: navy

State each speed with its weight, altitude, configuration, and rating. Which of these speeds does the RFP specify?
:::

## Three optimum lift coefficients

:::{table} The three optimum lift coefficients of a parabolic polar. The last column is $C_L$ for the Learjet 45 polar of Gudmundsson (2022), Table 17-8.
:label: tbl-optimum-cl

| Condition | $C_L$ | $V$ | Used for | Learjet 45 |
| --- | --- | --- | --- | ---: |
| Minimum drag, $(L/D)_{max}$ | $\sqrt{C_{D_0}/K}$ | $V_{md}$ | Jet endurance and best climb angle | 0.618 |
| Minimum power | $\sqrt{3\,C_{D_0}/K}$ | $0.760\,V_{md}$ | Lowest sink rate in a glide | 1.070 |
| Best range of a jet, maximum $\sqrt{C_L}/C_D$ | $\sqrt{C_{D_0}/(3K)}$ | $1.316\,V_{md}$ | Jet range; $L/D = 0.866\,(L/D)_{max}$ | 0.357 |

:::

The speed for minimum drag and the best $L/D$ are

:::{math}
:label: eq-vmd-ldmax
V_{md} = \sqrt{\frac{2W}{\rho\,S}}\left(\frac{K}{C_{D_0}}\right)^{1/4}, \qquad
\left(\frac{L}{D}\right)_{max} = \frac{1}{2\sqrt{K\,C_{D_0}}}
:::

For the Learjet 45 at 20,000 lb and 30,000 ft, $(L/D)_{max}$ = 15.5, $V_{md}$ = 286 KTAS, and the maximum of $\sqrt{C_L}/C_D$ is 22.4 (Gudmundsson 2022, Examples 19-4, 20-5, 20-6, and 20-8). The same polar gives $V_{BR}$ = 377 KTAS at $L/D$ = 13.4.

The table assumes $C_{L_{minD}} = 0$. A cambered polar shifts all three values (Gudmundsson 2022, Eqs. 20-33 to 20-59).

:::{admonition} Navy Jet Trainer
:class: navy

The reserves are flown at maximum endurance speed. Which row is that for your engine, and does the engine deck agree?
:::

## Range and endurance

The Breguet equations of [Lecture 2](../lecture-02/mission-fuel.md) hold at constant $V$, $C_L$, and $C$ (Gudmundsson 2022, Eqs. 21-37 and 21-68):

:::{math}
:label: eq-perf-breguet
R = \frac{V}{C}\,\frac{L}{D}\,\ln\frac{W_i}{W_f}, \qquad
E = \frac{1}{C}\,\frac{L}{D}\,\ln\frac{W_i}{W_f}
:::

$W_i$ and $W_f$ are the weights at the start and at the end of the segment.

:::{figure} figures/range-endurance.svg
:label: fig-range-endurance
:alt: Two curves against true airspeed from 160 to 560 knots, each as a fraction of its maximum. The lift-to-drag ratio rises from 0.57 to its peak at 286 knots, marked V m d, and falls to 0.49 at 560 knots. The product of speed and lift-to-drag ratio rises from 0.28 to its peak at 377 knots, marked V B R, and falls to 0.84 at 560 knots. At V B R the lift-to-drag ratio is 0.866 of its maximum.
:width: 80%

$L/D$ and $V\,L/D$ of the Learjet 45, a published example, at 20,000 lb and 30,000 ft, each as a fraction of its maximum. Computed; inputs from Gudmundsson (2022), Table 17-8.
:::

With constant $C$, the best range of a jet is at the peak of $V\,L/D$ and the maximum endurance is at $(L/D)_{max}$.

## The segment table

:::{table} The columns of the segment table. One row per mission segment.
:label: tbl-segment-table

| Segment | $W$ at start (lb) | Fuel (lb) | Time (min) | Distance (nmi) | Altitude (ft) | Speed | Rating, $C_L$ |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 1 Warm-up, taxi | | | | | | | |
| 2 Takeoff | | | | | | | |
| 3 Climb | | | | | | | |
| ... | | | | | | | |
| Reserve | | | | | | | |
| Total | | | | | | | |

:::

- Make one table per mission. Each row starts at the end weight of the row before it.
- The climb and descent segments give time, fuel, and distance. The cruise covers the distance that remains.
- The totals must close on the fuel the sizing code carried.

:::{admonition} Navy Jet Trainer
:class: navy

The RFP asks for this table for the training flight and for the ferry flight. Do your totals match the fuel the sizing code carries, reserves included?
:::

:::{seealso}
Continue with [](climb-and-field.md): the steady climb, the best angle and the best rate, the takeoff speeds, the ground run, the balanced and critical field lengths, and the landing. The references for the three parts are at the end of [](maneuver-and-vn.md).
:::
