---
title: About these notes
short_title: About
---

These are the lecture notes for AAE 451 Advanced Aircraft Design in the School of Aeronautics and Astronautics at Purdue University. The course covers conceptual design and ends with a Preliminary Design Review. The instructor is Prof. Thiago Guimaraes.

The notes are written around one design problem: the AIAA 2026-27 Undergraduate Team Aircraft Design Competition request for proposal ({term}`RFP`), *Design of a Navy Jet Training Aircraft*.

::::{grid} 1 1 2 2

:::{card} Navy Jet Trainer RFP
:link: navy-rfp/navy-rfp.md
What the Navy asks for: performance, cockpit, missions, the analyses and data the proposal must contain, and how proposals are judged.
:::

:::{card} Lecture 1, part 1: The aircraft design process
:link: lecture-01/design-process.md
Phases of a program, what happens in conceptual design, the market and business case, the feasibility study, and the systems view.
:::

:::{card} Lecture 1, part 2: Needs, mission statement, and CONOPS
:link: lecture-01/needs-and-conops.md
Customer needs and stakeholders, the mission statement, the concept of operations, and the mission profile.
:::

:::{card} Lecture 1, part 3: Requirements
:link: lecture-01/requirements.md
SMART requirements, the tests for one requirement and for the set, the checklist, the compliance matrix, and trade studies.
:::

:::{card} Lecture 2, part 1: Starting from weight and the empty weight
:link: lecture-02/weight-estimation.md
Why takeoff weight comes first, the empty-weight trend lines and regression, how good they are, and fixed and rubber engines.
:::

:::{card} Lecture 2, part 2: The design mission, fuel weight, and the sizing loop
:link: lecture-02/mission-fuel.md
The design mission, the fuel weight fraction, historical segment fractions, the Breguet equations, and the sizing iteration.
:::

:::{card} Lecture 2, part 3: The sizing loop in MATLAB
:link: lecture-02/sizing-loop.ipynb
The sizing iteration run cell by cell on an invented small transport. The cells can be edited and rerun in the browser.
:::

:::{card} Lecture 2, part 4: Design missions and energy reserves
:link: lecture-02/design-missions.md
The two prescribed missions, which one sizes the fuel, point performance, what FCLP drives, and the seven questions each team answers before the SRR.
:::

:::{card} Lecture 3: Aircraft configuration
:link: lecture-03/configuration.md
Wing placement, fuselage cross-section, engine placement, tail and landing gear arrangements, the morphological chart, and the trainer cohort.
:::

:::{card} Lecture 4: Concept generation and selection
:link: lecture-04/concept-selection.md
Brainstorming, the morphological chart, Pugh's controlled convergence in ten steps, its limits, and weighted objectives.
:::

:::{card} Lecture 5, part 1: The airfoil
:link: lecture-05/airfoil.md
What the RFP asks of the wing, the airfoil families, reading section data, Reynolds and Mach effects, stall classes, and the comparison that selects an airfoil.
:::

:::{card} Lecture 5, part 2: Wing geometry and lift
:link: lecture-05/wing-geometry-and-lift.md
Planform, wing volume and height, aspect ratio, taper, sweep and drag divergence, twist, incidence, the lift-curve slope, clean maximum lift, and stall speed.
:::

:::{card} Lecture 6, part 1: High lift, requirements and devices
:link: lecture-06/high-lift-devices.md
The RFP field lengths and their MIL-STD-3013B definitions, what high lift does, the trailing-edge and leading-edge devices, their increments, and how to select a system.
:::

:::{card} Lecture 6, part 2: High lift, the wing and the field length
:link: lecture-06/high-lift-wing-and-field.md
Partial-span flaps, the partition method, trim and deck angle, the FCLP approach, the drag penalty, climb, the takeoff and landing segments, and the required maximum lift.
:::

:::{card} Lecture 7, part 1: Parasite drag
:link: lecture-07/parasite-drag.md
The three types of drag, the parasite drag build-up, skin friction and transition, wetted area, form and interference factors, miscellaneous drag, and the SR22 example.
:::

:::{card} Lecture 7, part 2: Drag due to lift and the polar
:link: lecture-07/drag-polar.md
Span efficiency, the SR22 polar, the polar at high lift, ground effect, compressibility drag, the three polars, and the checks against existing aircraft.
:::

:::{card} Lecture 8, part 1: Engine selection
:link: lecture-08/engine-selection.md
What the RFP asks of the propulsion model, where each engine class operates, propulsive efficiency, published engine data, and the number and location of the engines.
:::

:::{card} Lecture 8, part 2: Engine models and the engine deck
:link: lecture-08/engine-models.md
The thrust lapse, TSFC with altitude and Mach number, a published engine deck, installed performance, thrust sizing, rubber-engine scaling, and the engine trade.
:::

:::{card} Lecture 8, part 3: Inlet, nozzle, and the design sequence
:link: lecture-08/engine-integration.md
The capture area, pressure recovery, the diffuser, the nozzle, and the propulsion design sequence.
:::

:::{card} Lecture 9, part 1: The master equation
:link: lecture-09/constraint-method.md
The constraint diagram, energy height and specific excess power, the master equation and its cases, the field and stall boundaries, and how to read the diagram.
:::

:::{card} Lecture 9, part 2: The trainer boundaries and the design point
:link: lecture-09/trainer-boundaries.md
The RFP requirements as boundaries, the threshold and the objective, the choice of the design point, rubber and fixed engines, and the loop with the sizing code.
:::

:::{card} Lecture 9, part 3: Worked examples
:link: lecture-09/constraint-examples.md
The Cessna 162 of Gudmundsson's Example 3-1 and the T-45C, with their inputs and the values to reproduce.
:::

:::{card} Lecture 10, part 1: The method and the center of gravity
:link: lecture-10/cg-and-envelope.md
What the RFP asks, the eight steps of the method, the symbols, the CG table, and the CG envelope.
:::

:::{card} Lecture 10, part 2: Longitudinal stability and the tail
:link: lecture-10/longitudinal-stability.md
The pitching moment about the CG, the neutral point and the static margin, the scissor plot, and the tail geometry and incidence.
:::

:::{card} Lecture 10, part 3: Trim
:link: lecture-10/trim.md
The trim equations, the elevator derivatives, the trim diagram, trim with thrust, the conditions to check, and the trim drag.
:::

:::{card} Lecture 10, part 4: Lateral-directional stability and controls
:link: lecture-10/lateral-and-controls.md
The fin and its three checks, the dihedral, the control surfaces and the roll requirement, and the check with a vortex-lattice tool.
:::

:::{card} Assignment A01: RFP breakdown and system requirements
:link: assignments/a01.md
The first assignment: deconstruct the RFP, write the needs, the concept of operations, and the requirements, and trace them together.
:::

:::{card} Assignment A02: Aircraft sizing and certification requirements
:link: assignments/a02.md
The second assignment: the certification basis, the team aircraft database, the empty-weight trend, the first takeoff-weight estimate, and the AI use record.
:::

:::{card} Assignment A03: Sizing II, configuration selection and mission analysis
:link: assignments/a03.md
The third assignment: the refined sizing, the morphological chart and the Pugh selection, the mission analysis, and the SRR baseline.
:::

:::{card} Assignment A04: Airfoil, wing geometry, high lift and initial layout
:link: assignments/a04.md
The fourth assignment: the airfoil selection, the wing geometry, the high-lift estimate, the first dimensioned layout and loft, and the SRR action items.
:::

:::{card} Assignment A05: Propulsion selection and installed engine deck
:link: assignments/a05.md
The fifth assignment: propulsion requirements and engine class, candidates and selection, the installed engine deck in the sizing code, and the inlet.
:::

::::

More lectures will be added during the semester.

## How the notes are organized

Each lecture is one chapter. A chapter follows the slides shown in class and adds the explanation given in the room. Figures and tables from the slides are included. Diagrams were redrawn for the web so their text stays sharp at any zoom level. Each figure has alt text for screen readers.

## Boxes used in the notes

The notes use eight kinds of box. Each has one meaning.

:::{admonition} Navy Jet Trainer
:class: navy

Connects the lecture to the RFP. It points to the RFP sections that matter and to the questions your team has to answer. It does not give design answers. The configuration, the engine, and the design point are your team's decisions.
:::

:::{prf:definition} Example of a definition box
:label: def-sample

Defines a term the course uses in a fixed sense. The [glossary](glossary.md) collects these terms. In the text, a term with a dotted underline opens its definition.
:::

:::{exercise} Example of an exercise box
:label: ex-sample

A question to work through with your RFP. It is not graded. The assignment briefs on Brightspace state what is.
:::

:::{tip}
A working method, or a habit that saves rework later.
:::

:::{warning}
A common mistake, and how to avoid it.
:::

:::{note} What to take from this lecture
Three or four points the lecture is about.
:::

:::{important} Summary
The lecture's summary, or on an assignment page, its dates and what to submit.
:::

:::{seealso}
A reading, a resource, or the lecture page that teaches a method.
:::

## Using the notes with the assignments

The notes explain methods. The assignment briefs on Brightspace state what to submit and when. Where the two differ, the brief governs.

## Source and corrections

The notes are written in MyST Markdown and built with Jupyter Book 2. The source is on [GitHub](https://github.com/ThiagoPurdue/AAE451_Advanced_Design_Notes). Report an error by opening an issue there or by contacting the instructor through Brightspace.

The accessibility of this site is described in [](accessibility.md).
