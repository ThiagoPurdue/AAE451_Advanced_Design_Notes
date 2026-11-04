---
title: Design missions and energy reserves
short_title: Design missions and reserves
---

This is Lecture 5, *Design Missions and Energy Reserves*. The RFP prescribes the trainer's two missions segment by segment. The work is to interpret them: find what sizes the aircraft, resolve what the RFP leaves open, and turn each answer into an assumption or a requirement before the {term}`SRR`. Every number on this page comes from the RFP.

:::{note} What to take from this lecture
- The training flight and the ferry flight are both prescribed. Fly both in the sizing code before believing either one sizes the fuel.
- Point performance at 15,000 ft and half fuel sets the thrust class. The runway numbers are checks.
- FCLP is a design condition. It couples fuel, nose geometry, and gear loads.
- Every open question becomes a dated assumption in {term}`ASORT` or a derived requirement.
:::

## A prescribed mission

:::{table} What the RFP fixes for the Navy Jet Trainer, and the work that leaves.
:label: tbl-mission-prescribed

| Item | Navy Jet Trainer |
| --- | --- |
| Mission definition | Two profiles, prescribed segment by segment |
| Your task | Interpret: find what sizes the aircraft |
| Reserves | Explicit: 30 and 45 minutes at maximum endurance |
| Energy bookkeeping | Fuel |
| Sizing risk | Assuming that the ferry flight sizes the fuel |

:::

:::{admonition} Navy Jet Trainer
:class: navy

The RFP gives the missions; the team interprets them. Know that before the sizing code runs. Both profiles and their segment tables are on the [RFP page](../navy-rfp/navy-rfp.md).
:::

## The training flight

The RFP prescribes ten segments ({numref}`fig-training-flight-profile`). The segment table is on the RFP page, [Training flight](#tbl-training-mission).

:::{figure} figures/training-flight-profile.svg
:label: fig-training-flight-profile
:alt: Altitude against time for the training flight, with dashed lines at 10,000 and 20,000 feet. Segments 1 and 2 at sea level, 15 minutes at idle and 1 minute at takeoff thrust. Segments 3 and 4 climb at 250 KCAS and cruise at 20,000 feet to 50 nautical miles. Segment 5 descends at idle to 10,000 feet. Segment 6 is 30 minutes at military thrust at Mach 0.60. Segments 7 and 8 climb and return at 20,000 feet. Segment 9 descends at idle. Segment 10 is FCLP, 30 minutes at approach speed in landing configuration, drawn as three small bumps. A note marks the reserve of 30 minutes at maximum endurance.
:width: 100%

The training flight as the RFP prescribes it, with the condition the RFP states for each segment. Time is not to scale.
:::

:::{admonition} Navy Jet Trainer
:class: navy

Segments 4 and 8 say "speed/thrust not specified." That choice is yours, and it moves the fuel number.
:::

## The mission that sizes the fuel

::::{grid} 1 1 2 2

:::{card}
:header: Training flight
- About 100 nmi of transit.
- 30 min at military thrust, Mach 0.60.
- 30 min at approach speed in landing configuration (FCLP).
- 15 min at idle. Reserve 30 min.
:::

:::{card}
:header: Ferry flight
- 600 nmi, altitude and speed free.
- 10 min approach allowance.
- Reserve 45 min.
:::

::::

The winner is not obvious. The training flight is short, but it spends an hour at high thrust or high drag. The answer depends on the part-power specific fuel consumption.

:::{admonition} Navy Jet Trainer
:class: navy

Fly both missions in the sizing code. State which one sizes the fuel and by how much. Do not assume.
:::

## Point performance

The altitude points set the thrust class.

:::{table} Point performance requirements of the RFP, all in the International Standard Atmosphere. T is the threshold, O the objective.
:label: tbl-point-performance

| Requirement | Value | Condition |
| --- | --- | --- |
| Maximum operating speed | Mach 0.78 (T), Mach 0.90 (O) | MTOW less 50% fuel, 25,000 ft |
| {term}`Specific excess power` | 90 ft/s (T), 125 ft/s (O) | MTOW less 50% fuel, 15,000 ft |
| Sustained load factor | +4.0 g (T), +6.0 g (O) | MTOW less 50% fuel, 15,000 ft |
| Takeoff distance | 5,000 ft | MTOW, 5,000 ft density altitude |
| {term}`Critical field length` | 6,000 ft | MTOW, 5,000 ft density altitude |
| Landing distance | 5,000 ft | {term}`MLW`, 5,000 ft density altitude |

:::

Specific excess power and sustained load factor at 15,000 ft and half fuel set the thrust class. The runway numbers are checks. The gap between threshold and objective can change the thrust class.

:::{admonition} Navy Jet Trainer
:class: navy

MLW appears in a requirement but is never defined. Your team defines it and defends the definition.
:::

## FCLP shapes the aircraft

::::{grid} 1 1 3 3

:::{card}
:header: Fuel
The 30 min FCLP allowance at approach speed in landing configuration couples fuel volume to approach L/D. A draggy approach configuration is paid for in mission fuel.
:::

:::{card}
:header: Nose geometry
Over-the-nose visibility: the whole carrier stern in view on a 3.5° glide slope at approach speed. This sets nose geometry, seat height, and approach attitude together.
:::

:::{card}
:header: Gear and structure
Full-stop FCLPs are the stated role. Repeated patterns put many landing cycles on the gear and the structure. The RFP gives no sink rate; put your sourced assumption in ASORT.
:::

::::

:::{figure} ../lecture-03/figures/t45.jpg
:label: fig-t45-replaced
:alt: T-45 Goshawk in flight, a low-wing jet with side inlets and a single fin.
:width: 55%

The T-45 Goshawk, the aircraft being replaced. U.S. Navy photo by Lt. j.g. John A. Ivancic, public domain, via Wikimedia Commons.
:::

:::{admonition} Navy Jet Trainer
:class: navy

No carrier landings, yet the FCLP pattern is the reason this aircraft exists. Treat it as a design condition.
:::

## Questions your team must answer

:::{exercise} The seven questions
:label: ex-trainer-questions

1. Which mission sizes the fuel, and by how much? Both flown in code.
2. How many engines? What does critical field length mean for that count under the MIL-STD-3013B definitions?
3. What is MLW, and what sets it?
4. What speed and thrust fly the training-mission transit legs, and why?
5. What sink rate is the landing gear designed for?
6. What must "basic maneuvers" include: spins, aerobatics, departure resistance?
7. What approach speed satisfies the 3.5° visibility geometry?
:::

:::{admonition} Navy Jet Trainer
:class: navy

Each answer is a dated ASORT assumption or a requirement with a source. Where the RFP is silent, the team decides and records it.
:::

## From answers to artifacts

1. Every answer becomes one of two artifacts: a dated, sourced assumption in the ASORT file, or a derived requirement in `_Requirements.slreqx` traced to a {term}`need`.
2. An answer that lives on a slide only, or in a teammate's head, does not exist at the SRR.
3. The check is the sizing code: it runs both missions and names the one that sizes the fuel.

:::{admonition} Navy Jet Trainer
:class: navy

[A03](../assignments/a03.md) Deliverable 1 recomputes every segment your CONOPS states, and Deliverable 4 models both missions and reports which one sizes the fuel. These answers are their inputs.
:::

## This week

1. Answer the seven questions. One owner per question, named.
2. Enter each answer in ASORT or the requirement set. Date it and source it.
3. Run the sizing code with the updated mission. Report what moved.

:::{tip}
Where exact wording matters, as for the reserves and the FCLP visibility requirement, read the RFP text itself.
:::

:::{important} Summary
- The trainer missions are prescribed: find what sizes the aircraft, and fly both before believing either.
- Open questions get owners. Each becomes a dated assumption or a derived requirement before the SRR.
- Next is SRR week. Bring the answers.
:::

## References

- AIAA Aircraft Design Technical Committee, *2026-2027 Undergraduate Team Aircraft Design Competition Request for Proposal: Design of a Navy Jet Training Aircraft*, AIAA, 2026.
- Department of Defense, *MIL-STD-3013B, Glossary of Definitions, Ground Rules, and Mission Profiles to Define Air Vehicle Performance Capability*, 2022.
- Raymer, D. P., *Aircraft Design: A Conceptual Approach*, 6th ed., AIAA Education Series, 2018, Chapter 3.
