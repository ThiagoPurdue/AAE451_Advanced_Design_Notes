---
title: "Propulsion, part 2: Engine models and the engine deck"
short_title: Engine models and the engine deck
---

This is the second part of Lecture 8, *Propulsion Selection and Integration*. It turns the published values of [](engine-selection.md) into thrust and fuel flow over the envelope: the thrust lapse, TSFC against altitude and Mach number, a published engine deck, and installed performance. It then sizes the thrust, scales an engine, and shows how a report documents the engine trade. The figures are redrawn after the figures on the slides and reduced to the point each slide makes.

:::{note} What to take from this lecture
- Thrust and TSFC change with altitude, Mach number, and throttle setting. A single value per segment does not describe them.
- Lapse and TSFC relations stand in for an engine until one is chosen. A published {term}`engine deck` replaces them.
- Every thrust and fuel-flow value in the sizing code is installed and has a cited source.
:::

## Thrust lapse of a turbofan

The {term}`thrust lapse` relations use the total temperature and total pressure of the free stream, as ratios to the sea-level standard values:

:::{math}
:label: eq-theta-delta
\theta_0 = \frac{T}{T_{std}}\left(1+\frac{\gamma-1}{2}M^{2}\right), \qquad \delta_0 = \frac{p}{p_{std}}\left(1+\frac{\gamma-1}{2}M^{2}\right)^{\frac{\gamma}{\gamma-1}}
:::

$T$ and $p$ are the ambient temperature and pressure. $T_{std}$ and $p_{std}$ are their sea-level standard values. $F$ is the thrust, and $F_{SL}$ is its sea-level static value.

:::{prf:definition} Throttle ratio
:label: def-throttle-ratio

The {term}`throttle ratio`, $TR$, is the value of $\theta_0$ at which the turbine entry temperature reaches its limit. The engine maker sets $TR$.
:::

For a low-bypass turbofan at military thrust, without afterburner:

:::{math}
:label: eq-lapse-low
\frac{F}{F_{SL}} = \delta_0\left[1 - 3.8\,\frac{\theta_0 - TR}{\theta_0}\right]
:::

For a high-bypass turbofan below Mach 0.9:

:::{math}
:label: eq-lapse-high
\frac{F}{F_{SL}} = \delta_0\left[1 - 0.49\sqrt{M} - \frac{3\,(\theta_0 - TR)}{1.5 + M}\right]
:::

In both relations, drop the term in $\theta_0 - TR$ when $\theta_0 \le TR$. The relations are from Mattingly et al. (2002), as printed in Gudmundsson (2022), Eqs. 14-77 to 14-80. Mattingly et al. give the military thrust of the low-bypass engine as 0.6 times this lapse, on the sea-level static thrust with afterburner. Equation {eq}`eq-lapse-low` is that relation divided by 0.6. Its $F_{SL}$ is the military sea-level static thrust.

:::{figure} figures/turbofan-lapse.svg
:label: fig-turbofan-lapse
:alt: Two plots of thrust over sea-level static thrust against Mach number from 0 to 0.9, at sea level, 15,000, 25,000, and 35,000 feet. Left, the low-bypass turbofan at military thrust: at sea level the ratio rises from 1.00 to 1.27 at Mach 0.6 and falls to 1.18 at Mach 0.9. At altitude it rises with Mach number, from 0.56 to 0.95 at 15,000 feet, 0.37 to 0.63 at 25,000 feet, and 0.24 to 0.40 at 35,000 feet. Right, the high-bypass turbofan: at sea level the ratio falls from 1.00 to 0.78 by Mach 0.3 and reaches 0.71 at Mach 0.9. At altitude it dips slightly and then recovers: it stays between 0.44 and 0.56 at 15,000 feet, 0.29 and 0.37 at 25,000 feet, and 0.18 and 0.24 at 35,000 feet.
:width: 100%

The thrust lapse of the two turbofan classes, with $TR$ = 1.07 in the standard atmosphere. Computed from {eq}`eq-lapse-low` and {eq}`eq-lapse-high`. Gudmundsson (2022), Figures 14-16 and 14-17, use $TR$ = 1.072.
:::

- Ram pressure sustains the low-bypass thrust as Mach number rises. The thrust of the high-bypass engine falls from Mach 0.
- The break in the sea-level curves marks $\theta_0 = TR$.
- The low-bypass relation was fitted to afterburning mixed-flow engines. Check it against published data for your engine.

:::{admonition} Navy Jet Trainer
:class: navy

The specific excess power uses the thrust at 15,000 ft, and the maximum operating speed uses the thrust at 25,000 ft. How much of the sea-level static thrust does your engine keep there?
:::

## TSFC with altitude and Mach number

:::{table} Installed TSFC, in 1/h, with $\theta = T/T_{std}$ at ambient conditions. The jet-engine relations of Mattingly et al. (2002), as printed in Gudmundsson (2022), Eqs. 14-61 to 14-65.
:label: tbl-tsfc-relations

| Engine | TSFC (1/h) |
| --- | --- |
| Turbojet, military thrust | $(1.1 + 0.30\,M)\sqrt{\theta}$ |
| Turbojet, afterburner | $(1.5 + 0.23\,M)\sqrt{\theta}$ |
| Low-bypass turbofan, military thrust | $(0.9 + 0.30\,M)\sqrt{\theta}$ |
| Low-bypass turbofan, afterburner | $(1.6 + 0.27\,M)\sqrt{\theta}$ |
| High-bypass turbofan, $M < 0.9$ | $(0.45 + 0.54\,M)\sqrt{\theta}$ |

:::

- Use these relations until an engine is chosen.
- TSFC rises with Mach number. It falls with altitude up to the tropopause.
- The high-bypass relation gives values too high for modern engines. Typical values are 0.68 1/h or lower.
- Replace the relations with published values or an {term}`engine deck` once an engine is chosen.

:::{admonition} Navy Jet Trainer
:class: navy

The RFP asks for documented data sources. What is the source of the TSFC in each segment of your missions?
:::

## A published engine deck: the FJ44-3E

:::{figure} figures/fj44-deck.svg
:label: fig-fj44-deck
:alt: Two plots for the FJ44-3E. Left, installed net thrust against Mach number at the highest tabulated throttle setting, one line per altitude. At sea level the thrust falls from 2,254 pounds at rest to 1,581 pounds at Mach 0.35. At 10,000 feet it falls from 2,023 to 1,549 pounds at Mach 0.4. At 20,000 feet it is 1,376 to 1,224 pounds between Mach 0.2 and 0.5. At 30,000 feet it is about 920 pounds and at 40,000 feet about 600 pounds, nearly constant between Mach 0.3 and 0.6. Right, TSFC against installed net thrust at 20,000 feet and Mach 0.4: 0.67 per hour at 1,255 and 969 pounds, 0.73 at 607 pounds, 0.96 at 312 pounds, 1.24 at 170 pounds, and 1.91 at 80 pounds.
:width: 100%

The FJ44-3E installed in a pod: thrust at the highest tabulated throttle setting, and TSFC at part throttle. Values from Nicolai and Carichner (2010), Table J.2b.
:::

- The values are installed: {term}`pressure recovery` 0.995, nozzle coefficient 0.997, nozzle discharge coefficient 0.99.
- The engine drives a 20 hp load. The bleed is 12.5 lb/min up to 20,000 ft and 1 lb/min above.
- For another FJ44 variant, scale the thrust and the TSFC by the ratio of the sea-level static values.
- TSFC is flat near full throttle and rises steeply at low throttle settings. A single value underestimates the fuel of the descent and the loiter.

:::{admonition} Navy Jet Trainer
:class: navy

Up to 50,000 ft the deck stops at Mach 0.6. The RFP asks for Mach 0.78 (T) and Mach 0.90 (O). Which model do you use beyond the published data, and what is its source?
:::

## Installed fuel-flow charts

:::{figure} figures/tfe731-fuel-flow.svg
:label: fig-tfe731
:alt: Fuel flow against installed net thrust at sea level, one line for each Mach number from 0 to 0.7. The lines for Mach 0 to 0.4 start near idle, about 240 pounds per hour. The lines for Mach 0.5 to 0.7 start at 600 to 800 pounds per hour. Every line rises almost straight to a dashed line marked maximum continuous. At rest the line ends at 2,980 pounds of thrust and 1,550 pounds per hour. At Mach 0.7 it ends at 1,870 pounds and 1,760 pounds per hour. At a given thrust, a higher Mach number needs more fuel. A second dashed line, marked best cruise, crosses the lines between 1,250 and 1,400 pounds per hour.
:width: 75%

Installed fuel flow of the TFE731-1069 at sea level, one line per Mach number. Values read from Nicolai and Carichner (2010), Figure J.5a.
:::

:::{table} TFE731 variants at sea-level static conditions, uninstalled. Nicolai and Carichner (2010), Table J.5b.
:label: tbl-tfe731

| Variant | Thrust (lb) | TSFC (1/h) | Weight (lb) |
| --- | ---: | ---: | ---: |
| TFE731-1069 | 3,410 | 0.48 | 783 |
| TFE731-3 | 3,700 | 0.511 | 853 |
| TFE731-5 | 4,304 | 0.484 | 852 |
| TFE731-60 | 4,999 | 0.409 | 988 |

:::

- A deck in this form has one chart per altitude and one line per Mach number, from idle to maximum continuous thrust.
- Read the fuel flow at the thrust that the drag polar requires.
- For another variant, scale the thrust and the TSFC by the ratio of the sea-level static values.

## Installed performance

:::{prf:definition} Installed thrust
:label: def-installed-thrust

The {term}`installed thrust` is the thrust of the engine in the aircraft, after the inlet and nozzle losses, the power extraction, and the bleed.
:::

Installation losses of a jet:

- Pressure loss in the inlet.
- Ingestion of the boundary layer.
- Loss in the nozzle.

Power extraction:

- Generators for the avionics, the lights, the environmental control, and the de-icing.
- Hydraulic pumps.
- Bleed air for the cabin pressure, the anti-ice system, and the on-board oxygen generation system (OBOGS).

:::{admonition} Navy Jet Trainer
:class: navy

The RFP asks for the installed thrust and fuel flow. Which systems of your aircraft draw shaft power or bleed air? If you choose OBOGS, does it draw bleed air or electric power?
:::

## Thrust sizing

The takeoff thrust-to-weight ratio, $(T/W)_{TO}$, is set by cruise, maneuver, acceleration, takeoff, or maximum speed. The value chosen is a compromise over the whole mission.

:::{table} Takeoff thrust-to-weight ratio by dominant requirement, uninstalled. The values are trends, not targets. Nicolai and Carichner (2010), Table 18.1.
:label: tbl-thrust-to-weight

| Dominant requirement | $(T/W)_{TO}$ |
| --- | ---: |
| Long range | 0.20 to 0.35 |
| Short and intermediate range | 0.30 to 0.45 |
| STOL and utility transport | 0.40 to 0.60 |
| Fighter, close air support | 0.40 to 0.60 |
| Fighter, strike interdiction | 0.45 to 0.70 |
| Fighter, interceptor | 0.55 to 0.80 |
| Fighter, air-to-air | 0.80 to 1.30 |

:::

The maximum sustained load factor (Nicolai and Carichner 2010, Eq. 18.5):

:::{math}
:label: eq-sustained-load-factor
n_{MS} = \frac{q}{\sqrt{W/S}}\sqrt{\frac{1}{K}\left[\frac{T}{W}\,\frac{1}{q} - \frac{C_{D_0}}{W/S}\right]}
:::

- In {eq}`eq-sustained-load-factor`, $T/W$ and $W/S$ are the values at the flight condition, not at takeoff.
- A high $T/W$ raises $n_{MS}$. It also adds engine weight and moves the cruise away from the minimum TSFC.
- The takeoff distance depends on $T/W$, $W/S$, and the high-lift system together.

:::{admonition} Navy Jet Trainer
:class: navy

Sustained +4.0 g (T) and +6.0 g (O) at 15,000 ft, at MTOW less 50% fuel. What thrust does {eq}`eq-sustained-load-factor` give at your {term}`wing loading`, and how does it compare with the thrust for Mach 0.90?
:::

## Rubber-engine scaling

A {term}`rubber engine` is scaled from a reference engine. The scale factor is the ratio of the sea-level static airflows. At constant exit velocity it equals the ratio of the thrusts, $SF = \dot{m}/\dot{m}_{ref} = T/T_{ref}$ (Nicolai and Carichner 2010, Eqs. 18.1 to 18.4):

:::{math}
:label: eq-rubber-engine
W_{eng} = SF^{\,n}\,W_{ref}, \qquad d = SF^{1/2}\,d_{ref}, \qquad \ell = SF^{\,n-1/2}\,\ell_{ref}
:::

The exponent $n$ is 0.8 to 1.3, and usually about 1.0. To size for cruise, match the cruise drag with the thrust at the throttle setting of minimum TSFC. Check the start and the end of the cruise.

:::{table} A scaled TF39 for a four-engine transport at Mach 0.8, in a cruise climb from 31,000 ft to 41,000 ft. The weight uses the scale factor before rounding, 0.7745. Nicolai and Carichner (2010), Example 18.1.
:label: tbl-tf39

| Quantity | Value |
| --- | ---: |
| Drag per engine at the start of cruise | 7,327 lb |
| TF39 at 100% normal rated thrust, 31,000 ft | 9,460 lb |
| Scale factor | 0.775 |
| Weight, 0.775 × 7,026 lb | 5,442 lb |
| Diameter, $\sqrt{0.775}$ × 100 in | 88 in |
| Length, $\sqrt{0.775}$ × 271 in, with $n$ = 1 | 238.6 in |
| End of cruise, thrust required | 4,892 lb |
| End of cruise, thrust available | 4,960 lb |

:::

:::{iframe} ../quickcheck/rubber-engine.html
:label: qc-rubber-engine
:width: 100%

Quick check: a scaled engine from {eq}`eq-rubber-engine`. Shuffle gives new values; the solution shows the steps.
:::

:::{admonition} Navy Jet Trainer
:class: navy

A scaled engine is stated with its reference engine and its scale factor. Which published engine would be your reference?
:::

## An engine trade in a report

Team Draco's interceptor proposal won the AIAA 2024-25 undergraduate competition. It documents its engine trade in four steps.

:::{table} The engine trade of Team Draco (2025), and what each step asks of the Navy Jet Trainer.
:label: tbl-engine-trade

| What the report documents | Navy Jet Trainer |
| --- | --- |
| 1. The drivers: cost, thrust, and fuel. A unit cost limit of 25 million dollars ruled out a twin-engine aircraft | Your drivers; one engine or two |
| 2. Data for each candidate: sea-level static thrust, TSFC, airflow, bypass ratio, overall pressure ratio, weight, and size. A cycle model is checked against them | Textbook data and the maker's data |
| 3. Two candidates at the constraining segment, a 4 h loiter. Their bypass ratios are 0.36 and 0.68, and the fuel flow of the second is 15% lower | Your constraining segment |
| 4. Engine cost against thrust: the aircraft costs 24.7 or 25.1 million dollars, against the limit of 25 million | Cost in 2030 dollars |

:::

:::{figure} figures/engine-trade.svg
:label: fig-engine-trade
:alt: TSFC against thrust for two engines at 35,000 feet and Mach 0.8. Both curves fall steeply from 2.0 per hour at low thrust to a flat minimum and rise slightly toward maximum thrust. The F110-GE-132 lies below the F100-PW-229 everywhere: its minimum is about 0.80 near 3,500 pounds, against about 0.89 near 4,200 pounds. A shaded band between 1,960 and 2,860 pounds marks the loiter thrust range, to the left of both minima.
:width: 80%

Two candidate engines at 35,000 ft and Mach 0.8, with the loiter thrust range shaded. Values read from Team Draco (2025), Figure 28.
:::

The loiter range lies to the left of the TSFC minimum of both engines. Either engine is oversized for this segment. Another requirement sized the thrust.

## Mission points on the engine deck

:::{figure} figures/deck-mission-points.svg
:label: fig-deck-mission-points
:alt: TSFC against thrust for one engine at Mach 0.8, one curve for each altitude: 10,000, 20,000, 35,000, and 50,000 feet. Each curve falls steeply from low thrust to a minimum at two thirds or more of its maximum thrust. The curves move to lower thrust as altitude rises: the minimum is near 12,000 pounds at 10,000 feet and near 2,000 pounds at 50,000 feet. Two open circles on the 35,000 foot curve mark the start and the end of the loiter, at 2,860 pounds and 0.94 per hour and at 1,960 pounds and 1.08 per hour, both to the left of the minimum.
:width: 85%

The F100-PW-229 without afterburner at Mach 0.8, with the loiter points on the 35,000 ft curve. Values read from Team Draco (2025), Figure 31, which shows seven altitudes.
:::

The report places each mission segment on the deck in four steps (Team Draco 2025, Section VII.C and Table 11):

1. Compute the thrust required in each segment from the drag polar.
2. Build the installed deck. The report applies the installation losses of Nicolai and Carichner (2010), Chapter 16, about 4% of the thrust. It adds 2% bleed for the environmental control and the avionics cooling, and 50 kW of power extraction.
3. Plot each segment on the TSFC curve for its Mach number and altitude. Read the TSFC and the fuel flow there.
4. Show the margin to maximum thrust. The report shows it for the dash and combat segments.

:::{admonition} Navy Jet Trainer
:class: navy

Plot the cruise, the maneuvers at Mach 0.60 and 10,000 ft, the FCLP, and the reserve on your deck. In which of them is the engine farthest from its minimum TSFC?
:::

:::{seealso}
Continue with [](engine-integration.md): the inlet, the diffuser, the nozzle, and the design sequence. The references for the three parts are at the end of that page.
:::
