---
title: Needs, mission statement and concept of operations
short_title: Needs and CONOPS
---

This is the second part of Lecture 1. Before an aircraft is sized, the team has to know who it is for, what they need to do with it, and how it will be operated. This page covers the needs phase, the mission statement, the concept of operations ({term}`CONOPS`) and the mission profile.

## The needs phase

::::{grid} 1 1 2 2

:::{card}
:header: Customer needs
Find out what the customers require from the aircraft.

- **Gather customer feedback** through surveys, interviews and focus groups.
- **Define the requirements** for performance, capacity, cost and reliability.
- **Prioritize the needs** into essential and desirable features.
:::

:::{card}
:header: Stakeholders
A {term}`stakeholder` is anyone with an interest in the project.

- **List the stakeholders.** Customers, investors, regulators, suppliers and end users.
- **Engage them** through regular updates, feedback sessions and meetings.
- **Address their needs.** The design has to meet the expectations of all of them.
:::

::::

:::{prf:definition} Need
:label: def-need

A {term}`need` states what a stakeholder wants to be able to do. It does not name a solution.
:::

:::{prf:definition} Requirement
:label: def-requirement

A {term}`requirement` is an obligation on the system, written as "The system shall...". [](requirements.md) covers how to write one.
:::

Needs and requirements are kept in separate sets and traced to each other.

:::{admonition} Navy Jet Trainer
:class: navy

The RFP is written by one customer, but the trainer has many stakeholders. List everyone who flies, supports, pays for or approves the aircraft. For each RFP section, ask whether it states a need, and whose need it is, or a constraint. Assignment A01 asks you to work out the stakeholders and their needs from the RFP.
:::

## Mission statement

The mission statement is the first step of requirements analysis. It is a short statement of the purpose of the product. It includes:

- The **environment** the product operates in, and any special considerations.
- An **understanding** between the customer and the developer about what the product does.
- A brief description of the **product capabilities** and the main benefits to the stakeholders.
- The **assumptions and constraints** that guide development.
- The **business goals**, the **target markets** and the **stakeholders**.

:::{important}
The mission statement is the primary exhibit at the System Requirements Review ({term}`SRR`).
:::

:::{warning} Keep the product out of the mission statement
Do not name a specific product in the mission statement, even when you already know the general type of aircraft. This is hard in a course project, where the RFP already says "jet trainer". Write the purpose and the capabilities, and leave the configuration out.
:::

### Example: a 2022 student project

```{figure} figures/student-mission-statement-2022.jpg
:label: fig-mission-statement-example
:alt: Slide titled Mission Statement from a 2022 Purdue student project. It shows the mission statement text, an illustration of small aircraft flying over a city at night, credited to Gibson, the U.S. Forest Service shield and the Purdue School of Aeronautics and Astronautics logo.
:width: 85%

Mission statement slide from a 2022 Purdue student project for the U.S. Forest Service. The text of the statement is quoted below.
```

The mission statement on the slide reads:

> Generate a concept, based on urban or regional air mobility aircraft, of an advanced firefighting aircraft system for the U.S. Forest Service capable of: performance in serious wildfire conditions, dropping 3000 gallons of water per pass, operation from small public-use airports, and fitting within the Forest Service budget.

The statement names the customer, the operating environment, one measurable capability (3000 gallons per pass) and a cost constraint. It also names a product class, urban or regional air mobility aircraft, which a mission statement should avoid.

## Concept of operations

:::{prf:definition} Concept of operations
:label: def-conops

A CONOPS "describes how the system will be operated during life-cycle phases to meet stakeholder expectations" (NASA Systems Engineering Handbook, NASA SP-2007-6105).
:::

The CONOPS does three things:

- It drives the development of the requirements and the architecture.
- It shows the system goals from the operator's side.
- It is the basis for the later definition of the system.

A useful way to start is to tell the story of a day in the life of your aircraft. {numref}`tbl-conops-contents` lists what a CONOPS covers.

:::{table} Contents of a concept of operations.
:label: tbl-conops-contents

| Topic | What it covers |
| --- | --- |
| Life-cycle phases | Development: design, testing and certification. Operation: deployment, routine operations and maintenance. Disposal: decommissioning and recycling |
| Operational scenarios | The design mission, which is the most demanding mission the aircraft flies. Routine missions, the typical day-to-day operations. Emergency scenarios and the procedures for them |
| Ground operations | Pre-flight checks and preparation. Scheduled and unscheduled maintenance. Logistics support: supply chain and parts |
| Flight operations | Takeoff and landing procedures and requirements. In-flight operations: navigation, communication and mission tasks. Crew training |
| Infrastructure and facilities | Airports and airfields for takeoff, landing and ground support. Maintenance facilities. Support facilities: hangars, fuel storage and other infrastructure |

:::

:::{important}
Be sure you understand and can explain how your operator will use your aircraft.
:::

### Example: an urban air mobility CONOPS

```{figure} figures/wisk-uam-conops.jpg
:label: fig-wisk-conops
:alt: Illustration of urban air mobility in a city. An uncrewed passenger aircraft flies between vertiports on buildings and an airport. Labels name the communications, navigation and surveillance infrastructure, the fleet operations center with multi-vehicle supervisors and fleet managers, supplemental aeronautical data, the booking system, passengers, air traffic control, the vertiport operations center with the vertiport manager, the vertiport and ground management. Each label carries one or two lines that describe its role.
:width: 100%

A concept for advanced air mobility in urban environments. From Wisk Aero, *Concept of Operations for Uncrewed Urban Air Mobility* (2022), Figure 1, as shown in the lecture.
```

{numref}`fig-wisk-conops` places the aircraft among everything else it needs to operate. The aircraft has no pilot on board and carries four to six passengers. A multi-vehicle supervisor in a fleet operations center fills the legal role of pilot in command and supervises several aircraft. Fleet managers schedule and dispatch them. Passengers book flights through a booking system. Vertiports are fixed locations where aircraft take off and land, load and unload passengers and are serviced. A vertiport manager runs each vertiport, and ground crews handle the aircraft there. Air traffic control separates traffic. Communication, navigation and surveillance infrastructure carries the command and control datalinks.

Each of these elements puts requirements on the aircraft.

### Example: Purdue GoAERO team

```{figure} figures/goaero-conops.svg
:label: fig-goaero-conops
:alt: Diagram centered on an orange box labeled Operating Zone. Above it is the competition vehicle, a quadcopter, described as a semi-autonomous aircraft capable of transporting a single passenger and medium payloads. Top left, a GPS satellite that gives accurate positioning data, joined to the vehicle by a dotted line. Top right, icons of a storm cloud, a rain cloud, a person, a package and a target, labeled Areas of Operation: fly to and from objects of interest with autonomous recognition, adapting to diverse conditions. Left, gate and marker icons labeled Obstacles: the vehicle navigates complex obstacle environments using onboard sensors. Bottom center, Transportation: ground transport for the vehicle and the ground station to arrive at the required area of operation. Bottom right, a satellite dish labeled Ground Station: command and control center for the operator to fly the vehicle, joined to the vehicle by a dotted line. Green arrows run from the vehicle to the obstacles and to the areas of operation, from the obstacles and from the areas back to the operating zone, and from the operating zone up to the vehicle.
:width: 100%

CONOPS of the Purdue GoAERO team, redrawn from the lecture slide. Green arrows are flights. Red dotted lines are data links.
```

The GoAERO diagram is centered on the operating zone. It shows how the vehicle and the ground station arrive, where the vehicle flies, what it must avoid, and which links it depends on.

:::{admonition} Navy Jet Trainer
:class: navy

A day in the life of the trainer starts at a land base. The RFP gives two missions: the training flight, with basic maneuvers and {term}`FCLP` touch-and-go landings, and the ferry flight. It also says what the trainer is not required to do: it does not have to land on carriers. Your CONOPS should also cover the people who operate and support the aircraft. Assignment A01 asks for the CONOPS and states what it must contain.
:::

## Mission profile

:::{prf:definition} Mission profile
:label: def-mission-profile

The {term}`mission profile` draws one mission as altitude against distance or time, divided into numbered segments. Each segment has a condition: an altitude, a speed, a time, a distance or a thrust setting.
:::

Mission analysis later turns each segment into a weight fraction. {numref}`fig-combat-mission` is a generic combat mission.

```{figure} figures/combat-mission-profile.svg
:label: fig-combat-mission
:alt: Altitude against distance for a mission that starts and ends at the origin, drawn as a filled profile. Phase 1, engine start and takeoff. Phase 2, accelerate and climb to cruise speed and altitude. Phase 3, cruise to the destination. Phase 4, accelerate to a high-speed dash. Phase 5, combat, drawn as a descending coil. Phase 6, climb and cruise back to the origin at a higher altitude. Phase 7, descend and loiter, drawn as a small loop. Phase 8, land, taxi and engine shutdown. A list inside the profile names the eight phases.
:width: 90%

A generic combat mission profile. Redrawn after the figure credited to Raymer on the lecture slide. Phase numbers match {numref}`tbl-combat-mission`.
```

:::{table} Phases of the generic combat mission.
:label: tbl-combat-mission

| Phase | Description |
| ---: | --- |
| 1 | Engine start and takeoff |
| 2 | Accelerate and climb to cruise speed and altitude |
| 3 | Cruise to destination |
| 4 | Accelerate to high-speed dash |
| 5 | Combat |
| 6 | Cruise back to origin |
| 7 | Loiter |
| 8 | Land, taxi and engine shutdown |

:::

:::{admonition} Navy Jet Trainer
:class: navy

The RFP draws both of its mission profiles. They are redrawn in [](../navy-rfp/navy-rfp.md#fig-navy-training) and [](../navy-rfp/navy-rfp.md#fig-navy-ferry). Some segments are fully defined, such as the 30 minutes of basic maneuvers at 10,000 ft and Mach 0.60. Others are left to you, such as the cruise speed of the training flight or the cruise altitude of the ferry flight. Mark each choice you make as an assumption. [](../navy-rfp/navy-rfp.md#ex-rfp-assumptions) asks you to list them.
:::

## References

- NASA, *NASA Systems Engineering Handbook*, NASA SP-2007-6105 Rev 1, 2007.
- Raymer, D. P., *Aircraft Design: A Conceptual Approach*, 6th ed., AIAA Education Series, 2018.
- Wisk Aero, *Concept of Operations for Uncrewed Urban Air Mobility*, 2022.
