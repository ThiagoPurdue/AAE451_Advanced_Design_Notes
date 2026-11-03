---
title: The aircraft design process
short_title: Design process
---

This is the first part of Lecture 1, *Introduction to Aircraft Design*. It covers the phases of an aircraft program, the work done in conceptual design, the market and business case, the feasibility study and the systems view of an aircraft. The second part, [](needs-and-conops.md), covers needs and operations. The third part, [](requirements.md), covers requirements.

## Phases of an aircraft program

An aircraft program runs through six phases, from the first feasibility study to the retirement of the fleet ({numref}`fig-design-phases`).

```{figure} figures/design-phases.svg
:label: fig-design-phases
:alt: Six arrows in a row. Phase 0 feasibility study, Phase 1 conceptual design, Phase 2 preliminary design, Phase 3 detail design, Phase 4 entry into service and production, Phase 5 operation and phase-out.
:width: 100%

Phases of an aircraft program. Redrawn after Venson, as credited on the lecture slide.
```

Phase 0, the feasibility study, asks whether the program should start at all. Phases 1 to 3 are design. Phase 4 is certification, entry into service and production. Phase 5 is operation of the fleet and its retirement.

This course is Phase 1, conceptual design, carried to a Preliminary Design Review at the end of the semester.

## What happens in conceptual design

{numref}`fig-design-process-flow` shows the conceptual design process as Nicolai and Carichner describe it. The process starts with the customer and the mission requirements. It ends with a point design that is ready for preliminary design.

```{figure} figures/design-process-flow.svg
:label: fig-design-process-flow
:alt: Flow chart in five rows. Row 1, the customer leads to mission requirements, then the concept of operations, then design guidelines (radius, payload, altitude, signature). Two input boxes feed this row. One is evaluating and negotiating requirements with the customer. The other is the system approach, technology, measures of merit and selection criteria. Row 2 runs back from configuration sketches to concepts 1 to n, initial sizing and select configuration. Row 3 runs from functional inputs (aero, propulsion, weights, structure) to design trades (W/S, T/W, AR, sweep), select preferred configuration and the baseline design. Row 4 runs from mission trades (radius, payload, speed, time) and technology trades (TSFC, engine T/W, empty weight, L/D) to a decision, satisfied? Risk assessment feeds the decision. If no, the design returns to initial sizing through connector A. If yes, trade results are shared with the customer. Row 5 asks whether the requirements change. If yes, the process returns to the design guidelines. If no, the point design (outer mold line, arrangement, performance, subsystems, risk, cost, technology readiness level 3 to 4) goes on to preliminary design.
:width: 100%

The conceptual design process. Simplified and redrawn after Nicolai and Carichner (2010). The two boxes marked A are one connection: an unsatisfactory trade result sends the design back to initial sizing.
```

Read the chart in four steps:

1. **Define the problem.** The customer states the mission. The team writes the concept of operations and the design guidelines. The measures of merit are set here. These are the quantities used to rank concepts, such as life cycle cost or takeoff weight.
2. **Find a baseline.** The team sketches several configurations, sizes each one and selects one. Design trades on wing loading (W/S), thrust-to-weight ratio (T/W), aspect ratio (AR) and sweep refine it into a baseline design.
3. **Trade and decide.** Mission trades change the requirements, such as radius, payload or speed. Technology trades change the assumptions, such as specific fuel consumption, engine thrust-to-weight ratio or empty weight. Each trade is plotted as the change in a measure of merit. If the result is not acceptable, the design returns to initial sizing.
4. **Share and close.** The trade results go back to the customer. If the customer changes a requirement, the process starts again from the design guidelines. If not, the point design goes forward.

Requirements are not fixed at the start. A trade study can show that one requirement costs far more than it is worth, and the customer may then change it.

{numref}`tbl-design-phases-detail` shows what is known, what is produced and how mature the technology is at the end of each design phase.

:::{table} What is known and what is produced in each design phase, after Nicolai and Carichner (2010). TRL is the technology readiness level.
:label: tbl-design-phases-detail

| Aspect | Phase 1, conceptual design | Phase 2, preliminary design | Phase 3, detail design |
|---|---|---|---|
| Known | Basic mission requirements: range, altitude and speed. Basic material properties: strength-to-density ratio σ/ρ, stiffness-to-density ratio E/ρ, cost per pound | Aeroelastic, fatigue and flutter requirements. Overall strength requirements | Local strength requirements. Producibility. Functional requirements |
| Results | Geometry: airfoil type, aspect ratio, thickness ratio t/c, taper ratio λ, sweep Λ. Design objectives: drag level, weight goals, cost goals | Basic internal arrangement. Complete external configuration, with camber and twist distribution and local flow problems solved. Major loads, stresses and deflections | Detail design of mechanisms, joints, fittings and attachments. Design refinements from testing |
| Output | Feasible design | Mature design | Shop designs |
| TRL | 2 to 3 | 4 to 5 | 6 to 7 |
:::

The slide illustrates each phase with a sketch. Phase 1 compares two wing planforms. Phase 2 compares two airfoil sections and two incidence angles, 3° and 5°. Phase 3 shows the internal structure of a wing box.

Raymer describes the same three phases by the questions each one answers ({numref}`fig-design-funnel`).

```{figure} figures/design-funnel.svg
:label: fig-design-funnel
:alt: Three stacked funnels between requirements at the top and fabrication at the bottom. Conceptual design asks what requirements drive the design, what it should look like, its weight and cost, what trade-offs to consider, what technologies to use, and whether the requirements give a viable and salable aircraft. Preliminary design freezes the configuration, develops the lofting (surface definition) and the test and analytical database, designs the major items and develops the cost estimate. Detail design designs the pieces to be built and the tooling and fabrication process, tests major items such as structure and landing gear, and finalizes the weight and performance estimates.
:width: 85%

Conceptual, preliminary and detail design. Redrawn after Raymer (2018).
```

Raymer adds two remarks. Preliminary design is where the company commits to the program. He calls the commitment made at that stage, based on that cost estimate, "you bet your company". Detail design is where the real numbers are learned. Every number in conceptual design is an estimate. Keep track of what each estimate rests on.

:::{admonition} Navy Jet Trainer
:class: note

The RFP asks for "a preliminary design". In this course you carry the design through conceptual design to a Preliminary Design Review. Expect your weights and performance to change as the methods improve during the semester. Record the source of every number so you can update it.
:::

## Market analysis and business case

An aircraft program starts with a market. The market analysis finds the demand and the competition:

- **Market segments.** Commercial, military, business and other segments.
- **Competitors.** Their strengths, weaknesses and market share.
- **Demand forecast.** Future trends, growth areas and the age of the fleets in service.

The business case justifies the program in terms of profit and strategic fit:

- **Cost analysis.** Development, production and operating costs against the expected revenue.
- **Return on investment.** The financial return the program can produce.
- **Risk assessment.** Technical, financial and market risks, and how to reduce them.

The lecture recommends the video [Turboprops, regional aviation and other stuff](https://www.youtube.com/watch?v=_33Zqer6Nzc) by Marcelo Alves Araujo.

### Example: narrow-body aircraft

{numref}`fig-narrowbody-production` compares production numbers of narrow-body airliners. Two families dominate. The Airbus A320 family and the Boeing 737 family together account for more aircraft than all the others combined.

```{figure} figures/narrowbody-production.svg
:label: fig-narrowbody-production
:alt: Horizontal bar chart of the number of aircraft produced. Airbus A318, A319, A320 and A321, 16,000. Boeing 737 family, 10,500. Bombardier CRJ family, 1,945. Embraer E-Jets first generation, 1,500. McDonnell Douglas MD-80 and MD-90, 1,191. COMAC C919, 305. Fokker 100, 283. Bombardier CSeries, now the Airbus A220, 220. Sukhoi Superjet 100, 200. Embraer E-Jets E2, 200. Fokker 70, 47. Mitsubishi SpaceJet, 0.
:width: 90%

Narrow-body aircraft production. Values as shown on the lecture slide. They are rounded and are not current production totals.
```

A new aircraft enters a market that already has a leader. The Mitsubishi SpaceJet, formerly the MRJ, is the example at the bottom of the chart.

```{figure} figures/spacejet-ja21mj.jpg
:label: fig-spacejet
:alt: Photograph of a white Mitsubishi MRJ90 with red and black stripes and MRJ on the tail, on its takeoff roll.
:width: 80%

The first MRJ90 flight-test aircraft, JA21MJ, in Japan in 2016. Photo by CHIYODA I, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:JA21MJ_TAKEOFF_ROLL.jpg).
```

The SpaceJet flew and went through years of flight testing, yet no aircraft was delivered. Mitsubishi Heavy Industries ended the program in 2023, citing the cost and time still needed for type certification and a weak market. The lecture slide shows one of the flight-test aircraft being cut up. A program can fail on certification, cost and schedule even after the aircraft flies.

## Feasibility study

The feasibility study is Phase 0. It checks four things:

- **Technical feasibility.** Can the design be built with current technology?
- **Economic viability.** Is the program financially sustainable?
- **Operational feasibility.** Can the aircraft be operated within existing infrastructure?
- **Environmental impact.** What are the negative environmental effects, and how can they be reduced?

:::{admonition} Navy Jet Trainer
:class: note

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

:::{admonition} Navy Jet Trainer
:class: note

What is Level 1 for the trainer, and which other elements sit beside the aircraft in it? Level 3 starts with the list in the RFP's aircraft systems section: propulsion, landing gear, electrical, hydraulics, fuel, pressurization, air conditioning and oxygen, avionics, control system actuators and flight control computers. Ask which requirements the trainer inherits from Level 1 before writing requirements for Level 2.
:::

## References

- Nicolai, L. M., and Carichner, G. E., *Fundamentals of Aircraft and Airship Design, Volume I: Aircraft Design*, AIAA Education Series, 2010.
- Raymer, D. P., *Aircraft Design: A Conceptual Approach*, 6th ed., AIAA Education Series, 2018.
- Sadraey, M. H., *Aircraft Design: A Systems Engineering Approach*, Wiley, 2012.
