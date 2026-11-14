---
title: "Stability and control, part 3: Trim"
short_title: Trim
---

This is the third part of Lecture 10, *Stability and Control*. It covers step 4 of the method: the trim equations, the elevator derivatives, the trim diagram, trim with the thrust line, the conditions to check, the trim drag, and the maneuver and approach cases. It uses the horizontal tail of [](longitudinal-stability.md) and the CG limits of [](cg-and-envelope.md). "Forward CG" and "aft CG" mean the CG at the forward limit and at the aft limit. The figures are redrawn after the figures on the slides.

:::{note} What to take from this lecture
- Trim is two equations at every condition the RFP names: no moment about the CG, and lift equal to weight.
- The forward CG needs the largest elevator deflection. The condition with the largest deflection sizes the elevator.
- A tail download adds drag. The performance analysis uses the trimmed polar.
:::

## Step 4: trim defined

:::{prf:definition} Trim
:label: def-trim

An aircraft is in {term}`trim` when the moment about the CG is zero and the lift equals the weight. The angle of attack $\alpha$ and the elevator deflection $\delta_e$ are the two unknowns.
:::

:::{figure} figures/trim-defined.svg
:label: fig-trim-defined
:alt: Side view of a jet trainer, nose to the left and pitched up. The flow V comes horizontally from the left along a dotted flight-path line through the CG. A dash-dot reference line runs along the fuselage; the angle between the flight path and the reference line is alpha. Below, the tail is drawn three times larger at the same attitude: the elevator is deflected trailing edge down from the dashed chord line of the stabilizer by the angle delta e.
:width: 85%

The two unknowns of trim, $\alpha$ and $\delta_e$. Schematic.
:::

Both conditions are linear in the two unknowns, with the elevator derivatives $C_{L\delta_e}$ and $C_{M\delta_e}$ of the next section:

:::{math}
:label: eq-trim-pair
\begin{aligned}
C_M &= 0 = C_{M0} + C_{M\alpha}\,\alpha_{trim} + C_{M\delta_e}\,\delta_{e,trim}\\
C_L &= \frac{W}{qS} = C_{L0} + C_{L\alpha}\,\alpha_{trim} + C_{L\delta_e}\,\delta_{e,trim}
\end{aligned}
:::

$C_{M0}$ and $C_{L0}$ are the values of the complete aircraft at $\alpha = 0$ and $\delta_e = 0$. The solution is

:::{math}
:label: eq-trim-solution
\alpha_{trim} = \frac{C_{M0}\,C_{L\delta_e} + C_{M\delta_e}\,(C_{L,trim} - C_{L0})}{C_{L\alpha}\,C_{M\delta_e} - C_{L\delta_e}\,C_{M\alpha}}, \qquad
\delta_{e,trim} = -\frac{C_{M0}\,C_{L\alpha} + C_{M\alpha}\,(C_{L,trim} - C_{L0})}{C_{L\alpha}\,C_{M\delta_e} - C_{L\delta_e}\,C_{M\alpha}}
:::

Each condition has one solution. In a turn, $C_{L,trim} = nW/(qS)$. The source is Nelson (1998), Chapter 2.

:::{figure} figures/trim-lines.svg
:label: fig-trim-lines
:alt: Pitching moment coefficient against angle of attack for three elevator settings. The three lines are parallel and fall with angle of attack. The line for an elevator deflection of 0 degrees crosses zero at 10 degrees. The line for minus 2 degrees lies above it and crosses zero at 16.6 degrees. The line for plus 2 degrees lies below it and crosses zero at 3.4 degrees.
:width: 75%

An elevator deflection shifts the $C_M$ line, and each setting trims at one $\alpha$. Computed with the derivatives of Gudmundsson (2022), Example 24-6.
:::

:::{admonition} Navy Jet Trainer
:class: navy

The trim analysis the RFP asks for is {eq}`eq-trim-pair` solved at every condition of {numref}`tbl-trim-conditions`. At which condition is your elevator deflection largest?
:::

## Elevator derivatives

The elevator changes the lift of the tail only. With the change of $C_{M,ac}^{T}$ dropped, the elevator derivatives are

:::{math}
:label: eq-elevator-derivatives
C_{L\delta_e} = \eta_H\frac{S_t}{S}\,C_{L\alpha}^{T}\,\tau, \qquad
C_{M\delta_e} = \eta_H C_{L\alpha}^{T}\,\tau\Big[\frac{S_t}{S}(\bar x_{cg} - \bar x_{ac}) - V_H\Big]
:::

For a plain flap with $E = c_e/\bar c_t$, thin-airfoil theory gives the flap effectiveness

:::{math}
:label: eq-tau
\tau = \frac{\cos^{-1}(1 - 2E) + 2\sqrt{E\,(1 - E)}}{\pi}
:::

:::{figure} figures/tau.svg
:label: fig-tau
:alt: Flap effectiveness tau against elevator chord ratio from 0 to 0.5. The thin-airfoil curve rises steeply from zero and reaches 0.66 at a chord ratio of 0.3 and 0.82 at 0.5. The empirical curve lies below it, about a quarter lower, and reaches 0.51 at a chord ratio of 0.3, marked with a dot, and 0.65 at 0.5.
:width: 70%

The flap effectiveness: thin-airfoil theory, {eq}`eq-tau`, and the empirical curve of Gudmundsson (2022), Eq. 24-86.
:::

The empirical curve of {numref}`fig-tau`, valid for $0.025 < E < 0.5$, runs 20% to 35% below {eq}`eq-tau` for $E$ from 0.1 to 0.5, and more below 0.1. Use the empirical curve. An all-moving tail has $\tau = 1$. Take $C_{L\alpha}^{T}$ and $\tau$ at the Mach number of the condition. An elevator deflection shifts the line of $C_M$ against $C_L$ and leaves its slope unchanged.

## The trim diagram

:::{figure} figures/trim-diagram.svg
:label: fig-trim-diagram
:alt: Two plots against trim lift coefficient from minus 0.5 to 2, one line for a forward CG, static margin 0.25, and one for an aft CG, static margin 0.05. Left, the trim angle of attack rises from about minus 9 to 22 degrees, and the two lines nearly coincide. Right, the trim elevator deflection falls with lift coefficient: from 15 to minus 25 degrees for the forward CG, and from 6 to minus 2 degrees for the aft CG. Dotted lines mark an elevator limit of plus and minus 20 degrees. The forward CG line meets the lower limit at a lift coefficient of 1.70, marked as the slowest trimmable speed.
:width: 100%

The trim diagram for two CG positions. Computed from invented derivatives.
:::

{numref}`fig-trim-diagram` plots $\alpha_{trim}$ and $\delta_{e,trim}$ against $C_{L,trim}$ for a forward CG and an aft CG. The two lines of $\alpha_{trim}$ nearly coincide. The forward CG needs the largest elevator deflection, trailing edge up, at high lift. The point where its line meets the elevator limit is the slowest speed the aircraft can trim. Draw one diagram for each configuration. Keep 5° to 10° of elevator travel for the flare and the gusts.

## Trim with thrust

{numref}`fig-thrust-trim` is drawn for the propeller aircraft of the textbook example below. The thrust $T$ acts along a line at a height $z_T$ above the CG, and a normal force $T_N$ acts at the propeller, a distance $x_T$ ahead of the CG.

:::{figure} figures/thrust-trim.svg
:label: fig-thrust-trim
:alt: Side view of a single-engine propeller aircraft, nose to the left, with a propeller disc at the nose, a wing, a horizontal tail, and a fin. The flow comes from the left. Lift, weight, and drag act at the CG. The thrust T acts forward along the propeller axis, a dashed line a height z T above the CG. A normal force T N acts upward at the propeller, a distance x T ahead of the CG. A curved arrow above the CG marks the moment about the CG, M cg, in the nose-up sense.
:width: 80%

Forces at the CG in flight-path axes, the thrust line $z_T$ above the CG, and the propeller normal force $T_N$ of the textbook example at $x_T$ ahead of it. Schematic: the forces and the thrust line after Gudmundsson (2022), Figure 24-42; $T_N$, $z_T$, and $x_T$ from his Example 24-7.
:::

With the thrust in the balance, the unknowns are $\alpha$, $\delta_e$, and $T$. For small $\alpha$, with the thrust along the flight path and the flaps fixed, the equations along the flight path, normal to it, and about the CG are (after Gudmundsson 2022, Eqs. 24-137 to 24-141):

:::{math}
:label: eq-trim-thrust
\begin{aligned}
C_{D\alpha}\,\alpha + C_{D\delta_e}\,\delta_e - \frac{T}{qS} &= -C_{D_{min}}\\
C_{L\alpha}\,\alpha + C_{L\delta_e}\,\delta_e &= \frac{W}{qS} - C_{L0}\\
C_{M\alpha}\,\alpha + C_{M\delta_e}\,\delta_e - \frac{z_T\,T}{qS\bar c} &= -C_{M0} - \frac{T_N\,x_T}{qS\bar c}
\end{aligned}
:::

Gudmundsson writes $C_{D_{min}}$; with $C_{L_{minD}}$ = 0 it is the $C_{D_0}$ of [Lecture 7](../lecture-07/drag-polar.md). The system is {eq}`eq-trim-pair` plus the drag balance, and each condition needs one linear solve. A thrust line above the CG pitches the nose down with power. $T_N$ is the propeller normal force of the textbook example below: ahead of the CG it pitches the nose up, and it is taken as a constant. For a jet, the corresponding normal force at the inlet is usually dropped on a first pass, and $x_T$ and $T_N$ leave the third equation.

### Textbook example: trim at two speeds

Gudmundsson (2022), Example 24-7, solves {eq}`eq-trim-thrust` for a propeller aircraft at two speeds.

:::{table} Inputs of Gudmundsson (2022), Example 24-7, a propeller aircraft with flaps up at sea level. Derivatives per radian.
:label: tbl-example-24-7-inputs

| Quantity | Value |
| --- | --- |
| $W$; $S$; $\bar c$ | 3,400 lb; 144.9 ft²; 3.78 ft |
| Thrust line; propeller; $T_N$ | 0.5 ft above the CG; 13.06 ft ahead of it; 50 lb |
| $C_{L\alpha}$, $C_{L\delta_e}$, $C_{L0}$ | 4.8, 0.355, 0.2 |
| $C_{M\alpha}$, $C_{M\delta_e}$, $C_{M0}$ | −0.72, −0.923, 0 |
| $C_{D_{min}}$, $C_{D\delta_e}$ | 0.0254, 0.000175 |
| $C_{D\alpha}$, fast and slow | 0.0863, 0.497 |
| Propeller efficiency, fast and slow | 0.85, 0.60 |

:::

:::{table} The solution of {eq}`eq-trim-thrust` at two speeds. Gudmundsson (2022), Example 24-7; with the inputs listed, $\alpha$ recomputes to 12.8° at 75 KCAS.
:label: tbl-example-24-7

| Quantity | 180 KCAS | 75 KCAS |
| --- | ---: | ---: |
| $q$ (lb/ft²) | 109.8 | 19.06 |
| $\alpha$ | 0.14° | 12.9° |
| $\delta_e$ | 0.36° | −7.26° |
| $T$ (lb) | 408 | 378 |
| Power (BHP) | 265 | 145 |

:::

At the low speed the aircraft needs 7° of elevator deflection, trailing edge up, and 13° of $\alpha$ at this CG. Repeat the solve at the forward limit. The 145 BHP is low, because the drag model of the example is simplified at high lift.

## Trim conditions to check

:::{table} The conditions at which to solve the trim equations. The speeds, altitudes, weights, and load factors are from the RFP; T is the threshold, O the objective.
:label: tbl-trim-conditions

| Condition | Navy Jet Trainer |
| --- | --- |
| Maximum operating speed, cruise | Mach 0.78 (T), Mach 0.90 (O) at 25,000 ft, at MTOW less 50% fuel; the design cruise; both CG limits |
| Climb | The training-flight climbs at 250 KCAS to 20,000 ft; the thrust line in {eq}`eq-trim-thrust`; both CG limits |
| Maneuver | Sustained +4.0 g (T), +6.0 g (O) at 15,000 ft, at MTOW less 50% fuel; elevator deflection per g at the aft CG |
| Takeoff rotation | MTOW, 5,000 ft density altitude, forward CG, takeoff flaps |
| Approach, landing | MLW, 5,000 ft density altitude; {term}`FCLP` on the 3.5° glide slope; forward CG |
| Engine-out case | Only with two engines; see [part 4](lateral-and-controls.md) |

:::

For each condition of {numref}`tbl-trim-conditions`, report $C_{L,trim}$, $\alpha_{trim}$, $\delta_{e,trim}$ against the limit, $C_{L}^{T}$ against the stall of the tail, and the trim drag. These results form the trim table. The condition with the largest deflection sizes the elevator, in [part 4](lateral-and-controls.md).

## Trim drag

The trimmed polar adds the induced drag of the tail to that of the wing, each at its own lift coefficient. $K$ is the induced-drag factor of [Lecture 7](../lecture-07/drag-polar.md), and $e_t$ the span efficiency of the tail:

:::{math}
:label: eq-trim-drag
C_D = C_{D_0} + K\,(C_{L}^{W})^{2} + \eta_H\frac{S_t}{S}\,\frac{(C_{L}^{T})^{2}}{\pi\, e_t\, AR_t}
:::

The two lift coefficients at trim are

:::{math}
:label: eq-trim-lifts
C_{L}^{W} = C_{L0}^{W} + C_{L\alpha}^{W}\,\alpha_{trim}, \qquad
C_{L}^{T} = C_{L\alpha}^{T}\,\alpha_{t} + C_{L\alpha}^{T}\,\tau\,\delta_{e,trim}, \qquad
\alpha_t = \alpha_{trim} + i_t - \varepsilon
:::

:::{figure} figures/trimmed-polar.svg
:label: fig-trimmed-polar
:alt: Drag coefficient against trim lift coefficient from minus 0.4 to 1.8, with invented inputs. The untrimmed polar of the wing alone, labeled untrimmed, wing only, and the trimmed polar start together near 0.025 at zero lift. As lift rises the trimmed polar lies above the untrimmed polar; at a lift coefficient of 1.8 it reaches 0.21 against 0.19.
:width: 75%

The trimmed polar against the untrimmed polar at a forward CG. Computed from invented inputs.
:::

A download on the tail makes the wing lift more than the weight. The induced drag of the wing rises, and the tail adds its own. The trim drag is largest at the forward CG and at high $C_L$. Compute one polar for each CG, on top of the build-up of [Lecture 7](../lecture-07/drag-polar.md).

:::{admonition} Navy Jet Trainer
:class: navy

How much does trim add to your cruise drag at the forward CG?
:::

## Maneuver and approach

The elevator deflection per g, with $\mu = 2W/(\rho\,g\,S\,\bar c)$, is (Etkin and Reid 1996, Section 3.1)

:::{math}
:label: eq-elevator-per-g
\frac{\Delta\delta_e}{n - 1} = -\frac{C_{L,1g}}{C_{M\delta_e}}\Big[\frac{C_{M\alpha}}{C_{L\alpha}} + \frac{C_{Mq}}{2\mu}\Big]
:::

$C_{L,1g} = W/(qS)$ is the lift coefficient in level flight at the speed of the pull-up. $C_{Mq}$ is the pitch damping, the derivative of $C_M$ with the nondimensional pitch rate $\hat q = Q\bar c/(2V)$, where $Q$ is the pitch rate; a value given per $Q\bar c/V$ must be doubled first. $C_{Mq}$ is negative, and the tail supplies most of it. $\mu$ is the relative mass parameter, not a friction coefficient. The maneuver point is $\bar x_m = \bar x_n - C_{Mq}/(2\mu)$. It lies aft of the neutral point. Compute $\delta_e$ at the load factor for both CG limits. The lift coefficient at $n$ g, $nW/(qS)$, must stay below the usable $C_{L_{max}}$, as in [Lecture 9](../lecture-09/trainer-boundaries.md).

On approach, the {term}`deck angle` is $\theta = \alpha_{trim} - \gamma_{app}$, with $\gamma_{app}$ the glide-slope angle, 3.5°, taken positive. Trim at the forward CG with the flaps down. Leave elevator travel for the flare, and keep the tail below its stall. The view over the nose must cover $\alpha_{trim}$ plus the angle from the flight path down to the carrier stern. The RFP requires the pilot to see the stern; see [Lecture 6](../lecture-06/high-lift-wing-and-field.md).

:::{admonition} Navy Jet Trainer
:class: navy

The RFP asks for +4.0 g (T) and +6.0 g (O) at 15,000 ft, and for FCLP on a 3.5° glide slope. How much elevator travel does each leave?
:::

:::{seealso}
Continue with [](lateral-and-controls.md): the fin, the dihedral effect, the control surfaces, the check with a vortex-lattice tool, and the work for the week. The references for the four parts are at the end of that page.
:::
