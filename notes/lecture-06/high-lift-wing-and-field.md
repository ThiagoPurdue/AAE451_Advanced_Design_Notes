---
title: "High lift, part 2: The wing and the field length"
short_title: The wing and the field length
---

This is the second part of Lecture 6, *High-Lift Systems*. It carries the section increments of [](high-lift-devices.md) to the wing: partial-span flaps, the partition method, trim and deck angle, the FCLP approach, the drag penalty, and climb. It then turns the field length into the maximum lift the wing must reach: the reference speeds, the takeoff and landing segments, a worked example, and the required $C_{L_{max}}$. The figures are redrawn after the figures on the slides and reduced to the point each slide makes.

:::{note} What to take from this lecture
- The wing value comes from the section increments, the flapped span, and the hinge-line sweep.
- Flaps lower $\alpha_{stall}$ and the {term}`deck angle`; slats raise both. The FCLP view over the nose depends on the net change.
- Flap drag is paid in the climb gradient and, for FCLP, in fuel.
- The field length sets the stall speed, and the stall speed sets the required maximum lift.
:::

## Partial-span flaps

:::{figure} figures/partial-span-flaps.svg
:label: fig-partial-span
:alt: Left, a half wing in top view with the flap shaded along the inboard trailing edge and the aileron along the outboard trailing edge. Right, section lift coefficient along the span: flaps up, a gently falling line; flaps down, the same line raised over the flapped span, near the flapped section's maximum.
:width: 100%

Flaps inboard, ailerons outboard, and what the flaps do to the spanwise lift. Schematic, after Gudmundsson (2022), Figure 10-52.
:::

- Full-span flaps: the outboard segment is also the aileron.
- Flaps move the stall outboard. Check roll control at stall.

:::{admonition} Navy Jet Trainer
:class: navy

Where do the flaps end and the ailerons start on the trainers in your A02 database, and what fraction of the span is flapped?
:::

## Wing partition method

:::{figure} figures/wing-partition.svg
:label: fig-wing-partition
:alt: A half wing in top view divided into four segments by spanwise stations at 0, 3, 11.75, 16.42, and 19.15 feet: segment I, root, 14.88 square feet; segment II, flap, 36.49 square feet, shaded; segment III, aileron, 15.27 square feet; segment IV, tip, 7.57 square feet.
:width: 85%

The half wing split at the ends of the flap and the aileron, with the segment areas of the SR22 example below. After Gudmundsson (2022), Figure 10-54 and Table 10-8.
:::

:::{math}
:label: eq-partition
C_{L_{max}} \approx \frac{0.9}{S}\left[\sum_{flapped} C_{l_{max},i}\,S_i\cos\Lambda_{hinge,i} + \sum_{unflapped} C_{l,i}\,S_i\right]
:::

1. Split the wing at the ends of the flap and the aileron.
2. Flapped segments: the section $C_{l_{max}}$ with the device increment.
3. Unflapped segments: the section $C_l$ at the flapped section's $\alpha_{stall}$.
4. Sum by area over both half wings. The factor 0.9 covers the finite wing (Gudmundsson 2022, Eq. 10-2).

:::{admonition} Navy Jet Trainer
:class: navy

Swept hinge lines lose lift by $\cos\Lambda_{hinge}$. Count it.
:::

## Worked example: Cirrus SR22, flaps 32°

:::{table} The partition sum for one half wing. The flap row includes $\cos 4°$ for the hinge line. Gudmundsson (2022), Example 10-3, Tables 10-8 and 10-9.
:label: tbl-sr22-partition

| Segment | Station (ft) | $S_i$ (ft²) | $C_l$ | $S_i\,C_l$ |
| --- | --- | ---: | ---: | ---: |
| I, root | 0 to 3.00 | 14.88 | 1.562 | 23.24 |
| II, flap | 3.00 to 11.75 | 36.49 | 2.662 | 96.90 |
| III, aileron | 11.75 to 16.42 | 15.27 | 1.562 | 23.85 |
| IV, tip | 16.42 to 19.15 | 7.57 | 1.562 | 11.83 |
| Sum, one half wing | | | | 155.81 |

:::

Section data: clean $C_{l_{max}}$ = 1.62 at $\alpha_{stall}$ = 16°; flaps 32°, $C_{l_{max}}$ = 2.66 at $\alpha_{stall}$ = 12°; the clean section at 12° gives $C_l$ = 1.562.

Result: $C_{L_{max}} = 0.9\,(2)(155.81)/144.9 = 1.94$. The handbook value is 1.99; the estimate is 97% of it.

:::{admonition} Navy Jet Trainer
:class: navy

One flapped segment carries 62% of the sum. Flap span matters as much as flap type.
:::

## Trim and deck angle

:::{figure} figures/slot-lift-curve.svg
:label: fig-slot-lift-curve
:alt: Lift coefficient against angle of attack for a clean airfoil, peaking at about 1.4 near 12 degrees, and for the same airfoil with a fixed slot, which follows the same line and continues to a higher peak of about 2.0 near 18 degrees.
:width: 75%

A fixed slot delays the stall. Schematic, after Gudmundsson (2022), Figure 8-61, which shows the Clark Y with and without a slot.
:::

::::{grid} 1 1 2 2

:::{card}
:header: Flaps
Nose-down pitching moment. The tail download to trim reduces the usable $C_{L_{max}}$. $\alpha_{stall}$ falls by 1° to 5°, plain to single-slotted: a lower deck angle.
:::

:::{card}
:header: Leading-edge devices
A small effect on trim. $\alpha_{stall}$ rises by 5° to 11°: a higher deck angle. Combined with flaps, the net rise is small.
:::

::::

## The FCLP approach

:::{figure} figures/t45-landing.jpg
:label: fig-t45-landing
:alt: A T-45C Goshawk on final approach in the landing configuration, gear down, flaps and slats extended, nose high.
:width: 60%

T-45C Goshawk, landing configuration. Leading-edge slats were added to the Hawk wing, and the published approach speed is 125 kt (Wikipedia, *McDonnell Douglas T-45 Goshawk*). Photo: National Museum of the U.S. Navy, public domain, via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:160423-YB023-N-023_(26721993536).jpg).
:::

:::{figure} figures/fclp-approach.svg
:label: fig-fclp-approach
:alt: Side view, not to scale. The pilot's eye is on a body axis drawn nose up. The flight path runs down from the eye to an aim point on the ground at the glide-slope angle gamma of 3.5 degrees. A sight line runs from the eye to the carrier stern on the ground, short of the aim point. Arcs mark the approach angle of attack between the body axis and the flight path, and the view over the nose, the angle between the body axis and the sight line to the stern.
:width: 85%

The FCLP approach. With $\alpha_{pa}$ the approach angle of attack, the deck angle on the glide slope is $\theta = \alpha_{pa} - \gamma$, and the view over the nose must cover $\alpha_{pa}$ plus the angle from the flight path down to the stern. Schematic, not to scale.
:::

Flaps lower $\alpha_{pa}$. Flying slower on a slat raises it.

:::{admonition} Navy Jet Trainer
:class: navy

MIL-STD-3013 has a land-based and a carrier approach speed. The RFP aircraft is land based and flies FCLP: state which one you apply.
:::

## The high-lift drag penalty

:::{math}
:label: eq-flap-drag
\Delta C_{D_{flap}} = \Delta_1\,\Delta_2\,\frac{S_{flap}}{S}
:::

:::{figure} figures/flap-drag.svg
:label: fig-flap-drag
:alt: Flap drag coefficient increment at 30 and 50 degrees of deflection for three flap types, drawn as lines between the two points: plain or split from 0.050 to 0.100, Fowler from 0.032 to 0.083, slotted from 0.020 to 0.050.
:width: 70%

The drag increment of a flap of 60% span and 25% chord at two deflections. Values from Gudmundsson (2022), Figure 16-63, Eq. 16-166, and Table 16-18.
:::

:::{table} The values plotted in {numref}`fig-flap-drag`: $\Delta C_D$ of a flap of 60% span and 25% chord. Gudmundsson (2022), Table 16-18.
:label: tbl-flap-drag

| Flap | 30° | 50° |
| --- | ---: | ---: |
| Plain or split | 0.050 | 0.100 |
| Slotted | 0.020 | 0.050 |
| Fowler | 0.032 | 0.083 |

:::

Takeoff: partial deflection, for the climb $L/D$. Landing: full deflection, for the steeper approach.

:::{admonition} Navy Jet Trainer
:class: navy

FCLP is flown for 30 minutes in the landing configuration. The flap drag of that half hour is in the mission fuel.
:::

## Climb in the high-lift configuration

:::{table} Climb requirements in the high-lift configuration. MIL-STD-3013; the RFP cites revision B.
:label: tbl-highlift-climb

| Case | Configuration | Minimum |
| --- | --- | --- |
| Obstacle clearance speed | Gear up, takeoff flaps, takeoff thrust | 2.5% potential gradient |
| Approach speed | Gear up, approach configuration, takeoff thrust | 2.5% potential gradient |

:::

:::{admonition} Navy Jet Trainer
:class: navy

Flap drag sets the gradient in each configuration.
:::

## Reference speeds

:::{table} Speed factors on the stall speed. MIL-STD-3013 (2003 issue), Sections 3.2.3, 3.2.4, 3.8.1, and 3.8.2, uses the power-off stall speed, and each speed is the highest of several criteria. The SR22 example below uses the former Part 23 factors, §23.51 and §23.73, as in Gudmundsson (2022), Tables 18-3 and 23-4; the touchdown factor is his analysis assumption.
:label: tbl-reference-speeds

| Speed | MIL-STD-3013 | Former Part 23 |
| --- | --- | --- |
| Liftoff | 1.10 $V_S$ | 1.1 $V_{S1}$ |
| At 50 ft, takeoff | 1.20 $V_S$ | 1.2 $V_{S1}$ |
| At 50 ft, approach | 1.20 $V_S$ | 1.3 $V_{S0}$ |
| Touchdown | 1.10 $V_S$ | 1.1 $V_{S0}$ |

:::

:::{admonition} Navy Jet Trainer
:class: navy

The RFP cites MIL-STD-3013B for the speed definitions. Use its factors, not the Part 23 ones.
:::

## Takeoff over an obstacle

:::{figure} figures/takeoff-segments.svg
:label: fig-takeoff-segments
:alt: Side view of a takeoff from brake release. The ground run ends at the rotation speed, a short rotation ends at liftoff, a circular transition arc reaches the climb angle at the transition height, and a straight climb reaches the 50 ft obstacle at the speed V2 of 1.2 times the stall speed. Arrows mark the four distances: ground run, rotation, transition, and climb.
:width: 100%

The takeoff segments. After Gudmundsson (2022), Figures 18-2 and 18-14.
:::

:::{math}
:label: eq-takeoff
\begin{aligned}
S_G &= \frac{V_R^{2}\,W}{2g\left[T-D-\mu\,(W-L)\right]} \quad \text{evaluated at } V_R/\sqrt{2} \\
S_{ROT} &= V_{LOF}\,(1\ \text{s}), \quad \text{large aircraft 3 s} \\
\sin\gamma &= \frac{T}{W}-\frac{1}{L/D} \\
R &= 0.2156\,V_{S1}^{2} \\
S_{TR} &= R\sin\gamma, \qquad h_{TR} = R\,(1-\cos\gamma) \\
S_C &= \frac{h_{obst}-h_{TR}}{\tan\gamma}
\end{aligned}
:::

Speeds in ft/s, distances in ft. Dry pavement, rolling: $\mu$ = 0.03 to 0.05. The radius is $R = V_{TR}^{2}/[g\,(n-1)]$ with $V_{TR} = 1.15\,V_{S1}$ and $n$ = 1.19, the load factor of 0.9 $C_{L_{max}}$ at 1.15 $V_{S1}$; that gives 0.216, and Gudmundsson prints 0.2156, which the SR22 example uses. If the obstacle is cleared during the transition, $S_{obst} = \sqrt{R^{2}-(R-h_{obst})^{2}}$. Gudmundsson (2022), Eqs. 18-22 to 18-32.

:::{admonition} Navy Jet Trainer
:class: navy

The climb angle comes from $T/W$ and from $L/D$ in the takeoff configuration.
:::

## Landing over an obstacle

:::{figure} figures/landing-segments.svg
:label: fig-landing-segments
:alt: Side view of a landing from the 50 ft obstacle. A straight approach at the approach angle, starting at the approach speed, ends at the flare height, a circular flare reaches the ground at the touchdown speed, a short free roll follows, and the braking roll ends at the stop. Arrows mark the four distances: approach, flare, free roll, and braking.
:width: 100%

The landing segments. After Gudmundsson (2022), Figure 23-3.
:::

:::{math}
:label: eq-landing
\begin{aligned}
h_F &= 0.1512\,V_{S0}^{2}\,(1-\cos\gamma_{app}) \\
S_A &= \frac{h_{obst}-h_F}{\tan\gamma_{app}} \\
S_F &= 0.1512\,V_{S0}^{2}\,\sin\gamma_{app} \\
S_{FR} &= V_{TD}\,(1\ \text{s}), \quad \text{large aircraft 3 s} \\
S_{BR} &= \frac{V_{BR}^{2}\,W}{2g\left[\mu\,(W-L)+D-T\right]} \quad \text{evaluated at } V_{BR}/\sqrt{2}
\end{aligned}
:::

Speeds in ft/s, distances in ft. Dry pavement, braking: $\mu$ = 0.3 to 0.5. Reverse thrust: $T < 0$. The constant 0.1512 is $R = V^{2}/[g\,(n-1)]$ at $1.2\,V_{S0}$ with $n$ = 1.296, the load factor of 0.9 $C_{L_{max}}$ at 1.2 $V_{S0}$ (Gudmundsson 2022, Eqs. 23-10 and 23-11). Lift during the roll unloads the wheels: dump it. Gudmundsson (2022), Eqs. 23-8 to 23-16.

:::{admonition} Navy Jet Trainer
:class: navy

Re-derive the two constants, 0.2156 and 0.1512, for the speed factors of MIL-STD-3013B.
:::

## Worked example: Cirrus SR22 field lengths

:::{figure} figures/sr22-field-lengths.svg
:label: fig-sr22-field-lengths
:alt: Two horizontal stacked bars in feet. Takeoff: ground run 963, rotation 119, transition 406, climb 104, total 1,592 against a handbook value of 1,594. Landing: approach 914, flare 79, free roll 110, braking 1,019, total 2,122 against a handbook value of 2,344. Ground segments are gold, air segments gray.
:width: 100%

The SR22 takeoff and landing, segment by segment, against the handbook. Gudmundsson (2022), Examples 18-7, 18-8, and 23-1.
:::

Conditions: sea level, ISA, 3,400 lb. Takeoff with $C_{L_{max}}$ = 1.69 and a climb at 9.3°. Landing with $V_{S0}$ = 59 KCAS, an approach at 3°, and $\mu$ = 0.3.

The ground run is 60% of the takeoff. At 3°, the approach from 50 ft is 43% of the landing.

:::{admonition} Navy Jet Trainer
:class: navy

Reproduce both SR22 cases with your code before you solve your own field length.
:::

## Required maximum lift

1. Field length, weight, and atmosphere from the RFP.
2. Approach angle, braking coefficient, thrust: each one a dated {term}`ASORT` assumption.
3. Solve the landing equations for $V_{S0}$ and the takeoff equations for $V_{S1}$.
4. Convert to $C_{L_{max}}$ at the ASORT {term}`wing loading`.
5. Compare with the value your system reaches.

:::{math}
:label: eq-required-clmax
C_{L_{max}}^{\,req} = \frac{2\,(W/S)}{\rho_0\,\sigma\,V_S^{2}}
:::

:::{table} The density ratio of the RFP condition, from the standard atmosphere.
:label: tbl-density-ratio

| RFP condition | $\sigma$ |
| --- | ---: |
| 5,000 ft density altitude | 0.862 |

:::

:::{iframe} ../quickcheck/required-clmax.html
:label: qc-required-clmax
:width: 100%

Quick check: the maximum lift coefficient a field requires, from {eq}`eq-required-clmax`, and the approach speed. Shuffle gives new values; the solution shows the steps.
:::

:::{admonition} Navy Jet Trainer
:class: navy

MLW is yours to define. $W/S$ is provisional until the constraint diagram fixes the design point.
:::

## This week

1. Choose the devices. Justify the choice against the field requirement. Describe them: the RFP requires it.
2. Section increments from published data. The wing partition method. Takeoff and landing $C_{L_{max}}$.
3. Stall speeds at the ASORT wing loading, with the speed definitions of MIL-STD-3013B.
4. The required $C_{L_{max}}$ from the field length.
5. Draw the devices on the three-view. Enter every value in ASORT.

:::{tip}
Where exact wording matters, read the RFP and MIL-STD-3013B, not this page.
:::

:::{important} Summary
- Each device buys maximum lift and costs drag, pitching moment, weight, and complexity.
- The wing value comes from the section increments, the flapped span, and the hinge-line sweep.
- The field length sets the stall speed, and the stall speed sets the required maximum lift.
:::

:::{exercise} For discussion
:label: ex-high-lift

Take the T-45 from your A02 database: its wing area, its published approach speed, and its landing weight if you can find one. Which $C_{L_{max}}$ does that approach speed imply at sea level, with the MIL-STD-3013 factor of 1.2 on the stall speed? Which row of {numref}`tbl-typical-clmax` does it fall in, and does that match the devices you see in {numref}`fig-t45-landing`?
:::

:::{seealso} Reading
Gudmundsson (2022), Chapter 10. [Lecture 7](../lecture-07/parasite-drag.md) covers drag: the parasite drag build-up and the polar, with the takeoff and landing polars from the flap settings and increments of this lecture. [](../assignments/a04.md) states what Deliverable 3 asks for.
:::

## References

- Gudmundsson, S., *General Aviation Aircraft Design: Applied Methods and Procedures*, 2nd ed., Butterworth-Heinemann, 2022. Chapters 8, 10, 16, 18, and 23.
- Anderson, J. D., *Aircraft Performance and Design*, McGraw-Hill, 1999. Table 5.3.
- Department of Defense, *MIL-STD-3013, Glossary of Definitions, Ground Rules, and Mission Profiles to Define Air Vehicle Performance Capability*, 14 February 2003. The RFP cites revision B, 2022.
- 14 CFR Part 23, *Airworthiness Standards: Normal Category Airplanes*, Amendment 23-64, for the former speed factors used in the SR22 example.
- AIAA 2026-27 Undergraduate Team Aircraft Design Competition RFP, *Design of a Navy Jet Training Aircraft*; see [](../navy-rfp/navy-rfp.md).
