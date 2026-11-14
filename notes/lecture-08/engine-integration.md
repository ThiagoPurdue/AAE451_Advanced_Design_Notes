---
title: "Propulsion, part 3: Inlet, nozzle, and the design sequence"
short_title: Inlet, nozzle, and the design sequence
---

This is the third part of Lecture 8, *Propulsion Selection and Integration*. It installs the engine of [](engine-selection.md) and [](engine-models.md) in the aircraft: the capture area of the inlet, the diffuser, and the nozzle. It closes with the design sequence and the work for the week. The figures are redrawn after the figures on the slides and reduced to the point each slide makes.

:::{note} What to take from this lecture
- The inlet is sized by the airflow the engine demands at a stated design point, and checked at takeoff.
- The duct length follows from the diffuser angle. It adds fuselage length and moves the CG.
- {term}`Pressure recovery` and the nozzle coefficient turn an uninstalled engine deck into an installed one. An installed deck already includes them. Each loss is counted once.
:::

## Jet inlet: the capture area

:::{prf:definition} Demand capture area
:label: def-capture-area

The {term}`capture area` the engine demands, $A_{\infty E}$, is the free-stream cross-section of the streamtube that the engine and the secondary systems take in. Nicolai and Carichner (2010) call the opening of the inlet at the lip, $A_c$, the cowl capture area. These notes call it the lip area.
:::

With the engine airflow $\dot{m}_E$ and the secondary airflow $\dot{m}_S$ in lbm/s, the density in slug/ft³, and the speed in ft/s, the capture area is (Nicolai and Carichner 2010, Eq. 15.2)

:::{math}
:label: eq-capture-area
A_{\infty E} = \frac{\dot{m}_E + \dot{m}_S}{32.17\,\rho_\infty V_\infty}
:::

:::{figure} figures/inlet-streamtube.svg
:label: fig-inlet-streamtube
:alt: Two sketches of an inlet in section with the air flowing in from the left. At rest, the streamlines converge on the inlet from a region much wider than the lip, and some curve around the lip from outside. At cruise, the streamlines are nearly parallel and the streamtube that enters the inlet is narrower far upstream than the lip, and widens as it reaches it. The cross-section of that streamtube far upstream is marked as the demand capture area, and the opening between the lips as the lip area.
:width: 65%

The captured streamtube at rest and at cruise. Schematic, after Gudmundsson (2022), Figure 7-38.
:::

The inlet is sized in five steps:

1. Take $\dot{m}_E$ at the design point from the engine data. Without data, hold the corrected airflow $\dot{m}\sqrt{\theta_0}/\delta_0$ at its sea-level static value: $\dot{m}_E = \dot{m}_{SLS}\,\delta_0/\sqrt{\theta_0}$, with $\theta_0$ and $\delta_0$ from [part 2](engine-models.md).
2. Add the secondary airflow as a fraction of the engine airflow, from {numref}`tbl-secondary-air`.
3. State the design point. Nicolai and Carichner (2010), Section 15.7, size the inlet at the cruise altitude and Mach number, or at the maximum speed. Gudmundsson (2022), Section 7.3.5, sizes it at static takeoff thrust. With a cruise design point, the lip area is about the area of the cruise streamtube.
4. Check takeoff. The streamtube is then wider than the lip. Round the lips, and add auxiliary doors if the lip area is small.
5. Keep the compressor face at Mach 0.4 to 0.5. Record $A_{\infty E}$, the lip area, and the design point in {term}`ASORT`.

:::{table} Secondary airflow as a fraction of the engine airflow. Selected rows of Nicolai and Carichner (2010), Table 15.1; see also Section 15.7.
:label: tbl-secondary-air

| Use | $\dot{m}_S/\dot{m}_E$ |
| --- | ---: |
| Environmental control | 0.02 to 0.05 |
| Nacelle cooling | 0 to 0.04 |
| Oil cooling | 0 to 0.01 |
| Hydraulics cooling | 0 to 0.01 |

:::

The secondary air costs drag (Gudmundsson 2022, Eqs. 7-19 and 16-147):

- A heat exchanger that rejects the heat $Q$ needs the airflow $\dot{m} = Q/(c_p\,\Delta T)$. Here $c_p$ is the specific heat of air at constant pressure and $\Delta T$ the temperature rise of the air. $\Delta T$ is smallest on the hot day.
- The cooling drag is $D = \dot{m}\,(V_\infty - V_e)$, with $V_e$ the exit speed of the cooling air. Near zero speed there is no ram pressure, and a fan or a blower moves the air.
- The drag enters the polar of [Lecture 7](../lecture-07/parasite-drag.md) as $\Delta C_{D_0}$. The exchanger, the pump, and the fluid enter the empty weight.

:::{admonition} Navy Jet Trainer
:class: navy

Which condition is your inlet design point, and why? Check the capture area at Mach 0.90 and 25,000 ft, and at takeoff at 5,000 ft density altitude.
:::

## Inlet design in a report

:::{table} The inlet design of the Team Draco (2025) Mach 2 interceptor, and the matching item for the Navy Jet Trainer.
:label: tbl-inlet-report

| What the report documents | Navy Jet Trainer |
| --- | --- |
| 1. The airflow at a stated design point, Mach 1.8, gives $A_{\infty E}$ | {eq}`eq-capture-area` at your design point; check takeoff |
| 2. The inlet type: an external-compression spike | Your inlet type (Nicolai and Carichner 2010, Figure 15.12) |
| 3. Pressure recovery against Mach number with the mission points, entered in the engine deck | The same, subsonic; compare with MIL-E-5008B |
| 4. An S-duct, and the height of the diverter (Nicolai and Carichner 2010, Chapter 16) | Only for a buried or side inlet |
| 5. The inlet area against an aircraft with the same engine | An aircraft that uses your engine or its reference engine |
| 6. Auxiliary doors and the starter | Doors if the inlet is sized at cruise |
| 7. Dimensioned drawings of the duct and the inlet | Required |

:::

:::{prf:definition} Pressure recovery
:label: def-pressure-recovery

The {term}`pressure recovery` of an inlet is the total pressure at the compressor face divided by the total pressure of the free stream.
:::

:::{figure} figures/inlet-recovery.svg
:label: fig-inlet-recovery
:alt: Pressure recovery from shocks against flight Mach number from 0 to 2. Two curves, for a single normal shock and for the MIL-E-5008B specification, equal 1 up to Mach 1. They cross near Mach 1.23, and above it the normal shock falls faster, to 0.93 at Mach 1.5 and 0.72 at Mach 2. The specification falls to 0.97 at Mach 1.5 and 0.925 at Mach 2.
:width: 80%

The pressure recovery after shock losses: one normal shock, and the MIL-E-5008B specification. Computed from the normal-shock relation and from the specification as given in Mattingly et al. (2002).
:::

Below Mach 1 a pitot inlet has no shock loss. The lip and the duct set its recovery. Check a published recovery curve against {numref}`fig-inlet-recovery` before you use it. Figure 36 of the report shows 0.90 for one shock at Mach 1.0, where the relation gives 1 ({numref}`fig-draco-recovery`).

:::{figure} figures/draco-recovery.svg
:label: fig-draco-recovery
:alt: Inlet pressure recovery against Mach number from 0 to 2.3, as a winning report plots it. The MIL-E-5008B curve is 1 up to Mach 1 and falls to 0.925 at Mach 2. The two-shock external spike the report chose rises from 0.97 at rest to about 0.997 near Mach 0.8, then falls with the specification to 0.925 at Mach 2; eight open circles on it mark the mission points between Mach 0.52 and 2.0. The report's one-shock curve falls from 1 at rest to 0.90 at Mach 1.0, where a normal shock loses nothing.
:width: 80%

Inlet pressure recovery of a winning report: the chosen spike with its mission points, the specification, and the report's one-shock curve. Values read from Team Draco (2025), Figure 36.
:::

The report also cites MIL-HDBK-516C, Section 5.2.3, for inlet compatibility. That section covers the aeroelastic design of control surfaces.

:::{admonition} Navy Jet Trainer
:class: navy

MIL-HDBK-516C covers inlet compatibility in Section 7.2.5.3. What recovery do you enter in your deck, and what is its source?
:::

## Diffuser: duct length and recovery

:::{figure} figures/diffuser.svg
:label: fig-diffuser
:alt: Left, an inlet duct in section. It widens from the throat diameter at the lip to the compressor-face diameter over a length L, and the walls, extended forward, meet at the included angle theta. Right, the included angle against diffuser length over throat diameter, with two falling curves: no separation below the lower, transitory separation between them, full separation above the upper. The lower curve falls from 40 degrees at a ratio of 0.4 to 19 degrees at 2 and 10.5 degrees at 6. The upper lies about 3 degrees higher. A line at 10 degrees stays below both over the whole range.
:width: 100%

Diffuser geometry, and the included angle at which the flow separates. The geometry is schematic; the limits are read from Gudmundsson (2022), Figures 7-39 and 7-40.
:::

Take the compressor-face diameter $D_f$ from the engine data and the throat diameter $D_t$ from the capture area. Size the length $L$ for an included angle $\theta \le 10°$ (Nicolai and Carichner 2010, Section 15.7). Here $\theta$ is an angle, not the temperature ratio of [part 2](engine-models.md):

:::{math}
:label: eq-diffuser-length
L \ge \frac{D_f - D_t}{2\tan\,(\theta/2)}
:::

Add 1 to 3 throat radii of straight duct ahead of the compressor (Nicolai and Carichner 2010, Section 15.7). A side or buried inlet has an S-duct, and its offset adds length and loss. An inlet on the side of the fuselage needs a boundary-layer diverter (Nicolai and Carichner 2010, Chapter 16).

A recovery below the value the engine maker assumed costs thrust: the loss in percent is about $C_{ram}$ times the loss in recovery in percent, with $C_{ram}$ about 1.35 below Mach 1 (Raymer 2018, Chapter 13). The FJ44-3E deck of [part 2](engine-models.md) is already installed, with a recovery of 0.995 for a podded engine; do not apply it again. State the value you use.

:::{admonition} Navy Jet Trainer
:class: navy

The length from the inlet to the engine adds fuselage length and moves the CG. How does it change between a buried and a podded engine?
:::

## Nozzle: what to check

The net thrust of a single stream (Gudmundsson 2022, Section 14.2) is

:::{math}
:label: eq-net-thrust
T = \dot{m}\,(V_e - V_\infty) + (p_e - p_\infty)\,A_e
:::

Here $p_e$ and $A_e$ are the pressure and the area at the nozzle exit. For a turbofan, sum the core and bypass streams.

:::{prf:definition} Nozzle pressure ratio
:label: def-npr

The {term}`nozzle pressure ratio` is the total pressure at the nozzle exit divided by the ambient pressure, $\mathrm{NPR} = p_{t,e}/p_\infty$.
:::

A convergent nozzle chokes at

:::{math}
:label: eq-choked-nozzle
\mathrm{NPR} \ge \left(\frac{\gamma+1}{2}\right)^{\frac{\gamma}{\gamma-1}} = 1.893 \quad (\gamma = 1.4)
:::

The limit is about 1.85 for the hot core flow (Mattingly et al. 2002). Below it, $p_e = p_\infty$. Above it, the exit Mach number is 1.

Check four things:

1. A subsonic aircraft without afterburner uses a fixed convergent nozzle (Nicolai and Carichner 2010, Figure 15.12). Take the exit area from the engine data.
2. Read the NPR at the maximum Mach number from the deck. The pressure term of {eq}`eq-net-thrust` is already in the deck thrust. Do not add it again.
3. The nozzle coefficient multiplies the gross thrust, not the net thrust. The FJ44-3E deck already includes 0.997 for a podded engine. State the value you use, and apply it only to an uninstalled deck.
4. Boattail drag belongs to the drag build-up of [Lecture 7](../lecture-07/parasite-drag.md), not to the deck. Count it once.

:::{admonition} Navy Jet Trainer
:class: navy

Show the nozzle and the afterbody on the layout. Is the thrust counted once, in the deck, and the boattail drag once, in the build-up?
:::

## Design sequence

:::{table} The propulsion design sequence and where each output goes. After Sadraey (2013).
:label: tbl-design-sequence

| Step | Output | Where |
| --- | --- | --- |
| 1. Propulsion requirements from the RFP and the constraint diagram | Thrust at each condition; {term}`ratings <rating>`; day and altitude | A05 Deliverable 1; ASORT |
| 2. Engine class, on the operational map | The class, with the candidates it admits | A05 Deliverable 1 |
| 3. Number of engines | The number, with its criteria | A05 Deliverable 2 |
| 4. Locations | Layout sketch; the engine-out case of a twin | A05 Deliverable 4; layout |
| 5. A {term}`fixed engine`, or a scaled one | Engine, scale factor, weight, size, cost basis | A05 Deliverable 2 |
| 6. Inlet | $A_{\infty E}$ and the duct | A05 Deliverable 4; layout |
| 7. Installation: mounts, cowl, cooling, fuel system, fire protection | Volumes and weights | Layout; weights |
| 8. Check with installed values; return to the step that fails | The installed deck against every requirement | A05 Deliverables 3 and 5 |

:::

:::{admonition} Navy Jet Trainer
:class: navy

The RFP requires an identified engine: type, manufacturer, and model. Is yours a fixed engine or a scaled one?
:::

## This week

1. Place your requirements on the operational map of [part 1](engine-selection.md). List at least two candidate classes.
2. Collect published data for three or more candidate engines, from Nicolai and Carichner (2010), Appendix J, and the maker's data. Cite each number.
3. Build the installed deck over the RFP envelope: thrust and TSFC.
4. Code the lapse and TSFC relations of [part 2](engine-models.md). Check them against a published curve.
5. Compute the installed thrust at Mach 0.78 and Mach 0.90 at 25,000 ft, and at 15,000 ft, at the rating you assume for each condition.

:::{tip}
[](../assignments/a05.md) asks for the propulsion requirements and the engine class, the candidates and the selection, the installed engine deck, and the inlet. The constraint analysis that follows uses this deck.
:::

:::{important} Summary
- The speed, altitude, and field requirements narrow the engine class. The number and location of the engines follow from the requirements and the failure cases.
- Sizing needs installed thrust and fuel flow against altitude, Mach number, and throttle setting, with a cited source.
- The inlet, the duct, and the nozzle set the installation losses. Each loss is counted once.
:::

:::{exercise} For discussion
:label: ex-propulsion

Up to 50,000 ft the FJ44-3E deck stops at Mach 0.6, and the low-bypass lapse relation was fitted to afterburning engines. Take your candidate engine at Mach 0.90 and 25,000 ft. Which published point is closest to that condition, how do you extend the model from it, and what margin do you carry on the thrust?
:::

:::{seealso} Reading
Gudmundsson (2022), Chapters 7 and 14, and Nicolai and Carichner (2010), Chapters 15 and 18 and Appendix J. [Lecture 9](../lecture-09/constraint-method.md) covers the constraint analysis: the master equation, the trainer boundaries, and the design point.
:::

## References

- Gudmundsson, S., *General Aviation Aircraft Design: Applied Methods and Procedures*, 2nd ed., Butterworth-Heinemann, 2022. Chapters 7, 14, 15, and 16.
- Mattingly, J. D., Heiser, W. H., and Pratt, D. T., *Aircraft Engine Design*, 2nd ed., AIAA Education Series, 2002.
- Nicolai, L. M., and Carichner, G. E., *Fundamentals of Aircraft and Airship Design, Volume 1: Aircraft Design*, AIAA Education Series, 2010. Chapters 15, 16, and 18, and Appendix J.
- Raymer, D. P., *Aircraft Design: A Conceptual Approach*, 6th ed., AIAA, 2018. Chapters 3 and 13.
- Sadraey, M. H., *Aircraft Design: A Systems Engineering Approach*, Wiley, 2013.
- Team Draco, "Homelander: Homeland Defense Interceptor Design Proposal," University of Illinois Urbana-Champaign, AIAA 2024-25 Undergraduate Aircraft Design Competition, first place, 2025.
- MIL-HDBK-516C, *Airworthiness Certification Criteria*, U.S. Department of Defense, 2014.
- AIAA 2026-27 Undergraduate Team Aircraft Design Competition RFP, *Design of a Navy Jet Training Aircraft*; see [](../navy-rfp/navy-rfp.md).
