---
title: Requirements
short_title: Requirements
---

This is the third part of Lecture 1. It covers how to write a requirement, how to test one, how a set of requirements is checked, and how aerospace customers state requirements through an RFP.

## Writing a requirement

A requirement is written as "The system shall..." and states one obligation. A good requirement is **SMART**:

Specific
: One obligation, stated without ambiguity, with the condition under which it applies. State what must be true, not how it will be achieved.

Measurable
: A quantity with units, or a condition that is plainly met or not met.

Achievable
: Possible within the limits of the RFP. A requirement no design can meet is an error in the requirement.

Relevant
: It answers a stakeholder need. A requirement that answers no need is either unnecessary or a sign that a need is missing.

Traceable
: It carries its source and rationale, and it leads to the evidence that will show it is met.

The lecture slide spells SMART as simple, measurable, attainable, realistic and time-bound. That version comes from goal setting, where T is time-bound. For requirements this course uses specific, measurable, achievable, relevant and traceable, as in assignment A01.

Compare two requirements from the slide:

> The system shall provide a means of communication between the transport and the dispatch station to exchange health and status data of the transport system, exchanged every 15 minutes.

This one is good. It names the two ends of the link, the data exchanged and a rate that a test can check.

> The system shall be able to operate in all weather.

This one is poor. "All weather" has no limit, so no test can show it is met. It also uses "be able to", which the checklist below rejects. A better version states the conditions: wind, visibility, icing, temperature and precipitation, each with a value.

## Testing each requirement

Each requirement is tested on its own:

1. Is it traceable to a user need or an operational requirement?
2. Is it redundant with another requirement?
3. Is it consistent with the other requirements?
4. Is it unambiguous, and not open to interpretation?
5. Is it technologically feasible?
6. Is it affordable?
7. Is it verifiable?

## Testing the set

The set of requirements is then tested as a whole:

1. Does the set cover all the user needs and operational requirements?
2. Is the set feasible in cost, schedule and technology?
3. Can the set be verified as a whole?

A set can fail even when every requirement in it passes. Two feasible requirements can be infeasible together, for example a short field length, a high cruise speed and a low unit cost.

## Checklist: is this a requirement?

{numref}`tbl-goodness-checklist` is the checklist from the lecture, after Ulrich and Eppinger (2000).

:::{table} Checklist for a well-written requirement.
:label: tbl-goodness-checklist

| Check | What to look for |
|---|---|
| Dependent | The requirement depends on a need and traces to it |
| Verifiable | A test, analysis, demonstration or inspection can show it is met |
| Free of ambiguous terms | No "as appropriate", "etc.", "and/or", "support", "but not limited to", "be able to", "be capable of" |
| Free of indefinite pronouns | No "this" or "these" without a clear subject |
| Free of unverifiable terms | No "flexible", "user-friendly", "robust", "lightweight", "maximize", "adequate", "small", "portable", "easily", or other words ending in -ly or -ize |
| Free of implementation | It states what is needed, not how to provide it. State the problem, not the solution |
| Necessary | Ask why the requirement is needed. The answer may lead to the real requirement |
| Free of descriptions of operations | Ask whether the developer controls it, and whether it is a need the product must satisfy or an activity involving the product |
| Free of TBDs | Avoid "to be determined". Use a best estimate marked TBR, to be resolved, with its rationale |
:::

:::{admonition} Navy Jet Trainer
:class: note

Apply the checklist to the RFP itself. Read these three sentences from it:

- "The cockpit shall accommodate two Martin Baker Mk 14 ejection seats, or similar."
- "Maximum cockpit altitude shall be no greater than 8000 ft."
- "Advanced materials may be used to reduce the empty weight of the aircraft."

Which one is a verifiable requirement as written? Which one contains an ambiguous term, and what would your team have to decide to remove it? Which one is not a requirement at all? The customer writes the RFP for bidders, and not every sentence in it is a requirement.
:::

## Setting requirements for aerospace systems

You show that your aircraft meets the customer's needs by showing that it meets the requirements. Customers such as the Department of Defense and NASA have traditionally stated their needs in a request for proposal (RFP). The RFP gives the requirements, and the bidders propose designs that meet them.

The lecture recommends the video [System engineering requirements: aircraft system development process](https://www.youtube.com/watch?v=3afHlAwBudM), a talk from the EASA Rotorcraft and VTOL Symposium 2019. It shows how requirements are organized from the aircraft down to the functional elements.

### Requirements compliance matrix

A compliance matrix lists each requirement with its threshold, its target and the current value of the design. {numref}`tbl-compliance-example` is the example from the lecture, a small general aviation aircraft. The status column is added here so the result does not depend on color.

:::{table} Example requirements compliance matrix. A threshold is the minimum acceptable value and a target is the desired value.
:label: tbl-compliance-example

| Requirement | Unit | Threshold | Target | Current value | Status |
|---|---|---|---|---|---|
| Seats | count | 4 | 6 | 4 | Meets threshold |
| Sizing mission range | nmi | 250 | 300 | 250 | Meets threshold |
| Takeoff field length over a 50 ft obstacle | ft | 2,500 | 2,000 | 2,750 | Does not meet threshold |
| Noise limit | dBA | 85 | 80 | 90 | Does not meet threshold |
| Landing field length over a 50 ft obstacle | ft | 2,500 | 2,000 | 2,250 | Meets threshold |
| Nominal mission total flight time | min | 45 | 40 | 45 | Meets threshold |
:::

Read the matrix row by row. For seats and range a larger value is better. For field lengths, noise and flight time a smaller value is better. This design meets four thresholds, fails two and meets no target. The takeoff field length and the noise are the next design problems.

:::{admonition} Navy Jet Trainer
:class: note

The RFP uses threshold and objective instead of threshold and target. Keep a compliance matrix from the start of the semester. Its rows are the RFP requirements in [](../navy-rfp/navy-rfp.md#tbl-rfp-performance) and the requirements your team writes. Update the current values each time the design changes. At the Preliminary Design Review the design is judged against this matrix.
:::

### A database of similar aircraft

Build a database of existing aircraft similar to yours. It shows what has been achieved, and it gives the statistics used in initial sizing. {numref}`tbl-comparator-example` is the lecture example, a set of very light jets.

:::{table} Example database of very light jets, values as shown on the lecture slide. MTOW is maximum takeoff weight, OEW is operating empty weight and PAX is the number of passengers.
:label: tbl-comparator-example

| Aircraft | Crew | PAX | MTOW (kg) | OEW (kg) | Cruise speed (km/h) | Range (km) | Engines and rated thrust |
|---|---|---|---|---|---|---|---|
| Adam A700 AdamJet | 1 | 5 | 4,250 | 2,523 | 610 | 2,340 | 2 × FJ33-4A, 6.0 kN each |
| Cessna Citation Mustang | 1 | 5 | 3,930 | 2,522 | 630 | 2,160 | 2 × PW615F, 6.5 kN each |
| Cirrus Vision SF50 | 1 | 5 | 2,727 | 1,681 | 550 | 2,000 | 1 × FJ33-5A, 8.4 kN |
| Diamond D-Jet | 1 | 4 | 2,320 | 1,175 | 583 | 2,500 | 1 × FJ33-5A, 8.4 kN |
| Eclipse 500 | 1 | 4 | 2,700 | 1,610 | 685 | 2,080 | 2 × PW610F, 4 kN each |
| Embraer Phenom 100 | 1 | 5 | 4,750 | 3,235 | 710 | 2,180 | 2 × PW617F, 7.2 kN each |
| Honda HA-420 HondaJet | 1 | 5 | 4,170 | 2,427 | 778 | 2,185 | 2 × HF120, 9.2 kN each |
:::

Record the source of every value in the database. Manufacturer brochures, type certificate data sheets and Jane's often give different values for the same aircraft. Note which one you used.

:::{admonition} Navy Jet Trainer
:class: note

For the Navy trainer, the database holds jet trainers that are in service or in development, starting with the T-45 the RFP names. Use the same columns where they apply. Add the columns your RFP makes important, such as maximum operating Mach number and sustained load factor.
:::

## Initial requirements trade studies

A requirements trade study changes one requirement and measures the effect on the size, weight and cost of the aircraft. Payload, range and speed have a large effect on takeoff weight, total fuel and cost. Run these trades early, while the customer can still change the requirements. This is the loop through the customer in [](design-process.md#fig-design-process-flow).

:::{admonition} Navy Jet Trainer
:class: note

The RFP asks for design and cost trade studies between the threshold and objective values. Three requirements have both:

- Maximum operating speed, Mach 0.78 and Mach 0.90.
- Specific excess power, 90 ft/s and 125 ft/s.
- Sustained load factor, +4.0 g and +6.0 g.

Each objective has a cost in weight and in money. The trade study shows that cost to the customer.
:::

## Reading

- Kossiakoff, A., Biemer, S. M., Seymour, S. J., and Flanigan, D. A., *Systems Engineering Principles and Practice*, 3rd ed., Wiley, 2020, Chapter 6.
- Raymer, D. P., *Aircraft Design: A Conceptual Approach*, 6th ed., AIAA Education Series, 2018, Chapters 1 and 2.
- Sadraey, M. H., *Aircraft Design: A Systems Engineering Approach*, Wiley, 2012, Chapter 2.

## References

- Ulrich, K. T., and Eppinger, S. D., *Product Design and Development*, 2nd ed., McGraw-Hill, 2000.
