---
title: The Navy Jet Trainer RFP
short_title: Navy Jet Trainer RFP
---

Teams in this course design to one of two AIAA 2026-27 RFPs. These notes follow the Undergraduate Team Aircraft Design Competition RFP, *Design of a Navy Jet Training Aircraft*, issued by the AIAA Aircraft Design Technical Committee. This page summarizes it. Read the full RFP on the [AIAA design competitions page](https://aiaa.org/get-involved/university-students/design-competitions/). Where this summary and the RFP differ, the RFP governs.

The RFP states that its attributes and constraints come from open-source material, tailored for a student design. They are not official Navy requirements.

## What the Navy asks for

The Navy uses the T-45 Goshawk for intermediate and advanced pilot training. The airframe and engines are aging. The Navy also needs to prepare students for fourth- and fifth-generation fighter and attack aircraft.

The new trainer is land based. It is not required to land on carriers or to meet carrier suitability requirements. It must perform full-stop Field Carrier Landing Practice (FCLP) on land runways.

The objective is a preliminary design of an affordable, effective land-based trainer for naval aviators. It must meet the airworthiness criteria of MIL-HDBK-516C. The RFP writes this as "MIL-HDB-516C". Speeds and performance parameters are defined in MIL-STD-3013B.

## Performance requirements

The RFP gives three performance requirements a threshold (T) and an objective (O). The three field lengths are single required values. A threshold is the minimum acceptable value. An objective is the value the customer would like. The RFP asks for design and cost trade studies between the two. All calculations use the International Standard Atmosphere.

:::{table} Performance requirements of the Navy Jet Trainer RFP. MTOW is maximum takeoff weight and MLW is maximum landing weight.
:label: tbl-rfp-performance

| Requirement | Threshold or required value | Objective | Weight | Altitude |
|---|---|---|---|---|
| Maximum operating speed | Mach 0.78 | Mach 0.90 | MTOW less 50% fuel | 25,000 ft pressure altitude |
| Specific excess power | 90 ft/s | 125 ft/s | MTOW less 50% fuel | 15,000 ft pressure altitude |
| Sustained load factor | +4.0 g | +6.0 g | MTOW less 50% fuel | 15,000 ft pressure altitude |
| Takeoff distance | 5,000 ft | none given | MTOW | 5,000 ft density altitude |
| Critical field length | 6,000 ft | none given | MTOW | 5,000 ft density altitude |
| Landing distance | 5,000 ft | none given | MLW | 5,000 ft density altitude |
:::

## Cockpit accommodation

The cockpit seats two pilots and must fit the full range of pilot sizes in {numref}`tbl-rfp-cockpit`.

:::{table} Pilot size range the cockpit must accommodate.
:label: tbl-rfp-cockpit

| Dimension | Minimum | Maximum |
|---|---|---|
| Weight, nude | 103 lb | 205 lb |
| Height | 62 in | 77 in |
| Sitting height | 31 in | 40.9 in |
| Sitting eye height | 26 in | 31.4 in |
:::

The RFP adds these cockpit requirements:

- Flight suit, equipment and survival kit weigh 35 lb per pilot.
- The cockpit accommodates two Martin-Baker Mk 14 ejection seats, or similar.
- Oxygen comes from an On-Board Oxygen Generating System (OBOGS) or from bottles.
- Cockpit altitude is no greater than 8,000 ft.
- During FCLP, the view over the nose keeps the whole carrier stern in sight on a 3.5° glide slope at landing approach speed.

## Missions

Internal fuel must cover two missions. Each has its own fuel reserve.

### Training flight

```{figure} figures/navy-training-mission.svg
:label: fig-navy-training
:alt: Altitude against distance for the training flight. The aircraft starts at 0 ft for segments 1 and 2, climbs to 20,000 ft in segment 3, cruises in segment 4, descends to 10,000 ft in segment 5, maneuvers at 10,000 ft in segment 6, climbs back to 20,000 ft in segment 7, cruises home in segment 8, descends to sea level in segment 9 and flies touch-and-go landings in segment 10. Arrows mark 50 nm from the start of the climb to the start of the maneuvers, and 50 nm from the end of the maneuvers to the end of the descent.
:width: 100%

Training flight profile, redrawn from the Navy Jet Trainer RFP. Segment numbers match {numref}`tbl-training-mission`. Distance is not to scale.
```

:::{table} Training flight segments, from the RFP.
:label: tbl-training-mission

| Segment | Description |
|---|---|
| 1 | Engine start, warm-up and taxi: 15 minutes at idle thrust |
| 2 | Takeoff and acceleration to climb speed: 1 minute at takeoff thrust |
| 3 | Cruise climb to 20,000 ft at 250 KCAS |
| 4 | Cruise to 50 nm from the departure airport, speed and thrust not specified |
| 5 | Descent to 10,000 ft at idle thrust |
| 6 | Basic maneuvers at 10,000 ft: 30 minutes at military thrust at Mach 0.60 |
| 7 | Climb to 20,000 ft at 250 KCAS |
| 8 | Return to the departure airport, speed and thrust not specified |
| 9 | Descent to sea level at idle thrust |
| 10 | FCLP touch-and-go landings: fuel for 30 minutes at approach speed in landing configuration, flaps as required, gear down |
:::

The fuel reserve for the training flight is 30 minutes at maximum endurance speed in cruise configuration.

### Ferry flight

```{figure} figures/navy-ferry-mission.svg
:label: fig-navy-ferry
:alt: Altitude against distance for the ferry flight. Segments 1 and 2 are at 0 ft. Segment 3 climbs to a cruise altitude chosen by the team, segment 4 cruises, segment 5 descends to sea level and segment 6 is the approach and landing. An arrow marks 600 nm across segments 3 to 5.
:width: 100%

Ferry flight profile, redrawn from the Navy Jet Trainer RFP. Segment numbers match {numref}`tbl-ferry-mission`. Distance is not to scale.
```

:::{table} Ferry flight segments, from the RFP.
:label: tbl-ferry-mission

| Segment | Description |
|---|---|
| 1 | Engine start, warm-up and taxi: 15 minutes at idle thrust |
| 2 | Takeoff and acceleration to climb speed: 1 minute at takeoff thrust |
| 3 | Cruise climb to the cruise altitude you choose |
| 4 | Cruise at the altitude and speed you choose |
| 5 | Descent to sea level at the speed you choose |
| 6 | Approach and landing: fuel for 10 minutes at approach speed in landing configuration, flaps as required, gear down |
:::

Segments 3 to 5 together cover 600 nm. The fuel reserve for the ferry flight is 45 minutes at maximum endurance speed in cruise configuration.

## Analyses the RFP requires

The RFP lists the analyses a proposal must contain.

Mass properties
: An empty weight estimate with component breakdowns. At least these groups: propulsion; airframe structure (wing, empennage, landing gear with wheels, tires and brakes, fuselage); systems (instruments and avionics, fuel and oil, hydraulic, pneumatic and electrical systems if chosen). A center of gravity calculation for all loading cases. An operational weight roll-up to MTOW with empty weight, pilots, payload and fuel.

Structures
: A conceptual structural layout. The material of each major component. The strength of the structure compared with what the ultimate loads require. The major load paths. Advanced materials may be used to reduce empty weight.

Propulsion
: The RFP gives no engine data. Identify the engine type, manufacturer and model, and document the data sources. Document the installed thrust and fuel flow models.

Aerodynamics
: Lift and drag for climb, cruise, maneuvering, takeoff and landing. The wing planform and airfoil selection. The derivation of the lift and drag models.

Aircraft systems
: Description, function, location and layout of the major systems: propulsion, landing gear, electrical, hydraulics, fuel, pressurization with air conditioning and oxygen, avionics, control system actuators and flight control computers.

Stability and control
: Analysis for climb, cruise, maneuvering, takeoff and landing. The aircraft may be statically stable or unstable. Specify the flight control system architecture and its major components. Give the criteria for horizontal and vertical tail sizing, the longitudinal static stability and trim analysis, and the longitudinal and lateral-directional dynamic stability analysis.

Cost
: The cost of engineering and manufacturing development, testing and certification, in 2030 dollars. Two production phases: Low Rate Initial Production of 10 aircraft and Full Rate Production of 500 aircraft. Unit flyaway cost for Full Rate Production and the full program life cycle cost. Direct operating cost per flight hour, including fuel, oil, tires, brakes, batteries and other consumables, and maintenance cost per flight hour. Explain the design features and processes that raise or lower cost. Discuss cost trades between threshold and objective requirements.

Certification
: The aircraft meets MIL-HDBK-516C. Definitions of speeds and performance parameters come from MIL-STD-3013B.

## Data the RFP requires

:::{table} Design data required for the final configuration.
:label: tbl-rfp-design-data

| No. | Design data |
|---|---|
| 1 | Dimensioned three-view drawing with the neutral point, the tail moment arms and a table of aircraft areas |
| 2 | 3-D model imagery |
| 3 | Cockpit layout drawing with pilots, equipment and controls |
| 4 | Location and volume of the fuel tanks |
| 5 | Inboard profile |
| 6 | Landing gear drawing, extended and retracted |
| 7 | Weight statement, including minimum and maximum crew weights and single-pilot operation |
| 8 | Center of gravity envelope |
| 9 | Wing and empennage geometry: aspect ratio, taper ratio, thickness, sweep and a description of the high-lift devices |
| 10 | Control surface sizes |
| 11 | Drag polars for cruise, takeoff and landing configurations |
| 12 | Structural materials |
:::

:::{table} Performance data required for the final configuration.
:label: tbl-rfp-performance-data

| No. | Performance data |
|---|---|
| 1 | Trade study results that find the minimum weight aircraft |
| 2 | Flight envelope (altitude against speed) and V-n diagram |
| 3 | Maximum dive speed |
| 4 | Segment-by-segment results for each mission: weight, fuel used, time, distance, altitude and speed |
| 5 | Takeoff field length at MTOW and landing field length at MLW |
| 6 | Summary of the stability and control analyses |
| 7 | Breakdown of development and manufacturing costs. Life cycle cost is optional here |
:::

The proposal must also show the alternative concepts the team considered and the method used to select one. Present the method and rationale for the down-select. At a minimum, give a qualitative assessment of the strengths and weaknesses of each alternative. A quantitative comparison against the measures of merit makes the case stronger. Include the major trade studies behind the optimization, sizing, arrangement and integration of the selected concept. Quantitative data must show that the selected concept works and best meets the requirements.

## How proposals are judged

The AIAA rules that apply to every design competition give the approximate judging points in {numref}`tbl-aiaa-judging` unless an RFP states otherwise. The Navy Jet Trainer RFP does not.

:::{table} AIAA judging criteria, from the AIAA Design Competitions Official Rules (July 2026).
:label: tbl-aiaa-judging

| Criterion | Points | What judges look for |
|---|---|---|
| Technical content | 40 | Requirements, concept selection, quantitative analysis of the selected concept, tools and methods, technical soundness and completeness |
| Organization and presentation | 20 | Neatness and style, logical flow, a clear introduction, uncluttered figures and tables, grammar, citation of previous work, substantiated conclusions |
| Originality | 10 | Independent thinking, unconventional concepts considered, adapted or new design tools |
| Practical application and feasibility | 30 | Technical feasibility, economic feasibility, broader impacts |
:::

The same rules limit the report to 100 double-spaced pages on letter paper, with type no smaller than 10 pt Times New Roman and 1 in margins. Pages with other spacing are counted at 1.75 pages each. Every computer code used must be listed with the URL where it can be obtained. The rules discourage generative AI. If any AI tool was used for the design or the report, a one-page disclosure must be attached outside the page count.

:::{admonition} Reading the RFP
:class: tip

- Separate thresholds from objectives. Meeting every threshold gives an acceptable design. Trade studies cover the range between threshold and objective.
- Read the notes under each table. A requirement without its weight and altitude cannot be checked.
- Mark anything the RFP leaves to you, such as the ferry cruise altitude. Your choice becomes an assumption and must be stated.
- Assignment A01 turns this RFP into stakeholder needs and system requirements. [](../lecture-01/requirements.md) explains how.
:::
