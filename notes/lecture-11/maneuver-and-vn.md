---
title: "Performance, part 3: Maneuver and the V-n diagram"
short_title: Maneuver and the V-n diagram
---

This is the third part of Lecture 11, *Performance Assessment*. It covers energy height and specific excess power, turns, the turn-rate chart, the flight envelope, the load factor of each maneuver, the specific excess power at load factor, and the maneuver V-n diagram. The equations of motion and the symbols are in [](level-flight-and-range.md).

:::{note} What to take from this lecture
- Specific excess power is the rate of change of the energy height. A turn with $P_s = 0$ is a sustained turn.
- The stall, the limit load factor, and the thrust limit the load factor of a turn.
- The maneuver V-n diagram shows $P_s$ at each load factor and speed.
:::

## Energy height and specific excess power

The {term}`energy height` $z_e$ and the {term}`specific excess power` $P_s$ are those of [Lecture 9](../lecture-09/constraint-method.md):

:::{math}
:label: eq-perf-energy-height
W\,z_e = W\,h + \frac{1}{2}\frac{W}{g}V^2, \qquad z_e = h + \frac{V^2}{2g}
:::

:::{math}
:label: eq-perf-ps
P_s = \frac{dz_e}{dt} = \frac{dh}{dt} + \frac{V}{g}\frac{dV}{dt} = \frac{V\,(T - D)}{W}
:::

- $P_s$ is spent on climbing, on accelerating, or on both.
- In a turn the drag grows with the load factor $n$, and $P_s$ falls. A turn with $P_s = 0$ is a sustained turn.

:::{exercise} Back to the master equation
:label: ex-perf-master

Write $D$ with the polar at the load factor $n$ and divide $P_s$ by $V$. Set $T = \alpha\,T_{SL}$ and $W = \beta\,W_{TO}$, with the thrust lapse $\alpha$ and the weight fraction $\beta$ of Lecture 9, and solve for $T_{SL}/W_{TO}$. Compare the result with the master equation, {eq}`eq-master`, with $K_2 = 0$ and $C_{D_R} = 0$.
:::

:::{admonition} Navy Jet Trainer
:class: navy

The RFP asks for a specific excess power of 90 ft/s (T) and 125 ft/s (O) at 15,000 ft, at MTOW less 50% fuel. At which speed do you read it?
:::

## Turns

The level turn of [part 1](level-flight-and-range.md) gives the load factor, the turn rate, and the radius:

:::{math}
:label: eq-turn
n = \frac{L}{W} = \frac{1}{\cos\phi}, \qquad \omega = \frac{g\sqrt{n^2 - 1}}{V}, \qquad r = \frac{V^2}{g\sqrt{n^2-1}}
:::

Three limits act on the load factor of a turn:

- The stall: $n = q\,C_{L_{max}}/(W/S)$.
- The structure: $n = n_{max}$.
- The thrust, in a sustained turn with $P_s = 0$:

:::{math}
:label: eq-n-sustained
n_{sus} = \sqrt{\frac{q}{K\,(W/S)}\left(\frac{T}{W} - \frac{q\,C_{D_0}}{W/S}\right)}
:::

This is the $n_{MS}$ of {eq}`eq-sustained-load-factor` in [Lecture 8](../lecture-08/engine-models.md). $T/W$ and $W/S$ are the values at the flight condition.

:::{prf:definition} Corner speed
:label: def-corner-speed

The {term}`corner speed` $V^*$ is the speed at which the stall limit and the limit load factor meet. It gives the highest instantaneous turn rate.

$$V^* = \sqrt{\frac{2\,n_{max}\,W}{\rho\,S\,C_{L_{max}}}}$$
:::

- An instantaneous turn has $P_s < 0$ and loses energy. A sustained turn holds it.

:::{iframe} ../quickcheck/turn-point.html
:label: qc-turn-point
:width: 100%

Quick check: the load factor, the turn rate, and the radius of a level turn from {eq}`eq-turn`. Shuffle gives new values; the solution shows the steps.
:::

:::{admonition} Navy Jet Trainer
:class: navy

The RFP asks for a sustained load factor of +4.0 g (T) and +6.0 g (O) at 15,000 ft, at MTOW less 50% fuel. Is the lift coefficient of that turn below the break $C_L$ of your polar?
:::

## The turn-rate chart

:::{figure} figures/turn-rate-chart.svg
:label: fig-turn-rate-chart
:alt: Turn rate against Mach number. A black boundary starts on the axis at Mach 0.22, the 1 g stall, rises along the stall limit to the corner at Mach 0.42 and 13.9 degrees per second, falls along the limit load factor of 3.5 to 9.0 degrees per second at Mach 0.65, and drops to the axis along the maximum operating speed, V M O. A blue line, the sustained turn where the specific excess power is zero, runs from the stall limit at Mach 0.34 to the limit load factor at Mach 0.55 and peaks at 10.8 degrees per second at Mach 0.44. Dashed contours of specific excess power: minus 25 feet per second above the blue line, 25 and 75 feet per second below it.
:width: 85%

The turn-rate chart of the Learjet 45, a published example, at 20,000 lb and 15,000 ft, with the maximum thrust of the Mattingly model (Gudmundsson 2022, Eq. 14-75) and $n_{max}$ = 3.5 as in his Example 20-10. The right edge is the published operating limit $V_{MO}$ = 330 KIAS, Mach 0.65 at this altitude. Computed; inputs from Gudmundsson (2022), Table 17-8.
:::

- Outside the black boundary the aircraft stalls, exceeds the limit load factor, or exceeds the maximum operating speed.
- The blue line is the sustained turn. Its best rate is 10.8 deg/s at Mach 0.44.
- Above the blue line $P_s < 0$, and the turn loses energy.
- The right edge is $V_{MO}$ or $M_{MO}$, whichever is lower at the altitude.
- The polar has no break, so the sustained line is optimistic.

:::{admonition} Navy Jet Trainer
:class: navy

The RFP point for this chart is 15,000 ft at MTOW less 50% fuel. Where do +4.0 g (T) and +6.0 g (O) lie against your sustained line?
:::

## The flight envelope

:::{figure} figures/flight-envelope.svg
:label: fig-flight-envelope
:alt: Pressure altitude against Mach number, with a closed boundary. On the left, the 1 g stall line rises from Mach 0.17 at sea level to Mach 0.34 at 34,000 feet. On top, a blue line where the specific excess power is zero rises from there to the absolute ceiling, 49,000 feet, at Mach 0.81. On the right, the boundary runs down the maximum operating Mach number, 0.81, to 26,800 feet, then down the maximum operating speed, 330 knots indicated, to Mach 0.50 at sea level. Thin contours inside show a specific excess power of 50, 100, and 150 feet per second; they meet the right edge at 29,100, 14,500, and 2,600 feet. A label gives the service ceiling, 48,000 feet.
:width: 85%

The 1 g {term}`flight envelope` of the Learjet 45, a published example, at 20,000 lb with the maximum thrust of the Mattingly model. The right edge follows the published operating limits, $V_{MO}$ 330 KIAS and $M_{MO}$ 0.81. The polar has no compressibility drag. Computed; inputs from Gudmundsson (2022), Table 17-8.
:::

- The left edge is the stall. The top is the absolute ceiling, where $P_s = 0$: 49,000 ft here, reached on the $M_{MO}$ line.
- The service ceiling is where $P_s$ = 100 ft/min: 48,000 ft here. The figure rounds both ceilings to the nearest 1,000 ft; they are about 770 ft apart.
- The contours of $P_s$ at 1 g give the climb capability at any point.
- The drag rise can close the envelope before $V_{MO}$ and $M_{MO}$.
- Repeat the chart at $n > 1$ for the $P_s$ in a maneuver.

:::{admonition} Navy Jet Trainer
:class: navy

The RFP asks for the flight envelope. Where does each RFP condition lie on it?
:::

## Load factor by maneuver

:::{table} The load factor and the turn rate of each maneuver. $r$ is the radius of the flight path. After Anderson (2016), Chapter 6, and Gudmundsson (2022), Chapter 20.
:label: tbl-maneuver-load-factor

| Maneuver | $n = L/W$ | Turn rate $\omega$ |
| --- | --- | --- |
| Level turn at the bank angle $\phi$ | $1/\cos\phi$ | $g\sqrt{n^2-1}/V$ |
| Pull-up with the wings level, the bottom of a loop | $1 + V^2/(g\,r)$ | $g\,(n-1)/V$ |
| Pull-down from inverted, the top of a loop or a split-S | $V^2/(g\,r) - 1$ | $g\,(n+1)/V$ |
| Steady climb at the angle $\gamma$ | $\cos\gamma$ | 0 |

:::

:::{figure} figures/loop-forces.svg
:label: fig-loop-forces
:alt: A loop seen from the side, drawn as a dashed circle of radius r and flown counterclockwise. At the bottom the trainer is upright and flies to the right. Lift L points up toward the center and weight W points down, with the relation L minus W equals W over g times V squared over r. At the top the trainer is inverted and flies to the left. Lift L and weight W both point down toward the center, with the relation L plus W equals W over g times V squared over r. The lift arrow at the bottom is more than three times as long as the one at the top.
:width: 75%

Lift and weight at the bottom and at the top of a loop, drawn with the same $V^2/r$ at both points. Schematic.
:::

- The maneuver sets $n$ and $\omega$. At the same $n$, the pull-down from inverted turns fastest.
- At one weight, altitude, and rating, $P_s$ depends on $n$ and $V$ only.

:::{admonition} Navy Jet Trainer
:class: navy

The training flight includes 30 minutes of basic maneuvers at military thrust, Mach 0.60, and 10,000 ft. Which maneuvers do you assume, and what is the load factor of each?
:::

## Specific excess power at load factor

At the load factor $n$ the lift is $nW$, and the drag due to lift grows with $n^2$:

:::{math}
:label: eq-drag-at-n
D(n) = q\,S\,C_{D_0} + \frac{K\,n^2\,W^2}{q\,S}
:::

:::{math}
:label: eq-ps-at-n
P_s(n) = \frac{V\,[T - D(n)]}{W} = P_s(1\,\mathrm{g}) - \frac{K\,W\,V}{q\,S}\,(n^2 - 1)
:::

The load factor at a given $P_s$ (Mattingly et al. 2002, Chapter 2):

:::{math}
:label: eq-n-at-ps
n = \sqrt{\frac{q}{K\,(W/S)}\left(\frac{T}{W} - \frac{q\,C_{D_0}}{W/S} - \frac{P_s}{V}\right)}
:::

With $P_s = 0$ this is $n_{sus}$ of {eq}`eq-n-sustained`.

- Each g above 1 lowers $P_s$: the second term of {eq}`eq-ps-at-n` grows with $n^2 - 1$.
- With $P_s > 0$ the aircraft can climb at $dh/dt = P_s$ or accelerate at $dV/dt = g\,P_s/V$ during the maneuver.
- With $P_s < 0$ the maneuver loses altitude or speed at the same rates. It lasts until the speed or the altitude runs out.
- The stall and $n_{max}$ still limit $n$.

:::{admonition} Navy Jet Trainer
:class: navy

The specific excess power and the sustained load factor of the RFP are two points of one $P_s(n, V)$ field at 15,000 ft. Do you read both at the same speed and rating?
:::

## The maneuver V-n diagram: Air-to-Air Fighter

:::{prf:definition} Maneuver V-n diagram
:label: def-maneuver-vn

The {term}`maneuver V-n diagram` plots the load factor against the speed or the Mach number at one weight and one altitude. It shows the stall line, the limit load factor, the maximum operating speed, and lines of constant specific excess power.
:::

:::{figure} figures/maneuver-vn.svg
:label: fig-maneuver-vn
:alt: Load factor against Mach number at 30,000 feet. A black boundary starts at the 1 g stall, Mach 0.24, rises along the stall line for a maximum lift coefficient of 2.0 to the corner at Mach 0.64, and runs level at the limit load factor, 7.33, to Mach 0.9, where a dotted line closes the chart. A blue line, specific excess power zero, rises to a load factor of 5.23 at Mach 0.9. Four dashed lines of constant specific excess power end on diamonds at Mach 0.9. A table at the right gives the bank angle and the specific excess power at each diamond.
:width: 90%

The maneuver V-n diagram of the Air-to-Air Fighter of Mattingly et al. (2002), Chapter 2, a published example, at 30,000 ft: $T_{SL}/W_{TO}$ = 1.25, $W_{TO}/S$ = 64 lb/ft², $\beta$ = 0.78, $C_{D_0}$ = 0.016 (the value at Mach 0.9), $K$ = 0.18, $C_{L_{max}}$ = 2.0, and maximum power, with afterburner, at a throttle ratio of 1.07. The limit load factor 7.33 is assumed, after Nicolai and Carichner (2010), Example 5.1. Each dashed line is the $P_s$ through one diamond, in ft/s. Computed.
:::

- The black boundary is the 1 g stall speed, the stall line at $C_{L_{max}}$, and $n_{max}$. The dotted line at Mach 0.9 is the end of the chart.
- The blue line is $P_s = 0$. It gives $n_{sus}$ = 5.23 at Mach 0.9.
- Below the blue line the aircraft gains energy. Above it the aircraft loses energy.
- The diamonds are the rows of {numref}`tbl-ps-by-maneuver`. The angles at the right are the bank of a level turn, from $n = 1/\cos\phi$.
- The polar is parabolic and $C_{L_{max}}$ is 2.0 at every Mach number, so the chart is optimistic.

:::{warning}
The V-n diagram the RFP asks for is the structural one, with its load factors and its dive speed. This lecture covers the maneuver diagram only.
:::

:::{admonition} Navy Jet Trainer
:class: navy

At 15,000 ft and MTOW less 50% fuel, what is your $P_s$ at +4.0 g (T) and at +6.0 g (O)?
:::

## Specific excess power by maneuver

:::{table} Specific excess power of the Air-to-Air Fighter by maneuver, at 30,000 ft, Mach 0.9, $\beta$ = 0.78, and maximum power, with afterburner: the diamonds of {numref}`fig-maneuver-vn`. The last two columns are the same energy rate, as a climb at constant speed or as an acceleration in level flight. Computed.
:label: tbl-ps-by-maneuver

| Maneuver | $n$ | $\omega$ (deg/s) | $P_s$ (ft/s) | $dh/dt$ (ft/min) | $dV/dt$ (kt/s) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Level flight, wings level | 1.00 | 0 | 596 | 35,700 | 12.7 |
| Level turn, 60° bank | 2.00 | 3.6 | 528 | 31,700 | 11.2 |
| Level turn, 75.5° bank | 4.00 | 8.0 | 257 | 15,400 | 5.5 |
| Sustained turn, 79.0° bank | 5.23 | 10.6 | 0 | 0 | 0 |
| Level turn at $n_{max}$, 82.2° bank | 7.33 | 15.0 | −595 | −35,700 | −12.7 |
| Pull-up at $n_{max}$ | 7.33 | 13.0 | −595 | −35,700 | −12.7 |
| Pull-down from inverted at $n_{max}$ | 7.33 | 17.2 | −595 | −35,700 | −12.7 |

:::

- The requirement of the Air-to-Air Fighter is 5 g sustained at Mach 0.9 and 30,000 ft. With $n_{sus}$ = 5.23 it is met.
- A negative $P_s$ drains energy height. The next segment must recover it.
- The same $n$ gives the same $P_s$. The three maneuvers at $n_{max}$ differ only in turn rate.

:::{admonition} Navy Jet Trainer
:class: navy

The basic-maneuvers segment is flown at Mach 0.60, 10,000 ft, and military thrust. Which of your maneuvers have a negative $P_s$, and how long can each be held?
:::

## This week

1. Compute the speeds at each RFP condition, from the polar and the engine deck of the sizing code: $V_S$, $V_{md}$, $V_{BR}$ or the cruise speed, and $V_H$, each with its margin.
2. Fill the segment table for each mission. Its totals must match the fuel the sizing code carries.
3. Plot the rate of climb and the climb angle against speed, the contours of $P_s$, and the flight envelope.
4. Integrate the field lengths at the RFP conditions, and find the critical field length.
5. Draw the turn-rate chart and the maneuver V-n diagram at 15,000 ft, and compute the $P_s$ of each basic maneuver at Mach 0.60, 10,000 ft, and military thrust.
6. Check the ferry flight: 600 nmi on internal fuel, with its reserve.
7. Make a {term}`compliance table <compliance matrix>`: requirement, value, and margin. Send every shortfall back to the sizing loop.

:::{tip}
[Assignment A08](../assignments/a08.md) asks for these results from the sizing code: the speeds, the two missions, the climb and the flight envelope, the turns, the field performance, the maneuver V-n diagram, and the compliance table.
:::

:::{important} Summary
- Performance uses the same polar, engine deck, and weights as the sizing code.
- The speeds for minimum drag, minimum power, and best range come from three optimum lift coefficients; range and endurance come from the Breguet equations.
- Field lengths come from integration, $P_s$ from the energy equation, turns from the force balance, and the maneuver V-n diagram from $P_s$ at each load factor.
:::

:::{exercise} For discussion
:label: ex-performance

Take the requirement with the smallest margin in your compliance table. Which input of that result is an estimate: the polar, the engine deck, or a weight? How far does the result move if that input is wrong by 10%? What do you change in the sizing code if the margin is negative?
:::

:::{seealso} Reading
Gudmundsson (2022), Chapters 17 to 23; Raymer (2018), Chapter 17; and Mattingly et al. (2002), Chapter 2.
:::

## Quiz

:::{iframe} ../quickcheck/quiz-lecture-11.html
:label: quiz-lecture-11
:width: 100%

Quiz on Lecture 11: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Gudmundsson, S., *General Aviation Aircraft Design: Applied Methods and Procedures*, 2nd ed., Butterworth-Heinemann, 2022. Chapter 14 (Section 14.3.4, the Mattingly thrust model), Chapter 17 (Table 17-8), and Chapters 18 to 23.
- Anderson, J. D., *Introduction to Flight*, 8th ed., McGraw-Hill, 2016. Chapter 6.
- Mattingly, J. D., Heiser, W. H., and Pratt, D. T., *Aircraft Engine Design*, 2nd ed., AIAA Education Series, 2002. Chapter 2.
- Nicolai, L. M., and Carichner, G. E., *Fundamentals of Aircraft and Airship Design, Volume 1: Aircraft Design*, AIAA Education Series, 2010. Example 5.1.
- Nelson, R. C., *Flight Stability and Automatic Control*, 2nd ed., McGraw-Hill, 1998. Chapter 2.
- Raymer, D. P., *Aircraft Design: A Conceptual Approach*, 6th ed., AIAA Education Series, 2018. Chapter 17.
- Torenbeek, E., *Synthesis of Subsonic Airplane Design*, Delft University Press, 1982.
- MIL-STD-3013, *Glossary of Definitions, Ground Rules, and Mission Profiles to Define Air Vehicle Performance Capability*, U.S. Department of Defense, 2003. The RFP refers to revision B.
- Learjet 45 operating limits, as published for the type: $V_{MO}$ = 330 KIAS below 26,756 ft and $M_{MO}$ = 0.81 above.
- AIAA 2026-27 Undergraduate Team Aircraft Design Competition RFP, *Design of a Navy Jet Training Aircraft*; see [](../navy-rfp/navy-rfp.md).
