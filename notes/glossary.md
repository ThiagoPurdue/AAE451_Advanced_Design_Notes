---
title: Glossary
---

The notes use these terms in a fixed sense. In the text, a term with a dotted underline opens its definition.

:::{glossary}
Aspect ratio
: $AR = b^2/S$, the span squared over the wing area. High aspect ratio lowers the induced drag and raises the wing weight.

ASORT
: Authoritative source of truth. One parameter file that every script of the sizing code reads, so that no constant is duplicated in code.

Certification basis
: The airworthiness document and the sections of it that apply to the aircraft, against which compliance is shown. In this course the Navy Jet Trainer uses MIL-HDBK-516C.

Compliance matrix
: A table with one row per requirement: its threshold, its objective or target, and the current value of the design.

Compressibility drag
: $C_{D_c}$, the drag added by shock waves and shock-induced separation as the flight Mach number passes the critical Mach number.

Conceptual design
: Phase 1 of an aircraft program. It selects the configuration, sizes it, and shows that the requirements can be met. Its output is a feasible design.

Configuration
: The type, location, and count of each major component of the aircraft: wing, fuselage, engines, tail, and landing gear.

CONOPS
: Concept of operations. A description of how the system will be operated during its life-cycle phases to meet stakeholder expectations.

Critical field length
: The runway length at which, after an engine failure at the critical speed, continuing the takeoff and stopping take the same distance. Defined for the Navy Jet Trainer in MIL-STD-3013B.

Critical Mach number
: $M_{crit}$, the flight Mach number at which the flow first reaches sonic speed somewhere on the airfoil.

Datum
: The reference concept in a Pugh matrix. Every other concept is scored against it, criterion by criterion. At the first run it is often an existing aircraft.

Deck angle
: The pitch attitude of the fuselage on the approach, the angle of attack less the glide-slope angle. Flaps lower it; slats raise it.

Design mission
: The most demanding mission the aircraft must fly. The operating mission is the one it usually flies, and it is shorter. The RFP prescribes two missions and the briefs call each a design mission; which one sizes the fuel is known only after both are computed.

Drag count
: A drag coefficient of 0.0001.

Drag divergence Mach number
: $M_{dd}$, the Mach number at which the drag starts to rise steeply with Mach. Boeing: the section drag 0.002 above its incompressible value. Douglas: the slope $dC_d/dM$ reaching 0.10.

Drag polar
: The drag coefficient of an airfoil or aircraft against its lift coefficient, in one configuration at one Mach number.

Engine deck
: Thrust and fuel flow against altitude, speed, ambient temperature, and rating.

FCLP
: Field Carrier Landing Practice. Carrier approaches and landings flown to a land runway marked as a carrier deck.

Fixed engine
: An engine selected off the shelf, with known thrust and fuel flow, that does not change during sizing.

Flap
: A trailing-edge device that adds camber and, for the Fowler type, chord. It raises the maximum lift coefficient and lowers the stall angle.

Flat-plate area
: $f = C_{D_0} S_{ref}$, the parasite drag of an aircraft or a component written as an area with a drag coefficient of 1.

Form factor
: $FF$, the factor on skin friction drag that accounts for the pressure drag of a component.

Ground effect
: The drop in induced drag and the rise in lift of a wing close to the ground.

Induced drag
: $C_{D_i}$, the drag due to lift: $K C_L^2$ with $K = 1/(\pi\,AR\,e)$.

Interference factor
: $Q$, the factor on the drag of a component that accounts for the flow around its neighbors.

Mean geometric chord
: $c_{MGC}$, the chord-weighted mean chord, $(2/S)\int_0^{b/2} c^2\,dy$; for a trapezoidal wing it is the chord at the spanwise centroid of the half-wing. A04 calls it the mean aerodynamic chord. The subsonic aerodynamic center sits near its quarter chord.

Measure of merit
: A quantity used to rank concepts, such as life-cycle cost or takeoff weight. Trade studies report the change in a measure of merit.

Mission profile
: One mission drawn as altitude against distance or time, divided into numbered segments, each with a stated condition.

MLW
: Maximum landing weight. The highest weight at which the aircraft is allowed to land.

Morphological chart
: A table with one row per major arrangement choice and one column per option. One pick per row is a configuration.

MTOW
: Maximum takeoff weight. The highest weight at which the aircraft is allowed to take off.

Need
: What a stakeholder wants to be able to do, stated independently of any solution.

Objective
: The value of a requirement that the customer would like to reach. In the lecture example it is called the target.

Parasite drag
: $C_{D_0}$, the drag at zero lift: skin friction, form, interference, and the miscellaneous items.

PDR
: Preliminary Design Review. The review at the end of this course, where the converged conceptual design is judged against the requirements.

Performance condition
: A point requirement the RFP states at a weight, altitude, and day, outside the mission profiles.

Pugh matrix
: A selection matrix that scores each concept against a datum, criterion by criterion.

Rating
: A power setting the engine maker names, such as idle, maximum continuous, or takeoff.

Requirement
: An obligation on the system, written as "The system shall...", with a verification method.

Reynolds number
: $Re = \rho V l/\mu$, the ratio of inertial to viscous forces, on a reference length: the mean geometric chord for wing and airfoil data, the component length in the drag build-up.

RFP
: Request for proposal. The document in which a customer states what it needs and the limits a bidder's design must meet.

Rubber engine
: An engine that scales with the aircraft during sizing. It implies new engine development.

Skin friction coefficient
: $C_f$, the viscous drag of a surface per unit of wetted area and dynamic pressure.

Slat
: A leading-edge device that moves forward and down to open a slot ahead of the wing. It delays separation and raises both the maximum lift coefficient and the stall angle.

Span efficiency
: $e$, the ratio of the induced drag of an elliptic wing to the induced drag of the wing or aircraft at the same lift and aspect ratio.

Specific excess power
: The rate at which the aircraft can gain energy height, (T − D)V/W, in ft/s. It measures the thrust available beyond the drag at a given speed, altitude, and weight.

SRR
: System Requirements Review. The review at which the mission statement, the needs, and the requirements are baselined.

Stakeholder
: Anyone with an interest in the project: customers, operators, maintainers, investors, regulators, suppliers, and end users.

Taper ratio
: $\lambda = c_t/c_r$, the tip chord over the root chord.

Technology factor
: A factor applied to a regression result to account for a technology the database never saw, such as a composite structure.

Threshold
: The minimum acceptable value of a requirement. A design that meets every threshold is acceptable.

Trade study
: An analysis that changes one requirement or one assumption and measures the effect on the design, usually as a change in a measure of merit.

TRL
: Technology readiness level. A scale from 1, basic principles observed, to 9, proven in operation.

Waiver
: A written record of a change to a baselined requirement, with the reason for the change. Kept in the deck appendix.

Washout
: Twist that lowers the incidence of the tip relative to the root, so the stall starts inboard. Geometric washout of 1° to 4° is typical.

Weighted objectives
: A selection method that scores each concept against each objective and sums weight times score. The weights and the scores are both judgments, so the total can only shortlist.

Wetted area
: $S_{wet}$, the surface area of a component exposed to the flow.

Wing loading
: $W/S$, the weight per unit wing area, in lb/ft². With the takeoff weight it gives the wing area; with the maximum lift coefficient it gives the stall speed.
:::
