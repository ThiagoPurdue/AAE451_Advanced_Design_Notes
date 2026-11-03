---
title: The aircraft design process
short_title: Design process
---

This is the first part of Lecture 1, *Introduction to Aircraft Design*. It covers the phases of an aircraft program, the work done in conceptual design, the market and business case, the feasibility study and the systems view of an aircraft. The second part, [](needs-and-conops.md), covers needs and operations. The third part, [](requirements.md), covers requirements.

## Phases of an aircraft program

An aircraft program runs through six phases, from the first feasibility study to the retirement of the fleet ({numref}`fig-design-phases`).

```{figure} figures/design-phases.svg
:label: fig-design-phases
:alt: Six chevrons in a row. Phase 0, feasibility study, in gray. Phases 1 to 5 in blue: conceptual design, preliminary design, detailed design, entry into service and production, operating and phase out.
:width: 100%

Phases of an aircraft program. Redrawn after Venson, as credited on the lecture slide.
```

Phase 0, the feasibility study, asks whether the program should start at all. Phases 1 to 3 are design. Phase 4 is certification, entry into service and production. Phase 5 is operation of the fleet and its retirement.

:::{important} Where this course sits
This course is Phase 1, {term}`conceptual design`, carried to a Preliminary Design Review ({term}`PDR`) at the end of the semester.
:::

## What happens in conceptual design

{numref}`fig-design-process-flow` shows the conceptual design process as Nicolai and Carichner describe it. The process starts with the customer and the mission requirements. It ends with a point design that is ready for preliminary design.

```{figure} figures/design-process-flow.svg
:label: fig-design-process-flow
:alt: Flow chart of the conceptual design process. The customer sets the mission requirements, which lead to the concept of operations. Requirements are evaluated and negotiated with the customer before a GO decision. The concept of operations, the selection criteria, the system approach (tactics, support aircraft, ECM, subsystems), the technology (materials, stealth, propulsion) and the measures of merit (life cycle cost, takeoff weight, targets killed per life cycle cost) feed the design guidelines (radius, payload, altitude, signature). The guidelines lead to configuration sketches and a stack of concepts, then to initial sizing and selection of a configuration. Functional inputs (aero, propulsion, weights, materials and structure, signature) feed design trades on wing loading, thrust-to-weight ratio, aspect ratio and sweep, plotted against the measures of merit, which lead to the preferred configuration and the baseline design. The baseline goes through mission trades (radius, payload, speed, box size, hover time) and technology trades (TSFC, engine thrust-to-weight ratio, empty weight, drag coefficient, lift-to-drag ratio, maximum lift coefficient), each plotted as the change in a measure of merit for changes of minus 10 to plus 10 percent. A risk assessment feeds the question Happy? If no, the design is iterated from point A, which re-enters at the design trades. If yes, the trade results are shared with the customer. If the requirements change, the process goes back to GO. If not, the point design (outer mold line, general arrangement, performance, subsystems, risk analysis, requirements analysis, systems engineering results, management plan, reliability, maintainability and supportability, life cycle cost analysis, system specifications, test planning, technology readiness level 3 to 4) goes on to preliminary design.
:width: 100%

The conceptual design process. Redrawn after Nicolai and Carichner (2010), as shown on the lecture slide. Point A is where a design iteration re-enters the process. MoM is a measure of merit.
```

:::{prf:definition} Measure of merit
:label: def-measure-of-merit

A {term}`measure of merit` is a quantity used to rank concepts, such as life cycle cost or takeoff weight. Trade studies report the change in a measure of merit. The chart abbreviates it MoM.
:::

Read the chart in four steps:

1. **Define the problem.** The customer states the mission. The team writes the concept of operations, evaluates and negotiates the requirements with the customer, and gets a GO decision. The design guidelines and the measures of merit are set here.
2. **Find a baseline.** The team sketches several configurations, sizes each one and selects one. Design trades on wing loading (W/S), thrust-to-weight ratio (T/W), aspect ratio (AR) and sweep refine it into a baseline design.
3. **Trade and decide.** Mission trades change the requirements, such as radius, payload or speed. Technology trades change the assumptions, such as specific fuel consumption, engine thrust-to-weight ratio or empty weight. Each trade is plotted as the change in a measure of merit. If the result is not acceptable, the design is iterated from point A, back through the design trades.
4. **Share and close.** The trade results go back to the customer. If the customer changes a requirement, the process goes back to GO. If not, the point design goes forward.

Requirements are not fixed at the start. A trade study can show that one requirement costs far more than it is worth, and the customer may then change it.

{numref}`tbl-design-phases-detail` shows what is known, what is produced and how mature the technology is at the end of each design phase.

:::{table} What is known and what is produced in each design phase, after Nicolai and Carichner (2010). TRL is the technology readiness level.
:label: tbl-design-phases-detail

| Aspect | Phase 1, conceptual design | Phase 2, preliminary design | Phase 3, detail design |
| --- | --- | --- | --- |
| Known | Basic mission requirements: range, altitude and speed. Basic material properties: strength-to-density ratio σ/ρ, stiffness-to-density ratio E/ρ, cost per pound | Aeroelastic, fatigue and flutter requirements. Overall strength requirements | Local strength requirements. Producibility. Functional requirements |
| Results | Geometry: airfoil type, aspect ratio, thickness ratio t/c, taper ratio λ, sweep Λ. Design objectives: drag level, weight goals, cost goals | Basic internal arrangement. Complete external configuration, with camber and twist distribution and local flow problems solved. Major loads, stresses and deflections | Detail design of mechanisms, joints, fittings and attachments. Design refinements from testing |
| Output | Feasible design | Mature design | Shop designs |
| {term}`TRL` | 2 to 3 | 4 to 5 | 6 to 7 |

:::

The slide illustrates each phase with a sketch. Phase 1 compares two wing planforms. Phase 2 compares two airfoil sections and two incidence angles, 3° and 5°. Phase 3 shows the internal structure of a wing box.

Raymer describes the same three phases by the questions each one answers ({numref}`fig-design-funnel`).

```{figure} figures/design-funnel.svg
:label: fig-design-funnel
:alt: Three stacked boxes, each with a chevron pointing down into the next. A box labeled Requirements points into the first. Conceptual Design: What requirements drive the design? What should it look like? Weight? Cost? What tradeoffs should be considered? What technologies should be used? Do these requirements produce a viable and salable plane? Preliminary Design: Freeze the configuration. Develop lofting (surface definition). Develop test and analytical database. Design major items. Develop actual cost estimate (statistical), you bet your company. Detail Design: Design actual pieces to be built. Design tooling and fabrication process. Test major items, structure, landing gear and so on. Finalize weight and performance estimates, now you learn the real numbers. The last chevron points into a box labeled Fabrication.
:width: 85%

Conceptual, preliminary and detail design. Redrawn after Raymer, as shown on the lecture slide.
```

Raymer adds two remarks. Preliminary design is where the company commits to the program. He calls the commitment made at that stage, based on that cost estimate, "you bet your company". Detail design is where the real numbers are learned. Every number in conceptual design is an estimate. Keep track of what each estimate rests on.

:::{admonition} Navy Jet Trainer
:class: navy

The RFP asks for "a preliminary design". In this course you carry the design through conceptual design to a Preliminary Design Review. Expect your weights and performance to change as the methods improve during the semester. Record the source of every number so you can update it.
:::

## Market analysis and business case

An aircraft program starts with a market.

::::{grid} 1 1 2 2

:::{card}
:header: Market analysis
Understand the demand and the competition.

- **Market segments.** Commercial, military, business and other segments.
- **Competitors.** Their strengths, weaknesses and market share.
- **Demand forecast.** Future trends, growth areas and the age of the fleets in service.
:::

:::{card}
:header: Business case
Justify the program in terms of profit and strategic fit.

- **Cost analysis.** Development, production and operating costs against the expected revenue.
- **Return on investment.** The financial return the program can produce.
- **Risk assessment.** Technical, financial and market risks, and how to reduce them.
:::

::::

:::{seealso}
The lecture recommends the video [Turboprops, regional aviation and other stuff](https://www.youtube.com/watch?v=_33Zqer6Nzc) by Marcelo Alves Araujo.
:::

### Example: narrow-body aircraft

{numref}`fig-narrowbody-production` compares production numbers of narrow-body airliners. Two families dominate. The Airbus A320 family and the Boeing 737 family together account for more aircraft than all the others combined.

```{figure} figures/narrowbody-production.svg
:label: fig-narrowbody-production
:alt: Horizontal bar chart titled Narrow Body Aircraft Production, showing the number of aircraft produced. From the top: McDonnell Douglas MD-80 and MD-90, 1191. COMAC C919, 305. Mitsubishi SpaceJet, 0. Bombardier CSeries, now the Airbus A220, 220. Sukhoi Superjet 100, 200. Embraer E-Jets E2, second generation, 200. Bombardier CRJ family, 1945. Embraer E-Jets, first generation, 1500. Fokker 100, 283. Fokker 70, 47. Boeing 737 family, 10500. Airbus A318, A319, A320 and A321, 16000.
:width: 90%

Narrow-body aircraft production. Redrawn from the lecture slide with its values. They are rounded and are not current production totals.
```

A new aircraft enters a market that already has a leader. The Mitsubishi SpaceJet, formerly the MRJ, is the example at the bottom of the chart.

```{figure} figures/spacejet-ja21mj.jpg
:label: fig-spacejet
:alt: Photograph of a white Mitsubishi MRJ90 with red and black stripes and MRJ on the tail, on its takeoff roll.
:width: 80%

The first MRJ90 flight-test aircraft, JA21MJ, in Japan in 2016. Photo by CHIYODA I, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:JA21MJ_TAKEOFF_ROLL.jpg).
```

:::{warning} The SpaceJet
The SpaceJet flew and went through years of flight testing, yet no aircraft was delivered. Mitsubishi Heavy Industries ended the program in 2023, citing the cost and time still needed for type certification and a weak market. The lecture slide shows one of the flight-test aircraft being cut up. A program can fail on certification, cost and schedule even after the aircraft flies.
:::

## Feasibility study

The feasibility study is Phase 0. It checks four things.

::::{grid} 1 2 2 4

:::{card}
:header: Technical feasibility
Can the design be built with current technology?
:::

:::{card}
:header: Economic viability
Is the program financially sustainable?
:::

:::{card}
:header: Operational feasibility
Can the aircraft be operated within existing infrastructure?
:::

:::{card}
:header: Environmental impact
What are the negative environmental effects, and how can they be reduced?
:::

::::

:::{admonition} Navy Jet Trainer
:class: navy

The customer is the Navy. The business case appears in the RFP's cost section. It asks for development, test and certification cost in 2030 dollars. Production is 10 aircraft at low rate and 500 at full rate. The RFP also asks for the unit flyaway cost, the life cycle cost and the operating cost per flight hour. See [](../navy-rfp/navy-rfp.md).
:::

## The systems engineering approach

An aircraft is a complex product of many subsystems, components and parts. It is also only one system inside a larger air transportation or defense "system of systems" ({numref}`fig-system-levels`).

```{figure} figures/system-levels.svg
:label: fig-system-levels
:alt: Five levels, each decomposing into the next. Level 1, system of systems: the air transportation or defense system, with aircraft, missiles, satellites, ground stations, airports and air traffic management. Level 2, system: the aircraft and related systems such as operators, trainers, manufacturing plants and maintenance shops. Level 3, subsystem: flight control, hydraulic, electric, avionics, powerplant, fuel, air conditioning and structure. Level 4, component: wing, fuselage, tail, landing gear, radar, pumps, nacelles, control surfaces and auxiliary power unit. Level 5, part: fittings, fasteners, blades, screws, nuts, ribs, spars, frames, stiffeners, skin, shafts, pipes and propellers.
:width: 100%

Levels of an aircraft system. Redrawn after Sadraey (2012).
```

Each level is designed against requirements that come from the level above. A requirement on the aircraft, Level 2, comes from the system of systems it serves, Level 1. The aircraft requirement then flows down to the subsystems at Level 3.

:::{exercise} Levels of the trainer
:label: ex-system-levels

What is Level 1 for the trainer, and which other elements sit beside the aircraft in it? Level 3 starts with the list in the RFP's aircraft systems section: propulsion, landing gear, electrical, hydraulics, fuel, pressurization, air conditioning and oxygen, avionics, control system actuators and flight control computers. Which requirements does the trainer inherit from Level 1? Answer that before writing requirements for Level 2.
:::

## References

- Nicolai, L. M., and Carichner, G. E., *Fundamentals of Aircraft and Airship Design, Volume I: Aircraft Design*, AIAA Education Series, 2010.
- Raymer, D. P., *Aircraft Design: A Conceptual Approach*, 6th ed., AIAA Education Series, 2018.
- Sadraey, M. H., *Aircraft Design: A Systems Engineering Approach*, Wiley, 2012.
