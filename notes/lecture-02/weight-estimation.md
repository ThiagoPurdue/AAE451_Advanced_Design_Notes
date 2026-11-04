---
title: Starting from weight and the empty weight
short_title: Weight estimation
---

This is the first part of Lecture 2, *Aircraft Sizing*. It covers why the takeoff weight comes first, how the empty weight is estimated from aircraft that exist, how good that estimate is, and how the engine is represented during sizing. The second part, [](mission-fuel.md), covers the design mission, the fuel weight, and the sizing loop.

:::{note} What to take from this lecture
- Empty weight and fuel weight are both functions of the takeoff weight you are trying to find. That is why sizing is iterative.
- Some of the numbers in the mission-segment and fuel-fraction equations come from your RFP. The rest are yours to assume, and to state.
- Your team's sizing code has to compute the takeoff weight before center of gravity or performance analysis can follow.
:::

## Starting from weight

The design process begins with an estimate of the takeoff weight, $W_0$, before the geometry is known. Three sizing variables usually matter most: wing loading $W_0/S$, thrust-to-weight ratio $T/W_0$ (or power-to-weight ratio for propeller aircraft), and aspect ratio $AR$.

:::{prf:definition} Nonexpendable and expendable payload
:label: def-payload

Nonexpendable payload stays aboard for the whole mission. Expendable payload is used up or dropped in flight.
:::

:::{important}
Empty weight is the weakest link in conceptual design. Validate it against real aircraft wherever you can.
:::

:::{admonition} Navy Jet Trainer
:class: navy

Each pilot, whose nude weight the RFP bounds at 103 to 205 lb, plus the 35 lb of flight suit, equipment, and survival kit the RFP adds per pilot, is nonexpendable payload. The RFP names no expendable payload. Where do the two Martin-Baker Mk 14 seats, or similar, sit in your roll-up, payload or empty weight, and why? The {term}`MTOW` roll-up the RFP asks for starts from these items.
:::

## Empty weight from a trend line

Nicolai and Carichner (2010), Appendix I, draw one empty-weight trend line per aircraft class, three for fighters, on log axes of empty weight against takeoff gross weight. Figure I.4 plots fifteen jet trainers, three of them proposal weights for aircraft that were never built, from the T-37B to the M-346 and the T-45A Goshawk. They lie close to the line $W_e = 0.747\,W_{TO}^{0.993}$. Figure I.3 plots fifteen light civil aircraft of conventional metal structure around $W_e = 0.911\,W_{TO}^{0.947}$, the same line as multipurpose fighters and transports. {numref}`fig-empty-weight-trends` draws the two lines.

```{figure} figures/empty-weight-trends.svg
:label: fig-empty-weight-trends
:alt: Log-log plot of empty weight against takeoff gross weight from 1,000 to 100,000 pounds. A solid line for military jet trainers, empty weight equals 0.747 times takeoff weight to the power 0.993, lies above a dashed line for multipurpose fighters and light civil aircraft, empty weight equals 0.911 times takeoff weight to the power 0.947. A square marks the Grumman F9F-5 at 17,500 pounds takeoff weight and 10,223 pounds empty weight, between the two lines and closer to the dashed one.
:width: 85%

Empty-weight trend lines from Nicolai and Carichner (2010), Table 5.1, with the Grumman F9F-5 from their Table I.5a. Nicolai's Figures I.4 and I.3 plot fifteen aircraft around each line.
```

Both lines assume conventional metal structure and differ only in their coefficients. Use the line drawn from your aircraft's own class. {numref}`tbl-nicolai-trends` lists the lines that matter for a jet trainer.

:::{table} Empty-weight trend lines, $W_e = (\text{constant})\,W_{TO}^{\,x}$, excerpt from Nicolai and Carichner (2010), Table 5.1.
:label: tbl-nicolai-trends

| Aircraft type | Constant | Exponent x |
| --- | ---: | ---: |
| Military jet trainer | 0.747 | 0.993 |
| Fighter, multipurpose | 0.911 | 0.947 |
| Fighter, air-to-air or developmental | 1.2 | 0.947 |
| Fighter, air-to-ground | 0.774 | 0.947 |
| Bomber and transport | 0.911 | 0.947 |
| Light general aviation | 0.911 | 0.947 |

:::

## Empty weight from Raymer's regression

Raymer's Table 6.1 refines the single-variable trend into a regression on five design variables. For jet aircraft, in foot-pound-second units,

```{math}
:label: eq-raymer-jet
\frac{W_e}{W_0} = \left[a + b\,W_0^{\,C_1}\, AR^{\,C_2}\, \left(\frac{T}{W_0}\right)^{C_3} \left(\frac{W_0}{S}\right)^{C_4} M_{max}^{\,C_5}\right] K_{vs}
```

where $M_{max}$ is the maximum Mach number and $K_{vs}$ is the variable-sweep factor, 1.00 for a fixed wing. {numref}`tbl-raymer-jet` gives the coefficients.

:::{table} Coefficients of {eq}`eq-raymer-jet` for jet aircraft, from Raymer (2018), Table 6.1.
:label: tbl-raymer-jet

| Aircraft type | a | b | C1 | C2 | C3 | C4 | C5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Jet trainer | 0 | 4.28 | −0.10 | 0.10 | 0.20 | −0.24 | 0.11 |
| Jet fighter | −0.02 | 2.16 | −0.10 | 0.20 | 0.04 | −0.10 | 0.08 |
| Military cargo/bomber | 0.07 | 1.71 | −0.10 | 0.10 | 0.06 | −0.10 | 0.05 |
| Jet transport | 0.32 | 0.66 | −0.13 | 0.30 | 0.06 | −0.05 | 0.05 |

:::

:::{admonition} Navy Jet Trainer
:class: navy

The Navy trainer sits in the jet-trainer row. The regression needs $W_0$, $AR$, $T/W_0$, $W_0/S$, and $M_{max}$. The empty weight therefore depends on the three sizing variables and on the maximum operating Mach number: Mach 0.78 threshold, Mach 0.90 objective in the RFP. Which of the two goes into $M_{max}$, and what does the choice do to $W_e/W_0$?
:::

## Validate against real aircraft

Nicolai's Table I.5a is a weights summary of thirteen Navy and Air Force fighters. The lecture highlights the Grumman F9F-5 Panther. It was carrier-capable and trainer-sized, and its two-seat Cougar derivative was the Navy's advanced trainer. {numref}`tbl-f9f5` is its column.

:::{table} Grumman F9F-5 column of Nicolai and Carichner (2010), Table I.5a, fighter aircraft weights summary. GW is the flight design gross weight.
:label: tbl-f9f5

| Quantity | F9F-5 |
| --- | ---: |
| Fixed equipment total | 2,140 lb |
| Oil and trapped fuel | 0 lb |
| Maximum fuel capacity | 7,160 lb |
| Payload at maximum fuel | 0 lb |
| Flight design gross weight, GW | 14,900 lb |
| Structure/GW | 0.349 |
| Power plant/GW | 0.193 |
| Fixed equipment/GW | 0.144 |
| Empty weight/GW | 0.686 |
| Wing group/GW | 0.154 |
| Empennage group/GW | 0.027 |
| Fuselage group/GW | 0.119 |
| Engine section/GW | 0.000 |
| Landing gear group/GW | 0.049 |
| Takeoff gross weight | 17,500 lb |
| Empty weight | 10,223 lb |
| Wing group per wing area | 9.2 lb/ft² |
| Empennage group per empennage area | 3.5 lb/ft² |
| Ultimate load factor | 11.3 |
| Wing area | 250 ft² |
| Horizontal tail area | 48 ft² |
| Vertical tail area | 66 ft² |
| Empennage area | 114 ft² |

:::

## How good a trend line is

Apply two of the trend lines in {numref}`tbl-nicolai-trends` to the F9F-5, takeoff gross weight 17,500 lb and actual empty weight 10,223 lb ({numref}`tbl-regression-check`).

:::{table} One aircraft, two trend lines. Worked from Nicolai and Carichner (2010), Tables 5.1 and I.5a.
:label: tbl-regression-check

| Trend line applied | Predicted $W_e$ | Actual $W_e$ | Error |
| --- | ---: | ---: | ---: |
| Military jet trainer, $0.747\,W_{TO}^{\,0.993}$ | 12,208 lb | 10,223 lb | +19% |
| Fighter, multipurpose, $0.911\,W_{TO}^{\,0.947}$ | 9,499 lb | 10,223 lb | −7% |

:::

The class is set by the airframe. The F9F-5 trained naval aviators, but its structure is a carrier fighter's, and the fighter line fits it. A trend line gives the average of its class. One aircraft can sit well off it: the trainer line misses the F9F-5 by 19 percent.

:::{prf:definition} Technology factor
:label: def-technology-factor

A factor applied to a regression result to account for a technology the database never saw, such as a composite structure. Raymer (2018), Table 15.4, and Nicolai and Carichner (2010), Section 20.3.3 and Appendix I.3, discuss it. Take yours from NASA reports, AIAA papers, or Aviation Week, and cite the source.
:::

:::{exercise} The T-45 and the two estimates
:label: ex-t45-empty-weight

Take the T-45 Goshawk from your database of similar aircraft. Apply the jet-trainer trend line of {numref}`tbl-nicolai-trends` and the jet-trainer row of {eq}`eq-raymer-jet` to its takeoff weight, and compare both results with its published empty weight. Which is closer, and by how much?
:::

## Representing the engine

::::{grid} 1 1 2 2

:::{card}
:header: {term}`Fixed engine`
- Select an off-the-shelf engine.
- Thrust (or power) and fuel flow are known.
- Does not change during sizing.
- Adds a constraint, which can make sizing difficult.
:::

:::{card}
:header: {term}`Rubber engine`
- Implies new engine development.
- The engine "stretches" during sizing.
- Sea-level thrust $T_{SL}$ or power $P_{SL}$ changes each iteration.
- Avoids the fixed-engine constraint.
:::

::::

:::{admonition} Navy Jet Trainer
:class: navy

A trainer that replaces an aging jet is the classic fixed-engine case. The RFP gives no engine data. It asks you to identify the engine type, manufacturer, and model, and to document the installed thrust and fuel flow models. Which engine data must be in hand before the loop can run?
:::

## References

- Nicolai, L. M., and Carichner, G. E., *Fundamentals of Aircraft and Airship Design, Volume I: Aircraft Design*, AIAA Education Series, 2010, Chapter 5 and Appendix I.
- Raymer, D. P., *Aircraft Design: A Conceptual Approach*, 6th ed., AIAA Education Series, 2018, Chapter 6.
