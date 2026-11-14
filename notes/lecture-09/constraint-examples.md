---
title: "Constraint analysis, part 3: Worked examples"
short_title: Worked examples
---

This is the third part of Lecture 9, *Constraint Analysis and the Design Point*. It works two aircraft through the method of [](constraint-method.md) and [](trainer-boundaries.md): the Cessna 162, a published textbook example, and the T-45C, a similar aircraft. Neither is your design. Reproduce both with your code before you draw your own diagram. The page closes with the work for the week. The figures are recomputed from the inputs listed here.

:::{note} What to take from this lecture
- A constraint code is checked on a published example before it is used on your aircraft.
- The Cessna 162 checks the cases of the master equation. The T-45C checks the thrust lapse, the weight fractions, and the field boundaries.
- Where an input is an estimate, the boundary that rests on it is checked first.
:::

## Cessna 162

The example is Gudmundsson (2022), Example 3-1. The Cessna 162 is a propeller aircraft. Its climb, turn, cruise, and ceiling boundaries are the cases of the master equation with $\alpha = \beta = 1$. Its takeoff boundary adds the drag and the rolling friction of the ground run. Gudmundsson writes $C_{D_{min}}$ and $K$; with $C_{L_{minD}}$ = 0 they are the $C_{D_0}$ and $K_1$ of the master equation ([Lecture 7](../lecture-07/drag-polar.md)).

:::{table} Inputs of the Cessna 162 example. Gudmundsson (2022), Example 3-1 and Table 3-1.
:label: tbl-c162-inputs

| Input | Value |
| --- | --- |
| Gross weight; wing area | 1,320 lb; 120 ft² |
| $AR$; $e$; $K = 1/(\pi\,AR\,e)$ | 8; 0.8106; 0.04909 |
| $C_{D_{min}}$ | 0.0333 |
| Takeoff | Ground run 640 ft at sea level; $C_{L_{max}}$ 1.756; rolling friction $\mu$ 0.04; $C_{L_{TO}}$ 0.5 and $C_{D_{TO}}$ 0.038 during the ground run |
| Climb | 880 ft/min at sea level, at the best rate-of-climb speed $V_Y$ = 43.591 + 2.2452 ($W/S$) in KCAS |
| Cruise | 108 KTAS at 8,000 ft, where $\rho$ = 0.001869 slug/ft³ |
| Sustained turn | 30° bank, $n$ = 1.155, at 108 KTAS and 8,000 ft |
| Service ceiling | 15,000 ft, where the density ratio $\sigma$ = 0.6292; 100 ft/min at $V_Y$ |
| Landing | 1,369 ft over 50 ft; this limits $W/S$ to 11.37 lb/ft² |

:::

:::{table} The cases as the example uses them, with $dh/dt$ the rate of climb in ft/s. After Gudmundsson (2022), Eqs. 3-1, 3-2, 3-7, 3-10, and 3-11.
:label: tbl-c162-cases

| Requirement | $T/W$ |
| --- | --- |
| Takeoff ground run | $\dfrac{1.21}{g\,\rho\,C_{L_{max}}}\dfrac{W/S}{s_G} + \dfrac{0.605}{C_{L_{max}}}\left(C_{D_{TO}} - \mu\,C_{L_{TO}}\right) + \mu$ |
| Climb | $\dfrac{dh/dt}{V} + \dfrac{q\,C_{D_{min}}}{W/S} + \dfrac{K}{q}\dfrac{W}{S}$ |
| Sustained turn | $q\left[\dfrac{C_{D_{min}}}{W/S} + K\left(\dfrac{n}{q}\right)^{2}\dfrac{W}{S}\right]$ |
| Cruise | $\dfrac{q\,C_{D_{min}}}{W/S} + \dfrac{K}{q}\dfrac{W}{S}$ |
| Service ceiling | The climb form with $dh/dt$ = 1.667 ft/s, $q$ at sea level and $V_Y$, and $V = V_Y/\sqrt{\sigma}$ |

:::

### Thrust to power

A propeller aircraft is sized in power. Each $T/W$ boundary becomes sea-level power in three steps (Gudmundsson 2022, Eqs. 3-15 to 3-17):

1. The thrust at the condition is $T = (T/W)\,W$.
2. The power is $P = T\,V/(550\,\eta_p)$ in hp, with $T$ in lb, the true airspeed $V$ in ft/s, and the propeller efficiency $\eta_p$ at that speed.
3. For a piston engine, the Gagg and Ferrar model gives the sea-level power, $P_{SL} = P/(1.132\,\sigma - 0.132)$.

The example uses $\eta_p$ = 0.60 at the liftoff speed $V_{LOF} = 1.1\,V_S$, 0.65 for the climb and the ceiling, and 0.75 for the cruise and the turn. At rest $\eta_p$ is zero and step 2 fails. The takeoff boundary is therefore converted at a speed on the ground run, here $V_{LOF}$.

:::{table} The Cessna 162 boundaries at $W/S$ = 10 lb/ft². $T/W$ as Gudmundsson (2022) prints it; $P_{SL}$ recomputed.
:label: tbl-c162-values

| Requirement | $T/W$ | $P_{SL}$ (hp) |
| --- | ---: | ---: |
| Ground run of 640 ft | 0.187 | 56.9 |
| 880 ft/min at $V_Y$, sea level | 0.214 | 88.1 |
| 30° bank at 108 KTAS, 8,000 ft | 0.125 | 95.9 |
| Cruise at 108 KTAS, 8,000 ft | 0.119 | 91.8 |
| Service ceiling of 15,000 ft | 0.094 | 84.3 |

:::

The cruise at $W/S$ = 10 lb/ft² needs 69.5 hp at 8,000 ft, or 91.8 hp at sea level. Gudmundsson, with $T/W$ rounded to 0.1192, prints 69.56 hp and 92 hp.

:::{figure} figures/c162-diagram.svg
:label: fig-c162-diagram
:alt: Two constraint diagrams of the Cessna 162 against wing loading, each with takeoff, climb, turn, cruise, and ceiling boundaries and a vertical landing boundary at 11.37 pounds per square foot. Left, thrust-to-weight ratio. The takeoff line rises from 0.10 to 0.47, the climb curve falls from 0.26 to 0.16, the turn and cruise curves fall from 0.27 at 4 pounds per square foot to about 0.1 above 12, and the ceiling curve stays between 0.09 and 0.11. The lowest feasible value is 0.208, on the climb curve at the landing boundary. Right, sea-level power in horsepower. The turn and cruise curves fall steeply from about 205, and the climb, ceiling, and takeoff curves rise from 87, 81, and 20 to 111, 133, and 247. The lowest feasible power is 89.3 at a wing loading of 11.2, where the turn and climb curves cross.
:width: 100%

The Cessna 162 in thrust-to-weight ratio and in sea-level power. Recomputed from {numref}`tbl-c162-inputs`; after Gudmundsson (2022), Figure 3-2.
:::

The lowest point differs between the two diagrams. In $T/W$, the climb and the landing boundary set it. In power, the turn and the climb set it. The ceiling boundary here follows Eq. 3-11, with $V_Y$ changing with the wing loading. The book's figure holds the dynamic pressure fixed for that curve, and the two agree only at $W/S$ = 10 lb/ft².

:::{figure} figures/c162-design-point.svg
:label: fig-c162-design-point
:alt: Sea-level power against wing loading for the Cessna 162, with the same five boundaries and the landing boundary, and a second vertical axis for the maximum lift coefficient. Two straight lines through the origin give the maximum lift coefficient that a stall speed needs: a steep line for 45 knots and a flatter line for 61 knots. The design point is marked at a wing loading of 11.2 and 89 horsepower. An arrow rises from it to the 45 knot line and runs right to the second axis, where it reads 1.63.
:width: 85%

The design point, and the $C_{L_{max}}$ that a stall speed needs, $C_{L_{max}} = (W/S)/q_{stall}$. Recomputed; after Gudmundsson (2022), Figure 3-3.
:::

Gudmundsson's design point is 11.2 lb/ft² and 89.4 hp. This recomputation gives 89.3 hp at the same wing loading. A stall speed of 45 KCAS then needs $C_{L_{max}}$ = 1.63; Gudmundsson reads 1.62 from his figure.

## T-45C Goshawk

The T-45C is the trainer the RFP replaces. Its diagram uses the thrust form of the master equation with the low-bypass lapse of [Lecture 8](../lecture-08/engine-models.md).

:::{table} Published values of the T-45C. The weight limits, the stall speeds, and the approach speed are from the NATOPS flight manual and the Training Air Wing One checklist card (2011). The thrust is from the U.S. Navy fact file. The wing area, the fuel, the speed, the climb, the ceiling, and the distances are public type data credited to Jane's; confirm them against the NATOPS manual.
:label: tbl-t45-published

| Quantity | Value |
| --- | --- |
| Weight limits, takeoff and landing | 14,500 lb; 13,360 lb |
| Wing area; span | 190.1 ft²; 30 ft 10 in |
| Internal fuel | 2,893 lb |
| Engine, installed static thrust | F405-RR-401, 5,527 lb |
| Maximum speed | 543 kt at 8,000 ft, Mach 0.84 at that altitude |
| Rate of climb at sea level | 8,000 ft/min |
| Service ceiling | 42,500 ft |
| Takeoff to 50 ft; landing from 50 ft | 3,610 ft; 3,310 ft |
| Stall speed at 11,500 lb, power on | 99 KIAS with half flaps; 94 KIAS with full flaps |
| Approach speed at 11,500 lb, full flaps | 116 KIAS, held to touchdown |

:::

:::{table} Values derived from {numref}`tbl-t45-published`, and the condition of each boundary.
:label: tbl-t45-derived

| Quantity | Value |
| --- | --- |
| Aspect ratio | 5.0 |
| $\beta$ at MTOW less 50% of the internal fuel | (14,500 − 1,447)/14,500 = 0.90, for the maximum speed, the climb, and the ceiling |
| $\beta$ at takeoff; at landing | 1.0; 13,360/14,500 = 0.92 |
| $C_{L_{max}}$ from the stall speeds at 11,500 lb | 1.82 with half flaps, for the takeoff; 2.02 with full flaps, for the landing |
| $k_{TD}$ | 116/94 = 1.23 |
| $K_1 = 1/(\pi\,AR\,e)$, with the estimated $e$ | 0.080 |
| Actual point | $W_{TO}/S$ = 76.3 lb/ft²; $T_{SL}/W_{TO}$ = 0.38 |

:::

:::{table} Estimated inputs of the T-45C example.
:label: tbl-t45-estimated

| Quantity | Value |
| --- | --- |
| $C_{D_0}$; $C_{D_c}$; $e$ | 0.020; 0.015 at Mach 0.84; 0.80 |
| $\alpha$ | Low-bypass lapse at military thrust, {term}`throttle ratio` 1.07; Mach 0.1 for the takeoff |
| Speed for the climb, at sea level; speed at the ceiling | 300 KCAS; Mach 0.70 |
| Rate of climb at the service ceiling | 100 ft/min |
| Ground run, at sea level; $k_{TO}$ | 0.7 × 3,610 = 2,530 ft; 1.10 |
| Landing, at sea level | 3.5° approach from 50 ft; 1 s of free roll; $\mu_B$ = 0.40 |

:::

The landing boundary comes from {eq}`eq-landing-boundary` of [part 1](constraint-method.md). The braking roll is the landing distance less the air distance on the 3.5° approach and less the free roll. MIL-STD-3013 uses the power-off stall speed; the stall speeds here are power on.

:::{figure} figures/t45-diagram.svg
:label: fig-t45-diagram
:alt: Constraint diagram of the T-45C: thrust-to-weight ratio against wing loading from 30 to 120 pounds per square foot. The maximum speed curve falls from 0.8 to 0.21. The climb curve falls slowly from 0.39 to 0.27. The ceiling curve falls from 0.43 to a minimum near 0.33 and rises to 0.38. The takeoff line rises from 0.10 to 0.41. A vertical landing boundary stands at 99. The feasible region is shaded above the highest boundary and left of the landing boundary. The T-45C is marked at 76.3 and 0.38, inside the region and just above the ceiling and maximum speed curves.
:width: 90%

The constraint diagram of the T-45C from the inputs of {numref}`tbl-t45-published` to {numref}`tbl-t45-estimated`. The point is the T-45C at its takeoff weight limit, with the installed static thrust. Computed.
:::

:::{table} The T-45C boundaries at $W_{TO}/S$ = 76.3 lb/ft².
:label: tbl-t45-values

| Boundary | $T_{SL}/W_{TO}$ |
| --- | ---: |
| Service ceiling | 0.33 |
| Maximum speed | 0.32 |
| Climb | 0.29 |
| Takeoff | 0.26 |
| Landing | $W_{TO}/S \le 99$ lb/ft² |

:::

The T-45C at 0.38 is about 16% above the highest boundary, the ceiling, and the landing boundary is 23 lb/ft² to its right. The two highest boundaries rest on estimates: $\alpha$ at altitude and $C_{D_c}$. Check them first. With $k_{TD}$ = 1.10 in place of 1.23, the landing boundary moves right by a factor of about $(1.23/1.10)^{2}$.

:::{admonition} Navy Jet Trainer
:class: navy

Where do the other aircraft of your A02 cohort lie on these axes, and what does that say about the estimated inputs?
:::

## This week

1. Code the master equation with your polar and your installed deck. Reproduce the Cessna 162 and the T-45C values first.
2. Draw one boundary for each RFP requirement, at the weight and the altitude the RFP states, in the standard atmosphere. Draw the threshold and the objective where both exist.
3. State the speed at which you read the specific excess power and the sustained load factor.
4. Plot the A02 cohort on the same axes.
5. Choose the design point. Report the active boundaries and the margin to each.
6. Enter $W_{TO}/S$ and $T_{SL}/W_{TO}$ in ASORT and run the sizing code again.

:::{tip}
Assignment A06, on Brightspace, asks for the boundaries and their inputs, the code checked on the two examples, the diagram, the design point, and the sizing run again there. The performance analysis starts from this design point.
:::

:::{important} Summary
- Every point requirement is a boundary in wing loading and thrust-to-weight ratio, drawn from the same inputs as the sizing code.
- The trainer's point requirements set the thrust at altitude: the maximum operating speed, the specific excess power, and the sustained load factor. The field lengths add boundaries in thrust and a limit on the wing loading.
- The design point is chosen inside the feasible region with stated margins, and the sizing code closes the loop.
:::

:::{exercise} For discussion
:label: ex-constraint

The T-45C lies about 16% above its highest boundary, and its two highest boundaries rest on an estimated lapse and an estimated compressibility drag. Take your design point and its nearest boundary. Which input of that boundary is an estimate? How far does the boundary move if the input is wrong by 10%? Is the margin larger than that?
:::

:::{seealso} Reading
Mattingly et al. (2002), Chapter 2, and Gudmundsson (2022), Chapter 3. [Lecture 10](../lecture-10/cg-and-envelope.md) covers stability and control: the CG, the tail, trim, and the control surfaces.
:::

## References

- Mattingly, J. D., Heiser, W. H., and Pratt, D. T., *Aircraft Engine Design*, 2nd ed., AIAA Education Series, 2002. Chapter 2.
- Gudmundsson, S., *General Aviation Aircraft Design: Applied Methods and Procedures*, 2nd ed., Butterworth-Heinemann, 2022. Chapter 3.
- MIL-STD-3013, *Glossary of Definitions, Ground Rules, and Mission Profiles to Define Air Vehicle Performance Capability*, U.S. Department of Defense, 2003. The RFP refers to revision B.
- Naval Air Systems Command, *NATOPS Flight Manual, Navy Model T-45C*, A1-T45AC-NFM-000.
- U.S. Navy, *T-45C Goshawk training aircraft*, fact file.
- AIAA 2026-27 Undergraduate Team Aircraft Design Competition RFP, *Design of a Navy Jet Training Aircraft*; see [](../navy-rfp/navy-rfp.md).
